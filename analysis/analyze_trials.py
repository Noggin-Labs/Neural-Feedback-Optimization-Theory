#!/usr/bin/env python3
"""Auditable descriptive analysis of an NFOT derived trial table.

This script does not validate event semantics or reproduce the original v5
extraction. It accepts only a table whose provenance has been separately
reviewed and reports what can be recomputed from the supplied columns.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED = {
    "file", "trial", "t0_s", "tfb_s", "L_s", "Y", "subject",
}


class AnalysisError(ValueError):
    """Raised when the supplied table cannot support this analysis."""


def read_trials(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.is_file():
        raise AnalysisError(f"Input file does not exist: {path}")
    try:
        df = pd.read_csv(path)
    except Exception as exc:
        raise AnalysisError(f"Could not read CSV: {exc}") from exc
    missing = REQUIRED - set(df.columns)
    if missing:
        raise AnalysisError(f"Missing required columns: {sorted(missing)}")
    out = df.copy()
    for col in ["trial", "t0_s", "tfb_s", "L_s", "Y"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    if out[list(REQUIRED)].isna().any().any():
        raise AnalysisError("Required columns contain missing or non-numeric values.")
    if not np.isfinite(out[["t0_s", "tfb_s", "L_s", "Y"]].to_numpy()).all():
        raise AnalysisError("Required numeric columns contain non-finite values.")
    if not set(out["Y"].unique()).issubset({0, 1}):
        raise AnalysisError("Y must contain only 0 and 1.")
    if (out["L_s"] < 0).any() or (out["tfb_s"] < out["t0_s"]).any():
        raise AnalysisError("Negative or reversed timing intervals found.")
    if not np.isclose(out["tfb_s"] - out["t0_s"], out["L_s"], atol=1e-12).all():
        raise AnalysisError("L_s does not equal tfb_s - t0_s for every row.")
    if out.duplicated(["file", "trial"]).any():
        raise AnalysisError("Duplicate file/trial identifiers found.")
    return out.sort_values(["subject", "file", "trial"], kind="stable").reset_index(drop=True)


def _pearson(x: pd.Series, y: pd.Series) -> float | None:
    if len(x) < 2 or x.nunique() < 2 or y.nunique() < 2:
        return None
    return float(np.corrcoef(x.to_numpy(float), y.to_numpy(float))[0, 1])


def run_analysis(df: pd.DataFrame, outdir: str | Path) -> dict:
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    participant = (
        df.groupby("subject", as_index=False)
        .agg(n_trials=("Y", "size"), accuracy=("Y", "mean"),
             L_mean=("L_s", "mean"), L_sd=("L_s", lambda s: s.std(ddof=1)))
    )
    correlations = []
    for subject, group in df.groupby("subject", sort=True):
        centered_l = group["L_s"] - group["L_s"].mean()
        correlations.append({
            "subject": str(subject),
            "n_trials": int(len(group)),
            "within_subject_pearson_L_Y": _pearson(centered_l, group["Y"]),
        })
    report = {
        "analysis_version": "NFOT-v6-available-derived-table-1.0",
        "status": "descriptive_reanalysis_of_derived_table",
        "input_rows": int(len(df)),
        "n_subjects": int(df["subject"].nunique()),
        "n_files": int(df["file"].nunique()),
        "accuracy": float(df["Y"].mean()),
        "correct_count": int(df["Y"].sum()),
        "L_mean_seconds": float(df["L_s"].mean()),
        "L_sd_seconds": float(df["L_s"].std(ddof=1)),
        "L_min_seconds": float(df["L_s"].min()),
        "L_median_seconds": float(df["L_s"].median()),
        "L_max_seconds": float(df["L_s"].max()),
        "participant_summary_path": str(outdir / "participant_summary.csv"),
        "participant_correlations": correlations,
        "claims_not_reproduced": [
            "The original extraction from EDF or converted source files.",
            "The reported within-participant beta and p-value.",
            "The reported LOSO slope-direction result.",
            "The reported AUC values and confidence interval.",
            "Any causal or mechanistic claim.",
        ],
        "interpretation": (
            "These calculations describe the supplied derived table only. "
            "They do not establish event semantics, label validity, causality, "
            "or independent replication of v5."
        ),
    }
    participant.to_csv(outdir / "participant_summary.csv", index=False)
    (outdir / "analysis_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trials_csv")
    parser.add_argument("--outdir", default="nfot_v6_analysis")
    args = parser.parse_args()
    try:
        report = run_analysis(read_trials(args.trials_csv), args.outdir)
    except (AnalysisError, OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
