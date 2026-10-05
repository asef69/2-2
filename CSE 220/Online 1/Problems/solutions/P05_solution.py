"""
Problem 5 - Multipath / echo model.
Build y(t) = sum_{k=0}^{K} alpha^k * x(t - k*d) from a prototype pulse x(t)
using time-shift (delay), then study its energy as K grows.
Reference solution.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

T_MIN, T_MAX, N = -2.0, 14.0, 8001


def x_of_t(t: np.ndarray) -> np.ndarray:
    """Prototype 'ping': a Gaussian-modulated cosine pulse centred at t=0."""
    return np.exp(-((t) ** 2) / (2 * 0.25 ** 2)) * np.cos(2 * np.pi * 3.0 * t)


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def delay(t: np.ndarray, x: np.ndarray, d: float) -> np.ndarray:
    """Return x(t - d) sampled on grid t (a delay to the right for d>0),
    using linear interpolation, 0 outside the original support."""
    return np.interp(t - d, t, x, left=0.0, right=0.0)


def build_echo(t: np.ndarray, x: np.ndarray,
               alpha: float, d: float, K: int) -> np.ndarray:
    """y(t) = sum_{k=0}^{K} alpha^k * x(t - k*d)."""
    y = np.zeros_like(t, dtype=float)
    for k in range(K + 1):
        y = y + (alpha ** k) * delay(t, x, k * d)
    return y


def energy_ct(t: np.ndarray, x: np.ndarray) -> float:
    """Integral of |x|^2 dt (trapezoidal)."""
    return float(np.trapezoid(np.abs(x) ** 2, t))


# ----------------------------
# Provided plotting
# ----------------------------
def plot_signals(t, x, y, K, alpha, d, ax):
    ax.plot(t, x, color="0.6", lw=1, label="prototype x(t)")
    ax.plot(t, y, lw=1.6, label=f"echoed y(t), K={K}")
    ax.set_title(fr"$\alpha={alpha},\ d={d}$")
    ax.grid(alpha=.3); ax.legend(fontsize=8); ax.set_xlabel("t")


def main():
    t = np.linspace(T_MIN, T_MAX, N)
    x = x_of_t(t)

    alpha, d = 0.6, 1.5
    Ks = list(range(0, 8))
    energies = []
    for K in Ks:
        y = build_echo(t, x, alpha, d, K)
        energies.append(energy_ct(t, y))

    for K, E in zip(Ks, energies):
        print(f"K={K}:  E(y) = {E:.5f}")

    # As d is large enough that echoes barely overlap, the total energy tends
    # to E0 * (1 + alpha^2 + alpha^4 + ...) = E0 / (1 - alpha^2).
    E0 = energy_ct(t, x)
    predicted = E0 / (1 - alpha ** 2)
    print(f"\nsingle-pulse energy E0 = {E0:.5f}")
    print(f"geometric prediction E0/(1-alpha^2) = {predicted:.5f}")
    print(f"measured at K={Ks[-1]}         = {energies[-1]:.5f}")

    fig, axes = plt.subplots(2, 1, figsize=(9, 6))
    plot_signals(t, x, build_echo(t, x, alpha, d, 5), 5, alpha, d, axes[0])
    axes[1].plot(Ks, energies, "o-", label="measured E(y)")
    axes[1].axhline(predicted, color="r", ls="--", label="E0/(1-alpha^2)")
    axes[1].set_xlabel("number of echoes K"); axes[1].set_ylabel("energy")
    axes[1].grid(alpha=.3); axes[1].legend(fontsize=8)
    fig.tight_layout()
    plt.show()

    # ---- verification ----
    assert abs(energies[-1] - predicted) < 0.02 * predicted
    # energy is monotonically increasing in K
    assert all(energies[i] <= energies[i + 1] + 1e-9 for i in range(len(energies) - 1))
    print("\nAll assertions passed.")


if __name__ == "__main__":
    main()
