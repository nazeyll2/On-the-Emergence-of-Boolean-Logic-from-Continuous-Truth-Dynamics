import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Parameters
# ============================================================

lam = 1.0
eps = 1.0

gc = lam * np.tanh(2 * eps) / (2 * eps)

print("Analytical critical coupling gc =", gc)

# ============================================================
# Numerical settings
# ============================================================

dt = 0.02
T = 80.0
steps = int(T / dt)

# System sizes to test
N_values = [8, 16, 32, 64]

# Coupling values
g_values = np.linspace(0.0, 1.0, 81)

# Number of random trials for each N and g
n_trials = 6

# Initial condition:
# small positive bias selects the positive symmetry-broken branch;
# small disorder tests robustness against finite-N heterogeneity.
bias = 1e-2
disorder = 1e-3

rng = np.random.default_rng(12345)

# ============================================================
# N-dimensional truth dynamics
# ============================================================

def rhs_vector(x, g, lam, eps):
    """
    Full N-dimensional mean-field truth dynamics.

    dx_i/dt = -lambda x_i
              + sum_j W_ij tanh(eps (x_i + x_j)) / tanh(2 eps)

    with W_ii = 0 and W_ij = g/(N-1), i != j.
    """
    N = len(x)

    pair_sum = x[:, None] + x[None, :]
    interaction = np.tanh(eps * pair_sum) / np.tanh(2 * eps)

    # Remove self-coupling: W_ii = 0
    np.fill_diagonal(interaction, 0.0)

    coupling_term = (g / (N - 1)) * np.sum(interaction, axis=1)

    return -lam * x + coupling_term


def rk4_integrate(x0, g, lam, eps, dt, steps):
    """
    Fourth-order Runge-Kutta integration.
    No clipping or artificial bounding is used.
    """
    x = x0.copy()

    for _ in range(steps):
        k1 = rhs_vector(x, g, lam, eps)
        k2 = rhs_vector(x + 0.5 * dt * k1, g, lam, eps)
        k3 = rhs_vector(x + 0.5 * dt * k2, g, lam, eps)
        k4 = rhs_vector(x + dt * k3, g, lam, eps)

        x = x + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

    return x


# ============================================================
# Finite-size scan
# ============================================================

mean_abs_m = {}
std_abs_m = {}
max_abs_x = {}

for N in N_values:
    print(f"\nRunning N = {N}")

    abs_m_for_N = []
    std_m_for_N = []
    max_x_for_N = []

    for g in g_values:
        trial_abs_m = []
        trial_max_x = []

        for trial in range(n_trials):
            x0 = bias + disorder * rng.normal(size=N)

            xT = rk4_integrate(
                x0=x0,
                g=g,
                lam=lam,
                eps=eps,
                dt=dt,
                steps=steps
            )

            mT = np.mean(xT)

            trial_abs_m.append(abs(mT))
            trial_max_x.append(np.max(np.abs(xT)))

        abs_m_for_N.append(np.mean(trial_abs_m))
        std_m_for_N.append(np.std(trial_abs_m))
        max_x_for_N.append(np.max(trial_max_x))

    mean_abs_m[N] = np.array(abs_m_for_N)
    std_abs_m[N] = np.array(std_m_for_N)
    max_abs_x[N] = np.array(max_x_for_N)

    print("Maximum |x_i| reached =", np.max(max_abs_x[N]))

    if np.max(max_abs_x[N]) > 1.0:
        print("Warning: Some trajectories left the interval [-1,1].")
    else:
        print("All trajectories remained inside [-1,1].")


# ============================================================
# Apparent critical point and steepness estimate
# ============================================================

threshold = 1e-2

print("\nFinite-size estimates:")
print("N    g_app      |g_app-gc|     max steepness")

apparent_gc = {}
steepness = {}

for N in N_values:
    y = mean_abs_m[N]

    # Apparent critical point:
    # first g where |m*| becomes larger than threshold
    idx_candidates = np.where(y > threshold)[0]

    if len(idx_candidates) > 0:
        idx = idx_candidates[0]
        g_app = g_values[idx]
    else:
        g_app = np.nan

    apparent_gc[N] = g_app

    # Steepness of transition:
    # maximum numerical derivative d|m*|/dg
    dy_dg = np.gradient(y, g_values)
    steep = np.max(np.abs(dy_dg))
    steepness[N] = steep

    print(f"{N:<4d} {g_app: .6f}   {abs(g_app-gc): .6e}   {steep: .6f}")


# ============================================================
# Academic plot style
# ============================================================

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 12,
    "axes.labelsize": 13,
    "axes.titlesize": 13,
    "legend.fontsize": 10,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "axes.linewidth": 1.0,
})

# ============================================================
# Figure 1: finite-size order parameter curves
# ============================================================

fig, ax = plt.subplots(figsize=(6.7, 4.7))

line_styles = ["-", "--", "-.", ":", "-"]
markers = ["o", "s", "^", "D", "v"]

for k, N in enumerate(N_values):
    ax.plot(
        g_values,
        mean_abs_m[N],
        linestyle=line_styles[k % len(line_styles)],
        marker=markers[k % len(markers)],
        markevery=12,
        linewidth=1.8,
        markersize=4,
        label=fr"$N={N}$"
    )

ax.axvline(
    gc,
    color="firebrick",
    linestyle=":",
    linewidth=2.0,
    label=fr"$g_c={gc:.3f}$"
)

ax.axhline(0, color="gray", linewidth=0.8)

ax.set_xlabel(r"Coupling strength $g$")
ax.set_ylabel(r"Order parameter $|m_\ast|$")
ax.set_xlim(0.0, 1.0)
ax.set_ylim(-0.02, 1.05)

ax.grid(True, which="major", linestyle=":", linewidth=0.7, alpha=0.6)
ax.legend(frameon=True, loc="best")

fig.tight_layout()

plt.savefig("finite_size_order_parameter.pdf", bbox_inches="tight")
plt.savefig("finite_size_order_parameter.png", dpi=300, bbox_inches="tight")

plt.show()


# ============================================================
# Figure 2: steepness versus system size
# ============================================================

fig, ax = plt.subplots(figsize=(6.2, 4.2))

Ns_array = np.array(N_values)
steep_array = np.array([steepness[N] for N in N_values])

ax.plot(
    Ns_array,
    steep_array,
    color="black",
    linewidth=2.0,
    marker="o",
    markersize=5
)

ax.set_xlabel(r"System size $N$")
ax.set_ylabel(r"Maximum transition steepness")
ax.set_xscale("log", base=2)

ax.grid(True, which="major", linestyle=":", linewidth=0.7, alpha=0.6)

fig.tight_layout()

plt.savefig("finite_size_steepness.pdf", bbox_inches="tight")
plt.savefig("finite_size_steepness.png", dpi=300, bbox_inches="tight")

plt.show()