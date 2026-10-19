            "standard_errors": {k: float(v) for k, v in fitted.bse.items()},
            "p_values": {k: float(v) for k, v in fitted.pvalues.items()},
            "confidence_intervals": {
                k: [float(v[0]), float(v[1])]
                for k, v in fitted.conf_int().iterrows()
            },
            "warning": "Exploratory only; 15 clusters is a small basis for robust asymptotic inference.",
        }
        gee_note = "GEE fit completed; interpret cautiously because participants, not trials, are the independent clusters."
    except ImportError:
        pass
    except Exception as exc:
        gee_note = f"GEE fit failed and was omitted: {type(exc).__name__}: {exc}"

    # Small-N participant-level model. This is a key audit because the proposed
    # incremental SD claim is between-person and its independent unit is subject.
    ols_result = None
    ols_note = "Not run; install statsmodels to compute HC3 OLS diagnostics."
    try:
        import statsmodels.api as sm
        predictors = participant[["L_mean", "L_sd"]].copy()
        predictors = (predictors - predictors.mean()) / predictors.std(ddof=1).replace(0, np.nan)
        if not predictors.isna().any().any():
            X = sm.add_constant(predictors)
            fit = sm.OLS(participant["accuracy"], X).fit(cov_type="HC3")
            ols_result = {
                "formula": "participant accuracy ~ standardized L_mean + standardized L_sd",
                "n_subjects": int(len(participant)),
                "coefficients": {k: float(v) for k, v in fit.params.items()},
                "standard_errors_HC3": {k: float(v) for k, v in fit.bse.items()},
                "p_values_HC3": {k: float(v) for k, v in fit.pvalues.items()},
                "confidence_intervals_HC3": {
                    k: [float(v[0]), float(v[1])]
                    for k, v in fit.conf_int().iterrows()
                },
                "r_squared": float(fit.rsquared),
                "warning": "Very small participant-level N; exploratory, not confirmatory.",
            }
            ols_note = "Participant-level OLS fit completed; small-N inference is fragile."
        else:
            ols_note = "OLS omitted because one predictor has zero variance."
    except ImportError:
        pass
    except Exception as exc:
        ols_note = f"OLS fit failed and was omitted: {type(exc).__name__}: {exc}"

    report = {
        "analysis_version": "NFOT-v6-validation-kit-0.1",
        "input_rows": int(len(df)),
        "n_subjects": int(df["subject_id"].nunique()),
        "overall_accuracy": float(df["Y"].mean()),
        "overall_L_mean_seconds": float(df["L"].mean()),
        "overall_L_sd_seconds": float(df["L"].std(ddof=1)),
        "y_counts": {str(int(k)): int(v) for k, v in df["Y"].value_counts().sort_index().items()},
        "participant_correlations": correlations,
        "trial_level_gee": gee_result,
        "trial_level_gee_note": gee_note,
        "participant_level_ols": ols_result,
        "participant_level_ols_note": ols_note,
        "non_reproduced_claims": [
            "Reported thresholds (8.88 s and 12 s) are not treated as confirmatory unless prespecified independently.",
            "Reported AUC delta is not reproduced because the original binary outcome, model, fold construction, and prediction target are not supplied.",
            "LOSO is not reproduced without the exact held-out-subject pipeline, preprocessing, model-selection, and scoring code.",
        ],
        "critical_interpretation": [
            "Participant-level SD is constant within participant; it cannot be estimated as a separate within-participant predictor with subject fixed effects.",
            "For the SD-beyond-mean claim, participant is the independent unit; 444 repeated trials do not make n=15 between-subject observations into n=444.",
            "A same-trial association between L and Y is observational. Feedback delay assigned after the selection cannot cause that already-decided selection's correctness; prospective randomized timing effects should be tested on subsequent outcomes or a clearly defined downstream endpoint.",
        ],
    }
    (outdir / "analysis_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trials_csv", help="Combined extracted trial-level CSV")
    parser.add_argument("--outdir", default="nfot_v6_analysis", help="Output directory")
    args = parser.parse_args()
    try:
        df = read_trials(args.trials_csv)
        report = run_analysis(df, args.outdir)
        print(json.dumps({
            "n_trials": report["input_rows"],
            "n_subjects": report["n_subjects"],
            "accuracy": report["overall_accuracy"],
            "L_mean_seconds": report["overall_L_mean_seconds"],
            "L_sd_seconds": report["overall_L_sd_seconds"],
            "participant_summary": str(Path(args.outdir) / "participant_summary.csv"),
            "full_report": str(Path(args.outdir) / "analysis_report.json"),
        }, indent=2))
        return 0
    except (AnalysisError, OSError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
