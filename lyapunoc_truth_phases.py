import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Parameters
# ============================================================

lam = 1.0       # damping coefficient
eps = 1.0       # nonlinearity parameter

# Analytical critical coupling
gc = lam * np.tanh(2 * eps) / (2 * eps)
print("Critical coupling gc =", gc)

# Time integration parameters
dt = 0.005
T = 80.0
steps = int(T / dt)

# Coupling range
g_values = np.linspace(0.0, 1.0, 80)

# ============================================================
# Reduced truth dynamics
# ============================================================

def rhs(x, g, lam, eps):
    return -lam * x + g * np.tanh(2 * eps * x) / np.tanh(2 * eps)

def evolve(x0, g, lam, eps, dt, steps):
    x = x0
    for _ in range(steps):
        k1 = rhs(x, g, lam, eps)
        k2 = rhs(x + 0.5 * dt * k1, g, lam, eps)
        k3 = rhs(x + 0.5 * dt * k2, g, lam, eps)
        k4 = rhs(x + dt * k3, g, lam, eps)

        x = x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
    return x

def lyapunov_local(x_star, g, lam, eps):
    sech2 = 1.0 / np.cosh(2 * eps * x_star)**2
    return -lam + g * (2 * eps * sech2) / np.tanh(2 * eps)

# ============================================================
# Numerical scan
# ============================================================

x_plus = []
x_minus = []

lyap_plus = []
lyap_minus = []
lyap_neutral = []

for g in g_values:
    xp = evolve(x0=+0.01, g=g, lam=lam, eps=eps, dt=dt, steps=steps)
    xm = evolve(x0=-0.01, g=g, lam=lam, eps=eps, dt=dt, steps=steps)

    x_plus.append(xp)
    x_minus.append(xm)

    lyap_plus.append(lyapunov_local(xp, g, lam, eps))
    lyap_minus.append(lyapunov_local(xm, g, lam, eps))
    lyap_neutral.append(lyapunov_local(0.0, g, lam, eps))

x_plus = np.array(x_plus)
x_minus = np.array(x_minus)

lyap_plus = np.array(lyap_plus)
lyap_minus = np.array(lyap_minus)
lyap_neutral = np.array(lyap_neutral)

max_abs_x = max(np.max(np.abs(x_plus)), np.max(np.abs(x_minus)))
print("Maximum |x*| reached =", max_abs_x)

if max_abs_x > 1.0:
    print("Warning: Some trajectories left the physical interval [-1,1].")
else:
    print("All asymptotic values remained inside [-1,1].")

# ============================================================
# Plot style: academic / clean
# ============================================================

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 12,
    "axes.labelsize": 13,
    "axes.titlesize": 13,
    "legend.fontsize": 11,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "axes.linewidth": 1.0,
})

fig, ax = plt.subplots(figsize=(6.5, 4.5))

# Neutral branch
ax.plot(
    g_values,
    lyap_neutral,
    color="black",
    linewidth=2.0,
    label=r"neutral state $x_\ast=0$"
)

# Positive branch
ax.plot(
    g_values,
    lyap_plus,
    color="dimgray",
    linewidth=2.0,
    label=r"positive branch"
)

# Negative branch
ax.plot(
    g_values,
    lyap_minus,
    color="dimgray",
    linewidth=2.0,
    linestyle="--",
    label=r"negative branch"
)

# Critical coupling line
ax.axvline(
    gc,
    color="firebrick",
    linestyle=":",
    linewidth=2.0,
    label=fr"$g_c={gc:.3f}$"
)

# Zero line
ax.axhline(
    0,
    color="gray",
    linewidth=0.9,
    alpha=0.8
)

# Labels
ax.set_xlabel(r"Coupling strength $g$")
ax.set_ylabel(r"Local Lyapunov exponent $\Lambda$")

# Optional title: remove if using LaTeX caption only
# ax.set_title("Local Lyapunov stability of truth phases")

# Limits
ax.set_xlim(0.0, 1.0)

# Grid
ax.grid(True, which="major", linestyle=":", linewidth=0.7, alpha=0.6)

# Legend
ax.legend(frameon=True, loc="best")

# Clean layout
fig.tight_layout()

# Save figure
plt.savefig("lyapunov_truth_phases.pdf", bbox_inches="tight")
plt.savefig("lyapunov_truth_phases.png", dpi=300, bbox_inches="tight")

plt.show()