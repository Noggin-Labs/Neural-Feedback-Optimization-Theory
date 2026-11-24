# NFOT v7 power and precision plan

No authoritative sample size is asserted because the primary outcome, randomization unit, within-participant correlation, timing conditions, attrition, and plausible effect size are not established.

The planning requirement is to simulate the locked primary analysis across a grid of participant counts, trials per condition, baseline outcome rates, participant heterogeneity, missingness, and absolute effects. Report both rejection frequency under assumed effects and precision of the estimated contrast. The design must distinguish feasibility timing work from confirmatory inference.

`analysis/v7_power_simulation.py` provides a deliberately simple synthetic paired-Bernoulli sensitivity calculation. It is not an NFOT result, does not model every planned nuisance parameter, and must be replaced or extended once the primary outcome and analysis are frozen. Its output must be labeled synthetic.

Required future assumptions: pilot-informed outcome probability, participant variance, within-participant correlation, condition delivery rate, attrition, number of valid trials, and the minimum practically meaningful effect. Sensitivity should include effects near zero, the smallest meaningful effect, and adverse timing-failure scenarios. Stopping rules and interim looks must be declared before confirmatory collection.
