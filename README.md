# Neural Feedback Optimization Theory (NFOT)

**The Write-Back Gap as a trial-level temporal variable in closed-loop learning systems.**

---

## What this is

NFOT proposes a measurable variable — the **Write-Back Gap** ($L$) — for studying feedback timing in closed-loop systems like BCIs, neurofeedback platforms, and adaptive learning technologies.

$L$ is defined as the achieved, trial-level interval between a prespecified biological event $t_0$ and the completion of the corresponding feedback $t_{\mathrm{fb}}$, measured on matched pairs.

The central hypothesis: **the trial-level Write-Back Gap contains information about learning outcomes, and its distribution may matter beyond its mean.**

This hypothesis is stated. It is **not** claimed to be true. It has not been tested.

---

## What this repository contains

- The **current version** of the NFOT preprint (v3).
- The **dataset survey** documenting that public closed-loop datasets do not currently preserve trial-level selection or feedback timing in an accessible format.
- The **PTSP protocol** — a proposed experimental design for testing the hypothesis.
- The **falsification criteria** — stated in advance, so that any outcome is interpretable.

---

## What this repository does *not* contain

- **No numerical time constant.** Earlier versions of this framework contained a specific numerical claim (approximately 28.42 ms). That claim was derived from a simulation whose assumptions could not be independently verified, and has been removed. The present version does not claim a numerical constant.
- **No derived functional form.** The Lorentzian form $E(L) = c/(L^2 + c)$ appears only as one candidate among several (exponential, Gaussian, power-law). No candidate has theoretical priority.
- **No claimed mechanism.** The Asymmetric Biological Eligibility Trace Hypothesis (ABETH) is mentioned only as a possible future extension, with no specific time constants.
- **No simulation output presented as evidence.** Simulations can illustrate what the framework implies under specified assumptions. They cannot establish biological constants.

---

## The hypothesis

**Predictive hypothesis.** After the target event and feedback modality are prespecified, the achieved trial-level Write-Back Gap $L$ contains reproducible out-of-sample information about learning-related outcomes under at least some closed-loop conditions.

**Causal hypothesis (stronger, tested separately).** Manipulating $L$ while holding relevant feedback properties constant changes the learning-related outcome.

**Distributional prediction.** Two closed-loop systems with matched mean latency but different latency variance may produce different learning outcomes.

---

## What would falsify it

| Empirical result | Interpretation |
|---|---|
| $L$ improves preregistered out-of-sample prediction | Supports the predictive hypothesis |
| $L$ adds no reproducible predictive information after controls | Challenges the predictive hypothesis |
| Mean $L$ does not matter, but variance or tails do | Supports the distributional prediction |
| Manipulating $L$ does not change the outcome under matched feedback content | Challenges the causal hypothesis |

---

## Current status

- **Literature review:** Ongoing. Prior work (Tidare et al. 2018; Nogay & Akinci 2026; Horschig et al. 2015) treats feedback delay as an engineering property. The trial-level distributional analysis does not appear to have been performed.
- **Dataset survey:** Two public datasets examined (BCI-FIT ds007720; Chandravadia et al. ds005028). Neither preserves trial-level selection or feedback timing in an accessible format.
- **Status of the hypothesis:** Untested. The data required to test it does not currently exist in public archives.

---

## What the field needs to record

For the hypothesis to be testable, future closed-loop studies should record:

1. $t_0$ — the biological event timestamp, at trial resolution.
2. $t_{\mathrm{fb}}$ — the completion of feedback delivery, not enqueue or dispatch.
3. The outcome $Y$ — measured after the intervention, not during it.
4. Matched pairs — each $t_0$ linked to its corresponding $t_{\mathrm{fb}}$ and $Y$.

If published in BIDS format, selection and feedback events should appear in `events.tsv` with a distinct `trial_type` (e.g., `selection`) and an `onset` value at the moment of delivery.

---

## Versions

This is v3. Previous versions (v1, v2) contained a specific numerical claim (28.42 ms) and a derived functional form (the Lorentzian law) that were not independently defensible. Those claims have been removed. Readers interested in the history of the framework should consult the previous versions.

---

## Citation

Kassim, F. A. (2026). *Neural Feedback Optimization Theory (NFOT): A Trial-Level Feedback Timing Hypothesis and a Survey of Public Dataset Availability.* Zenodo Preprint, v3.

---

## License

MIT 
