# Neural Feedback Optimization Theory v6: Measurement Validation, Distributional Predictors, and a Prospective Test of Feedback Timing

**Manuscript status:** Draft release candidate. The prospective experiment described here has not been conducted, approved, or preregistered.

## Abstract

Neural Feedback Optimization Theory (NFOT) asks whether a trial-level interval between defined stimulus and feedback events contains information about performance in closed-loop learning systems. This v6 audit distinguishes what is arithmetically reproducible from the supplied repository artifact, what remains historical and unverified, and what requires prospective testing. The repository contains a 444-row derived table from 15 subject identifiers and a v5 PDF, but it does not contain the raw EDF recordings, complete converted event streams, source-level audit traces, inclusion manifest, or exact inferential-analysis outputs needed to reproduce the historical extraction and model claims. From the supplied derived table, 368/444 rows are coded correct, mean `L_s` is 7.060 s, and sample SD is 3.321 s. These are derived-table arithmetic checks, not independent validation of event semantics or labels. Official bigP3BCI documentation supports phase-aware interpretation of `PhaseInSequence`, `StimulusBegin`, `StimulusType`, character channels, `CurrentTarget`, `SelectedTarget`, and `DisplayResult`, and does not support treating the binary `StimulusType` field as a character identity [1] [2]. The historical association, LOSO result, and AUC improvement remain unresolved. We propose a draft randomized post-selection feedback-delay experiment whose primary outcome is downstream performance, because a delay applied after a selection cannot cause correctness of that already completed selection. NFOT therefore remains a falsifiable operational hypothesis, not an established biological mechanism or causal theory.

## Research question and scope

The minimal operational question is whether an event-defined Write-Back Gap, `L = t_fb - t0`, contains trial-level information about performance beyond simple aggregate latency. In the historical analysis, `t0` is intended to be the first verified stimulus-onset event during the relevant trial phase and `t_fb` the first verified feedback-display event. The interval is an operational measurement. It is not automatically neural processing time, display photon onset, synaptic eligibility time, or a causal learning variable.

This release audits the repository at commit `88045e34d8b63243459a85945830bb167818b17d`. It preserves the v5 PDF and derived table, adds guarded validation code and documentation, and does not publish or overwrite a release.

## Background and related work

The official bigP3BCI documentation defines pre-run, pre-trial, during-trial, and post-trial phases and distinguishes stimulus onsets, target/non-target stimulus markers, character-presentation channels, current targets, predicted selections, and feedback display events [1] [2]. The dataset is heterogeneous across studies, paradigms, grids, and participants, so event semantics must be verified against the source export rather than inferred from a filename or an old script.

Primary BCI studies suggest that timing can matter without identifying a universal optimum. A P300-speller study found a training-stage feedback advantage most clearly at four flashes per row/column, with weaker or absent evidence at larger flash counts and no significant group-by-flash-count interaction [3]. A single-case restorative BCI study observed improvement under 16–96 ms proprioceptive update intervals, but its design did not isolate an optimal timing effect [4]. An offline classifier study reported 67% accuracy using a 750-ms window and 32-ms updates, which is not causal evidence about delivered feedback [5].

Neural plasticity studies provide a possible mechanistic rationale for delayed signals, but not a direct NFOT mechanism. Ex vivo work supports transient eligibility states that can be gated by later monoaminergic signals. Reported windows differ across cortical, hippocampal, and corticostriatal preparations, including a tested approximately two-second dopamine window in one striatal protocol [6] [7]. These results are preparation-specific and do not establish that a software event interval in a human BCI measures a synaptic trace.

In educational and neuroadaptive systems, feedback timing also depends on the outcome. Immediate feedback outperformed 250- and 500-ms delays for a controlled parietal-alpha neurofeedback outcome, while educational prototypes using 5–15-second EEG aggregation and update windows reported engagement or immediate-comprehension effects without establishing a general latency rule or durable learning benefit [8] [9] [10]. Experimental learning studies likewise find conditional effects of immediate versus delayed feedback on later recall, transfer, and assessment performance rather than a universal direction [11] [12].

## Data provenance and methods

The repository contains a v5 PDF, scripts, documentation, a 444-row derived trial table, a 12-row software timing-prototype CSV, and two empty purported source CSVs. It does not contain the raw EDF files, complete converted event streams, converter metadata, original v5 outputs, or an exact inclusion manifest. SHA-256 hashes and command provenance are recorded in `docs/V6_RESULTS_PROVENANCE.md`.

The guarded extractor on this branch requires explicit time units and source-export confirmation. It uses `StimulusBegin`, `DisplayResult`, `CurrentTarget`, and `SelectedTarget`; it rejects empty or ambiguous inputs and never uses `StimulusType` as a character label. The extractor was not run on source data because those inputs are unavailable.

The available-table analysis validates required columns, numeric domains, binary outcomes, nonnegative intervals, `L_s = tfb_s - t0_s`, and duplicate `(file, trial)` identifiers. It produces descriptive summaries only. The repaired analysis entry point does not claim to reproduce the historical beta, p-value, LOSO slopes, or AUC interval.

## Results that can be reproduced

The supplied table contains 444 rows, 15 subjects, and 74 files. It contains 368 coded correct outcomes and 76 coded incorrect outcomes. The stored accuracy is 82.8829%. Mean `L_s` is 7.0602477 s, sample SD is 3.3209017 s, median is 6.125 s, minimum is 1.875 s, and maximum is 15.0 s. All 444 rows satisfy `L_s = tfb_s - t0_s` at `1e-12` tolerance. No missing values, full-row duplicates, or duplicate `(file, trial)` identifiers were found in the supplied derived table.

These results describe the artifact as stored. They do not verify that the timestamps came from the intended source events or that `Y` was constructed from valid target and selection semantics. The software timing prototype contains 12 rows, four per assigned delay of 0.25, 1.00, and 2.00 s. Its timestamps are explicitly marked as software-command proxies, with physical display timing and biological measurement both false.

## Historical results that remain unresolved

The v5 PDF reports a within-participant coefficient of `-0.111` with `p=.030`, negative LOSO slopes in 15/15 folds, and an AUC increase from 0.656 to 0.731 with a reported 95% interval of `[0.021, 0.131]`. The repository does not supply the exact model code, binary prediction target, held-out predictions, bootstrap procedure, or complete source inputs needed to reproduce these claims. They are preserved as historical reported results, not upgraded to v6 findings. The target-label conflict involving `CurrentTarget` and `StimulusType` also remains unresolved because the raw event source is missing.

## Robustness and sensitivity requirements

A defensible reanalysis must begin with source-level event validation. It should record event-row indices, phase transitions, timestamp units, target values, selected values, and exclusion reasons. It should produce an old-to-new crosswalk rather than silently replace the v5 table.

For the same-trial association, the primary observational model should use within-participant-centered `L`, account for participant clustering, and report an effect estimate with uncertainty and diagnostics. Sensitivities should address trial order, flash count, participant exclusions, alternative supported event interpretations, and influential observations. For distributional predictors, the independent unit is the participant or participant-session, not the repeated trial. Participant-grouped validation is required when claiming generalization to unseen participants; preprocessing, feature selection, and tuning must occur inside training folds [13] [14].

## Discussion and limitations

NFOT v6 supports a narrower claim than the strongest historical narrative: an event-defined timing interval may be worth investigating as a performance-related variable. The available repository does not establish that interval as a biological mechanism, does not demonstrate that timing causes current-trial correctness, and does not independently reproduce the historical inferential statistics.

Physical display timing is a separate measurement problem. Photodiode and photodetector studies report hardware-, scan-position-, pixel-response-, browser-, and operating-system-dependent discrepancies between software commands and measured display transitions [15] [16]. API timestamps are estimates whose reliability depends on backend and hardware. If the theory makes a claim about actual visual onset, external timing measurement with a declared luminance criterion is required.

## Prospective test

The draft protocol in `docs/V6_PROSPECTIVE_PROTOCOL.md` separates association from causation. The causal design randomizes post-selection feedback timing and prespecifies a downstream outcome, such as accuracy over a subsequent fixed set of eligible trials or a subsequent block. Exact timing levels, randomization unit, primary outcome, sample size, stopping rule, missing-data policy, and model must be frozen after engineering feasibility work and appropriate supervision/ethics review. The primary analysis should be intention-to-treat by assigned condition. Achieved timing is a manipulation check, not a randomized exposure by assumption.

A result favoring one assigned condition would support only the specified downstream effect under the studied conditions. A null or opposite result would weaken the corresponding causal hypothesis. Neither outcome alone would establish a neural or synaptic mechanism.

## Data and code availability

All code changes are on the unpushed branch `nfot-v6-audit`. The audit, validation report, provenance ledger, theory review, protocol draft, research notes, and unit tests are included in this working tree. No release, publication, or GitHub push was performed.

## References

[1]: https://doi.org/10.13026/0byy-ry86 "bigP3BCI official PhysioNet dataset and data dictionary"
[2]: https://www.physionet.org/content/bigp3bci/1.0.0/README.md "bigP3BCI v1.0.0 official README and protocol"
[3]: https://doi.org/10.1109/EMBC.2015.7318856 "Effects of feedback latency on P300-based Brain-computer Interface"
[4]: https://doi.org/10.1098/rsos.170660 "Investigating the impact of feedback update interval on the efficacy of restorative brain–computer interfaces"
[5]: https://doi.org/10.1109/EMBC.2013.6609813 "Trade-off between time window length, classifier update rate and classification accuracy"
[6]: https://doi.org/10.1016/j.neuron.2015.09.037 "Distinct Eligibility Traces for LTP and LTD in Cortical Synapses"
[7]: https://doi.org/10.1111/ejn.13921 "A Silent Eligibility Trace Enables Dopamine-Dependent Synaptic Plasticity"
[8]: https://doi.org/10.1088/1741-2552/abc8d7 "Short-delay neurofeedback facilitates training of the parietal alpha rhythm"
[9]: https://doi.org/10.3390/s19235200 "AttentivU: EEG-based closed-loop biofeedback for personalized learning"
[10]: https://doi.org/10.1145/3719160.3736623 "NeuroChat: A Neuroadaptive AI Chatbot for Customizing Learning Experiences"
[11]: https://doi.org/10.1037/1076-898x.13.4.273 "The effect of type and timing of feedback on learning from multiple-choice tests"
[12]: https://doi.org/10.1016/j.jarmac.2014.05.001 "Delaying feedback promotes transfer of knowledge despite student preferences"
[13]: https://doi.org/10.1001/archpsyc.61.3.310 "Move over ANOVA: progress in analyzing repeated-measures data"
[14]: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html "Official GroupKFold documentation"
[15]: https://doi.org/10.1371/journal.pone.0085108 "Measuring Software Timing Errors in Visual Stimuli"
[16]: https://doi.org/10.7717/peerj.9414 "The timing mega-study"
