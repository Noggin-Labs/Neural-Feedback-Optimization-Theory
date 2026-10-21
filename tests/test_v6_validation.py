import tempfile
import unittest
from pathlib import Path

import pandas as pd

from analysis.analyze_trials import AnalysisError, read_trials, run_analysis
from analysis.extract import ExtractionConfig, ExtractionError, extract_trials_from_frame
from analysis.v7_power_simulation import simulate


class V6ValidationTests(unittest.TestCase):
    def base(self):
        return pd.DataFrame({
            "file": ["a.edf", "a.edf", "b.edf"],
            "trial": [0, 1, 0],
            "t0_s": [1.0, 3.0, 2.0],
            "tfb_s": [2.0, 5.0, 4.0],
            "L_s": [1.0, 2.0, 2.0],
            "Y": [1, 0, 1],
            "subject": ["S1", "S1", "S2"],
        })

    def write(self, frame, directory):
        path = Path(directory) / "trials.csv"
        frame.to_csv(path, index=False)
        return path

    def test_valid_table_and_output_schema(self):
        with tempfile.TemporaryDirectory() as td:
            path = self.write(self.base(), td)
            df = read_trials(path)
            report = run_analysis(df, Path(td) / "out")
            self.assertEqual(report["input_rows"], 3)
            self.assertEqual(report["n_subjects"], 2)
            self.assertAlmostEqual(report["accuracy"], 2 / 3)
            self.assertTrue((Path(td) / "out" / "analysis_report.json").is_file())
            self.assertTrue((Path(td) / "out" / "participant_summary.csv").is_file())

    def test_rejects_gap_mismatch(self):
        frame = self.base()
        frame.loc[0, "L_s"] = 9.0
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(AnalysisError):
                read_trials(self.write(frame, td))

    def test_rejects_duplicate_trial_identifier(self):
        frame = self.base()
        frame.loc[2, "file"] = "a.edf"
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(AnalysisError):
                read_trials(self.write(frame, td))

    def test_rejects_invalid_binary_label(self):
        frame = self.base()
        frame.loc[0, "Y"] = 2
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(AnalysisError):
                read_trials(self.write(frame, td))

    def event_frame(self):
        return pd.DataFrame({
            "PhaseInSequence": [1, 2, 2, 2, 3, 3, 3, 2, 2, 3, 3],
            "StimulusBegin": [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            "DisplayResult": [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            "CurrentTarget": [0, 0, 5, 5, 5, 5, 0, 0, 9, 9, 0],
            "SelectedTarget": [0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 9],
            "StimulusType": [0] * 11,
        })

    def test_event_edges_and_label_construction(self):
        result = extract_trials_from_frame(
            self.event_frame(), ExtractionConfig(time_unit="seconds"), "x.csv"
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(result.loc[0, "Y"], 1)
        self.assertEqual(result.loc[1, "Y"], 1)
        self.assertEqual(result.loc[0, "source_t0_row"], 2)
        self.assertEqual(result.loc[0, "source_tfb_row"], 5)

    def test_millisecond_conversion_is_explicit(self):
        result = extract_trials_from_frame(
            self.event_frame(), ExtractionConfig(time_unit="milliseconds"), "x.csv"
        )
        self.assertAlmostEqual(result.loc[0, "L_s"], 0.003)

    def test_missing_feedback_event_fails_closed(self):
        frame = self.event_frame()
        frame["DisplayResult"] = 0
        with self.assertRaises(ExtractionError):
            extract_trials_from_frame(frame, ExtractionConfig(), "x.csv")

    def test_synthetic_power_simulation_is_deterministic(self):
        kwargs = dict(
            n_participants=6,
            trials_per_condition=8,
            baseline_probability=0.7,
            absolute_effect=0.1,
            repetitions=20,
            seed=123,
        )
        self.assertEqual(simulate(**kwargs), simulate(**kwargs))

    def test_synthetic_power_simulation_rejects_invalid_probability(self):
        with self.assertRaises(ValueError):
            simulate(
                n_participants=6,
                trials_per_condition=8,
                baseline_probability=0.99,
                absolute_effect=0.1,
                repetitions=20,
                seed=123,
            )


if __name__ == "__main__":
    unittest.main()
