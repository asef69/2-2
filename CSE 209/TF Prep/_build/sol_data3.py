"""Solutions, part 3 (Ch3 arithmetic + Outside Notes). Items may be callables returning item lists."""
from traces import div_v1, div_v2, mult_v1, mult_v2

S = {}


def mult_tables(mc, mp, n=4):
    r1, P = mult_v1(mc, mp, n)
    r2, P2 = mult_v2(mc, mp, n)
    fmt = lambda s: s[:-n] + " " + s[-n:]
    return [("T", ["Iter", "Step (first version)", "Multiplier", "Multiplicand", "Product"], [list(r) for r in r1], [7, 41, 14, 19, 19]),
            ("T", ["Iter", "Step (refined version)", "Multiplicand", "Product (left | right = multiplier)"], [[r[0], r[1], r[2], fmt(r[3])] for r in r2], [7, 47, 16, 30])]


def mult_refined(mc, mp, n=4):
    r2, _ = mult_v2(mc, mp, n)
    fmt = lambda s: s[:-n] + " " + s[-n:]
    return [("T", ["Iter", "Step", "Multiplicand", "Product (left | right)"], [[r[0], r[1], r[2], fmt(r[3])] for r in r2], [7, 47, 16, 30])]


def div_refined_2223():
    rows, q, rm = div_v2(0b101111001111, 0b110101, 6)
    return [("T", ["Iter", "Step (refined, 6-bit ALU)", "Divisor", "Remainder register"],
             [[r[0], r[1], r[2], (r[3] if " " in r[3] else r[3][:-6] + " | " + r[3][-6:])] for r in rows], [7, 47, 16, 30]),
            "A: Quotient = 111001₂ = 57, remainder = 000010₂ = 2 (57×53 + 2 = 3023 ✓)."]


FPADD_FLOW = ["| 1. Compare exponents; shift the significand of the smaller number right until exponents match",
              "| 2. Add the significands (with signs)",
              "| 3. Normalize (shift right/left, increment/decrement exponent);  overflow or underflow? -> exception",
              "| 4. Round the significand;  still normalized? no -> back to step 3"]

S[("2023-24", "CSE 209", "7(a)")] = dict(
    q="Draw the integer multiplication hardware following (i) the long-multiplication approach and (ii) the parallel add/shift approach, for 32-bit multiplier and multiplicand. For each approach also simulate the steps for the 4-bit numbers 1000 (multiplicand) and 1011 (multiplier).",
    s=[("IMG", "ch3_6", "(i) First (long-multiplication) hardware and flowchart: 64-bit multiplicand shifting left, 32-bit multiplier shifting right, 64-bit ALU and product (Ch. 3, sl. 6)"),
       ("IMG", "ch3_7", "(ii) Optimized hardware: 32-bit multiplicand and ALU, 64-bit product shifting right with the multiplier in its right half (Ch. 3, sl. 7)"),
       "Simulation of 1000 × 1011 (8 × 11):", lambda: mult_tables(0b1000, 0b1011), "A: Product = 0101 1000 = 88 ✓."])
S[("2023-24", "CSE 209", "7(b)")] = dict(
    q="What is the purpose of a positive bias in IEEE 754? Find the smallest and largest values that can be expressed in (i) single precision (32 bit) and (ii) double precision (64 bit).",
    s=["**Bias**: the exponent is stored as actual + bias (127 / 1023), so the field is an unsigned number: most negative exponent = 00…01, most positive = 11…10. Then two FP numbers of the same sign can be compared with integer comparison hardware, bit pattern by bit pattern.",
       ("T", ["", "Single", "Double"], [
           ["Reserved fields", "00000000, 11111111", "all 0s, all 1s"],
           ["Smallest normalized", "1.0 × 2^{−126} ≈ 1.18×10^{−38}", "1.0 × 2^{−1022} ≈ 2.23×10^{−308}"],
           ["Largest", "(2 − 2^{−23}) × 2^{127} ≈ 3.40×10^{38}", "(2 − 2^{−52}) × 2^{1023} ≈ 1.80×10^{308}"],
           ["Smallest denormal", "2^{−149} ≈ 1.4×10^{−45}", "2^{−1074} ≈ 4.9×10^{−324}"]], [24, 38, 38])])
S[("2022-23", "CSE 209", "1(a)")] = dict(
    q="Express the steps of floating-point addition using a flow chart. Also write the conditions of overflow, underflow, NaN and infinity during a floating-point addition.",
    s=FPADD_FLOW + [
        ("T", ["Condition", "When (single precision)"], [
            ["Overflow", "after normalizing the exponent is > 127 (field would be 255) → ±∞"],
            ["Underflow", "after normalizing the exponent is < −126 → denormal or 0"],
            ["Infinity", "an operand is ±∞ (∞ + x = ∞), or overflow occurred"],
            ["NaN", "an operand is NaN, or (+∞) + (−∞)"]], [20, 80]),
        "Example (binary): 1.000₂×2^{−1} + (−1.110₂×2^{−2}) = 0.5 − 0.4375. Align: −0.111×2^{−1}; add: 0.001×2^{−1}; normalize: 1.000×2^{−4}; round: unchanged = 0.0625."])
S[("2022-23", "CSE 209", "4")] = dict(
    q="Draw the hardware block diagram and the flowchart of the sequential version of the multiplication algorithm. Also draw the hardware block diagram and flowchart of the refined version.",
    s=[("IMG", "ch3_6", "Sequential (first) version: hardware and flowchart (Ch. 3, sl. 6)"),
       "Flowchart: test Multiplier0; if 1, Product = Product + Multiplicand; shift Multiplicand left 1; shift Multiplier right 1; repeat for 32 repetitions.",
       ("IMG", "ch3_7", "Refined version: hardware (Ch. 3, sl. 7)"),
       "Flowchart: test Product0; if 1, left half of Product += Multiplicand; shift the Product register right 1 bit; repeat 32 times.",
       "A: Improvements: 32-bit multiplicand and ALU instead of 64; no separate multiplier register (it sits in the right half of the product); add and shift happen in the same cycle."])
S[("2022-23", "CSE 305", "8(b)")] = dict(
    q="Consider a 32-bit system where 19 bits are reserved for the fraction, one bit for the sign, and the rest for the exponent. (i) What is the precision range of this system? (ii) What are the smallest and largest absolute values? (iii) What is the smallest denormalized number?",
    s=["Exponent bits = 32 − 1 − 19 = 12, bias = 2^{11} − 1 = 2047. Normalized exponent range 1 − 2047 = −2046 … 4094 − 2047 = +2047.",
       "(i) Precision 2^{−19} ≈ 1.9×10^{−6}, i.e. 19 × log₁₀2 ≈ 5.7 decimal digits.",
       "(ii) Smallest = 1.0 × 2^{−2046}; largest = (2 − 2^{−19}) × 2^{2047}.",
       "(iii) Smallest denormal = 2^{−19} × 2^{−2046} = 2^{−2065}."])
S[("2022-23", "CSE 305", "8(c)")] = dict(
    q="f1 and f2 are normalized IEEE single-precision floats, f1 < f2. (i) If the two 32-bit strings are treated as unsigned integers i1, i2, can we conclude i1 < i2? (ii) If treated as signed integers j1, j2, can we conclude j1 < j2?",
    s=[("T", ["Case", "Unsigned i1 < i2?", "Signed j1 < j2?"], [
        ["0 ≤ f1 < f2", "Yes (sign 0; exponent then fraction order = integer order)", "Yes"],
        ["f1 < 0 ≤ f2", "No (i1 has MSB 1 so i1 > i2)", "Yes (j1 negative)"],
        ["f1 < f2 < 0", "No (larger magnitude gives larger i)", "No (j1 > j2)"]], [20, 44, 36]),
       "A: Neither conclusion holds in general. (i) holds only for non-negative numbers; (ii) fails when both are negative. Example: −3.0 = 0xC0400000, −1.0 = 0xBF800000: unsigned 0xC0400000 > 0xBF800000 and signed −1 069 547 520 > −1 082 130 432."])
S[("2021-22", "CSE 305", "6(c)")] = dict(
    q="Draw the block diagram of the 32-bit combined multiplication and division hardware that uses a 32-bit ALU, and briefly mention the functions of its components.",
    s=["The refined multiplier and the refined divider have the same datapath, so one unit does both:",
       "• **Multiplicand/Divisor register** (32 bits) — holds the second operand.",
       "• **32-bit ALU** — adds (multiply) or subtracts (divide) into the left half of the product/remainder register.",
       "• **Product/Remainder register** (64 bits) — shifts **right** for multiply (product, multiplier in the right half) and **left** for divide (remainder in the left half, quotient bits enter the right half). MIPS names it HI:LO.",
       "• **Control** — tests Product0 (multiply) or the ALU sign (divide), selects add/subtract/shift and counts 32 repetitions.",
       ("IMG", "ch3_7", "Refined multiplier datapath (Ch. 3, sl. 7) — the combined unit adds a left-shift path and a subtract control to it")])
S[("2021-22", "CSE 305", "8(b)")] = dict(
    q="Consider representing the consecutive positive integers {1, 2, 3, …, n} using IEEE single-precision floating point (8-bit exponent, 23-bit fraction). Find the largest n such that every number in the set can be represented.",
    s=["An integer is exact if its binary form fits the 24-bit significand (1 hidden + 23 fraction bits). Every integer up to 2^{24} = 16 777 216 fits (2^{24} = 1.0 × 2^{24}).",
       "2^{24} + 1 = 1.000…0001 × 2^{24} needs 25 significant bits, so it rounds to 2^{24}.",
       "A: **n = 2^{24} = 16 777 216** (confirmed numerically)."])
S[("2020-21", "CSE 305", "13(a)")] = dict(
    q="Consider a 32-bit system where 24 bits are reserved for the fraction, one bit for the sign and the rest for the exponent. (i) Why is bias used in floating-point representation? (ii) What should be the value of the bias, and why? (iii) What are the smallest and largest absolute values? (iv) What is the smallest denormalized number?",
    s=["Exponent bits = 32 − 1 − 24 = 7.",
       "(i) Bias makes the exponent field unsigned, so FP numbers can be compared with integer comparators and a zero exponent field does not mean a negative exponent.",
       "(ii) Bias = 2^{6} − 1 = **63**: it splits the 126 usable exponent values (fields 1…126) into −62 … +63 — nearly symmetric; fields 0 and 127 are reserved.",
       "(iii) Smallest = 1.0 × 2^{−62}; largest = (2 − 2^{−24}) × 2^{63} ≈ 1.84×10^{19}.",
       "(iv) Smallest denormal = 2^{−24} × 2^{−62} = **2^{−86}**."])
S[("2019-20", "CSE 305", "4(a)")] = dict(
    q="A 16-bit floating-point system: largest absolute value 1.11…1₂ × 2^{63}, smallest 1.00…0₂ × 2^{−62}. (i) Show the format. (ii) Represent −110.11₂ × 2¹ with an appropriate bias. (iii) What is the smallest absolute denormalized value?",
    s=["Exponents −62 … +63 → 126 normalized values + 2 reserved = 128 = 2^{7}: **7 exponent bits**, bias 63; fraction = 16 − 1 − 7 = **8 bits**.",
       "| (i)   | S 1 | Exponent 7 (bias 63) | Fraction 8 |",
       "| (ii)  −110.11₂×2¹ = −1.1011₂×2³ → S=1, E = 3+63 = 66 = 1000010, F = 10110000",
       "|       1 1000010 10110000 = 0xC2B0   (value −13.5)",
       "| (iii) smallest denormal = 2^-8 × 2^(1−63) = 2^-70 ≈ 8.5×10^-22",
       "A: (i) 1/7/8, (ii) 0xC2B0, (iii) 2^{−70}."])
S[("2019-20", "CSE 305", "4(b)")] = dict(
    q="Figure 4b shows the first multiplication hardware (64-bit multiplicand shifting left, 64-bit ALU, 32-bit multiplier shifting right, 64-bit product). Describe why it is inefficient, what changes make it efficient, and draw the efficient hardware.",
    s=["**Inefficient because**: a 64-bit ALU and 64-bit multiplicand register are used although only 32 bits are added per step (half the multiplicand is always 0); a separate multiplier register is needed; and add, shift-left, shift-right are three sequential steps per bit (≈ 3×32 cycles).",
       "**Changes**: 32-bit multiplicand and 32-bit ALU; shift the **product right** instead of the multiplicand left; keep the multiplier in the unused right half of the 64-bit product register; do the add and the shift in the same cycle → 32 cycles.",
       ("IMG", "ch3_7", "Efficient (refined) multiplication hardware (Ch. 3, sl. 7)")])

# ============================================================ OUTSIDE
S[("2022-23", "CSE 209", "1(b)")] = dict(
    q="You have a 6-bit ALU and must perform a division where the dividend is 1011 1100 1111 and the divisor is 110101. Determine the result of the division; show the step-by-step calculation with each relevant register at each step.",
    s=["Dividend = 3023, divisor = 53. The upper half of the dividend (101111 = 47) is smaller than the divisor, so the 6-bit quotient does not overflow and the refined divider (6-bit ALU, 12-bit remainder register that shifts left) applies:", div_refined_2223])
S[("2022-23", "CSE 305", "8(a)")] = dict(
    q="Write an efficient sequence of MIPS instructions for: float a, b, c; double w, x, y, z; if (a+b > c) x = (y*z)/w;  Assume appropriate registers.",
    s=["a $f0, b $f1, c $f2 (single); w $f4, x $f6, y $f8, z $f10 (double register pairs).",
       "| add.s  $f3, $f0, $f1      # a + b",
       "| c.le.s $f3, $f2           # (a+b) <= c ?",
       "| bc1t   Skip               # true -> condition false, skip",
       "| mul.d  $f12, $f8, $f10    # y * z",
       "| div.d  $f6, $f12, $f4     # x = (y*z)/w",
       "| Skip:"])
S[("2021-22", "CSE 305", "5(c)")] = dict(
    q="Discuss how subword parallelism can be used to accelerate common operations, such as matrix multiplication or image processing.",
    s=["A wide (64/128-bit) adder is partitioned so one instruction works on many short operands at once: 16×8-bit, 8×16-bit, 4×32-bit or 2×64-bit (SIMD — MMX/SSE/AVX, ARM NEON).",
       "**Image processing** uses 8-bit pixels, so one instruction adds, averages or saturates 16 pixels. **Matrix multiplication** uses packed multiply-add on 4 floats (or 2 doubles) per instruction, cutting the inner-loop instruction count to a quarter or less on the same hardware."])
S[("2020-21", "CSE 305", "10(c)")] = dict(
    q="Briefly describe how to perform a signed multiplication operation.",
    s=["**Simple method**: remember the signs; convert negative operands to positive (2's complement); multiply the magnitudes with the unsigned algorithm (31 iterations); negate the product if the operand signs differ (S_{A} ⊕ S_{B}).",
       "**Booth's algorithm** works directly on 2's-complement numbers: examine multiplier bits (b_{i}, b_{i−1}): 10 → subtract the multiplicand, 01 → add it, 00/11 → only shift; shifts are arithmetic (sign-extending)."])
S[("2020-21", "CSE 305", "11(a)")] = dict(
    q="SPECBM101: Program 2–6 have execution times 527, 586, 109, 470, 275 s and reference times 10490, 12100, 20720, 7020, 6900 s; Program 1 has reference time 9770 s. If the geometric mean of the benchmark is 28.74 s, what is the execution time of Program 1?",
    s=["SPEC ratio = reference time / execution time; the benchmark figure is the geometric mean of the ratios: (Π ratio_{i})^{1/6}.",
       "Ratios 2–6: 19.905, 20.649, 190.09, 14.936, 25.091; Π(others) ≈ 2.93×10^{7} and 28.74^{6} ≈ 5.64×10^{8}, so ratio_{1} = 5.64×10^{8} / 2.93×10^{7} = 19.25.",
       "A: T_{1} = 9770 / 19.25 = **507.6 s**."])
S[("2020-21", "CSE 305", "11(b)")] = dict(
    q="Figure 11(b) shows a processor unit with a scratchpad memory (MUX for input data, scratchpad with Read/Write and Address, output data feeding registers A and B (Load), ALU with function select, shifter, result back to the MUX). How many micro-operations does an addition of two operands with the result stored require? Which changes and constraints are needed to reduce this to one?",
    s=["With one read port feeding registers A and B, the addition takes **3 micro-operations**: (1) A ← M[address of operand 1]; (2) B ← M[address of operand 2]; (3) M[destination] ← A + B (ALU → shifter → MUX → scratchpad write).",
       "A: To make it **one** micro-operation the scratchpad must have two read ports and one write port (a register file), the ALU must take both operands directly from the memory outputs (registers A and B removed) and the result must be written back in the same clock cycle (edge-triggered write). Constraint: the two operands must be in different locations addressable at the same time."])
S[("2020-21", "CSE 305", "12(c)")] = dict(
    q="Briefly explain the importance of guard digit, round digit and sticky bit during rounding of an intermediate floating-point number.",
    s=["Bits shifted out during alignment or normalization would be lost. IEEE 754 keeps two extra bits, **guard** and **round**, so the result can be rounded as if computed exactly. Example with 3 digits: 2.56×10⁰ + 2.34×10² = 2.3400 + 0.0256 = 2.3656 → 2.37; without them 2.34 + 0.02 = 2.36 (error in the last digit).",
       "The **sticky bit** is set if any non-zero bit was shifted past the round bit; it lets round-to-nearest-even tell an exact tie (…100…0) from 'more than half', so ties are resolved correctly.",
       "A: Together they give results within ½ unit in the last place."])
S[("2020-21", "CSE 305", "13(c)")] = dict(
    q="Write an efficient sequence of MIPS instructions for: float a, b, c; double w, x, y, z; if (a+b>c) x=(y*z)/w;",
    s=["Same as 2022-23 CSE 305 8(a):",
       "| add.s  $f3, $f0, $f1",
       "| c.le.s $f3, $f2",
       "| bc1t   Skip",
       "| mul.d  $f12, $f8, $f10",
       "| div.d  $f6, $f12, $f4",
       "| Skip:"])
S[("2019-20", "CSE 305", "4(c)")] = dict(
    q="a, b, c, d and e are of type double with values in $f2, $f4, $f6, $f8 and $f10. Write MIPS for: if (a>b) c = c − (c*e)/d; else c = c + d; using the least number of instructions.",
    s=["| c.le.d $f2, $f4           # a <= b ?",
       "| bc1t   Else",
       "| mul.d  $f12, $f6, $f10    # c * e",
       "| div.d  $f12, $f12, $f8    # (c*e)/d",
       "| sub.d  $f6, $f6, $f12     # c = c - (c*e)/d",
       "| j      Exit",
       "| Else: add.d $f6, $f6, $f8 # c = c + d",
       "| Exit:"])
