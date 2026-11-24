# Neural Feedback Optimization Theory (NFOT)

### The Write-Back Gap as a Trial-Level Temporal Variable in Closed-Loop Learning Systems

**Current working manuscript:** NFOT v6  
**Research areas:** Computational neuroscience · Brain–computer interfaces · Closed-loop learning systems · Temporal dynamics  
**Repository:** Noggin Labs

NFOT investigates whether the timing and distribution of feedback in closed-loop systems contain trial-level information about system performance that is obscured by aggregate latency measures.

The central construct is the **Write-Back Gap**, defined for the historical analysis as:

\[
L = t_{\mathrm{fb}} - t_0
\]

where \(t_0\) is the defined stimulus-onset event and \(t_{\mathrm{fb}}\) is the rising edge of the corresponding feedback-display event. This is an operational event-to-feedback interval; it should not automatically be interpreted as neural processing time or a direct biological measurement.

## Research question

**Does the trial-level Write-Back Gap, including its distributional characteristics, contain information about BCI performance beyond what is captured by its mean?**

A related prospective question is whether controlled changes in feedback timing produce measurable changes in performance. That requires prospective intervention and measurement validation.

## Evidence status

The repository contains historical analyses, a v6 manuscript draft, provenance and validation documentation, a timing prototype, and a prospective experimental planning track.

Important distinctions:

- Historical v5 statistics are **reported historical results**, not independently reproduced inferential findings.
- The v6 source-level provenance audit remains a separate validation task.
- Raw EDF recordings or complete trusted event streams, converter metadata, and the source-level inclusion manifest must be available before source extraction can be independently reconstructed.
- The timing prototype supports instrumentation and workflow testing; it does not validate the historical BCI findings.
- Prospective causal effects and a biological mechanism have not been established.

Do not describe NFOT as a demonstrated breakthrough. Preserve the distinction between observed association, prediction, causal evidence, and proposed mechanism.

## Repository guide

| Path | Purpose |
|---|---|
| `manuscript/` | Current v6 working manuscript |
| `docs/` | Research status, methods, hypotheses, audits, protocols, and evidence ledger |
| `analysis/` | Analysis and audit scripts |
| `data/` | Historical derived data, source exports, and prototype trial data |
| `src/` | Reusable project code, including VampireBCI integration code |
| `demos/` | Interactive timing demonstration |
| `formal/` | Lean formalization and verification notes |
| `tests/` | Automated checks |
| `research/` | Research source notes |
| `publications/` | Released manuscript/preprint artifacts |
| `archive/unreviewed_v7_material/` | V7-labelled working material retained for review; not the canonical manuscript |

See [docs/INDEX.md](docs/INDEX.md) for the document map and [data/README.md](data/README.md) for data-handling notes.

## Reproducibility

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the test suite:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

Check the exact event definitions, dataset version, inclusion criteria, timestamp units, target reconstruction, and analysis specification before interpreting any result. Raw source data should remain unchanged; cleaning and exclusion decisions should be documented. Do not commit identifiable or sensitive participant information.

## Historical preprint

The v5 preprint is retained in `publications/NFOT_v5_preprint.pdf`. Its claims and reported results must be read alongside the subsequent audit and provenance documentation.

## Citation

See [CITATION.cff](CITATION.cff) and the [Zenodo record](https://zenodo.org/records/23140358).

---

*This repository documents independent exploratory research. It is not clinical evidence, and NFOT should be treated as a testable research programme pending stronger validation and independent replication.*
