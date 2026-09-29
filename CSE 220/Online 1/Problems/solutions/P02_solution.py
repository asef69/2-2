"""
Problem 2 - General affine time transform  y(t) = x(alpha*t + beta)
via the lecture's shift -> reverse -> scale recipe.
Reference solution.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

T_MIN, T_MAX, N = -6.0, 6.0, 4801


def x_of_t(t: np.ndarray) -> np.ndarray:
    """Base signal: the piecewise 'triangle-with-a-flat-top' used in lecture,
    slightly enriched so that reversal and shifting are visible."""
    y = np.zeros_like(t, dtype=float)
    m1 = (t >= 0) & (t < 1)          # rising ramp
    y[m1] = t[m1]
    m2 = (t >= 1) & (t <= 2)         # flat top then fall
    y[m2] = 2 - t[m2]
    return y


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def interp_sample(t: np.ndarray, x: np.ndarray, t_query: np.ndarray) -> np.ndarray:
    """Evaluate the sampled signal x (defined on grid t) at arbitrary query
    times using linear interpolation. Return 0 outside the original range."""
    return np.interp(t_query, t, x, left=0.0, right=0.0)


def apply_shift(t: np.ndarray, x: np.ndarray, beta: float) -> np.ndarray:
    """Return samples of x(t + beta) on the SAME grid t.
    beta > 0 shifts the graph LEFT (advance)."""
    return interp_sample(t, x, t + beta)


def apply_reverse(t: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Return samples of x(-t) on the same grid t."""
    return interp_sample(t, x, -t)


def apply_scale(t: np.ndarray, x: np.ndarray, a: float) -> np.ndarray:
    """Return samples of x(a*t) on the same grid t. Require a > 0
    (reversal handles the sign separately)."""
    assert a > 0
    return interp_sample(t, x, a * t)


def affine_transform(t: np.ndarray, x: np.ndarray,
                     alpha: float, beta: float) -> np.ndarray:
    """Produce y(t) = x(alpha*t + beta) using the 3-step recipe:
        Step 1  g1(t) = x(t + beta)                (shift)
        Step 2  g2(t) = g1(-t)  only if alpha < 0  (reversal)
        Step 3  g3(t) = g2(|alpha| t)              (scale)
    """
    g1 = apply_shift(t, x, beta)
    g2 = apply_reverse(t, g1) if alpha < 0 else g1
    g3 = apply_scale(t, g2, abs(alpha))
    return g3


def direct_transform(t: np.ndarray, x: np.ndarray,
                     alpha: float, beta: float) -> np.ndarray:
    """Ground truth: evaluate x directly at alpha*t + beta."""
    return interp_sample(t, x, alpha * t + beta)


# ----------------------------
# Provided plotting
# ----------------------------
def plot_case(t, x, y_recipe, y_direct, alpha, beta, ax):
    ax.plot(t, x, "k--", lw=1, label="x(t)")
    ax.plot(t, y_recipe, lw=2, label="recipe")
    ax.plot(t, y_direct, ":", lw=2, label="direct")
    ax.set_title(fr"$y(t)=x({alpha:g}t{beta:+g})$")
    ax.grid(alpha=.3); ax.legend(fontsize=7)


def main():
    t = np.linspace(T_MIN, T_MAX, N)
    x = x_of_t(t)

    cases = [(-3.0, 2.0), (2.0, 3.0), (0.5, -1.0), (-1.0, 0.0)]
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    for (alpha, beta), ax in zip(cases, axes.ravel()):
        yr = affine_transform(t, x, alpha, beta)
        yd = direct_transform(t, x, alpha, beta)
        mse = float(np.mean((yr - yd) ** 2))
        print(f"alpha={alpha:+g}, beta={beta:+g} -> MSE(recipe,direct)={mse:.2e}")
        plot_case(t, x, yr, yd, alpha, beta, ax)
    fig.tight_layout()
    plt.show()

    # ---- verification: recipe must match direct evaluation ----
    for alpha, beta in cases:
        yr = affine_transform(t, x, alpha, beta)
        yd = direct_transform(t, x, alpha, beta)
        assert float(np.mean((yr - yd) ** 2)) < 1e-4, (alpha, beta)
    print("All assertions passed.")


if __name__ == "__main__":
    main()
