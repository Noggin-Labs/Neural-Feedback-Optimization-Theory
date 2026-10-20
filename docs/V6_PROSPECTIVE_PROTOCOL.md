# NFOT v6 prospective validation protocol draft

**Status:** Draft for supervisory and ethics review. This protocol has not been conducted, approved, or preregistered.

## Primary causal question and estimand

**Question:** Does randomized post-selection feedback delay affect a prespecified downstream performance outcome?  
**Estimand:** Intention-to-treat contrast in the mean downstream outcome under assigned delay conditions, with participant and randomization-unit dependence modeled explicitly.

A post-selection delay cannot cause correctness of the selection already completed. Same-trial correctness is therefore a negative-control or secondary outcome for this causal question, not the primary endpoint.

## Design skeleton

Use a within-participant randomized design only after qualified supervision and ethics review. Candidate conditions are fast, standard, and programmed-delay feedback. Exact delay levels are **provisional** and must be chosen from engineering feasibility measurements before confirmatory enrollment; no value is treated as established by this document. Randomization may be at trial or block level, but the unit must be fixed before data collection and balanced within participant where feasible.

The primary downstream outcome should be fixed before enrollment, for example mean correctness over the next prespecified set of eligible trials or a subsequent fixed-length block. The final choice must be justified by the task and the plausible temporal reach of the manipulation.

## Measurement and manipulation checks

Record assigned delay, decision time, requested feedback time, actual display-onset time if available, event timestamps, trial identifiers, participant/session identifiers, protocol deviations, and technical failures. Compute achieved post-decision delay from verified endpoints. A software command timestamp must not be described as physical display onset without an independent display measurement. Report achieved timing by assigned condition and retain out-of-tolerance observations under prespecified rules.

## Inclusion, exclusion, and missingness

Define eligibility, consent or assent, age-appropriate oversight, privacy safeguards, withdrawal, device failure, clock synchronization failure, incomplete event sequences, duplicate events, invalid target/prediction, missed feedback, and out-of-tolerance timing before data collection. Exclusions must not depend on the outcome. Report missing primary outcomes by assigned condition and participant.

## Statistical analysis

The primary model should match the randomization unit and repeated-measures structure. A reasonable starting point is a mixed-effects or marginal model for the downstream outcome with assigned condition as the primary predictor and participant as the clustering unit, but the exact model must be frozen before confirmatory data collection. Report absolute contrasts, uncertainty intervals, sample sizes, missingness, diagnostics, and technical-failure rates. Analyze assigned condition as intention-to-treat; treat achieved timing as a manipulation check and secondary exposure, not as randomized by assumption.

Observational analyses of achieved `L` must be separated from the randomized contrast. If a dispersion feature is evaluated, select one primary metric before outcome analysis and label other summaries exploratory. Use participant-grouped validation and participant-level resampling for predictive claims.

## Sample-size and stopping rationale

No numeric sample size is asserted here. Before enrollment, simulate the locked primary analysis using defensible pilot-informed assumptions, the chosen randomization unit, within-participant correlation, attrition, and a precision or power target. The effect assumption must be labeled provisional and sensitivity-analyzed. Stopping rules, interim looks, and any multiplicity adjustment must be written before confirmatory data collection.

## Decision criteria

The primary result should be reported as an estimated assigned-delay contrast with an uncertainty interval. A null, imprecise, or opposite result should be reported without post hoc redefinition of the endpoint. A statistically non-null result would support only the specified downstream timing effect under the studied conditions; it would not establish a neural mechanism or validate every NFOT claim.
