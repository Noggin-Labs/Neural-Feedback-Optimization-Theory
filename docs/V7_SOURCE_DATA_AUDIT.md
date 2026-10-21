# NFOT v7 source-data audit

## Finding

Source-level reconstruction is **BLOCKED**. The checkout contains no raw EDF recordings, complete trusted event-stream exports, converter settings/version, source-row inclusion manifest, or authoritative Study M export capable of resolving the target-channel discrepancy.

The readable derived table has 444 rows and internally consistent stored timing arithmetic. That is not source recovery. The two tracked files under `analysis/csv/` are empty two-byte placeholders and cannot support extraction.

## Required source investigation

The authoritative bigP3BCI data dictionary documents `PhaseInSequence`, `StimulusBegin`, `StimulusType`, character channels, `CurrentTarget`, `SelectedTarget`, and `DisplayResult`. The guarded extractor therefore requires explicit unit confirmation and uses `CurrentTarget` rather than treating binary `StimulusType` as a character index. It rejects ambiguous or incomplete trials.

A valid source recovery must report event-row indices, file/session/participant identifiers, phase transitions, duplicate or missing events, target and selection values, timestamp units, trial exclusions, and a source-to-derived crosswalk. It must compare the reconstructed rows with the preserved 444-row table without overwriting it.

## Status by check

- Missing onset: not assessable without source events.
- Missing feedback: not assessable without source events.
- Duplicate/out-of-order events: not assessable without source events.
- Negative or zero gaps: no negative gaps in the derived table; source semantics unresolved.
- Clock discontinuities and units: blocked.
- Phase transitions: blocked.
- Target validity: blocked by the `CurrentTarget`/`StimulusType` discrepancy.
- Trial linkage and participant IDs: derived identifiers are internally unique; source linkage blocked.
- Historical 444-row extraction: reported/derived-table arithmetic only.

## Inclusion/exclusion manifest status

No source-level manifest can be generated honestly. `analysis/v7_source_manifest.json` records this explicitly rather than fabricating rows or exclusions.
