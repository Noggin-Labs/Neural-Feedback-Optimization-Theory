# NFOT Data Dictionary

## Purpose

This document describes important concepts and variables used in the Neural Feedback Optimization Theory (NFOT) project.

**Important:** Verify every column name against the exact CSV file and script version used for an analysis. A conceptual description is not proof that a particular file contains a field with that exact name.

## Core NFOT Concept

### Write-Back Gap (`L`)

The Write-Back Gap is defined as:

`L = t_fb - t0`

It represents an interval between a specified start event and a feedback-completion event.

The meaning of `L` depends on the event definitions and timestamp source. It should not automatically be interpreted as a direct measurement of neural processing time.

## Historical BCI Dataset

The historical analysis used the bigP3BCI Study M dataset and event markers extracted using VampireBCI.

| Concept | Definition |
|---|---|
| `t0` | `StimulusBegin` event timestamp |
| `t_fb` | Rising edge of `DisplayResults` |
| Historical `L` | `t_fb - t0` |
| Target reconstruction | The project reports checks against 4,192 of 4,192 applicable events |

The historical event markers are software or system event timestamps. They should not be assumed to measure physical display onset without independent verification.

## Timing-Pilot Variables

The timing demonstration is implemented in `NFOT-Timing_Demo.py`.

The following descriptions reflect the intended meaning of the corresponding fields. Confirm exact names and calculations in the relevant CSV and script version.

| Variable | Meaning |
|---|---|
| `trial` | Trial identifier or trial index |
| `assigned_delay_s` | Post-response feedback delay assigned by the experiment |
| `rt_s` | Recorded response-time measure, in seconds |
| `achieved_post_response_delay_s` | Measured interval between the recorded response and the feedback-related endpoint |
| `delay_error_s` | Difference between achieved and assigned post-response delay, according to the script's sign convention |
| `L_s` | Write-Back Gap calculated using the prototype's software timestamps |
| `correct` | Indicator of whether the response was correct |

Before analysis, document the precise formula for each derived field, including the sign convention for `delay_error_s`.

## Timing Distinctions

The prototype and historical BCI analysis do not necessarily use identical event definitions.

### Historical Analysis

`L = DisplayResults rising-edge timestamp - StimulusBegin timestamp`

### Timing Prototype

`L_s` is calculated from software timestamps associated with the stimulus-update process and the feedback-command process.

These definitions should not be treated as interchangeable without a documented equivalence test.

## Units and Data Types

- Fields ending in `_s` are intended to represent seconds.
- Correctness fields should have a documented encoding, such as Boolean values or 0/1.
- Trial identifiers should be treated as identifiers, not continuous measurements.
- Missing, invalid, or interrupted trials should have an explicit representation and handling rule.

## Data Validation Recommendations

1. Check that the CSV header matches the analysis script.
2. Check that numeric timing fields contain valid numeric values.
3. Recalculate derived timing fields from their source timestamps.
4. Verify the sign convention for timing error.
5. Check for missing, duplicated, or invalid trial records.
6. Compare assigned and achieved delays using a prespecified tolerance.
7. Record the script version and analysis procedure.
8. Keep raw records unchanged and document any transformations.

## Interpretation Cautions

- Assigned delay is not necessarily equal to achieved delay.
- Software timestamps are not automatically physical display-onset measurements.
- A correlation between `L` and correctness does not establish causation.
- A post-response delay cannot cause the correctness of the response that occurred before the delay.
- Definitions and conclusions should be limited to what the recorded data can support.
