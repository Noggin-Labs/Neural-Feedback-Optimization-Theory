# PTSP — Phase-Targeted Stimulation Protocol

**Status:** Protocol identity and scope clarification. This document is not a locked protocol, preregistration, ethics approval, or authorization to conduct stimulation.

## 1. Official name

**PTSP** means **Phase-Targeted Stimulation Protocol**.

Use this expansion consistently in the NFOT project, research notes, preregistration drafts, and repository documentation. The previous expansion, “Perturbation Timing Sensitivity Project,” is incorrect and should not be used.

## 2. Relationship to NFOT

PTSP belongs to the Neural Feedback Optimization Theory (NFOT) research programme. It is the protocol through which the relevant experimental questions are intended to be investigated; it is not a separate competing theory.

Do not describe NFOT and PTSP as unrelated projects. Equally, do not imply that the protocol has already validated NFOT.

## 3. What the current repository establishes

The repository contains historical/proposed work on feedback timing, including a matched-mean variability design. That design compares feedback-delay distributions with matched means and different dispersion.

However, the currently available matched-mean protocol does **not** specify the defining phase-targeting procedure. It does not establish:
- which physiological or signal phase is targeted;
- how that phase is operationally defined or estimated;
- how a stimulation event is synchronized to the target phase;
- what stimulation modality or parameters are approved;
- how timing accuracy and signal/artifact quality are validated.

Therefore, the matched-mean feedback-delay study must be described as a related proposed experiment within the NFOT/PTSP research programme, not as a complete description of PTSP.

## 4. Phase-targeting specification required

The authoritative PTSP protocol must recover and document, from the original design record and qualified supervision:

1. The signal source and acquisition context.
2. The operational definition of the target phase.
3. The phase-estimation method and its validation.
4. The high-level timing relationship between phase estimation and the planned stimulation event.
5. The instrumentation and independent timing-validation approach.
6. Signal-quality, artifact, invalid-estimate, missed-event, and protocol-deviation handling.
7. The intended outcome measures and the causal estimand.
8. The applicable safety review, qualified adult oversight, and institutional ethics requirements.

These items are intentionally **unresolved** in this clarification. No phase, frequency, stimulation intensity, pulse sequence, device configuration, or implementation procedure should be inferred or invented here.

## 5. Status of the matched-mean documents

The files `PTSP_PROTOCOL_2026-11-03.md` and `PTSP_PREREG_DRAFT.md` contain earlier proposed feedback-delay/variability designs. Preserve them as historical design material while their relationship to the corrected PTSP scope is reviewed.

Do not silently merge their parameter values, outcomes, or randomization choices into a phase-targeted protocol. Resolve discrepancies against the latest approved design record before selecting a confirmatory study.

The Write-Back Gap remains an operational system/task interval defined by its event timestamps. It is not, by itself, a measurement of neural phase, neural processing time, or biological mechanism.

## 6. Preregistration lock conditions

A confirmatory preregistration is not ready until the authoritative phase-targeting specification, study question, primary estimand, outcomes, randomization, sample-size justification, timing validation, missing-data rules, stopping criteria, and ethics arrangements have been reviewed and frozen prospectively.

Any human-participant stimulation work requires qualified adult research supervision, appropriate institutional review and approval, and approved equipment and procedures. This document is a research-planning record, not an instruction to conduct stimulation.

## 7. Decision record

- **Confirmed:** PTSP = Phase-Targeted Stimulation Protocol.
- **Confirmed:** PTSP is part of the NFOT research programme, not a separate theory.
- **Confirmed:** the matched-mean feedback-variability work is not, by itself, the full phase-targeted protocol.
- **Unresolved:** the authoritative phase definition, estimator, stimulation timing specification, instrumentation, and validation criteria must be recovered from the original PTSP design record.
