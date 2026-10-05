"""
transforms.py  --  YOUR CODE GOES HERE.

The shared transform core used by BOTH tasks. Write it once; bigmul.py
(Task A) and image_conv.py (Task B) import it.

Nothing in this file may call numpy.fft, scipy.fft, numpy.convolve,
scipy.signal, or any other library routine that performs a Fourier
transform, a convolution or a correlation for you. NumPy is for array
arithmetic only.

A quick self-test you should run before touching either application:

    import numpy as np
    from transforms import DFTAnalyzer, FFTTransformer
    x = np.random.randn(64) + 1j * np.random.randn(64)
    d, f = DFTAnalyzer(), FFTTransformer()
    assert np.max(np.abs(d.transform(x) - f.transform(x))) < 1e-9
    assert np.max(np.abs(d.inverse(d.transform(x)) - x)) < 1e-9
"""

import numpy as np #type:ignore


def next_power_of_two(n):
    """
    Return the smallest power of two that is >= ``n`` (and at least 1).

    Both tasks need this to choose a transform length for the radix-2 FFT.
    """
    if n<=1:
        return 1
    
    return 1<<(n-1).bit_length()


class DFTAnalyzer:
    """
    The Discrete Fourier Transform, computed straight from its definition.

        Analysis:   X[k] = sum_{n=0}^{N-1} x[n] * exp(-2j*pi*k*n/N)
        Synthesis:  x[n] = (1/N) * sum_{k=0}^{N-1} X[k] * exp(+2j*pi*k*n/N)

    How you write it is up to you -- a literal double loop, a precomputed
    table of twiddle factors indexed by (k*n) % N, or a NumPy expression --
    as long as it computes these sums directly and is not secretly an FFT.
    """

    name = "dft"

    def transform(self, x):
        """
        Forward DFT.

        Parameters
        ----------
        x : 1D array_like, length N (real or complex)

        Returns
        -------
        numpy.ndarray of complex128, shape (N,)
        """
        x=np.asarray(x,dtype=np.complex128)
        N=x.shape[0]
        
        n=np.arange(N)
        k=n.reshape((N,1))
        W=np.exp(-2j*np.pi*k*n/N)
        
        return W@x

    def inverse(self, spectrum):
        """
        Inverse DFT, including the 1/N factor.

        Parameters
        ----------
        spectrum : 1D array_like, length N (complex)

        Returns
        -------
        numpy.ndarray of complex128, shape (N,)
            Do NOT discard the imaginary part here -- the caller decides when
            it is safe to take .real.
        """
        spectrum=np.asarray(spectrum,dtype=np.complex128)
        N=spectrum.shape[0]
        
        n=np.arange(N)
        k=n.reshape((N,1))
        W=np.exp(2j*np.pi*k*n/N)
        return (W@spectrum)/N


class FFTTransformer(DFTAnalyzer):
    """
    Radix-2 decimation-in-time (Cooley-Tukey) FFT, in O(N log N).

    It inherits from DFTAnalyzer so that both applications can treat the two
    interchangeably: they call ``engine.transform(...)`` and
    ``engine.inverse(...)`` without caring which engine they hold.

    Requirements:
      * Recursive or iterative (with bit-reversal permutation) -- your choice.
      * N must be a power of two; raise ValueError for any other length.
        The caller is responsible for zero-padding up to next_power_of_two.
      * The inverse must reuse the same butterfly machinery (conjugated
        twiddles, or conjugate-transform-conjugate), not a second copy of it.
      * Twiddle factors for a stage are computed once per stage, never once
        per butterfly.
    """
    
    @staticmethod
    def bit_reversal_permutation(N):
        num_bits=N.bit_length()-1
        idx=np.arange(N,dtype=np.int64)
        rev=np.zeros(N,dtype=np.int64)
        for _ in range(num_bits):
            rev=(rev<<1)|(idx&1)
            idx>>=1
        return rev 
    
    def fft(self,data,invert):
        a=np.asarray(data,dtype=np.complex128)
        N=a.shape[0]
        if N==0 or  (N & (N-1))!=0:
            raise ValueError("FFT length must be a power of two but we got %d"%N)
        
        a=a[self.bit_reversal_permutation(N)].copy()
        
        sign=1.0 if invert else -1.0
        
        length=2
        
        while length<=N:
            half=length//2
            twiddle_factor=np.exp(sign*2j*np.pi*np.arange(half)/length)
            blocks = a.reshape(-1, length)
            even = blocks[:, :half].copy()
            odd = blocks[:, half:]
            t = odd * twiddle_factor
            blocks[:, :half] = even + t
            blocks[:, half:] = even - t
            length*=2
        
        if invert:
            a/=N
        
        return a               

    name = "fft"

    def transform(self, x):
        """Forward FFT. Same contract as DFTAnalyzer.transform."""
        return self.fft(x,invert=False)

    def inverse(self, spectrum):
        """Inverse FFT, including the 1/N factor."""
        return self.fft(spectrum,invert=True)


# ---------------------------------------------------------------------------
# BONUS (optional) -- arbitrary-length FFT.
#
# Delete this class if you are not attempting the bonus. If you do attempt it,
# run both tasks with --engine arbitrary and leave those output directories in
# your submission as the evidence.
# ---------------------------------------------------------------------------
class ArbitraryLengthFFT(FFTTransformer):
    """
    Bonus: an O(N log N) transform for ANY length N, not just powers of two.

    Bluestein's chirp-z algorithm is the usual route: rewrite the DFT as a
    convolution of two chirp sequences, and evaluate that convolution with a
    radix-2 FFT of length >= 2N-1. A mixed-radix Cooley-Tukey that factorises
    N is equally acceptable.

    With this engine, Task A no longer has to pad the digit arrays up to a
    power of two, and Task B no longer has to pad the image up to one.
    """
    
    """
        Learnt it from LLM:
        Bluestein's chirp-z transform: compute a length-N DFT (or, with
        invert=True, an inverse DFT including the 1/N factor) for ANY N,
        by rewriting it as a convolution and evaluating that convolution
        with the radix-2 FFT machinery already built in FFTTransformer
        (self._fft_core), reused rather than duplicated.
 
        Identity used:  k*n = (k^2 + n^2 - (k-n)^2) / 2, so
 
            exp(-2j*pi*k*n/N) = exp(-j*pi*k^2/N) * exp(-j*pi*n^2/N)
                                * exp(+j*pi*(k-n)^2/N)
 
        Setting a[n] = x[n]*exp(-j*pi*n^2/N) and b[m] = exp(+j*pi*m^2/N)
        (for m ranging over -(N-1)..N-1), the sum over n becomes the linear
        convolution (a * b)[k], and X[k] = exp(-j*pi*k^2/N) * (a*b)[k].
        The inverse just flips the sign of every exponent and divides by N.
        """

    name = "arbitrary"
    
    
    def algorithm(self,data,invert):
        x = np.asarray(data, dtype=np.complex128)
        N = x.shape[0]
        if N <= 1:
            return x.copy()
        sign=1.0 if invert else -1.0
        n = np.arange(N, dtype=np.float64)
        chirp_n = np.exp(sign * 1j * np.pi * (n ** 2) / N)
        
        a=x*chirp_n
        m = np.arange(-(N - 1), N, dtype=np.float64)
        chirp_kernel = np.exp(-sign * 1j * np.pi * (m ** 2) / N)
        
        M = next_power_of_two(2 * N - 1)
        a_padded = np.zeros(M, dtype=np.complex128)
        a_padded[:N] = a
        b_padded = np.zeros(M, dtype=np.complex128)
        b_padded[:N] = chirp_kernel[N - 1:]        
        b_padded[M - (N - 1):] = chirp_kernel[:N - 1]  
 
        spectrum_a = self.fft(a_padded, invert=False)
        spectrum_b = self.fft(b_padded, invert=False)
        convolved = self.fft(spectrum_a * spectrum_b, invert=True)
 
        result = convolved[:N] * chirp_n
        if invert:
            result = result / N
        return result
        

    def transform(self, x):
        # TODO (bonus): implement this method
        return self.algorithm(x,invert=False)

    def inverse(self, spectrum):
        # TODO (bonus): implement this method
        return self.algorithm(spectrum,invert=True)
