
# ================================================================
# NFOT PROTOTYPE v0.1
# Write-Back Gap (L) Timing Demonstration
# Google Colab / Jupyter Notebook
#
# IMPORTANT:
# This is a software-timing pilot, not proof of NFOT.
# Timestamps are software command/callback times, NOT physical
# display-onset measurements. No EEG or biological signals recorded.
# ================================================================

import sys
import time
import random
import platform
from datetime import datetime, timezone

import pandas as pd
import ipywidgets as widgets
from IPython.display import display

# ------------------------- CONFIGURATION -------------------------

TRIALS_PER_CONDITION = 4
ASSIGNED_DELAYS_S = [0.25, 1.00, 2.00]
RANDOM_SEED = None  # Use an integer for repeatable trial order.

# ------------------------- ENVIRONMENT ---------------------------

print("NFOT Timing Demo")
print("Python:", sys.version.split()[0])
print("Platform:", platform.platform())
print("pandas:", pd.__version__)
print("ipywidgets:", widgets.__version__)
print()

# ------------------------- TRIAL PLAN ----------------------------

rng = random.Random(RANDOM_SEED)

conditions = [
    delay
    for delay in ASSIGNED_DELAYS_S
    for _ in range(TRIALS_PER_CONDITION)
]
rng.shuffle(conditions)

trial_plan = [
    {"trial": i + 1, "assigned_delay_s": delay}
    for i, delay in enumerate(conditions)
]

TOTAL_TRIALS = len(trial_plan)

print("Planned trials:", TOTAL_TRIALS)
print("Assigned delays:", ASSIGNED_DELAYS_S)
print("Trials per condition:", TRIALS_PER_CONDITION)

# ------------------------- STATE ---------------------------------

records = []
active_trial = None
task_finished = False
callback_busy = False

def utc_now():
    """UTC wall-clock timestamp for recordkeeping."""
    return datetime.now(timezone.utc).isoformat()

def set_response_buttons(enabled):
    even_button.disabled = not enabled
    odd_button.disabled = not enabled

def show_feedback(message):
    feedback.value = (
        "<div style='padding:12px; border-radius:8px; "
        "border:1px solid #aaa;'>"
        f"{message}</div>"
    )

# ------------------------- USER INTERFACE ------------------------

title = widgets.HTML(
    "<h2>NFOT Write-Back Gap Timing Demo</h2>"
    "<p>Classify each number as even or odd.</p>"
)

status = widgets.HTML("<p>Ready to begin.</p>")

stimulus = widgets.HTML(
    "<div style='font-size:24px; padding:20px; "
    "border:1px solid #aaa; border-radius:8px;'>"
    "Press Start trial when ready.</div>"
)

feedback = widgets.HTML("<p>Feedback will appear here.</p>")

even_button = widgets.Button(
    description="Even",
    button_style="primary",
    disabled=True,
    layout=widgets.Layout(width="130px", height="45px")
)

odd_button = widgets.Button(
    description="Odd",
    button_style="primary",
    disabled=True,
    layout=widgets.Layout(width="130px", height="45px")
)

start_button = widgets.Button(
    description="Start trial",
    button_style="success",
    layout=widgets.Layout(width="160px", height="40px")
)

validate_button = widgets.Button(
    description="Validate and download CSV",
    button_style="info",
    disabled=True,
    layout=widgets.Layout(width="260px", height="40px")
)

output = widgets.Output()

ui = widgets.VBox([
    title,
    status,
    stimulus,
    widgets.HBox([even_button, odd_button]),
    feedback,
    start_button,
    validate_button,
    output
])

display(ui)

# ------------------------- START TRIAL ---------------------------

def on_start_clicked(_):
    global active_trial, task_finished

    if task_finished or active_trial is not None:
        return

    if len(records) >= TOTAL_TRIALS:
        finish_task()
        return

    plan = trial_plan[len(records)]
    number = rng.randint(1, 99)

    active_trial = {
        "trial": plan["trial"],
        "assigned_delay_s": float(plan["assigned_delay_s"]),
        "number": number,
        "correct_answer": "Even" if number % 2 == 0 else "Odd",
    }

    # t0: immediately before requesting the stimulus widget update.
    active_trial["t0_utc"] = utc_now()
    active_trial["t0_perf"] = time.perf_counter()

    stimulus.value = (
        "<div style='font-size:20px;'>"
        "Is this number even or odd?</div>"
        f"<div style='font-size:52px; font-weight:bold; "
        f"padding:15px;'>{number}</div>"
    )

    status.value = (
        f"<p>Trial {plan['trial']} of {TOTAL_TRIALS}</p>"
    )

    show_feedback("Choose Even or Odd.")
    set_response_buttons(True)
    start_button.disabled = True

# ------------------------- HANDLE RESPONSE -----------------------

def on_response(answer):
    global active_trial, callback_busy

    # Prevent double clicks and overlapping callbacks.
    if active_trial is None or callback_busy:
        return

    callback_busy = True
    set_response_buttons(False)

    try:
        # t_response: when Python begins handling the button callback.
        t_response_perf = time.perf_counter()
        t_response_utc = utc_now()

        rt_s = t_response_perf - active_trial["t0_perf"]
        assigned_delay = active_trial["assigned_delay_s"]
        correct = answer == active_trial["correct_answer"]

        # Intentional post-response wait.
        time.sleep(assigned_delay)

        # t_fb: immediately before requesting feedback widget update.
        t_fb_perf = time.perf_counter()
        t_fb_utc = utc_now()

        achieved_delay = t_fb_perf - t_response_perf
        L_s = t_fb_perf - active_trial["t0_perf"]

        record = {
            "trial": active_trial["trial"],
            "assigned_delay_s": assigned_delay,
            "number": active_trial["number"],
            "response": answer,
            "correct_answer": active_trial["correct_answer"],
            "rt_s": rt_s,
            "achieved_post_response_delay_s": achieved_delay,
            "delay_error_s": achieved_delay - assigned_delay,
            "L_s": L_s,
            "correct": bool(correct),
            "t0_utc": active_trial["t0_utc"],
            "t_response_utc": t_response_utc,
            "t_fb_utc": t_fb_utc,
        }

        records.append(record)

        # Round only for presentation/export consistency.
        # Keep full-precision values in memory for calculations.
        show_feedback(
            "Correct!" if correct
            else "Incorrect. The correct answer was "
                 + active_trial["correct_answer"] + "."
        )

        status.value = (
            f"<p>Completed {len(records)} of {TOTAL_TRIALS} trials.</p>"
        )

        active_trial = None

        if len(records) >= TOTAL_TRIALS:
            finish_task()
        else:
            start_button.disabled = False

    finally:
        callback_busy = False

# ------------------------- FINISH TASK ---------------------------

def finish_task():
    global task_finished

    task_finished = True
    set_response_buttons(False)
    start_button.disabled = True
    validate_button.disabled = False

    status.value = (
        "<p><b>All trials completed.</b> "
        "Validate the records and download your CSV.</p>"
    )

def on_even_clicked(_):
    on_response("Even")

def on_odd_clicked(_):
    on_response("Odd")

even_button.on_click(on_even_clicked)
odd_button.on_click(on_odd_clicked)
start_button.on_click(on_start_clicked)

# ------------------------- VALIDATION + EXPORT -------------------

def validate_and_download(_):
    with output:
        output.clear_output(wait=True)

        if len(records) != TOTAL_TRIALS:
            print(
                f"FAIL: expected {TOTAL_TRIALS} trials, "
                f"found {len(records)}."
            )
            return

        df = pd.DataFrame(records)

        # Check assigned condition counts.
        expected_counts = pd.Series(
            ASSIGNED_DELAYS_S, dtype=float
        ).value_counts().sort_index()

        actual_counts = (
            df["assigned_delay_s"].value_counts().sort_index()
        )

        counts_ok = expected_counts.equals(actual_counts)

        # Check L = RT + achieved post-response delay.
        l_difference = (
            df["L_s"]
            - (
                df["rt_s"]
                + df["achieved_post_response_delay_s"]
            )
        ).abs()

        # Check delay_error = achieved - assigned.
        delay_difference = (
            df["delay_error_s"]
            - (
                df["achieved_post_response_delay_s"]
                - df["assigned_delay_s"]
            )
        ).abs()

        numeric_cols = [
            "rt_s",
            "achieved_post_response_delay_s",
            "delay_error_s",
            "L_s",
        ]

        finite_ok = (
            df[numeric_cols].notna().all().all()
            and df[numeric_cols].map(
                lambda col: col.map(
                    lambda value: abs(value) != float("inf")
                )
            ).all().all()
        )

        unique_trials_ok = (
            df["trial"].nunique() == TOTAL_TRIALS
        )

        print("========== VALIDATION REPORT ==========")
        print(f"Trial count: {len(df)} / {TOTAL_TRIALS}")
        print("Condition counts correct:", counts_ok)
        print("Trial IDs unique:", unique_trials_ok)
        print("Timing values finite:", finite_ok)
        print(
            "Max |L - (RT + achieved delay)|:",
            f"{l_difference.max():.8f} s"
        )
        print(
            "Max delay-error arithmetic difference:",
            f"{delay_difference.max():.8f} s"
        )

        checks_pass = (
            counts_ok
            and unique_trials_ok
            and finite_ok
            and l_difference.max() < 1e-4
            and delay_difference.max() < 1e-4
        )

        print("Basic checks passed:", checks_pass)

        print("\n========== SUMMARY BY CONDITION ==========")

        summary = (
            df.groupby("assigned_delay_s")
            .agg(
                n=("trial", "count"),
                mean_L_s=("L_s", "mean"),
                sd_L_s=("L_s", "std"),
                mean_RT_s=("rt_s", "mean"),
                mean_achieved_delay_s=(
                    "achieved_post_response_delay_s", "mean"
                ),
                mean_delay_error_s=("delay_error_s", "mean"),
                accuracy=("correct", "mean"),
            )
            .reset_index()
        )

        display(summary.round(4))

        print("\n========== SCIENTIFIC LIMITATIONS ==========")
        print("• This is a small software-timing pilot.")
        print("• L includes response time and post-response delay.")
        print("• Widget update requests are not physical display-onset times.")
        print("• This task does not measure learning or EEG.")
        print("• Passing checks does not validate the NFOT hypothesis.")

        timestamp = datetime.now(timezone.utc).strftime(
            "%Y%m%dT%H%M%SZ"
        )

        filename = f"nfot_timing_pilot_{timestamp}.csv"

        # Round numeric values for a tidy CSV.
        export_df = df.copy()
        for col in numeric_cols:
            export_df[col] = export_df[col].round(6)

        export_df.to_csv(filename, index=False)

        print(f"\nCSV saved: {filename}")

        try:
            from google.colab import files
            files.download(filename)
        except ImportError:
            print(
                "Not running in Google Colab. "
                "The CSV is saved in the notebook working directory."
            )

validate_button.on_click(validate_and_download)

print("\nReady. Click Start trial to begin.")
