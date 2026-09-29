import numpy as np
import matplotlib.pyplot as plt

T_MIN, T_MAX, N = -12.0, 12.0, 24001


def x_of_t(t): return np.exp(-np.abs(t))            # base signal (given)
def x_tri(t):                                        # second base signal (given)
    y = np.zeros_like(t, dtype=float)
    m = np.abs(t) <= 2
    y[m] = 1 - np.abs(t[m]) / 2
    return y


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def scale_signal(t, x, a):
    """Return y(t)=x(a*t) on grid t (a>1 compresses, 0<a<1 stretches, a<0
    also reverses). Use linear interpolation."""
    return np.interp(a*t,t,x,left=0.0,right=0.0)


def energy_ct(t, x):
    """Integral of |x|^2 dt (trapezoidal)."""
    return float(np.trapezoid(np.abs(x)**2,t))


def scaling_law_check(t, x, a):
    """Return (E_base, E_scaled, E_scaled*|a|). The third value should equal
    E_base for every a -- that is the law you must confirm."""
    E_base = energy_ct(t,x)
    E_scaled = energy_ct(t,scale_signal(t,x,a))
    return E_base, E_scaled, E_scaled*abs(a)


def main():
    t = np.linspace(T_MIN, T_MAX, N)
    for label, xfunc in [("e^{-|t|}", x_of_t), ("triangle", x_tri)]:
        x = xfunc(t)
        print(f"\n=== base: {label} ===  E_base={energy_ct(t, x):.5f}")
        print(f"{'a':>6}{'E_scaled':>12}{'|a|*E_scaled':>14}")
        for a in [0.5, 1.0, 2.0, 3.0, 4.0, -2.0, -0.5]:
            _, Es, Es_a = scaling_law_check(t, x, a)
            print(f"{a:6.2f}{Es:12.5f}{Es_a:14.5f}")

    x = x_of_t(t)
    fig, ax = plt.subplots(figsize=(9, 4))
    for a in [0.5, 1.0, 2.0, 4.0]:
        ax.plot(t, scale_signal(t, x, a), label=f"x({a}t)")
    ax.set_xlim(-6, 6); ax.grid(alpha=.3); ax.legend(fontsize=8)
    ax.set_xlabel("t"); fig.tight_layout(); plt.show()


if __name__ == "__main__":
    main()
