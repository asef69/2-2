import numpy as np #type:ignore
import matplotlib.pyplot as plt


def base_signal(t):
    x = np.exp(-t) * np.cos(t)
    x[(t < -np.pi) | (t > np.pi)] = 0
    return x



def transform_signal(t, x, alpha):
    # Compute y(t) = alpha * x(-t)
    # Use interpolation so that sampled -t maps to appropriate x values.
    # Values outside the original t range are treated as 0 via left/right params.
    x_at_neg_t = np.interp(-t, t, x, left=0.0, right=0.0)
    y = alpha * x_at_neg_t
    return y


def main():
    t = np.linspace(-np.pi, np.pi, 1000)
    x = base_signal(t)

    while True:
        user_in = input("Enter alpha (or 'q' to quit): ").strip()
        if user_in.lower() == 'q':
            print('Quitting.')
            break

        try:
            alpha = float(user_in)
        except ValueError:
            print("Invalid input. Enter a number for alpha or 'q' to quit.")
            continue

        y = transform_signal(t, x, alpha)

        plt.figure(figsize=(8, 5))
        plt.plot(t, x, label='x(t)')
        plt.plot(t, y, label=f'y(t) = {alpha} * x(-t)')
        plt.xlabel('t')
        plt.ylabel('Amplitude')
        plt.title('Time Reversal and Amplitude Scaling of x(t)')
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    main()