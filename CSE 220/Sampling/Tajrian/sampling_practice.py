"""Sampling Practice Template.

Mirrors the style of your alias.py assignment: fill in the functions
marked TODO, then run this file to check your answers against the
test cases at the bottom (main() is provided — do not modify it).

Covers Templates A-E from the study guide:
    A - lowest_alias_partner        (find an alias partner)
    B - nyquist_check                (is fs fast enough?)
    C - reverse_alias_candidates     (what could the true frequency be?)
    D - ideal_reconstruction_cutoff  (what cutoff should the LPF use?)
    E - dft_bin_to_frequency         (bin index -> physical frequency)

Run with:  python sampling_practice.py
"""

import numpy as np


# ---------------------------------------------------------------------------
# Template A: lowest positive alias partner
# ---------------------------------------------------------------------------
def lowest_alias_partner(f, fs):
    """Smallest positive frequency other than f giving identical samples at fs.

    Assumes 0 < f < fs/2.
    """
    
    return (fs - f)


# ---------------------------------------------------------------------------
# Template B: Nyquist check
# ---------------------------------------------------------------------------
def nyquist_check(f_max, fs):
    """Return True if sampling at fs avoids aliasing for a signal whose
    highest frequency component is f_max, False otherwise.
    """
    
    return (fs > 2*f_max)


# ---------------------------------------------------------------------------
# Template C: reverse alias - list plausible true frequencies
# ---------------------------------------------------------------------------
def reverse_alias_candidates(f_obs, fs, f_range):
    """Return a sorted list of frequencies in f_range=(low, high) that would
    alias down to f_obs when sampled at fs.

    A frequency f_true aliases to f_obs if, for some integer k:
        f_obs == f_true + k*fs   or   f_obs == -f_true + k*fs

    Search a reasonable range of k (e.g. -20..20) and keep the candidates
    that land inside f_range.
    """
    low, high = f_range
    
    candidates = set()
    
    for k in range(-20, 21):
        f_true = f_obs - k*fs
        
        if low <= f_true <= high:
            candidates.add(f_true)
            
        f_true = k*fs - f_obs 
        
        if low <= f_true <= high:
            candidates.add(f_true)   
    
    return sorted(candidates)     


# ---------------------------------------------------------------------------
# Template D: ideal reconstruction filter cutoff
# ---------------------------------------------------------------------------
def ideal_reconstruction_cutoff(f_max, fs):
    """Return the conventional cutoff frequency (Hz) for the ideal
    reconstruction low-pass filter: the midpoint between f_max and fs - f_max.

    Raise ValueError if Nyquist is not satisfied (no valid cutoff exists).
    """
    if(fs <= 2*f_max):
        raise ValueError("frequency less than  minimum")
    else:
        return fs/2


# ---------------------------------------------------------------------------
# Template E: DFT bin <-> physical frequency
# ---------------------------------------------------------------------------
def dft_bin_to_frequency(k, N, fs):
    """Physical frequency (Hz) represented by DFT bin k, for an N-point DFT
    of a signal sampled at fs.

    For k <= N/2: positive frequency = k * fs / N
    For k >  N/2: wrapped negative frequency = (k - N) * fs / N
    """
    if k <= N/2:
        return k * fs / N
    else:
        return (k - N) * fs / N
    
def ideal_lpf_sinc(samples, fs, t, fc=None):
    """Filter/reconstruct by convolving with sinc, evaluated at times t.
 
    With fc = fs/2 (the default) this is exact reconstruction: the
    filter passes the whole baseband and nothing else. With fc < fs/2
    it becomes a genuine low-pass, and the impulse response narrows in
    frequency, so it WIDENS in time - h(t) = (2*fc/fs)*sinc(2*fc*t).
 
    np.sinc is the normalised sinc, sin(pi*u)/(pi*u), so the argument
    carries no extra factor of pi."""
    fc = fs / 2 if fc is None else fc
    samples = np.asarray(samples, dtype=float)
    n = np.arange(len(samples))
    t = np.atleast_1d(np.asarray(t, dtype=float))
    dt = t[:, None] - n[None, :] / fs
    h = (2 * fc / fs) * np.sinc(2 * fc * dt)
    return h @ samples
 
 
# ----- Form B: the brick wall, applied to the spectrum ------------------
 
def ideal_lpf_fft(x, fs, fc):
    """Zero every rfft bin above fc. Same filter, exact on this record.
 
    Bin i sits at i*fs/len(x) - the length of the TIME record, not of
    the rfft output. irfft is given n=len(x) so odd-length records keep
    their length.
    """
    X = np.fft.rfft(np.asarray(x, dtype=float))
    freqs = np.arange(len(X)) * fs / len(x)
    X[freqs > fc] = 0.0
    return np.fft.irfft(X, n=len(x))
 
 
# ----- What the filter looks like ---------------------------------------
 
def lpf_impulse_response(fs, fc, t):
    """h(t) = (2*fc/fs)*sinc(2*fc*t), the inverse transform of the wall.
 
    Non-causal (it is non-zero for t < 0) and it decays only as 1/t.
    Both facts make it unrealizable in hardware - hence the ZOH and the
    first-order hold as practical stand-ins.
    """
    t = np.asarray(t, dtype=float)
    return (2 * fc / fs) * np.sinc(2 * fc * t)


# ---------------------------------------------------------------------------
# Everything below is provided. Do not modify.
# ---------------------------------------------------------------------------

def _check(label, got, expected, tol=1e-6):
    if isinstance(expected, (list, tuple, np.ndarray)):
        got_arr = np.array(sorted(got), dtype=float)
        exp_arr = np.array(sorted(expected), dtype=float)
        ok = (len(got_arr) == len(exp_arr)) and np.allclose(got_arr, exp_arr, atol=tol)
    elif isinstance(expected, bool):
        ok = (got == expected)
    else:
        ok = abs(got - expected) < tol
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {label}")
    print(f"         got:      {got}")
    print(f"         expected: {expected}")
    return ok


def main():
    total = 0
    passed = 0

    print("=" * 70)
    print("Template A - lowest_alias_partner")
    print("=" * 70)
    cases_a = [
        ((300, 1000), 700),
        ((100, 1000), 900),
        ((440, 8000), 7560),
        ((50, 400), 350),
        ((1200, 3000), 1800),
    ]
    for (f, fs), expected in cases_a:
        total += 1
        try:
            got = lowest_alias_partner(f, fs)
            passed += _check(f"f={f}, fs={fs}", got, expected)
        except NotImplementedError:
            print(f"  [TODO] f={f}, fs={fs} -- not implemented yet")

    print()
    print("=" * 70)
    print("Template B - nyquist_check")
    print("=" * 70)
    cases_b = [
        ((900, 1500), False),   # fs=1500 < 2*900=1800 -> aliasing
        ((3000, 10000), True),  # fs=10000 > 2*3000=6000 -> safe
        ((20000, 44100), True), # standard audio example
        ((5000, 9000), False),  # fs=9000 < 2*5000=10000 -> aliasing
    ]
    for (f_max, fs), expected in cases_b:
        total += 1
        try:
            got = nyquist_check(f_max, fs)
            passed += _check(f"f_max={f_max}, fs={fs}", got, expected)
        except NotImplementedError:
            print(f"  [TODO] f_max={f_max}, fs={fs} -- not implemented yet")

    print()
    print("=" * 70)
    print("Template C - reverse_alias_candidates")
    print("=" * 70)
    cases_c = [
        ((500, 8000, (7000, 9000)), [7500, 8500]),
        ((300, 4000, (3500, 4500)), [3700, 4300]),
        ((200, 1000, (0, 1000)), [200, 800]),
    ]
    for (f_obs, fs, f_range), expected in cases_c:
        total += 1
        try:
            got = reverse_alias_candidates(f_obs, fs, f_range)
            passed += _check(f"f_obs={f_obs}, fs={fs}, range={f_range}", got, expected)
        except NotImplementedError:
            print(f"  [TODO] f_obs={f_obs}, fs={fs}, range={f_range} -- not implemented yet")

    print()
    print("=" * 70)
    print("Template D - ideal_reconstruction_cutoff")
    print("=" * 70)
    cases_d = [
        ((3000, 10000), 5000),
        ((20000, 44100), 22050),
        ((900, 2000), 1000),
    ]
    for (f_max, fs), expected in cases_d:
        total += 1
        try:
            got = ideal_reconstruction_cutoff(f_max, fs)
            passed += _check(f"f_max={f_max}, fs={fs}", got, expected)
        except NotImplementedError:
            print(f"  [TODO] f_max={f_max}, fs={fs} -- not implemented yet")

    print()
    print("=" * 70)
    print("Template E - dft_bin_to_frequency")
    print("=" * 70)
    cases_e = [
        ((100, 1024, 8000), 781.25),
        ((900, 1024, 8000), -968.75),
        ((64, 512, 16000), 2000.0),
        ((480, 512, 16000), -1000.0),
    ]
    for (k, N, fs), expected in cases_e:
        total += 1
        try:
            got = dft_bin_to_frequency(k, N, fs)
            passed += _check(f"k={k}, N={N}, fs={fs}", got, expected)
        except NotImplementedError:
            print(f"  [TODO] k={k}, N={N}, fs={fs} -- not implemented yet")

    print()
    print("=" * 70)
    print(f"TOTAL: {passed} / {total} passed")
    print("=" * 70)
    
    
    fs, N = 1000.0, 500          # coherent for both tones: 25 and 150 cycles
    n = np.arange(N)
 
    # A signal with one tone to keep and one to remove.
    x = np.cos(2 * np.pi * 50 * n / fs) + 0.8 * np.cos(2 * np.pi * 300 * n / fs)
 
    y = ideal_lpf_fft(x, fs, fc=120.0)
    want = np.cos(2 * np.pi * 50 * n / fs)
    print("Form B - brick wall at 120 Hz")
    print(f"  max |output - pure 50 Hz tone| = {np.max(np.abs(y - want)):.2e}")
 
    # Reconstruction between the samples: 40 Hz sampled at 400 Hz,
    # rebuilt on a 10x finer grid.
    f, fs2, M = 40.0, 400.0, 300            # record lasts 0.75 s
    s = np.cos(2 * np.pi * f * np.arange(M) / fs2)
    t = np.linspace(0.35, 0.40, 200)        # well inside the record
    xr = ideal_lpf_sinc(s, fs2, t)
    print("Form A - sinc reconstruction between samples")
    print(f"  max |x_r(t) - cos(2*pi*40*t)| = "
          f"{np.max(np.abs(xr - np.cos(2 * np.pi * f * t))):.2e}")
 
    # The same sinc filter used as a real low-pass, cutoff 120 Hz.
    t2 = np.arange(N) / fs
    y2 = ideal_lpf_sinc(x, fs, t2, fc=120.0)
    interior = slice(100, N - 100)           # skip the truncated ends
    print("Form A - sinc used as a 120 Hz low-pass")
    print(f"  max |output - pure 50 Hz tone| (interior) = "
          f"{np.max(np.abs(y2[interior] - want[interior])):.2e}")
 
    # Why it is unrealizable: h(t) decays like 1/t.
    probes = np.array([0.0, 0.00625, 0.05208, 0.10208])
    h = lpf_impulse_response(fs, 120.0, probes)
    print("Impulse response h(t) at t = 0, 6.25, 52, 102 ms")
    print("  " + "  ".join(f"{v:+.4f}" for v in h))
    print("  (still non-zero 100 ms out, and non-zero for t < 0 as well)")


if __name__ == "__main__":
    main()
