"""
extract.py

Extract trial-level (L, Y) pairs from one bigP3BCI CSV file.

Input: a CSV file converted from an EDF file in the bigP3BCI dataset
       (PhysioNet ds005795), specifically from Study M's ADdiff condition.

Output: a pandas DataFrame with one row per selection event, containing:
    trial            - trial index
    t0               - timestamp of the first flash in the trial (seconds)
    tfb              - timestamp of the feedback/selection (seconds)
    L                - Write-Back Gap = tfb - t0 (seconds)
    SelectedTarget   - the system's predicted character index
    Target           - the actual target character index (from StimulusType)
    Y                - 1 if SelectedTarget == Target, else 0

Note on the target channel:
    The PhysioNet documentation for bigP3BCI states that the target character
    is stored in 'CurrentTarget'. In Study M, CurrentTarget is empty (all
    zeros), and the target character index is actually stored in
    'StimulusType'. This function uses StimulusType.
"""

import os
import pandas as pd
import numpy as np


def load_and_clean(filepath):
    """Load a bigP3BCI CSV and clean the column headers."""
    df = pd.read_csv(filepath, sep=',', low_memory=False)
    # Remove type suffixes like ' (bool)', ' (int)', ' (uV)'
    df.columns = df.columns.str.replace(r'\s*\([^)]*\)', '', regex=True)
    return df


def extract_trials_from_file(filepath):
    """
    Extract trial-level (L, Y) pairs from one CSV file.
    Returns a DataFrame, or None if the file cannot be processed.
    """
    try:
        df = load_and_clean(filepath)
    except Exception as e:
        print(f"  [skip] {filepath}: could not read ({e})")
        return None

    # Sanity check: required columns
    required = ['Time', 'PhaseInSequence', 'SelectedTarget', 'StimulusType']
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"  [skip] {filepath}: missing columns {missing}")
        return None

    # Detect events
    df['Flash_Start'] = (df['PhaseInSequence'] == 1) & (df['PhaseInSequence'].shift(1) != 1)
    df['Selection_Event'] = (df['SelectedTarget'] != 0) & (df['SelectedTarget'] != df['SelectedTarget'].shift(1))

    flash_df = (
        df[df['Flash_Start'] == True][['Time']]
        .rename(columns={'Time': 't0_candidate'})
        .sort_values('t0_candidate')
        .reset_index(drop=True)
    )

    selection_df = (
        df[df['Selection_Event'] == True][['Time', 'SelectedTarget']]
        .rename(columns={'Time': 'tfb'})
        .sort_values('tfb')
        .reset_index(drop=True)
    )

    if len(selection_df) == 0 or len(flash_df) == 0:
        print(f"  [skip] {filepath}: no selections or no flashes")
        return None

    # Build one trial per selection event
    trials = []
    for i in range(len(selection_df)):
        tfb = selection_df.loc[i, 'tfb']
        sel = selection_df.loc[i, 'SelectedTarget']

        # The trial window is between the previous selection and this one.
        t_lower = 0.0 if i == 0 else selection_df.loc[i - 1, 'tfb']

        # Find the first flash in this window
        mask = (flash_df['t0_candidate'] > t_lower) & (flash_df['t0_candidate'] < tfb)
        flashes_in_window = flash_df.loc[mask, 't0_candidate']
        if len(flashes_in_window) == 0:
            continue
        t0 = flashes_in_window.min()

        # Sample the target character from StimulusType at the moment of feedback
        tfb_row = (df['Time'] - tfb).abs().idxmin()
        target = df.loc[tfb_row, 'StimulusType']

        L = tfb - t0
        Y = 1 if sel == target else 0

        trials.append({
            'trial': i,
            't0': round(t0, 4),
            'tfb': round(tfb, 4),
            'L': round(L, 4),
            'SelectedTarget': sel,
            'Target': target,
            'Y': Y,
        })

    if not trials:
        print(f"  [skip] {filepath}: no valid trials extracted")
        return None

    out = pd.DataFrame(trials)
    out['file'] = os.path.basename(filepath)
    return out


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python extract.py <path_to_csv>")
        sys.exit(1)
    result = extract_trials_from_file(sys.argv[1])
    if result is not None:
        print(result.to_string(index=False))
        print()
        print(f"L mean: {result['L'].mean():.3f}")
        print(f"L std:  {result['L'].std():.3f}")
        print(f"Y distribution: {result['Y'].value_counts().to_dict()}")
