"""
bigmul.py  --  TASK A: multiplying huge integers with your own transform.

YOUR CODE GOES HERE. The provided modules io_utils.py (file reading, random
operands) and bench_utils.py (timing, runtime plots) are already imported;
everything mathematical is yours.

Usage (the command line is already wired up for you):

    python3 bigmul.py inputs/1.txt --engine fft --out-dir outputs/1
    python3 bigmul.py inputs/3.txt --engine dft --out-dir outputs/3
    python3 bigmul.py --benchmark --out-dir outputs/benchmark

Restrictions: no numpy.fft / scipy.fft / numpy.convolve / scipy.signal, and
no Python big-integer multiplication of the operands themselves. Python's
own integers may be used ONLY to check your answer at the end.
"""

import argparse
import os
import sys

import numpy as np #type:ignore

from bench_utils import plot_runtime_curve, time_best, timing_table_lines
from io_utils import random_decimal, read_operands, write_report, write_text
from transforms import ArbitraryLengthFFT, DFTAnalyzer, FFTTransformer, next_power_of_two

# Python 3.11+ refuses to print integers longer than 4300 digits unless this
# limit is raised, and the verification step below prints one.
sys.set_int_max_str_digits(2_000_000)

# Number of decimal digits packed into one "limb" (one polynomial
# coefficient). The specification explains why 4 is a safe choice and what
# breaks if you raise it too far.
BASE_DIGITS = 4
BASE = 10 ** BASE_DIGITS


def to_limbs(text, base_digits=BASE_DIGITS):
    """
    Convert a decimal string into polynomial coefficients.

    "123456789" with base_digits = 4 becomes the little-endian limb array
    [6789, 2345, 1] -- that is, 1*BASE^2 + 2345*BASE^1 + 6789*BASE^0.

    Parameters
    ----------
    text : str
        A decimal integer, possibly with a leading '+' or '-'.
    base_digits : int
        Decimal digits per limb.

    Returns
    -------
    (int, numpy.ndarray)
        The sign (+1 or -1) and the little-endian limb array (dtype int64).
        Handle the sign separately from the magnitude: the transform never
        sees it.
    """
    # TODO: implement this function
    sign=-1 if text[0]=="-" else 1
    body=text[1:] if text[0] in "+-" else text
    body=body.lstrip("0") or "0"
    
    limbs=[]
    end=len(body)
    
    while end>0:
        start=max(0,end-base_digits)
        limbs.append(int(body[start:end]))
        end=start
    if not limbs:
        limbs=[0]
        
    return sign, np.array(limbs,dtype=np.int64)        


def from_limbs(sign, limbs, base_digits=BASE_DIGITS):
    """
    Convert limbs back into a decimal string, propagating carries.

    The limbs handed to this function are the convolution result, so they are
    NOT yet reduced: an entry may be far larger than BASE. Sweep from the
    least significant limb upwards, carrying the overflow into the next one,
    then strip leading zeros and re-attach the sign.

    Returns
    -------
    str
        The decimal representation. "0" must come out as "0", not "-0" or "".
    """
    # TODO: implement this function
    base=10**base_digits
    
    carry=0
    carried=[]
    for value in limbs:
        total=int(round(float(value)))+carry
        carry,digit=divmod(total,base)
        carried.append(digit)
    
    while carry:
        carry,digit=divmod(carry,base)
        carried.append(digit)
        
    while len(carried) > 1 and carried[-1] == 0:
        carried.pop()
        
    most_significant = carried[-1]
    rest = carried[:-1]
    text = str(most_significant) + "".join(
        str(limb).zfill(base_digits) for limb in reversed(rest)
    )
 
    if int(text) == 0:
        return "0"
    return ("-" if sign < 0 else "") + text            


def multiply_transform(a, b, engine):
    """
    Multiply two limb arrays through the frequency domain.

    The product of two polynomials is the LINEAR convolution of their
    coefficients, and the transform gives you convolution as a pointwise
    product -- but a DFT of length N gives you CIRCULAR convolution of period
    N. Choose N large enough that the linear result fits, or the high-order
    coefficients wrap around and silently corrupt the answer.

    Steps:
      1. Choose the transform length N (see above; for FFTTransformer it must
         also be a power of two -- next_power_of_two is in transforms.py).
      2. Zero-pad both limb arrays to length N.
      3. Transform both, multiply the two spectra pointwise, inverse-transform.
      4. The result is real up to rounding error: take the real part and round
         to the nearest integer.

    Parameters
    ----------
    a, b : numpy.ndarray of int64
        Little-endian limb arrays.
    engine : DFTAnalyzer or FFTTransformer

    Returns
    -------
    (numpy.ndarray of int64, int)
        The un-carried convolution coefficients, and the transform length N
        you used (report.txt has to state it).
    """
    # TODO: implement this function
    linear_length=len(a)+len(b)-1
    
    if engine.name=="fft":
        N=next_power_of_two(linear_length)
    else:
        N=linear_length
    
    a_padded=np.zeros(N,dtype=np.complex128)
    b_padded=np.zeros(N,dtype=np.complex128)
    
    a_padded[:len(a)]=a
    b_padded[:len(b)]=b
    
    spectrum_a=engine.transform(a_padded)
    spectrum_b=engine.transform(b_padded)        
    
    spectrum_product=spectrum_a*spectrum_b
    convolved=engine.inverse(spectrum_product)
    
    result=np.rint(convolved.real).astype(np.int64)
    return result,N


def multiply_schoolbook(a, b):
    """
    OPTIONAL baseline: the O(n^2) method everyone learns at school, on limbs.

    Only needed if you want a third curve on your runtime plot. Expect it to
    be competitive for a long time: a NumPy-assisted schoolbook multiply has a
    very small constant factor, and constant factors decide who wins at small
    sizes.
    """
    # TODO (optional): implement this function
    n,q=len(a),len(b)
    result=np.zeros(n+q-1,dtype=np.int64)
    
    for i in range(n):
        result[i:i+q]+=a[i]*b
    
    return result

def ntt_bit_reversal_permutation(N):
    num_bits=N.bit_length()-1
    idx=np.arange(N,dtype=np.int64)
    rev = np.zeros(N, dtype=np.int64)
    for _ in range(num_bits):
        rev=(rev<<1)|(idx&1)
        idx>>=1
    return rev

NTT_MOD = 998244353
NTT_ROOT = 3
NTT_BASE_DIGITS = 2
NTT_BASE = 10 ** NTT_BASE_DIGITS

def ntt_transform(a,invert,mod=NTT_MOD,root=NTT_ROOT):
    a=np.asarray(a,dtype=np.int64)%mod
    N=a.shape[0]
    
    if N==0 or (N&(N-1))!=0:
        raise ValueError("NTT length must be a power of two, got %d" % N)
    a=a[ntt_bit_reversal_permutation(N)].copy()
    
    length=2
    while length<=N:
        half=length//2
        
        w = pow(root, (mod-1)//length, mod)
        if invert:
            w = pow(w, mod-2, mod)
            
        twiddle=np.empty(half,dtype=np.int64)
        cur=1
        for i in range(half):
            twiddle[i]=cur
            cur=(cur*w)%mod
        for start in range(0,N,length):
            even = a[start:start + half]
            odd = a[start + half:start + length]
            t = (odd * twiddle) % mod
            new_even = (even + t) % mod
            new_odd = (even - t) % mod
            a[start:start + half] = new_even
            a[start + half:start + length] = new_odd
        length*=2
    if invert:
        inv_N = pow(N, mod - 2, mod)  
        a = (a * inv_N) % mod
    return a                        

def multiply_ntt(a, b, mod=NTT_MOD, root=NTT_ROOT):
    linear_len = len(a) + len(b) - 1
    N = next_power_of_two(linear_len)
 
    a_padded = np.zeros(N, dtype=np.int64)
    b_padded = np.zeros(N, dtype=np.int64)
    a_padded[:len(a)] = a
    b_padded[:len(b)] = b
 
    spectrum_a = ntt_transform(a_padded, invert=False, mod=mod, root=root)
    spectrum_b = ntt_transform(b_padded, invert=False, mod=mod, root=root)
    spectrum_product = (spectrum_a * spectrum_b) % mod
    convolved = ntt_transform(spectrum_product, invert=True, mod=mod, root=root)
    
    return convolved,N

def multiply(text_a, text_b, method):
    """
    Multiply two decimal strings and return (product_string, N, limbs_a, limbs_b).

    ``method`` is one of "dft", "fft", "schoolbook" (optional) or "arbitrary"
    (bonus). Pick the engine, convert to limbs, convolve, carry, re-sign.
    """
    # TODO: implement this function
    base_digits = NTT_BASE_DIGITS if method == "ntt" else BASE_DIGITS
 
    sign_a, limbs_a = to_limbs(text_a, base_digits)
    sign_b, limbs_b = to_limbs(text_b, base_digits)
    sign = sign_a * sign_b
 
    if method == "dft":
        convolved, N = multiply_transform(limbs_a, limbs_b, DFTAnalyzer())
    elif method == "fft":
        convolved, N = multiply_transform(limbs_a, limbs_b, FFTTransformer())
    elif method == "arbitrary":
        convolved, N = multiply_transform(limbs_a, limbs_b, ArbitraryLengthFFT())
    elif method == "schoolbook":
        convolved = multiply_schoolbook(limbs_a, limbs_b)
        N = len(convolved)
    elif method == "ntt":
        convolved, N = multiply_ntt(limbs_a, limbs_b)
    else:
        raise ValueError("unknown method: %r" % (method,))
 
    product_text = from_limbs(sign, convolved, base_digits)
    return product_text, N, limbs_a, limbs_b


def run_single(path, method, out_dir):
    """
    Process one input file and write the required outputs.

    Must produce, inside ``out_dir``:
      product.txt -- the product as a single decimal string
      report.txt  -- input path, method, digit counts of both operands, the
                     base used, limb counts, the transform length N, the digit
                     count of the product, and the verification verdict.
                     It is written by your code; there is no separate
                     write-up to hand in.

    Verification: compare your product against ``int(text_a) * int(text_b)``.
    This is the ONLY place Python's big integers may be used. Print MATCH or
    MISMATCH; a MISMATCH must not be silently swallowed.
    """
    # TODO: implement this function
    text_a, text_b = read_operands(path)
    product_text, N, limbs_a, limbs_b = multiply(text_a, text_b, method)
 
    write_text(os.path.join(out_dir, "product.txt"), product_text)
    expected = int(text_a) * int(text_b)
    actual = int(product_text)
    verdict = "MATCH" if actual == expected else "MISMATCH"
 
    digits_a = len(text_a.lstrip("+-").lstrip("0")) or 1
    digits_b = len(text_b.lstrip("+-").lstrip("0")) or 1
    base_digits_used = NTT_BASE_DIGITS if method == "ntt" else BASE_DIGITS
 
    report_lines = [
        "Task A -- big-integer multiplication by spectral convolution",
        "input file          : %s" % path,
        "method              : %s" % method,
        "digits of A / B     : %d / %d" % (digits_a, digits_b),
        "base                : 10^%d" % base_digits_used,
        "limbs of A / B      : %d / %d" % (len(limbs_a), len(limbs_b)),
        "transform length N  : %d" % N,
        "digits of product   : %d" % len(product_text.lstrip("-")),
        "verification        : %s" % verdict,
    ]
    write_report(os.path.join(out_dir, "report.txt"), report_lines)
 
    print("%s: %s" % (path, verdict))
    if verdict == "MISMATCH":
        print("  WARNING: product does not match Python's int multiplication!")


# ---------------------------------------------------------------------------
# PROVIDED -- run_benchmark is already written. It calls your multiply(), so
# it starts working as soon as your transforms and multiply() are correct.
# You do not need to modify anything below (though you may extend it).
# ---------------------------------------------------------------------------
DFT_SIZES = [128, 256, 512, 1024, 2048, 4096]
FFT_SIZES = [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]
TIME_BUDGET = 20.0          # stop a sweep once one measurement exceeds this


def run_benchmark(out_dir):
    """
    Measure naive DFT against radix-2 FFT over growing operands and write
    runtime_bigmul.png plus the timing table in report.txt.

    Each sweep stops early once a single measurement exceeds TIME_BUDGET
    seconds, so a slow machine (or a slow DFT) simply produces a shorter
    curve rather than hanging.
    """
    def measure(label, method, sizes):
        xs, ys = [], []
        print("%s:" % label)
        for digits in sizes:
            a = random_decimal(digits, seed=digits)
            b = random_decimal(digits, seed=digits + 1)
            seconds = time_best(lambda: multiply(a, b, method), repeats=2)
            xs.append(digits)
            ys.append(seconds)
            print("  %8d digits   %9.4f s" % (digits, seconds))
            if seconds > TIME_BUDGET:
                print("  (stopping this curve -- over the time budget)")
                break
        return xs, ys

    series = {}
    series["Naive DFT"] = measure("naive DFT", "dft", DFT_SIZES)
    series["Radix-2 FFT"] = measure("radix-2 FFT", "fft", FFT_SIZES)
    try:                                    # optional third curve
        series["Schoolbook"] = measure("schoolbook", "schoolbook", FFT_SIZES)
    except NotImplementedError:
        series.pop("Schoolbook", None)
        print("schoolbook: not implemented, skipping that curve")

    plot_path = os.path.join(out_dir, "runtime_bigmul.png")
    plot_runtime_curve(series, plot_path,
                       title="Task A: big-integer multiplication",
                       xlabel="decimal digits per operand",
                       references=("n2", "nlogn"))
    write_report(os.path.join(out_dir, "report.txt"),
                 ["Task A -- runtime benchmark", ""]
                 + timing_table_lines(series, size_label="digits")
                 + ["", "plot: %s" % os.path.basename(plot_path)])
    print("wrote", plot_path)


def main():
    ap = argparse.ArgumentParser(description="Big-integer multiplication by DFT/FFT")
    ap.add_argument("input", nargs="?", help="input file with the two operands")
    ap.add_argument("--engine", default="fft",
                    choices=["dft", "fft", "schoolbook", "arbitrary","ntt"])
    ap.add_argument("--out-dir", default="outputs")
    ap.add_argument("--benchmark", action="store_true",
                    help="run the timing study instead of a single multiplication")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    if args.benchmark:
        run_benchmark(args.out_dir)
    else:
        if not args.input:
            ap.error("an input file is required unless --benchmark is given")
        run_single(args.input, args.engine, args.out_dir)


if __name__ == "__main__":
    main()
