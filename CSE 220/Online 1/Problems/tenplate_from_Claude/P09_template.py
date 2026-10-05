import numpy as np
import matplotlib.pyplot as plt

T_MIN, T_MAX = -1.0, 8.0


def x_of_t(t):
    """One-sided decaying cosine e^{-0.7t}cos(5t) u(t) (given)."""
    return np.where(t >= 0, np.exp(-0.7 * t) * np.cos(5.0 * t), 0.0)


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def ct_energy_reference(xfunc, t0, t1, n=2_000_001):
    """High-resolution reference for integral |x|^2 dt (trapezoidal)."""
    raise NotImplementedError


def dt_energy_estimate(xfunc, t0, t1, dt):
    """Sample x at spacing dt on [t0,t1]; return dt * sum |x[n]|^2."""
    raise NotImplementedError


def convergence_study(xfunc, t0, t1, dts):
    """Return (reference, estimates_array, abs_errors_array)."""
    raise NotImplementedError


def main():
    dts = np.array([0.5, 0.25, 0.1, 0.05, 0.025, 0.01, 0.005])
    ref, est, err = convergence_study(x_of_t, T_MIN, T_MAX, dts)
    print(f"Reference energy = {ref:.8f}\n")
    print(f"{'dt':>8}{'estimate':>14}{'abs error':>14}")
    for d, e, er in zip(dts, est, err):
        print(f"{d:8.3f}{e:14.8f}{er:14.2e}")

    mask = dts <= 0.1
    slope = np.polyfit(np.log(dts[mask]), np.log(err[mask] + 1e-18), 1)[0]
    print(f"\nEmpirical convergence order (slope) ~ {slope:.2f}")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.loglog(dts, err, "o-"); ax.grid(alpha=.3, which="both")
    ax.set_xlabel("dt"); ax.set_ylabel("|estimate - reference|")
    fig.tight_layout(); plt.show()


if __name__ == "__main__":
    main()
