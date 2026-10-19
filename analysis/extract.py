"""Guarded, event-based trial extraction for bigP3BCI Study M ADdiff CSVs.

Operational mapping follows the public bigP3BCI v1.0.0 data dictionary:
- PhaseInSequence: 0 pre-run, 1 pre-trial, 2 during trial, 3 post-trial
- StimulusBegin: 0 off, 1 on
- StimulusType: binary target/non-target stimulus indicator (NOT a character ID)
- CurrentTarget: target character index during phase 2
- SelectedTarget: predicted character index during phase 3
- DisplayResult: feedback-presented marker during phase 3

The CSV export's timing units and Study-M-specific signal behavior still need
spot-checking against a raw recording / converter. CLI extraction therefore
requires explicit --time-unit and --confirm-studyM-export arguments. This
script fails closed on ambiguous trial segmentation or labels.
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

DATA_DICTIONARY_URL = (
    "https://physionet.org/content/bigp3bci/1.0.0/bigP3BCI-data/"
)
GRID_SIZE = 72  # Study M uses a 9 x 8 character grid.


class ExtractionError(ValueError):
    """Input signals do not support unambiguous trial-level extraction."""


@dataclass(frozen=True)
class ExtractionConfig:
    time_unit: str = "seconds"  # Explicitly selected by the caller.
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
    out.columns = (
        pd.Index(out.columns.astype(str))
        .str.replace(r"\s*\([^)]*\)", "", regex=True)
        .str.strip()
    )
    duplicated = out.columns[out.columns.duplicated()].tolist()
    if duplicated:
        raise ExtractionError(
            f"Duplicate column names after suffix removal: {duplicated}"
        )

    # The official data dictionary uses DisplayResult (singular). Some local
    # exports / analysis code have used DisplayResults (plural); accept either,
    # but never silently choose if both are present.
    has_singular = "DisplayResult" in out.columns
    has_plural = "DisplayResults" in out.columns
    if has_singular and has_plural:
        raise ExtractionError(
            "Both DisplayResult and DisplayResults columns exist; resolve the alias explicitly."
        )
    if has_plural:
        out = out.rename(columns={"DisplayResults": "DisplayResult"})
    return out


def load_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.is_file():
        raise ExtractionError(f"Input file does not exist: {path}")
    try:
        df = pd.read_csv(path, low_memory=False)
    except Exception as exc:  # preserve a clear CLI error
        raise ExtractionError(f"Could not read CSV {path}: {exc}") from exc
    if df.empty:
        raise ExtractionError("Input CSV is empty.")
    return _clean_headers(df).reset_index(drop=True)


def _numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
