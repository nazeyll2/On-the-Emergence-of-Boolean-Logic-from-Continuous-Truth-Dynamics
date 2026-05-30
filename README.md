# On-the-Emergence-of-Boolean-Logic-from-Continuous-Truth-Dynamics
# Continuous Truth Dynamics and Emergent Boolean Regimes

This repository contains the numerical experiments supporting a theoretical framework in which Boolean-like truth regimes emerge from continuous nonlinear truth dynamics.

The central idea is that truth values need not be assumed to be discrete from the outset. Instead, propositions are represented by bounded continuous variables \(x_i \in [-1,1]\), and their interactions are modeled through nonlinear saturating coupling terms. Under sufficiently strong collective coupling, the neutral truth regime loses stability and separates into two stable bipolar phases. After threshold projection, these stable phases can be interpreted as effective Boolean-like states.

This repository provides the numerical evidence for this mechanism through bifurcation analysis, Lyapunov stability analysis, and finite-size multidimensional simulations.

---

## Relation to the Paper

The numerical simulations in this repository support the main claims developed in the accompanying paper.

The paper proposes that classical Boolean logic may be interpreted not as a fundamental axiomatic structure, but as a stable macroscopic phase emerging from continuous truth dynamics. In this framework, Boolean-like separation arises through a pitchfork bifurcation mechanism, and the stability of the resulting phases is analyzed through local Lyapunov exponents.

The code in this repository supports three main parts of the paper:

1. **Pitchfork bifurcation of truth dynamics**

   The reduced one-dimensional truth dynamics is numerically integrated for different values of the coupling parameter \(g\). The results show that the neutral state loses stability at the analytically predicted critical coupling \(g_c\), and two symmetric stable branches emerge.

2. **Local Lyapunov stability of truth phases**

   The local Lyapunov exponent \(\Lambda\) is computed around the neutral and symmetry-broken branches. The sign change of \(\Lambda\) identifies the transition from the stable neutral phase to the unstable neutral regime and the emergence of stable Boolean-like attractor phases.

3. **Finite-size \(N\)-dimensional robustness**

   The model is extended to finite \(N\)-dimensional systems with \(N=\{8,16,32,64\}\). The asymptotic order parameter \(|m_\ast|\) is used to measure Boolean-like polarization. The persistence of this order parameter with increasing \(N\) indicates that the observed Boolean-like separation is not merely a one-dimensional artifact, but a robust collective feature of the proposed dynamics.

---

## Repository Structure

```text
.
├── bifurcation_truth_dynaamics.py
├── lyapunoc_truth_phases.py
├── finite_size_order_parameter.py
├── Appendix/
│   └── appendix_materials.pdf
├── figures/
│   ├── bifurcation_truth_dynamics.png
│   ├── lyapunov_truth_phases.png
│   ├── finite_size_order_parameter.png
│   └── finite_size_steepness.png
└── README.md
````

> Note: The file names can be kept as they are, but for clarity it is recommended to rename them as:
>
> ```text
> bifurcation_truth_dynamics.py
> lyapunov_truth_phases.py
> finite_size_order_parameter.py
> ```

---

## Numerical Model

The reduced truth dynamics has the form

```math
\frac{dx}{dt}
=
-\lambda x
+
g
\frac{\tanh(2\varepsilon x)}
{\tanh(2\varepsilon)}.
```

Here:

* (\lambda>0) is the damping or relaxation coefficient,
* (\varepsilon>0) controls the sharpness of the nonlinear interaction,
* (g) is the collective coupling strength.

The analytical critical coupling is

```math
g_c
=
\lambda
\frac{\tanh(2\varepsilon)}
{2\varepsilon}.
```

For (g<g_c), the neutral state remains stable. For (g>g_c), the system undergoes a supercritical pitchfork bifurcation and separates into two stable Boolean-like phases.

---

## Scripts

### 1. `bifurcation_truth_dynaamics.py`

This script performs the numerical bifurcation analysis of the reduced truth dynamics.

It scans the coupling strength (g\in[0,1]), integrates the dynamics from small positive and negative initial conditions, and plots the asymptotic truth phase (x_\ast). The critical coupling (g_c) is also shown in the figure.

Expected output:

```text
bifurcation_truth_dynamics.png
bifurcation_truth_dynamics.pdf
```

---

### 2. `lyapunoc_truth_phases.py`

This script computes the local Lyapunov stability of the truth phases.

It evaluates the local Lyapunov exponent

```math
\Lambda
=
-\lambda
+
g
\frac{2\varepsilon\,\mathrm{sech}^2(2\varepsilon x_\ast)}
{\tanh(2\varepsilon)}
```

along the neutral, positive, and negative branches. The sign of (\Lambda) determines whether a fixed point is locally stable or unstable.

Expected output:

```text
lyapunov_truth_phases.png
lyapunov_truth_phases.pdf
```

---

### 3. `finite_size_order_parameter.py`

This script tests whether the Boolean-like phase separation persists in finite (N)-dimensional systems.

The (N)-dimensional mean-field truth dynamics is integrated for

```math
N=\{8,16,32,64\}.
```

The asymptotic polarization

```math
|m_\ast|
=
\left|
\frac{1}{N}
\sum_{i=1}^{N} x_i
\right|
```

is used as an effective order parameter for Boolean-like collective organization.

Expected output:

```text
finite_size_order_parameter.png
finite_size_order_parameter.pdf
finite_size_steepness.png
finite_size_steepness.pdf
```

---

## Installation

The simulations require Python 3 and the following packages:

```bash
pip install numpy matplotlib
```

---

## Running the Simulations

Run each script independently:

```bash
python bifurcation_truth_dynaamics.py
python lyapunoc_truth_phases.py
python finite_size_order_parameter.py
```

Each script produces publication-ready figures in both `.png` and `.pdf` formats.



## Appendix Materials

The appendix contains the detailed analytical derivations supporting the numerical simulations, including:

* boundary preservation of the nonlinear truth operator,
* weak-coupling and strong-coupling limits,
* derivation of the critical coupling (g_c),
* local Lyapunov stability analysis,
* gradient-flow interpretation,
* additional comments on the Gödel regime and threshold projection.

The appendix is included to make the analytical background of the numerical experiments explicit and reproducible.


## Main Interpretation

The numerical results support the following interpretation:

* Boolean-like truth values can emerge from continuous truth variables.
* The transition is controlled by a nonlinear collective coupling parameter.
* The neutral truth regime loses stability at a critical threshold.
* Stable bipolar truth phases appear as attractors.
* Threshold projection maps these stable continuous phases to effective Boolean states.
* The phenomenon persists in finite (N)-dimensional systems, suggesting that the mechanism is not merely a one-dimensional artifact.

In this sense, the repository provides computational support for a dynamical view of Boolean logic, where discrete symbolic regimes arise as stable macroscopic outcomes of an underlying continuous nonlinear truth dynamics.


## License

This repository is intended for academic and research purposes. A license file may be added depending on the intended mode of distribution.
