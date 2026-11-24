# Data directory

This directory separates historical derived data, small source-export artifacts, and prototype-generated trial data.

## Contents

- `historical_bigp3bci/` — pooled historical trial table retained from the previous `StimulusAnalysis(final)` directory. Preserve its provenance and do not treat it as raw EDF data.
- `source_exports/` — small CSV export artifacts previously stored under `analysis/csv/`. Their current contents are preserved exactly; inspect and validate them before relying on them.
- `prototype/` — trial-level CSV output associated with the interactive timing prototype.

## Data-handling rules

1. Never overwrite original source data with cleaned or transformed data.
2. Record dataset source/version, checksums where practical, event semantics, timestamp units, inclusion criteria, and transformation steps.
3. Keep derived data clearly labelled as derived.
4. Do not commit identifiable or sensitive participant information.
5. Do not claim source-level reproducibility from a derived table alone.
6. Treat prototype task data separately from historical BCI data; the prototype does not reproduce the historical analysis.
