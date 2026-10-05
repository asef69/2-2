"""
Problem 9 - Bridging discrete and continuous energy.
The continuous energy  integral |x(t)|^2 dt  is the limit of the discrete
Riemann sum  dt * sum |x[n]|^2 .  Sample x(t) at spacing dt and watch the
discrete energy estimate converge to the continuous value as dt -> 0.
Reference solution.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

T_MIN, T_MAX = -1.0, 8.0


def x_of_t(t: np.ndarray) -> np.ndarray:
    """Energy signal: a one-sided decaying cosine  e^{-0.7t}cos(5t) u(t).
    The jump at t=0 keeps the Riemann convergence at a clean polynomial rate
    (a fully smooth pulse would converge deceptively fast)."""
    return np.where(t >= 0, np.exp(-0.7 * t) * np.cos(5.0 * t), 0.0)


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def ct_energy_reference(xfunc, t0: float, t1: float, n: int = 2_000_001) -> float:
    """High-resolution reference for integral |x(t)|^2 dt (trapezoidal)."""
    t = np.linspace(t0, t1, n)
    return float(np.trapezoid(np.abs(xfunc(t)) ** 2, t))


def dt_energy_estimate(xfunc, t0: float, t1: float, dt: float) -> float:
    """Sample x at spacing dt on [t0, t1] and return the Riemann estimate
    dt * sum |x[n]|^2  of the continuous energy."""
    n = np.arange(t0, t1 + dt / 2, dt)
    x = xfunc(n)
    return float(dt * np.sum(np.abs(x) ** 2))


def convergence_study(xfunc, t0, t1, dts):
    """Return (estimates, abs_errors) versus the fine reference."""
    ref = ct_energy_reference(xfunc, t0, t1)
    est = np.array([dt_energy_estimate(xfunc, t0, t1, dt) for dt in dts])
    err = np.abs(est - ref)
    return ref, est, err


# ----------------------------
# Provided plotting
# ----------------------------
def main():
    dts = np.array([0.5, 0.25, 0.1, 0.05, 0.025, 0.01, 0.005])
    ref, est, err = convergence_study(x_of_t, T_MIN, T_MAX, dts)

    print(f"Continuous reference energy = {ref:.8f}\n")
    print(f"{'dt':>8}{'estimate':>14}{'abs error':>14}")
    for d, e, er in zip(dts, est, err):
        print(f"{d:8.3f}{e:14.8f}{er:14.2e}")

    # Empirical convergence order from the last few points (slope on log-log).
    mask = dts <= 0.1
    slope = np.polyfit(np.log(dts[mask]), np.log(err[mask] + 1e-18), 1)[0]
    print(f"\nEmpirical convergence order (slope) ~ {slope:.2f}")

    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    tt = np.linspace(T_MIN, T_MAX, 1500)
    ax[0].plot(tt, x_of_t(tt), lw=1.2)
    ns = np.arange(T_MIN, T_MAX + 0.1, 0.2)
    ax[0].plot(ns, x_of_t(ns), "o", ms=4, label="dt=0.2 samples")
    ax[0].set_title("x(t) and its samples"); ax[0].grid(alpha=.3)
    ax[0].legend(fontsize=8); ax[0].set_xlabel("t")
    ax[1].loglog(dts, err, "o-")
    ax[1].set_xlabel("sampling step dt"); ax[1].set_ylabel("|estimate - reference|")
    ax[1].set_title(f"Error vs dt (order ~ {slope:.1f})"); ax[1].grid(alpha=.3, which="both")
    fig.tight_layout()
    plt.show()

    # ---- verification ----
    assert err[-1] < err[0]                     # finer sampling -> smaller error
    assert abs(est[-1] - ref) < 4e-3            # converges to the CT value
    assert 0.7 < slope < 2.5                    # clean polynomial convergence
    print("\nAll assertions passed.")


if __name__ == "__main__":
    main()
