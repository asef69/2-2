import numpy as np #type:ignore
import matplotlib.pyplot as plt


# ─────────────────────────────────────────────
#  BASE SIGNAL  x(t) = e^{-|t|}  for -2 <= t <= 2, else 0
# ─────────────────────────────────────────────

def base_signal(t):
    x = np.exp(-np.abs(t))
    x[(t < -2) | (t > 2)] = 0
    return x


# ═══════════════════════════════════════════════════════════════════
#  QUESTION 1 – Time Reversal + Amplitude Scaling
#  y(t) = alpha * x(-t)
# ═══════════════════════════════════════════════════════════════════

def q1_transform(t, x, alpha):
    """
    Compute y(t) = alpha * x(-t).

    Steps:
      1. Use np.interp(-t, t, x) to evaluate x at -t.
         np.interp(query_points, known_t, known_x, left=0, right=0)
         returns 0 for any query point outside [t[0], t[-1]].
      2. Multiply the result by alpha.

    Returns:
        y (np.ndarray): transformed signal sampled on the same t axis.
    """
    y=alpha*np.interp(-t,t,x,left=0,right=0)
    return y


def q1_main():
    t = np.linspace(-2, 2, 1000)
    x = base_signal(t)

    while True:
        raw = input("Q1 | Enter alpha (or 'q' to quit): ").strip()
        if raw.lower() == 'q':
            break
        try:
            alpha = float(raw)
        except ValueError:
            print("  Invalid input. Please enter a number.")
            continue

        y = q1_transform(t, x, alpha)

        plt.figure(figsize=(8, 4))
        plt.plot(t, x, label='x(t)')
        plt.plot(t, y, label=f'y(t) = {alpha} * x(-t)', linestyle='--')
        plt.xlabel('t')
        plt.ylabel('Amplitude')
        plt.title('Q1 – Time Reversal & Amplitude Scaling')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


# ═══════════════════════════════════════════════════════════════════
#  QUESTION 2 – Time Scaling
#  y(t) = x(a*t)
# ═══════════════════════════════════════════════════════════════════

def q2_transform(t, x, a):
    """
    Compute y(t) = x(a*t).

    Steps:
      1. Use np.interp(a*t, t, x, left=0, right=0) to evaluate x at a*t.
      2. Return the result directly (no amplitude change).

    Note:
      - |a| > 1  compresses the signal in time.
      - |a| < 1  stretches the signal in time.
      - a < 0    also reverses the signal.

    Returns:
        y (np.ndarray): transformed signal sampled on the same t axis.
    """
    y=np.interp(a*t,t,x,left=0,right=0)
    return y

def q2_main():
    t = np.linspace(-4, 4, 2000)   # wider window to show stretching
    x = base_signal(t)

    while True:
        raw = input("Q2 | Enter scaling factor a (or 'q' to quit): ").strip()
        if raw.lower() == 'q':
            break
        try:
            a = float(raw)
            if a == 0:
                print("  'a' must be nonzero.")
                continue
        except ValueError:
            print("  Invalid input. Please enter a number.")
            continue

        y = q2_transform(t, x, a)

        plt.figure(figsize=(8, 4))
        plt.plot(t, x, label='x(t)')
        plt.plot(t, y, label=f'y(t) = x({a}t)', linestyle='--')
        plt.xlabel('t')
        plt.ylabel('Amplitude')
        plt.title('Q2 – Time Scaling')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


# ═══════════════════════════════════════════════════════════════════
#  QUESTION 3 – Combined Transformation
#  y(t) = beta * x(a*t - t0)
# ═══════════════════════════════════════════════════════════════════

def q3_transform(t, x, beta, a, t0):
    """
    Compute y(t) = beta * x(a*t - t0).

    Steps:
      1. Compute the query points: q = a*t - t0
      2. Use np.interp(q, t, x, left=0, right=0) to evaluate x at q.
      3. Multiply by beta.

    Returns:
        y (np.ndarray): transformed signal sampled on the same t axis.
    """
    q=a*t-t0
    y=beta*np.interp(q,t,x,left=0,right=0)
    return y


def q3_main():
    t = np.linspace(-6, 6, 2000)
    x = base_signal(t)

    while True:
        raw = input("Q3 | Enter 'beta a t0' (e.g. 2 0.5 1) or 'q': ").strip()
        if raw.lower() == 'q':
            break
        parts = raw.split()
        if len(parts) != 3:
            print("  Please enter exactly three numbers.")
            continue
        try:
            beta, a, t0 = float(parts[0]), float(parts[1]), float(parts[2])
            if a == 0:
                print("  'a' must be nonzero.")
                continue
        except ValueError:
            print("  Invalid input.")
            continue

        y = q3_transform(t, x, beta, a, t0)

        plt.figure(figsize=(8, 4))
        plt.plot(t, x, label='x(t)')
        plt.plot(t, y, label=f'y(t) = {beta}·x({a}t - {t0})', linestyle='--')
        plt.xlabel('t')
        plt.ylabel('Amplitude')
        plt.title('Q3 – Combined Transformation')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


# ═══════════════════════════════════════════════════════════════════
#  QUESTION 4 – Odd / Even Decomposition
#  x_e(t) = [x(t) + x(-t)] / 2
#  x_o(t) = [x(t) - x(-t)] / 2
# ═══════════════════════════════════════════════════════════════════

def q4_even(t, x):
    """
    Compute the even part: x_e(t) = [x(t) + x(-t)] / 2.

    Steps:
      1. Use np.interp(-t, t, x, left=0, right=0) to get x(-t).
      2. Return (x + x_reversed) / 2.

    Returns:
        x_e (np.ndarray)
    """
    x_reversed=np.interp(-t,t,x,left=0,right=0)
    return (x+x_reversed)/2


def q4_odd(t, x):
    """
    Compute the odd part: x_o(t) = [x(t) - x(-t)] / 2.

    Steps:
      1. Use np.interp(-t, t, x, left=0, right=0) to get x(-t).
      2. Return (x - x_reversed) / 2.

    Returns:
        x_o (np.ndarray)
    """
    x_reversed=np.interp(-t,t,x,left=0,right=0)
    return (x-x_reversed)/2


def q4_main():
    t = np.linspace(-2, 2, 1000)
    x = base_signal(t)

    x_e = q4_even(t, x)
    x_o = q4_odd(t, x)

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    axes[0, 0].plot(t, x, color='steelblue')
    axes[0, 0].set_title('x(t) – Original Signal')
    axes[0, 0].set_xlabel('t'); axes[0, 0].set_ylabel('Amplitude')
    axes[0, 0].grid(True)

    axes[0, 1].plot(t, x_e, color='darkorange')
    axes[0, 1].set_title('x_e(t) – Even Part')
    axes[0, 1].set_xlabel('t'); axes[0, 1].set_ylabel('Amplitude')
    axes[0, 1].grid(True)

    axes[1, 0].plot(t, x_o, color='green')
    axes[1, 0].set_title('x_o(t) – Odd Part')
    axes[1, 0].set_xlabel('t'); axes[1, 0].set_ylabel('Amplitude')
    axes[1, 0].grid(True)

    if x_e is not None and x_o is not None:
        reconstructed = x_e + x_o
        axes[1, 1].plot(t, reconstructed, color='purple')
        axes[1, 1].set_title('x_e(t) + x_o(t) – Reconstruction (verify = x(t))')
    else:
        axes[1, 1].set_title('Reconstruction (implement functions first)')
    axes[1, 1].set_xlabel('t'); axes[1, 1].set_ylabel('Amplitude')
    axes[1, 1].grid(True)

    plt.suptitle('Q4 – Odd / Even Decomposition', fontsize=14)
    plt.tight_layout()
    plt.show()


# ═══════════════════════════════════════════════════════════════════
#  QUESTION 5 – Energy and Power
#  E = integral of |x(t)|^2 dt   (Riemann sum)
#  P = E / T_total
# ═══════════════════════════════════════════════════════════════════

def q5_energy(t, x):
    """
    Compute total energy using a Riemann sum.

      E = integral |x(t)|^2 dt
        ≈ sum( x[i]^2 * dt )   where dt = t[1] - t[0]

    Steps:
      1. Compute dt = t[1] - t[0].
      2. Return np.sum(x**2) * dt.

    Returns:
        E (float)
    """
    dt=t[1]-t[0]
    E=np.sum(x**2)*dt
    return float(E)


def q5_power(t, x):
    """
    Compute average power over the observation window.

      P = (1 / T_total) * integral |x(t)|^2 dt
        = E / T_total

    Steps:
      1. Compute E using q5_energy(t, x).
      2. Compute T_total = t[-1] - t[0].
      3. Return E / T_total.

    Returns:
        P (float)
    """
    T_total=t[-1]-t[0]
    P=q5_energy(t,x)/T_total
    return P


def q5_main():
    t = np.linspace(-2, 2, 10000)
    x = base_signal(t)

    E = q5_energy(t, x)
    P = q5_power(t, x)

    plt.figure(figsize=(8, 4))
    plt.plot(t, x, label='x(t)')
    plt.fill_between(t, x**2, alpha=0.2, label='|x(t)|^2 (energy density)')
    plt.xlabel('t')
    plt.ylabel('Amplitude')
    plt.title('Q5 – Energy & Power')
    plt.legend()
    plt.grid(True)

    info = ""
    if E is not None:
        info += f"Energy  E = {E:.6f} J\n"
    if P is not None:
        info += f"Power   P = {P:.6f} W"
    if info:
        plt.gcf().text(0.15, 0.78, info, fontsize=10,
                       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    plt.show()

    print(f"\n{'='*40}")
    if E is not None:
        print(f"  Energy  E = {E:.6f} J")
    else:
        print("  Energy: Not implemented yet.")
    if P is not None:
        print(f"  Power   P = {P:.6f} W")
    else:
        print("  Power:  Not implemented yet.")
    print(f"{'='*40}\n")


# ═══════════════════════════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════════════════════════

MENU = """
╔══════════════════════════════════════════════╗
║   CSE 220 – Signals Practice Set             ║
╠══════════════════════════════════════════════╣
║  1. Time Reversal + Amplitude Scaling        ║
║  2. Time Scaling                             ║
║  3. Combined Transformation (scale+shift)    ║
║  4. Odd / Even Decomposition                 ║
║  5. Energy and Power                         ║
║  q. Quit                                     ║
╚══════════════════════════════════════════════╝
"""

def main():
    handlers = {
        '1': q1_main,
        '2': q2_main,
        '3': q3_main,
        '4': q4_main,
        '5': q5_main,
    }
    while True:
        print(MENU)
        choice = input("Select a question: ").strip()
        if choice.lower() == 'q':
            print("Goodbye!")
            break
        if choice in handlers:
            handlers[choice]()
        else:
            print("  Invalid choice. Enter 1-5 or q.")


if __name__ == "__main__":
    main()
