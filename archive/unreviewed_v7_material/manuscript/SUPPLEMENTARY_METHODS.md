# NFOT v7 supplementary methods

## Repository audit

The baseline was inspected with Git history, tracked-file inventory, file-size and type checks, PDF metadata/text extraction, CSV schema and hash checks, structural audit, timing audit, unit tests, syntax compilation, and `git diff --check`. Remote state was verified with `gh`: PR #1 remains open, `origin/main` is not at the v6 audit commit, and no release exists.

## Source-data gate

The source gate fails closed unless raw EDFs or complete trusted event streams, converter metadata, explicit units, and a source manifest are present. The derived table cannot satisfy this gate. Any successful future extraction must emit source row indices, trial identifiers, target and selection values, event phases, exclusion reasons, and a discrepancy report.

## Observational models

Use a binary-outcome participant-aware model with within-person centered gap and a separate between-person mean. Report odds ratios or probability contrasts with intervals, convergence, and diagnostics. Avoid interpreting a within-person observational coefficient as a causal delay effect.

## Predictive models

Define the deployment target before splitting. For new participants, use grouped outer folds; for future trials, use temporal folds. Compute all participant summaries, imputation, scaling, feature selection, and tuning inside the training partition. Compare intercept-only, conventional latency, within-person gap, and one prespecified distributional model using identical observations and uncertainty procedures.

## Synthetic planning

The v7 simulation uses a fixed random seed, paired participant-level synthetic Bernoulli outcomes, and a simple two-sided normal rejection rule. It is intentionally transparent and incomplete. It provides sensitivity information only; a final design requires the locked primary estimand and pilot-informed nuisance parameters.
