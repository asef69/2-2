"""Sampling Practice Set II - REFERENCE SOLUTION.

Twenty-five stand-alone problems, each sized for about 25-30 minutes of work.
Each problem's docstrings state the contract; the notes explain why the
code is what it is.

Run with:  python sampling_solution.py
Expected output: 25 of 25 problems passed.
"""

import numpy as np
from fractions import Fraction


# ==========================================================================
# Problem 1 - Aliasing analyser: fold, partner, and tone identification
# ==========================================================================

def folded_frequency(f, fs):
    """Apparent baseband frequency of cos(2*pi*f*t) sampled at fs.

    Sampling hides f + k*fs AND -f + k*fs, so the apparent frequency is
    the distance from f to the NEAREST multiple of fs - not f % fs.
    700 Hz at fs = 1000 folds down to 300 Hz; 700 % 1000 would wrongly
    give 700. abs() drops the sign a cosine cannot see, so the result
    always lands in [0, fs/2]. Valid for any f >= 0.
    """
    f = float(f)
    fs = float(fs)
    return abs(f - fs * round(f / fs))


def alias_with_phase(f, phi, fs):
    """Smallest positive partner of cos(2*pi*f*t + phi), with its phase.

    Assumes 0 < f < fs/2, so the nearest partners are fs - f and fs + f
    and fs - f is the smaller. On that reflected branch the sampled
    angle runs backwards,

        2*pi*(fs - f)*n/fs + phi' = 2*pi*n - (2*pi*f*n/fs - phi'),

    and cos is even, so this equals cos(2*pi*f*n/fs - phi'). Matching
    the original forces phi' = -phi. Returns (f_alias, phi_alias) with
    the phase reported in [0, 2*pi). On the fs + f branch the phase
    would have stayed +phi instead.
    """
    return (fs - f, (-phi) % (2 * np.pi))


def identify_tone(x, fs):
    """Recover (A, f, phi) of a single cosine from its samples.

    For x[n] = A cos(2*pi*f*n/fs + phi) with f exactly on the DFT grid,
    the rfft puts all the energy in one bin with X[k] = (N/2)*A*exp(j*phi).
    So the amplitude is 2|X[k]|/N, the frequency is k*fs/N using the
    length of the TIME record (not the shorter rfft length), and the
    phase is the angle of that bin. Bin 0 is zeroed first so that a dc
    offset cannot win the argmax.

    Returns the apparent frequency: if the tone was above fs/2 the
    answer is the folded one, which is all the samples can tell you.
    """
    x = np.asarray(x, dtype=float)
    N = len(x)
    X = np.fft.rfft(x)
    mag = np.abs(X)
    mag[0] = 0.0
    k = int(np.argmax(mag))
    return (2.0 * np.abs(X[k]) / N, k * fs / N, float(np.angle(X[k])) % (2 * np.pi))


# ==========================================================================
# Problem 2 - Multi-tone sampling simulator and rate selection
# ==========================================================================

def sample_signal(components, fs, duration):
    """Sample a sum of cosines. components = [(A, f, phi), ...].

    Sample times are t_n = n/fs for n = 0 ... N-1 with N = int(duration*fs),
    the same convention used everywhere in this set. Returns (t, x).
    """
    N = int(duration * fs)
    t = np.arange(N) / fs
    x = np.zeros(N)
    for A, f, phi in components:
        x += A * np.cos(2 * np.pi * f * t + phi)
    return t, x


def apparent_components(components, fs):
    """What each component turns into after sampling: (A, f_app, phi_app).

    Fold f to the nearest multiple of fs. If the signed offset comes out
    negative the component has landed on the reflected branch, so the
    frequency is negated and - crucially - so is the phase, exactly as
    in alias_with_phase. Amplitude is untouched; phase is reported in
    [0, 2*pi). Order follows the input.
    """
    out = []
    for A, f, phi in components:
        m = round(f / fs)
        f_app = f - m * fs
        if f_app < 0:
            f_app = -f_app
            phi = -phi
        out.append((A, f_app, phi % (2 * np.pi)))
    return out


def min_rate_without_alias(components, candidate_rates):
    """Smallest candidate rate at which no component is corrupted.

    Two conditions, both needed: every component must sit strictly below
    fs/2 (nothing folded at all), and the apparent frequencies must stay
    distinct (no two components landing on the same baseband line, which
    would sum irrecoverably). Rounding before the set comparison stops
    float dust from reporting two equal values as distinct. Returns None
    if no candidate works.
    """
    for fs in sorted(candidate_rates):
        app = apparent_components(components, fs)
        f_app = [a[1] for a in app]
        if (all(c[1] < fs / 2 for c in components)
                and len(set(np.round(f_app, 9))) == len(f_app)):
            return fs
    return None


# ==========================================================================
# Problem 3 - Three reconstruction filters, measured against the truth
# ==========================================================================

def sinc_reconstruct(samples, fs, t):
    """Whittaker-Shannon interpolation: sum_n x[n]*sinc((t - n/fs)/T).

    np.sinc is the NORMALISED sinc, sin(pi*u)/(pi*u), so the argument is
    (t - n/fs)*fs with no extra factor of pi. Broadcasting t against n
    builds the whole len(t) x len(samples) weight matrix at once and one
    matrix-vector product does the sum; a nested Python loop is far too
    slow to be comfortable here.
    """
    n = np.arange(len(samples))
    t = np.atleast_1d(np.asarray(t, dtype=float))
    weights = np.sinc((t[:, None] - n[None, :] / fs) * fs)
    return weights @ np.asarray(samples, dtype=float)


def zoh_reconstruct(samples, fs, t):
    """Zero-order hold: hold the most recent sample (the DAC staircase).

    Sample n keeps full weight from n*T until (n+1)*T, so the output at
    t is sample floor(t*fs). The clip covers both ends: before t = 0 the
    output is x[0], at or past the last sample it stays x[N-1] instead
    of indexing off the array.
    """
    t = np.atleast_1d(np.asarray(t, dtype=float))
    idx = np.clip(np.floor(t * fs).astype(int), 0, len(samples) - 1)
    return np.asarray(samples, dtype=float)[idx]


def linear_reconstruct(samples, fs, t):
    """First-order hold: straight lines between adjacent samples.

    This is convolution with the triangular h1(t), which is what
    np.interp computes pointwise; np.interp also clamps to the endpoint
    values outside the record, which is the behaviour asked for. The
    only thing to get right is the sample-time grid n/fs.
    """
    t = np.atleast_1d(np.asarray(t, dtype=float))
    return np.interp(t, np.arange(len(samples)) / fs,
                     np.asarray(samples, dtype=float))


def compare_reconstructions(f, fs, duration, t):
    """Max absolute error of each reconstruction of a unit cosine.

    Sample cos(2*pi*f*t), rebuild it three ways, and compare against the
    exact cosine at the query times. Returns
    {"sinc": ..., "linear": ..., "zoh": ...}.

    The expected ordering is sinc < linear < zoh, which is the frequency
    picture read backwards: the ideal brick wall, then T*sinc**2 with
    its fast rolloff, then T*sinc with the worst image leakage. The sinc
    error is not zero only because the sum is truncated at the ends of a
    finite record.
    """
    _, x = sample_signal([(1.0, f, 0.0)], fs, duration)
    true = np.cos(2 * np.pi * f * np.asarray(t, dtype=float))
    return {
        "sinc": float(np.max(np.abs(sinc_reconstruct(x, fs, t) - true))),
        "linear": float(np.max(np.abs(linear_reconstruct(x, fs, t) - true))),
        "zoh": float(np.max(np.abs(zoh_reconstruct(x, fs, t) - true))),
    }


# ==========================================================================
# Problem 4 - The hold filters in the frequency domain
# ==========================================================================

def hold_magnitude(w, T, order):
    """|H(jw)| of the zero-order (order 0) or first-order (order 1) hold.

    H0(jw) = T*exp(-j*w*T/2)*sinc(w*T/2pi); the exponential is a pure
    delay of T/2 with unit modulus and drops out of the magnitude. The
    triangle h1 is h0 convolved with itself (up to 1/T), and convolution
    squares the transform, hence sinc**2. Accepts a scalar or an array.
    """
    s = np.abs(np.sinc(np.asarray(w, dtype=float) * T / (2 * np.pi)))
    return T * (s if order == 0 else s ** 2)


def droop_db(order):
    """In-band attenuation at w = ws/2 relative to dc, in dB.

    The ratio is scale-free, so evaluate at T = 1, where ws = 2*pi and
    the band edge is w = pi. There sinc(1/2) = 2/pi, giving about
    -3.92 dB for the ZOH and exactly twice that many dB for the FOH.
    """
    return 20 * np.log10(hold_magnitude(np.pi, 1.0, order)
                         / hold_magnitude(0.0, 1.0, order))


def image_leakage_db(order, T):
    """Image energy above ws/2 relative to baseband energy, in dB.

    Integrate |H(jw)|**2 over [0, ws/2] and over [ws/2, 2.5*ws] on the
    fixed grid np.linspace(0, 2.5*ws, 100001) with the trapezoid rule,
    and report 10*log10(image/baseband). This quantifies the second
    complaint about the holds: the gain outside the passband is not
    zero, so the spectral images leak into the analogue output. The FOH
    should come out roughly 6 dB better than the ZOH.
    """
    ws = 2 * np.pi / T
    w = np.linspace(0.0, 2.5 * ws, 100001)
    p = hold_magnitude(w, T, order) ** 2
    lo = w <= ws / 2
    hi = w >= ws / 2
    base = np.trapezoid(p[lo], w[lo])
    image = np.trapezoid(p[hi], w[hi])
    return 10 * np.log10(image / base)


def zoh_compensation_gain(f, fs):
    """Digital pre-emphasis that cancels the ZOH droop: 1/sinc(f/fs).

    Since w*T/(2*pi) = f/fs, the ZOH shapes the band by sinc(f/fs), so a
    filter with the reciprocal response flattens it. The gain is 1 at dc
    and about pi/2 at the band edge. Accepts a scalar or an array.
    """
    return 1.0 / np.sinc(np.asarray(f, dtype=float) / fs)


# ==========================================================================
# Problem 5 - The DFT grid, coherent sampling, and leakage
# ==========================================================================

def dft_bin_frequencies(N, fs):
    """Signed physical frequency of each of the N DFT bins.

    An N-point DFT samples one ws-wide period of the sampled spectrum,
    so bins past the halfway point are wrapped negative frequencies, not
    very high positive ones: k*fs/N for k <= N//2, (k-N)*fs/N above.
    """
    k = np.arange(N)
    return np.where(k > N / 2, k - N, k) * fs / N


def coherent_N(f, fs, Nmax):
    """Smallest record length that puts f exactly on a DFT bin.

    f lands on a bin when f*N/fs is an integer, so write f/fs as a
    fraction in lowest terms and read off its denominator. Using
    Fraction (rather than a float search) makes the answer exact.
    Returns None when that N exceeds Nmax.
    """
    r = (Fraction(f).limit_denominator(10 ** 6)
         / Fraction(fs).limit_denominator(10 ** 6))
    N = r.denominator
    return N if N <= Nmax else None


def leakage_fraction(f, fs, N):
    """Fraction of spectral energy that misses the peak bin.

    Sample cos(2*pi*f*t) for N points, take |rfft|**2, and return
    1 - max_bin/total. When the record is coherent (f*N/fs an integer)
    every period fits whole, the implicit periodic extension is
    continuous, and the answer is essentially 0. Otherwise the
    discontinuity at the wrap smears energy across all bins - spectral
    leakage - and the fraction is appreciable.
    """
    n = np.arange(N)
    x = np.cos(2 * np.pi * f * n / fs)
    p = np.abs(np.fft.rfft(x)) ** 2
    return float(1.0 - p.max() / p.sum())


# ==========================================================================
# Problem 6 - Copy geometry and bandpass (sub-Nyquist) sampling
# ==========================================================================

def spectral_copies(wM, ws, K):
    """Support of each spectral copy, plus an overlap flag.

    Sampling convolves X(jw) with an impulse train spaced ws apart, so a
    copy of [-wM, wM] lands at every k*ws. Returns the list of
    (low, high) pairs for k = -K ... K in that order, and True exactly
    when neighbours overlap. They stay apart when wM < ws - wM, which
    rearranges to ws > 2*wM, so aliasing is ws < 2*wM.
    """
    return ([(k * ws - wM, k * ws + wM) for k in range(-K, K + 1)],
            bool(ws < 2 * wM))


def valid_bandpass_rates(f1, f2):
    """Sub-Nyquist rate windows for a signal occupying [f1, f2].

    A bandpass signal need not be sampled above 2*f2 - only fast enough
    that the copies of the positive and negative bands interleave
    without collision. That happens for

        2*f2/(m+1) <= fs <= 2*f1/m,   m = 1 ... floor(f1/B),  B = f2-f1.

    Each m is one window; larger m means a slower rate and a tighter
    window. Windows with lo > hi are empty and dropped. The list is
    sorted ascending; the always-safe baseband region fs >= 2*f2 is not
    included, since it is unbounded.
    """
    B = f2 - f1
    m_max = int(np.floor(f1 / B)) if B > 0 else 0
    out = []
    for m in range(1, m_max + 1):
        lo = 2 * f2 / (m + 1)
        hi = 2 * f1 / m
        if lo <= hi:
            out.append((lo, hi))
    return sorted(out)


def bandpass_alias_free(f1, f2, fs):
    """True when fs is a usable rate for the band [f1, f2].

    Either fs falls inside one of the sub-Nyquist windows, or it is at
    or above the ordinary Nyquist rate 2*f2. A small tolerance keeps the
    window edges inclusive against float error.
    """
    for lo, hi in valid_bandpass_rates(f1, f2):
        if lo - 1e-12 <= fs <= hi + 1e-12:
            return True
    return bool(fs >= 2 * f2)


# ==========================================================================
# Problem 7 - Periodic signals: Fourier series, DFT bins, harmonic folding
# ==========================================================================

def synthesize(coeffs, N):
    """One period of x[n] = sum_k a_k exp(j*2*pi*k*n/N), n = 0 ... N-1.

    coeffs maps harmonic index k (possibly negative) to a possibly
    complex a_k. The result is complex in general; it is real exactly
    when a_(-k) is the conjugate of a_k.
    """
    n = np.arange(N)
    x = np.zeros(N, dtype=complex)
    for k, a in coeffs.items():
        x += a * np.exp(2j * np.pi * k * n / N)
    return x


def dft_from_series(coeffs, N):
    """Predicted N-point DFT of synthesize(coeffs, N): X[k] = N*a_k.

    Negative harmonics sit at the wrapped bin k % N - the same wrap as
    dft_bin_frequencies. Harmonics that collide after wrapping are
    accumulated, which is precisely how aliasing shows up in the bins,
    so += rather than = matters.
    """
    X = np.zeros(N, dtype=complex)
    for k, a in coeffs.items():
        X[k % N] += N * a
    return X


def recover_series(x, kset):
    """Read the Fourier-series coefficients back out: a_k = X[k % N]/N.

    The inverse of dft_from_series, valid when the signal is band-limited
    to the Nyquist band so no two harmonics share a bin. Returns a dict
    over the requested indices.
    """
    N = len(x)
    X = np.fft.fft(x)
    return {k: X[k % N] / N for k in kset}


def aliased_series(coeffs, N):
    """Where the harmonics end up when only N samples per period are taken.

    Harmonic k is indistinguishable from k + N, so fold k into
    (-N/2, N/2] by taking k % N and subtracting N when the result passes
    the halfway point. Coefficients that land on the same folded index
    ADD - that sum is the irreversible part of aliasing. Returns a dict
    keyed by folded index.
    """
    out = {}
    for k, a in coeffs.items():
        kk = k % N
        if kk > N / 2:
            kk -= N
        out[kk] = out.get(kk, 0) + a
    return out


# ==========================================================================
# Problem 8 - Decimation, with and without the anti-alias filter
# ==========================================================================

def decimation_alias(f, fs, M):
    """Apparent frequency after keeping every M-th sample, no filter.

    Decimation by M is just sampling at fs/M, so fold at the reduced
    rate. A tone comfortably below fs/2 can easily exceed fs/(2M) and
    fold - which is the whole reason decimators filter first.
    """
    return folded_frequency(f, fs / M)


def lowpass_fft(x, fs, fc):
    """Brick-wall low-pass by zeroing rfft bins above fc.

    Bin i of the rfft sits at i*fs/len(x) - note the length of the time
    record, not of the rfft output. irfft is given n=len(x) so the output
    length matches the input even when len(x) is odd.
    """
    X = np.fft.rfft(x)
    freqs = np.arange(len(X)) * fs / len(x)
    X[freqs > fc] = 0
    return np.fft.irfft(X, n=len(x))


def decimate(x, fs, M, antialias=True):
    """Keep every M-th sample, optionally filtering first.

    With antialias=True, remove everything above the new Nyquist
    frequency fs/(2*M) before throwing samples away; a tone above that
    edge is then simply gone. With antialias=False the same tone
    survives, folded onto decimation_alias(f, fs, M) - a false signal
    that no later processing can remove.
    """
    y = lowpass_fft(x, fs, fs / (2 * M)) if antialias else np.asarray(x, dtype=float)
    return y[::M]


# ==========================================================================
# Problem 9 - Upsampling: zero stuffing, images, and FFT interpolation
# ==========================================================================

def zero_stuff(x, L):
    """Insert L-1 zeros after every sample (rate L*fs, same spectrum).

    Zero stuffing does not change the spectrum's content at all; it only
    reinterprets it on a wider frequency axis, so the old copies at
    multiples of fs now appear as IMAGES inside the new baseband
    [0, L*fs/2]. Interpolation is what removes them.
    """
    y = np.zeros(len(x) * L)
    y[::L] = x
    return y


def interpolate_fft(x, L):
    """Ideal band-limited interpolation by L, done in the DFT domain.

    Take the rfft, place it at the bottom of a spectrum L times longer,
    leave the new high bins at zero (that zero region IS the ideal
    low-pass that kills the images), inverse transform at length N*L,
    and scale by L to undo numpy's 1/N normalisation. For a signal
    periodic in the record this reproduces the underlying continuous
    signal to machine precision.
    """
    N = len(x)
    X = np.fft.rfft(x)
    Y = np.zeros(N * L // 2 + 1, dtype=complex)
    Y[:len(X)] = X
    return np.fft.irfft(Y, n=N * L) * L


def image_frequencies(f, fs, L, fmax):
    """Image frequencies of a tone f after zero stuffing by L, up to fmax.

    The images are the old alias family k*fs +/- f, now sitting inside
    the wider band [0, L*fs/2]. Returns them sorted, excluding f itself.
    Walk k upward until even the lower branch k*fs - f passes fmax.
    """
    out = set()
    k = 0
    while True:
        for c in (k * fs + f, k * fs - f):
            if 0 < c <= fmax and abs(c - f) > 1e-12:
                out.add(round(c, 9))
        k += 1
        if k * fs - f > fmax:
            break
    return sorted(out)


# ==========================================================================
# Problem 10 - A real converter: quantisation noise and aperture jitter
# ==========================================================================

def quantize(x, bits, vref):
    """Uniform mid-tread quantiser on [-vref, vref) with 2**bits levels.

    Step size is the full range divided by the number of levels,
    2*vref/2**bits. Round to the nearest multiple of the step, then clip
    to the representable range so an input at +vref does not produce a
    code that does not exist.
    """
    step = 2.0 * vref / (2 ** bits)
    q = np.round(np.asarray(x, dtype=float) / step) * step
    return np.clip(q, -vref, vref - step)


def snr_db(clean, noisy):
    """10*log10(signal power / error power), with error = noisy - clean."""
    clean = np.asarray(clean, dtype=float)
    err = np.asarray(noisy, dtype=float) - clean
    return 10 * np.log10(np.sum(clean ** 2) / np.sum(err ** 2))


def theoretical_snr_db(bits):
    """The textbook full-scale sine figure, 6.02*bits + 1.76 dB.

    A measured value lands a couple of dB below this whenever the input
    does not use the full input range, since the quantisation noise is
    fixed by the step size while the signal power is not.
    """
    return 6.02 * bits + 1.76


def jitter_samples(f, fs, N, sigma, seed):
    """Sample cos(2*pi*f*t) at jittered times t_n = n/fs + e_n.

    e_n is Gaussian with standard deviation sigma, drawn from
    np.random.default_rng(seed) so the result is reproducible. Aperture
    jitter is a timing error, but it shows up as an amplitude error, and
    the faster the signal the worse it is.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(N) / fs + rng.normal(0.0, sigma, N)
    return np.cos(2 * np.pi * f * t)


def jitter_rms_bound(f, sigma):
    """Predicted rms sampling error from jitter: 2*pi*f*sigma/sqrt(2).

    For small e, the error is x'(t)*e = -2*pi*f*sin(2*pi*f*t)*e. The two
    factors are independent, sin contributes rms 1/sqrt(2) and e
    contributes sigma, giving this product. It grows linearly with f,
    which is why a fast converter needs a low-jitter clock far more than
    a slow one does.
    """
    return 2 * np.pi * f * sigma / np.sqrt(2)



# ==========================================================================
# Problem 11 - The moving-average anti-alias filter
# ==========================================================================

def ma_magnitude(w, L):
    """|H(e^jw)| of an L-point moving average, w in rad/sample.

    Summing L samples and dividing by L is a geometric series, giving
    the Dirichlet kernel |sin(wL/2) / (L*sin(w/2))|. At w = 0 both parts
    vanish; the limit is 1, so that case is special-cased rather than
    divided. Accepts a scalar or an array.
    """
    w = np.asarray(w, dtype=float)
    den = L * np.sin(w / 2)
    safe = np.where(np.abs(den) < 1e-12, 1.0, den)
    out = np.abs(np.sin(w * L / 2) / safe)
    return np.where(np.abs(den) < 1e-12, 1.0, out)


def ma_nulls(L, fs):
    """Physical frequencies (Hz) where the L-point average is exactly zero.

    The numerator sin(wL/2) vanishes at w = 2*pi*k/L, i.e. at k*fs/L for
    k = 1 ... L-1. Those nulls are why a length-M average is the cheapest
    possible anti-alias filter for decimation by M: the nulls land
    exactly on the frequencies that would fold onto dc.
    """
    return [k * fs / L for k in range(1, L)]


def decimate_ma(x, M):
    """Decimate by M after an M-point moving average.

    Use np.convolve(..., mode="same") with an M-point box so the output
    length matches the input before the M-fold downsample. It is a crude
    filter - the stopband is only about -13 dB at its worst - but the
    nulls are in the right places, and a tone that a brick wall would
    delete is at least heavily attenuated rather than folded at full
    strength.
    """
    x = np.asarray(x, dtype=float)
    y = np.convolve(x, np.ones(M) / M, mode="same")
    return y[::M]


# ==========================================================================
# Problem 12 - Sample-and-hold aperture effect
# ==========================================================================

def sh_magnitude(f, tau):
    """Amplitude an aperture of width tau leaves at frequency f.

    A real track-and-hold does not read an instant; it AVERAGES the
    input over an aperture of width tau. Averaging is convolution with a
    rectangle, whose transform is sinc(f*tau) - the same sinc as the
    ZOH, but set by the aperture rather than by the sample period.
    """
    return np.abs(np.sinc(np.asarray(f, dtype=float) * tau))


def sample_with_aperture(f, fs, N, tau, nsub):
    """Sample cos(2*pi*f*t) with a finite aperture, by numeric averaging.

    Sample n averages the input over [n/fs, n/fs + tau]; approximate the
    average with nsub midpoint samples inside the window. Broadcasting
    the N sample instants against the nsub offsets does it in one
    expression. Returns the N averaged samples.

    The recovered amplitude should match sh_magnitude(f, tau), and the
    recovered phase should be advanced by pi*f*tau, since averaging over
    a window also delays by half its width.
    """
    n = np.arange(N)[:, None]
    u = (np.arange(nsub)[None, :] + 0.5) / nsub * tau
    return np.mean(np.cos(2 * np.pi * f * (n / fs + u)), axis=1)


# ==========================================================================
# Problem 13 - Non-uniform samples, solved by least squares
# ==========================================================================

def design_matrix(times, freqs):
    """Columns [cos(2*pi*f*t) for f in freqs] then [sin(...) for f in freqs].

    Shape is (len(times), 2*len(freqs)). Splitting each tone into a
    cosine and a sine keeps the unknowns LINEAR - amplitude and phase
    are not, but the pair (a, b) in a*cos + b*sin is.
    """
    t = np.asarray(times, dtype=float)[:, None]
    f = np.asarray(freqs, dtype=float)[None, :]
    return np.hstack([np.cos(2 * np.pi * f * t), np.sin(2 * np.pi * f * t)])


def fit_tones(times, x, freqs):
    """Recover [(A, phi), ...] from samples taken at arbitrary times.

    Solve the least-squares system with np.linalg.lstsq, then convert
    each (a, b) pair back with A = hypot(a, b) and phi = atan2(-b, a) -
    the minus sign because a*cos + b*sin = A*cos(theta + phi) needs
    b = -A*sin(phi). Report phases in [0, 2*pi), in the order of freqs.

    Note what this buys you: the samples need not be uniform at all, so
    the Nyquist rate in its usual form does not apply. What matters is
    only that the system is well conditioned, i.e. enough samples,
    spread out, and the candidate frequencies not too close together.
    """
    A = design_matrix(times, freqs)
    c, *_ = np.linalg.lstsq(A, np.asarray(x, dtype=float), rcond=None)
    F = len(freqs)
    return [(float(np.hypot(c[i], c[i + F])),
             float(np.arctan2(-c[i + F], c[i]) % (2 * np.pi))) for i in range(F)]


# ==========================================================================
# Problem 14 - Sub-bin frequency estimation
# ==========================================================================

def parabolic_interpolate(mag, k):
    """Sub-bin offset of a peak, by fitting a parabola to three points.

    Through mag[k-1], mag[k], mag[k+1] there is exactly one parabola;
    its vertex sits at delta = 0.5*(a - c)/(a - 2b + c) bins from k.
    Returns delta, normally in (-0.5, 0.5).
    """
    a, b, c = float(mag[k - 1]), float(mag[k]), float(mag[k + 1])
    return 0.5 * (a - c) / (a - 2 * b + c)


def estimate_frequency(x, fs):
    """Frequency estimate finer than the fs/N bin spacing.

    Apply a Hann window first (a rectangular window's leakage pattern is
    too peaked for the parabola to fit well), take |rfft|, zero bin 0,
    find the peak bin k, refine it with parabolic_interpolate, and
    convert (k + delta)*fs/N. Fall back to delta = 0 if the peak is at
    either end, where no three-point fit exists.
    """
    x = np.asarray(x, dtype=float)
    N = len(x)
    w = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(N) / N)
    mag = np.abs(np.fft.rfft(x * w))
    mag[0] = 0.0
    k = int(np.argmax(mag))
    d = parabolic_interpolate(mag, k) if 0 < k < len(mag) - 1 else 0.0
    return (k + d) * fs / N


# ==========================================================================
# Problem 15 - Windows, leakage, and equivalent noise bandwidth
# ==========================================================================

def hann(N):
    """The periodic Hann window, 0.5 - 0.5*cos(2*pi*n/N), n = 0 ... N-1.

    Periodic (divide by N), not symmetric (divide by N-1): the periodic
    form is the one that belongs with the DFT.
    """
    return 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(N) / N)


def far_leakage(f, fs, N, window, guard=2):
    """Energy fraction landing more than `guard` bins from the peak.

    Window the tone, take |rfft|**2, and return the fraction of the
    total that falls outside bins [k-guard, k+guard]. The guard band is
    the point: a window does NOT reduce total spread - it widens the
    main lobe, so more energy sits in the immediate neighbours - but it
    cuts the FAR sidelobes enormously, and it is the far sidelobes that
    bury small tones next to large ones.
    """
    x = np.cos(2 * np.pi * f * np.arange(N) / fs) * np.asarray(window, dtype=float)
    p = np.abs(np.fft.rfft(x)) ** 2
    k = int(np.argmax(p))
    lo, hi = max(0, k - guard), min(len(p), k + guard + 1)
    return float(1.0 - p[lo:hi].sum() / p.sum())


def enbw(window):
    """Equivalent noise bandwidth in bins: N*sum(w**2)/sum(w)**2.

    How many bins' worth of white noise the window lets into one bin.
    It is exactly 1 for the rectangular window and exactly 1.5 for Hann
    - the price paid for the sidelobe suppression.
    """
    w = np.asarray(window, dtype=float)
    return float(len(w) * np.sum(w ** 2) / np.sum(w) ** 2)


# ==========================================================================
# Problem 16 - Measuring the ZOH images in a real staircase
# ==========================================================================

def stair_signal(samples, L):
    """The ZOH staircase, oversampled L times per sample (np.repeat).

    This is what a DAC actually emits, viewed on a grid fine enough that
    its spectrum can be examined: each sample held flat for L points at
    the rate L*fs.
    """
    return np.repeat(np.asarray(samples, dtype=float), L)


def zoh_image_ratio(f, fs, L, N):
    """Measured amplitude of the first image relative to the fundamental.

    Sample a cosine, build its staircase at rate L*fs, take the rfft,
    and compare the bin nearest fs - f with the bin nearest f. Build the
    frequency axis from the staircase length and its rate L*fs; the
    nearest-bin lookup keeps the result honest when the record is not
    perfectly coherent.
    """
    n = np.arange(N)
    y = stair_signal(np.cos(2 * np.pi * f * n / fs), L)
    Y = np.abs(np.fft.rfft(y))
    fr = np.arange(len(Y)) * (fs * L) / len(y)
    at = lambda target: Y[int(np.argmin(np.abs(fr - target)))]
    return float(at(fs - f) / at(f))


def zoh_image_ratio_theory(f, fs):
    """Predicted ratio, |sinc((fs - f)/fs)| / |sinc(f/fs)|.

    The staircase is the impulse train shaped by H0, so every image is
    the original line scaled by the sinc envelope evaluated at that
    image's frequency. Measurement and theory should agree within a few
    percent - the remaining gap is the finite record.
    """
    return float(np.abs(np.sinc((fs - f) / fs) / np.sinc(f / fs)))


# ==========================================================================
# Problem 17 - A chirp folding off the Nyquist wall
# ==========================================================================

def chirp_samples(f0, f1, dur, fs):
    """Linear chirp from f0 to f1 over dur seconds, sampled at fs.

    The instantaneous frequency is the DERIVATIVE of the phase, so the
    phase must be the integral: 2*pi*(f0*t + 0.5*rate*t**2) with
    rate = (f1 - f0)/dur. Writing 2*pi*f(t)*t instead is the classic
    error and sweeps at twice the intended rate. Returns (t, x).
    """
    N = int(dur * fs)
    t = np.arange(N) / fs
    rate = (f1 - f0) / dur
    return t, np.cos(2 * np.pi * (f0 * t + 0.5 * rate * t ** 2))


def instantaneous_frequency(f0, f1, dur, t):
    """The true instantaneous frequency f0 + (f1 - f0)*t/dur."""
    return f0 + (f1 - f0) * np.asarray(t, dtype=float) / dur


def apparent_instantaneous(f0, f1, dur, fs, t):
    """What the sampled chirp appears to do: the fold, applied pointwise.

    Once the sweep crosses fs/2 the apparent tone turns around and comes
    back down, then bounces again at 0 - the audible "folding" of an
    under-sampled sweep. Must work for an array of times, so use the
    vectorised fold rather than a Python loop.
    """
    f = instantaneous_frequency(f0, f1, dur, t)
    return np.abs(f - fs * np.round(f / fs))


# ==========================================================================
# Problem 18 - Complex (IQ) sampling: wrapping instead of folding
# ==========================================================================

def complex_fold(f, fs):
    """Apparent frequency of exp(j*2*pi*f*t) sampled at fs, in (-fs/2, fs/2].

    A complex exponential has a one-sided spectrum, so nothing reflects:
    frequencies simply WRAP modulo fs, keeping their sign. The shift
    trick ((f + fs/2) % fs) - fs/2 puts the result in the right half-open
    interval in one line. Compare with folded_frequency: 700 Hz at
    fs = 1000 is +300 for a real cosine but -300 here, and that sign is
    real information an IQ receiver can use.
    """
    return ((float(f) + fs / 2) % fs) - fs / 2


def identify_complex_tone(z, fs):
    """Signed frequency of a complex tone, from the full (not real) FFT.

    Use np.fft.fft, take the argmax bin, and unwrap indices above N/2 to
    negative ones before converting to hertz. rfft would be wrong here:
    it assumes a real signal and throws away exactly the sign this
    problem is about.
    """
    N = len(z)
    k = int(np.argmax(np.abs(np.fft.fft(z))))
    if k > N / 2:
        k -= N
    return k * fs / N


# ==========================================================================
# Problem 19 - Nyquist zones and spectral inversion
# ==========================================================================

def nyquist_zone(f, fs):
    """Which Nyquist zone f lives in, counting from 1.

    The zones are [0, fs/2), [fs/2, fs), [fs, 3fs/2), ... so the answer
    is floor(f/(fs/2)) + 1.
    """
    return int(np.floor(f / (fs / 2))) + 1


def zone_inverts(zone):
    """True when a zone lands on the sampled axis reversed.

    Even zones arrive mirrored - a rising tone there appears to fall.
    This is what makes bandpass sampling usable in practice: the
    inversion is predictable, so it can be undone.
    """
    return zone % 2 == 0


def true_frequency(f_app, zone, fs):
    """Undo the fold, given the apparent frequency and the known zone.

    Odd zones: (zone-1)*fs/2 + f_app. Even zones: zone*fs/2 - f_app,
    because of the inversion. Sampling alone cannot tell you the zone -
    that has to come from the analogue bandpass filter in front of the
    converter, which is the whole design idea.
    """
    if zone % 2 == 1:
        return (zone - 1) * fs / 2 + f_app
    return zone * fs / 2 - f_app


# ==========================================================================
# Problem 20 - How reconstruction error scales with oversampling
# ==========================================================================

def reconstruction_error(f, fs, dur, t, method):
    """Max absolute error of one reconstruction method against the truth.

    method is "sinc", "linear" or "zoh". Sample a unit cosine for dur
    seconds at fs, rebuild, and compare at the times t.
    """
    _, x = sample_signal([(1.0, f, 0.0)], fs, dur)
    true = np.cos(2 * np.pi * f * np.asarray(t, dtype=float))
    fn = {"sinc": sinc_reconstruct, "linear": linear_reconstruct,
          "zoh": zoh_reconstruct}[method]
    return float(np.max(np.abs(fn(x, fs, t) - true)))


def error_slope(f, osr_list, method):
    """Log-log slope of error against oversampling ratio.

    For each OSR in osr_list sample at fs = OSR*2*f (so OSR = 1 is the
    Nyquist rate), measure the error over one period well inside the
    record, and fit a straight line through log(error) vs log(OSR) with
    np.polyfit.

    Predict the answers first from the Taylor error of each
    interpolator: the ZOH is first-order accurate, so slope about -1
    (error halves when the rate doubles), and linear interpolation is
    second-order, so slope about -2 (error quarters). This is the
    quantitative version of "oversample and a cheap reconstruction will
    do".
    """
    t = np.linspace(2 / f, 3 / f, 200)
    e = [reconstruction_error(f, o * 2 * f, 6 / f, t, method) for o in osr_list]
    return float(np.polyfit(np.log(osr_list), np.log(e), 1)[0])


# ==========================================================================
# Problem 21 - Parseval and band power on the DFT grid
# ==========================================================================

def parseval_error(x):
    """|sum x[n]**2 - sum |X[k]|**2 / N| : should be float noise.

    Parseval's relation for the DFT carries a 1/N because numpy puts no
    normalisation in the forward transform. Getting this to ~1e-13 is
    the cheapest possible check that your transform conventions are
    right before you trust any power number computed from them.
    """
    x = np.asarray(x, dtype=float)
    X = np.fft.fft(x)
    return float(abs(np.sum(x ** 2) - np.sum(np.abs(X) ** 2) / len(x)))


def band_power(x, fs, flo, fhi):
    """Average power of x in the band [flo, fhi], from the DFT.

    Use the full fft and np.fft.fftfreq so that BOTH the positive and
    the negative bins of the band are counted - a real tone splits its
    power between them - and divide by N**2 to turn the sum into average
    power. A unit-amplitude cosine inside the band must give exactly
    0.5, which is the test worth doing first.
    """
    x = np.asarray(x, dtype=float)
    N = len(x)
    X = np.fft.fft(x)
    fr = np.fft.fftfreq(N, 1 / fs)
    m = (np.abs(fr) >= flo) & (np.abs(fr) <= fhi)
    return float(np.sum(np.abs(X[m]) ** 2) / N ** 2)


# ==========================================================================
# Problem 22 - Truncating the sinc: how many neighbours are enough
# ==========================================================================

def truncated_sinc_reconstruct(samples, fs, t, K):
    """Whittaker-Shannon using only samples within K of the query time.

    Build the matrix of distances d = t*fs - n in SAMPLE units, keep
    np.sinc(d) where |d| <= K and zero elsewhere, then the same
    matrix-vector product as the full version. No Python loop needed.

    The point of the exercise: the ideal filter is unrealizable because
    the sinc has infinite support and decays only as 1/t, so the error
    falls off slowly with K - roughly like 1/K. Compare a few values of
    K and see for yourself how expensive "ideal" really is.
    """
    samples = np.asarray(samples, dtype=float)
    n = np.arange(len(samples))
    t = np.atleast_1d(np.asarray(t, dtype=float))
    d = t[:, None] * fs - n[None, :]
    W = np.where(np.abs(d) <= K, np.sinc(d), 0.0)
    return W @ samples


# ==========================================================================
# Problem 23 - Rational rate conversion by L/M
# ==========================================================================

def resample_rational(x, L, M):
    """Change the rate by the factor L/M: interpolate by L, decimate by M.

    Upsampling must come FIRST. Doing it the other way risks throwing
    away information that the interpolation could have kept, and can
    alias irreversibly. Here the interpolation is the exact FFT one from
    Problem 9, so for a signal periodic in the record the conversion is
    exact; a practical resampler substitutes a polyphase FIR for it.

    Requires L*len(x)/M to be a whole number to land on a clean grid.
    """
    return interpolate_fft(x, L)[::M]


# ==========================================================================
# Problem 24 - Reading amplitudes off a real spectrum correctly
# ==========================================================================

def real_spectrum_amplitudes(x, fs):
    """(freqs, amplitudes) of a real record, with dc and Nyquist handled.

    A real cosine at an interior bin splits its energy between +k and
    -k, so its amplitude is 2|X[k]|/N. The dc bin has no partner, and
    for even N neither does the Nyquist bin - both take |X|/N with NO
    factor of two. Doubling them is one of the most common ways a
    perfectly good spectrum ends up 6 dB wrong at the edges.

    Returns the rfft bin frequencies and the matching amplitudes.
    """
    x = np.asarray(x, dtype=float)
    N = len(x)
    X = np.fft.rfft(x)
    A = 2 * np.abs(X) / N
    A[0] = np.abs(X[0]) / N
    if N % 2 == 0:
        A[-1] = np.abs(X[-1]) / N
    return np.arange(len(A)) * fs / N, A


# ==========================================================================
# Problem 25 - The stroboscopic (wagon-wheel) effect
# ==========================================================================

def wheel_apparent_rate(rot_hz, frame_hz):
    """Apparent rotation rate of a wheel filmed at frame_hz, signed.

    Rotation is genuinely a complex phasor - it has a direction - so
    this is the complex wrap of Problem 18, not the real fold: the
    answer lies in (-frame_hz/2, frame_hz/2] and keeps its sign. A wheel
    at 29 rev/s filmed at 30 fps appears to turn BACKWARDS at 1 rev/s.
    """
    return complex_fold(rot_hz, frame_hz)


def strobe_direction(rot_hz, frame_hz):
    """+1 forwards, -1 backwards, 0 frozen - the sign of the apparent rate.

    Zero is the strobe condition: the wheel is an exact multiple of the
    frame rate, every frame catches it in the same place, and it appears
    to stand still no matter how fast it is really going.
    """
    return int(np.sign(wheel_apparent_rate(rot_hz, frame_hz)))


# ==========================================================================
# PROVIDED TEST HARNESS - do not modify anything below this line.
# ==========================================================================

def _p1():
    n = np.arange(50)
    fa, pa = alias_with_phase(300, 0.7, 1000)
    x = np.cos(2 * np.pi * 125 * np.arange(256) / 1000 + 0.4)
    A, f, phi = identify_tone(x, 1000)
    return (np.isclose(folded_frequency(1200, 1000), 200)
            and np.isclose(folded_frequency(700, 1000), 300)
            and np.isclose(folded_frequency(2000, 1000), 0)
            and 0 <= pa < 2 * np.pi
            and np.allclose(np.cos(2 * np.pi * 300 * n / 1000 + 0.7),
                            np.cos(2 * np.pi * fa * n / 1000 + pa))
            and np.isclose(A, 1.0, atol=1e-6) and np.isclose(f, 125.0)
            and np.isclose(phi, 0.4, atol=1e-6))


def _p2():
    t, x = sample_signal([(2.0, 100, 0.0)], 1000, 0.05)
    app = apparent_components([(1.0, 700, 0.5), (1.0, 100, 0.25)], 1000)
    best = min_rate_without_alias([(1, 100, 0), (1, 300, 0)], [400, 700, 900])
    return (len(x) == 50 and np.isclose(t[1], 0.001) and np.isclose(x[0], 2.0)
            and np.isclose(app[0][1], 300)
            and np.isclose(app[0][2], (-0.5) % (2 * np.pi))
            and np.isclose(app[1][1], 100) and np.isclose(app[1][2], 0.25)
            and best == 700)


def _p3():
    t = np.linspace(2.0, 3.0, 60)
    e = compare_reconstructions(3.0, 40.0, 5.0, t)
    return (e["sinc"] < 0.01 and e["sinc"] < e["linear"] < e["zoh"]
            and e["zoh"] > 0.3)


def _p4():
    return (np.isclose(droop_db(0), 20 * np.log10(2 / np.pi))
            and np.isclose(droop_db(1), 40 * np.log10(2 / np.pi))
            and np.isclose(hold_magnitude(0.0, 2.0, 0), 2.0)
            and np.isclose(image_leakage_db(0, 1.0), -6.20, atol=0.15)
            and np.isclose(image_leakage_db(1, 1.0), -12.79, atol=0.15)
            and np.isclose(zoh_compensation_gain(0.0, 1000), 1.0)
            and np.isclose(zoh_compensation_gain(500.0, 1000), np.pi / 2))


def _p5():
    return (np.allclose(dft_bin_frequencies(8, 800),
                        [0, 100, 200, 300, 400, -300, -200, -100])
            and coherent_N(250, 1000, 4096) == 4
            and coherent_N(253, 1000, 4096) == 1000
            and coherent_N(253, 1000, 100) is None
            and leakage_fraction(250, 1000, 64) < 1e-9
            and leakage_fraction(253, 1000, 64) > 0.05)


def _p6():
    cps, al = spectral_copies(2.0, 10.0, 1)
    _, al2 = spectral_copies(6.0, 10.0, 1)
    wins = valid_bandpass_rates(100.0, 140.0)
    return (tuple(cps[0]) == (-12.0, -8.0) and tuple(cps[1]) == (-2.0, 2.0)
            and al is False and al2 is True
            and len(wins) == 2
            and np.allclose(wins[0], (280 / 3, 100.0))
            and np.allclose(wins[1], (140.0, 200.0))
            and bandpass_alias_free(100.0, 140.0, 150.0) is True
            and bandpass_alias_free(100.0, 140.0, 120.0) is False
            and bandpass_alias_free(100.0, 140.0, 300.0) is True)


def _p7():
    c = {0: 1.0, 1: 0.5, -1: 0.5, 3: 0.25j}
    x = synthesize(c, 16)
    rec = recover_series(x, [1, -1, 3])
    al = aliased_series({1: 1.0, 9: 2.0, 5: 1.0}, 8)
    return (np.max(np.abs(np.fft.fft(x) - dft_from_series(c, 16))) < 1e-9
            and abs(rec[1] - 0.5) < 1e-9 and abs(rec[3] - 0.25j) < 1e-9
            and abs(al[1] - 3.0) < 1e-12 and abs(al[-3] - 1.0) < 1e-12)


def _p8():
    n = np.arange(400)
    x300 = np.cos(2 * np.pi * 300 * n / 1000)
    x50 = np.cos(2 * np.pi * 50 * n / 1000)
    y_bad = decimate(x300, 1000, 4, antialias=False)
    y_good = decimate(x300, 1000, 4, antialias=True)
    y_keep = decimate(x50, 1000, 4, antialias=True)
    _, f_bad, _ = identify_tone(y_bad, 250)
    return (np.isclose(decimation_alias(300, 1000, 4), 50)
            and np.isclose(decimation_alias(100, 1000, 2), 100)
            and len(y_bad) == 100 and np.isclose(f_bad, 50.0, atol=3)
            and np.max(np.abs(y_good)) < 1e-6
            and np.max(np.abs(y_keep)) > 0.9)


def _p9():
    x = np.cos(2 * np.pi * 4 * np.arange(64) / 64)
    z = zero_stuff(x, 4)
    up = interpolate_fft(x, 4)
    truth = np.cos(2 * np.pi * 4 * np.arange(256) / 256)
    imgs = image_frequencies(300.0, 1000.0, 4, 2000.0)
    return (len(z) == 256 and np.isclose(z[0], x[0]) and z[1] == 0
            and np.max(np.abs(up - truth)) < 1e-9
            and imgs == [700.0, 1300.0, 1700.0])


def _p10():
    n = np.arange(4096)
    clean = np.cos(2 * np.pi * 50 * n / 1000)
    q = quantize(clean, 10, 1.05)
    measured = snr_db(clean, q)
    jit = jitter_samples(50, 1000, 4000, 1e-4, 7)
    err = jit - np.cos(2 * np.pi * 50 * np.arange(4000) / 1000)
    rms = np.sqrt(np.mean(err ** 2))
    return (np.isclose(theoretical_snr_db(10), 61.96, atol=0.01)
            and 55 < measured < theoretical_snr_db(10)
            and np.isclose(rms, jitter_rms_bound(50, 1e-4), rtol=0.15)
            and np.max(np.abs(quantize([0.0], 8, 1.0))) < 1e-12)




def _p11():
    x = np.cos(2 * np.pi * 300 * np.arange(400) / 1000)
    return (np.isclose(ma_magnitude(0.0, 4), 1.0)
            and abs(float(ma_magnitude(np.pi / 2, 4))) < 1e-9
            and ma_nulls(4, 1000) == [250.0, 500.0, 750.0]
            and len(decimate_ma(x, 4)) == 100
            and np.max(np.abs(decimate_ma(x, 4))) < 0.4)


def _p12():
    y = sample_with_aperture(300, 1000, 100, 1e-3, 400)
    A, f, phi = identify_tone(y, 1000)
    return (np.isclose(A, sh_magnitude(300, 1e-3), rtol=1e-3)
            and np.isclose(f, 300.0)
            and np.isclose(phi, (np.pi * 300 * 1e-3) % (2 * np.pi), atol=1e-3)
            and np.isclose(sh_magnitude(0.0, 1e-3), 1.0))


def _p13():
    t = np.sort(np.random.default_rng(1).uniform(0, 1, 200))
    x = 1.5 * np.cos(2 * np.pi * 3 * t + 0.4) + 0.7 * np.cos(2 * np.pi * 11 * t)
    D = design_matrix(t, [3, 11])
    fit = fit_tones(t, x, [3, 11])
    return (D.shape == (200, 4)
            and np.isclose(fit[0][0], 1.5, atol=1e-6)
            and np.isclose(fit[0][1], 0.4, atol=1e-6)
            and np.isclose(fit[1][0], 0.7, atol=1e-6))


def _p14():
    x = np.cos(2 * np.pi * 253.3 * np.arange(512) / 1000)
    mag = np.array([1.0, 3.0, 2.0])
    return (np.isclose(parabolic_interpolate(mag, 1), 1 / 6)
            and np.isclose(estimate_frequency(x, 1000), 253.3, atol=0.3))


def _p15():
    w = hann(64)
    return (np.isclose(w[0], 0.0) and np.isclose(enbw(np.ones(64)), 1.0)
            and np.isclose(enbw(w), 1.5, atol=1e-9)
            and far_leakage(253, 1000, 64, w) < 0.01 * far_leakage(253, 1000, 64, np.ones(64)))


def _p16():
    s = stair_signal([1.0, 2.0], 3)
    return (list(s) == [1, 1, 1, 2, 2, 2]
            and np.isclose(zoh_image_ratio(100, 1000, 8, 256),
                           zoh_image_ratio_theory(100, 1000), rtol=0.1)
            and np.isclose(zoh_image_ratio_theory(100, 1000), 1 / 9, rtol=1e-6))


def _p17():
    t, x = chirp_samples(0.0, 800.0, 0.5, 1000.0)
    app = apparent_instantaneous(0.0, 800.0, 0.5, 1000.0, [0.25, 0.4375])
    return (len(x) == 500
            and np.isclose(instantaneous_frequency(0, 800, 0.5, 0.25), 400)
            and np.isclose(app[0], 400.0) and np.isclose(app[1], 300.0))


def _p18():
    z = np.exp(2j * np.pi * 700 * np.arange(250) / 1000)
    return (np.isclose(complex_fold(700, 1000), -300.0)
            and np.isclose(complex_fold(300, 1000), 300.0)
            and np.isclose(complex_fold(1300, 1000), 300.0)
            and np.isclose(identify_complex_tone(z, 1000), -300.0, atol=2.0))


def _p19():
    return (nyquist_zone(700, 1000) == 2 and nyquist_zone(300, 1000) == 1
            and nyquist_zone(1200, 1000) == 3
            and zone_inverts(2) is True and zone_inverts(3) is False
            and np.isclose(true_frequency(300, 2, 1000), 700)
            and np.isclose(true_frequency(200, 3, 1000), 1200))


def _p20():
    s_zoh = error_slope(5.0, [2, 4, 8, 16], "zoh")
    s_lin = error_slope(5.0, [2, 4, 8, 16], "linear")
    return (-1.35 < s_zoh < -0.6 and -2.35 < s_lin < -1.5 and s_lin < s_zoh)


def _p21():
    x = np.cos(2 * np.pi * 50 * np.arange(1000) / 1000)
    return (parseval_error(x) < 1e-9
            and np.isclose(band_power(x, 1000, 40, 60), 0.5, atol=1e-9)
            and band_power(x, 1000, 100, 200) < 1e-12)


def _p22():
    _, x = sample_signal([(1.0, 3.0, 0.0)], 40.0, 5.0)
    t = np.linspace(2.0, 3.0, 40)
    true = np.cos(2 * np.pi * 3 * t)
    e5 = np.max(np.abs(truncated_sinc_reconstruct(x, 40, t, 5) - true))
    e60 = np.max(np.abs(truncated_sinc_reconstruct(x, 40, t, 60) - true))
    e_all = np.max(np.abs(truncated_sinc_reconstruct(x, 40, t, 500) - true))
    full = np.max(np.abs(sinc_reconstruct(x, 40, t) - true))
    return (e5 > 5 * e60 and e60 > e_all and np.isclose(e_all, full, atol=1e-9))


def _p23():
    x = np.cos(2 * np.pi * 4 * np.arange(64) / 64)
    y = resample_rational(x, 3, 2)
    return (len(y) == 96
            and np.max(np.abs(y - np.cos(2 * np.pi * 4 * np.arange(96) / 96))) < 1e-9)


def _p24():
    n = np.arange(100)
    x = 2.0 + 1.0 * np.cos(2 * np.pi * 100 * n / 1000 + 0.3) + 0.5 * np.cos(np.pi * n)
    fr, A = real_spectrum_amplitudes(x, 1000)
    return (np.isclose(A[0], 2.0, atol=1e-9)
            and np.isclose(A[int(np.argmin(np.abs(fr - 100)))], 1.0, atol=1e-9)
            and np.isclose(A[-1], 0.5, atol=1e-9))


def _p25():
    return (np.isclose(wheel_apparent_rate(29, 30), -1.0)
            and np.isclose(wheel_apparent_rate(31, 30), 1.0)
            and np.isclose(wheel_apparent_rate(60, 30), 0.0)
            and strobe_direction(29, 30) == -1
            and strobe_direction(31, 30) == 1
            and strobe_direction(60, 30) == 0)


CHECKS = [
    ("P1  aliasing analyser", _p1),
    ("P2  multi-tone sampler", _p2),
    ("P3  reconstruction filters", _p3),
    ("P4  hold filters in frequency", _p4),
    ("P5  DFT grid and leakage", _p5),
    ("P6  bandpass sampling", _p6),
    ("P7  periodic signals and DFT", _p7),
    ("P8  decimation", _p8),
    ("P9  upsampling", _p9),
    ("P10 quantisation and jitter", _p10),
    ("P11 moving-average anti-alias", _p11),
    ("P12 sample-and-hold aperture", _p12),
    ("P13 non-uniform least squares", _p13),
    ("P14 sub-bin frequency estimate", _p14),
    ("P15 windows and leakage", _p15),
    ("P16 measured ZOH images", _p16),
    ("P17 chirp folding", _p17),
    ("P18 complex (IQ) sampling", _p18),
    ("P19 Nyquist zones", _p19),
    ("P20 error vs oversampling", _p20),
    ("P21 Parseval and band power", _p21),
    ("P22 truncated sinc", _p22),
    ("P23 rational resampling", _p23),
    ("P24 real spectrum amplitudes", _p24),
    ("P25 stroboscopic effect", _p25),
]


def main():
    print(f"{'problem':<32} result")
    print("-" * 44)
    passed = 0
    for name, fn in CHECKS:
        try:
            ok = bool(fn())
        except Exception as exc:
            ok = False
            print(f"{name:<32} ERROR  ({type(exc).__name__}: {exc})")
            continue
        passed += ok
        print(f"{name:<32} {'PASS' if ok else 'FAIL'}")
    print("-" * 44)
    print(f"{passed} of {len(CHECKS)} problems passed.")


if __name__ == "__main__":
    main()
