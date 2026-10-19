
"""
extract.py
-----------
Guarded trial-level extraction for bigP3BCI Study M, ADdiff.

Output:
    trial, t0, tfb, L, SelectedTarget, Target, Y, file

IMPORTANT:
    The legacy event and target mappings must be independently verified
    before analysis-ready labels can be generated.

    This implementation preserves the legacy event definitions as explicit,
    configurable hypotheses. Passing the checks below does NOT itself prove
    that those definitions match the dataset's ground truth.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class ExtractionConfig:
    # Set these to True ONLY after independent verification.
    flash_mapping_verified: bool = False
    selection_mapping_verified: bool = False
    target_mapping_verified: bool = False
    trial_pairing_verified: bool = False
    timestamp_units_verified: bool = False

    # These settings encode the legacy hypotheses.
    target_column: str = "StimulusType"
    flash_phase_value: float = 1.0
    no_selection_value: float = 0.0

    # Maximum allowed distance between the feedback timestamp and the
    # row used to sample the target. Set based on documented sampling
    # semantics and the recording's sampling frequency.
    max_target_sample_distance_seconds: float = 0.1

    # Require timestamps to be nondecreasing. Duplicate timestamps are
    # permitted, but ambiguous target sampling will be rejected.
    require_nondecreasing_time: bool = True


REQUIRED_COLUMNS = {
    "Time",
    "PhaseInSequence",
    "SelectedTarget",
}


class ExtractionError(ValueError):
    """Raised when the input cannot be safely extracted."""


# ---------------------------------------------------------------------
# Input loading and validation
# ---------------------------------------------------------------------

def load_and_clean(filepath: str | Path) -> pd.DataFrame:
    """Load a CSV and remove type suffixes from column names."""
    path = Path(filepath)

    if not path.is_file():
        raise ExtractionError(f"Input file does not exist: {path}")

    df = pd.read_csv(path, low_memory=False)

    if df.empty:
        raise ExtractionError(f"Input CSV is empty: {path}")

    # Remove suffixes such as " (bool)", " (int)", and " (uV)".
    df.columns = df.columns.str.replace(
        r"\s*\([^)]*\)", "", regex=True
    ).str.strip()

    duplicated = df.columns[df.columns.duplicated()].tolist()
    if duplicated:
        raise ExtractionError(
            f"Duplicate column names after cleaning: {duplicated}"
        )

    return df


def validate_config(config: ExtractionConfig) -> None:
    """Block extraction unless every required mapping is verified."""
    checks = {
        "flash event mapping": config.flash_mapping_verified,
        "selection event mapping": config.selection_mapping_verified,
        "target label mapping": config.target_mapping_verified,
        "trial pairing rule": config.trial_pairing_verified,
        "timestamp units": config.timestamp_units_verified,
    }

    unverified = [name for name, passed in checks.items() if not passed]

    if unverified:
        raise ExtractionError(
            "Extraction blocked. Independently verify and explicitly "
            "enable these configuration checks: "
            + ", ".join(unverified)
        )

    if config.max_target_sample_distance_seconds <= 0:
        raise ExtractionError(
            "max_target_sample_distance_seconds must be positive."
        )


def validate_dataframe(
    df: pd.DataFrame,
    config: ExtractionConfig,
) -> pd.DataFrame:
    """Validate required columns, timestamps, and numeric event fields."""
    required = REQUIRED_COLUMNS | {config.target_column}
    missing = sorted(required - set(df.columns))

    if missing:
        raise ExtractionError(f"Missing required columns: {missing}")

    out = df.copy()

    for column in ("Time", "PhaseInSequence", "SelectedTarget"):
        out[column] = pd.to_numeric(out[column], errors="coerce")

    # Target labels must also be numeric character indices under this
    # implementation. Adapt only if the documented schema says otherwise.
    out[config.target_column] = pd.to_numeric(
        out[config.target_column], errors="coerce"
    )

    if out["Time"].isna().any():
        bad_rows = out.index[out["Time"].isna()].tolist()[:10]
        raise ExtractionError(
            f"Time contains missing/non-numeric values. "
            f"Example row indices: {bad_rows}"
        )

    if not np.isfinite(out["Time"].to_numpy(dtype=float)).all():
        raise ExtractionError("Time contains infinite values.")

    if config.require_nondecreasing_time:
        time_values = out["Time"].to_numpy(dtype=float)
        if np.any(np.diff(time_values) < 0):
            raise ExtractionError(
                "Time is not nondecreasing. Check row order before extraction."
            )

    for column in ("PhaseInSequence", "SelectedTarget"):
        if out[column].isna().any():
            raise ExtractionError(
                f"{column} contains missing/non-numeric values."
            )

    return out


# ---------------------------------------------------------------------
# Event detection
# ---------------------------------------------------------------------

def detect_events(
    df: pd.DataFrame,
    config: ExtractionConfig,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detect events using the configured legacy hypotheses.

    Flash:
        PhaseInSequence enters flash_phase_value from another value.

    Selection:
        SelectedTarget becomes nonzero and differs from the previous row.

    These event definitions are valid only if verified against the
    dataset's documented event semantics.
    """
    phase = df["PhaseInSequence"]
    selected = df["SelectedTarget"]

    previous_phase = phase.shift(1)
    previous_selected = selected.shift(1)

    # The first row is NOT automatically treated as a flash onset.
    flash_start = (
        phase.eq(config.flash_phase_value)
        & previous_phase.notna()
        & previous_phase.ne(config.flash_phase_value)
    )

    selection_event = (
        selected.ne(config.no_selection_value)
        & previous_selected.notna()
        & selected.ne(previous_selected)
    )

    flashes = (
        df.loc[flash_start, ["Time"]]
        .rename(columns={"Time": "t0_candidate"})
        .reset_index(drop=True)
    )

    selections = (
        df.loc[selection_event, ["Time", "SelectedTarget"]]
        .rename(columns={"Time": "tfb"})
        .reset_index(drop=True)
    )

    if flashes.empty:
        raise ExtractionError(
            "No flash starts detected. Verify the flash-event mapping."
        )

    if selections.empty:
        raise ExtractionError(
            "No selection events detected. Verify the selection-event mapping."
        )

    return flashes, selections


# ---------------------------------------------------------------------
# Target sampling
# ---------------------------------------------------------------------

def sample_target(
    df: pd.DataFrame,
    feedback_time: float,
    config: ExtractionConfig,
) -> float:
    """
    Sample the target column at the nearest recorded timestamp.

    This strategy is retained from the legacy implementation and must
    be independently justified by the dataset's event documentation.
    """
    times = df["Time"].to_numpy(dtype=float)
    distances = np.abs(times - feedback_time)
    minimum_distance = float(distances.min())

    if minimum_distance > config.max_target_sample_distance_seconds:
        raise ExtractionError(
            f"No row is close enough to feedback time {feedback_time:.6f}s. "
            f"Nearest distance: {minimum_distance:.6f}s."
        )

    candidates = np.flatnonzero(
        np.isclose(
            distances,
            minimum_distance,
            rtol=0.0,
            atol=1e-12,
        )
    )

    # If tied timestamps carry different target values, do not guess.
    candidate_targets = (
        df.iloc[candidates][config.target_column]
        .dropna()
        .unique()
    )

    if len(candidate_targets) != 1:
        raise ExtractionError(
            f"Target sampling is ambiguous at feedback time "
            f"{feedback_time:.6f}s."
        )

    target = candidate_targets[0]

    if not np.isfinite(float(target)):
        raise ExtractionError(
            f"Invalid target value at feedback time {feedback_time:.6f}s."
        )

    return float(target)


# ---------------------------------------------------------------------
# Trial extraction
# ---------------------------------------------------------------------

def extract_trials_from_file(
    filepath: str | Path,
    config: ExtractionConfig,
) -> pd.DataFrame:
    """
    Extract candidate (L, Y) pairs after the required mappings are verified.

    Pairing rule:
        For each selection, choose the earliest detected flash strictly
        after the previous selection and strictly before the current one.

    This pairing rule is an explicit assumption, not a universal definition
    of a BCI trial.
    """
    validate_config(config)

    df = load_and_clean(filepath)
    df = validate_dataframe(df, config)

    flashes, selections = detect_events(df, config)

    flash_times = flashes["t0_candidate"].to_numpy(dtype=float)
    selection_times = selections["tfb"].to_numpy(dtype=float)

    if np.any(np.diff(selection_times) < 0):
        raise ExtractionError("Selection timestamps are not ordered.")

    records = []
    skipped_no_flash = []

    for i, selection in selections.iterrows():
        tfb = float(selection["tfb"])
        selected_target = float(selection["SelectedTarget"])

        previous_feedback = (
            float(selections.iloc[i - 1]["tfb"]) if i > 0 else -np.inf
        )

        # Strict interval: previous selection < flash < current selection.
        candidate_indices = np.flatnonzero(
            (flash_times > previous_feedback)
            & (flash_times < tfb)
        )

        if len(candidate_indices) == 0:
            skipped_no_flash.append(i)
            continue

        # Legacy pairing hypothesis: use the earliest flash in the interval.
        t0 = float(flash_times[candidate_indices[0]])

        if tfb <= t0:
            raise ExtractionError(
                f"Nonpositive interval for selection {i}: t0={t0}, tfb={tfb}"
            )

        target = sample_target(df, tfb, config)
        gap = tfb - t0

        # Both indices are numeric character identifiers in this version.
        correct = int(selected_target == target)

        records.append({
            "trial": len(records),
            "source_selection_index": int(i),
            "t0": t0,
            "tfb": tfb,
            "L": gap,
            "SelectedTarget": selected_target,
            "Target": target,
            "Y": correct,
        })

    if not records:
        raise ExtractionError(
            "No trials could be extracted. Review the event mappings "
            "and trial-pairing rule."
        )

    result = pd.DataFrame.from_records(records)
    result["file"] = Path(filepath).name

    # Final integrity checks.
    if not np.isfinite(result[["t0", "tfb", "L"]].to_numpy()).all():
        raise ExtractionError("Output contains non-finite timestamps or gaps.")

    if (result["L"] <= 0).any():
        raise ExtractionError("Output contains nonpositive Write-Back Gaps.")

    if not result["Y"].isin([0, 1]).all():
        raise ExtractionError("Output contains invalid correctness labels.")

    if skipped_no_flash:
        print(
            f"[warning] {len(skipped_no_flash)} selection event(s) had no "
            "detected flash in their pairing window. They were excluded. "
            f"First source indices: {skipped_no_flash[:10]}",
            file=sys.stderr,
        )

    return result


# ---------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Guarded bigP3BCI trial-level extractor."
    )
    parser.add_argument("csv", help="Path to one converted recording CSV.")
    parser.add_argument(
        "--config",
        help=(
            "Optional JSON file containing explicitly verified extraction "
            "settings. All verification flags default to False."
        ),
    )
    parser.add_argument(
        "--output",
        help="Optional output CSV path. No file is written unless extraction succeeds.",
    )
    args = parser.parse_args()

    try:
        if args.config:
            with open(args.config, "r", encoding="utf-8") as handle:
                raw_config = json.load(handle)
            config = ExtractionConfig(**raw_config)
        else:
            config = ExtractionConfig()

        result = extract_trials_from_file(args.csv, config)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            result.to_csv(output_path, index=False, float_format="%.10g")
            print(f"Saved {len(result)} rows to {output_path}")
        else:
            print(result.to_string(index=False))

        print(f"\nExtracted trials: {len(result)}")
        print(f"L mean: {result['L'].mean():.6f} seconds")
        print(f"L std:  {result['L'].std():.6f} seconds")
        print(f"Y distribution: {result['Y'].value_counts().to_dict()}")

        return 0

    except (ExtractionError, OSError, ValueError, TypeError) as exc:
        print(f"[ERROR] Extraction refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
