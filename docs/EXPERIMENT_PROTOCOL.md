# NFOT Prospective Experiment Protocol

**Status:** Draft for development. This document is not a preregistration, ethics approval, or completed experiment.

## 1. Research Question

Does experimentally manipulating the timing of feedback after a response affect performance on subsequent trials or a prespecified learning outcome?

The experiment should distinguish the effect of assigned feedback timing from observational associations between the Write-Back Gap and task performance.

## 2. Background

Neural Feedback Optimization Theory (NFOT) proposes that the Write-Back Gap may be a useful trial-level temporal variable in closed-loop learning systems.

The historical analysis used BCI event markers to calculate:

`L = t_fb - t0`

Where:

- `t0` is the `StimulusBegin` event.
- `t_fb` is the rising edge of `DisplayResults`.

An association between `L` and performance does not establish causation. A prospective experiment is needed to evaluate the effect of a controlled timing manipulation.

## 3. Core Design Principle

The feedback delay occurs after the response that precedes it. Therefore, the delay cannot cause the correctness of that already-submitted response.

The primary outcome must instead be defined so that it can plausibly be affected by the timing manipulation. A candidate is subsequent-trial performance or a prespecified learning measure.

The primary outcome must be selected before confirmatory data collection.

## 4. Experimental Conditions

A candidate design includes three assigned post-response feedback-delay conditions:

- Fast feedback
- Intermediate feedback
- Slow feedback

The exact delay values must be chosen and documented before confirmatory data collection. They should be justified by the task, software timing capability, and pilot measurements.

Condition order should be randomized or counterbalanced using a documented procedure.

## 5. Timing Definitions

The protocol must define the following before data collection:

- The start event used to calculate the Write-Back Gap
- The feedback endpoint
- The timestamp source for each event
- Any filtering, thresholding, or event-detection rules
- The method used to verify achieved delay
- The tolerance used to classify timing as successfully delivered

Software-command timestamps must not be described as physical display-onset measurements unless physical display onset has actually been measured.

If the study uses the historical BCI event definition, it should retain the documented event semantics and explain any differences from the software prototype.

## 6. Outcomes

### Primary Outcome

**To be specified before confirmatory data collection.**

The primary outcome should measure a subsequent response or learning process that could plausibly be affected by the preceding feedback delay.

### Secondary Outcomes

Possible secondary measures include:

- Subsequent-trial accuracy
- Response time on subsequent trials
- Learning across repeated trials
- Assigned versus achieved delay
- Timing error and timing variability

Secondary outcomes should be identified in advance and should not be presented as confirmatory if they were selected after examining the results.

## 7. Hypothesis

**Confirmatory hypothesis: to be specified before data collection.**

The protocol must state the predicted direction or pattern of the primary outcome across timing conditions. It must also define what result would count against the hypothesis.

If NFOT predicts that the distribution of Write-Back Gap values provides information beyond the mean, the analysis must specify the relevant distributional measure and how its contribution will be evaluated.

## 8. Randomization and Timing Verification

Document:

1. How conditions are assigned.
2. How trial order is generated.
3. Whether assignment is balanced within participants.
4. How assigned delays are logged.
5. How achieved delays are calculated.
6. How missed, interrupted, or invalid trials are handled.
7. The prespecified tolerance for timing deviations.

Analyze achieved timing as a manipulation check. Do not silently exclude trials based on their outcomes.

## 9. Analysis Plan

The statistical model must be selected and documented before confirmatory data collection.

The plan should specify:

- The unit of analysis
- The primary outcome and predictor
- Participant-level dependence and repeated-measures handling
- Covariates and their justification
- Missing-data and invalid-trial rules
- Effect-size reporting
- Uncertainty intervals
- Planned sensitivity analyses
- The approach to multiple comparisons, if applicable

If observational Write-Back Gap measures are also analyzed, keep those analyses distinct from the randomized-condition comparison.

## 10. Sample Size

**To be determined before confirmatory data collection.**

The sample-size justification should use the planned primary outcome, study design, a defensible effect-size assumption, and the intended precision or statistical power. Do not choose the sample size solely because it produces a desired result.

## 11. Human-Participant Safeguards

Before involving participants, obtain appropriate adult research supervision and determine the applicable ethics-review and consent requirements.

Use an appropriate consent or assent process, protect participant privacy, minimize collected data, and document withdrawal procedures. Do not collect identifiable or sensitive information without a clear need and suitable safeguards.

## 12. Interpretation

A difference between randomized timing conditions may support a causal effect of the assigned timing manipulation on the prespecified outcome, provided the design and implementation are sound.

It would not automatically establish a neural mechanism, validate every NFOT claim, or demonstrate that the same effect generalizes to other tasks or populations.

A null result, an imprecise result, or a result opposite to the prediction should be reported transparently.

## 13. Preregistration Checklist

Before confirmatory data collection, finalize:

- [ ] Primary research question
- [ ] Confirmatory hypothesis
- [ ] Primary outcome
- [ ] Exact condition definitions
- [ ] Timing-event definitions
- [ ] Randomization procedure
- [ ] Sample-size justification
- [ ] Statistical model
- [ ] Exclusion and missing-data rules
- [ ] Timing-validation procedure
- [ ] Ethics and consent requirements
- [ ] Reporting and reproducibility plan

## 14. Current Status

This is a protocol draft. It does not claim that a prospective causal experiment has been run, preregistered, or approved.
