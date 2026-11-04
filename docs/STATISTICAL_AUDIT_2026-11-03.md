# NFOT independent statistical audit — 2026-11-03

**Scope:** the 444-row derived table in this repository. **Status: exploratory.** The original v5/v6 inferential analysis is *not* reproduced here and cannot be, because the raw EDFs, the original inferential code and the original prediction outputs are absent.

**Script:** `analysis/statistical_audit.py`. **Output:** `statistical_audit.json`.
**Environment:** Python 3.12.3, NumPy 2.5.4, pandas 3.1.0, SciPy 1.18.1, scikit-learn 1.9.1. Seed 20261103, 2000 bootstrap replicates.

---

## 1. Correction to the phase-1 audit

Phase 1 reported a "naive pooled within-participant correlation r = −0.1123, p = 0.0179" and described it as "weakly encouraging" because the point estimate was close to the reported β = −0.111.

**That framing was wrong, and is corrected here.** The pooled p-value treats 444 trials as 444 independent observations. They are clustered within 15 participants. Once the standard error is clustered by participant, the same association is not statistically distinguishable from zero:

| Quantity | Naive (phase 1) | Cluster-robust (this audit) |
|---|---|---|
| Coefficient on participant-centred `L` | −0.1123 (correlation) | **−0.0163** (linear probability slope, per second) |
| Standard error | — (trial-level) | **0.0101** |
| t | — | −1.62 |
| df | 442 | **14** (clusters − 1) |
| p (two-sided, exploratory) | 0.0179 | **0.127** |
| 95% CI | — | **[−0.0380, +0.0053]** — includes zero |

These two numbers are not the same parameter, so they are not "close". The naive test overstated the evidence by roughly the design effect of the clustering. The 95% interval spans both a meaningful negative effect and zero.

## 2. Within-participant vs between-participant

| Analysis | Estimate | n | Reading |
|---|---|---|---|
| Within-participant (centred `L`, clustered SE) | b = −0.0163, p = 0.127 | 444 trials / 15 clusters | Not distinguishable from zero |
| Between-participant (participant accuracy on participant mean `L`) | slope = −0.0480, r = −0.759, p = 0.001 | **15 participants** | Strong, but cross-sectional and confounded |

The strong association is **between** participants: participants whose mean gap is longer are less accurate overall. That is compatible with a large number of confounders — overall speed, engagement, fatigue, signal quality — and is not evidence that changing feedback timing within a participant would change that participant's accuracy. Conflating these two is the single most likely way this result could be over-interpreted.

## 3. Leave-one-participant-out stability

The slope sign is negative in **15 of 15** held-out folds (median slope −0.0161, range from the audit JSON). Direction is stable; magnitude is small and the clustered interval includes zero. **Sign stability is not significance**, and this is not the originally disclosed LOSO result.

## 4. AUC

Two models on **identical rows and identical folds** (296 complete-case rows; 148 dropped because the first trial of every recording has no prior-trial variance):

| Model | Pooled out-of-fold AUC | Mean per-fold AUC |
|---|---|---|
| Baseline (centred `L`) | 0.4142 | **0.5617** (13 evaluable folds) |
| Augmented (centred `L` + centred prior-trial variance) | 0.4007 | 0.5424 |
| Difference | **−0.0134** | −0.0193 |

Cluster bootstrap over participants (2000 replicates): mean difference −0.0143, 95% percentile interval **[−0.0363, +0.0045]**, 92.4% of replicates ≤ 0.

Three findings, in order of importance:

1. **The augmented model does not improve on the baseline.** The point estimate is negative for both the pooled and per-fold summaries, and the interval is centred below zero. This is the opposite direction to the reported 0.656 → 0.731 improvement, on a different feature set and sample.
2. **Pooled out-of-fold AUC is the wrong summary here.** It (0.414) is well below the mean per-fold AUC (0.562) and below chance, because each fold's model carries its own intercept fitted to a different set of participants. Pooling predictions across participants with different base rates produces a ranking dominated by cross-participant differences. Per-fold AUC should be reported, with the spread.
3. **Per-fold AUC is wildly unstable**: individual folds range from 0.111 to 1.000 across 13 evaluated folds. With ~24–30 trials per participant, a fold AUC is nearly meaningless on its own. Two folds were skipped for having a single outcome class.

## 5. Sensitivity to the 125 ms quantisation

| `L` grid | Distinct `L` values | Within-participant b | p | Baseline AUC |
|---|---|---|---|---|
| Original (0.125 s) | 90 | −0.0163 | 0.127 | 0.4142 |
| Coarsened to 0.25 s | 48 | −0.0160 | 0.137 | 0.4630 |
| Coarsened to 0.5 s | 26 | −0.0162 | 0.136 | 0.4634 |

The estimate is **insensitive** to coarsening, which is expected: a 0.125 s grid is fine relative to an SD of 3.32 s. This does not license sub-125 ms claims about resolution, but it does mean the quantisation is not what drives the result.

## 6. Sensitivity to the missing recording block

Excluding `M_19` (24 of 30 trials present): b = −0.0161, p = 0.170. The association is not driven by the participant with the incomplete block.

## 7. What this audit does and does not establish

**Does establish:** the descriptive counts, accuracy and gap statistics are exact; the within-participant association is small, directionally stable, and statistically indistinguishable from zero under appropriate clustering; the strong association is between-participant; the distributional augmentation does not improve out-of-fold discrimination in this sample.

**Does not establish:** that the reported v5 β, p, LOSO or AUC are wrong. They were computed from source data that is not present, possibly with covariates, different feature definitions and a different validation scheme. They remain **UNVERIFIED**, not refuted. No claim here about causation, mechanism, or any biological process.
