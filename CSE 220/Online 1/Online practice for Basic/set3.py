import numpy as np #type:ignore
import matplotlib.pyplot as plt
from typing import Tuple

INF = 8

def plot(
        signal, 
        title=None, 
        y_range=(-1, 3), 
        figsize = (8, 3),
        x_label='n (Time Index)',
        y_label='x[n]',
        saveTo=None
    ):
    plt.figure(figsize=figsize)
    # create x indices centered so that the center index corresponds to 0
    N = len(signal)
    center = (N - 1) // 2
    x = np.arange(N) - center

    # set x ticks (limit number of ticks to reasonable amount)
    plt.xticks(x)

    y_range = (y_range[0], max(np.max(signal), y_range[1]) + 1)
    plt.ylim(*y_range)
    plt.stem(x, signal)
    plt.title(title)#type:ignore
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    if saveTo is not None:
        plt.savefig(saveTo)
    # plt.show()

def init_signal():
    return np.zeros(2 * INF + 1)


def time_scale_signal(x, k):
    y = np.zeros_like(x)
    n = np.arange(len(x)) - INF
    mask = (n % k == 0)
    src_n = n[mask] // k
    src_i = src_n + INF
    valid = (src_i >= 0) & (src_i < len(x))
    out_i = (n[mask] + INF)[valid]
    y[out_i] = x[src_i[valid]]
    return y

def time_scale_signal_interpolate(x, k):
    y = time_scale_signal(x, k)  # correct x[n/k] with zeros, from above
    n = np.arange(len(x)) - INF
    for idx in range(len(x)):
        if n[idx] % k != 0:
            # find surrounding filled samples
            left_n = (n[idx] // k) * k
            right_n = left_n + k
            left_i, right_i = left_n + INF, right_n + INF
            if 0 <= left_i < len(x) and 0 <= right_i < len(x):
                y[idx] = (y[left_i] + y[right_i]) / 2
    return y                            # ← never fills intermediate values!


def main():
    img_root = '.'
    signal = init_signal()
    signal[INF] = 1
    signal[INF+1] = .5
    signal[INF-1] = 2
    signal[INF + 2] = 1
    signal[INF - 2] = .5

    plot(signal, title='Original Signal(x[n])', saveTo=f'{img_root}/x[n].png')
    plot(time_scale_signal(signal, 3), title='x[n/3]', saveTo=f'{img_root}/x[n divided by 3].png')
    plot(time_scale_signal(signal, 1), title='x[n/1]', saveTo=f'{img_root}/x[n divided by 1].png')
    plot(time_scale_signal_interpolate(signal, 3), title='x[n/3] with interpolation', saveTo=f'{img_root}/x[n divided by 3]_with_interpolation.png')
    plot(time_scale_signal_interpolate(signal, 1), title='x[n/1] with interpolation', saveTo=f'{img_root}/x[n divided by 1]_with_interpolation.png')

main()
