import numpy as np
import matplotlib.pyplot as plt

T_MIN, T_MAX, N = -4.0, 9.0, 13001


def prototype(t):
    """Asymmetric continuous pulse: rise slope +1 on [0,1], fall slope -1/3 on
    [1,4], zero else. Peak 1 at t=1 (given)."""
    p = np.zeros_like(t, dtype=float)
    m1 = (t >= 0) & (t <= 1); p[m1] = t[m1]
    m2 = (t > 1) & (t <= 4);  p[m2] = (4 - t[m2]) / 3
    return p


def target_analytic(t):
    """Target = p(t) on [0,4]  +  1.5*p(8-t) on [4,8]  (given, for checking)."""
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
    """Linear interpolation of sampled x at query times tq, 0 outside."""
    raise NotImplementedError


def amp_scale(x, c):
    """Amplitude scaling c*x."""
    raise NotImplementedError


def shift(t, x, t0):
    """Time shift x(t - t0) (delay for t0>0), on grid t."""
    raise NotImplementedError


def reverse(t, x):
    """Time reversal x(-t), on grid t."""
    raise NotImplementedError


def build_target(t, p):
    """Reconstruct target using ONLY amp_scale, shift, reverse on p.
    Copy A = p(t);  Copy B = 1.5 * p(8 - t) = reverse first, then delay by 8."""
    raise NotImplementedError


def main():
    t = np.linspace(T_MIN, T_MAX, N); p = prototype(t)
    s_built = build_target(t, p); s_true = target_analytic(t)
    print(f"MSE(built, analytic) = {np.mean((s_built-s_true)**2):.3e}")

    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.plot(t, p, color="0.6", lw=1, label="prototype p(t)")
    ax.plot(t, s_true, "k--", lw=2, label="target (analytic)")
    ax.plot(t, s_built, lw=1.6, label="built from p(t)")
    ax.set_xlim(-1, 9); ax.grid(alpha=.3); ax.legend(fontsize=8); ax.set_xlabel("t")
    fig.tight_layout(); plt.show()


if __name__ == "__main__":
    main()
