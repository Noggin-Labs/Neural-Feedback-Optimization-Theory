# NFOT v7 final mission report

## A. Executive verdict

NFOT is not currently a demonstrated breakthrough. It is a scientifically testable research programme with a potentially useful timing-measurement and validation framework. The available evidence establishes arithmetic coherence of a derived table and supports further investigation; it does not establish source-level reproducibility, a causal effect, added predictive value, or a biological mechanism.

## B. What changed

V7 added a baseline/scope record, source-data audit, machine-readable blocked manifest, hostile claim ledger, statistical plan, formal model, prospective protocol, preregistration draft, synthetic power-sensitivity script, falsification matrix, literature review, novelty matrix, neuroscience mechanism review, application assessment, benchmark specification, red-team review, breakthrough-readiness scorecard, reproducibility guide, manuscript, supplementary methods, bibliography, changelog, and release checklist. README and research-status documents were updated.

## C. What the data establish

The preserved derived table contains 444 rows, 15 subjects, and 74 files. It contains 368 coded correct outcomes and 76 incorrect outcomes. Stored accuracy is 82.8829%; mean gap is 7.0602477 s; sample SD is 3.3209017 s; and every stored gap equals `tfb_s - t0_s` at `1e-12` tolerance. These are derived-artifact arithmetic results. No independent source-level empirical finding was reproduced.

## D. What remains unverified

Raw event semantics, timestamp units, physical display timing, target-label validity, source trial linkage, inclusion/exclusion history, historical beta/p-value, LOSO predictions, threshold effects, AUC interval, distributional added value, causal effects, independent replication, and biological interpretation remain unverified or blocked.

## E. The strongest scientific contribution

The strongest contribution is a disciplined framework that separates event measurement, descriptive association, participant-aware prediction, causal timing manipulation, and biological interpretation while preserving the historical record. This is narrower than a new theory, but scientifically useful if it leads to independently reproducible timing measurements and fair tests.

## F. The strongest competing explanation

The most plausible explanation is ordinary task/interface latency confounding: harder trials, flash count, order, fatigue, participant state, processing and display timing may increase the measured gap and reduce accuracy without any NFOT-specific mechanism. Source reconstruction and a randomized downstream-outcome experiment are the discriminating tests.

## G. The decisive next experiment

Proposed experiment: randomize post-selection feedback delay, verify achieved and physical timing, and measure a prespecified subsequent performance or learning outcome. Analyze assigned condition by intention-to-treat with participant clustering. Falsification is a null/opposite downstream contrast, failed timing delivery, or an effect explained by order or technical artifacts. No experiment has been conducted.

## H. Reproducibility

Executed commands included `python3 -m unittest discover -s tests -p 'test_*.py' -v`, `python3 -m py_compile analysis/*.py nfot_dataset_audit.py`, `python3 nfot_dataset_audit.py . --output ...`, `python3 analysis/audit_v5.py ...`, `python3 analysis/analyze_trials.py ...`, `python3 analysis/v7_power_simulation.py ...`, and `git diff --check`. The source-level extractor could not be run because required source data are unavailable. No command conducted human research or publication.

## I. Repository status

Branch: `nfot-v7-validation`. Baseline commit: `a2d88e922e19fd087dd0c2e0892684085d0fd9a8`. At the time of v7 baseline inspection, the working tree was clean, PR #1 was open, `origin/main` was `88045e3`, and no release existed. V7 changes are local and have not been pushed or merged.

## J. Breakthrough-readiness assessment

Measurement validity and provenance are blocked. Computational reproducibility is partially established. Statistical robustness is preliminary. Predictive generalization and causal identification are blocked/proposed. Theoretical specificity and novelty are preliminary. Independent replication and cross-task generality are not assessed. Biological mechanism is unsupported. Practical usefulness is preliminary within timing monitoring. These statuses are not averaged.

## K. Next three actions

1. Recover the raw EDFs or complete trusted event streams, converter metadata, permissions, and source manifest; resolve the target-channel discrepancy.
2. Reconstruct and lock the source-level extraction, then rerun the observational models and fair grouped benchmark with uncertainty.
3. Finalize the supervised, ethics-ready randomized downstream-outcome protocol and its design simulation; do not enroll until preregistered.

## L. Honest conclusion

NFOT is not a demonstrated breakthrough. It is a testable research programme. The strongest supported result is that the preserved derived table is internally arithmetically coherent. The most important missing evidence is source-level reconstruction from authoritative event data. Confidence would increase substantially after independent extraction, a fair validation benchmark, and a replicated randomized downstream timing effect. I would recommend abandoning or substantially narrowing the theory if the source association disappears, distributional features do not add value over ordinary latency, or randomized delay fails to produce the prespecified downstream pattern.
