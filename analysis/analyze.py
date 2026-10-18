
#!/usr/bin/env python3
"""
NFOT exploratory analysis with leakage and data-integrity safeguards.

Expected CSV columns:
    participant_id : participant identifier
    recording_id   : recording/session identifier
    L              : Write-Back Gap in seconds
    Y              : binary outcome (0 or 1)
    trial          : optional trial-order column

IMPORTANT:
- This script does not establish that the source labels are correct.
- Verify target reconstruction and event timestamps before analysis.
- Results are exploratory, not causal evidence.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


REQUIRED = {"participant_id", "recording_id", "L", "Y"}


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}. "
            "Map the real dataset schema explicitly; do not guess."
        )

    df = df.copy()
    df["L"] = pd.to_numeric(df["L"], errors="coerce")
    df["Y"] = pd.to_numeric(df["Y"], errors="coerce")

    if df[["participant_id", "recording_id"]].isna().any().any():
        raise ValueError("Participant and recording IDs cannot be missing.")

    if df[["L", "Y"]].isna().any().any():
        raise ValueError(
            "L or Y contains missing/non-numeric values. "
            "Investigate them before deciding how to handle them."
        )

    if not np.isfinite(df["L"]).all():
        raise ValueError("L contains infinite values.")

    if (df["L"] < 0).any():
        raise ValueError("Negative L values found; audit timestamps.")

    if not set(df["Y"].unique()).issubset({0, 1}):
        raise ValueError("Y must contain only verified binary labels 0 and 1.")

    if df["Y"].nunique() != 2:
        raise ValueError("Both outcome classes are required.")

    # Never silently treat file order as chronological order when a
    # trial-order column is available.
    if "trial" not in df.columns:
        raise ValueError(
            "Missing trial-order column. Add a verified chronological "
            "'trial' column before computing rolling features."
        )

    df["trial"] = pd.to_numeric(df["trial"], errors="raise")

    if df.duplicated(["recording_id", "trial"]).any():
        raise ValueError(
            "Duplicate recording_id/trial pairs found. "
            "Resolve duplicate or ambiguous trial ordering."
        )

    return df.sort_values(
        ["recording_id", "trial"], kind="stable"
    ).reset_index(drop=True)


def add_past_only_variance(
    df: pd.DataFrame, window: int = 5, min_periods: int = 2
) -> pd.DataFrame:
    """Variance of earlier L values in the same recording only."""
    if window < 2:
        raise ValueError("window must be at least 2.")
    if min_periods < 2 or min_periods > window:
        raise ValueError("min_periods must be between 2 and window.")

    result = df.copy()
    result["L_prior_var"] = (
        result.groupby("recording_id", sort=False)["L"]
        .transform(
            lambda s: s.shift(1).rolling(
                window=window, min_periods=min_periods
            ).var()
        )
    )
    return result


def within_participant_center(
    df: pd.DataFrame, column: str
) -> pd.Series:
    """Center a feature around each participant's observed mean."""
    return df[column] - df.groupby("participant_id")[column].transform("mean")


def grouped_auc(
    X: pd.DataFrame, y: pd.Series, groups: pd.Series
) -> dict:
    """Out-of-participant predictions; report pooled AUC and fold coverage."""
    n_groups = groups.nunique()
    if n_groups < 3:
        raise ValueError(
            "At least 3 distinct participants are required for grouped CV."
        )

    splitter = GroupKFold(n_splits=min(5, n_groups))
    predictions = np.full(len(y), np.nan)
    fold_results = []

    for train_idx, test_idx in splitter.split(X, y, groups):
        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]

        if y_train.nunique() != 2:
            fold_results.append({"status": "skipped", "reason": "one training class"})
            continue

        if y_test.nunique() != 2:
            fold_results.append({"status": "skipped", "reason": "one test class"})
            continue

        model = make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            LogisticRegression(max_iter=2000, random_state=0),
        )
        model.fit(X.iloc[train_idx], y_train)
        predictions[test_idx] = model.predict_proba(X.iloc[test_idx])[:, 1]

        fold_results.append({
            "status": "evaluated",
            "test_participants": int(groups.iloc[test_idx].nunique()),
            "test_trials": int(len(test_idx)),
            "auc": float(
                roc_auc_score(y_test, predictions[test_idx])
            ),
        })

    valid = np.isfinite(predictions)
    if valid.sum() == 0 or y.iloc[np.flatnonzero(valid)].nunique() != 2:
        raise ValueError(
            "No valid pooled AUC could be calculated. "
            "Inspect class balance and participant-level fold composition."
        )

    return {
        "pooled_auc": float(
            roc_auc_score(y.iloc[np.flatnonzero(valid)], predictions[valid])
        ),
        "evaluated_trials": int(valid.sum()),
        "total_trials": int(len(y)),
        "folds": fold_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path, help="Verified analysis CSV")
    parser.add_argument(
        "--labels-verified",
        action="store_true",
        help="Confirm that Y is a correctly reconstructed outcome label",
    )
    parser.add_argument(
        "--output", type=Path, default=Path("nfot_analysis_report.json")
    )
    args = parser.parse_args()

    if not args.labels_verified:
        parser.error(
            "Refusing to analyze unverified labels. Audit target/event "
            "reconstruction, then pass --labels-verified."
        )

    df = add_past_only_variance(load_data(args.csv))

    # Use the identical complete-case sample and identical folds for both
    # models. No missing rolling variance is filled using future trials.
    sample = df.dropna(subset=["L_prior_var"]).copy().reset_index(drop=True)

    if sample.empty:
        raise ValueError("No rows have enough prior trials for rolling variance.")

    sample["L_within"] = within_participant_center(sample, "L")
    sample["L_prior_var_within"] = within_participant_center(
        sample, "L_prior_var"
    )

    X_base = sample[["L_within"]]
    X_augmented = sample[["L_within", "L_prior_var_within"]]
    y = sample["Y"]
    groups = sample["participant_id"]

    # Both models use the same sample and deterministic grouped-fold rule.
    baseline = grouped_auc(X_base, y, groups)
    augmented = grouped_auc(X_augmented, y, groups)

    report = {
        "status": "exploratory",
        "causal_claim": False,
        "n_trials": int(len(sample)),
        "n_participants": int(groups.nunique()),
        "n_recordings": int(sample["recording_id"].nunique()),
        "outcome_accuracy": float(y.mean()),
        "rolling_feature": (
            "sample variance of up to five prior L values, "
            "within the same recording"
        ),
        "baseline_model": ["L_within"],
        "augmented_model": ["L_within", "L_prior_var_within"],
        "baseline": baseline,
        "augmented": augmented,
        "auc_difference": float(
            augmented["pooled_auc"] - baseline["pooled_auc"]
        ),
        "interpretation_warning": (
            "AUC differences alone do not establish statistical significance, "
            "causality, or generalization beyond this dataset. Use paired "
            "participant-level uncertainty estimates for formal comparisons."
        ),
    }

    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print(f"\nSaved report to: {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
