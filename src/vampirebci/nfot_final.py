"""
VampireBCI — final
Extracts trial-level (L, Y) data from bigP3BCI EDFs.
Handles M_04 through M_25 (M_08 does not exist).
"""

import pyedflib
import numpy as np
import pandas as pd
import glob
import os
import zipfile
import re

EVENT_CHANNELS = [
    "StimulusBegin", "DisplayResults", "CurrentTarget",
    "SelectedTarget", "SelectedRow", "SelectedColumn",
    "PhaseInSequence", "StimulusCode", "StimulusType",
]

GRID_COLS = 8


# ============================================================
# Find EDFs anywhere under a root (case-insensitive, unzips first)
# ============================================================
def find_edfs(root="/content"):
    zips = glob.glob(os.path.join(root, "**", "*.zip"), recursive=True)
    for z in zips:
        try:
            with zipfile.ZipFile(z) as zf:
                zf.extractall(os.path.dirname(z))
            print(f"  unzipped: {os.path.basename(z)}")
        except Exception as e:
            print(f"  [skip zip] {z}: {e}")

    found = []
    for p in glob.glob(os.path.join(root, "**", "*"), recursive=True):
        if os.path.isfile(p) and p.lower().endswith(".edf"):
            found.append(p)
    return sorted(found)


# ============================================================
# EDF reading
# ============================================================
def read_edf(path):
    f = pyedflib.EdfReader(path)
    labels = f.getSignalLabels()
    data = {}
    fs = None
    for name in EVENT_CHANNELS:
        if name in labels:
            idx = labels.index(name)
            data[name] = f.readSignal(idx)
            if fs is None:
                fs = f.getSampleFrequency(idx)
    ann = f.readAnnotations()
    f.close()
    if fs is None:
        raise ValueError("no event channels found")
    return data, ann, fs


# ============================================================
# Helpers
# ============================================================
def decode_cell(cell_index):
    """cell = (row-1)*8 + col -> (row, col), 1-indexed."""
    if cell_index == 0:
        return (0, 0)
    row = (cell_index - 1) // GRID_COLS + 1
    col = (cell_index - 1) % GRID_COLS + 1
    return (row, col)


def find_feedback_onsets(dr):
    return np.where((dr[1:] == 1) & (dr[:-1] == 0))[0] + 1


def find_flash_onsets(sb):
    return np.where((sb[1:] == 1) & (sb[:-1] == 0))[0] + 1


def find_selected_runs(st):
    nz = np.where(st != 0)[0]
    if len(nz) == 0:
        return np.array([], dtype=int), np.array([], dtype=int)
    breaks = np.where(np.diff(nz) > 1)[0]
    starts = np.concatenate([[nz[0]], nz[breaks + 1]])
    ends = np.concatenate([nz[breaks], [nz[-1]]])
    return starts, ends


def parse_filename(path):
    """
    From 'M_05_SE001_ADdiff_Test01.edf' extract:
      subject = 'M_05'
      session = 'SE001'
      test    = 'Test01'
    """
    base = os.path.basename(path)
    for ext in (".edf", ".EDF"):
        if base.endswith(ext):
            base = base[: -len(ext)]
            break
    parts = base.split("_")

    subject = "_".join(parts[:2]) if len(parts) >= 2 else "unknown"
    session = parts[2] if len(parts) >= 3 else "unknown"
    test = parts[-1] if len(parts) >= 1 else "unknown"
    return subject, session, test


def subject_num(subject):
    """Extract numeric ID from 'M_XX'. Returns None if not parseable."""
    m = re.match(r"M_(\d+)", subject)
    return int(m.group(1)) if m else None


# ============================================================
# Extraction — one file
# ============================================================
def extract_file(path, verbose=True):
    try:
        data, ann, fs = read_edf(path)
    except Exception as e:
        if verbose:
            print(f"  [skip] {os.path.basename(path)}: {e}")
        return None

    sb = data.get("StimulusBegin")
    dr = data.get("DisplayResults")
    st = data.get("SelectedTarget")
    ct = data.get("CurrentTarget")

    if sb is None or dr is None or st is None:
        if verbose:
            print(f"  [skip] {os.path.basename(path)}: missing core channels")
        return None

    fb_idx = find_feedback_onsets(dr)
    fl_idx = find_flash_onsets(sb)
    run_starts, run_ends = find_selected_runs(st)

    if len(fb_idx) == 0 or len(run_starts) == 0:
        if verbose:
            print(f"  [skip] {os.path.basename(path)}: "
                  f"{len(fb_idx)} feedback, {len(run_starts)} selection runs")
        return None

    n_trials = min(len(fb_idx), len(run_starts))
    trials = []
    prev_fb = -1

    for k in range(n_trials):
        tfb_i = fb_idx[k]
        run_s, run_e = run_starts[k], run_ends[k]

        sel_cell = int(st[run_s:run_e + 1].max())
        sel_row, sel_col = decode_cell(sel_cell)

        tgt = 0
        if ct is not None:
            win = ct[max(0, tfb_i - int(1.0 * fs)):tfb_i + 1]
            nz = win[win != 0]
            if len(nz):
                tgt = int(nz[-1])

        flashes = fl_idx[(fl_idx > prev_fb) & (fl_idx < tfb_i)]
        if len(flashes) == 0:
            prev_fb = tfb_i
            continue
        t0_i = int(flashes.min())

        L = (tfb_i - t0_i) / fs
        Y = 1 if (sel_cell != 0 and sel_cell == tgt) else 0

        trials.append({
            "file": os.path.basename(path),
            "trial": k,
            "t0_s": t0_i / fs,
            "tfb_s": tfb_i / fs,
            "L_s": L,
            "selected_cell": sel_cell,
            "selected_row": sel_row,
            "selected_col": sel_col,
            "true_target": tgt,
            "Y": Y,
            "n_flashes": int(len(flashes)),
        })

        prev_fb = tfb_i

    if not trials:
        return None

    df = pd.DataFrame(trials)
    subject, session, test = parse_filename(path)
    df["subject"] = subject
    df["session"] = session
    df["test"] = test

    if verbose:
        acc = df["Y"].mean() * 100
        print(f"  {os.path.basename(path)}: {len(df)} trials  "
              f"acc={acc:.1f}%  L_mean={df['L_s'].mean():.3f}s  "
              f"L_std={df['L_s'].std():.3f}s")

    return df


# ============================================================
# Main
# ============================================================
def main(root="/content", out_csv="pooled_trials_full.csv"):
    print(f"Searching for EDFs under {root} ...")
    edfs = find_edfs(root)
    print(f"Found {len(edfs)} EDF files\n")

    if not edfs:
        print("Nothing to process.")
        return None

    all_trials = []
    skipped = []

    for p in edfs:
        r = extract_file(p)
        if r is not None:
            all_trials.append(r)
        else:
            skipped.append(os.path.basename(p))

    if not all_trials:
        print("\nNo trials extracted.")
        return None

    pooled = pd.concat(all_trials, ignore_index=True)

    # Sort by subject number, then session, then test, so output is stable
    pooled["_subj_num"] = pooled["subject"].apply(subject_num).fillna(999)
    pooled = pooled.sort_values(["_subj_num", "session", "test", "trial"])
    pooled = pooled.drop(columns=["_subj_num"]).reset_index(drop=True)

    pooled.to_csv(out_csv, index=False)

    print()
    print("=" * 60)
    print(f"POOLED: {len(pooled)} trials from "
          f"{pooled['file'].nunique()} files, "
          f"{pooled['subject'].nunique()} subjects")
    print("=" * 60)

    n = len(pooled)
    acc = pooled["Y"].mean() * 100
    print(f"Accuracy:   {acc:.1f}%  ({int(pooled['Y'].sum())}/{n})")
    print(f"L mean:     {pooled['L_s'].mean():.4f} s")
    print(f"L std:      {pooled['L_s'].std():.4f} s")
    print(f"L min/max:  {pooled['L_s'].min():.4f} / "
          f"{pooled['L_s'].max():.4f} s")

    print()
    print("Per subject:")
    for subj, g in pooled.groupby("subject"):
        print(f"  {subj}: n={len(g):4d}  acc={g['Y'].mean()*100:5.1f}%  "
              f"L_mean={g['L_s'].mean():.3f}s  "
              f"L_std={g['L_s'].std():.3f}s")

    # Which subjects are in the new range?
    nums = sorted(set(
        subject_num(s) for s in pooled["subject"].unique()
        if subject_num(s) is not None
    ))
    print()
    print(f"Subject IDs present: {nums}")

    if skipped:
        print()
        print(f"Skipped {len(skipped)} files:")
        for s in skipped[:20]:
            print(f"  - {s}")
        if len(skipped) > 20:
            print(f"  ... and {len(skipped) - 20} more")

    print()
    print(f"Saved to {out_csv}")
    return pooled


# ============================================================
# Run
# ============================================================
if __name__ == "__main__":
    pooled = main("/content")
