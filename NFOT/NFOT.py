import time
import numpy as np
from collections import deque
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, DetrendOperations, WindowOperations, FilterTypes

try:
    from IPython.display import clear_output
    HAS_IPYTHON = True
except ImportError:
    HAS_IPYTHON = False
    import os

# --- NFOT Closed-Loop Parameters ---
ALPHA_TARGET_BAND = (8.0, 12.0)
TOTAL_BAND = (2.0, 45.0)
WINDOW_SIZE = 8            # Ring buffer history depth
MIN_SLEEP = 0.05           # Max responsive state (50ms gap)
MAX_SLEEP = 0.80           # Resource-conservation state (800ms gap)
ALPHA_THRESHOLD = 0.35     # Sigmoid midpoint gain shift
SIGMOID_K = 12.0           # Gain sensitivity slope

def calculate_continuous_gap(alpha_val: float) -> float:
    """Computes dynamic write-back gap via continuous NFOT sigmoidal modulation."""
    # Sigmoidal mapping: Higher alpha smoothly compresses polling sleep interval
    gain = 1.0 / (1.0 + np.exp(-SIGMOID_K * (alpha_val - ALPHA_THRESHOLD)))
    return MAX_SLEEP - gain * (MAX_SLEEP - MIN_SLEEP)

def clean_console():
    """Universal console clear tool for notebook vs local scripts."""
    if HAS_IPYTHON:
        clear_output(wait=True)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')

def main():
    params = BrainFlowInputParams()
    board_id = BoardIds.SYNTHETIC_BOARD.value
    board = BoardShim(board_id, params)

    alpha_history = deque(maxlen=WINDOW_SIZE)
    current_sleep = MAX_SLEEP

    try:
        board.prepare_session()
        board.start_stream()
        sampling_rate = BoardShim.get_sampling_rate(board_id)
        eeg_channels = BoardShim.get_eeg_channels(board_id)[:2]
        nfft = DataFilter.get_nearest_power_of_two(sampling_rate)

        print("--- NFOT Continuous Polling Engine Active ---")

        while True:
            time.sleep(current_sleep)

            # Pull double the sample buffer size to guarantee enough data points for Welch NFFT calculation
            data = board.get_current_board_data(sampling_rate * 2)
            if data is None or data.shape[1] < nfft:
                continue

            channel_powers = []

            for ch in eeg_channels:
                # Isolate channel slice memory as a contiguous vector to prevent in-place matrix mutation
                channel_data = np.ascontiguousarray(data[ch], dtype=np.float64)

                # Corrected Bandpass Center = 23.5Hz ((45+2)/2), Bandwidth = 43.0Hz (45-2)
                DataFilter.perform_bandpass(
                    channel_data, sampling_rate, 23.5, 43.0, 4, FilterTypes.BUTTERWORTH.value, 0
                )
                DataFilter.detrend(channel_data, DetrendOperations.CONSTANT.value)

                # Spectral power estimation using isolated channel data vector
                psd = DataFilter.get_psd_welch(
                    channel_data, nfft, nfft // 2, sampling_rate, WindowOperations.BLACKMAN_HARRIS.value
                )
                alpha_power = DataFilter.get_band_power(psd, ALPHA_TARGET_BAND[0], ALPHA_TARGET_BAND[1])
                total_power = DataFilter.get_band_power(psd, TOTAL_BAND[0], TOTAL_BAND[1])

                channel_powers.append(alpha_power / total_power if total_power > 0 else 0.0)

            # --- Continuous NFOT State Tracking and Updates ---
            current_alpha = float(np.mean(channel_powers))
            alpha_history.append(current_alpha)
            smoothed_alpha = float(np.mean(alpha_history))

            current_sleep = calculate_continuous_gap(smoothed_alpha)
            compression_ratio = ((MAX_SLEEP - current_sleep) / (MAX_SLEEP - MIN_SLEEP)) * 100

            # Diagnostic Output Rendering
            clean_console()
            print(f"--- NFOT Continuous Polling Engine Active ---")
            print(f"Smoothed Alpha Index: {smoothed_alpha:.4f}")
            print(f"Polling Interval:     {current_sleep * 1000:.1f} ms")
            print(f"Write-Back Gap state: {compression_ratio:.1f}% Compressed")

    except KeyboardInterrupt:
        print("\n[NFOT Engine] Termination signal received.")
    except Exception as e:
        print(f"\n[NFOT Engine] Operational Error: {e}")
    finally:
        if board.is_prepared():
            board.stop_stream()
            board.release_session()
            print("--- Session Safely Closed ---")

if __name__ == '__main__':
    main()
