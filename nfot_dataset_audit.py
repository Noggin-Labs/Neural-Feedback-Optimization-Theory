
"""
NFOT Independent Dataset Eligibility Audit
==========================================

Purpose:
    Inspect CSV and TSV files before attempting an independent
    validation of the Neural Feedback Optimization Theory.

This script does NOT:
    - Infer causality from observational data.
    - Assume event names have verified meanings.
    - Claim that a dataset independently replicates NFOT.
    - Modify the original dataset.

Usage:
    python nfot_dataset_audit.py /path/to/dataset

Dependency:
    pip install pandas
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


TABLE_EXTENSIONS = {".csv", ".tsv"}

TIME_TOKENS = (
    "time", "timestamp", "latency", "onset", "duration"
)

EVENT_TOKENS = (
    "event", "marker", "trigger", "stimulus",
    "feedback", "response", "target", "result"
)

OUTCOME_TOKENS = (
    "correct", "accuracy", "outcome", "selected",
    "target", "error", "success"
)

PARTICIPANT_TOKENS = (
    "participant", "subject", "sub_id", "session"
)

TRIAL_TOKENS = ("trial", "epoch", "sequence")


def classify_column(name: str) -> list[str]:
    """Identify column names worth inspecting, not their true meaning."""
    normalized = name.lower().replace("-", "_").replace(" ", "_")
    categories = []

    if any(token in normalized for token in TIME_TOKENS):
        categories.append("possible_time")

    if any(token in normalized for token in EVENT_TOKENS):
        categories.append("possible_event")

    if any(token in normalized for token in OUTCOME_TOKENS):
        categories.append("possible_outcome")

    if any(token in normalized for token in PARTICIPANT_TOKENS):
        categories.append("possible_participant")

    if any(token in normalized for token in TRIAL_TOKENS):
        categories.append("possible_trial")

    return categories


def inspect_file(path: Path, root: Path) -> dict:
    """Read a table and return a structural audit."""
    relative_path = str(path.relative_to(root))

    result = {
        "file": relative_path,
        "readable": False,
        "rows": None,
        "columns": [],
        "candidate_columns": {},
        "warnings": [],
    }

    try:
        separator = "\t" if path.suffix.lower() == ".tsv" else ","

        # Read as strings to avoid silently changing event codes or IDs.
        frame = pd.read_csv(
            path,
            sep=separator,
            dtype=str,
            low_memory=False,
            on_bad_lines="error",
        )

        result["readable"] = True
        result["rows"] = len(frame)
        result["columns"] = list(frame.columns)

        for column in frame.columns:
            categories = classify_column(column)
            if categories:
                result["candidate_columns"][column] = categories

        if frame.empty:
            result["warnings"].append("Table contains no data rows.")

        if frame.columns.duplicated().any():
            result["warnings"].append(
                "Duplicate column names detected."
            )

        if not result["candidate_columns"]:
            result["warnings"].append(
                "No obvious candidate columns found by name."
            )

    except Exception as exc:
        result["warnings"].append(
            f"Could not read file: {type(exc).__name__}: {exc}"
        )

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit tables for potential NFOT validation."
    )
    parser.add_argument(
        "dataset",
        type=Path,
        help="Path to a dataset directory or a single CSV/TSV file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("nfot_dataset_audit.json"),
        help="Path for the JSON audit report.",
    )
    args = parser.parse_args()

    source = args.dataset.expanduser().resolve()

    if source.is_file():
        files = [source] if source.suffix.lower() in TABLE_EXTENSIONS else []
        root = source.parent
    elif source.is_dir():
        root = source
        files = sorted(
            path
            for path in source.rglob("*")
            if path.is_file()
            and path.suffix.lower() in TABLE_EXTENSIONS
        )
    else:
        parser.error("Dataset path does not exist.")

    if not files:
        parser.error("No CSV or TSV files were found.")

    print("\nNFOT INDEPENDENT DATASET AUDIT")
    print("=" * 42)
    print(f"Dataset: {source}")
    print(f"Tables found: {len(files)}")
    print("\nNo scientific conclusions will be inferred automatically.\n")

    reports = []

    for path in files:
        report = inspect_file(path, root)
        reports.append(report)

        print(f"FILE: {report['file']}")
        print(f"Readable: {report['readable']}")
        print(f"Rows: {report['rows']}")

        if report["columns"]:
            print("Columns:")
            for column in report["columns"]:
                categories = report["candidate_columns"].get(
                    column, []
                )
                suffix = f"  [{', '.join(categories)}]" if categories else ""
                print(f"  - {column}{suffix}")

        for warning in report["warnings"]:
            print(f"WARNING: {warning}")

        print()

    audit = {
        "audit_version": "1.0.0",
        "purpose": "Structural eligibility screening only",
        "dataset_path": str(source),
        "tables_found": len(files),
        "readable_tables": sum(r["readable"] for r in reports),
        "files": reports,
        "scientific_status": "NOT_EVALUATED",
        "next_step": (
            "Verify event semantics, timestamp units, trial matching, "
            "feedback completion, outcome definitions, and data provenance "
            "before specifying any validation analysis."
        ),
    }

    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(audit, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 42)
    print(f"Audit report saved to: {output}")
    print("Scientific eligibility: NOT YET DETERMINED")
    print("\nNext: inspect the event definitions and data documentation.")


if __name__ == "__main__":
    main()
