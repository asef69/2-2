"""Step-by-step traces (multiplication, division, FP) — imported by the note builders and verify.py."""
import math
import struct


def b(x, n):
    return format(x & ((1 << n) - 1), f"0{n}b")


def mult_v1(mcand, mplier, n=4):
    """First (long-multiplication) hardware: 2n-bit multiplicand shifts left, n-bit multiplier shifts right,
    2n-bit product/ALU.  Returns rows (iter, step, multiplier, multiplicand, product)."""
    M, Q, P = mcand, mplier, 0
    rows = [("0", "Initial values", b(Q, n), b(M, 2 * n), b(P, 2 * n))]
    for i in range(1, n + 1):
        if Q & 1:
            P = (P + M) & ((1 << 2 * n) - 1)
            rows.append((str(i), "1a: Multiplier0 = 1 → Prod = Prod + Mcand", b(Q, n), b(M, 2 * n), b(P, 2 * n)))
        else:
            rows.append((str(i), "1: Multiplier0 = 0 → no add", b(Q, n), b(M, 2 * n), b(P, 2 * n)))
        M = (M << 1) & ((1 << 2 * n) - 1)
        rows.append(("", "2: Shift left Multiplicand", b(Q, n), b(M, 2 * n), b(P, 2 * n)))
        Q >>= 1
        rows.append(("", "3: Shift right Multiplier", b(Q, n), b(M, 2 * n), b(P, 2 * n)))
    return rows, P


def mult_v2(mcand, mplier, n=4):
    """Refined hardware: n-bit multiplicand, n-bit ALU, 2n(+1 carry)-bit product register holding the
    multiplier in its right half; product shifts right.  Rows (iter, step, multiplicand, product)."""
    P = mplier  # right half
    rows = [("0", "Initial: Product = 0000 | multiplier", b(mcand, n), b(P, 2 * n))]
    for i in range(1, n + 1):
        if P & 1:
            hi = (P >> n) + mcand          # may produce a carry (n+1 bits)
            P = (hi << n) | (P & ((1 << n) - 1))
            rows.append((str(i), "1a: Prod0 = 1 → left half += Mcand", b(mcand, n), b(P, 2 * n + (1 if P >> 2 * n else 0))))
        else:
            rows.append((str(i), "1: Prod0 = 0 → no add", b(mcand, n), b(P, 2 * n)))
        P >>= 1
        rows.append(("", "2: Shift right Product (carry enters MSB)", b(mcand, n), b(P, 2 * n)))
    return rows, P


def div_v1(dividend, divisor, n):
    """First division hardware for a 2n-bit dividend and an n-bit divisor (textbook Fig. 3.8 scaled):
    2n-bit divisor register starts in the LEFT half and shifts right, 2n-bit remainder, quotient
    shifts left; n+1 repetitions.  Rows (iter, step, quotient, divisor, remainder)."""
    W = 2 * n
    mask = (1 << W) - 1
    Q, D, R = 0, divisor << n, dividend
    qn = n + 1
    rows = [("0", "Initial values", b(Q, qn), b(D, W), b(R, W))]
    for i in range(1, n + 2):
        R2 = R - D
        if R2 >= 0:
            R = R2
            rows.append((str(i), "1: Rem = Rem − Div → Rem ≥ 0", b(Q, qn), b(D, W), b(R, W)))
            Q = (Q << 1) | 1
            rows.append(("", "2a: Shift Q left, Q0 = 1", b(Q, qn), b(D, W), b(R, W)))
        else:
            rows.append((str(i), "1: Rem = Rem − Div → Rem < 0", b(Q, qn), b(D, W), b(R2 & mask, W)))
            rows.append(("", "2b: Rem = Rem + Div (restore); shift Q left, Q0 = 0", b((Q << 1), qn), b(D, W), b(R, W)))
            Q = Q << 1
        D >>= 1
        rows.append(("", "3: Shift Divisor right", b(Q, qn), b(D, W), b(R, W)))
    return rows, Q, R


def div_v2(dividend, divisor, n):
    """Refined division hardware: n-bit divisor, n-bit ALU, 2n-bit remainder register that holds the
    dividend and collects the quotient in its right half (shift left).  Needs dividend_hi < divisor.
    Rows (iter, step, divisor, remainder)."""
    W = 2 * n
    R = dividend
    rows = [("0", "Initial: Rem = dividend", b(divisor, n), b(R, W))]
    R = R << 1
    rows.append(("", "Shift Rem left 1", b(divisor, n), b(R, W + 1)))
    for i in range(1, n + 1):
        hi = R >> n
        if hi >= divisor:
            R = ((hi - divisor) << n) | (R & ((1 << n) - 1))
            R = (R << 1) | 1
            rows.append((str(i), "Left half − Div ≥ 0 → keep; shift Rem left, R0 = 1", b(divisor, n), b(R, W + 1)))
        else:
            R = R << 1
            rows.append((str(i), "Left half − Div < 0 → restore; shift Rem left, R0 = 0", b(divisor, n), b(R, W + 1)))
    rem = (R >> (n + 1)) & ((1 << n) - 1)
    q = R & ((1 << n) - 1)
    rows.append(("", "Shift left half right 1 (final fix-up)", b(divisor, n), b(rem, n) + " " + b(q, n)))
    return rows, q, rem


def f32_bits(x):
    return struct.unpack(">I", struct.pack(">f", x))[0]


def bits_f32(u):
    return struct.unpack(">f", struct.pack(">I", u))[0]


def custom_fp(value, ebits, fbits):
    """Encode value in a (1, ebits, fbits) IEEE-like format, bias = 2^(ebits-1) - 1 (normalized only)."""
    bias = (1 << (ebits - 1)) - 1
    s = 1 if value < 0 else 0
    v = abs(value)
    e = math.floor(math.log2(v))
    frac = v / 2 ** e - 1
    F = round(frac * (1 << fbits))
    E = e + bias
    return s, E, F, (s << (ebits + fbits)) | (E << fbits) | F


def custom_decode(u, ebits, fbits):
    bias = (1 << (ebits - 1)) - 1
    s = u >> (ebits + fbits)
    E = (u >> fbits) & ((1 << ebits) - 1)
    F = u & ((1 << fbits) - 1)
    return (-1) ** s * (1 + F / (1 << fbits)) * 2.0 ** (E - bias)
