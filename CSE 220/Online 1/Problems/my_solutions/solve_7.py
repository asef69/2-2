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
    xr = np.interp(-t,t,x,left=0.0, right=0.0)
    ev=0.5*(x+xr)
    od = 0.5*(x-xr)
    return ev,od


def even_odd_dt(n, x):
    """Even and odd parts of a DT signal on a symmetric index range."""
    xr = np.interp(-n,n,x,left=0.0, right=0.0)
    ev=0.5*(x+xr)
    od = 0.5*(x-xr)
    return ev,od


def energy_ct(t, x):
    return float(np.trapezoid(np.abs(x)**2,t))
def cross_energy_ct(t, a, b):
    return float(np.trapezoid(np.abs(a*np.conj(b)),t))
def energy_dt(x):
    return float(np.sum(np.abs(x)**2))
def cross_energy_dt(a, b):  
    return float(np.sum(np.abs(a*b)))


def main():
    t = np.linspace(T_MIN, T_MAX, N)
    x = x_ct(t)
    xe, xo = even_odd_ct(t, x)
    print("=== Continuous-time ===")
    print(f"E_x        = {energy_ct(t, x):.6f}")
    print(f"E_xe+E_xo  = {energy_ct(t, xe)+energy_ct(t, xo):.6f}")
    print(f"cross-eng  = {cross_energy_ct(t, xe, xo):.2e}")

    n = np.arange(-40, 41)
    xd = x_dt(n)
    xde, xdo = even_odd_dt(n, xd)
    print("\n=== Discrete-time ===")
    print(f"E_x        = {energy_dt(xd):.6f}")
    print(f"E_xe+E_xo  = {energy_dt(xde)+energy_dt(xdo):.6f}")
    print(f"cross-eng  = {cross_energy_dt(xde, xdo):.2e}")

    # TODO: plot the CT and DT even/odd parts.
    fig,ax = plt.subplots(1,2,figsize=(10,6))
    ax[0].plot(t,x,"r--",lw=1)
    ax[0].plot(t,xe,"b--",lw=1)
    ax[0].plot(t,xo,"c--", lw=1)
    ax[0].set_xlim(-5,5)
    ax[0].grid(alpha=0.3)

    ml,sl,bl = ax[1].stem(n,xd, markerfmt='C0o',linefmt = 'C0-', label = 'x[n]')
    bl.set_visible(False)
    ml,sl,bl = ax[1].stem(n,xde,markerfmt='C1s',linefmt='C1-', label='xe[n]')
    bl.set_visible(False)
    ml,sl,bl = ax[1].stem(n,xdo,markerfmt='C2o',linefmt='C2-', label = 'xo[n]')
    bl.set_visible(False)
    ax[1].set_xlim(-15,15)
    ax[1].grid(alpha=0.3)
    ax[1].legend(fontsize=8)

    fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
