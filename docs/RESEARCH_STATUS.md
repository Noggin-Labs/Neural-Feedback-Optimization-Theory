# NFOT Research Status

**Project:** Neural Feedback Optimization Theory (NFOT)

**Status:** Observational analysis completed; prospective causal validation remains outstanding.

## 1. Research Question

NFOT investigates whether the Write-Back Gap can serve as a useful trial-level temporal variable in closed-loop learning systems.

The Write-Back Gap is defined as:

`L = t_fb - t0`

Its interpretation depends on the operational definitions of the start and feedback events.

## 2. Historical Analysis

The project reports an observational analysis of bigP3BCI Study M data from PhysioNet, processed using VampireBCI.

The documented V5 analysis includes:

- 444 trials
- 15 participants
- 82.9% overall accuracy
- Mean Write-Back Gap of 7.06 seconds
- Write-Back Gap standard deviation of 3.32 seconds
- Within-participant association: β = -0.111, p = 0.030
- Negative slope direction in 15 of 15 leave-one-subject-out folds
- Baseline AUC of 0.656 and augmented AUC of 0.731
- Reported AUC improvement of 0.076, with a 95% confidence interval of [0.021, 0.131]

These figures describe the project's reported analysis. They should be interpreted as observational results, not proof of causation or a biological mechanism.

## 3. Timing Prototype

The project includes `NFOT-Timing_Demo.py`, a software demonstration of randomized post-response feedback delays.

The intended configuration includes 12 trials with four assigned to each of three delay conditions: 0.25, 1.00, and 2.00 seconds.

The project reports completion of the timing pilot and CSV arithmetic/consistency checks. The prototype uses software timestamps and does not record EEG.

Its timing measurements should not be described as physical display-onset measurements unless independently verified.

## 4. What the Current Evidence Supports

The reported historical analysis supports further investigation of the relationship between the Write-Back Gap and performance.

The timing prototype supports development and testing of the experimental software and timing records.

Neither establishes that manipulating feedback delay causes a change in learning. The historical association may reflect other factors, and the prototype is not a neural measurement.

## 5. Outstanding Questions

- Does randomized manipulation of feedback timing affect a prespecified subsequent-trial or learning outcome?
- Do distributional properties of the Write-Back Gap add useful information beyond its mean?
- How accurately do software event timestamps correspond to physical stimulus and feedback presentation?
- Do the findings replicate in independent data and other settings?

## 6. Next Milestone

The next major milestone is a prospectively specified causal experiment.

Before confirmatory data collection, define the hypothesis, primary outcome, timing events, randomized conditions, sample-size justification, statistical analysis, and exclusion rules. Because feedback delay occurs after the current response, the primary outcome should concern a subsequent response or learning measure rather than the correctness of the already-submitted response.

Any human-participant research should proceed with appropriate adult supervision, ethics review, consent or assent, and privacy safeguards.

## 7. Reproducibility

Preserve the raw data, scripts, environment requirements, and analysis outputs. Document versions and transformations so that another researcher can reproduce the reported results.

Do not describe the prospective experiment as completed, preregistered, or approved until those milestones have actually occurred.

## 8. Summary

NFOT currently has a reported observational result and a software timing prototype. Prospective causal testing, physical timing validation where needed, and independent replication remain important steps toward determining the theory's scope and validity.
