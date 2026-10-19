# PTSP preregistration draft — not ready for final lock

**Protocol status:** draft only. This cannot honestly be called preregistered until the corrected extraction, primary estimand and timing manipulation are reviewed and frozen before data collection.

## 1. Motivation and question

The observational NFOT v5 analysis reported that Write-Back Gap (WBG), defined as the interval from first stimulus onset to feedback presentation, and a participant-level dispersion measure may relate to selection accuracy. These claims require reanalysis because the legacy extractor's use of `PhaseInSequence == 1` as a flash onset and `StimulusType` as a character target conflicts with the general bigP3BCI data dictionary.

PTSP should test a specific causal timing question, not use a manipulation to retroactively validate all observational associations.

## 2. Separate the estimands (must select one primary)

### Option A — causal effect of post-selection feedback delay on subsequent performance

Randomize feedback timing **after the current selection is complete**. Because current-trial correctness is already determined before the randomized delay, the primary outcome must be downstream—for example, accuracy on the next K eligible trials or the next fixed-length block. Choose the K / block definition before enrollment.

This design tests whether feedback timing changes later adaptation or behavior. It does **not** test whether delaying feedback causes the correctness of the already-completed selection.

### Option B — causal effect on same-trial selection accuracy

A same-trial accuracy question requires the timing manipulation to occur before the current selection outcome is determined. Simply holding back feedback after selection cannot answer it. Altering stimulus pacing or evidence availability may affect both elapsed time and available information, so its treatment contrast and mechanisms must be defined separately. Do not describe a post-selection wait as a direct same-trial accuracy intervention.

**Recommended starting point:** Option A is the cleaner isolated intervention; the target and downstream endpoint must be approved by a qualified supervisor before lock.

## 3. Population / setting

To be completed by the supervising research team: eligibility criteria, sample-size justification, consent/assent process, institution and ethics review, device/software version, accessibility needs, and stopping criteria. Any prospective human-participant research must be developed and overseen by qualified adults and the appropriate institutional ethics process. A simulation / offline pipeline test can be conducted first.

## 4. Arms and randomization (draft skeleton)

Three assigned timing conditions:

1. **Fast feedback:** minimum feasible and technically stable post-selection delay.
2. **Standard feedback:** current validated default delay.
3. **Programmed delay:** a prespecified added delay selected for ethical, practical and technical acceptability.

Use computer-generated randomized assignments at the prespecified unit (trial or block) with stratification / blocking if necessary. State exact delay values and tolerance before data collection; these must be chosen from system measurements/pilot feasibility data, not tuned to outcomes. Keep feedback content, display duration, task, classifier and stimuli matched across arms. Log assignment, requested delay, actual feedback onset, failures, and all timestamps.

Do not tell participants the specific trial-by-trial timing schedule if that would create avoidable expectancy effects, unless disclosure is required by the consent protocol; document the information given to participants.

## 5. Event definitions (freeze before collection)

- `t0`: onset edge of the first visual stimulus in the current trial, captured from the display/event logger.
- `t_decision`: timestamp when the BCI system commits the predicted character, before the randomized feedback delay.
- `tfb`: actual display-presentation onset, not the requested/preset delay timestamp.
- `L = tfb - t0`.
- `D_assigned`: randomized timing assignment.
- `D_achieved = tfb - t_decision`: actual post-decision feedback delay (manipulation-check variable; separate from L).
- `Target`: independent trial target used by the BCI task.
- `SelectedTarget`: prediction frozen at `t_decision`.
- `Y_current = 1(SelectedTarget == Target)`: current-trial correctness, determined before delay assignment takes effect.
- `Y_future`: primary downstream outcome under Option A, defined here before the study (e.g. mean correctness over the next K eligible trials).

Store event samples and monotonic system clock values; record the mapping between BCI event time and wall/display time. Define dropped/missed feedback and out-of-tolerance events in advance.

## 6. Primary hypothesis and analysis (Option A template)

**Primary null:** assigned post-selection feedback delay has no effect on the prespecified subsequent-performance endpoint.

**Primary contrast:** programmed-delay versus standard-feedback condition on the participant-level / block-level `Y_future` endpoint, with the exact contrast choice fixed before enrollment. Fast versus standard and ordered-trend analyses are secondary unless selected as primary before lock.

**Primary estimand:** intention-to-treat effect of assigned delay. Analyze participants according to randomized assignment, including all assigned trials under prespecified rules. Do not replace randomized assignment with achieved L as though achieved timing were randomized.

Use a model that accounts for repeated observations within participant and randomization unit. Report absolute effect, uncertainty interval, model diagnostics, missingness, exclusions and all planned contrasts. Determine sample size using a simulation/pilot-based power analysis for the chosen primary endpoint and clustering; do not select N just because it produces statistical significance.

**Manipulation check:** distribution of achieved post-decision delay and achieved WBG by assigned arm; report technical failures and overlap. This is not the primary effectiveness test.

**Secondary outcomes:** current-trial correctness (negative control for a post-selection delay effect), response latency on subsequent trials, next-block accuracy, completion rate, and participant experience as approved by the supervising study team.

## 7. Exclusions and missing data

Specify exclusions without reference to outcomes: incomplete source events, clock synchronization failure, feedback not rendered, impossible/duplicate event sequence, invalid target/prediction, device failure, participant withdrawal, and protocol deviations. Report each category by assigned arm. Do not silently delete an inconvenient or slow trial. The handling of missing primary outcomes must be predeclared.

## 8. Multiplicity and robustness

Name one primary endpoint and one primary contrast. All additional contrasts, WBG summaries (mean, SD, IQR, high quantile), thresholds, subgroup tests, and outcome windows are secondary or exploratory, with an explicit multiplicity strategy. Use sensitivity analyses for technical failures and assigned-versus-achieved timing without changing the primary estimand.

## 9. Data/code transparency

Before starting: timestamped preregistration; frozen code commit; simulated-data test results; event dictionary; data schema; randomization seed handling; versioned software/dependencies; primary model formula; sample-size calculation; and anonymized analysis plan. After the study: publish deviations, null results and all prespecified outcomes, not only favorable ones.

## 10. Final lock checklist

- [ ] Corrected extraction replicated from a source-level audit.
- [ ] Exact v5 participant/file manifest resolved.
- [ ] Observational analyses rerun with participant-aware inference.
- [ ] Primary dispersion metric frozen or downgraded to exploratory.
- [ ] Primary PTSP estimand selected (Option A or B).
- [ ] Exact timing levels justified with pilot engineering measurements.
- [ ] Decision timestamp separated from feedback display timestamp.
- [ ] Primary outcome cannot be causally downstream of the intervention by mistake.
- [ ] Randomization, exclusions, sample size, models and multiplicity locked.
- [ ] Qualified supervisor and applicable ethics review have approved the protocol.
