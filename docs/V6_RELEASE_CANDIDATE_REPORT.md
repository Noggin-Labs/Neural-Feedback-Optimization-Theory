# NFOT v6 release-candidate report

**Branch:** `nfot-v6-audit`  
**Base commit:** `88045e34d8b63243459a85945830bb167818b17d`  
**Publication/push:** None. No release was published and no GitHub push was performed.

## Work completed

The repository was cloned and audited non-destructively. A separate working branch was created. Git history, tracked files, file types, hashes, the v5 PDF, documentation, scripts, tests, CSV schemas, missingness, duplicates, timing arithmetic, and participant/file counts were inspected.

A forensic v5 audit, v6 validation report, results-provenance ledger, theory review, prospective protocol draft, manuscript draft, and literature research archive were added under `docs/` and `research/v6_sources/`. The manuscript uses the provisional title requested by the mission and explicitly states that prospective validation has not occurred.

The malformed `analysis/analyze_trials.py` was replaced with a small deterministic descriptive-analysis entry point that accepts the repository’s actual derived-table schema and fails closed on invalid timing, labels, missingness, and duplicate identifiers. The truncated `analysis/extract.py` was completed as a guarded event-based extractor with explicit time-unit and source-export confirmation requirements. Optional scikit-learn imports in `analysis/analyze.py` were made lazy so deterministic safety helpers do not fail at import time when predictive-analysis dependencies are absent. The stale target-label statement in `analysis/README.md` and the main README feedback-event wording were corrected.

Seven dependency-light unit tests now pass. Research notes cite official bigP3BCI documentation, primary BCI-timing studies, primary eligibility-trace studies, neuroadaptive educational systems, repeated-measures and grouped-validation methods, causal feedback-learning experiments, and physical display-timing validation.

## Commands and tests executed

```text
git rev-parse HEAD
git status --short --branch
git log --oneline --decorate -20
git ls-files -s
file <tracked files>
pdfinfo 'Neural_Feedback_Optimization_Theory__NFOT_ (3).pdf'
pdftotext -layout 'Neural_Feedback_Optimization_Theory__NFOT_ (3).pdf' /tmp/nfot_v5.txt
python3 nfot_dataset_audit.py . --output /tmp/nfot_structural_audit.json
python3 analysis/audit_v5.py 'StimulusAnalysis(final)/pooled_trials_full (1).csv' --output-dir /tmp/nfot_v5_audit --participant-col subject --t0-col t0_s --feedback-col tfb_s --gap-col L_s --outcome-col Y
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m py_compile analysis/*.py nfot_dataset_audit.py
python3 analysis/analyze_trials.py 'StimulusAnalysis(final)/pooled_trials_full (1).csv' --outdir /tmp/nfot_v6_available
git diff --check
```

Final test result: **7 tests passed**. Python syntax checks passed. The structural audit found four tables: one readable 444-row derived table, one readable 12-row prototype table, and two empty two-byte CSVs that could not be parsed.

## Verified findings

The available derived table contains 444 rows, 15 subjects, and 74 files. It contains 368 coded correct outcomes and 76 incorrect outcomes, for 82.8829% stored accuracy. Mean `L_s` is 7.0602477 s and sample SD is 3.3209017 s. All stored gaps equal `tfb_s - t0_s` at `1e-12` tolerance; no missing values or duplicate `(file, trial)` identifiers were found.

The v5 PDF reports additional inferential values, but those values were not independently reproduced. Official bigP3BCI documentation supports phase-aware event interpretation and identifies `CurrentTarget` as the character-target field and `StimulusType` as a binary target/non-target stimulus marker. The historical repository claim that `StimulusType` contains character indices remains unresolved because the raw source data are missing.

The literature review supports a cautious conclusion: feedback timing can matter, but effects are conditional on task, timing target, outcome, and measurement layer. No reviewed evidence establishes a universal optimal delay or a biological mechanism for NFOT. Physical display onset must be independently measured when that level of claim matters.

## Unresolved issues and known limitations

The raw EDF recordings, complete event-stream exports, converter settings, original v5 inclusion manifest, exact historical inferential code, held-out predictions, and bootstrap outputs are absent. Therefore source-level event semantics, timestamp units, target-label validity, trial linkage, the historical within-participant coefficient, LOSO result, AUC result, and the 4,192/4,192 reconstruction check remain unresolved. Derived-table arithmetic must not be described as corrected extraction or independent replication.

The current guarded extractor is a code correction and testable foundation, not a validated result. Its source-level execution must wait for the missing data and a documented audit of the Study M export. The prospective protocol remains a draft pending qualified supervision, ethics/privacy review, engineering feasibility, and a frozen primary estimand and sample-size rationale.

## Remaining prerequisites for a defensible v6 release

1. Obtain the raw or complete trusted source event streams and their provenance.
2. Resolve the `CurrentTarget`/`StimulusType` discrepancy against source evidence.
3. Re-extract with source row identifiers, explicit exclusions, and an old-to-new crosswalk.
4. Recompute observational models with participant-aware uncertainty and frozen feature definitions.
5. Reproduce or formally downgrade the historical beta, LOSO, threshold, dispersion, and AUC claims.
6. Freeze and review the prospective protocol, including timing validation, primary downstream outcome, power rationale, stopping rules, and ethics safeguards.
7. Conduct an independent review before any publication or push.

## Single highest-priority next action

**Obtain the exact Study M raw EDF recordings or complete converted event-stream files, together with converter/version metadata and the original v5 inclusion manifest, then resolve the target-label discrepancy before accepting any corrected NFOT statistic.**
