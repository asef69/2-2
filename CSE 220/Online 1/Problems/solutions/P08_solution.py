"""
Problem 8 - "Averaging over one period is enough."
For a periodic signal, verify that the average power computed over a single
fundamental period equals the average power over K periods, and compare with
the exact analytic values.
Reference solution.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def power_over_interval(xfunc, t0: float, t1: float, n: int = 200001) -> float:
    """Average power of x over [t0, t1]:
        (1/(t1-t0)) * integral_{t0}^{t1} |x(t)|^2 dt   (trapezoidal)."""
    t = np.linspace(t0, t1, n)
    x = xfunc(t)
    energy = np.trapezoid(np.abs(x) ** 2, t)
    return float(energy / (t1 - t0))


def power_one_period(xfunc, T: float) -> float:
    """Average power over exactly one fundamental period [0, T]."""
    return power_over_interval(xfunc, 0.0, T)


def power_k_periods(xfunc, T: float, K: int) -> float:
    """Average power over K fundamental periods [0, K*T]."""
    return power_over_interval(xfunc, 0.0, K * T)


# ----------------------------
# Periodic test signals (provided)
# ----------------------------
def rectified_sine(t):        # |sin t|, period pi, exact power 1/2
    return np.abs(np.sin(t))


def square_wave(t):           # +/-1, period 2, exact power 1
    return np.sign(np.sin(np.pi * t)) + (np.sin(np.pi * t) == 0)


def half_sine_train(t):       # lecture signal: sin on [0,pi], rest on [pi,2pi]
    tt = np.mod(t, 2 * np.pi)
    return np.where(tt <= np.pi, np.sin(tt), 0.0)


def cos_squared(t):           # cos^2 t, period pi, exact power <cos^4> = 3/8
    return np.cos(t) ** 2


def main():
    signals = [
        ("|sin t|",         rectified_sine,  np.pi,     0.5),
        ("square wave",     square_wave,     2.0,       1.0),
        ("half-sine train", half_sine_train, 2 * np.pi, 0.25),
        ("cos^2 t",         cos_squared,     np.pi,     3 / 8),
    ]

    print(f"{'signal':18s}{'P(1 period)':>13s}{'P(8 periods)':>14s}{'exact':>9s}")
    for name, f, T, exact in signals:
        p1 = power_one_period(f, T)
        pK = power_k_periods(f, T, 8)
        print(f"{name:18s}{p1:13.6f}{pK:14.6f}{exact:9.4f}")

    # Plot the half-sine train and highlight one period
    t = np.linspace(0, 4 * np.pi, 2000)
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.plot(t, half_sine_train(t), lw=1.8)
    ax.axvspan(0, 2 * np.pi, color="orange", alpha=.15, label="one period")
    ax.set_title("Half-sine train: power over one period = power over many")
    ax.set_xlabel("t"); ax.grid(alpha=.3); ax.legend(fontsize=8)
    fig.tight_layout()
    plt.show()

    # ---- verification ----
    for name, f, T, exact in signals:
        p1 = power_one_period(f, T)
        pK = power_k_periods(f, T, 8)
        assert abs(p1 - pK) < 1e-3, (name, p1, pK)
        assert abs(p1 - exact) < 2e-3, (name, p1, exact)
    print("\nAll assertions passed.")


if __name__ == "__main__":
    main()
