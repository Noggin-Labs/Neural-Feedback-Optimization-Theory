
#!/usr/bin/env python3
"""
NFOT v5 — Write-Back Gap Integrity Audit
========================================

Audits trial-level data for consistency with the NFOT definition:

    L = t_fb - t0

where:
    t0  = the prespecified starting event
    tfb = the prespecified feedback-display event

This script checks data integrity and timing definitions.
It does NOT independently reproduce every v5 statistical result.

Usage:
    python analysis/audit_v5.py path/to/trials.csv

Optional:
    python analysis/audit_v5.py path/to/trials.csv \
        --output-dir audit_results \
        --participant-col participant_id \
        --t0-col t0 \
        --feedback-col tfb \
        --gap-col L_s

Dependencies:
    pip install pandas numpy
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ALIASES = {
    "participant": [
        "participant_id", "participant", "subject_id",
        "subject", "participant_code"
    ],
    "t0": [
        "t0", "t0_s", "stimulus_time_s",
        "stimulus_begin", "StimulusBegin"
    ],
    "feedback": [
        "tfb", "t_fb", "feedback_time_s",
        "displayresults", "DisplayResults"
    ],
    "gap": [
        "L", "L_s", "write_back_gap_s",
        "writeback_gap_s"
    ],
    "outcome": [
        "correct", "accuracy", "response_correct", "Y"
    ],
}


def find_column(df, explicit, aliases, required=False):
    """Find a column without silently inventing missing measurements."""
    if explicit:
        if explicit not in df.columns:
            raise ValueError(
                f"Requested column {explicit!r} was not found. "
                f"Available columns: {list(df.columns)}"
            )
        return explicit

    lookup = {str(c).casefold(): c for c in df.columns}

    for alias in aliases:
        if alias.casefold() in lookup:
            return lookup[alias.casefold()]

    if required:
        raise ValueError(
            f"Could not identify a required column. "
            f"Tried aliases: {aliases}. "
            f"Available columns: {list(df.columns)}"
        )

    return None


def numeric(series):
    """Convert values to numbers; invalid values become NaN."""
    return pd.to_numeric(series, errors="coerce")


def audit(df, args):
    participant_col = find_column(
        df, args.participant_col, ALIASES["participant"]
    )
    t0_col = find_column(
        df, args.t0_col, ALIASES["t0"], required=True
    )
    feedback_col = find_column(
        df, args.feedback_col, ALIASES["feedback"], required=True
    )
    gap_col = find_column(
        df, args.gap_col, ALIASES["gap"]
    )
    outcome_col = find_column(
        df, args.outcome_col, ALIASES["outcome"]
    )

    work = df.copy()

    work["_t0"] = numeric(work[t0_col])
    work["_tfb"] = numeric(work[feedback_col])
    work["_L_recomputed"] = work["_tfb"] - work["_t0"]

    # Preserve original rows so every flagged trial can be inspected.
    work["_row_number"] = np.arange(2, len(work) + 2)

    valid_times = (
        work["_t0"].notna()
        & work["_tfb"].notna()
        & np.isfinite(work["_t0"])
        & np.isfinite(work["_tfb"])
    )

    negative_gap = (
        valid_times & (work["_L_recomputed"] < 0)
    )

    report = {
        "audit_name": "NFOT v5 Write-Back Gap Integrity Audit",
        "input_rows": int(len(work)),
        "columns": {
            "participant": participant_col,
            "t0": t0_col,
            "feedback": feedback_col,
            "reported_gap": gap_col,
            "outcome": outcome_col,
        },
        "definition": "L = tfb - t0",
        "valid_timestamp_rows": int(valid_times.sum()),
        "invalid_timestamp_rows": int((~valid_times).sum()),
        "negative_gap_rows": int(negative_gap.sum()),
        "reported_gap_comparison": None,
        "outcome_summary": None,
        "limitations": [
            "Column names alone do not establish event semantics.",
            "Confirm that t0 and tfb match the prespecified v5 events.",
            "This audit does not establish causality.",
            "This audit does not reproduce all reported v5 statistics.",
        ],
    }

    if valid_times.any():
        gaps = work.loc[valid_times, "_L_recomputed"]

        report["recomputed_gap_seconds"] = {
            "count": int(gaps.count()),
            "mean": float(gaps.mean()),
            "std_sample": (
                float(gaps.std(ddof=1))
                if len(gaps) > 1 else None
            ),
            "min": float(gaps.min()),
            "median": float(gaps.median()),
            "max": float(gaps.max()),
        }

    if gap_col is not None:
        work["_L_reported"] = numeric(work[gap_col])

        comparable = (
            valid_times
            & work["_L_reported"].notna()
            & np.isfinite(work["_L_reported"])
        )

        if comparable.any():
            difference = (
                work.loc[comparable, "_L_reported"]
                - work.loc[comparable, "_L_recomputed"]
            )

            tolerance = args.tolerance_s
            mismatches = difference.abs() > tolerance

            report["reported_gap_comparison"] = {
                "comparable_rows": int(comparable.sum()),
                "mismatch_rows": int(mismatches.sum()),
                "tolerance_seconds": tolerance,
                "max_absolute_difference_seconds": float(
                    difference.abs().max()
                ),
                "mean_signed_difference_seconds": float(
                    difference.mean()
                ),
            }

            work["_gap_mismatch"] = False
            work.loc[comparable, "_gap_mismatch"] = mismatches

    if participant_col is not None:
        report["participant_summary"] = {
            "unique_nonmissing_participants": int(
                work[participant_col].nunique(dropna=True)
            ),
            "missing_participant_rows": int(
                work[participant_col].isna().sum()
            ),
        }

    if outcome_col is not None:
        y = numeric(work[outcome_col])
        observed = y.dropna()

        report["outcome_summary"] = {
            "nonmissing_rows": int(observed.size),
            "unique_values": sorted(
                observed.unique().tolist()
            ),
            "mean": (
                float(observed.mean())
                if observed.size else None
            ),
        }

        if not observed.empty:
            values = set(observed.unique())
            if not values.issubset({0, 1}):
                report["outcome_summary"][
                    "warning"
                ] = (
                    "Outcome is not strictly binary 0/1. "
                    "Verify its coding before modeling."
                )

    flagged = (
        (~valid_times)
        | negative_gap
    )

    if "_gap_mismatch" in work.columns:
        flagged |= work["_gap_mismatch"]

    audit_columns = [
        "_row_number", t0_col, feedback_col,
        "_L_recomputed"
    ]

    if participant_col is not None:
        audit_columns.insert(1, participant_col)

    if gap_col is not None:
        audit_columns.append(gap_col)

    flagged_rows = work.loc[flagged, audit_columns].copy()

    return report, work, flagged_rows


def main():
    parser = argparse.ArgumentParser(
        description="Audit NFOT v5 trial-level timing integrity."
    )
    parser.add_argument("csv", type=Path)
    parser.add_argument(
        "--output-dir", type=Path, default=Path("audit_results")
    )
    parser.add_argument("--participant-col")
    parser.add_argument("--t0-col")
    parser.add_argument("--feedback-col")
    parser.add_argument("--gap-col")
    parser.add_argument("--outcome-col")
    parser.add_argument(
        "--tolerance-s",
        type=float,
        default=0.001,
        help="Allowed absolute difference between reported and "
             "recomputed gap, in seconds (default: 0.001)."
    )

    args = parser.parse_args()

    if args.tolerance_s < 0:
        parser.error("--tolerance-s must be nonnegative")

    if not args.csv.is_file():
        parser.error(f"Input file does not exist: {args.csv}")

    try:
        df = pd.read_csv(args.csv)
        report, work, flagged = audit(df, args)

        args.output_dir.mkdir(parents=True, exist_ok=True)

        report_path = args.output_dir / "timing_audit.json"
        flagged_path = args.output_dir / "flagged_rows.csv"
        recomputed_path = args.output_dir / "recomputed_trials.csv"

        report_path.write_text(
            json.dumps(report, indent=2, allow_nan=False),
            encoding="utf-8",
        )
        flagged.to_csv(flagged_path, index=False)

        output = work.copy()
        output.to_csv(recomputed_path, index=False)

        print("\nNFOT v5 — TIMING INTEGRITY AUDIT")
        print("=" * 38)
        print(f"Input rows: {report['input_rows']}")
        print(
            "Valid timestamp rows: "
            f"{report['valid_timestamp_rows']}"
        )
        print(
            "Invalid timestamp rows: "
            f"{report['invalid_timestamp_rows']}"
        )
        print(
            "Negative gaps: "
            f"{report['negative_gap_rows']}"
        )

        comparison = report["reported_gap_comparison"]
        if comparison is not None:
            print(
                "Reported/recomputed mismatches: "
                f"{comparison['mismatch_rows']} / "
                f"{comparison['comparable_rows']}"
            )

        print(f"\nReport: {report_path}")
        print(f"Flagged rows: {flagged_path}")
        print(f"Recomputed data: {recomputed_path}")

        print(
            "\nIMPORTANT: A clean timing audit does not prove "
            "that the selected columns represent the intended "
            "NFOT events. Verify event semantics against the "
            "original extraction pipeline."
        )

    except (ValueError, OSError, pd.errors.ParserError) as exc:
        print(f"Audit failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
