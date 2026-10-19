# NFOT v6 validation pipeline and release gates

## Phase 0 — preserve what was previously reported

1. Freeze the v5 PDF/preprint, original source code, environment/requirements, trial-level dataset, analysis notebook/scripts, participant inclusion list and all output tables in a read-only archive.
2. Hash each source file (SHA-256); record dataset version, converter version/settings, and command-line invocations.
3. Do not overwrite the v5 extraction output. New extraction is a new versioned dataset.

**Gate 0:** source artefacts exist, filenames and hashes recorded, and the exact v5 subject/file inclusion list is available. If the original analysis code/data cannot be recovered, report that exact reproduction is impossible and label new work a reanalysis, not a reproduction.

## Phase 1 — dataset dictionary + signal audit

Official bigP3BCI v1.0.0 dictionary:

| Signal | Documented meaning | Extraction role |
|---|---|---|
| `PhaseInSequence` | 0 pre-run, 1 pre-trial, 2 during trial, 3 post-trial | Segment phase-2 trial blocks |
| `StimulusBegin` | 0 stimulus off, 1 stimulus on | Detect 0→1 stimulus-onset edges within phase 2 |
| `StimulusType` | 0 non-target stimulus event and 1 target stimulus event when `StimulusBegin=1` | Diagnostic event type only; never the character index |
| `CurrentTarget` | Target character index during phase 2 | Trial target label source |
| `SelectedTarget` | Predicted target character index in phase 3 | Predicted character value at feedback |
| `DisplayResult` | 0 feedback not presented, 1 feedback presented | Detect feedback 0→1 edge (`tfb`) |

The dictionary is generic across the dataset. It does **not** prove that a particular local CSV export retained names, units, timing, or values correctly. In particular, a reported all-zero `CurrentTarget` column in an ADdiff CSV is a data-conversion discrepancy to investigate, not a reason to reinterpret binary `StimulusType` as a character index.

Run audit-only on a small sample from each condition / recording source before extracting all files. Compare event transitions in CSV against raw EDF channels or a separately verified export. Inspect at least several trials from early, middle and late recording sections. Include edge rows and adjacent rows in the audit trace.

**Gate 1:** `Time` unit confirmed; phase codes conform; phase-2 blocks correspond to target-character trials; stimulus and feedback edges align with raw EDF; `CurrentTarget` values are understood; `SelectedTarget` is available at feedback time; trial pairing is 1:1. Ambiguity means stop and investigate.

## Phase 2 — create a corrected, auditable extraction

For each complete trial:

- `t0`: first `StimulusBegin` 0→1 edge while `PhaseInSequence == 2`.
- `tfb`: `DisplayResult` 0→1 edge associated with that trial in phase 3.
- `Target`: the unique positive `CurrentTarget` index observed during phase 2.
- `SelectedTarget`: predicted character index at the phase-3 feedback edge.
- `L = tfb - t0` in seconds; reject nonpositive values.
- `Y = 1(SelectedTarget == Target)`.

Keep source row indexes for `t0` and `tfb`, full precision, source filename, and a manifest. Record every exclusion with reason. Never infer a character target from `StimulusType`. If target/selected value timing does not fit this convention, inspect and resolve it rather than silently using nearest timestamps.

**Gate 2:** automated tests pass; spot-check audit trails pass; no silent trial dropping; the new sample counts and exclusion reasons are explainable.

## Phase 3 — reconcile old and corrected outputs

If the original v5 output exists, join old/new rows using stable identifiers that do not depend on rounded L alone (source file + event row indices or a verified trial identity). Produce:

1. Trial-flow counts by subject/file: raw candidate trials → eligible paired trials → excluded trials and reasons.
2. Target disagreement and correctness-label disagreement tables.
3. `t0_old`, `t0_new`, `tfb_old`, `tfb_new`, `L_old`, `L_new` differences.
4. Per-subject and overall summaries for old and corrected data.
5. A written log of all differences and their causes.

Do not force one-to-one matching if a stable crosswalk cannot be established. Report unmatched trials separately.

**Gate 3:** every difference in count, label or timestamp is explained or explicitly marked unresolved. No v5 numerical claim is treated as validated before this gate.

## Phase 4 — analysis plan before looking at corrected outcomes

### Primary observational estimands

1. **Within-participant association:** the relationship between within-person-centered L and same-trial Y, with participant clustering. Report effect estimate, confidence interval, and heterogeneity rather than only a p-value.
2. **Between-participant incremental value:** does the prespecified participant/session-level dispersion statistic improve prediction of participant accuracy beyond mean L? Independent unit is the participant/session. This is not a trial-level SD predictor when one SD is computed per person.

Choose one primary dispersion statistic (for example, session SD or IQR) before the corrected-outcome analysis. Secondary statistics can be reported transparently with multiplicity correction or explicitly marked exploratory.

### Required sensitivity checks

- Mean-only vs mean-plus-dispersion; report coefficient changes, CIs, calibration and predictive scoring.
- Participant-level bootstrap (resample participants, not individual trials) for between-person claims.
- Leave-one-participant-out influence analysis.
- Remove-one-subject-at-a-time estimates and plots.
- Trial-order / time-on-task sensitivity; stimulus count and trial duration where available.
- Alternative predeclared target/feedback edge interpretations only if the raw documentation supports them; no outcome-guided signal selection.
- Missingness / excluded-trial analysis by participant and condition.
- Verify target indexing matches `SelectedTarget` numbering (both represent the same character index convention).

### Model-validation rules

- Keep train/validation/test partitions grouped by participant for between-person predictions.
- All feature engineering and model tuning happen inside training folds.
- Compare baseline mean-only model to mean-plus-dispersion model on identical held-out participants.
- Report fold-wise predictions, metric definitions, confidence intervals, calibration, and a baseline/null comparator.
- Do not compute a high/low accuracy AUC without documenting the binary outcome threshold and why that threshold is meaningful.
- If AUC is reported, it must be generated from out-of-fold or independent predictions; compare paired AUCs on the same independent units.

**Gate 4:** locked analysis code reproduces the final tables from the newly extracted trial table, with all model and split details recorded.

## Phase 5 — conclusions and external replication

Classify each original claim as reproduced, weakened, not reproduced, or not testable with these data. A corrected association in this dataset is not external replication and is not proof of mechanism. Identify a second compatible cohort/condition and freeze the analysis before viewing its outcome data.

**Gate 5:** observational evidence is honestly characterized; PTSP's primary causal question and estimand are clear; design review by a qualified research mentor is complete.

## PTSP readiness checklist

PTSP can be finalized only after all measurement/analysis gates above are passed or remaining blockers are explicitly accepted in a protocol amendment. The preregistration needs to state whether the primary question is:

- an **observational current-trial prediction** (WBG and same-trial correctness), or
- a **causal downstream feedback-timing effect** (randomized delay after current selection, with future behavior/performance as the outcome).

These are not the same estimand. A feedback delay assigned after a selection cannot change whether that already-made selection matched the target.
