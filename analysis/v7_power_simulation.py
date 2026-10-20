#!/usr/bin/env python3
"""Synthetic design sensitivity for a paired randomized delay experiment.

This is a planning tool only. It generates synthetic Bernoulli outcomes under
an assigned-condition effect and estimates rejection frequency using a paired
normal approximation across participants. It is not an analysis of NFOT data.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def simulate(
    *,
    n_participants: int,
    trials_per_condition: int,
    baseline_probability: float,
    absolute_effect: float,
    repetitions: int,
    seed: int,
) -> dict:
    if n_participants < 3 or trials_per_condition < 1 or repetitions < 1:
        raise ValueError("n_participants, trials_per_condition, and repetitions must be positive; n_participants >= 3.")
    if not 0 < baseline_probability < 1:
        raise ValueError("baseline_probability must be between 0 and 1.")
    if not -baseline_probability < absolute_effect < 1 - baseline_probability:
        raise ValueError("absolute_effect would produce an invalid probability.")
    rng = np.random.default_rng(seed)
    p_fast = baseline_probability
    p_slow = baseline_probability + absolute_effect
    rejections = 0
    estimates: list[float] = []
    for _ in range(repetitions):
        fast = rng.binomial(trials_per_condition, p_fast, size=n_participants) / trials_per_condition
        slow = rng.binomial(trials_per_condition, p_slow, size=n_participants) / trials_per_condition
        diff = slow - fast
        mean_diff = float(diff.mean())
        sd = float(diff.std(ddof=1))
        se = sd / np.sqrt(n_participants)
        z = mean_diff / se if se > 0 else (np.inf if mean_diff != 0 else 0.0)
        if abs(z) >= 1.959964:
            rejections += 1
        estimates.append(mean_diff)
    return {
        "simulation_type": "synthetic_paired_randomized_delay_sensitivity",
        "n_participants": n_participants,
        "trials_per_condition": trials_per_condition,
        "baseline_probability": baseline_probability,
        "absolute_effect": absolute_effect,
        "repetitions": repetitions,
        "seed": seed,
        "estimated_two_sided_rejection_frequency": rejections / repetitions,
        "mean_estimated_effect": float(np.mean(estimates)),
        "sd_estimated_effect": float(np.std(estimates, ddof=1)) if repetitions > 1 else 0.0,
        "warning": "Synthetic planning output; not an empirical NFOT result and not a substitute for a design-specific power analysis.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--participants", type=int, default=30)
    parser.add_argument("--trials-per-condition", type=int, default=30)
    parser.add_argument("--baseline", type=float, default=0.75)
    parser.add_argument("--effect", type=float, default=0.05)
    parser.add_argument("--repetitions", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20261020)
    parser.add_argument("--output", type=Path, default=Path("v7_power_simulation.json"))
    args = parser.parse_args()
    result = simulate(
        n_participants=args.participants,
        trials_per_condition=args.trials_per_condition,
        baseline_probability=args.baseline,
        absolute_effect=args.effect,
        repetitions=args.repetitions,
        seed=args.seed,
    )
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
