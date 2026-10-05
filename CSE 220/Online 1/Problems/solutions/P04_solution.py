"""
Problem 4 - Does an infinite-range signal have finite energy?
Study E(T) = integral_{-T}^{T} |x(t)|^2 dt as T grows.
Reference solution.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# ==========================================================
# ANSWER IMPLEMENTATION
#==========================================================

def energy_window(xfunc, T: float, samples_per_unit: int = 800) -> float:
    """Numerically integrate |x(t)|^2 over [-T, T] (trapezoidal)."""
    n = min(4_000_001, int(samples_per_unit * T) + 1)
    t = np.linspace(-T, T, n)
    x = xfunc(t)
    return float(np.trapezoid(np.abs(x) ** 2, t))


def energy_curve(xfunc, Ts):
    """Return array E(T) for each window half-width in Ts."""
    return np.array([energy_window(xfunc, T) for T in Ts])


def classify_convergence(Ts, E) -> str:
    """Decide from the tail of E(T), assuming Ts grows geometrically (e.g. it
    doubles each step). The right question is not whether E is still changing
    but whether the *increments* are dying out.

       dE_k = E(T_{k+1}) - E(T_k)

       * finite energy : dE_k shrinks toward 0 (here: at least halves over
                         two doubling steps).
       * otherwise     : dE_k stays roughly constant (log-divergent) or grows
                         (power signal) -> infinite energy.
    """
    dE = np.diff(E)
    if len(dE) < 3:
        raise ValueError("need at least 4 window sizes")
    if dE[-1] <= 0.6 * dE[-3] + 1e-12:
        return "finite"
    return "infinite"


def estimated_limit(Ts, E) -> float:
    """Best estimate of the total energy: the last (largest-window) value."""
    return float(E[-1])


# ----------------------------
# Test signals (provided)
# ----------------------------
def x_exp(t):        # two-sided decaying exponential ; E = 1/a with a=1
    return np.exp(-np.abs(t))


def x_tail(t):       # the lecture signal: 1 on |t|<=1, then 1/|t| ; E = 4
    y = np.zeros_like(t, dtype=float)
    inside = np.abs(t) <= 1
    y[inside] = 1.0
    outside = ~inside
    y[outside] = 1.0 / np.abs(t[outside])
    return y


def x_slow(t):       # 1/sqrt(1+|t|) : tail ~ 1/|t| under the square -> diverges
    return 1.0 / np.sqrt(1.0 + np.abs(t))


def x_cos(t):        # cos(t): power signal, energy diverges linearly
    return np.cos(t)


def main():
    Ts = 2.0 ** np.arange(1, 13)   # 2, 4, 8, ..., 4096  (geometric)
    signals = {
        "e^{-|t|}  (E=1)":       x_exp,
        "lecture 1/|t| (E=4)":   x_tail,
        "1/sqrt(1+|t|)":         x_slow,
        "cos(t)":                x_cos,
    }

    fig, ax = plt.subplots(figsize=(9, 4.2))
    for name, f in signals.items():
        E = energy_curve(f, Ts)
        kind = classify_convergence(Ts, E)
        lim = estimated_limit(Ts, E) if kind == "finite" else np.inf
        print(f"{name:22s} -> {kind:8s}  E(inf) ~ {lim:.4g}")
        ax.plot(Ts, E, marker="o", label=f"{name} [{kind}]")
    ax.set_xscale("log")
    ax.set_xlabel("window half-width T"); ax.set_ylabel("E over [-T, T]")
    ax.set_ylim(0, 12); ax.grid(alpha=.3); ax.legend(fontsize=8)
    ax.set_title("Energy accumulated vs window size")
    fig.tight_layout()
    plt.show()

    # ---- verification ----
    assert classify_convergence(Ts, energy_curve(x_exp, Ts)) == "finite"
    assert abs(estimated_limit(Ts, energy_curve(x_exp, Ts)) - 1.0) < 1e-2
    assert classify_convergence(Ts, energy_curve(x_tail, Ts)) == "finite"
    assert abs(estimated_limit(Ts, energy_curve(x_tail, Ts)) - 4.0) < 1e-2
    assert classify_convergence(Ts, energy_curve(x_slow, Ts)) == "infinite"
    assert classify_convergence(Ts, energy_curve(x_cos, Ts)) == "infinite"
    print("All assertions passed.")


if __name__ == "__main__":
    main()
