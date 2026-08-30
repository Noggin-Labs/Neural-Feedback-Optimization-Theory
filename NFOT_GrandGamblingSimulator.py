#@title 🎲 NFOT Grand Gambling Simulator (With Mitigation Filter) { run: "auto" }
import numpy as np
import matplotlib.pyplot as plt

#@markdown ### 🎛️ Configure Mathematical System Constraints and Try your Luck!:
target_latency_ms = 3.12 #@param {type:"slider", min:1, max:50, step:0.5}
system_noise_jitter = 30 #@param {type:"slider", min:0, max:50, step:1}
#@markdown ### 🛡️ Activate Algorithmic Edge Patch:
activate_moving_average_filter = True #@param {type:"boolean"}

c_potentiation = 1500
c_depression = 3500
total_events = 500
trials = np.arange(1, total_events + 1)

# Generate raw stochastic latency distributions
np.random.seed(42)
raw_noise = np.random.exponential(scale=system_noise_jitter, size=total_events)
raw_latencies = target_latency_ms + raw_noise

# Apply our Edge Predictive Mitigation Filter if enabled
if activate_moving_average_filter:
    # A 5-point moving window acts as a low-pass filter to smooth out sudden hardware spikes
    window_size = 5
    actual_latencies = np.convolve(raw_latencies, np.ones(window_size)/window_size, mode='same')
    # Correct edge artifacts from convolution
    actual_latencies[:window_size] = raw_latencies[:window_size]
    actual_latencies[-window_size:] = raw_latencies[-window_size:]
else:
    actual_latencies = raw_latencies

# --- Dynamic Scaling for 28.42ms Crossover ---
crossover_threshold = 28.42

# Calculate the exact scaling factor needed to make curves cross at 28.42 ms
ltd_at_threshold = c_depression / (crossover_threshold**2 + c_depression)
scaled_c_potentiation = ltd_at_threshold * (crossover_threshold**2 + c_potentiation)

# Corrected efficiency equations
eff_LTP = scaled_c_potentiation / (actual_latencies**2 + c_potentiation)
eff_LTD = c_depression / (actual_latencies**2 + c_depression)
net_shifts = eff_LTP - eff_LTD


# Compute evaluation metrics
mean_latency = np.mean(actual_latencies)
losing_trials = np.sum(net_shifts < 0)
winning_trials = total_events - losing_trials
win_percentage = (winning_trials / total_events) * 100

# --- Render Visualizations ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), dpi=120, facecolor='#ffffff')

# Top Plot: Latency Profiles
ax1.plot(trials, raw_latencies, color='#ff7f0e', alpha=0.3, linewidth=1, label='Raw Unfiltered Jitter')
ax1.plot(trials, actual_latencies, color='#1f77b4', alpha=0.9, linewidth=1.5, label='Filtered Loop Latency')
ax1.axhline(y=target_latency_ms, color='#2ca02c', linestyle='--', label=f'Baseline Profile ({target_latency_ms}ms)')
ax1.set_ylabel('Write-Back Gap ($L$) [ms]', fontsize=10, fontweight='bold')
ax1.set_title('Real-Time BCI Hardware Latency Jitter Mitigation', fontsize=12, fontweight='bold')
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='upper right')

# Bottom Plot: ABETH Shifts
ax2.plot(trials, net_shifts, color='#7f7f7f', linewidth=0.8, alpha=0.4)
ax2.fill_between(trials, net_shifts, 0, where=(net_shifts >= 0), color='#2ca02c', alpha=0.4, label='Potentiation Zone')
ax2.fill_between(trials, net_shifts, 0, where=(net_shifts < 0), color='#d62728', alpha=0.4, label='Depressive Bias Zone (ABETH)')
ax2.set_xlabel('Feedback Event Sequence (Evaluations)', fontsize=10, fontweight='bold')
ax2.set_ylabel(r'Net Learning Shift ($	riangle W$)', fontsize=10, fontweight='bold')
ax2.set_title('Dynamic Synaptic Weight Adjustments Under Mitigation', fontsize=12, fontweight='bold')
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(loc='lower left')

plt.tight_layout()
plt.show()

print("\n" + "="*55)
print("     NFOT GRAND GAMBLING SIMULATOR RECEIPT    ")
print("="*55)
print(f"  Target Baseline Specification: {target_latency_ms} ms")
print(f"  Computed Mean System Latency:  {mean_latency:.2f} ms")
print(f"  Potentiation Events Sustained: {winning_trials} times")
print(f"  Depressive Deviations (ABETH): {losing_trials} times")
print(f"  Sustained Target System Success Rate: {win_percentage:.1f}%")
print("="*55)
if win_percentage > 75:
    print("  🏆 STATUS: Pipeline optimized. Synaptic reinforcement remains structurally stable.")
else:
    print("  ⚠️ STATUS: Jitter thresholds exceeded. System experiencing systemic efficiency losses.")
print("="*55)
print(" 🎲 | Thanks for playing the NFOT Grand Gambling Simulator, you scallywag scientist! Now GET OUT.")
