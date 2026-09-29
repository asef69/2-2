"""
Problem 7 - Energy is shared between the even and odd parts.
Show numerically that  E_x = E_xe + E_xo  and that the cross-energy
integral(xe * xo) = 0  (the even and odd parts are orthogonal), for both a
continuous-time and a discrete-time signal.
Reference solution.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

T_MIN, T_MAX, N = -8.0, 8.0, 16001   # symmetric grid, 0 is a sample


def x_ct(t: np.ndarray) -> np.ndarray:
    """One-sided decaying exponential x(t)=e^{-t} for t>=0, else 0.
    This is neither even nor odd, so both parts are nontrivial."""
    return np.where(t >= 0, np.exp(-t), 0.0)


def x_dt(n: np.ndarray) -> np.ndarray:
    """One-sided geometric x[n] = (0.7)^n for n>=0, else 0."""
    return np.where(n >= 0, 0.7 ** np.abs(n), 0.0)


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def even_odd_ct(t: np.ndarray, x: np.ndarray):
    """Even and odd parts of a CT signal sampled on a grid symmetric about 0.
    xe(t)=(x(t)+x(-t))/2 ,  xo(t)=(x(t)-x(-t))/2 . x(-t) obtained by flipping
    the sample array (valid on a symmetric grid)."""
    xr = x[::-1]                      # samples of x(-t)
    xe = 0.5 * (x + xr)
    xo = 0.5 * (x - xr)
    return xe, xo


def even_odd_dt(n: np.ndarray, x: np.ndarray):
    """Even and odd parts of a DT signal on a symmetric index range."""
    xr = x[::-1]                      # x[-n]
    xe = 0.5 * (x + xr)
    xo = 0.5 * (x - xr)
    return xe, xo


def energy_ct(t, x):
    return float(np.trapezoid(np.abs(x) ** 2, t))


def cross_energy_ct(t, a, b):
    return float(np.trapezoid(a * b, t))


def energy_dt(x):
    return float(np.sum(np.abs(x) ** 2))


def cross_energy_dt(a, b):
    return float(np.sum(a * b))


# ----------------------------
# Provided plotting
# ----------------------------
def main():
    # ---------- continuous ----------
    t = np.linspace(T_MIN, T_MAX, N)
    x = x_ct(t)
    xe, xo = even_odd_ct(t, x)

    Ex = energy_ct(t, x)
    Exe = energy_ct(t, xe)
    Exo = energy_ct(t, xo)
    cross = cross_energy_ct(t, xe, xo)
    print("=== Continuous-time  x(t)=e^{-t}u(t) ===")
    print(f"E_x           = {Ex:.6f}")
    print(f"E_xe + E_xo   = {Exe + Exo:.6f}  (E_xe={Exe:.6f}, E_xo={Exo:.6f})")
    print(f"cross-energy  = {cross:.2e}  (should be ~0)")

    # ---------- discrete ----------
    n = np.arange(-40, 41)
    xd = x_dt(n)
    xde, xdo = even_odd_dt(n, xd)
    Exd = energy_dt(xd)
    Exde = energy_dt(xde)
    Exdo = energy_dt(xdo)
    crossd = cross_energy_dt(xde, xdo)
    print("\n=== Discrete-time  x[n]=(0.7)^n u[n] ===")
    print(f"E_x           = {Exd:.6f}")
    print(f"E_xe + E_xo   = {Exde + Exdo:.6f}")
    print(f"cross-energy  = {crossd:.2e}  (should be ~0)")

    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(t, x, "k--", lw=1, label="x(t)")
    ax[0].plot(t, xe, label="xe(t)")
    ax[0].plot(t, xo, label="xo(t)")
    ax[0].set_xlim(-5, 5)
    ax[0].grid(alpha=.3)
    ax[0].legend(fontsize=8)
    ax[0].set_title("CT even/odd parts")
    ml, sl, bl = ax[1].stem(n, xde, linefmt="C0-", markerfmt="C0o", label="xe[n]")
    bl.set_visible(False)
    ml, sl, bl = ax[1].stem(n, xdo, linefmt="C1-", markerfmt="C1s", label="xo[n]")
    bl.set_visible(False)
    ax[1].set_xlim(-15, 15)
    ax[1].grid(alpha=.3)
    ax[1].legend(fontsize=8)
    ax[1].set_title("DT even/odd parts")
    fig.tight_layout()
    plt.show()

    # ---- verification ----
    assert abs((Exe + Exo) - Ex) < 1e-4 * Ex
    assert abs(cross) < 1e-6
    assert abs((Exde + Exdo) - Exd) < 1e-9
    assert abs(crossd) < 1e-9
    print("\nAll assertions passed.")


if __name__ == "__main__":
    main()
