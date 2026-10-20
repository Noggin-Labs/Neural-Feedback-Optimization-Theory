# NFOT v6 results provenance

**Repository commit:** `88045e34d8b63243459a85945830bb167818b17d`  
**Working branch:** `nfot-v6-audit`  
**Python:** 3.12.3  
**Available packages used:** NumPy 2.5.3 and pandas 3.0.6. SciPy, scikit-learn, statsmodels, and pytest were not installed in the initial environment.

## Provenance ledger

| Result or check | Input and hash | Code | Command | Status |
|---|---|---|---|---|
| Structural inventory | All tracked repository files at the commit above | Shell/Git commands | `git ls-files -s`, `file`, `git rev-parse HEAD` | Executed |
| Derived-table row count and schema | `StimulusAnalysis(final)/pooled_trials_full (1).csv`; SHA-256 `2b030f2cec7a6d357b21b81cf050d02f6d2556a3aa55bd29a0876cfdf5074105` | `nfot_dataset_audit.py` | `python3 nfot_dataset_audit.py . --output /tmp/nfot_structural_audit.json` | Executed |
| Arithmetic timing audit | Same 444-row table | `analysis/audit_v5.py` | `python3 analysis/audit_v5.py ... --t0-col t0_s --feedback-col tfb_s --gap-col L_s --outcome-col Y` | Executed; 0 mismatches |
| 444 / 15 counts | Same derived table | `analysis/analyze_trials.py` | `python3 analysis/analyze_trials.py ... --outdir /tmp/nfot_v6_available` | Executed |
| 82.8829% accuracy | Same derived table | `analysis/analyze_trials.py` | Same command | Executed; derived-table arithmetic only |
| Mean 7.0602477 s, SD 3.3209017 s | Same derived table | `analysis/analyze_trials.py` | Same command | Executed; derived-table arithmetic only |
| Historical beta, p-value, LOSO, and AUC claims | Raw EDFs, complete event streams, original inferential code, and prediction outputs | Not available | No valid reproduction command exists from this checkout | **NOT REPRODUCIBLE FROM AVAILABLE REPOSITORY CONTENTS** |
| Prototype delay balance and arithmetic | `nfot_interactive_trials.csv`; SHA-256 `0143e3570fd452d11667e8c8f42c4717ae577390e1b9de1e18d4b96743ec456f` | CSV/schema inspection | pandas structural audit | Executed; 12 rows, four per assigned delay |

## Output interpretation

The available-table results are descriptive reanalysis of a supplied derived artifact. They do not independently establish that the artifact was extracted with correct event semantics, time units, target labels, or trial boundaries. No corrected source-level results are reported because the necessary source evidence is absent.

## Reproducibility limitations

The repository does not pin a full environment, does not include raw EDFs, does not include the original v5 analysis outputs, and includes a malformed historical `analysis/analyze_trials.py` entry point that was repaired on this audit branch. The repair is intentionally narrow and does not claim to recreate the missing v5 inferential pipeline.
