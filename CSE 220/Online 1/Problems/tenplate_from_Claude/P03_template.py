import numpy as np #type:ignore
import matplotlib.pyplot as plt
from fractions import Fraction
from math import gcd

# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def sinusoid_period(Omega: float, max_den: int = 1000):
    """cos(Omega*n) is periodic iff Omega/(2*pi) is rational = k/N. Return
    (is_periodic, N_fundamental) or (False, None). Hint: fractions.Fraction
    with .limit_denominator, then divide N by gcd(k, N)."""
    raise NotImplementedError


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def combined_period(omegas):
    """Fundamental period of a sum of sinusoids = LCM of individual periods.
    Return (is_periodic, N)."""
    raise NotImplementedError


def verify_period(x_func, N: int, n_test=None) -> float:
    """Return max |x[n+N]-x[n]| over a test range (small => period N)."""
    raise NotImplementedError


def stem(ax, n, x, label):
    ml, sl, bl = ax.stem(n, x, label=label); bl.set_visible(False)
    ax.grid(alpha=.3); ax.set_xlabel("n"); ax.set_ylabel("amp")


def main():
    print("=== Single sinusoids ===")
    for w in [np.pi/4, 3*np.pi/5, np.pi/3, 1.0, 2*np.pi/7]:
        ok, N = sinusoid_period(w)
        if ok:
            r = verify_period(lambda n: np.cos(w*n), N)
            print(f"Omega={w:.5f} -> periodic, N={N:3d} (residual={r:.1e})")
        else:
            print(f"Omega={w:.5f} -> NOT periodic")

    print("\n=== Sum of sinusoids ===")
    omegas = [np.pi/3, np.pi/4]
    ok, N = combined_period(omegas)
    def xsum(n): return np.cos(np.pi*n/3) + 0.5*np.sin(np.pi*n/4)
    print(f"omegas={omegas} -> periodic={ok}, N={N}")

    if ok:
        n = np.arange(0, 2*N)
        fig, ax = plt.subplots(figsize=(9, 3.2))
        stem(ax, n, xsum(n), "x[n]")
        ax.set_title(f"Fundamental period N={N}"); ax.legend(fontsize=8)
        fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
