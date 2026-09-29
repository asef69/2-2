import numpy as np
import matplotlib.pyplot as plt

T_MIN, T_MAX, N = -8.0, 8.0, 16001   # symmetric grid, 0 is a sample


def x_ct(t): return np.where(t >= 0, np.exp(-t), 0.0)          # given
def x_dt(n): return np.where(n >= 0, 0.7 ** np.abs(n), 0.0)    # given


# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def even_odd_ct(t, x):
    """Even and odd parts on a grid symmetric about 0. Hint: x(-t) is the
    reversed sample array x[::-1]."""
    raise NotImplementedError


def even_odd_dt(n, x):
    """Even and odd parts of a DT signal on a symmetric index range."""
    raise NotImplementedError


def energy_ct(t, x):        raise NotImplementedError
def cross_energy_ct(t, a, b): raise NotImplementedError
def energy_dt(x):           raise NotImplementedError
def cross_energy_dt(a, b):  raise NotImplementedError


def main():
    t = np.linspace(T_MIN, T_MAX, N); x = x_ct(t)
    xe, xo = even_odd_ct(t, x)
    print("=== Continuous-time ===")
    print(f"E_x        = {energy_ct(t, x):.6f}")
    print(f"E_xe+E_xo  = {energy_ct(t, xe)+energy_ct(t, xo):.6f}")
    print(f"cross-eng  = {cross_energy_ct(t, xe, xo):.2e}")

    n = np.arange(-40, 41); xd = x_dt(n)
    xde, xdo = even_odd_dt(n, xd)
    print("\n=== Discrete-time ===")
    print(f"E_x        = {energy_dt(xd):.6f}")
    print(f"E_xe+E_xo  = {energy_dt(xde)+energy_dt(xdo):.6f}")
    print(f"cross-eng  = {cross_energy_dt(xde, xdo):.2e}")

    # TODO: plot the CT and DT even/odd parts.
    plt.show()


if __name__ == "__main__":
    main()
