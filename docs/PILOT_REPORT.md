# NFOT Timing Pilot Report

## Purpose

The NFOT timing pilot evaluates whether a software prototype can assign post-response feedback delays and record the resulting timing variables consistently.

The pilot is an instrumentation and feasibility exercise. It does not establish that feedback delay causes improved or reduced learning performance, and it does not measure neural activity.

## Prototype

The prototype is `NFOT-Timing_Demo.py`, an interactive parity-task demonstration.

The intended configuration contains 12 trials, with four trials assigned to each post-response delay:

- 0.25 seconds
- 1.00 second
- 2.00 seconds

Trial order is randomized.

## Recorded Variables

The prototype records timing and task variables including:

- Assigned post-response delay
- Response time
- Achieved post-response delay
- Delay error
- Write-Back Gap (`L_s`)
- Response correctness

Refer to the actual CSV header and the version of the script used when interpreting individual fields.

## Timing Definitions

In the software prototype, the Write-Back Gap is measured using software timestamps. Its start timestamp is associated with the stimulus-update process, and its endpoint is associated with the feedback-command process.

These timestamps do not necessarily correspond to the physical moment the stimulus or feedback becomes visible on the display.

The prototype's timing definition is therefore not identical to the historical BCI dataset definition, which uses the `StimulusBegin` and `DisplayResults` event markers.

## Scope and Limitations

The pilot can help assess whether the software schedules delays and records timing fields as intended.

It cannot, by itself, establish:

- A causal effect of feedback delay on learning
- A biological mechanism underlying the Write-Back Gap
- Equivalence between software timestamps and physical display onset
- Generalization to other tasks, participants, or BCI systems

Because feedback comes after the current response, its delay cannot cause the correctness of that already-submitted response. A causal study of feedback timing should define a suitable subsequent-trial or learning outcome in advance.

## Research Status

The project reports that the timing pilot and CSV arithmetic/consistency checks have been completed. This report does not claim unreported numerical results or independent validation of physical display timing.

## Next Steps

1. Verify the CSV schema against the exact script version.
2. Document timestamp definitions and known measurement limitations.
3. Test whether achieved delays match assigned delays within a prespecified tolerance.
4. Define a primary outcome that can plausibly be affected by the feedback manipulation.
5. Prespecify the analysis before collecting confirmatory data.
6. Seek appropriate adult research supervision and ethics review before conducting research with human participants.

## Conclusion

The timing pilot is a software feasibility step toward testing NFOT. It is not, on its own, evidence of a causal learning effect or a neural mechanism.
