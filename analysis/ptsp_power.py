#!/usr/bin/env python3
"""Project Lost Light / PTSP — power simulation for the matched-mean timing-variability design.

SYNTHETIC DATA ONLY. Nothing produced by this script is empirical evidence. Its
only purpose is to check that the planned design can detect an effect of the size
it claims to care about, and to show how power depends on assumptions that have
not yet been estimated.

The design
----------
Two feedback-timing conditions are matched on the *mean* Write-Back Gap:

    E[L_A] = E[L_B]      (within a prespecified tolerance of delta_mean)

but differ in *dispersion*:

    Var(L_A) != Var(L_B)

The scientific question is whether the dispersion of feedback timing affects the
*subsequent* trial, because a post-response delay cannot cause the correctness of
the response that already happened.

Data-generating model (explicit, and deliberately simple)
--------------------------------------------------------
For participant i, condition c, trial t:

    L_ict ~ Normal(mu, sigma_c)
    p(correct)_ict = logistic(a_i + b_dev * |L_ict - mu| + b_cond * 1[c = B])
    a_i ~ Normal(a0, sigma_a)                      # participant intercept
    Y_ict ~ Bernoulli(p(correct)_ict)

``b_dev`` is the effect of timing *deviation* on the next trial's correctness.
Its sign is an input, not an assumption: the design is intended to test direction,
so the simulation must not presuppose that low variability is better.
``b_cond`` is an optional residual condition effect (e.g. any difference not
mediated by timing); setting it to 0 makes the simulation a pure test of the
dispersion hypothesis.

Primary analysis (prespecified)
-------------------------------
Aggregate to participant-level mean accuracy per condition, then a paired t-test
(two-sided, alpha = 0.05). Trials are never treated as independent replicates.
Power is the fraction of replications reaching p < alpha.

Usage
-----
    python ptsp_power.py --n-participants 24 --trials 40 --b-dev -0.05
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def _logistic(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def simulate(
    *,
    n_participants: int = 24,
    trials_per_condition: int = 40,
    mu: float = 7.0,
    sd_low: float = 1.5,
    sd_high: float = 3.0,
    a0: float = 0.6,
    sigma_a: float = 0.5,
    b_dev: float = -0.05,
    b_cond: float = 0.0,
    delta_mean: float = 0.0,
    alpha: float = 0.05,
    repetitions: int = 400,
    seed: int = 20261103,
) -> dict:
    """Estimate power for the paired participant-level accuracy comparison."""
    if sd_low <= 0 or sd_high <= 0:
        raise ValueError("sd_low and sd_high must be positive")
    if sd_low == sd_high and b_dev == 0 and b_cond == 0:
        raise ValueError("conditions are identical; power is undefined and should not be reported")
    if n_participants < 3:
        raise ValueError("at least 3 participants are required for a paired analysis")

    from scipy import stats

    rng = np.random.default_rng(seed)
    rejections = 0
    effect_sizes: list[float] = []
    dz_values: list[float] = []

    for _ in range(repetitions):
        intercepts = rng.normal(a0, sigma_a, size=n_participants)
        means = np.empty((n_participants, 2))
        for condition, sd in enumerate((sd_low, sd_high)):
            L = rng.normal(mu + condition * delta_mean, sd,
                           size=(n_participants, trials_per_condition))
            linear = intercepts[:, None] + b_dev * np.abs(L - mu) + b_cond * condition
            p = _logistic(linear)
            Y = rng.random(p.shape) < p
            means[:, condition] = Y.mean(axis=1)

        diff = means[:, 1] - means[:, 0]
        effect_sizes.append(diff.mean())
        # Cohen's dz is standardised by the WITHIN-replication SD of the paired
        # differences, not by the spread of means across replications.
        if diff.std(ddof=1) > 0:
            dz_values.append(float(diff.mean() / diff.std(ddof=1)))
        if stats.ttest_rel(means[:, 1], means[:, 0]).pvalue < alpha:
            rejections += 1

    cohens_dz = float(np.mean(dz_values)) if dz_values else None
    return {
        "design": {
            "n_participants": n_participants,
            "trials_per_condition": trials_per_condition,
            "mu_seconds": mu,
            "sd_low_seconds": sd_low,
            "sd_high_seconds": sd_high,
            "delta_mean_seconds": delta_mean,
            "b_dev": b_dev,
            "b_cond": b_cond,
            "a0": a0,
            "sigma_a": sigma_a,
            "alpha": alpha,
            "repetitions": repetitions,
            "seed": seed,
        },
        "power": rejections / repetitions,
        "n_rejections": rejections,
        "mean_accuracy_difference_high_minus_low_sd": float(np.mean(effect_sizes)),
        "approx_cohens_dz": cohens_dz,
        "status": "SYNTHETIC_SIMULATION_NOT_OBSERVED_DATA",
        "minimum_detectable_effect_note": (
            "Power depends on b_dev, sigma_a and the within-participant trial count, "
            "none of which have been estimated from real data. Treat these numbers "
            "as design sensitivity checks, not as predictions of study outcome."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-participants", type=int, default=24)
    parser.add_argument("--trials", type=int, default=40)
    parser.add_argument("--b-dev", type=float, default=-0.05)
    parser.add_argument("--b-cond", type=float, default=0.0)
    parser.add_argument("--sd-low", type=float, default=1.5)
    parser.add_argument("--sd-high", type=float, default=3.0)
    parser.add_argument("--repetitions", type=int, default=400)
    parser.add_argument("--seed", type=int, default=20261103)
    parser.add_argument("--grid", action="store_true",
                        help="Sweep participant counts instead of a single design")
    parser.add_argument("--output", default="ptsp_power.json")
    args = parser.parse_args()

    kwargs = dict(
        trials_per_condition=args.trials, b_dev=args.b_dev, b_cond=args.b_cond,
        sd_low=args.sd_low, sd_high=args.sd_high,
        repetitions=args.repetitions, seed=args.seed,
    )

    if args.grid:
        rows = []
        for n in (12, 16, 20, 24, 32, 40):
            result = simulate(n_participants=n, **kwargs)
            rows.append({
                "n_participants": n,
                "power": result["power"],
                "approx_cohens_dz": result["approx_cohens_dz"],
            })
            print(f"n={n:3d}  power={result['power']:.3f}  dz~{result['approx_cohens_dz']:.3f}")
        payload = {"grid": rows, "base": kwargs, "status": "SYNTHETIC_SIMULATION_NOT_OBSERVED_DATA"}
    else:
        payload = simulate(n_participants=args.n_participants, **kwargs)
        print(json.dumps(payload, indent=2))

    Path(args.output).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
