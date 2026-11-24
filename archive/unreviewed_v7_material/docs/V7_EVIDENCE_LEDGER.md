# NFOT v7 evidence ledger

| ID | Claim | Status | Required next evidence | Main alternative |
|---|---|---|---|---|
| C1 | `L = t_fb - t0` is arithmetically defined in the derived table | PARTIALLY VERIFIED | Source-level event reconstruction | Stored columns may not have intended semantics |
| C2 | `t0` is the intended physical/stimulus onset | NOT ASSESSABLE | Raw/event-stream audit and timing measurement | Software marker, conversion or phase error |
| C3 | `t_fb` is feedback presentation/completion | NOT ASSESSABLE | Documented endpoint plus external timing where needed | Command/queue timestamp or display lag |
| C4 | `CurrentTarget`/selection labels are valid for Study M | NOT ASSESSABLE | Authoritative Study M source export | Constant/misconverted channel or wrong legacy substitution |
| C5 | 444 trials, 15 subjects and 82.9% accuracy | PARTIALLY VERIFIED | Reconstruct inclusion manifest | Derived artifact arithmetic only |
| C6 | Mean gap 7.06 s and SD 3.32 s | PARTIALLY VERIFIED | Source-verified re-extraction | Arithmetic of unverified columns |
| C7 | Longer gaps predict lower same-trial accuracy | REPORTED, NOT REPRODUCED | Corrected labels, clustered model, preregistered estimand | Difficulty, flashes, order, fatigue, participant differences |
| C8 | LOSO slopes are negative in 15/15 folds | REPORTED, NOT REPRODUCED | Held-out predictions and exact fold code | Leakage or selected preprocessing |
| C9 | Distributional features add predictive value | HYPOTHESIS | Fair participant-grouped benchmark | Mean/latency baseline sufficient |
| C10 | Gap timing causes learning or subsequent performance | PROPOSED | Randomized post-selection delay experiment | Ordinary delay effects or no effect |
| C11 | Gap is a synaptic eligibility trace | UNSUPPORTED | Neural/physiological measurement and mechanistic experiment | Behavioral timing is only a system marker |
| C12 | NFOT is a novel theory rather than a measurement framework | HYPOTHESIS | Novelty matrix plus added predictive/causal value | Existing latency, credit-assignment and learning frameworks |

The strongest current contribution is a falsifiable measurement-and-validation programme with explicit separation of event timing, observational association, prediction, causation, and biological interpretation. It is not currently a demonstrated breakthrough.
