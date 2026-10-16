# Neural Feedback Optimization Theory (NFOT)

### The Write-Back Gap as a Trial-Level Temporal Variable in Closed-Loop Learning Systems

**Version:** 5  
**Status:** Observational analysis completed; prospective causal validation remains outstanding  
**Research areas:** Computational neuroscience · Brain–computer interfaces · Closed-loop learning systems · Temporal dynamics

[**Read the NFOT v5 preprint on Zenodo**](https://zenodo.org/records/23140358)

---

## Overview

Neural Feedback Optimization Theory (NFOT) investigates whether the timing of feedback in a closed-loop system contains meaningful trial-level information about system performance that may be obscured by aggregate latency measures.

The central construct is the **Write-Back Gap**, \(L\): the elapsed time between a defined starting event and the completion of the corresponding feedback event.

$L=t_{\text{fb}}-t_0$

NFOT proposes that the distribution of this interval—including its variability and tail behavior—may provide information about performance beyond its mean alone.

The current research evaluates this proposal using historical brain–computer interface (BCI) data. The results motivate further investigation but do not establish that the Write-Back Gap causally determines performance.

## Research Question

**Does the trial-level Write-Back Gap, including its distributional characteristics, contain information about BCI performance beyond what is captured by its mean?**

A related experimental question is whether controlled changes in feedback timing produce measurable changes in performance. This requires prospective intervention rather than observational analysis alone.

## The Write-Back Gap

The operational definition used in the historical analysis is:

- **$t_0$:** The `StimulusBegin` event, representing stimulus onset in the event stream.
- **$t_{\mathrm{fb}}$:** The rising edge of `DisplayResults`, representing the feedback-display event in the event stream.
- **$L$:** The elapsed interval between these two events.

The interval is a trial-level event-to-feedback measure. It should not automatically be interpreted as neural processing time, pure system latency, or a direct measurement of biological feedback processing.

The definition depends on the event markers available in the dataset and must be specified before analysis in prospective studies.

## Historical BCI Analysis

### Dataset and Processing

The observational analysis used **bigP3BCI Study M data from PhysioNet**.

The analysis pipeline used VampireBCI to extract relevant event markers, including:

- `StimulusBegin`
- `DisplayResults`
- `CurrentTarget`
- `SelectedTarget`

Target selection was reconstructed from the recorded row and column events using the dataset's target-grid convention. The reconstruction was checked against 4,192 of 4,192 applicable events.

### Analysis Sample

The NFOT v5 analysis included:

- **444 trials**
- **15 participants**
- Participants M_04–M_20, excluding M_08

The primary outcome was trial-level BCI target-selection accuracy.

### Reported Results

The v5 analysis reported the following results:

| Measure | Reported result |
|---|---:|
| Trials analyzed | 444 |
| Participants | 15 |
| Overall accuracy | 82.9% |
| Mean Write-Back Gap | 7.06 s |
| Standard deviation of $L$ | 3.32 s |
| Within-participant association | $\beta = -0.111$, $p = 0.030$ |
| Leave-one-subject-out slope direction | Negative in 15/15 folds |
| AUC, baseline model | 0.656 |
| AUC, augmented model | 0.731 |
| AUC difference | +0.076 |
| Reported 95% CI for AUC difference | [0.021, 0.131] |

These figures describe the reported analysis and should be interpreted in the context of its model specifications, uncertainty estimates, and observational design.

The leave-one-subject-out result indicates that the estimated association's direction was consistent across the reported folds. It does not establish causation or guarantee generalization to independent datasets.

### Distributional Analysis

The v5 analysis also investigated whether trial-level variability in $L$ was associated with performance beyond mean timing.

The reported results suggested that variability-related measures may contain additional predictive information. This motivates testing distributional features in future work, with their definitions, model specifications, and evaluation procedures fixed in advance.

Predictive improvement in a retrospective dataset does not, by itself, establish a new biological mechanism.

## Interpretation

The historical findings are consistent with the hypothesis that trial-level feedback timing may be informative about BCI performance.

Three distinctions are essential:

1. **Association is not causation.** The observed relationship does not show that manipulating $L$ will change accuracy.
2. **Prediction is not mechanism.** Better predictive performance does not establish why the association occurs.
3. **A temporal interval is not automatically a neural variable.** The measured interval includes the events and processing stages between its operational endpoints.

Potential confounds, measurement choices, model assumptions, participant-level dependence, and external validity remain relevant to interpretation.

## Why Controlled Validation Is Necessary

The next stage is a prospective experiment that manipulates feedback timing under a predefined protocol.

A rigorous validation plan should specify:

1. Fixed event definitions, signal processing, and event-detection rules.
2. Predefined fast-feedback, slow-feedback, and programmed-delay conditions.
3. Randomized assignment of timing conditions where appropriate.
4. A prespecified primary outcome and statistical analysis.
5. Verification of achieved timing rather than reliance only on assigned delays.
6. Participant-level analysis and transparent handling of missing or invalid trials.
7. Independent replication before making broad claims.

The experiment should distinguish the assigned delay from the achieved Write-Back Gap and should validate physical display timing if claims depend on actual screen onset.

## Software Prototype

The accompanying interactive prototype is a separate software-development tool. It runs a simple number-parity task with randomized post-response delays, records response and feedback-command timestamps, and exports trial-level CSV data.

It is useful for testing:

- Trial sequencing and randomization.
- Timestamp bookkeeping.
- Assigned-versus-achieved delay calculations.
- CSV export and basic consistency checks.

**The prototype does not independently validate the historical BCI findings.** It does not record EEG, directly measure physical display onset, or establish an effect on learning. Its simple task is a starting point for testing the instrumentation workflow.

## Reproducibility

For reproducible research, future releases should document:

- Dataset version and source.
- Event extraction and target-reconstruction procedures.
- Inclusion and exclusion criteria.
- Exact definitions of timing variables.
- Model specifications and uncertainty calculations.
- Software versions and analysis scripts.
- Deviations from the planned protocol.

Raw data should remain unchanged, and all cleaning and exclusion decisions should be documented. Do not publish sensitive or identifiable participant information.

## Limitations

The current evidence has important limitations:

- The historical analysis is observational.
- The sample is limited to the analyzed dataset and participants.
- Event markers are operational measurements and may not equal physical display onset.
- Trial-level observations from the same participant are not independent.
- Predictive performance may change across tasks, devices, datasets, and populations.
- Prospective manipulation and independent replication are still needed.

These limitations define the next research steps; they do not make the question unworthy of investigation.

## Research Status

| Component | Status |
|---|---|
| Write-Back Gap operationalization | Defined for the historical dataset |
| Historical BCI analysis | Completed for v5 |
| Trial-level association analysis | Reported |
| Distributional-feature investigation | Exploratory evidence reported |
| Interactive timing prototype | Implemented separately |
| Prospective causal manipulation | Not yet established |
| Independent replication | Outstanding |
| Biological mechanism | Not established |

## Conclusion

NFOT investigates whether trial-level feedback timing—and particularly the distribution of the Write-Back Gap—can improve how closed-loop system performance is characterized.

The v5 historical analysis reports an association between the Write-Back Gap and BCI accuracy, along with predictive results that motivate further study. The next scientific milestone is not to assume a breakthrough, but to test whether the reported patterns survive controlled manipulation, stronger measurement validation, and independent replication.

**The central claim remains falsifiable:** if prospectively specified analyses fail to show the predicted relationships under appropriately controlled conditions, the hypothesis must be revised or rejected.

## Citation

**Neural Feedback Optimization Theory (NFOT), Version 5.** *The Write-Back Gap as a Trial-Level Temporal Variable in Closed-Loop Learning Systems.* F. A. Kassim, 2026.

[Zenodo record](https://zenodo.org/records/23140358)

---

*This repository documents exploratory independent research. The results are not clinical evidence, and NFOT should not be treated as an established scientific theory without further validation.*
