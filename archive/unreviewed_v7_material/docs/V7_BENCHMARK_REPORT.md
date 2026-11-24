# NFOT v7 benchmark report

**Status:** Scientific benchmark blocked; no source-level benchmark result is claimed.

The required target labels and source semantics are not verified, and the historical held-out predictions are unavailable. Therefore this repository does not report an empirical comparison of NFOT features against baselines.

## Planned benchmark

For unseen-participant deployment, compare an intercept-only model, conventional latency/task covariates, within-person gap, and one prespecified distributional feature. Use identical participants, outcomes, outer participant-grouped folds, and tuning budgets. Construct participant summaries inside training folds. For future-trial deployment, use time-ordered splits within participant instead. Report log loss, Brier score, calibration, discrimination, participant variability, and paired uncertainty in model differences.

The key decision is whether an NFOT feature improves a simple conventional latency baseline reliably and interpretably. A single AUC increase is insufficient. If the source data remain unavailable, only synthetic fixtures may be used, and every output must be labeled synthetic.
