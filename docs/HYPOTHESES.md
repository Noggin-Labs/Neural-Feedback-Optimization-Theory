# Competing, falsifiable hypotheses for NFOT v6

The current evidence is observational and reported rather than independently reproduced. These are competing explanations to distinguish, not claims that any one is true.

## H1 — WBG mean reflects task/selection difficulty

**Hypothesis:** longer first-stimulus-to-feedback intervals associate with lower accuracy because difficult trials take longer (more flashes/processing or slower decoding), not because elapsed time itself degrades performance.

**Predictions:** the negative L–Y association attenuates after controlling for number of stimulus onsets, phase-2 duration, prior accuracy, and participant-specific baseline. It may vary by condition.

**Test:** after correct event linkage, model Y with within-subject-centered L and prespecified difficulty/time covariates; inspect overlap and collinearity. Report unadjusted and adjusted estimates, not only the preferred model.

## H2 — WBG dispersion carries information beyond its mean

**Hypothesis:** at the participant/session level, dispersion or upper-tail mass in L predicts accuracy beyond mean L.

**Predictions:** a prespecified dispersion metric adds out-of-sample predictive information when whole participants are held out; the effect is not driven by one subject or a few extreme trials.

**Test:** define one primary dispersion metric before rerunning (e.g. session-level SD or IQR; do not switch between them after seeing outcomes). Compare mean-only vs mean-plus-dispersion using subject-level nested/outer validation and participant bootstrap intervals. Show leave-one-participant-out influence diagnostics. With ~15 participants, regard the result as exploratory.

**Falsification:** the dispersion coefficient consistently changes sign or its predictive increment vanishes under held-out-subject evaluation or correction of event labels.

## H3 — Tail risk, not variance, is the useful summary

**Hypothesis:** unusually long WBG trials (tail probability / high quantiles) relate to poorer performance more strongly than SD.

**Test:** preregister a single tail statistic such as the 90th percentile or fraction beyond a threshold derived from an independent pilot. Compare it to mean and SD with multiplicity control. Do not select a favorable threshold on the same outcome dataset.

## H4 — Measurement artefact explains some or all of the association

**Hypothesis:** incorrect t0 detection, wrong target labels, trial mismatch, timestamp unit conversions, or selection-event deduplication created or exaggerated the apparent relation.

**Predictions:** corrected extraction changes L distributions, target accuracy or subject inclusion; some old trials fail one-to-one matching.

**Test:** create a paired audit table old-to-new using explicit event-row identifiers. Quantify `n matched`, `t0_old - t0_new`, `tfb_old - tfb_new`, target disagreements, Y disagreements and exclusions. Recompute all summary claims only on validated pairs and report the attrition flow.

## H5 — Within-person state / time-on-task drives both L and accuracy

**Hypothesis:** within-session drift (fatigue, adaptation, learning or changing task conditions) creates dependence between L and Y.

**Test:** plot L and Y over trial order; model prespecified linear or nonlinear trial-order terms and condition/file effects. Use blocked time-respecting sensitivity analysis. Do not overfit splines with this sample.

## H6 — There is a general within-trial temporal association

**Hypothesis:** after valid segmentation, longer L is associated with a lower probability of correct selection within a participant, not only between participants.

**Test:** logistic model / GEE with within-person centered L, participant clustering, and prespecified covariates. Provide subject-level slopes and heterogeneity. Do not infer causality from this association.

## H7 — Feedback timing affects subsequent adaptation, not already-made correctness

**Hypothesis:** externally delaying feedback after a selection changes future behavior or the accuracy of subsequent trials, even though it cannot alter the correctness of the selection that was already made.

**Test:** randomized timing intervention after selection; primary endpoint must be a downstream outcome (e.g. next-trial or subsequent-block accuracy/response dynamics) fixed in the preregistration. Keep feedback content identical; analyze assigned delay as intention-to-treat. Treat achieved L as a manipulation check/secondary exposure, not a randomized instrument by assumption.

## H8 — No stable incremental dispersion effect

**Hypothesis:** the apparent SD result reflects small-sample noise, a chosen metric, or outliers, and does not replicate across participants or compatible datasets.

**Test:** use the same frozen code on an independent cohort/condition and report null results. This is a meaningful result, not a project failure.

## Recommended order

H4 (measurement integrity) → H6 (within-person association) and H2/H3 (incremental distribution information) → independent replication → PTSP for an appropriately defined causal question. Do not jump straight from the reported SD association to a causal narrative.
