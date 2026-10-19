# NFOT v6 evidence ledger — initial audit

Statuses: **documented** = supported by the official data dictionary; **reported** = quoted from the project's current notes but not independently reproduced here; **blocked** = cannot be accepted pending source-data or code verification; **hypothesis** = a testable interpretation, not an established result.

| ID | Claim | Current status | Required evidence / next test |
|---|---|---|---|
| E1 | `PhaseInSequence == 1` identifies first flash onset | **Contradicted by dictionary** | Phase 1 is pre-trial; identify the first `StimulusBegin` 0→1 transition during phase 2. |
| E2 | `StimulusType` gives the target character index | **Contradicted by dictionary** | Dictionary says it is binary target/non-target status for a stimulus; obtain target character index from `CurrentTarget` during phase 2 or another explicitly documented ground-truth channel. |
| E3 | `CurrentTarget` is all zero in Study M and cannot be used | **Blocked / source-data check needed** | Inspect actual M ADdiff converted CSVs and the original EDF in parallel; report nonzero counts by phase, file, and subject. If truly all zero, investigate conversion/channel mapping rather than substituting `StimulusType`. |
| E4 | `SelectedTarget` changes reliably identify every selection | **Not established** | A value-change detector can miss a repeated same-target selection. Compare with `DisplayResult` rising edges and inspect consecutive selections. |
| E5 | Operational WBG is `DisplayResult` rising edge minus first stimulus onset | **Definition, still needs implementation verification** | Fix `t0` as `StimulusBegin` rising edge within phase 2 and `tfb` as `DisplayResult` rising edge in phase 3; audit edge alignment sample-by-sample. |
| E6 | v5 contains 444 trials and 15 subjects | **Reported** | Recreate an inclusion manifest from source filenames and exclusion logs; recompute counts from extracted trials. |
| E7 | Subject range “M_04–M_20 excluding M_08” contains 15 subjects | **Arithmetic inconsistency to resolve** | IDs M_04 through M_20, excluding only M_08, yield 16 identifiers. Publish exact included subject list and explain any additional exclusion. |
| E8 | Longer WBG is associated with lower trial accuracy (`β = −0.111`, `p = .030`) | **Reported, not reproduced** | Re-run on corrected labels; use a within-participant effect, account for participant clustering and time-on-task; publish model formula, coding, convergence, CIs, and exact analysis table. |
| E9 | LOSO slopes are negative for all 15 subjects | **Reported, not reproduced** | Publish per-fold estimates and exact held-out unit; ensure no subject-level features, thresholds, scaling, or model selection leak from held-out subjects. |
| E10 | The upper-quartile cut (reported 8.88 s) and 12 s cut separate accuracy | **Reported / likely exploratory** | Recalculate on corrected WBG; establish whether the cutoffs were prespecified or selected after examining these data. Do not treat optimized cutoffs as confirmatory. |
| E11 | WBG SD predicts accuracy beyond mean WBG | **Central reported hypothesis; blocked pending reanalysis** | Identify the unit for SD (per participant/session vs rolling window), the independent sample size, the target outcome, and the model. If SD is per subject, the independent between-subject sample is the number of subjects, not the number of trials. Compare against mean-only model with participant-level resampling and held-out subjects. |
| E12 | AUC improves from 0.656 to 0.731 (reported Δ≈0.076) | **Reported, not reproducible from supplied information** | Specify the binary target being classified, the feature/model definitions, the train/test split unit, and the exact out-of-sample predictions. Compute paired ΔAUC CI on the same held-out units; prevent leakage and nested tuning errors. |
| E13 | 28.42 ms is a characteristic timescale | **Correctly removed from v5 per project notes** | Do not reintroduce without a derivation tied to defined variables and an independent preregistered test. |
| E14 | Lorentzian efficiency law is established | **Correctly removed from v5 per project notes** | Do not reintroduce without derivation, model comparison, calibration, and independent validation. |
| E15 | WBG variability has a causal effect on BCI performance | **Not established** | Observational association is not causal. PTSP must specify when timing is manipulated relative to selection and choose an outcome the intervention can affect. |

## Cross-cutting threats to validity

1. **Measurement validity:** the legacy `t0` and target-label code conflict with the general official data dictionary.
2. **Trial linkage:** each target, selection, feedback and stimulus must be verified as belonging to the same trial.
3. **Repeated measures:** trials are nested within participants; ordinary trial-level tests may underestimate uncertainty.
4. **Small between-subject sample:** a reported N of 15 creates fragile between-person models, especially models with multiple predictors.
5. **Outcome leakage:** a same-trial feedback delay occurs after the selected character is already decided; it cannot cause that same selection's correctness.
6. **Threshold/data snooping:** the reported cut points are exploratory unless fixed independently before the outcome analysis.
7. **Multiplicity:** many possible summaries (SD, variance, IQR, tail quantiles, thresholds) invite selective reporting; one primary feature/contrast must be prespecified.
8. **Generalization:** the ADdiff condition in one study may not generalize to other paradigms, devices, BCI users or real-time systems.

## Decision rule

Do not claim replication or move the central causal claim to PTSP until E1–E7 are resolved and the key inferential claims E8, E11 and E12 are either reproduced under a documented validation plan or explicitly downgraded/withdrawn.
