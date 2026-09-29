import numpy as np
import matplotlib.pyplot as plt

T_MIN, T_MAX, N = -6.0, 6.0, 4801


def x_of_t(t: np.ndarray) -> np.ndarray:
    """Base signal (given)."""
    y = np.zeros_like(t, dtype=float)
    m1 = (t >= 0) & (t < 1)
    y[m1] = t[m1]
    m2 = (t >= 1) & (t <= 2)
    y[m2] = 2 - t[m2]
    return y


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def interp_sample(t, x, t_query):
    """Evaluate sampled x on grid t at arbitrary t_query via linear
    interpolation; 0 outside the original range."""
    return np.interp(t_query,t,x,left=0.0,right=0.0)


def apply_shift(t, x, beta):
    """Return samples of x(t + beta) on the SAME grid t (beta>0 shifts LEFT)."""
    return interp_sample(t,x,t+beta)


def apply_reverse(t, x):
    """Return samples of x(-t) on grid t."""
    return interp_sample(t,x,-t)


def apply_scale(t, x, a):
    """Return samples of x(a*t) on grid t, a>0."""
    return interp_sample(t,x,a*t)


def affine_transform(t, x, alpha, beta):
    """y(t)=x(alpha*t+beta) via recipe: shift by beta -> reverse if alpha<0
    -> scale by |alpha|."""
    g1 = apply_shift(t,x,beta)
    if alpha<0:
        g2 = apply_reverse(t,g1)
    else:
        g2 = g1
    g3 = apply_scale(t,g2,abs(alpha))
    return g3


def direct_transform(t, x, alpha, beta):
    """Ground truth: evaluate x directly at alpha*t + beta (given, uses your
    interp_sample)."""
    return interp_sample(t, x, alpha * t + beta)


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
        print(f"alpha={alpha:+g}, beta={beta:+g} -> MSE={np.mean((yr-yd)**2):.2e}")
        plot_case(t, x, yr, yd, alpha, beta, ax)
    fig.tight_layout(); plt.show()


if __name__ == "__main__":
    main()
