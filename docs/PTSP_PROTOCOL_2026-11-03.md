# Project Lost Light / PTSP — matched-mean timing-variability protocol

**Status:** Proposed. Design-stage document. No data have been collected, no ethics approval is claimed, and no result is reported here.

**Central comparison:** two feedback-timing conditions matched on the mean Write-Back Gap but differing in dispersion:

    E[L_A] ≈ E[L_B]        (within a prespecified tolerance)
    Var(L_A) ≠ Var(L_B)

**Direction is not assumed.** The hypothesis is not "lower variability is better". A plausible competing prediction is that moderate variability aids learning by preventing temporal over-fitting to a single feedback latency, and a third is that variability is irrelevant once the mean is controlled. The study is designed to distinguish these, and an inconclusive result is a legitimate outcome.

---

## 1. Definitions

| Symbol | Definition | Operationalisation |
|---|---|---|
| `t0` | Prespecified onset event | First sample at which the trial's stimulus/response prompt is on screen, detected by the prespecified detector in §4 |
| `t_fb` | Feedback completion | First sample at which the complete correctness feedback (all required elements, §3) has been presented |
| `L` | Write-Back Gap | `t_fb − t0` for that trial |
| `L_A`, `L_B` | Condition-level timing variable | The realised per-trial `L` under each condition |

`L` is a system-and-task interval. It is **not** a neural processing time, and the protocol makes no claim about eligibility traces or neuromodulatory timing. Those are motivating hypotheses, not measured quantities here.

## 2. Conditions

- **Condition A (matched-mean, low dispersion):** per-trial `L` drawn from a bounded distribution with target mean μ and target SD σ_low.
- **Condition B (matched-mean, high dispersion):** same target mean μ, target SD σ_high > σ_low.
- Both conditions use the **same** feedback content, wording, visual layout, duration of display, and modality. Only the *scheduling* of when feedback begins differs.
- Target values for the design (to be piloted, not assumed): μ ≈ 1.5 s post-response; σ_low ≈ 0.15 s; σ_high ≈ 0.60 s. These are placeholders pending pilot measurement of achievable timing control.

### Delay distributions

Use bounded, symmetric distributions so that no trial can produce a negative or absurd delay after clipping:

- A: uniform on `[μ − a, μ + a]`
- B: uniform on `[μ − b, μ + b]`, with `b > a`

Uniform distributions with equal mean and different half-widths give `Var = (half-width)²/3`, so `Var_B / Var_A = (b/a)²`. Matching a *uniform* to a *uniform* keeps both bounded and both symmetric, avoiding a distribution-shape confound. **Do not** compare a uniform to an exponential: that confounds shape with dispersion.

### Mean-matching tolerance

Prespecified: the realised condition means must satisfy

    | mean(L_A) − mean(L_B) | ≤ 0.10 s   and   | mean(L_A) − μ | ≤ 0.10 s

If either fails after the run, the primary analysis is still run but the achieved means, the achieved SDs, and the matching error are reported, and the study is labelled "mean-matching criterion not met". It is not silently re-matched by dropping trials.

## 3. Feedback-content controls

To argue that any effect is due to *timing* rather than *information*, all of the following are fixed across conditions:

- identical correctness signal (same icon/wording);
- identical explanatory text length range;
- identical on-screen duration of the feedback event;
- identical inter-trial interval measured from feedback completion;
- no adaptive difficulty changes during the experiment;
- the same number of trials per condition.

## 4. Instrumentation and event detection

Software timestamps alone are insufficient. Required:

1. **Prespecified `t0` detector.** A fixed rule applied identically to every trial, e.g. "the first display refresh at which the prompt's first frame is presented", recorded via the rendering pipeline's frame-presented callback. The rule is written before data collection and never tuned to the data.
2. **Independent physical timing check.** At least one of: a photodiode/phototransistor on the display measuring actual onset and feedback luminance change, or a high-speed camera check on a sample of trials. Report measured physical-vs-logged offset with its distribution.
3. **Clock provenance.** Record the clock source, monotonicity, resolution and any drift correction.
4. **Per-trial log fields:** `trial_id`, `condition`, `assigned_delay`, `t0_logged`, `t0_physical` (if measured), `response_time`, `t_fb_logged`, `t_fb_physical`, `L`, `delay_error = t_fb_achieved − t_fb_assigned`, `correct`, `feedback_elements_shown`.

If no physical timing measure is possible, the study must state in its title and abstract that timing is a software event interval, and must not describe `L` as a display latency.

## 5. Randomisation

- Conditions assigned per trial by a **prespecified randomisation list with permuted blocks**, block size 4 (two per condition), so that condition counts cannot drift far within a session.
- The randomisation seed and the generated list are archived before data collection.
- The participant is blind to condition. The experimenter is blind where feasible.
- Trial order is otherwise fixed per participant to control practice and fatigue.

## 6. Participants and exclusions

- Target population: adult volunteers, or school-age learners **only** with the safeguards in §10.
- Prespecified exclusions, decided before analysis and applied by rule:
  1. no response on > 20% of trials;
  2. any session where the physical-vs-logged timing offset exceeds 50 ms on > 10% of trials;
  3. sessions where the software logged a frame-drop event during feedback;
  4. duplicate or interrupted sessions.
- **Every** excluded participant and trial is listed with its reason. No row is dropped silently. Sensitivity analysis repeats the primary model including all exclusions reversed.

## 7. Outcomes

**Primary outcome (prespecified):** accuracy on the *subsequent* trial of the same item type, i.e. trial `t+1`. A post-response delay cannot affect the correctness of the response that already occurred, so the already-submitted trial is never the primary outcome.

**Secondary outcomes:**
1. Response time on trial `t+1`.
2. Learning block: accuracy on a delayed post-test of the same items.
3. Self-reported confidence (if collected).
4. Calibration of confidence against correctness.
5. Realised `L` dispersion per condition (manipulation check — a study whose manipulation failed reports that).

## 8. Statistical model

**Primary analysis.** A mixed-effects logistic regression of next-trial correctness on condition, with a random intercept per participant and a random slope for trial index:

    logit P(correct_{t+1}) = β0 + β1·condition + β2·trial + β3·(condition×trial) + u0_participant + u1_participant·trial

`β1` is the condition effect. Trials are clustered within participant; they are never treated as independent.

**Secondary, direct test of the dispersion hypothesis.** Include the participant-centred absolute deviation `|L_t − mean(L)|` as a predictor alongside condition. If dispersion is the operative variable, this term should carry the effect and `β1` should shrink. Report both models.

**Effect size.** Report the condition effect as an odds ratio with a 95% interval, plus the participant-level mean-accuracy difference and its paired standardised effect (Cohen's dz). Report participant-level scatter; do not report only a p-value.

**Multiplicity.** One primary outcome. Secondary outcomes are labelled exploratory and reported with intervals, not as confirmatory tests.

**Model diagnostics.** Check convergence, singularity of random effects, and separation. If the random-slope model does not converge, fall back to a prespecified random-intercept model and say so.

## 9. Power analysis

Power is computed by simulation (`analysis/ptsp_power.py`), because the outcome is clustered and binary.

**Status: synthetic only.** The numbers below are design-sensitivity checks, not observed data and not predictions.

Assumptions that are *guessed*, not estimated, and must be replaced by pilot values:

| Assumption | Placeholder value | Why it is uncertain |
|---|---|---|
| Effect of timing deviation on next-trial accuracy (`b_dev`) | −0.05 to −0.15 per second | No published estimate in this exact paradigm |
| Participant intercept SD (`sigma_a`) | 0.5 (logit scale) | Depends on task difficulty |
| Trials per condition | 40 | Constrained by session length |
| Between-participant SD of true effect | 0 | Likely non-zero; would reduce power further |

Synthetic simulation output, 400 replications, 40 trials per condition (archived as `ptsp_power_weak.json` and `ptsp_power_strong.json`):

| Participants | Power at `b_dev = −0.05` (dz ≈ −0.13) | Power at `b_dev = −0.15` (dz ≈ −0.40) |
|---|---|---|
| 12 | 0.107 | 0.233 |
| 16 | 0.083 | 0.302 |
| 20 | 0.090 | 0.333 |
| 24 | 0.107 | 0.445 |
| 32 | 0.125 | 0.588 |
| 40 | 0.122 | 0.675 |

The honest reading is that **this design, with 40 trials per condition, is badly underpowered unless the true effect is considerably larger than the placeholder**: a per-second deviation effect of −0.05 yields roughly 8–13% power at any feasible participant count, and even −0.15 only reaches 68% at 40 participants. Note that power does not increase monotonically at the weak effect (0.107 → 0.083 → 0.090), which is itself a signal that these estimates are noise-dominated at that effect size.

Consequences for the design, stated before data collection:

1. Increase trials per condition, or
2. frame the study as an **estimation study** reporting an interval for the condition effect rather than a significance test, or
3. obtain a pilot estimate of `b_dev` first and re-run this power analysis with it.

Reporting power at an assumed effect size and then claiming significance is not acceptable, and the placeholder values must be replaced by pilot estimates before any preregistration is submitted.

This is a real finding about the design and should be carried into the preregistration, not hidden.

## 10. Ethics and safeguards

- Adult participants: institutional approval and informed consent required before any collection.
- **Minors / school-age participants:** requires guardian consent, participant assent, institutional review, and a data-protection plan. This must not be undertaken unsupervised by a student researcher.
- No clinical, diagnostic or neurodevelopmental claims. No EEG/implants. No inference about a learner's ability, attention, or motivation from timing data.
- Store the minimum data necessary; pseudonymise at collection; never commit participant data to a repository.

## 11. Failure conditions (declared in advance)

The study is reported as **failed or inconclusive** if any of these hold:

1. The realised mean-matching tolerance in §2 is not met.
2. The realised SDs do not differ by at least a factor of 2 (manipulation check failed).
3. Physical-vs-logged timing offset exceeds the §6 exclusion threshold for the cohort.
4. The mixed model does not converge and no prespecified fallback is defensible.
5. Attrition or missingness exceeds the prespecified limit.

## 12. Reproducibility requirements

- Archive: randomisation list + seed, the exact build/commit of the experiment software, display hardware and refresh rate, the `t0` detector rule, the analysis script, and the model specification.
- Publish the analysis code and a synthetic example dataset with the same schema, so the pipeline is runnable without releasing participant data.
- Report the achieved timing distributions, not just the assigned ones.
