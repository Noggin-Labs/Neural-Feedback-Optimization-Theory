"""Guarded event-based extraction for bigP3BCI CSV exports.

This implementation is intentionally conservative: it requires explicit time
units and source-export confirmation, uses documented event columns, and never
uses StimulusType as a character label.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

DATA_DICTIONARY_URL = "https://physionet.org/content/bigp3bci/1.0.0/bigP3BCI-data/"
GRID_SIZE = 72


class ExtractionError(ValueError):
    """Input signals do not support unambiguous extraction."""


@dataclass(frozen=True)
class ExtractionConfig:
    time_unit: str = "seconds"
    grid_size: int = GRID_SIZE
    target_column: str = "CurrentTarget"
    selected_column: str = "SelectedTarget"
    phase_column: str = "PhaseInSequence"
    stimulus_column: str = "StimulusBegin"
    feedback_column: str = "DisplayResult"

    def __post_init__(self) -> None:
        if self.time_unit not in {"seconds", "milliseconds"}:
            raise ValueError("time_unit must be 'seconds' or 'milliseconds'.")
        if self.grid_size < 2:
            raise ValueError("grid_size must be >= 2.")


def _clean_headers(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = pd.Index(out.columns.astype(str)).str.replace(
        r"\s*\([^)]*\)", "", regex=True
    ).str.strip()
    if out.columns.duplicated().any():
        raise ExtractionError("Duplicate column names after header cleaning.")
    if "DisplayResult" in out and "DisplayResults" in out:
        raise ExtractionError("Both DisplayResult and DisplayResults are present.")
    if "DisplayResults" in out:
        out = out.rename(columns={"DisplayResults": "DisplayResult"})
    return out


def load_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.is_file():
        raise ExtractionError(f"Input CSV does not exist: {path}")
    try:
        df = pd.read_csv(path, low_memory=False)
    except Exception as exc:
        raise ExtractionError(f"Could not read CSV {path}: {exc}") from exc
    if df.empty:
        raise ExtractionError("Input CSV is empty.")
    return _clean_headers(df).reset_index(drop=True)


def _numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col not in out:
            raise ExtractionError(f"Missing required column: {col}")
        out[col] = pd.to_numeric(out[col], errors="coerce")
        if out[col].isna().any() or not np.isfinite(out[col]).all():
            raise ExtractionError(f"Column {col} contains invalid numeric values.")
    return out


def _rising_edges(values: pd.Series) -> np.ndarray:
    arr = values.to_numpy()
    return np.flatnonzero((arr[1:] == 1) & (arr[:-1] == 0)) + 1


def _cell_parts(value: int, grid_size: int) -> tuple[int, int]:
    if value < 1 or value > grid_size:
        return 0, 0
    return (value - 1) // 8 + 1, (value - 1) % 8 + 1


def _subject_metadata(path: Path) -> dict[str, str]:
    stem = path.stem
    match = re.match(r"(?P<subject>M_\d+)_(?P<session>[^_]+)_(?P<test>.+)", stem)
    if not match:
        return {"subject": "unknown", "session": "unknown", "test": stem}
    return match.groupdict()


def extract_trials_from_frame(df: pd.DataFrame, config: ExtractionConfig, source_name: str = "input.csv") -> pd.DataFrame:
    required = [config.phase_column, config.stimulus_column, config.feedback_column,
                config.target_column, config.selected_column]
    work = _numeric(df, required)
    phase = work[config.phase_column]
    stimulus = work[config.stimulus_column]
    feedback = work[config.feedback_column]
    if not set(phase.unique()).issubset({0, 1, 2, 3}):
        raise ExtractionError("PhaseInSequence contains values outside 0,1,2,3.")
    starts = _rising_edges(stimulus)
    feedback_edges = _rising_edges(feedback)
    feedback_edges = feedback_edges[phase.iloc[feedback_edges].to_numpy() == 3]
    if not len(starts) or not len(feedback_edges):
        raise ExtractionError("No stimulus or feedback rising edges found.")
    rows: list[dict[str, Any]] = []
    scale = 1.0 if config.time_unit == "seconds" else 0.001
    for trial_id, fb_idx in enumerate(feedback_edges):
        prior_starts = starts[(starts < fb_idx) & (phase.iloc[starts].to_numpy() == 2)]
        if len(prior_starts) == 0:
            continue
        t0_idx = int(prior_starts[-1])
        next_fb = feedback_edges[feedback_edges > fb_idx]
        boundary = int(next_fb[0]) if len(next_fb) else len(work)
        target_values = work.loc[t0_idx:fb_idx, config.target_column]
        target_values = target_values[target_values > 0].unique()
        if len(target_values) != 1:
            continue
        selected_values = work.loc[fb_idx:min(boundary - 1, fb_idx + 1), config.selected_column]
        selected_values = selected_values[selected_values > 0].unique()
        if len(selected_values) != 1:
            continue
        target = int(target_values[0])
        selected = int(selected_values[0])
        t0 = float(t0_idx) * scale
        tfb = float(fb_idx) * scale
        gap = tfb - t0
        if gap <= 0:
            continue
        row, col = _cell_parts(selected, config.grid_size)
        rows.append({
            "source_file": source_name, "source_t0_row": t0_idx,
            "source_tfb_row": int(fb_idx), "trial": trial_id,
            "t0_s": t0, "tfb_s": tfb, "L_s": gap,
            "selected_cell": selected, "selected_row": row,
            "selected_col": col, "true_target": target,
            "Y": int(selected == target),
        })
    if not rows:
        raise ExtractionError("No complete, uniquely labelled trials were extracted.")
    return pd.DataFrame(rows)


def extract_trials_from_file(path: str | Path, config: ExtractionConfig) -> pd.DataFrame:
    path = Path(path)
    result = extract_trials_from_frame(load_csv(path), config, path.name)
    for key, value in _subject_metadata(path).items():
        result[key] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--time-unit", required=True, choices=["seconds", "milliseconds"])
    parser.add_argument("--confirm-studyM-export", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("extracted_trials.csv"))
    parser.add_argument("--manifest", type=Path, default=Path("extraction_manifest.json"))
    args = parser.parse_args()
    if not args.confirm_studyM_export:
        parser.error("Pass --confirm-studyM-export only after source-export audit.")
    try:
        config = ExtractionConfig(time_unit=args.time_unit)
        result = extract_trials_from_file(args.csv, config)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(args.output, index=False)
        args.manifest.write_text(json.dumps({"config": asdict(config), "source": str(args.csv), "rows": len(result), "dictionary_url": DATA_DICTIONARY_URL}, indent=2) + "\n", encoding="utf-8")
        print(f"Extracted {len(result)} trials to {args.output}")
        return 0
    except (ExtractionError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
