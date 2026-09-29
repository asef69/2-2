"""
Problem 3 - Discrete-time periodicity: is x[n] periodic, and if so what is
its fundamental period N?
Reference solution.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from fractions import Fraction
from math import gcd


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def sinusoid_period(Omega: float, max_den: int = 1000):
    """A discrete sinusoid cos(Omega*n + phi) is periodic iff Omega/(2*pi)
    is rational, i.e. Omega = 2*pi*(k/N). Then the (not necessarily
    fundamental) period is N, and the FUNDAMENTAL period is N/gcd(k,N).

    Returns (is_periodic, N) with N an int, or (False, None).
    """
    ratio = Omega / (2 * np.pi)
    frac = Fraction(ratio).limit_denominator(max_den)
    # Check the rational approximation is actually faithful.
    if abs(float(frac) - ratio) > 1e-9:
        return False, None
    k, N = frac.numerator, frac.denominator
    if N == 0:
        return False, None
    N_fund = N // gcd(abs(k), N) if k != 0 else 1
    return True, N_fund


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def combined_period(omegas):
    """Fundamental period of a sum of sinusoids = LCM of the individual
    fundamental periods. Returns (is_periodic, N)."""
    periods = []
    for w in omegas:
        ok, N = sinusoid_period(w)
        if not ok:
            return False, None
        periods.append(N)
    N = 1
    for p in periods:
        N = lcm(N, p)
    return True, N


def verify_period(x_func, N: int, n_test=None) -> float:
    """Numerically verify periodicity: max |x[n+N] - x[n]| over a test range.
    A small value confirms period N."""
    if n_test is None:
        n_test = np.arange(-50, 51)
    return float(np.max(np.abs(x_func(n_test + N) - x_func(n_test))))


# ----------------------------
# Provided helpers
# ----------------------------
def stem(ax, n, x, label):
    ml, sl, bl = ax.stem(n, x, label=label)
    bl.set_visible(False)
    ax.grid(alpha=.3); ax.set_xlabel("n"); ax.set_ylabel("amp")


def main():
    print("=== Single sinusoids ===")
    tests = [np.pi / 4, 3 * np.pi / 5, np.pi / 3, 1.0, 2 * np.pi / 7]
    for w in tests:
        ok, N = sinusoid_period(w)
        if ok:
            resid = verify_period(lambda n: np.cos(w * n), N)
            print(f"Omega={w:.5f} -> periodic, N={N:3d}  (residual={resid:.1e})")
        else:
            print(f"Omega={w:.5f} -> NOT periodic")

    print("\n=== Sum of sinusoids ===")
    # x[n] = cos(pi n/3) + 0.5 sin(pi n/4)  -> N = lcm(6, 8) = 24
    omegas = [np.pi / 3, np.pi / 4]
    ok, N = combined_period(omegas)

    def xsum(n):
        return np.cos(np.pi * n / 3) + 0.5 * np.sin(np.pi * n / 4)

    resid = verify_period(xsum, N) if ok else None
    print(f"omegas={omegas} -> periodic={ok}, N={N}, residual={resid:.1e}")

    # A non-periodic sum: mixing a rational and an irrational frequency
    ok2, N2 = combined_period([np.pi / 3, 1.0])
    print(f"omegas=[pi/3, 1.0] -> periodic={ok2}, N={N2}")

    # Plot the periodic sum over ~2 periods
    n = np.arange(0, 2 * N)
    fig, ax = plt.subplots(figsize=(9, 3.2))
    stem(ax, n, xsum(n), "x[n]=cos(pi n/3)+0.5 sin(pi n/4)")
    for m in range(0, 2 * N + 1, N):
        ax.axvline(m - 0.5, color="r", ls="--", alpha=.4)
    ax.set_title(f"Fundamental period N = {N}")
    ax.legend(fontsize=8)
    fig.tight_layout()
    plt.show()

    # ---- verification ----
    assert sinusoid_period(np.pi / 4) == (True, 8)
    assert sinusoid_period(3 * np.pi / 5) == (True, 10)
    assert sinusoid_period(np.pi / 3) == (True, 6)
    assert sinusoid_period(1.0)[0] is False
    assert combined_period([np.pi / 3, np.pi / 4]) == (True, 24)
    print("\nAll assertions passed.")


if __name__ == "__main__":
    main()
