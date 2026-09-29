"""
Problem 6 - The time-scaling energy law.
If y(t) = x(a*t) then E_y = E_x / |a|.  Verify it numerically.
Reference solution.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

T_MIN, T_MAX, N = -12.0, 12.0, 24001


def x_of_t(t: np.ndarray) -> np.ndarray:
    """Base energy signal: a two-sided decaying exponential."""
    return np.exp(-np.abs(t))


def x_tri(t: np.ndarray) -> np.ndarray:
    """A second base signal: triangular pulse of half-width 2."""
    y = np.zeros_like(t, dtype=float)
    m = np.abs(t) <= 2
    y[m] = 1 - np.abs(t[m]) / 2
    return y


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def scale_signal(t: np.ndarray, x: np.ndarray, a: float) -> np.ndarray:
    """Return y(t) = x(a*t) sampled on grid t.  a>1 compresses, 0<a<1
    stretches, a<0 also reverses.  Uses linear interpolation."""
    return np.interp(a * t, t, x, left=0.0, right=0.0)


def energy_ct(t: np.ndarray, x: np.ndarray) -> float:
    return float(np.trapezoid(np.abs(x) ** 2, t))


def scaling_law_check(t: np.ndarray, x: np.ndarray, a: float):
    """Return (E_base, E_scaled, E_scaled_times_|a|).
    The third value should equal E_base for every a."""
    Eb = energy_ct(t, x)
    y = scale_signal(t, x, a)
    Es = energy_ct(t, y)
    return Eb, Es, Es * abs(a)


# ----------------------------
# Provided plotting
# ----------------------------
def main():
    t = np.linspace(T_MIN, T_MAX, N)

    for label, xfunc in [("e^{-|t|}", x_of_t), ("triangle", x_tri)]:
        x = xfunc(t)
        print(f"\n=== base signal: {label} ===")
        Eb = energy_ct(t, x)
        print(f"E_base = {Eb:.5f}")
        print(f"{'a':>6} {'E_scaled':>12} {'|a|*E_scaled':>14}")
        for a in [0.5, 1.0, 2.0, 3.0, 4.0, -2.0, -0.5]:
            _, Es, Es_a = scaling_law_check(t, x, a)
            print(f"{a:6.2f} {Es:12.5f} {Es_a:14.5f}")

    # Plot the exponential under a few scalings
    x = x_of_t(t)
    fig, ax = plt.subplots(figsize=(9, 4))
    for a in [0.5, 1.0, 2.0, 4.0]:
        ax.plot(t, scale_signal(t, x, a), label=f"x({a}t)")
    ax.set_xlim(-6, 6); ax.grid(alpha=.3); ax.legend(fontsize=8)
    ax.set_title(r"Compressing $x(t)=e^{-|t|}$ shrinks its energy by $1/|a|$")
    ax.set_xlabel("t")
    fig.tight_layout()
    plt.show()

    # ---- verification ----
    x = x_of_t(t)
    Eb = energy_ct(t, x)
    for a in [0.5, 2.0, 3.0, 4.0, -2.0]:
        _, _, Es_a = scaling_law_check(t, x, a)
        assert abs(Es_a - Eb) < 1e-2 * Eb, (a, Es_a, Eb)
    print("\nAll assertions passed.")


if __name__ == "__main__":
    main()
