# NFOT v7 reproducibility guide

The repository separates historical artifacts, v6 audits, and v7 planning work. Source-level extraction is blocked because raw EDF files, complete event streams, converter metadata, and an inclusion manifest are absent. The existing derived table must therefore be treated as a preserved artifact, not as a verified source reconstruction.

Create an environment from `requirements.txt`, then run the available checks:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m py_compile analysis/*.py nfot_dataset_audit.py
python3 nfot_dataset_audit.py . --output /tmp/nfot_structural_audit.json
python3 analysis/audit_v5.py 'StimulusAnalysis(final)/pooled_trials_full (1).csv' \
  --output-dir /tmp/nfot_timing_audit --participant-col subject \
  --t0-col t0_s --feedback-col tfb_s --gap-col L_s --outcome-col Y
python3 analysis/analyze_trials.py \
  'StimulusAnalysis(final)/pooled_trials_full (1).csv' \
  --outdir /tmp/nfot_available_analysis
python3 analysis/v7_power_simulation.py --output /tmp/nfot_v7_synthetic_power.json
```

The first analyses report structural and arithmetic properties of the supplied derived table only. They do not validate event semantics or target labels. The extractor requires `--time-unit` and `--confirm-studyM-export`; it should not be run on fabricated or unverified inputs. A valid source-level run must preserve source row identifiers, a manifest, exclusions, units, and a machine-readable discrepancy report.

The power script generates synthetic planning output only. It does not use NFOT observations and must not be cited as empirical evidence. No command in this guide conducts human-subject research, submits ethics material, publishes a manuscript, or creates a release.
