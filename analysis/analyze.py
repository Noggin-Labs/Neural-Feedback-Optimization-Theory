"""
analyze.py

Basic statistical analysis of pooled (L, Y) trials.

Analyses performed:
    1. Descriptive: means of L for correct vs incorrect trials.
    2. Logistic regression: does L predict Y?
    3. Distributional test: does adding variance/tail information improve
       prediction beyond the mean?

Usage:
    python analyze.py [pooled_trials.csv]

Requires: pandas, numpy, scipy, scikit-learn
"""

import sys
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score


def load_data(path='pooled_trials.csv'):
    df = pd.read_csv(path)
    required = ['L', 'Y']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in {path}: {missing}")
    return df


def descriptive(df):
    print("=" * 60)
    print("DESCRIPTIVE STATISTICS")
    print("=" * 60)
    print(f"Total trials: {len(df)}")
    print(f"Correct (Y=1): {(df['Y'] == 1).sum()}")
    print(f"Incorrect (Y=0): {(df['Y'] == 0).sum()}")
    print()

    correct_L = df.loc[df['Y'] == 1, 'L']
    incorrect_L = df.loc[df['Y'] == 0, 'L']

    print(f"L | Y=1: mean={correct_L.mean():.3f}, std={correct_L.std():.3f}")
    print(f"L | Y=0: mean={incorrect_L.mean():.3f}, std={incorrect_L.std():.3f}")
    print()

    if len(correct_L) > 1 and len(incorrect_L) > 1:
        t_stat, p_val = stats.ttest_ind(correct_L, incorrect_L, equal_var=False)
        print(f"Welch t-test: t={t_stat:.3f}, p={p_val:.4f}")
    else:
        print("Not enough data in each class for a t-test.")
    print()


def logistic_regression(df):
    print("=" * 60)
    print("LOGISTIC REGRESSION: Y ~ L")
    print("=" * 60)

    if df['Y'].nunique() < 2:
        print("Y has only one class. Cannot fit regression.")
        print()
        return

    X = df[['L']].values
    y = df['Y'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = LogisticRegression()
    model.fit(X_train, y_train)

    coef = model.coef_[0][0]
    intercept = model.intercept_[0]

    print(f"Beta coefficient: {coef:.4f}")
    print(f"Intercept: {intercept:.4f}")
    print(f"Interpretation: odds ratio per 1s change in L = {np.exp(coef):.4f}")

    if len(np.unique(y_test)) > 1:
        y_prob = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, y_prob)
        print(f"Out-of-sample ROC-AUC: {auc:.4f}")
        if auc > 0.55:
            print("Result: L may carry predictive information.")
        else:
            print("Result: L does not significantly improve prediction here.")
    else:
        print("Test set has only one class. AUC not computable.")
    print()


def distributional_test(df):
    print("=" * 60)
    print("DISTRIBUTIONAL PREDICTION TEST")
    print("=" * 60)
    print("(This is the NFOT-specific prediction.)")
    print()

    # Sort trials by file and trial order so that "previous trial L" is meaningful.
    df = df.sort_values(['file', 'trial']).reset_index(drop=True)

    # Rolling variance of L over the previous 5 trials
    df['L_rolling_var'] = df['L'].rolling(window=5, min_periods=2).var()

    # Drop rows where rolling variance is undefined
    sub = df.dropna(subset=['L_rolling_var'])

    if len(sub) < 20:
        print(f"Not enough trials with rolling variance ({len(sub)}).")
        print("Pool more files before testing the distributional prediction.")
        print()
        return

    if sub['Y'].nunique() < 2:
        print("Y has only one class. Cannot test.")
        print()
        return

    X = sub[['L', 'L_rolling_var']].values
    y = sub['Y'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_prob = model.predict_proba(X_test)[:, 1]

    if len(np.unique(y_test)) > 1:
        auc = roc_auc_score(y_test, y_prob)
        print(f"Out-of-sample AUC (L + rolling variance): {auc:.4f}")
        print()
        print("Compare to the AUC from Y ~ L alone.")
        print("If the distributional version is not higher, the distributional")
        print("prediction is not supported by this data.")
    else:
        print("Test set has only one class.")
    print()


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'pooled_trials.csv'
    df = load_data(path)

    descriptive(df)
    logistic_regression(df)
    distributional_test(df)
