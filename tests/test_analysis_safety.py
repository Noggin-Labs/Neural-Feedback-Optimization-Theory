
import unittest

import pandas as pd

from analysis.analyze import add_past_only_variance


class AnalysisSafetyTests(unittest.TestCase):
    def test_rolling_variance_uses_only_prior_trials(self):
        df = pd.DataFrame({
            "recording_id": ["A"] * 4,
            "trial": [1, 2, 3, 4],
            "L": [1.0, 3.0, 100.0, 5.0],
        })

        result = add_past_only_variance(df, window=5, min_periods=2)

        self.assertTrue(pd.isna(result.loc[0, "L_prior_var"]))
        self.assertTrue(pd.isna(result.loc[1, "L_prior_var"]))
        self.assertAlmostEqual(result.loc[2, "L_prior_var"], 2.0)
        self.assertAlmostEqual(
            result.loc[3, "L_prior_var"], pd.Series([1.0, 3.0, 100.0]).var()
        )


    def test_rolling_variance_does_not_cross_recordings(self):
        df = pd.DataFrame({
            "recording_id": ["A", "A", "B", "B"],
            "trial": [1, 2, 1, 2],
            "L": [1.0, 3.0, 50.0, 70.0],
        })

        result = add_past_only_variance(df, window=5, min_periods=2)

        self.assertTrue(pd.isna(result.loc[2, "L_prior_var"]))
        self.assertTrue(pd.isna(result.loc[3, "L_prior_var"]))


    def test_rolling_variance_rejects_invalid_window(self):
        df = pd.DataFrame({
            "recording_id": ["A"],
            "trial": [1],
            "L": [1.0],
        })

        with self.assertRaises(ValueError):
            add_past_only_variance(df, window=1)


if __name__ == "__main__":
    unittest.main()
