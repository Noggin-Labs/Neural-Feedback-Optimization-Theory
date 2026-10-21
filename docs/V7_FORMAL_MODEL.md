# NFOT v7 formal model

## Definition

For trial `i`,

`L_i = t_fb,i - t_0,i`.

`t_0` and `t_fb` are protocol-defined recorded events, not automatically physical display or neural events. Units must be declared. A valid observation has ordered events, a known clock relationship, a documented phase context, and a complete trial linkage. Missing, ambiguous, reversed, or out-of-tolerance trials are excluded with reasons rather than repaired silently.

If endpoint measurement errors are `e_0` and `e_fb`, then the observed gap is `L_obs = L_true + e_fb - e_0`. An independent display measurement is required when physical onset is part of the construct. Timing uncertainty can attenuate or distort an association and cannot be inferred from seconds as a unit.

## Competing observable hypotheses

**H0: baseline latency marker.** `Pr(Y_i=1)` depends on ordinary task covariates and participant/session effects; `L` adds no stable predictive value.

**H1: current-gap association.** `logit Pr(Y_i=1) = a_p + b_w(L_i - mean_p) + b_b mean_p + X_i gamma`. This is observational and does not imply causation.

**H2: prior-history model.** A subsequent outcome depends on prior verified gaps through a prespecified history summary, such as `H_i = sum_{j<i} exp(-(t_i-t_j)/tau) L_j`, with `tau` fixed or estimated only within training data.

**H3: randomized delay effect.** Under assigned condition `A_i`, a subsequent outcome has `logit Pr(Y_{i+1}=1)=a_p + theta A_i + X_i gamma`. `theta` is the causal estimand for the prospective experiment.

## Identifiability

`b_w` and `b_b` require repeated participants with within-person variation and a verified outcome. `theta` requires random assignment, valid timing delivery, and a downstream outcome. A biological interpretation is not identifiable from behavioral event timestamps alone. History parameters such as `tau` are weakly identified without many time-separated observations and must not be selected for best fit in one small dataset.

## Predictions and failure conditions

NFOT adds value only if a prespecified timing/history feature improves a fair baseline under the intended deployment split, or if randomized delay changes a downstream outcome in a pattern not explained by baseline delay alone. The theory is weakened if the association disappears after verified extraction and confounder checks, if a conventional latency model performs equally well, if distributional features do not generalize, or if randomized delay has no prespecified downstream effect.
