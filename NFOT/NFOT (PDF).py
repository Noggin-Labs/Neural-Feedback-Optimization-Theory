import numpy as np
import matplotlib.pyplot as plt

# Updated font settings to avoid warnings in environments without Arial/Helvetica
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

def generate_nfot_figure():
    # Model parameters
    c = 1500  # Scaling constant for behavioral efficiency decay curve
    L = np.linspace(0, 100, 1000)  # Write-Back Gap Latency in milliseconds
    E = c / (L**2 + c)  # NFOT Core Equation

    # Target benchmark from the edge pipeline
    achieved_latency = 3.12
    achieved_efficiency = c / (achieved_latency**2 + c)

    # Initialize single-column publication-sized figure (3.5 inches wide)
    fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=300)

    # Plot core NFOT decay function
    ax.plot(L, E, color='#1f77b4', linewidth=2, label=r'$E(L) = \frac{c}{L^2 + c}$')

    # Highlight the edge pipeline achievement (3.12 ms)
    ax.axvline(x=achieved_latency, color='#d62728', linestyle='--', alpha=0.7, linewidth=1)
    ax.scatter(achieved_latency, achieved_efficiency, color='#d62728', s=40, zorder=5,
               label=f'Achieved Pipeline ({achieved_latency:.2f} ms)')

    # Annotate the performance node
    ax.annotate(f'{achieved_efficiency*100:.2f}% Efficiency',
                xy=(achieved_latency, achieved_efficiency),
                xytext=(achieved_latency + 8, achieved_efficiency - 0.05),
                arrowprops=dict(arrowstyle="->", color='#d62728', lw=0.8),
                fontsize=8, color='#333333')

    # Formatting axes limits and labels
    ax.set_xlim(-2, 100)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel('Write-Back Gap ($L$) [ms]', fontsize=9, color='#222222')
    ax.set_ylabel('Behavioral Efficiency ($E$)', fontsize=9, color='#222222')
    ax.set_title('NFOT Efficiency Decay Profile', fontsize=10, fontweight='bold', pad=10)

    # Style gridlines and clean boundaries
    ax.grid(True, linestyle=':', alpha=0.5, color='#cccccc')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', labelsize=8, colors='#444444')

    # Legend position
    ax.legend(loc='upper right', fontsize=8, frameon=True, facecolor='white', edgecolor='none')

    plt.tight_layout()

    # Export options
    plt.savefig('nfot_decay_curve.pdf', format='pdf', bbox_inches='tight')
    plt.savefig('nfot_decay_curve.png', format='png', dpi=300, bbox_inches='tight')
    print("Figures successfully exported as 'nfot_decay_curve.pdf' and 'nfot_decay_curve.png'.")
    plt.show()

if __name__ == '__main__':
    generate_nfot_figure()
