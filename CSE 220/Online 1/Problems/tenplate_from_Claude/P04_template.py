import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def energy_window(xfunc, T: float, samples_per_unit: int = 800) -> float:
    """Numerically integrate |x(t)|^2 over [-T, T] (trapezoidal). Cap the
    number of samples so large T stays fast."""
    raise NotImplementedError


def energy_curve(xfunc, Ts):
    """Return array E(T) for each half-width in Ts."""
    raise NotImplementedError


def classify_convergence(Ts, E) -> str:
    """Assume Ts grows geometrically (doubles). Return "finite" if the
    increments dE_k = E[k+1]-E[k] shrink toward 0 (finite energy), else
    "infinite"."""
    raise NotImplementedError


def estimated_limit(Ts, E) -> float:
    """Best estimate of total energy = largest-window value."""
    raise NotImplementedError


# ----------------------------
# Test signals (given)
# ----------------------------
def x_exp(t):   return np.exp(-np.abs(t))
def x_slow(t):  return 1.0 / np.sqrt(1.0 + np.abs(t))
def x_cos(t):   return np.cos(t)
def x_tail(t):
    y = np.zeros_like(t, dtype=float); inside = np.abs(t) <= 1
    y[inside] = 1.0; y[~inside] = 1.0 / np.abs(t[~inside]); return y


def main():
    Ts = 2.0 ** np.arange(1, 13)   # 2,4,...,4096
    signals = {"e^{-|t|}": x_exp, "lecture 1/|t|": x_tail,
               "1/sqrt(1+|t|)": x_slow, "cos(t)": x_cos}
    fig, ax = plt.subplots(figsize=(9, 4.2))
    for name, f in signals.items():
        E = energy_curve(f, Ts)
        kind = classify_convergence(Ts, E)
        lim = estimated_limit(Ts, E) if kind == "finite" else np.inf
        print(f"{name:18s} -> {kind:8s}  E(inf) ~ {lim:.4g}")
        ax.plot(Ts, E, marker="o", label=f"{name} [{kind}]")
    ax.set_xscale("log"); ax.set_ylim(0, 12); ax.grid(alpha=.3)
    ax.set_xlabel("T"); ax.set_ylabel("E[-T,T]"); ax.legend(fontsize=8)
    fig.tight_layout(); plt.show()


if __name__ == "__main__":
    main()
