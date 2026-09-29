import numpy as np
import matplotlib.pyplot as plt

T_MIN, T_MAX, N = -2.0, 14.0, 8001


def x_of_t(t: np.ndarray) -> np.ndarray:
    """Prototype 'ping': Gaussian-modulated cosine pulse (given)."""
    return np.exp(-(t**2) / (2 * 0.25**2)) * np.cos(2 * np.pi * 3.0 * t)


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def delay(t, x, d):
    """Return x(t - d) on grid t via linear interpolation (0 outside)."""
    raise NotImplementedError


def build_echo(t, x, alpha, d, K):
    """y(t) = sum_{k=0}^{K} alpha^k * x(t - k*d)."""
    raise NotImplementedError


def energy_ct(t, x):
    """Integral of |x|^2 dt (trapezoidal)."""
    raise NotImplementedError


def plot_signals(t, x, y, K, alpha, d, ax):
    ax.plot(t, x, color="0.6", lw=1, label="prototype x(t)")
    ax.plot(t, y, lw=1.6, label=f"echoed y(t), K={K}")
    ax.set_title(fr"$\alpha={alpha},\ d={d}$"); ax.grid(alpha=.3)
    ax.legend(fontsize=8); ax.set_xlabel("t")


def main():
    t = np.linspace(T_MIN, T_MAX, N); x = x_of_t(t)
    alpha, d = 0.6, 1.5
    Ks = list(range(0, 8)); energies = []
    for K in Ks:
        energies.append(energy_ct(t, build_echo(t, x, alpha, d, K)))
        print(f"K={K}:  E(y) = {energies[-1]:.5f}")

    E0 = energy_ct(t, x); predicted = E0 / (1 - alpha**2)
    print(f"\nE0/(1-alpha^2) = {predicted:.5f}   measured = {energies[-1]:.5f}")

    fig, axes = plt.subplots(2, 1, figsize=(9, 6))
    plot_signals(t, x, build_echo(t, x, alpha, d, 5), 5, alpha, d, axes[0])
    axes[1].plot(Ks, energies, "o-", label="measured E(y)")
    axes[1].axhline(predicted, color="r", ls="--", label="E0/(1-alpha^2)")
    axes[1].set_xlabel("K"); axes[1].set_ylabel("energy")
    axes[1].grid(alpha=.3); axes[1].legend(fontsize=8)
    fig.tight_layout(); plt.show()


if __name__ == "__main__":
    main()
