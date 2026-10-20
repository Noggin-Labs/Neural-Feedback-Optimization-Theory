# NFOT v6 measurement validation report

**Status:** release-candidate audit; not a validated re-extraction.

## Scope and evidence boundary

This report evaluates the files present at commit `88045e34d8b63243459a85945830bb167818b17d`. The repository contains a derived trial table, not the raw EDF recordings or complete source event streams. Consequently, validation of event meaning, phase transitions, time units, target labels, and trial linkage is blocked at the source-data level.

## Operational definition under review

The intended measurement is `L = t_fb - t0`, with `t0` as the first verified stimulus-onset event in the relevant trial phase and `t_fb` as the first verified feedback-display event in the appropriate feedback phase. The repository’s guarded extractor uses `StimulusBegin`, `DisplayResult`, `CurrentTarget`, and `SelectedTarget`, and explicitly refuses to infer character identity from `StimulusType`. This is the scientifically safer implementation, but it has not been executed on the missing source files.

## Gate results

| Gate | Status | Finding |
|---|---|---|
| File/schema integrity of supplied derived table | **PASS** | 444 rows; required timing and outcome fields are complete; no duplicate `(file, trial)` identifiers. |
| Arithmetic identity `L_s = tfb_s - t0_s` | **PASS** | All 444 rows match at `1e-12` tolerance. |
| Nonnegative and ordered derived timestamps | **PASS** | No negative gaps or reversed `t0_s`/`tfb_s` values in the derived table. |
| Source time unit | **UNRESOLVED** | No raw source or converter metadata is available. |
| Phase-code semantics and event transitions | **UNRESOLVED** | No complete event stream or raw EDF is available. |
| `CurrentTarget` label validity | **UNRESOLVED** | The repository records a conflict between the official dictionary and legacy Study M extraction. |
| `StimulusType` as target character identity | **FAIL** | The guarded v6 extractor correctly rejects this interpretation absent authoritative evidence. |
| One-to-one trial linkage | **UNRESOLVED** | Derived identifiers are unique, but source event-level linkage cannot be checked. |
| Physical display onset equivalence | **FAIL for the available prototype** | The timing prototype explicitly records a software-command proxy and `physical_display_timing_verified=False`. |
| Corrected source-level extraction | **BLOCKED** | Required raw/converted inputs are missing. |

## Implemented safeguards

`analysis/extract.py` now documents the event mapping and fails closed on empty inputs, duplicate headers, ambiguous feedback-column aliases, invalid time units, ambiguous segmentation, missing target values, nonpositive gaps, and unsupported labels. `analysis/analyze_trials.py` validates required columns, numeric and binary domains, timing arithmetic, nonnegative intervals, and duplicate trial identifiers before producing descriptive output.

The new `tests/test_v6_validation.py` covers valid output creation, timing mismatch rejection, duplicate trial rejection, invalid binary-label rejection, and participant grouping. The existing rolling-variance safety tests were converted from an unavailable pytest-only form to standard-library `unittest` without changing their tested behavior.

## Required source-level validation before a defensible v6 release

Obtain and hash the raw EDFs or complete converted event streams. Record the authoritative data dictionary, converter version and settings, and exact commands. Audit early, middle, and late recording sections. Confirm `Time` units, `PhaseInSequence` transitions, `StimulusBegin` onset edges, `DisplayResult` feedback edges, `CurrentTarget` values, `SelectedTarget` timing, and one-to-one trial pairing. Preserve row-level source indices and an exclusion manifest. Then compare old and corrected extractions without overwriting the v5-derived table.
