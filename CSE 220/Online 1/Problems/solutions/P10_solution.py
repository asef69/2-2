"""
Problem 10 - Building a signal out of one prototype pulse.
Using only amplitude scaling, time shift, and time reversal of a single
ASYMMETRIC prototype pulse p(t), reconstruct a specified target waveform and
verify it against the analytic target.
Reference solution.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

T_MIN, T_MAX, N = -4.0, 9.0, 13001


def prototype(t: np.ndarray) -> np.ndarray:
    """Asymmetric continuous pulse: fast rise (slope +1 over [0,1]) then slow
    fall (slope -1/3 over [1,4]); zero elsewhere. Peak height 1 at t=1.
    Because it is NOT symmetric, time reversal produces a genuinely different
    shape (slow rise, fast fall) that no pure shift can reproduce."""
    p = np.zeros_like(t, dtype=float)
    m1 = (t >= 0) & (t <= 1); p[m1] = t[m1]
    m2 = (t > 1) & (t <= 4);  p[m2] = (4 - t[m2]) / 3
    return p


def target_analytic(t: np.ndarray) -> np.ndarray:
    """Target to reproduce:
         Copy A =        p(t)              on [0, 4]
         Copy B = 1.5 *  p(8 - t)          on [4, 8]   (a reversed, shifted,
                                                        amplified copy)
    Fully continuous piecewise-linear waveform."""
    s = np.zeros_like(t, dtype=float)
    a1 = (t >= 0) & (t <= 1); s[a1] += t[a1]
    a2 = (t > 1) & (t <= 4);  s[a2] += (4 - t[a2]) / 3
    b1 = (t >= 4) & (t <= 7); s[b1] += 1.5 * (t[b1] - 4) / 3
    b2 = (t > 7) & (t <= 8);  s[b2] += 1.5 * (8 - t[b2])
    return s


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def interp_sample(t, x, tq):
    return np.interp(tq, t, x, left=0.0, right=0.0)


def amp_scale(x: np.ndarray, c: float) -> np.ndarray:
    """Amplitude scaling: c * x."""
    return c * x


def shift(t: np.ndarray, x: np.ndarray, t0: float) -> np.ndarray:
    """Time shift (delay for t0>0): x(t - t0)."""
    return interp_sample(t, x, t - t0)


def reverse(t: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Time reversal: x(-t)."""
    return interp_sample(t, x, -t)


def build_target(t: np.ndarray, p: np.ndarray) -> np.ndarray:
    """Reconstruct s(t) from the prototype p(t) using only amp_scale, shift,
    and reverse.

        Copy A : p(t)                       -> p itself
        Copy B : 1.5 * p(8 - t)
                 p(8 - t) = p(-(t - 8)) = reverse first, THEN delay by 8.
    """
    A = p
    rev = reverse(t, p)                        # p(-t)
    B = amp_scale(shift(t, rev, 8.0), 1.5)     # 1.5 * p(-(t - 8)) = 1.5 p(8 - t)
    return A + B


# ----------------------------
# Provided plotting
# ----------------------------
def main():
    t = np.linspace(T_MIN, T_MAX, N)
    p = prototype(t)

    s_built = build_target(t, p)
    s_true = target_analytic(t)
    mse = float(np.mean((s_built - s_true) ** 2))
    print(f"MSE(built, analytic) = {mse:.3e}")

    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.plot(t, p, color="0.6", lw=1, label="prototype p(t)")
    ax.plot(t, s_true, "k--", lw=2, label="target (analytic)")
    ax.plot(t, s_built, lw=1.6, label="built from p(t)")
    ax.set_xlim(-1, 9); ax.grid(alpha=.3); ax.legend(fontsize=8); ax.set_xlabel("t")
    ax.set_title("Reconstructing a waveform from one asymmetric prototype")
    fig.tight_layout()
    plt.show()

    # ---- verification ----
    assert mse < 1e-4, mse
    print("All assertions passed.")


if __name__ == "__main__":
    main()
