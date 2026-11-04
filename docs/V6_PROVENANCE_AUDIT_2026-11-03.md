# NFOT v6/v7 provenance audit — 2026-11-03

**Auditor:** Milestone sprint audit (independent re-run, not the original analyst).
**Repository state audited:** `Noggin-Labs/Neural-Feedback-Optimization-Theory`, branch `main`, commit `e2328cb`.
**Environment:** Python 3.12.3, NumPy 2.5.4, pandas 3.1.0, SciPy 1.18.1, scikit-learn 1.9.1, pytest.
**Classification scheme:** Verified / Reported / Hypothesis / Proposed / Unverified / Rejected (§2 of the directive).

This audit does not relabel any v7 draft as v6. Where v5/v6 documents and the current checkout disagree, both are recorded.

---

## 1. What was actually re-run

| Check | Command | Result | Class |
|---|---|---|---|
| Test suite | `pytest -q` in `repos/nfot` | **12 passed in 0.31 s** | Verified |
| Row count and schema | `read_trials()` on the pooled table | 444 rows; required columns present; `L_s == tfb_s - t0_s` for all rows at 1e-12 | Verified |
| Overall accuracy | direct recomputation | 0.8288288288288288 (368/444) | Verified |
| Mean Write-Back Gap | direct recomputation | 7.060247747747748 s | Verified |
| SD of Write-Back Gap | direct recomputation, `ddof=1` | 3.3209016809595377 s | Verified |
| Participant count | `groupby` | 15 (`M_04`–`M_20`, excluding `M_07`, `M_08`) | Verified |
| Recording count | `file` unique | 74 | Verified |
| Target decoding sanity | `Y == (selected_cell == true_target)` | 0 mismatches in 444 rows | Verified |
| Duplicate trial keys | `(file, trial)` unique | 0 duplicates | Verified |

The three headline descriptive figures are therefore **reproduced exactly**. They are arithmetic over a supplied derived table.

## 2. New findings from this audit

### 2.1 Timestamps are quantised to 0.125 s (125 ms) — Verified
Every value of `t0_s`, `tfb_s` and `L_s` is an exact multiple of 0.125 s. There are only 90 distinct `L_s` values across 444 trials. This is not documented in the repository's data dictionary or provenance notes.

**Consequence:** the table cannot support any claim about timing resolution finer than 125 ms, and a 125 ms grid against an SD of 3.32 s means the timing variable carries far less information than its four-significant-figure summary suggests. Any statement of the form "feedback completed X ms later" is not supportable from this artifact.

### 2.2 The Checkerboard condition is absent — Verified
All 74 recordings are `ADdiff` (`M_xx_SE001_ADdiff_TestNN.edf`). There are **0** `CB` recordings and 0 CB trials. Participants with both paradigms: **0 of 15**.

**Consequence:** the cross-paradigm analysis (directive Task 4.2) is **blocked at the data level**, not at the analysis-code level. `analysis/cross_paradigm.py` is delivered and its paired-analysis path is implemented, but it correctly refuses to run and emits the blocker plus an acquisition checklist.

### 2.3 One recording block is silently missing — Verified
The identifier scheme implies 15 participants × 5 test sessions = 75 recordings of 6 trials each (444/74 = 6 exactly). Observed: 74 recordings, and `M_19` contributes 24 trials instead of 30.

**Consequence:** exactly one 6-trial block is absent and no inclusion/exclusion manifest documents it. `analysis/v7_source_manifest.json` correctly reports `included_source_rows: null`, but does not note this specific gap.

### 2.4 The reported inferential statistics are not reproducible — Unverified / not reproducible
β = −0.111, p = 0.030, 15/15 negative LOSO coefficients, AUC 0.656→0.731 and CI [0.021, 0.131] all require the raw EDFs or complete trusted event streams, the original inferential code, and the original prediction outputs. None are present.

For calibration only, a naive pooled within-participant correlation computed here gives **r = −0.1123, p = 0.0179 (n = 444)**. The point estimate is close to the reported β, which is weakly encouraging, but this is **not** the reported result: it treats 444 clustered trials as independent, ignores participant random effects, and its p-value differs. It must not be cited as a reproduction.

### 2.5 Two tracked source CSVs are empty — Verified
`analysis/csv/M_04_SE001_ADdiff_Test01.csv` and `..._Test02.csv` are 2-byte placeholders. They cannot support extraction.

## 3. Provenance table

| Result / claim | Depends on | Reproducible from this checkout? | Class |
|---|---|---|---|
| 444 trials, 15 participants | pooled derived CSV | Yes | Verified |
| `L = tfb − t0` arithmetic identity | pooled derived CSV | Yes | Verified |
| Accuracy 0.8288 | pooled derived CSV | Yes | Verified |
| Mean L 7.060 s, SD 3.321 s | pooled derived CSV | Yes | Verified |
| Event semantics (`StimulusBegin`, `DisplayResult`, `CurrentTarget`) | raw EDF / event stream | **No** | Unverified |
| Timestamp units and conversion | converter metadata | **No** | Unverified |
| 125 ms quantisation | pooled derived CSV | Yes (new) | Verified |
| Within-participant β = −0.111 | original inferential code + data | **No** | Unverified |
| p = 0.030 | original inferential code + data | **No** | Unverified |
| 15/15 negative LOSO coefficients | per-fold outputs | **No** | Unverified |
| AUC 0.656 → 0.731, CI [0.021, 0.131] | prediction outputs + raw data | **No** | Unverified |
| Checkerboard comparison | CB recordings | **No** — absent | Blocked |
| Feedback-delay → learning causation | a randomised prospective study | **No** — none run | Hypothesis |
| Physical display-onset timing | photodiode/display instrumentation | **No** — software proxy only | Rejected for the prototype |

## 4. Consistency of the v6 manuscript with the code

The v6 documents are internally consistent with the code in the checkout: `docs/V6_VALIDATION_REPORT.md` claims PASS only for the derived-table integrity and arithmetic gates, and marks source-level gates UNRESOLVED or BLOCKED. That is accurate.

Remaining inconsistencies to fix before any v7 submission:

1. `docs/RESEARCH_STATUS.md` lists β, p, LOSO and AUC as "the documented V5 analysis" without marking them non-reproducible in the same paragraph. They should carry an explicit provenance tag.
2. No document discloses the 125 ms quantisation, which materially limits interpretation.
3. No document discloses that `M_19` is 6 trials short, i.e. that the 444 total is not a complete 75-recording design.
4. `docs/DATA_DICTIONARY.md` defines `t_fb` as the *rising edge of* `DisplayResults`. The actual key in `analysis/extract.py` is `DisplayResult` (singular). A reader cannot tell which is authoritative.

## 5. Statistical-unit assessment

- Trials are the observation unit; participants are the inference unit. Any model must treat trials as clustered within participant (and within recording).
- The naive pooled correlation reported in §2.4 illustrates the failure mode: n = 444 overstates information by roughly the cluster size.
- 15 participants is very few for a within-participant slope plus a predictive comparison. Any AUC difference should be reported with a participant-level, out-of-fold uncertainty interval, and 5-fold grouped CV over 15 participants means folds of 3 participants each — extremely unstable.
- The AUC comparison is only valid if both models are evaluated on identical rows and identical folds. `analysis/analyze.py` does use a shared complete-case sample and deterministic `GroupKFold`, which is correct, but its reported number cannot be re-obtained here because no prediction output is preserved.

## 6. What this audit changes

- Nothing in the existing v5/v6 record is overwritten. This file is additive.
- Three previously undocumented data properties are now recorded: 125 ms quantisation, absence of CB, one missing 6-trial block.
- The cross-paradigm deliverable is a documented blocker plus runnable code, not a fabricated comparison.
- The strongest defensible NFOT claim remains: **a documented, reproducible measurement-and-validation framework for asking whether event-defined feedback timing adds information beyond conventional latency measures on a supplied derived artifact.** It is not a new biological mechanism and not a causal finding.
