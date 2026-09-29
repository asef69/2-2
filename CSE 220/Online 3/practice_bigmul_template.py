"""
practice_bigmul_template.py -- practice scaffold for the Big-Integer Track of the
CSE 220 DFT/FFT Practice Question Bank.

Companion code to CSE220_DFT_FFT_Practice_QuestionBank_BigMul.pdf.

This file imports your already-completed bigmul.py (so to_limbs, from_limbs,
multiply, and next_power_of_two are already available) and transforms.py,
and leaves ONLY the TODO-marked functions below for you to fill in, one
section per practice problem.

Do NOT modify transforms.py, io_utils.py, or bench_utils.py. You MAY copy
logic directly out of your own bigmul.py into the TODOs below -- that is the
point of reusing it.

Usage: pick one problem at a time, matching the "Run:" command shown for it
in the question bank PDF, e.g.

    python3 practice_bigmul_template.py p1 inputs/1.txt --engine fft --out-dir outputs/p1

Each pN() function at the bottom wires up argparse for that problem only.
"""

import argparse
import os
import sys

import numpy as np  # type: ignore

from bigmul import (BASE_DIGITS, DFTAnalyzer, FFTTransformer, ArbitraryLengthFFT,
                     from_limbs, multiply, next_power_of_two, to_limbs)
from io_utils import random_decimal, write_report, write_text

sys.set_int_max_str_digits(2_000_000)


def _make_engine(name):
    if name == "dft":
        return DFTAnalyzer()
    if name == "fft":
        return FFTTransformer()
    if name == "arbitrary":
        return ArbitraryLengthFFT()
    raise ValueError("unknown engine: %r" % name)


def read_one_operand(path):
    """Read just the first non-comment, non-blank line of an input file."""
    with open(path, "r") as handle:
        for raw in handle:
            line = raw.strip()
            if line and not line.startswith("#"):
                return line
    raise ValueError("%s: no operand line found" % path)


def read_two_operands(path):
    """Provided: same contract as io_utils.read_operands, re-exported here for convenience."""
    from io_utils import read_operands
    return read_operands(path)

def _mul_str(a_text, b_text, method):
    """Multiply two decimal strings via bigmul.multiply (the spectral engine)."""
    product_text, _N, _la, _lb = multiply(a_text, b_text, method)
    return product_text
 
 
def _truncate_div_pow10(text, p):
    """floor(int(text) / 10**p) for a NON-NEGATIVE decimal string, by slicing
    (this is truncation, not an algorithmic division, so it stays O(n))."""
    if p <= 0:
        return text
    if len(text) <= p:
        return "0"
    trimmed = text[:-p].lstrip("0")
    return trimmed if trimmed else "0"


def _positive(text):
    text = text.lstrip("+").lstrip("0")
    return text or "0"


def _compare_positive(left, right):
    left, right = _positive(left), _positive(right)
    if len(left) != len(right):
        return 1 if len(left) > len(right) else -1
    return (left > right) - (left < right)


def _add_positive(left, right):
    carry = 0
    result = []
    left, right = left[::-1], right[::-1]
    for index in range(max(len(left), len(right))):
        total = carry
        if index < len(left):
            total += ord(left[index]) - 48
        if index < len(right):
            total += ord(right[index]) - 48
        result.append(str(total % 10))
        carry = total // 10
    if carry:
        result.append(str(carry))
    return "".join(reversed(result))


def _subtract_positive(left, right):
    if _compare_positive(left, right) < 0:
        raise ValueError("positive subtraction would become negative")
    borrow = 0
    result = []
    left, right = left[::-1], right[::-1]
    for index, digit in enumerate(left):
        value = ord(digit) - 48 - borrow
        if index < len(right):
            value -= ord(right[index]) - 48
        if value < 0:
            value += 10
            borrow = 1
        else:
            borrow = 0
        result.append(str(value))
    return _positive("".join(reversed(result)))


def _multiply_positive(left, right, method):
    return _positive(_mul_str(_positive(left), _positive(right), method))


# ===========================================================================
# Problem 1 -- Fast squaring via a single spectral transform
# ===========================================================================
def square_via_transform(limbs, engine):
    """
    TODO (P1): zero-pad `limbs` to the correct transform length N (linear
    self-convolution length = 2*len(limbs)-1, rounded up to a power of two
    only if engine.name == 'fft'), transform ONCE, square the spectrum
    elementwise (a single NumPy `** 2`, NOT a second call to
    engine.transform), inverse-transform, round to the nearest integer, and
    return (uncarried_result, N) -- same contract as bigmul.multiply_transform.
    """
    limbs=np.asarray(limbs,dtype=np.float64)
    linear_length=2*len(limbs)-1
    if engine.name=='fft':
        N=next_power_of_two(linear_length)
    else:
        N=linear_length
    padded=np.zeros(N,dtype=np.complex128)
    padded[:len(limbs)]=limbs
    
    spectrum=engine.transform(padded)
    spectrum_square=spectrum**2
    convolved=engine.inverse(spectrum_square)
    
    result=np.rint(convolved.real).astype(np.int64)
    return result,N        


def square_decimal(text, method):
    """
    TODO (P1): convert text to limbs with to_limbs, dispatch to
    square_via_transform for a spectral engine (or a schoolbook self-multiply
    for method == 'schoolbook'), carry with from_limbs, and return the
    product string. A squared number is always non-negative regardless of
    the operand's sign -- do not just reuse the operand's sign unchanged.
    """
    _, limbs = to_limbs(text, BASE_DIGITS)
    
    if method=='schoolbook':
        n=len(limbs)
        convolved=np.zeros(2*n-1,dtype=np.int64)
        for i in range(n):
            convolved[i:i+n]+=limbs[i]*limbs
    else:
        engine=_make_engine(method)
        convolved,N=square_via_transform(limbs,engine)
    
    return from_limbs(1,convolved,BASE_DIGITS)            


def run_p1(args):
    text_a = read_one_operand(args.input)
    product_text = square_decimal(text_a, args.engine)
    expected = int(text_a) ** 2
    actual = int(product_text)
    verdict = "MATCH" if actual == expected else "MISMATCH"

    os.makedirs(args.out_dir, exist_ok=True)
    write_text(os.path.join(args.out_dir, "square.txt"), product_text)
    write_report(os.path.join(args.out_dir, "report.txt"), [
        "Practice P1 -- fast squaring via single spectral transform",
        "input      : %s" % args.input,
        "engine     : %s" % args.engine,
        "digits of a: %d" % len(text_a.lstrip("+-")),
        "verification: %s" % verdict,
    ])
    print(args.input, ":", verdict)


# ===========================================================================
# Problem 2 -- Big-integer division via Newton-Raphson reciprocal
# ===========================================================================
def newton_reciprocal(divisor_text, precision_digits, method):
    """
    TODO (P2): return a decimal string representing
    floor(10**precision_digits / int(divisor_text)), computed ONLY via the
    iteration x_(k+1) = x_k * (2*10^p - B*x_k) / 10^p (p = precision_digits),
    using bigmul.multiply(...) for every B*x_k-sized product. Start from a
    crude estimate based on divisor_text's digit count and iterate until two
    successive iterates agree in their leading (precision_digits - 10)
    digits.
    """
    divisor = _positive(divisor_text)
    if divisor == "0":
        raise ZeroDivisionError("division by zero")
    scale = "1" + "0" * precision_digits
    divisor_digits = len(divisor)
    estimate = "1" + "0" * max(0, precision_digits - divisor_digits)
    two_scale = _add_positive(scale, scale)
    iterations = max(4, (precision_digits.bit_length() + 2))
    for _ in range(iterations):
        product = _multiply_positive(divisor, estimate, method)
        if _compare_positive(product, two_scale) >= 0:
            factor = "0"
        else:
            factor = _subtract_positive(two_scale, product)
        estimate = _truncate_div_pow10(
            _multiply_positive(estimate, factor, method), precision_digits
        )
    return estimate


def divmod_big(text_a, text_b, method):
    """
    TODO (P2): use newton_reciprocal to get an approximate quotient
    q0 = floor(A * reciprocal(B) / 10**precision_digits), then correct it
    with a small number of +/-1 adjustments (using multiply() to recompute
    q0*B and compare against A each time) until q0*B <= A < (q0+1)*B.
    Return (quotient_text, remainder_text).
    """
    sign_a = -1 if text_a.startswith("-") else 1
    sign_b = -1 if text_b.startswith("-") else 1
    magnitude_a = _positive(text_a.lstrip("+-"))
    magnitude_b = _positive(text_b.lstrip("+-"))
    if magnitude_b == "0":
        raise ZeroDivisionError("division by zero")
    if magnitude_a == "0":
        return "0", "0"

    precision = len(magnitude_a) + len(magnitude_b) + 4
    reciprocal = newton_reciprocal(magnitude_b, precision, method)
    quotient = _truncate_div_pow10(
        _multiply_positive(magnitude_a, reciprocal, method), precision
    )
    product = _multiply_positive(quotient, magnitude_b, method)
    while _compare_positive(product, magnitude_a) > 0:
        quotient = _subtract_positive(quotient, "1")
        product = _multiply_positive(quotient, magnitude_b, method)
    remainder = _subtract_positive(magnitude_a, product)
    while _compare_positive(_add_positive(product, magnitude_b), magnitude_a) <= 0:
        quotient = _add_positive(quotient, "1")
        product = _add_positive(product, magnitude_b)
        remainder = _subtract_positive(magnitude_a, product)

    quotient_negative = sign_a != sign_b
    if sign_a < 0 and remainder != "0":
        quotient = _add_positive(quotient, "1")
        remainder = _subtract_positive(magnitude_b, remainder)
    quotient_text = ("-" if quotient_negative and quotient != "0" else "") + quotient
    remainder_text = ("-" if sign_b < 0 and remainder != "0" else "") + remainder
    return quotient_text, remainder_text


def run_p2(args):
    text_a, text_b = read_two_operands(args.input)
    quotient_text, remainder_text = divmod_big(text_a, text_b, args.engine) # type: ignore
    expected_q, expected_r = divmod(int(text_a), int(text_b))
    verdict = "MATCH" if (int(quotient_text) == expected_q and
                           int(remainder_text) == expected_r) else "MISMATCH"

    os.makedirs(args.out_dir, exist_ok=True)
    write_text(os.path.join(args.out_dir, "quotient.txt"), quotient_text)
    write_text(os.path.join(args.out_dir, "remainder.txt"), remainder_text)
    write_report(os.path.join(args.out_dir, "report.txt"), [
        "Practice P2 -- Newton-Raphson big-integer division",
        "input        : %s" % args.input,
        "engine       : %s" % args.engine,
        "verification : %s" % verdict,
    ])
    print(args.input, ":", verdict)


# ===========================================================================
# Problem 3 -- Modular exponentiation by repeated spectral squaring
# ===========================================================================
def mod_small(text, modulus):
    """
    TODO (P3): compute int(text) % modulus using Horner's rule digit by
    digit (acc = (acc*10 + digit) % modulus for each decimal digit of text,
    left to right). No call to int(text) on the full string, no big-integer
    division.
    """
    text=text.lstrip("+")
    negative=text.startswith("-")
    body=text.lstrip("0") or "0"
    acc=0
    for ch in body:
        acc=(acc*10+(ord(ch)-48))%modulus
    
    if negative and acc!=0:
        acc=(modulus-acc)%modulus
    
    return acc        


def modpow_big(base_text, exponent_text, modulus, method):
    """
    TODO (P3): binary (square-and-multiply) exponentiation. You may convert
    the EXPONENT itself with int() (it is not the "big" operand here).
    Maintain the running result as a decimal string, repeatedly squaring it
    with your spectral squaring/multiply machinery and reducing with
    mod_small after every squaring and every multiply-in of the base.
    Return the final result as a plain Python int (it is bounded by
    modulus - 1, so this is safe).
    """
    exponent=int(exponent_text)
    result=str(1%modulus)
    
    base = str(mod_small(base_text, modulus))
 
    while exponent > 0:
        if exponent & 1:
            product = _mul_str(result, base, method)
            result = str(mod_small(product, modulus))
        exponent >>= 1
        if exponent > 0:
            squared = _mul_str(base, base, method)
            base = str(mod_small(squared, modulus))
 
    return int(result) % modulus


def run_p3(args):
    base_text, exponent_text = read_two_operands(args.input)
    result = modpow_big(base_text, exponent_text, args.modulus, args.engine)
    expected = pow(int(base_text), int(exponent_text), args.modulus)
    verdict = "MATCH" if result == expected else "MISMATCH"

    os.makedirs(args.out_dir, exist_ok=True)
    write_text(os.path.join(args.out_dir, "result.txt"), str(result))
    write_report(os.path.join(args.out_dir, "report.txt"), [
        "Practice P3 -- modular exponentiation by repeated spectral squaring",
        "input        : %s" % args.input,
        "modulus      : %d" % args.modulus,
        "engine       : %s" % args.engine,
        "verification : %s" % verdict,
    ])
    print(args.input, ":", verdict)


# ===========================================================================
# Problem 4 -- Circular (wraparound) big-integer multiplication
# ===========================================================================
def multiply_circular(limbs_a, limbs_b, N, engine):
    """
    TODO (P4): zero-pad both limb arrays to EXACTLY length N (raise
    ValueError if N < max(len(limbs_a), len(limbs_b))), transform, multiply
    spectra, inverse-transform, round to integers. This deliberately
    represents (A*B) reduced modulo (BASE^N - 1) at the limb level when N is
    too small for the true linear convolution.
    """
    limbs_a = np.asarray(limbs_a, dtype=np.float64)
    limbs_b = np.asarray(limbs_b, dtype=np.float64)
    if N < max(len(limbs_a), len(limbs_b)):
        raise ValueError("N is too small for the input limb arrays")
    padded_a = np.zeros(N, dtype=np.complex128)
    padded_b = np.zeros(N, dtype=np.complex128)
    padded_a[:len(limbs_a)] = limbs_a
    padded_b[:len(limbs_b)] = limbs_b
    result = engine.inverse(
        engine.transform(padded_a) * engine.transform(padded_b)
    )
    return np.rint(result.real).astype(np.int64)


def decode_possibly_wrong(sign, wrapped_limbs, base_digits=BASE_DIGITS):
    """
    TODO (P4): run `wrapped_limbs` through the SAME carry-propagation logic
    as bigmul.from_limbs to obtain a decimal string, even though the result
    may be numerically wrong because it came from multiply_circular with an
    insufficient N. Just call bigmul.from_limbs directly -- do not
    reimplement or special-case it.
    """
    return from_limbs(sign, wrapped_limbs, base_digits)


def first_divergence(text_a, text_b, N, method):
    """
    TODO (P4): compute the correct product via bigmul.multiply(text_a,
    text_b, method) and the deliberately-wrapped product via to_limbs +
    multiply_circular + decode_possibly_wrong, then return the index
    (counting from the LEAST-significant digit, 0-based) of the first
    decimal digit at which the two decimal strings differ, or -1 if they
    match completely.
    """
    correct, _unused_n, _la, _lb = multiply(text_a, text_b, method)
    sign_a, limbs_a = to_limbs(text_a, BASE_DIGITS)
    sign_b, limbs_b = to_limbs(text_b, BASE_DIGITS)
    wrapped = multiply_circular(limbs_a, limbs_b, N, _make_engine(method))
    wrong = decode_possibly_wrong(sign_a * sign_b, wrapped, BASE_DIGITS)
    correct_digits = correct.lstrip("-")[::-1]
    wrong_digits = wrong.lstrip("-")[::-1]
    for index in range(max(len(correct_digits), len(wrong_digits))):
        left = correct_digits[index] if index < len(correct_digits) else "0"
        right = wrong_digits[index] if index < len(wrong_digits) else "0"
        if left != right:
            return index
    return -1


def run_p4(args):
    text_a, text_b = read_two_operands(args.input)
    divergence = first_divergence(text_a, text_b, args.N, args.engine)

    os.makedirs(args.out_dir, exist_ok=True)
    write_report(os.path.join(args.out_dir, "report.txt"), [
        "Practice P4 -- circular (wraparound) big-integer multiplication",
        "input               : %s" % args.input,
        "circular length N   : %d" % args.N,
        "engine              : %s" % args.engine,
        "first divergent digit (from LSB, -1 = no divergence): %d" % divergence,
    ])
    print(args.input, ": first divergence at digit", divergence, "(from LSB; -1 = exact)")


# ===========================================================================
# Problem 5 -- Fast radix conversion: decimal to base 65536
# ===========================================================================
def multiply_base_arrays(a, b, base, engine):
    """
    TODO (P5): convolve two little-endian digit arrays already expressed in
    `base` (not necessarily bigmul.BASE) and carry-propagate in that base --
    the same shape as multiply_transform + from_limbs, generalised to take
    `base` as a parameter. Return a plain little-endian list/array of ints
    in [0, base).
    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    length = len(a) + len(b) - 1
    transform_length = next_power_of_two(length) if engine.name == "fft" else length
    padded_a = np.zeros(transform_length, dtype=np.complex128)
    padded_b = np.zeros(transform_length, dtype=np.complex128)
    padded_a[:len(a)] = a
    padded_b[:len(b)] = b
    raw = np.rint(engine.inverse(
        engine.transform(padded_a) * engine.transform(padded_b)
    ).real).astype(object)
    digits = []
    carry = 0
    for value in raw[:length]:
        total = int(value) + carry
        carry, digit = divmod(total, base)
        digits.append(digit)
    while carry:
        carry, digit = divmod(carry, base)
        digits.append(digit)
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()
    return np.asarray(digits, dtype=np.int64)


def base_pow65536(exponent, base_from, engine):
    """
    TODO (P5): return the base-65536 little-endian digit array representing
    base_from ** exponent (base_from will always be 10 here), computed by
    REPEATED SQUARING using multiply_base_arrays -- not by naive repeated
    multiplication by base_from, which would defeat the purpose of using a
    spectral multiply.
    """
    result = np.array([1], dtype=np.int64)
    factor = np.array([base_from], dtype=np.int64)
    power = exponent
    while power:
        if power & 1:
            result = multiply_base_arrays(result, factor, 65536, engine)
        power >>= 1
        if power:
            factor = multiply_base_arrays(factor, factor, 65536, engine)
    return result


def decimal_to_base65536(text, engine, small_cutoff=8):
    """
    TODO (P5): if len(text) <= small_cutoff, convert directly with ordinary
    Python arithmetic on that small chunk (mirrors bigmul.to_limbs's own use
    of int() on individual small limbs). Otherwise split text into a high
    part and a low part of exactly `half` decimal digits (choose `half` so
    the low part is zero-padded to exactly that many digits -- do not drop
    leading zeros from the low half), recursively convert both halves, and
    combine as high_digits * base_pow65536(half, 10, engine) (via
    multiply_base_arrays) plus low_digits (as a big-array addition with
    carries in base 65536). Return a little-endian list/array of ints in
    [0, 65536).
    """
    negative = text.startswith("-")
    text = text.lstrip("+-").lstrip("0") or "0"
    if len(text) <= small_cutoff:
        value = int(text)
        digits = []
        while value:
            value, digit = divmod(value, 65536)
            digits.append(digit)
        return np.asarray(digits or [0], dtype=np.int64)

    half = len(text) // 2
    high = decimal_to_base65536(text[:-half], engine, small_cutoff)
    low = decimal_to_base65536(text[-half:], engine, small_cutoff)
    shifted = multiply_base_arrays(
        high, base_pow65536(half, 10, engine), 65536, engine
    )
    result = []
    carry = 0
    for index in range(max(len(shifted), len(low))):
        total = carry
        if index < len(shifted):
            total += int(shifted[index])
        if index < len(low):
            total += int(low[index])
        carry, digit = divmod(total, 65536)
        result.append(digit)
    while carry:
        carry, digit = divmod(carry, 65536)
        result.append(digit)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    if negative and any(result):
        raise ValueError("base conversion returns magnitude digits only")
    return np.asarray(result, dtype=np.int64)


def _reconstruct_from_base65536(digits):
    """Provided independent oracle: Horner evaluation back to a Python int.
    This is the ONE place ordinary big-integer arithmetic is allowed for
    this problem, exactly as run_single's final check is the one allowed
    place in bigmul.py."""
    value = 0
    for d in reversed(digits):
        value = value * 65536 + int(d)
    return value


def run_p5(args):
    text_a = read_one_operand(args.input)
    engine = _make_engine(args.engine)
    digits = decimal_to_base65536(text_a, engine)
    reconstructed = _reconstruct_from_base65536(digits)
    expected = int(text_a)
    verdict = "MATCH" if reconstructed == expected else "MISMATCH"

    os.makedirs(args.out_dir, exist_ok=True)
    write_report(os.path.join(args.out_dir, "report.txt"), [
        "Practice P5 -- divide-and-conquer radix conversion to base 65536",
        "input        : %s" % args.input,
        "engine       : %s" % args.engine,
        "base-65536 digit count: %d" % len(digits),
        "verification : %s" % verdict,
    ])
    print(args.input, ":", verdict)


# ===========================================================================
# CLI wiring -- one subcommand per problem, matching the PDF's "Run:" lines.
# ===========================================================================
def main():
    ap = argparse.ArgumentParser(description="CSE220 DFT/FFT big-integer practice scaffold")
    sub = ap.add_subparsers(dest="problem", required=True)

    p1 = sub.add_parser("p1")
    p1.add_argument("input")
    p1.add_argument("--engine", choices=["dft", "fft", "arbitrary", "schoolbook"], default="fft")
    p1.add_argument("--out-dir", default="outputs/p1")
    p1.set_defaults(func=run_p1)

    p2 = sub.add_parser("p2")
    p2.add_argument("input")
    p2.add_argument("--engine", choices=["dft", "fft", "arbitrary"], default="fft")
    p2.add_argument("--out-dir", default="outputs/p2")
    p2.set_defaults(func=run_p2)

    p3 = sub.add_parser("p3")
    p3.add_argument("input")
    p3.add_argument("--modulus", type=int, default=998244353)
    p3.add_argument("--engine", choices=["dft", "fft", "arbitrary"], default="fft")
    p3.add_argument("--out-dir", default="outputs/p3")
    p3.set_defaults(func=run_p3)

    p4 = sub.add_parser("p4")
    p4.add_argument("input")
    p4.add_argument("--N", type=int, default=64)
    p4.add_argument("--engine", choices=["dft", "fft", "arbitrary"], default="fft")
    p4.add_argument("--out-dir", default="outputs/p4")
    p4.set_defaults(func=run_p4)

    p5 = sub.add_parser("p5")
    p5.add_argument("input")
    p5.add_argument("--engine", choices=["dft", "fft", "arbitrary"], default="fft")
    p5.add_argument("--out-dir", default="outputs/p5")
    p5.set_defaults(func=run_p5)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
