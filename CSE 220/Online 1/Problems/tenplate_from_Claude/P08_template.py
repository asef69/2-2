import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# ANSWER IMPLEMENTATION
# ==========================================================

def power_over_interval(xfunc, t0, t1, n=200001):
    """Average power of x over [t0,t1]: (1/(t1-t0)) * integral |x|^2 dt."""
    raise NotImplementedError


def power_one_period(xfunc, T):
    """Average power over exactly one fundamental period [0, T]."""
    raise NotImplementedError


def power_k_periods(xfunc, T, K):
    """Average power over K periods [0, K*T]."""
    raise NotImplementedError


# ----------------------------
# Periodic test signals (given)
# ----------------------------
def rectified_sine(t): return np.abs(np.sin(t))
def cos_squared(t):    return np.cos(t) ** 2
def square_wave(t):    return np.sign(np.sin(np.pi*t)) + (np.sin(np.pi*t) == 0)
def half_sine_train(t):
    tt = np.mod(t, 2*np.pi); return np.where(tt <= np.pi, np.sin(tt), 0.0)


def main():
    signals = [("|sin t|", rectified_sine, np.pi, 0.5),
               ("square wave", square_wave, 2.0, 1.0),
               ("half-sine train", half_sine_train, 2*np.pi, 0.25),
               ("cos^2 t", cos_squared, np.pi, 3/8)]
    print(f"{'signal':18s}{'P(1 period)':>13s}{'P(8 periods)':>14s}{'exact':>9s}")
    for name, f, T, exact in signals:
        p1 = power_one_period(f, T); pK = power_k_periods(f, T, 8)
        print(f"{name:18s}{p1:13.6f}{pK:14.6f}{exact:9.4f}")

    t = np.linspace(0, 4*np.pi, 2000)
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.plot(t, half_sine_train(t), lw=1.8)
    ax.axvspan(0, 2*np.pi, color="orange", alpha=.15, label="one period")
    ax.grid(alpha=.3); ax.legend(fontsize=8); ax.set_xlabel("t")
    fig.tight_layout(); plt.show()


if __name__ == "__main__":
    main()
