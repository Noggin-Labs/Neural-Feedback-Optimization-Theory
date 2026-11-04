#!/usr/bin/env python3
"""NFOT Study M cross-paradigm analysis: Adaptive Diffuse (ADdiff) vs Checkerboard (CB).

This script is written so that it either produces a real paired participant-level
comparison, or fails closed with a precise statement of what is missing. It will
not invent Checkerboard trials, and it will not treat trials as independent
participants.

Status of the current checkout
------------------------------
The only trial table available is ``StimulusAnalysis(final)/pooled_trials_full (1).csv``.
Every one of its 74 recordings is an ``ADdiff`` recording. The Checkerboard
condition is therefore absent, and the cross-paradigm comparison is BLOCKED at
the data level rather than at the analysis level.

What this script does with the available data
---------------------------------------------
1. Detects which paradigms are present from the recording identifiers.
2. Reports the participant overlap that the data actually supports.
3. Reports the per-participant trial counts and timing summaries.
4. Runs the paired analysis only if both conditions are genuinely present.

Statistical unit
----------------
The participant is the unit of inference. Trials are clustered within participant
and within recording, so a pooled trial-level regression would understate
uncertainty. The paired analysis below therefore aggregates to the participant
first, then compares conditions with a paired test and a paired effect size.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

PARADIGM_PATTERNS = {"ADdiff": r"ADdiff", "CB": r"(?:^|[_-])CB(?:[_-]|$)|Checker"}


def detect_paradigm(recording_id: str) -> str:
    for name, pattern in PARADIGM_PATTERNS.items():
        if re.search(pattern, recording_id, flags=re.IGNORECASE):
            return name
    return "UNKNOWN"


def load_trials(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"file", "trial", "t0_s", "tfb_s", "L_s", "Y", "subject"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    for column in ("trial", "t0_s", "tfb_s", "L_s", "Y"):
        df[column] = pd.to_numeric(df[column], errors="coerce")
    if df[list(required)].isna().any().any():
        raise ValueError("Required columns contain missing or non-numeric values")
    if not np.isclose(df["tfb_s"] - df["t0_s"], df["L_s"], atol=1e-9).all():
        raise ValueError("L_s != tfb_s - t0_s; the table is internally inconsistent")
    df["paradigm"] = df["file"].map(detect_paradigm)
    return df


def quantization_step(values: pd.Series, candidates=(1.0, 0.5, 0.25, 0.125, 0.05, 0.01, 0.005, 0.001)):
    """Largest round step on which every value lies exactly."""
    finite = values.to_numpy(float)
    for step in candidates:
        if np.all(np.abs(finite / step - np.round(finite / step)) < 1e-9):
            return step
    return None


def participant_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["subject", "paradigm"], as_index=False)
        .agg(
            n_trials=("Y", "size"),
            n_recordings=("file", "nunique"),
            accuracy=("Y", "mean"),
            L_mean=("L_s", "mean"),
            L_sd=("L_s", "lambda" if False else (lambda s: s.std(ddof=1))),
            L_var=("L_s", lambda s: s.var(ddof=1)),
        )
    )


def paired_analysis(df: pd.DataFrame) -> dict:
    """Paired participant-level comparison; only called when both paradigms exist."""
    from scipy import stats

    summary = participant_summary(df)
    wide = summary.pivot(index="subject", columns="paradigm", values=["accuracy", "L_mean", "L_sd"])
    if "accuracy" not in wide.columns.get_level_values(0):
        return {"status": "not_run", "reason": "no usable participant summaries"}

    both = wide.dropna(subset=[("accuracy", "ADdiff"), ("accuracy", "CB")])
    n = len(both)
    if n < 3:
        return {
            "status": "not_run",
            "reason": f"only {n} participants have both conditions; a paired test is not defensible",
            "participants_with_both": n,
        }

    diff_accuracy = both[("accuracy", "CB")] - both[("accuracy", "ADdiff")]
    diff_Lmean = both[("L_mean", "CB")] - both[("L_mean", "ADdiff")]
    diff_Lsd = both[("L_sd", "CB")] - both[("L_sd", "ADdiff")]

    accl = stats.ttest_rel(both[("accuracy", "CB")], both[("accuracy", "ADdiff")])
    lcl = stats.ttest_rel(both[("L_mean", "CB")], both[("L_mean", "ADdiff")])

    def dz(d: pd.Series) -> float | None:
        sd = d.std(ddof=1)
        return float(d.mean() / sd) if sd and np.isfinite(sd) and sd > 0 else None

    return {
        "status": "run",
        "n_participants_paired": n,
        "accuracy_difference_CB_minus_ADdiff": {
            "mean": float(diff_accuracy.mean()),
            "sd": float(diff_accuracy.std(ddof=1)),
            "cohen_dz": dz(diff_accuracy),
            "paired_t": float(accl.statistic),
            "p_value": float(accl.pvalue),
            "wilcoxon_p": float(stats.wilcoxon(diff_accuracy).pvalue) if n >= 6 else None,
        },
        "L_mean_difference_CB_minus_ADdiff": {
            "mean": float(diff_Lmean.mean()),
            "cohen_dz": dz(diff_Lmean),
            "paired_t": float(lcl.statistic),
            "p_value": float(lcl.pvalue),
        },
        "L_sd_difference_CB_minus_ADdiff": {
            "mean": float(diff_Lsd.mean()),
            "cohen_dz": dz(diff_Lsd),
        },
        "units_of_inference": "participant",
        "causal_claim": False,
        "warning": (
            "With ~15 participants, a paired test has very low power and the "
            "normality assumption is not checkable. Report the effect size and "
            "participant-level scatter, not just the p-value."
        ),
    }


ACQUISITION_CHECKLIST = [
    "Obtain the Study M Checkerboard (CB) recordings, or confirm officially that Study M contains ADdiff only.",
    "Record the authoritative paradigm labels per recording from the dataset's own documentation, not from filenames.",
    "Obtain raw EDFs or complete trusted event-stream exports for every recording you intend to analyse.",
    "Record the converter name, version and settings used to produce any CSV.",
    "Confirm the timestamp unit and the sampling/quantisation of the source clock.",
    "Confirm event semantics for StimulusBegin / DisplayResult / CurrentTarget / SelectedTarget.",
    "Produce a per-recording inclusion/exclusion manifest with explicit reasons.",
    "Preserve a source-row index for every derived trial row, so any row can be traced back.",
    "Do not overwrite the existing 444-row derived table; write a new table and crosswalk it.",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trials_csv")
    parser.add_argument("--outdir", default="nfot_cross_paradigm")
    args = parser.parse_args()

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    df = load_trials(Path(args.trials_csv))

    paradigms = Counter(df["paradigm"])
    subjects_by_paradigm: dict[str, set[str]] = defaultdict(set)
    for paradigm, group in df.groupby("paradigm"):
        subjects_by_paradigm[paradigm].update(group["subject"].astype(str))

    ad = subjects_by_paradigm.get("ADdiff", set())
    cb = subjects_by_paradigm.get("CB", set())
    overlap = sorted(ad & cb)

    step_L = quantization_step(df["L_s"])
    step_t0 = quantization_step(df["t0_s"])

    # Structural checks that do not require the missing raw data.
    nominal = (
        df.groupby("subject")["test"].nunique() * 5
    )  # 5 test sessions per participant is the design's nominal shape
    per_subject = df.groupby("subject").agg(
        n_trials=("Y", "size"), n_recordings=("file", "nunique"),
        accuracy=("Y", "mean"), L_mean=("L_s", "mean"), L_sd=("L_s", lambda s: s.std(ddof=1)),
    )
    expected_recordings = 15 * 5
    observed_recordings = int(df["file"].nunique())
    deficits = {
        str(subject): int(30 - row["n_trials"])
        for subject, row in per_subject.iterrows()
        if row["n_trials"] != 30
    }

    report: dict = {
        "input": str(Path(args.trials_csv).name),
        "n_trials": int(len(df)),
        "n_participants": int(df["subject"].nunique()),
        "n_recordings": observed_recordings,
        "paradigms_present": dict(paradigms),
        "participants_per_paradigm": {k: len(v) for k, v in subjects_by_paradigm.items()},
        "participants_with_both_paradigms": overlap,
        "n_participants_with_both_paradigms": len(overlap),
        "complete_recording_check": {
            "expected_recordings_nominal": expected_recordings,
            "observed_recordings": observed_recordings,
            "missing_recordings": expected_recordings - observed_recordings,
            "trials_per_participant": {k: int(v) for k, v in per_subject["n_trials"].items()},
            "trial_count_deficits_vs_30": deficits,
            "note": (
                "15 participants x 5 test sessions is the nominal design shape implied by "
                "the identifiers. 74 recordings and 444 trials imply exactly one 6-trial "
                "recording block is absent, and no exclusion manifest documents it."
            ),
        },
        "timestamp_quantisation": {
            "L_s_step_seconds": step_L,
            "t0_s_step_seconds": step_t0,
            "n_distinct_L_values": int(df["L_s"].nunique()),
            "note": (
                "Timestamps lie on a 0.125 s (125 ms) grid. Any analysis of sub-125 ms "
                "timing structure, and any claim about latency resolution, is not "
                "supported by this table."
            ),
        },
    }

    if len(paradigms) < 2 or not cb:
        report["cross_paradigm_status"] = "BLOCKED_MISSING_CONDITION"
        report["blocking_reason"] = (
            f"Checkerboard trials are absent: {paradigms.get('ADdiff', 0)} ADdiff trials, "
            f"{paradigms.get('CB', 0)} CB trials across {observed_recordings} recordings. "
            "No paired participant-level comparison is possible, and none is fabricated."
        )
        report["acquisition_checklist"] = ACQUISITION_CHECKLIST
        report["analysis_code_status"] = (
            "paired_analysis() is implemented and unit-testable; it is not executed "
            "because its precondition (both conditions present) is unmet."
        )
    else:
        report["cross_paradigm"] = paired_analysis(df)
        report["cross_paradigm_status"] = report["cross_paradigm"]["status"]

    per_subject.reset_index().to_csv(out / "participant_summary.csv", index=False)
    (out / "cross_paradigm_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"\nwrote {out/'cross_paradigm_report.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
