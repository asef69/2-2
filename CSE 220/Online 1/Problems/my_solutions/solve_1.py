import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# ANSWER IMPLEMENTATION  (fill in the four functions below)
# ==========================================================

def energy_ct(t: np.ndarray, x: np.ndarray) -> float:
    """Energy of a sampled CT signal: integral of |x|^2 dt (use np.trapezoid)."""
    return float(np.trapezoid(np.abs(x)**2,t))


def power_ct(t: np.ndarray, x: np.ndarray) -> float:
    """Average power of a sampled CT signal: energy / (length of interval)."""
    T = t[-1] - t[0]
    return energy_ct(t,x)/T


def energy_dt(x: np.ndarray) -> float:
    """Energy of a DT signal: sum of |x[n]|^2."""
    return float(np.sum(np.abs(x)**2))


def power_dt(x: np.ndarray) -> float:
    """Average power of a DT signal: mean of |x[n]|^2."""
    # return energy_dt(x)/np.size(x)
    return float(np.mean(np.abs(x)**2))

def classify(energies: np.ndarray, powers: np.ndarray, e_tol: float = 1e6, p_tol: float = 1e-6) -> str:
    """Given energy/power measured over a sequence of GROWING windows, return
    one of "energy", "power", or "neither".
        energy signal : energy converges to a finite limit, power -> 0
        power  signal : energy grows without bound, power -> finite > 0
    """
    E_last = energies[-1]
    P_last = powers[-1]
    energy_settled = abs(energies[-1] - energies[-2]) <=0.02 * abs(energies[-1])

    power_settled = abs(powers[-1]-powers[-2]) <= 0.02 * abs(powers[-1]) 

    if energy_settled and E_last<e_tol:
        return "energy"
    if power_settled and P_last > p_tol:
        return "power"
    return "neither"


# ----------------------------
# Test signals (given)
# ----------------------------
def make_ct_signals():
    return {
        "e^{-|t|}":        lambda t: np.exp(-np.abs(t)),
        "cos(2*pi*0.5*t)": lambda t: np.cos(2 * np.pi * 0.5 * t),
        "constant 1":      lambda t: np.ones_like(t),
        "t (ramp)":        lambda t: t.astype(float),
    }


def make_dt_signals():
    return {
        "(0.8)^n u[n]":    lambda n: np.where(n >= 0, 0.8 ** np.abs(n), 0.0),
        "cos(pi n / 6)":   lambda n: np.cos(np.pi * n / 6),
        "n (ramp)":        lambda n: n.astype(float),
    }


def analyse_ct(xfunc, half_widths):
    Es, Ps = [], []
    for T in half_widths:
        t = np.linspace(-T, T, int(2000 * T) + 1)
        x = xfunc(t)
        Es.append(energy_ct(t, x)); Ps.append(power_ct(t, x))
    return np.array(Es), np.array(Ps)


def analyse_dt(xfunc, half_lengths):
    Es, Ps = [], []
    for M in half_lengths:
        n = np.arange(-M, M + 1)
        x = xfunc(n)
        Es.append(energy_dt(x)); Ps.append(power_dt(x))
    return np.array(Es), np.array(Ps)


def main():
    half_widths = [5, 10, 20, 40, 80]
    

    print("=== Continuous-time signals ===")
    for name, f in make_ct_signals().items():
        E, P = analyse_ct(f, half_widths)
        print(f"{name:22s} | E={E[-1]:.4g}  P={P[-1]:.4g}  -> {classify(E, P)}")
    half_lengths = [24, 120, 600, 1200, 3000]
    print("\n=== Discrete-time signals ===")
    for name, f in make_dt_signals().items():
        E, P = analyse_dt(f, half_lengths)
        print(f"{name:22s} | E={E[-1]:.4g}  P={P[-1]:.4g}  -> {classify(E, P)}")

    # TODO: also produce a plot of E vs window and P vs window (CT signals).
    fig,ax = plt.subplots(1,2,figsize=(10,4))
    for name,f in make_ct_signals().items():
        E,P = analyse_ct(f,half_widths)
        ax[0].plot(half_widths,E,marker='o', label = name)
        ax[1].plot(half_widths,P,marker='s', label = name)
    ax[0].set_title("Energy vs window (CT)")
    ax[0].set_xlabel("Half width T")
    ax[0].set_ylabel("E[-T,T]")
    ax[0].set_ylim(0,20)
    ax[0].legend(fontsize=7)
    ax[0].grid(alpha = .3)
    ax[1].set_title("Power vs Window")
    ax[1].set_xlabel("Half width T")
    ax[1].set_ylabel("P[-T,T]")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
