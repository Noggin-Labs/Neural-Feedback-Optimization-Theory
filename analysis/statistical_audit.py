#!/usr/bin/env python3
"""NFOT independent statistical audit of the supplied 444-row derived table.

Purpose: quantify how much of the reported inferential story is recoverable, and how
sensitive any within-participant association is to the properties this audit
discovered (125 ms timestamp quantisation, one missing recording block, 15
participants).

Everything produced here is EXPLORATORY. The original inferential analysis cannot be
reproduced because the raw EDFs, the original code, and the original prediction
outputs are absent. This script does not replace it and must not be cited as its
replication.

Statistical unit
----------------
The participant is the inference unit. Trials are clustered within participant, so
any standard error that treats 444 trials as independent is wrong by roughly the
cluster size. Where a trial-level model is fitted, the variance is cluster-robust
(CR1) by participant with G-1 degrees of freedom.

What is computed
----------------
1. Within-participant association: OLS of Y on participant-centred L, cluster-robust
   SE, plus a per-participant slope summary.
2. Between-participant association: participant accuracy regressed on participant
   mean L (n = 15), reported as exploratory only.
3. Leave-one-participant-out sign stability of the within-participant slope.
4. AUC: leave-one-participant-out cross-validation, baseline (centred L) versus
   augmented (centred L + prior-trial variance), on identical folds and rows.
5. AUC uncertainty: cluster bootstrap over participants.
6. Quantisation sensitivity: recompute 1 and 4 after coarsening L to 0.25 s and
   0.5 s grids.
7. Missing-recording sensitivity: recompute without participant M_19.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in ("trial", "t0_s", "tfb_s", "L_s", "Y", "n_flashes"):
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if df[["L_s", "Y", "subject"]].isna().any().any():
        raise ValueError("L_s, Y or subject contains missing values")
    if not np.isclose(df["tfb_s"] - df["t0_s"], df["L_s"], atol=1e-9).all():
        raise ValueError("L_s != tfb_s - t0_s")
    return df.sort_values(["subject", "file", "trial"]).reset_index(drop=True)


def centre_by_participant(df: pd.DataFrame, column: str) -> pd.Series:
    return df[column] - df.groupby("subject")[column].transform("mean")


def add_prior_variance(df: pd.DataFrame, window: int = 5, min_periods: int = 2) -> pd.DataFrame:
    out = df.copy()
    out["L_prior_var"] = (
        out.groupby("file", sort=False)["L_s"]
        .transform(lambda s: s.shift(1).rolling(window=window, min_periods=min_periods).var())
    )
    return out


def cluster_robust_ols(y: np.ndarray, X: np.ndarray, groups: np.ndarray) -> dict:
    """OLS with CR1 cluster-robust covariance. X already includes an intercept."""
    n, k = X.shape
    xtx_inv = np.linalg.pinv(X.T @ X)
    beta = xtx_inv @ X.T @ y
    resid = y - X @ beta

    meat = np.zeros((k, k))
    uniq = np.unique(groups)
    for g in uniq:
        mask = groups == g
        Xg, ug = X[mask], resid[mask]
        score = Xg.T @ ug
        meat += np.outer(score, score)

    G = len(uniq)
    correction = (G / (G - 1)) * ((n - 1) / max(1, n - k))
    cov = correction * xtx_inv @ meat @ xtx_inv
    se = np.sqrt(np.maximum(np.diag(cov), 0.0))
    return {
        "beta": beta.tolist(),
        "se": se.tolist(),
        "n_obs": int(n),
        "n_clusters": int(G),
        "df": int(G - 1),
        "correction": float(correction),
    }


def within_participant_model(df: pd.DataFrame, label: str) -> dict:
    from scipy import stats

    d = df.copy()
    d["L_c"] = centre_by_participant(d, "L_s")
    X = np.column_stack([np.ones(len(d)), d["L_c"].to_numpy(float)])
    fit = cluster_robust_ols(d["Y"].to_numpy(float), X, d["subject"].to_numpy())

    b, se, dfree = fit["beta"][1], fit["se"][1], fit["df"]
    t_stat = b / se if se > 0 else float("nan")
    p_val = 2 * (1 - stats.t.cdf(abs(t_stat), dfree)) if np.isfinite(t_stat) else float("nan")
    crit = stats.t.ppf(0.975, dfree)
    ci = [b - crit * se, b + crit * se]

    per_participant = []
    for subject, group in d.groupby("subject"):
        if group["L_c"].nunique() < 2:
            per_participant.append({"subject": subject, "slope": None, "n": int(len(group))})
            continue
        slope = np.polyfit(group["L_c"], group["Y"], 1)[0]
        per_participant.append({"subject": subject, "slope": float(slope), "n": int(len(group))})

    slopes = [p["slope"] for p in per_participant if p["slope"] is not None]
    return {
        "label": label,
        "n_obs": fit["n_obs"],
        "n_clusters": fit["n_clusters"],
        "coefficient_for_centred_L": float(b),
        "cluster_robust_se": float(se),
        "t": float(t_stat),
        "df_clusters_minus_1": fit["df"],
        "p_exploratory": float(p_val),
        "ci95_exploratory": ci,
        "participants_with_negative_slope": sum(1 for s in slopes if s < 0),
        "participants_with_slope": len(slopes),
        "per_participant": per_participant,
        "warning": (
            "Exploratory on a derived table. Not the original v5 analysis, and not "
            "confirmatory. One observation per trial treated as exchangeable within "
            "participant; no trial-order or difficulty covariates."
        ),
    }


def between_participant_model(df: pd.DataFrame) -> dict:
    from scipy import stats

    summary = df.groupby("subject").agg(accuracy=("Y", "mean"), L_mean=("L_s", "mean"), n=("Y", "size"))
    slope, intercept, r, p, se = stats.linregress(summary["L_mean"], summary["accuracy"])
    return {
        "n_participants": int(len(summary)),
        "slope": float(slope),
        "intercept": float(intercept),
        "r": float(r),
        "r_squared": float(r * r),
        "p_exploratory": float(p),
        "stderr": float(se),
        "warning": "n = 15. Grossly underpowered; a coefficient here is descriptive only.",
        "participant_values": summary.reset_index().to_dict(orient="records"),
    }


def loso_sign_stability(df: pd.DataFrame) -> dict:
    subjects = sorted(df["subject"].unique())
    signs = []
    for held_out in subjects:
        subset = df[df["subject"] != held_out]
        subset = subset.copy()
        subset["L_c"] = centre_by_participant(subset, "L_s")
        slope = np.polyfit(subset["L_c"], subset["Y"], 1)[0]
        signs.append({"held_out": held_out, "slope": float(slope)})
    slopes = np.array([s["slope"] for s in signs])
    return {
        "n_folds": len(signs),
        "all_negative": bool(np.all(slopes < 0)),
        "n_negative": int(np.sum(slopes < 0)),
        "slope_min": float(slopes.min()),
        "slope_max": float(slopes.max()),
        "slope_median": float(np.median(slopes)),
        "folds": signs,
        "note": (
            "This tests stability of a slope sign across held-out participants. It is "
            "not predictive validation and it is not the original disclosed LOSO result."
        ),
    }


def _design(df: pd.DataFrame, augment: bool) -> tuple[np.ndarray, list[str]]:
    cols = ["L_c"]
    if augment:
        cols.append("L_prior_var_c")
    return df[cols].to_numpy(float), cols


def lopo_auc(df: pd.DataFrame, augment: bool) -> dict:
    """Leave-one-participant-out AUC on a common complete-case sample."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.preprocessing import StandardScaler

    d = df.dropna(subset=["L_prior_var"]).copy() if augment else df.copy()
    d["L_c"] = d["L_s"] - d.groupby("subject")["L_s"].transform("mean")
    if augment:
        d["L_prior_var_c"] = d["L_prior_var"] - d.groupby("subject")["L_prior_var"].transform("mean")

    X, names = _design(d, augment)
    y = d["Y"].to_numpy(int)
    groups = d["subject"].to_numpy()

    preds = np.full(len(y), np.nan)
    per_fold = []
    for held_out in np.unique(groups):
        test = groups == held_out
        train = ~test
        if len(np.unique(y[train])) < 2 or len(np.unique(y[test])) < 2:
            per_fold.append({"held_out": str(held_out), "status": "skipped"})
            continue
        scaler = StandardScaler().fit(X[train])
        model = LogisticRegression(max_iter=2000, random_state=0)
        model.fit(scaler.transform(X[train]), y[train])
        preds[test] = model.predict_proba(scaler.transform(X[test]))[:, 1]
        per_fold.append({
            "held_out": str(held_out),
            "status": "evaluated",
            "auc": float(roc_auc_score(y[test], preds[test])),
            "n_test": int(test.sum()),
        })

    ok = np.isfinite(preds)
    auc = float(roc_auc_score(y[ok], preds[ok])) if ok.sum() and len(np.unique(y[ok])) == 2 else None
    return {
        "features": names,
        "pooled_lopo_auc": auc,
        "n_rows_used": int(ok.sum()),
        "n_rows_excluded_for_missing_feature": int((~ok).sum()),
        "per_fold": per_fold,
        "predictions": preds,
        "y": y,
        "groups": groups,
    }


def cluster_bootstrap_auc_difference(base: dict, aug: dict, reps: int, seed: int) -> dict:
    """Bootstrap over participants, not over trials."""
    from sklearn.metrics import roc_auc_score

    ok = np.isfinite(base["predictions"]) & np.isfinite(aug["predictions"])
    y, pb, pa, g = base["y"][ok], base["predictions"][ok], aug["predictions"][ok], base["groups"][ok]
    subjects = np.unique(g)
    rng = np.random.default_rng(seed)

    diffs = []
    for _ in range(reps):
        pick = rng.choice(subjects, size=len(subjects), replace=True)
        idx = np.concatenate([np.flatnonzero(g == s) for s in pick])
        if len(np.unique(y[idx])) < 2:
            continue
        diffs.append(roc_auc_score(y[idx], pa[idx]) - roc_auc_score(y[idx], pb[idx]))

    diffs = np.array(diffs)
    if len(diffs) < 20:
        return {"status": "insufficient_replicates", "n": int(len(diffs))}
    return {
        "n_replicates": int(len(diffs)),
        "mean_difference": float(diffs.mean()),
        "ci95_percentile": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))],
        "proportion_le_zero": float(np.mean(diffs <= 0)),
        "unit": "participant (cluster bootstrap)",
        "warning": (
            "With 15 clusters the bootstrap is coarse; the interval is indicative, not exact."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("trials_csv")
    ap.add_argument("--reps", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261103)
    ap.add_argument("--outdir", default="nfot_statistical_audit")
    args = ap.parse_args()

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    df = add_prior_variance(load(Path(args.trials_csv)))

    report: dict = {
        "status": "EXPLORATORY_ON_DERIVED_TABLE",
        "input_rows": int(len(df)),
        "n_participants": int(df["subject"].nunique()),
        "original_inferential_results_reproducible": False,
        "reason": (
            "Raw EDFs or trusted event streams, original inferential code, and original "
            "prediction outputs are absent from the repository."
        ),
        "within_participant": within_participant_model(df, "full sample"),
        "between_participant": between_participant_model(df),
        "loso_sign_stability": loso_sign_stability(df),
    }

    # Both models must be evaluated on the SAME rows and the SAME folds, otherwise the
    # AUC difference is confounded by a different sample. The augmented model needs a
    # prior-trial variance, which is missing for the first trial of every recording, so
    # the common complete-case sample is defined once and used by both.
    common = df.dropna(subset=["L_prior_var"]).copy()
    base = lopo_auc(common, augment=False)
    aug = lopo_auc(common, augment=True)
    full_sample_baseline = lopo_auc(df, augment=False)
    report["auc"] = {
        "common_complete_case_rows": int(len(common)),
        "rows_dropped_from_full_sample": int(len(df) - len(common)),
        "full_sample_baseline_auc_not_comparable": full_sample_baseline["pooled_lopo_auc"],
        "baseline_centred_L": {k: v for k, v in base.items() if k not in ("predictions", "y", "groups")},
        "augmented_centred_L_plus_prior_var": {k: v for k, v in aug.items() if k not in ("predictions", "y", "groups")},
        "same_rows_and_folds": base["n_rows_used"] == aug["n_rows_used"],
        "observed_difference": (
            (aug["pooled_lopo_auc"] - base["pooled_lopo_auc"])
            if base["pooled_lopo_auc"] is not None and aug["pooled_lopo_auc"] is not None
            else None
        ),
        "bootstrap_difference": cluster_bootstrap_auc_difference(base, aug, args.reps, args.seed),
    }

    # Sensitivity: coarser timestamp grids.
    sens = {}
    for step in (0.25, 0.5):
        d = df.copy()
        d["L_s"] = (d["L_s"] / step).round() * step
        d = add_prior_variance(d)
        b = lopo_auc(d, augment=False)
        a = lopo_auc(d, augment=True)
        sens[f"quantised_{step}s"] = {
            "within_participant": within_participant_model(d, f"L coarsened to {step}s"),
            "baseline_auc": b["pooled_lopo_auc"],
            "augmented_auc": a["pooled_lopo_auc"],
            "n_distinct_L": int(d["L_s"].nunique()),
        }
    report["quantisation_sensitivity"] = sens

    # Sensitivity: drop the participant with the missing block.
    without_19 = df[df["subject"] != "M_19"].copy()
    w = without_19.copy()
    w["L_c"] = centre_by_participant(w, "L_s")
    report["missing_recording_sensitivity"] = {
        "dropped": "M_19 (24 of 30 trials present)",
        "within_participant": within_participant_model(without_19, "excluding M_19"),
        "note": "Tests whether one short participant drives the direction of the effect.",
    }

    (out / "statistical_audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "within": {k: report["within_participant"][k] for k in
                   ("coefficient_for_centred_L", "cluster_robust_se", "p_exploratory",
                    "ci95_exploratory", "participants_with_negative_slope", "participants_with_slope")},
        "between": {k: report["between_participant"][k] for k in
                    ("n_participants", "slope", "r", "p_exploratory")},
        "loso": {k: report["loso_sign_stability"][k] for k in
                 ("n_folds", "all_negative", "n_negative", "slope_median")},
        "auc": {k: report["auc"][k] for k in
                ("same_rows_and_folds", "observed_difference", "bootstrap_difference")},
        "auc_baseline": report["auc"]["baseline_centred_L"]["pooled_lopo_auc"],
        "auc_augmented": report["auc"]["augmented_centred_L_plus_prior_var"]["pooled_lopo_auc"],
        "quantisation": {
            k: {"b_centred_L": v["within_participant"]["coefficient_for_centred_L"],
                "p": v["within_participant"]["p_exploratory"],
                "baseline_auc": v["baseline_auc"], "n_distinct_L": v["n_distinct_L"]}
            for k, v in sens.items()
        },
        "without_M_19": {
            "b": report["missing_recording_sensitivity"]["within_participant"]["coefficient_for_centred_L"],
            "p": report["missing_recording_sensitivity"]["within_participant"]["p_exploratory"],
        },
    }, indent=2))
    print(f"wrote {out/'statistical_audit.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
