# NFOT v5 forensic audit report

**Audit branch:** `nfot-v6-audit`  
**Repository commit audited:** `88045e34d8b63243459a85945830bb167818b17d`  
**Audit scope:** repository contents available at the commit above; no private files or raw recordings were assumed.

## Executive finding

The repository preserves a v5 PDF, a 444-row derived trial table, scripts, documentation, and a 12-row timing-prototype CSV. It does **not** preserve the raw EDF recordings, the complete converted event-stream CSV inputs, an inclusion manifest, the original v5 analysis environment, or the exact code that generated every reported inferential statistic. Two tracked files that appear to be source CSVs are empty two-byte files. Therefore the historical extraction and major inferential claims are **NOT REPRODUCIBLE FROM AVAILABLE REPOSITORY CONTENTS**. The available derived table reproduces several descriptive arithmetic quantities, but that is not independent validation of event semantics or labels.

## Files inspected

The tracked repository files were inventoried with `git ls-files -s`, `file`, SHA-1 index entries, and file-size checks. Key inputs are:

- `Neural_Feedback_Optimization_Theory__NFOT_ (3).pdf`: 11-page v5 PDF, 263,396 bytes.
- `StimulusAnalysis(final)/pooled_trials_full (1).csv`: 444 rows, 14 columns, SHA-256 `2b030f2cec7a6d357b21b81cf050d02f6d2556a3aa55bd29a0876cfdf5074105`.
- `nfot_interactive_trials.csv`: 12 rows, 25 columns, SHA-256 `0143e3570fd452d11667e8c8f42c4717ae577390e1b9de1e18d4b96743ec456f`.
- `analysis/csv/M_04_SE001_ADdiff_Test01.csv` and `Test02.csv`: each two bytes and empty; pandas cannot parse them.
- `VampireBCI/nfot_final.py`, `analysis/extract.py`, `analysis/pool.py`, `analysis/audit_v5.py`, `analysis/analyze.py`, and the malformed original `analysis/analyze_trials.py`.
- Existing documentation under `docs/`, including the v5 evidence ledger and validation pipeline.

Raw EDF files, converter logs/settings, original analysis outputs, source-level row identifiers, a v5 inclusion manifest, and the dataset version archive are unavailable in this checkout.

## Recomputed facts from the supplied derived table

The 444-row table contains 15 subjects: `M_04`, `M_05`, `M_06`, `M_09`–`M_20`. It contains 74 files, one session, and five test labels. There are 368 correct and 76 incorrect rows, giving 82.8829% accuracy. The supplied columns give mean `L_s = 7.0602477 s`, sample SD `3.3209017 s`, minimum 1.875 s, median 6.125 s, and maximum 15.0 s. `L_s` equals `tfb_s - t0_s` in all 444 rows at a tolerance of `1e-12`. There are no missing values, full-row duplicates, or duplicate `(file, trial)` identifiers in this table.

These are **derived-table arithmetic checks**, not a verified re-extraction. The table itself does not establish that `t0_s`, `tfb_s`, `true_target`, or `Y` have the intended source semantics.

## Historical claim classifications

| Historical item | Classification | Evidence and limitation |
|---|---|---|
| 444 trials and 15 participants | **PASS — derived-table count only** | Counts and subject list are present in the tracked table. The exact original inclusion process is unavailable. |
| 82.9% accuracy (368/444) | **PASS — derived-table arithmetic only** | `Y` yields 368/444. Label provenance is unresolved. |
| Mean WBG 7.06 s and SD 3.32 s | **PASS — derived-table arithmetic only** | Recomputed from `L_s`; source event semantics and units are not independently verified. |
| Negative within-participant coefficient `β=-0.111, p=.030` | **UNRESOLVED** | The repository does not contain the exact historical model code, output, or verified source inputs. |
| Negative LOSO slope in 15/15 folds | **UNRESOLVED** | Held-out folds, preprocessing, model selection, and predictions are not supplied. |
| AUC 0.656 versus 0.731, Δ=.076, CI [.021,.131] | **UNRESOLVED** | The target definition, fold predictions, bootstrap procedure, and model code are not supplied. |
| Target reconstruction checked against 4,192/4,192 events | **UNRESOLVED** | No event-level source table or audit trace is present. |
| `CurrentTarget` versus `StimulusType` semantics | **UNRESOLVED / BLOCKER** | The repository documents a conflict. No raw EDF or complete converted event stream is available to resolve it. |
| Historical v5 extraction | **FAIL — reproducibility gate** | Required source inputs and exact provenance are absent. This is not a finding that the published values are false. |

## Commands actually executed

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
python3 -m py_compile analysis/*.py nfot_dataset_audit.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 analysis/analyze_trials.py 'StimulusAnalysis(final)/pooled_trials_full (1).csv' --outdir /tmp/nfot_v6_available
```

## Highest-priority blockers

The next researcher must obtain the exact bigP3BCI Study M source recordings or a complete, trusted event-stream export; the converter version and settings; the original v5 file/participant manifest; and the exact historical inferential-analysis code and outputs. The `CurrentTarget` discrepancy must be resolved against the authoritative source representation before any corrected label analysis is treated as verified.
