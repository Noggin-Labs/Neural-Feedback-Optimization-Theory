"""
pool.py

Pool trial-level (L, Y) data across multiple bigP3BCI CSV files.

Place all of your converted CSVs in one folder, then run this script.
It will process each file, extract trials, concatenate everything into
one dataframe, report summary statistics, and save the pooled result
as 'pooled_trials.csv'.

Usage:
    python pool.py [folder] [pattern]

Defaults:
    folder = '.'
    pattern = '*.csv'
"""

import os
import sys
import glob
import pandas as pd
from extract import extract_trials_from_file


OUTPUT_CSV = 'pooled_trials.csv'


def pool_folder(folder='.', pattern='*.csv'):
    files = sorted(glob.glob(os.path.join(folder, pattern)))

    # Skip output files we might have created previously
    skip = {OUTPUT_CSV, 'brain_data.csv'}
    files = [f for f in files if os.path.basename(f) not in skip]

    print(f"Found {len(files)} CSV files in {folder}")
    print()

    all_trials = []
    for f in files:
        print(f"Processing {os.path.basename(f)}...")
        result = extract_trials_from_file(f)
        if result is not None:
            print(f"  → {len(result)} trials, "
                  f"L std={result['L'].std():.3f}, "
                  f"Y classes={sorted(result['Y'].unique().tolist())}")
            all_trials.append(result)
        print()

    if not all_trials:
        print("No usable files found.")
        return None

    return pd.concat(all_trials, ignore_index=True)


def summarize(pooled):
    print("=" * 60)
    print("POOLED RESULTS")
    print("=" * 60)
    print(f"Total trials: {len(pooled)}")
    print(f"Files pooled: {pooled['file'].nunique()}")
    print()

    print("=== L distribution ===")
    print(pooled['L'].describe())
    print()

    print("=== Y distribution ===")
    print(pooled['Y'].value_counts())
    print(f"Unique Y values: {sorted(pooled['Y'].unique().tolist())}")
    print()

    print("=== Per-file summary ===")
    summary = pooled.groupby('file').agg(
        n_trials=('L', 'count'),
        L_mean=('L', 'mean'),
        L_std=('L', 'std'),
        n_correct=('Y', 'sum'),
    ).reset_index()
    print(summary.to_string(index=False))
    print()


if __name__ == '__main__':
    folder = sys.argv[1] if len(sys.argv) > 1 else '.'
    pattern = sys.argv[2] if len(sys.argv) > 2 else '*.csv'

    pooled = pool_folder(folder, pattern)

    if pooled is not None:
        summarize(pooled)
        pooled.to_csv(OUTPUT_CSV, index=False)
        print(f"Saved pooled trials to {OUTPUT_CSV}")
