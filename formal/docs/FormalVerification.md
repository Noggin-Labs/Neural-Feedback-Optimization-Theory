# NFOT formal verification plan

## Purpose

The Lean component is a mathematical specification and proof-checking layer for
selected NFOT definitions and propositions. It is not a biological simulator,
statistical analysis package, or empirical validation substitute.

## Implemented in the initial Lean foundation

1. Protocol-recorded initiating and feedback timestamps.
2. The Write-Back Gap definition: `L = t_fb - t_0`.
3. Conditional non-negativity when `t_0 ≤ t_fb`.
4. Zero gap for coincident timestamps.
5. Invariance under a common shift of both timestamps.
6. Monotonicity in the feedback endpoint with the initiating event fixed.
7. Decomposition of an interval across an intermediate timestamp.
8. A finite equally weighted example with equal means and unequal population
   variances.

## Not yet formalised

- A probability-space or continuous-distribution treatment of variance.
- Within- and between-participant estimands and their identification assumptions.
- Potential outcomes, randomisation, and the intention-to-treat estimand.
- Sampling uncertainty, regression estimation, AUC, cross-validation, or power.
- Measurement error, event-detector uncertainty, clock synchronisation, and
  physical display-onset validation.

These should be added only with precise mathematical definitions and explicit
assumptions. In particular, an observational association must not be formalised
as a causal conclusion.

## Build and continuous integration

The Lean project is pinned to Lean 4.19.0 and Mathlib tag v4.19.0. The workflow
`.github/workflows/lean.yml` builds the library when the formal project changes.

## Scientific interpretation

A theorem establishes that a proposition follows from the encoded definitions
and hypotheses. It does not establish that the definitions correspond to the
intended events in a real BCI, that measurements are accurate, or that a
proposed timing relationship occurs in biological systems. Those questions
remain empirical and belong to the NFOT source-data audit and prospective PTSP
validation programme.
