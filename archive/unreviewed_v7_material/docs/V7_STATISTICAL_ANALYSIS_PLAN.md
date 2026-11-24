# NFOT v7 statistical analysis plan

**Status:** Planning document; no confirmatory analysis has been completed.

## Estimands

1. **Descriptive:** distribution of verified `L` and observed accuracy.
2. **Between-participant:** association between participant-level gap summaries and participant-level performance.
3. **Within-participant:** association between a trial's gap deviation from the participant's prespecified training-period mean and a prespecified outcome.
4. **Prospective causal:** intention-to-treat effect of randomized post-selection feedback delay on a subsequent outcome.

These estimands must not be conflated.

## Primary future observational model

If source labels are recovered, the primary observational model will be a logistic mixed-effects or participant-clustered model for verified binary outcome, with within-person centered `L` as the primary predictor and participant/session structure represented explicitly. A between-person mean-gap term may be included as a separate secondary predictor. The formula, covariates, missing-data rule, and influential-participant sensitivity must be frozen before confirmatory use.

Available covariates may include trial order, recording/session ID, flash count, target class, and selection count only if source verification establishes their meanings. Do not claim adjustment for unavailable difficulty, fatigue, or neural state.

## Distributional hypothesis

The primary distributional feature must be selected before outcome inspection. Candidate features are mean, median, SD, IQR, prespecified quantiles, and prior-only sequential variation. A distributional model must use the same participants and evaluation units as the mean-only baseline. Participant-level summaries must be computed inside training folds for unseen-participant prediction. Rolling features may use only prior trials.

## Predictive evaluation

For new-participant deployment, use participant-grouped outer splits and perform preprocessing, feature construction, tuning, and model selection inside training data. For future-trial deployment, use time-ordered splits within participants. Report log loss, Brier score, calibration, discrimination, and uncertainty in paired model differences. Do not declare success from one AUC increase.

## Historical exploratory analyses

The v5 beta, thresholds, LOSO slopes, and AUC values remain historical reported results. They are not confirmatory and are not reproduced by v7. Any reanalysis of the supplied table is descriptive or exploratory because source semantics are unresolved.

## Causal diagram in words

Task difficulty and interface state can influence both processing time and accuracy. Trial order, fatigue, learning, session and participant can influence both. The recorded gap may also contain software, communication and display delays. Conditioning on post-response variables can create bias. A randomized post-selection delay addresses the causal effect of assigned delay on subsequent outcomes, not the cause of the completed response.
