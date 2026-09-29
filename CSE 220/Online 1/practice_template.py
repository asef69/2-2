import numpy as np  # type: ignore
import matplotlib.pyplot as plt


# =====================================================================
#  CSE 219/220 - Signals: PRACTICE TEMPLATE
#  Covers every transformation style seen in Lecture 1 and in the
#  sample exam (spec_set2.pdf). Follows the same structure as the
#  official template (set2.py): a base_signal(t) generator, one
#  function per task, and a main() with an interactive input loop.
#
#  HOW TO USE:
#   - Each function below has a short docstring describing what the
#     real exam question will likely ask, plus a "# TODO" where you
#     write your own implementation during practice.
#   - main() already wires everything together with matplotlib so you
#     can just fill in the TODOs and run the file to see your plots.
# =====================================================================


# ---------------------------------------------------------------------
# 0. BASE SIGNALS (given in the exam, you normally don't write these)
# ---------------------------------------------------------------------

def base_signal_continuous(t):
    """
    A sample continuous-time base signal x(t), bounded on [-pi, pi],
    zero elsewhere. The real exam may give you a different formula
    (e.g. exp(-t)*cos(t), a triangular pulse, a piecewise signal) but
    the pattern is always: compute the formula, then zero-out the
    values outside the stated support using boolean masking.
    """
    x = np.exp(-t) * np.cos(t)
    x[(t < -np.pi) | (t > np.pi)] = 0
    return x


def base_signal_discrete(n):
    """
    A sample discrete-time base signal x[n], nonzero only for
    0 <= n <= 5 (a simple ramp), zero elsewhere. Discrete questions
    give you an integer index array n (e.g. np.arange(-10, 11)).
    """
    x = np.where((n >= 0) & (n <= 5), n * 0.5, 0.0)
    return x


# ---------------------------------------------------------------------
# 1. TIME SHIFTING:  y(t) = x(t - t0)   /   y[n] = x[n - n0]
# ---------------------------------------------------------------------

def shift_signal_continuous(t, x, t0):
    """
    Delay (t0 > 0) or advance (t0 < 0) a continuous signal:
        y(t) = x(t - t0)
    Use np.interp to resample x at (t - t0); points that fall outside
    the original t-range should map to 0 (left=0.0, right=0.0).
    """
    return np.interp(t-t0,t,x,left=0,right=0)
    
    


def shift_signal_discrete(n, x, n0):
    """
    Delay (n0 > 0) or advance (n0 < 0) a discrete signal:
        y[n] = x[n - n0]
    Since n is an integer index array, use np.interp with the same
    idea, or roll + zero-pad. np.interp also works cleanly here since
    n is evenly spaced integers.
    """
    return np.interp(n-n0,n,x,left=0,right=0)
    
    


# ---------------------------------------------------------------------
# 2. TIME REVERSAL:  y(t) = x(-t)   /   y[n] = x[-n]
# ---------------------------------------------------------------------

def reverse_signal(t, x):
    """
    Mirror the signal about the vertical axis: y(t) = x(-t).
    Works identically for continuous (t) or discrete (n) index arrays.
    """
    return np.interp(-t,t,x,left=0,right=0)
    
   


# ---------------------------------------------------------------------
# 3. AMPLITUDE SCALING:  y(t) = alpha * x(t)
# ---------------------------------------------------------------------

def amplitude_scale(x, alpha):
    """
    Scale (compress/expand/flip) the amplitude only; the time axis is
    untouched: y(t) = alpha * x(t).
    """
    return alpha*x
    


# ---------------------------------------------------------------------
# 4. TIME SCALING:  y(t) = x(alpha * t)   (compression if |alpha|>1,
#    stretching if |alpha|<1, reversal built in automatically if
#    alpha < 0)
# ---------------------------------------------------------------------

def time_scale(t, x, alpha):
    """
    Compress or stretch the time axis: y(t) = x(alpha * t).
    A negative alpha simultaneously reverses the signal, so this one
    function can be reused for reversal + scaling combos.
    """
    return np.interp(alpha*t,t,x,left=0,right=0)
    


# ---------------------------------------------------------------------
# 5. COMBINED TRANSFORM:  y(t) = alpha * x(beta * t + gamma)
#    (general "shift, reverse/scale" recipe from the lecture:
#       Step 1: g1(t) = x(t + gamma)          -- shift
#       Step 2: g2(t) = g1(-t) if beta<0 else g1(t)   -- reversal
#       Step 3: g3(t) = g2(|beta| * t) = x(beta*t + gamma) -- scale
#       Step 4: y(t)  = alpha * g3(t)          -- amplitude scale
# ---------------------------------------------------------------------

def transform_general(t, x, alpha=1.0, beta=1.0, gamma=0.0):
    """
    Most general single-function version of every transform combined:
        y(t) = alpha * x(beta * t + gamma)
    This is the pattern most exam questions like spec_set2.pdf boil
    down to (there alpha=alpha, beta=-1, gamma=0).
    """
    return alpha*np.interp(beta*t+gamma,t,x,left=0,right=0)
    


# ---------------------------------------------------------------------
# 6. EVEN / ODD DECOMPOSITION
#       x_e(t) = 0.5 * [x(t) + x(-t)]     (even part)
#       x_o(t) = 0.5 * [x(t) - x(-t)]     (odd part)
# ---------------------------------------------------------------------

def even_part(t, x):
    """Return the even part of x: xe(t) = 0.5*(x(t) + x(-t))."""
    x_rev=np.interp(-t,t,x,left=0,right=0)
    return 0.5*(x+x_rev)
    


def odd_part(t, x):
    """Return the odd part of x: xo(t) = 0.5*(x(t) - x(-t))."""
    x_rev=np.interp(-t,t,x,left=0,right=0)
    return 0.5*(x-x_rev)

    


# ---------------------------------------------------------------------
# 7. ENERGY AND POWER
#    Continuous:  E = integral |x(t)|^2 dt      (use np.trapz)
#                 P = E / (t2 - t1)
#    Discrete:    E = sum |x[n]|^2               (use np.sum)
#                 P = E / (n2 - n1 + 1)
# ---------------------------------------------------------------------

def energy_continuous(t, x):
    """Total energy of a continuous signal over the sampled range t."""
    return float(np.sum(np.abs(x)**2)*(t[-1]-t[0]))
    


def power_continuous(t, x):
    """Average power of a continuous signal over the sampled range t."""
    return energy_continuous(t,x)/(t[-1]-t[0])
    


def energy_discrete(x):
    """Total energy of a discrete signal (sum of squared magnitudes)."""
    return np.sum(np.abs(x)**2)
    


def power_discrete(x):
    """Average power of a discrete signal (energy / number of samples)."""
    return energy_discrete(x)/len(x)
    


# =====================================================================
# MAIN: interactive menu, same "loop until 'q'" style as the official
# template. Pick the task that matches your exam question and run it;
# delete/ignore the branches you don't need.
# =====================================================================

def main():
    # --- continuous-time setup ---
    t = np.linspace(-2 * np.pi, 2 * np.pi, 2000)
    x = base_signal_continuous(t)

    # --- discrete-time setup ---
    n = np.arange(-10, 11)
    xn = base_signal_discrete(n)

    menu = """
Choose a task:
  1) Time shift            y(t) = x(t - t0)
  2) Time reversal         y(t) = x(-t)
  3) Amplitude scaling     y(t) = alpha * x(t)
  4) Time scaling          y(t) = x(alpha * t)
  5) General combined      y(t) = alpha * x(beta*t + gamma)
  6) Even / Odd decomposition
  7) Energy & Power (continuous)
  8) Energy & Power (discrete, stem plot)
  q) Quit
"""

    while True:
        print(menu)
        choice = input("Enter choice: ").strip().lower()

        if choice == 'q':
            print("Quitting.")
            break

        elif choice == '1':
            t0 = float(input("t0 = "))
            y = shift_signal_continuous(t, x, t0)
            plt.figure(figsize=(8, 5))
            plt.plot(t, x, label='x(t)')
            plt.plot(t, y, label=f'y(t) = x(t - {t0})')
            plt.xlabel('t'); plt.ylabel('Amplitude')
            plt.title('Time Shift'); plt.legend(); plt.grid(True)
            plt.show()

        elif choice == '2':
            y = reverse_signal(t, x)
            plt.figure(figsize=(8, 5))
            plt.plot(t, x, label='x(t)')
            plt.plot(t, y, label='y(t) = x(-t)')
            plt.xlabel('t'); plt.ylabel('Amplitude')
            plt.title('Time Reversal'); plt.legend(); plt.grid(True)
            plt.show()

        elif choice == '3':
            alpha = float(input("alpha = "))
            y = amplitude_scale(x, alpha)
            plt.figure(figsize=(8, 5))
            plt.plot(t, x, label='x(t)')
            plt.plot(t, y, label=f'y(t) = {alpha} * x(t)')
            plt.xlabel('t'); plt.ylabel('Amplitude')
            plt.title('Amplitude Scaling'); plt.legend(); plt.grid(True)
            plt.show()

        elif choice == '4':
            alpha = float(input("alpha = "))
            y = time_scale(t, x, alpha)
            plt.figure(figsize=(8, 5))
            plt.plot(t, x, label='x(t)')
            plt.plot(t, y, label=f'y(t) = x({alpha} * t)')
            plt.xlabel('t'); plt.ylabel('Amplitude')
            plt.title('Time Scaling'); plt.legend(); plt.grid(True)
            plt.show()

        elif choice == '5':
            alpha = float(input("alpha = "))
            beta = float(input("beta  = "))
            gamma = float(input("gamma = "))
            y = transform_general(t, x, alpha, beta, gamma)
            plt.figure(figsize=(8, 5))
            plt.plot(t, x, label='x(t)')
            plt.plot(t, y, label=f'y(t) = {alpha}*x({beta}t + {gamma})')
            plt.xlabel('t'); plt.ylabel('Amplitude')
            plt.title('General Combined Transform')
            plt.legend(); plt.grid(True)
            plt.show()

        elif choice == '6':
            xe = even_part(t, x)
            xo = odd_part(t, x)
            fig, axs = plt.subplots(1, 3, figsize=(15, 4))
            axs[0].plot(t, x); axs[0].set_title('x(t)'); axs[0].grid(True)
            axs[1].plot(t, xe); axs[1].set_title('Even part'); axs[1].grid(True)
            axs[2].plot(t, xo); axs[2].set_title('Odd part'); axs[2].grid(True)
            for ax in axs:
                ax.set_xlabel('t'); ax.set_ylabel('Amplitude')
            plt.tight_layout()
            plt.show()

        elif choice == '7':
            E = energy_continuous(t, x)
            P = power_continuous(t, x)
            print(f"Energy = {E:.4f}, Power = {P:.4f}")
            plt.figure(figsize=(8, 5))
            plt.plot(t, x, label='x(t)')
            plt.title(f'x(t)  |  E = {E:.4f}, P = {P:.4f}')
            plt.xlabel('t'); plt.ylabel('Amplitude')
            plt.legend(); plt.grid(True)
            plt.show()

        elif choice == '8':
            E = energy_discrete(xn)
            P = power_discrete(xn)
            print(f"Energy = {E:.4f}, Power = {P:.4f}")
            plt.figure(figsize=(8, 5))
            plt.stem(n, xn)
            plt.title(f'x[n]  |  E = {E:.4f}, P = {P:.4f}')
            plt.xlabel('n'); plt.ylabel('Amplitude')
            plt.grid(True)
            plt.show()

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
