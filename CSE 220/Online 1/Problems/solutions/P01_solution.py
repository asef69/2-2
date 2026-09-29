"""
Problem 1 - Energy, Power, and Signal Classification
Reference solution.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def energy_ct(t: np.ndarray, x: np.ndarray) -> float:
    """Energy of a sampled continuous-time signal: integral of |x|^2 dt
    (trapezoidal rule)."""
    return float(np.trapezoid(np.abs(x) ** 2, t))


def power_ct(t: np.ndarray, x: np.ndarray) -> float:
    """Average power of a sampled CT signal: energy / (length of interval)."""
    T = t[-1] - t[0]
    return energy_ct(t, x) / T


def energy_dt(x: np.ndarray) -> float:
    """Energy of a discrete-time signal: sum of |x[n]|^2."""
    return float(np.sum(np.abs(x) ** 2))


def power_dt(x: np.ndarray) -> float:
    """Average power of a discrete-time signal: mean of |x[n]|^2."""
    return float(np.mean(np.abs(x) ** 2))


def classify(energies: np.ndarray, powers: np.ndarray,
             e_tol: float = 1e6, p_tol: float = 1e-6) -> str:
    """Classify a signal from its energy/power measured over a sequence of
    growing windows.

      * Energy signal : energy converges to a finite limit, power -> 0.
      * Power signal  : energy grows without bound, but power -> finite > 0.
      * Neither       : both blow up (or neither settles).
    """
    E_last = energies[-1]
    P_last = powers[-1]
    # Did the energy settle (last two windows agree to within 1%)?
    energy_settled = abs(energies[-1] - energies[-2]) <= 0.02 * abs(energies[-1] + 1e-12)
    # Did the power settle to a positive constant?
    power_settled = abs(powers[-1] - powers[-2]) <= 0.02 * abs(powers[-1] + 1e-12)

    if energy_settled and E_last < e_tol:
        return "energy"
    if power_settled and P_last > p_tol:
        return "power"
    return "neither"


# ----------------------------
# Test signals (provided)
# ----------------------------
def make_ct_signals():
    """Return a dict name -> callable x(t) for CT signals."""
    return {
        "e^{-|t|}":            lambda t: np.exp(-np.abs(t)),
        "cos(2*pi*0.5*t)":     lambda t: np.cos(2 * np.pi * 0.5 * t),
        "constant 1":          lambda t: np.ones_like(t),
        "t (ramp)":            lambda t: t.astype(float),
    }


def make_dt_signals():
    return {
        "(0.8)^n u[n]":        lambda n: np.where(n >= 0, 0.8 ** np.abs(n), 0.0),
        "cos(pi n / 6)":       lambda n: np.cos(np.pi * n / 6),
        "n (ramp)":            lambda n: n.astype(float),
    }


def analyse_ct(name, xfunc, half_widths):
    Es, Ps = [], []
    for T in half_widths:
        t = np.linspace(-T, T, int(2000 * T) + 1)
        x = xfunc(t)
        Es.append(energy_ct(t, x))
        Ps.append(power_ct(t, x))
    return np.array(Es), np.array(Ps)


def analyse_dt(name, xfunc, half_lengths):
    Es, Ps = [], []
    for M in half_lengths:
        n = np.arange(-M, M + 1)
        x = xfunc(n)
        Es.append(energy_dt(x))
        Ps.append(power_dt(x))
    return np.array(Es), np.array(Ps)


def main():
    half_widths = [5, 10, 20, 40, 80]
    print("=== Continuous-time signals ===")
    for name, f in make_ct_signals().items():
        E, P = analyse_ct(name, f, half_widths)
        kind = classify(E, P)
        print(f"{name:22s} | E(last)={E[-1]:.4g}  P(last)={P[-1]:.4g}  -> {kind}")

    print("\n=== Discrete-time signals ===")
    half_lengths = [24, 120, 600, 1200, 3000]
    for name, f in make_dt_signals().items():
        E, P = analyse_dt(name, f, half_lengths)
        kind = classify(E, P)
        print(f"{name:22s} | E(last)={E[-1]:.4g}  P(last)={P[-1]:.4g}  -> {kind}")

    # Figure: energy growth for one of each type
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for name, f in make_ct_signals().items():
        E, P = analyse_ct(name, f, half_widths)
        ax[0].plot(half_widths, E, marker="o", label=name)
    ax[0].set_title("Energy vs window (CT)")
    ax[0].set_xlabel("half-width T"); ax[0].set_ylabel("E[-T,T]")
    ax[0].set_ylim(0, 20); ax[0].legend(fontsize=7); ax[0].grid(alpha=.3)
    for name, f in make_ct_signals().items():
        E, P = analyse_ct(name, f, half_widths)
        ax[1].plot(half_widths, P, marker="s", label=name)
    ax[1].set_title("Power vs window (CT)")
    ax[1].set_xlabel("half-width T"); ax[1].set_ylabel("P[-T,T]")
    ax[1].legend(fontsize=7); ax[1].grid(alpha=.3)
    fig.tight_layout()
    plt.show()

    # ---- verification ----
    t = np.linspace(-60, 60, 240001)
    assert abs(energy_ct(t, np.exp(-np.abs(t))) - 1.0) < 1e-3, "E[e^-|t|] should be 1"
    n = np.arange(0, 200)
    assert abs(energy_dt(0.8 ** n) - 1/(1-0.64)) < 1e-6, "geometric energy"
    print("\nAll assertions passed.")


if __name__ == "__main__":
    main()
