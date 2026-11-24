# Neural Feedback Optimization Theory v7: Measurement Validation, Temporal Predictors and a Prospective Test of Feedback Timing

## Abstract

Neural Feedback Optimization Theory (NFOT) proposes that the interval between defined initiating and feedback events may be useful in closed-loop learning systems. This manuscript reports a repository audit and validation programme, not a completed causal experiment. The live repository preserves a v5 PDF, a 444-row derived table, a 12-row timing prototype, source code, tests, and v6 documentation. Raw EDF recordings or complete trusted event streams, converter metadata, source-level inclusion logs, and exact historical inferential outputs are unavailable. The supplied table reproduces 368/444 coded correct outcomes, mean gap 7.060 s, sample SD 3.321 s, and exact stored timing arithmetic. These are derived-artifact checks, not source-level replication. Historical beta, LOSO, and AUC claims remain reported but not reproduced. v7 formalizes descriptive, within-participant, predictive, causal, and biological questions separately; specifies a fair benchmark and falsification criteria; and proposes a randomized post-selection delay experiment with a downstream outcome. The most defensible current contribution is a measurement-and-validation framework. NFOT is not currently a demonstrated breakthrough.

## 1. Introduction

NFOT studies the Write-Back Gap, `L = t_fb - t0`, as a possible temporal variable in closed-loop systems. The central scientific risk is category error: a recorded event interval may be a useful system marker without being a neural process, a causal intervention, or a synaptic eligibility trace. This v7 work therefore asks what is actually established, what is blocked, and what experiment could distinguish NFOT from ordinary latency explanations.

## 2. Related work

Official bigP3BCI documentation distinguishes phase, stimulus, target, selection, and feedback fields. Timing studies in P300 and restorative BCIs show paradigm-specific effects rather than a universal optimum. Ex vivo plasticity studies support transient eligibility states gated by later neuromodulatory signals, but do not identify behavioral BCI intervals with synaptic traces. Human neurofeedback and educational studies show that timing can affect outcomes conditionally. Mixed-effects and grouped-validation methods establish that repeated observations require participant-aware uncertainty and that unseen-participant claims require participant-separated evaluation. Independent timing studies show that software timestamps and physical display transitions are not interchangeable.

## 3. Operational definition

`L` is defined as the difference between a protocol-specified feedback endpoint and initiating event on a shared or reconciled clock. The exact events, units, phase context, valid window, measurement uncertainty, and exclusion rules must be frozen before analysis. In the current guarded implementation, `StimulusBegin` and `DisplayResult` are candidate event channels, while `CurrentTarget` and `SelectedTarget` support label construction only after source audit. `StimulusType` is not accepted as a character identifier.

## 4. Research questions and hypotheses

The descriptive question concerns the distribution of verified gaps. The within-person question asks whether deviations from a participant's typical gap associate with an observed outcome. The predictive question asks whether a prespecified gap or history feature improves a fair baseline under a defined deployment split. The causal question asks whether randomized post-selection feedback delay affects a subsequent outcome. The biological question asks whether any behavioral timing pattern is linked to a measured physiological mechanism. These are distinct hypotheses.

## 5. Dataset and provenance

The baseline commit is `a2d88e922e19fd087dd0c2e0892684085d0fd9a8` on branch `nfot-v7-validation`. The repository contains the v5 PDF, a 444-row derived table, a 12-row prototype table, scripts, requirements, and tests. The two tracked source CSV placeholders are empty. Raw EDFs, complete event streams, converter metadata, inclusion/exclusion logs, and held-out predictions are unavailable. The v6 pull request remains open; it is not merged into `main`.

## 6. Event-extraction methodology

The guarded extractor requires explicit timestamp units and source-export confirmation. It cleans headers, rejects duplicates and invalid numeric data, checks documented phase values, detects rising edges, requires feedback edges in the post-trial phase, requires a unique target and selection, records source row indices, and creates a manifest. It does not run honestly without source data. The preserved derived table is not silently replaced.

## 7. Statistical methods

The primary future observational analysis is a participant-aware binary-outcome model separating within-person gap deviation from between-person typical gap. Candidate covariates are limited to source-verified variables such as trial order, session, flash count, and target class. Distributional features are hypotheses and must be selected before confirmatory evaluation. Prediction to new participants uses grouped outer splits with all feature construction and tuning inside training data. Future-trial prediction uses time-ordered splits. Model differences require paired uncertainty and calibration metrics.

## 8. Results

The available derived table contains 444 rows, 15 subjects, and 74 files. It contains 368 correct and 76 incorrect coded outcomes, for 82.8829% stored accuracy. Mean `L_s` is 7.0602477 s, sample SD is 3.3209017 s, median is 6.125 s, minimum is 1.875 s, and maximum is 15.0 s. All rows satisfy `L_s = tfb_s - t0_s` at `1e-12` tolerance. No missing values or duplicate `(file, trial)` identifiers were found.

These results are descriptive checks of the supplied artifact. No corrected source-level extraction, confirmatory association, fair benchmark, causal experiment, or biological measurement was completed. The v5 beta, p-value, LOSO slopes, threshold results, and AUC interval remain historical claims.

## 9. Robustness and sensitivity

The key sensitivity is source reconstruction. Once available, compare old and corrected rows, audit phase transitions, verify target labels, quantify missingness and exclusions, and test timing units. Statistical sensitivity should address participant weighting, order, session, flashes, influential participants, nonlinear terms chosen a priori, and alternative supported event definitions. A distributional feature that fails under grouped validation or does not beat a conventional latency baseline should not be retained as an NFOT-specific claim.

## 10. Theoretical interpretation

NFOT currently offers a candidate measurement framework. Existing temporal-credit-assignment and delayed-feedback literatures already explain why timing may influence later outcomes. NFOT would become more distinct only if a prespecified measurement or history feature adds reliable value beyond those baselines, or if a randomized timing manipulation produces a distinctive downstream pattern. The current data cannot identify a biological mechanism.

## 11. Alternative explanations

Longer gaps may mark harder trials, more flashes, fatigue, learning, session state, device processing, display buffering, or target/label errors. Participant-level differences may generate between-person associations. Model selection and thresholding may inflate retrospective results. Software command timestamps may not represent physical display onset. These alternatives are more plausible than a new biological theory until source validation and prospective tests address them.

## 12. Limitations

The central limitations are absent source recordings, unresolved event semantics, small reported participant count, unavailable historical model outputs, lack of independent replication, and no completed causal intervention. The manuscript does not claim a neural mechanism, clinical value, educational benefit, or breakthrough.

## 13. Falsification criteria

NFOT is weakened if the gap cannot be reconstructed, the historical association disappears after verified extraction and confounder checks, distributional features do not beat a conventional baseline, grouped prediction fails, or randomized delay has no prespecified downstream effect. It should be narrowed to timing instrumentation if no distinct predictive or causal value remains.

## 14. Prospective validation protocol

The proposed experiment randomizes post-selection feedback delay and measures a subsequent fixed outcome. Exact conditions, primary outcome, sample size, timing instrumentation, and stopping rules remain unresolved and must be fixed before ethics review and confirmatory enrollment. Same-trial correctness is not the primary causal outcome because the response precedes the manipulated delay.

## 15. Reproducibility statement

Available checks are run by `python3 -m unittest discover -s tests -p 'test_*.py' -v`, Python compilation, structural audit, timing arithmetic audit, and descriptive analysis. Synthetic planning output is generated by `analysis/v7_power_simulation.py` and is explicitly non-empirical. No source-level reproduction is possible from the current checkout.

## 16. Ethics and data governance

No human-subject research was conducted. Any future study requires appropriate supervision, ethics review, consent or assent, privacy safeguards, data minimization, and a documented withdrawal/deviation policy. No restricted data should be downloaded or redistributed without permission.

## 17. Conclusion

NFOT is currently a testable research programme centered on a potentially useful event-timing measure. The strongest supported result is arithmetic coherence of a derived table, not an independently replicated scientific effect. The decisive next step is recovery and audit of the source event data, followed by a randomized downstream-outcome experiment if the measurement survives.

## References

[1]: https://doi.org/10.13026/0byy-ry86 "Official bigP3BCI PhysioNet documentation and data dictionary"
[2]: https://doi.org/10.1109/EMBC.2015.7318856 "Effects of feedback latency on P300-based Brain-computer Interface"
[3]: https://doi.org/10.1098/rsos.170660 "Feedback update interval in restorative brain-computer interfaces"
[4]: https://doi.org/10.1016/j.neuron.2015.09.037 "Distinct eligibility traces for LTP and LTD"
[5]: https://doi.org/10.1111/ejn.13921 "Silent eligibility trace and dopamine-dependent plasticity"
[6]: https://doi.org/10.1001/archpsyc.61.3.310 "Mixed-effects models for repeated measures"
[7]: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html "GroupKFold documentation"
[8]: https://doi.org/10.1371/journal.pone.0085108 "Software timing errors in visual stimuli"
[9]: https://doi.org/10.7717/peerj.9414 "The timing mega-study"
