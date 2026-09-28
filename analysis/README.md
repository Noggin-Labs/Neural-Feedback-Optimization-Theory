# Trial-Level Analysis of bigP3BCI

Extracts and analyzes trial-level Write-Back Gap data from the
[bigP3BCI dataset](https://physionet.org/content/bigp3bci/1.0.0/)
(Mainsah et al. 2025, PhysioNet).

## What this does

For each P300 speller selection event in a bigP3BCI CSV file:

- `t0` — the first flash in the trial
- `tfb` — the feedback/selection event
- `L = tfb - t0` — the Write-Back Gap
- `Y` — whether the system's selection was correct

The output is one row per selection.

## Files

- `extract.py` — extract (L, Y) from a single CSV
- `pool.py` — extract from every CSV in a folder, concatenate, save
- `analyze.py` — run descriptive statistics, logistic regression,
  and the distributional test

## Usage

1. Convert each `.edf` file from bigP3BCI to `.csv` using your preferred tool.
2. Put all CSVs in the same folder.
3. Run:

```
python pool.py /path/to/csv/folder
```
