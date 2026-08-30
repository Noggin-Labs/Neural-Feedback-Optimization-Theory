#@title ABETH Synaptic Bias Dashboard { run: "auto" }
import numpy as np
import matplotlib.pyplot as plt

#@markdown ### 🎛️ Adjust ABETH System Constraints:
c_potentiation = 900 #@param {type:"slider", min:500, max:3000, step:100}
c_depression = 3500 #@param {type:"slider", min:2000, max:6000, step:100}
write_back_gap = 100 #@param {type:"slider", min:0, max:100, step:1}

# --- ABETH Mathematical Core Equations ---
L = np.linspace(0, 100, 1000)

# Calculate separate decay envelopes for Potentiation (LTP) and Depression (LTD)
E_LTP = c_potentiation / (L**2 + c_potentiation)
E_LTD = c_depression / (L**2 + c_depression)

# Compute values for your current user-selected Write-Back Gap
current_LTP = c_potentiation / (write_back_gap**2 + c_potentiation)
current_LTD = c_depression / (write_back_gap**2 + c_depression)

# Calculate the Net Learning Bias (LTP efficiency minus LTD efficiency)
net_bias = current_LTP - current_LTD

# --- Style and Render Publication-Quality Output ---
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=150)

# --- Plot 1: Dual Eligibility Envelopes ---
ax1.plot(L, E_LTP, color='#2ca02c', linewidth=2, label='Potentiation Tag ($E_{LTP}$)')
ax1.plot(L, E_LTD, color='#d62728', linewidth=2, label='Depression Tag ($E_{LTD}$)')
ax1.axvline(x=write_back_gap, color='#333333', linestyle=':', alpha=0.8, label=f'Current L ({write_back_gap}ms)')

# Highlights for current position
ax1.scatter(write_back_gap, current_LTP, color='#2ca02c', s=40, zorder=5)
ax1.scatter(write_back_gap, current_LTD, color='#d62728', s=40, zorder=5)

ax1.set_xlim(-2, 100)
ax1.set_ylim(-0.05, 1.05)
ax1.set_xlabel('Write-Back Gap ($L$) [ms]', fontsize=10)
ax1.set_ylabel('Tag Retention Efficiency ($E$)', fontsize=10)
ax1.set_title('Asymmetric Eligibility Trace Decay Profile', fontsize=11, fontweight='bold')
ax1.grid(True, linestyle=':', alpha=0.5)
ax1.legend(loc='upper right', fontsize=8)

# --- Plot 2: Net Dynamic Learning Bias ---
# Generate net bias curve across all latencies
net_curve = (c_potentiation / (L**2 + c_potentiation)) - (c_depression / (L**2 + c_depression))
ax2.plot(L, net_curve, color='#7f7f7f', linewidth=1.5, linestyle='--', label='Net Bias Profile')

# Color the regions to visually illustrate your ABETH hypothesis zones
ax2.fill_between(L, net_curve, 0, where=(net_curve >= 0), color='#2ca02c', alpha=0.2, label='Potentiation Zone')
ax2.fill_between(L, net_curve, 0, where=(net_curve < 0), color='#d62728', alpha=0.2, label='Depressive Bias Zone')
ax2.axvline(x=write_back_gap, color='#333333', linestyle=':', alpha=0.8)

# Highlight current dynamic point
bias_color = '#2ca02c' if net_bias >= 0 else '#d62728'
ax2.scatter(write_back_gap, net_bias, color=bias_color, s=60, edgecolor='black', zorder=5)

ax2.set_xlim(-2, 100)
ax2.set_ylim(-0.4, 0.4)
ax2.set_xlabel('Write-Back Gap ($L$) [ms]', fontsize=10)
ax2.set_ylabel('Net Directional Shift ($\Delta W$)', fontsize=10)
ax2.set_title('ABETH Learning Vector Shift', fontsize=11, fontweight='bold')
ax2.grid(True, linestyle=':', alpha=0.5)
ax2.legend(loc='lower right', fontsize=8)

plt.tight_layout()
plt.show()

# --- Status Readout ---
print("\n" + "="*50)
print(f"  ABETH ANALYSIS FOR L = {write_back_gap} ms")
print("="*50)
print(f"  LTP Tag Efficiency: {current_LTP*100:.2f}%")
print(f"  LTD Tag Efficiency: {current_LTD*100:.2f}%")
if net_bias >= 0:
    print(f"  SYSTEM STATUS: Stable Learning (+{net_bias*100:.2f}% Network Gain)")
else:
    print(f"  SYSTEM STATUS: 📉 SYSTEMATIC DEPRESSIVE BIAS DETECTED ({net_bias*100:.2f}% Loss)")
print("="*50)
