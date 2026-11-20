"""Build CSE209_ART_Ch3_Arithmetic_Notes.docx  (Lessons 19–23).   python -P build_notes_ch3.py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CH3, QUESTIONS, exam_map, marks_since, new
from traces import div_v1, div_v2, mult_v1, mult_v2

n = new("Chapter 3 · Arithmetic for Computers (short slides)", "CSE209_ART_Ch3_Arithmetic_Notes.docx")
n.front_matter(
    contents=[
        ("Exam Map — What the TF Papers Ask", "arithmetic questions and how much they matter"),
        ("Lesson 19 — Integer Addition, Subtraction and Overflow", "overflow rules, the O/SA/SB/SR table"),
        ("Lesson 20 — Multiplication Hardware", "first and refined multiplier, flowcharts, step-by-step traces"),
        ("Lesson 21 — IEEE 754 Floating-Point Representation", "format, bias, ranges, special values, custom formats"),
        ("Lesson 22 — Floating-Point Addition and the FP Adder", "4 steps, flowchart, over/underflow, traced examples"),
        ("Lesson 23 — Beyond the Short Slides (textbook insurance)", "division, signed multiplication, MIPS FP code, guard/round/sticky, subword parallelism"),
        ("Quick Notes — Arithmetic", "merged revision notes + key diagrams"),
    ],
    source_note="Slide numbers are PDF pages of Chapter_03_Arithmetic-shortslide.pdf (Tushar Sir, 20 slides; from PDF page 17 on the printed slide number is 2 higher). "
                "Lesson 23 covers textbook topics that are NOT on the short slides but are asked repeatedly (division even in 2022-23 CSE 209); those questions sit in the tracker's Outside Notes tab. "
                "All traces and encodings were generated and checked by _build/traces.py and verify.py.")

n.h1("Exam Map — What the TF Papers Ask")
n.p("Every Tushar-Sir-part question that this deck answers (★ = 2019-20 or later):")
out = [q for q in QUESTIONS if q["file"] == "OUT" and "Ch3" in q["area"]]
out.sort(key=lambda q: -int(q["year"][:4]))
exam_map(n, 4, extra_rows=[[f"{q['year']} ({q['course']})" + (" ★" if int(q["year"][:4]) >= 2019 else ""), q["qno"], q["question"] + "  [Outside Notes]",
                            str(q["marks"]), "L23"] for q in out])
n.callout("focus", f"Arithmetic is asked in every paper ({marks_since(4)} marks since 2019-20 from the slides, plus the Lesson 23 rows). Three repeating types: "
          "(1) multiplication hardware — draw both versions, flowchart, trace (9 papers); (2) floating-point representation — custom 16/32-bit formats, bias, smallest/largest, hex ↔ decimal (13 rows); "
          "(3) FP addition steps / flowchart / traced example (7 papers). Division and MIPS FP code are not on the short slides but appear 4 + 4 times — do Lesson 23 too.")

# ================================================================== LESSON 19
n.lesson("Lesson 19 — Integer Addition, Subtraction and Overflow", "Slides 2–4 (§3.1–3.2)")
n.h2("1. Addition (sl. 3)")
n.code(["Example 7 + 6 (carries in brackets):",
        "      (0)(0)(1)(1)(0)        carries",
        "  …    0  0  1  1  1         7",
        "  …    0  0  1  1  0         6",
        "  …    0  1  1  0  1        13"])
n.h2("2. Subtraction (sl. 4)")
n.p("Subtraction adds the negation of the second operand: 7 − 6 = 7 + (−6) → 0000…0111 + 1111…1010 = 0000…0001.")
n.h2("3. Overflow Rules (sl. 3–4) ★")
n.table(["Operation", "Operand A", "Operand B", "Overflow if result sign is"], [
    ["A + B", "≥ 0", "≥ 0", "1 (negative)"], ["A + B", "< 0", "< 0", "0 (non-negative)"], ["A + B", "opposite signs", "", "never"],
    ["A − B", "≥ 0", "< 0", "1"], ["A − B", "< 0", "≥ 0", "0"], ["A − B", "same signs", "", "never"],
], widths_cm=[2.8, 3.0, 3.0, 8.4])
n.p("Overflow means the true result is outside the 2's-complement range −2^{n−1} … 2^{n−1} − 1. In hardware it is detected as V = C_{n} ⊕ C_{n+1} (Lesson 9).")
n.exam_approach(["Turn subtraction into addition of the negated B: A − B overflows exactly when A + (−B) would.",
                 "Fill the sign table row by row; write V as a sum of minterms (no simplification needed)."])
n.practice("Lesson 19", "(a) Actual — 2016-17 8(a) = 2014-15 8(a). (b) Constructed.", [
    "(a) The table lists O (0 = A + B, 1 = A − B), S_{A}, S_{B} (sign bits) and S_{R} (sign of the result). Identify the overflow conditions and write V as a Boolean function. (10/12)",
    "(b) 4-bit: does +5 + +4, −6 − +3, +5 − −2 overflow?",
])
n.solution()
n.table(["O", "S_{A}", "S_{B}", "Effective operation", "Overflow possible?", "V"], [
    ["0", "0", "0", "(+) + (+)", "yes, if S_{R} = 1", "S_{R}"], ["0", "0", "1", "(+) + (−)", "no", "0"], ["0", "1", "0", "(−) + (+)", "no", "0"],
    ["0", "1", "1", "(−) + (−)", "yes, if S_{R} = 0", "S_{R}'"], ["1", "0", "0", "(+) − (+)", "no", "0"], ["1", "0", "1", "(+) − (−) = (+) + (+)", "yes, if S_{R} = 1", "S_{R}"],
    ["1", "1", "0", "(−) − (+) = (−) + (−)", "yes, if S_{R} = 0", "S_{R}'"], ["1", "1", "1", "(−) − (−)", "no", "0"],
], widths_cm=[1.0, 1.2, 1.2, 4.6, 4.2, 1.6])
n.formula(["V = O'·S_{A}'·S_{B}'·S_{R} + O'·S_{A}·S_{B}·S_{R}' + O·S_{A}'·S_{B}·S_{R} + O·S_{A}·S_{B}'·S_{R}'"])
n.callout("note", "The printed definition says 'V = 0: overflow occurred, 1: no overflow possible' — that is clearly swapped (V = 1 must mean overflow). State the convention you use; the function above has V = 1 for overflow.")
n.answer("(b)", "+5 + 4 = 0101 + 0100 = 1001: positive + positive gives sign 1 → overflow (9 > 7). −6 − 3 = 1010 + 1101 = (1)0111: negative + negative gives sign 0 → overflow (−9 < −8). +5 − (−2) = 0101 + 0010 = 0111 = +7 → no overflow.")

# ================================================================== LESSON 20
n.lesson("Lesson 20 — Multiplication Hardware", "Slides 5–8 (§3.3)")
n.h2("1. Long Multiplication (sl. 5)")
n.code(["        1000      multiplicand (8)",
        "      × 1001      multiplier   (9)",
        "        1000",
        "       0000",
        "      0000",
        "     1000",
        "     1001000      product (72) — length of product = sum of operand lengths"])
n.h2("2. First Version of the Hardware (sl. 5–6) ★")
n.figure_from_pdf(CH3, 6, "Figure 20.1 — First multiplication algorithm (flowchart) and hardware (sl. 6)", clip=(0.0, 0.12, 1.0, 0.92), width_cm=15.0)
n.bullets(["64-bit **Multiplicand** register, initially the 32-bit multiplicand in the right half — shifts **left** each step.",
           "32-bit **Multiplier** register — shifts **right**; its bit 0 is tested.",
           "64-bit **ALU** and 64-bit **Product** register (initially 0).",
           "Control test repeats 32 times: 1. if Multiplier0 = 1 add Multiplicand to Product; 2. shift Multiplicand left 1; 3. shift Multiplier right 1."])
n.code(["Start → Test Multiplier0 ──1──► 1a. Product = Product + Multiplicand ─┐",
        "                       └──0────────────────────────────────────────────┤",
        "        2. Shift the Multiplicand register left 1 bit ◄────────────────┘",
        "        3. Shift the Multiplier register right 1 bit",
        "        32nd repetition? ── No (< 32) → back to Test   ── Yes → Done"])
n.h2("3. Optimized (Refined) Multiplier (sl. 7) ★")
n.figure_from_pdf(CH3, 7, "Figure 20.2 — Optimized multiplier: 32-bit multiplicand and ALU, 64-bit product shifting right (sl. 7)", clip=(0.0, 0.18, 1.0, 0.82), width_cm=13.0)
n.p("Observations that make it efficient: half of the 64-bit multiplicand register was always 0 and only 32 bits are added each step; the product shifts right as the multiplier shifts right; "
    "the product's empty right half can hold the multiplier. So:")
n.bullets(["Multiplicand and ALU become **32 bits**; the separate Multiplier register is **removed** — the multiplier is loaded into the right half of the 64-bit Product register.",
           "Each step: if Product0 = 1, add Multiplicand to the left half of Product (the carry is kept); then shift the whole Product right 1 bit. Add and shift happen in parallel → **one cycle per partial-product addition**.",
           "32 repetitions; the product is in the 64-bit register at the end."])
n.code(["Start → Test Product0 ──1──► 1a. Left half of Product = left half + Multiplicand ─┐",
        "                    └──0───────────────────────────────────────────────────────┤",
        "        2. Shift the Product register right 1 bit (carry enters MSB) ◄──────────┘",
        "        32nd repetition? ── No → back to Test   ── Yes → Done"])
n.callout("answer", "Why the first hardware is inefficient (2019-20 4(b)): it needs a 64-bit ALU and a 64-bit multiplicand register although only 32 bits are ever added, a separate multiplier register, "
          "and three sequential steps (add, shift, shift) per bit → about 3 × 32 cycles. Changes: halve the multiplicand register and ALU to 32 bits, shift the product right instead of the multiplicand left, "
          "put the multiplier in the unused right half of the product register, and do the add and the shift in the same cycle → 32 cycles, less hardware (draw Fig. 20.2).")
n.h2("4. MIPS Multiplication (sl. 8)")
n.bullets(["Two 32-bit registers hold the product: **HI** (most-significant 32 bits) and **LO** (least-significant 32 bits).",
           "`mult rs, rt` / `multu rs, rt` → 64-bit product in HI/LO (read with mfhi, mflo — textbook).",
           "`mul rd, rs, rt` → least-significant 32 bits of the product into rd."])
n.h2("5. Combined Multiply/Divide Hardware (textbook, for 2021-22 6(c))")
n.p("The refined multiplier and the refined divider (Lesson 23) have the same datapath, so one unit does both: a 32-bit **Multiplicand/Divisor** register, a 32-bit **ALU** (add for multiply, subtract for divide), "
    "a 64-bit **Product/Remainder** register that can shift **right** (multiply) and **left** (divide) and is written by the ALU into its left half, and a **control** unit that tests Product0 (multiply) or the sign of the ALU result (divide). "
    "MIPS exposes the 64-bit register as HI and LO: after mult HI:LO = product; after div LO = quotient, HI = remainder.")
n.exam_approach(["Draw both diagrams with register widths (64/32) and shift directions.", "Flowchart: test, add, shift(s), count 32 (or n) repetitions.",
                 "Trace table columns: Iteration | Step | Multiplier | Multiplicand | Product (first version) or Multiplicand | Product (refined). Use n-bit operands (n = 4 in exams)."])
n.practice("Lesson 20", "(a) Actual — 2023-24 7(a). (b) Actual — 2016-17 8(c). (c) Methods — 2022-23 Q4, 2018-19 5(a), 2014-15 8(b), 2013-14 3(c), 2011-12 6(a), 2021-22 6(c).", [
    "(a) Draw the integer multiplication hardware (i) long-multiplication approach and (ii) parallel add/shift approach for 32-bit operands. Simulate each for 1000 (multiplicand) × 1011 (multiplier). (20)",
    "(b) Using the refined hardware (32-bit multiplicand and ALU, 64-bit product shifting right), simulate unsigned 0110 × 0110. (15)",
    "(c) Draw hardware + flowchart of the sequential version and of the refined version; for 2013-14 3(c) 'no separate multiplier register' = the refined version.",
])
n.solution()
n.answer("(a)", "Diagrams: Fig. 20.1 (first) and Fig. 20.2 (refined). 4-bit traces (8 × 11 = 88 = 0101 1000):")
rows, _ = mult_v1(0b1000, 0b1011)
n.table(["Iter", "Step (first version)", "Multiplier", "Multiplicand", "Product"], [list(r) for r in rows], widths_cm=[1.0, 7.2, 2.2, 3.0, 3.0], font_size=8.5)
rows, _ = mult_v2(0b1000, 0b1011)
n.table(["Iter", "Step (refined version)", "Multiplicand", "Product (left | right = multiplier)"], [[r[0], r[1], r[2], r[3][:-4] + " " + r[3][-4:]] for r in rows], widths_cm=[1.0, 8.2, 2.6, 5.4], font_size=8.5)
n.formula("Product = 0101 1000 = 88 = 8 × 11 ✓")
n.answer("(b)", "")
rows, _ = mult_v2(0b0110, 0b0110)
n.table(["Iter", "Step", "Multiplicand", "Product"], [[r[0], r[1], r[2], r[3][:-4] + " " + r[3][-4:]] for r in rows], widths_cm=[1.0, 8.2, 2.6, 5.4], font_size=8.5)
n.formula("Product = 0010 0100 = 36 = 6 × 6 ✓")
n.answer("(c)", "§2 and §3 diagrams and flowcharts; the improvement list in the EXAM-READY box; for the combined unit §5.")

# ================================================================== LESSON 21
n.lesson("Lesson 21 — IEEE 754 Floating-Point Representation", "Slides 9–16 (§3.5)")
n.h2("1. Floating Point and the Standard (sl. 9–10)")
n.p("Floating point represents non-integral numbers, including very small and very large ones, like scientific notation: −2.34 × 10^{56} and +987.02 × 10^{9}… "
    "**Normalized** means exactly one non-zero digit before the point (−2.34 × 10^{56} yes; +0.002 × 10^{−4} and +987.02 × 10^{9} no). In binary: ±1.xxxxxxx_{2} × 2^{yyyy} (float and double in C). "
    "IEEE Std 754-1985 was developed because representations diverged (portability of scientific code); it is now almost universally adopted, with single (32-bit) and double (64-bit) precision.")
n.h2("2. Format (sl. 11) ★")
n.code(["single:  | S 1 | Exponent 8  | Fraction 23 |",
        "double:  | S 1 | Exponent 11 | Fraction 52 |"])
n.formula(["x = (−1)^{S} × (1 + Fraction) × 2^{(Exponent − Bias)}",
           "Bias: single 127, double 1023"])
n.bullets(["S = 0 non-negative, 1 negative.", "Significand normalized: 1.0 ≤ |significand| < 2.0. The leading 1 is always there, so it is not stored (**hidden bit**); significand = fraction with '1.' restored.",
           "Exponent in excess (biased) form: stored = actual + bias, so the field is unsigned."])
n.callout("answer", "Why a (positive) bias (2023-24 7(b), 2018-19 7(c), 2015-16 7(c), 2012-13 8(a), 2020-21 13(a)(i)): with a bias the exponent field is an **unsigned** number — most negative exponent 00…01, most positive 11…10. "
          "Then two FP numbers of the same sign can be compared (and sorted) with **integer comparison hardware**, bit pattern by bit pattern, because a larger exponent always gives a larger field. "
          "2's-complement exponents would make negative exponents look larger. The bias 2^{e−1} − 1 makes the range of exponents roughly symmetric.")
n.h2("3. Ranges and Precision (sl. 12–14)")
n.table(["", "Single", "Double"], [
    ["Reserved exponent fields", "00000000 and 11111111", "000…00 and 111…11"],
    ["Smallest normalized", "exp field 1 → 1 − 127 = −126; ±1.0 × 2^{−126} ≈ ±1.2 × 10^{−38}", "exp 1 → −1022; ±1.0 × 2^{−1022} ≈ ±2.2 × 10^{−308}"],
    ["Largest", "exp 254 → +127; ±(2 − 2^{−23}) × 2^{127} ≈ ±3.4 × 10^{38}", "exp 2046 → +1023; ±(2 − 2^{−52}) × 2^{1023} ≈ ±1.8 × 10^{308}"],
    ["Relative precision", "2^{−23} → 23 × log_{10}2 ≈ 6 decimal digits", "2^{−52} → ≈ 16 decimal digits"],
    ["Smallest denormal (textbook)", "2^{−23} × 2^{−126} = 2^{−149} ≈ 1.4 × 10^{−45}", "2^{−1074} ≈ 4.9 × 10^{−324}"],
], widths_cm=[3.8, 6.9, 6.5], font_size=9)
n.h2("4. Special Values (textbook — needed for infinity, NaN and denormal questions)")
n.table(["Exponent field", "Fraction", "Meaning"], [
    ["0", "0", "±0"], ["0", "≠ 0", "Denormal: ±0.Fraction × 2^{1 − bias} (gradual underflow)"],
    ["1 … max − 1", "anything", "Normalized ±1.Fraction × 2^{E − bias}"],
    ["all 1s", "0", "±infinity: single 0 11111111 000…0 = 0x7F800000 (−∞ = 0xFF800000)"],
    ["all 1s", "≠ 0", "NaN (not a number), e.g. 0/0, ∞ − ∞"],
], widths_cm=[3.2, 2.4, 11.6])
n.h2("5. Worked Examples (sl. 15–16)")
n.code(["Represent −0.75:  −0.75 = (−1)^1 × 1.1_2 × 2^−1",
        "   S = 1, Fraction = 1000…00, Exponent = −1 + 127 = 126 = 01111110 (double: −1 + 1023 = 01111111110)",
        "   single: 1 01111110 1000…00 = 0xBF400000      double: 1 01111111110 1000…00",
        "Decode 1 10000001 01000…00:  S = 1, Fraction = 0.01_2 = 0.25, Exponent = 129",
        "   x = (−1) × (1 + 0.25) × 2^(129 − 127) = −1.25 × 4 = −5.0"])
n.h2("6. Recipe for a Custom Format (16-bit, 32-bit with other field sizes) ★")
n.numbered(["e = exponent bits, f = fraction bits, 1 + e + f = total. Bias = 2^{e−1} − 1 (unless the question fixes the range).",
            "Normalized exponents: 1 − bias … (2^{e} − 2) − bias (fields 00…0 and 11…1 reserved).",
            "Smallest normalized = 1.0 × 2^{1 − bias}; largest = (2 − 2^{−f}) × 2^{2^{e} − 2 − bias}.",
            "Smallest denormal = 2^{−f} × 2^{1 − bias}. Precision = 2^{−f} ≈ f × 0.301 decimal digits.",
            "Encode: normalize to 1.xxx × 2^{k}; field = k + bias in e bits; fraction = bits after the point, padded to f bits."])
n.exam_approach(["Write the format box first (S | E | F with widths).", "Show normalization, biased exponent, fraction padding, then group in 4s → hex.",
                 "Decode: split fields, check for special exponents, then (−1)^{S}(1 + F)2^{E − bias}."])
n.practice("Lesson 21", "(a) Actual — 2019-20 4(a). (b) Actual — 2022-23 (CSE 305) 8(b) and 2020-21 13(a). (c) Actual — 2018-19 5(b). (d) Actual — 2018-19 5(c), 2017-18 5(c), 2013-14 3(b). "
           "(e) Actual — 2023-24 7(b). (f) Actual — 2021-22 8(b). (g) Actual — 2022-23 (CSE 305) 8(c).", [
    "(a) 16-bit FP; largest absolute value 1.11…1 × 2^{63}, smallest 1.00…0 × 2^{−62}. (i) Field sizes. (ii) Represent −110.11_{2} × 2^{1}. (iii) Smallest denormalized value. (15)",
    "(b) 32-bit FP with 1 sign bit and (i) 19 fraction bits, (ii) 24 fraction bits, the rest exponent: precision, bias, smallest and largest absolute values, smallest denormal. (8 / 16)",
    "(c) 16-bit FP with a 4-bit exponent: represent −1.25 and 0.375. (8)",
    "(d) Decimal value of IEEE single 0xDF807500 and of 0x7F800005; single representation of −0.75. (5 / 5 / 10)",
    "(e) Purpose of a positive bias; smallest and largest values in single and double precision. (15)",
    "(f) Largest n such that every integer 1, 2, …, n is representable in IEEE single precision. (14)",
    "(g) f1 < f2 are normalized IEEE singles. Treated as unsigned integers i1, i2 — is i1 < i2? As signed integers j1, j2 — is j1 < j2? (20)",
])
n.solution()
n.answer("(a)", "Exponents −62 … +63 = 126 normalized values + 2 reserved = 128 = 2^{7} → **7 exponent bits**, bias 63 (field 1 → −62, field 126 → +63); fraction = 16 − 1 − 7 = **8 bits** (the largest has eight 1s after the point).")
n.code(["(i)   | S 1 | E 7 (bias 63) | F 8 |",
        "(ii)  −110.11_2 × 2^1 = −1.1011_2 × 2^3 → S = 1, E = 3 + 63 = 66 = 1000010, F = 10110000",
        "      1 1000010 10110000 = 1100 0010 1011 0000 = 0xC2B0   (value −13.5)",
        "(iii) smallest denormal = 0.00000001_2 × 2^(1 − 63) = 2^−8 × 2^−62 = 2^−70 ≈ 8.5 × 10^−22"])
n.answer("(b)", "")
n.table(["", "(i) 19-bit fraction (2022-23)", "(ii) 24-bit fraction (2020-21)"], [
    ["Exponent bits, bias", "32 − 1 − 19 = 12 → bias 2^{11} − 1 = 2047", "32 − 1 − 24 = 7 → bias 2^{6} − 1 = 63"],
    ["Precision", "2^{−19} ≈ 1.9 × 10^{−6} (≈ 5.7 decimal digits)", "2^{−24} ≈ 6 × 10^{−8} (≈ 7.2 digits)"],
    ["Smallest normalized", "1.0 × 2^{1 − 2047} = 2^{−2046}", "1.0 × 2^{−62}"],
    ["Largest", "(2 − 2^{−19}) × 2^{4094 − 2047} = (2 − 2^{−19}) × 2^{2047}", "(2 − 2^{−24}) × 2^{63} ≈ 1.84 × 10^{19}"],
    ["Smallest denormal", "2^{−19} × 2^{−2046} = 2^{−2065}", "2^{−24} × 2^{−62} = 2^{−86}"],
], widths_cm=[3.6, 7.0, 6.6], font_size=9)
n.answer("(c)", "4-bit exponent → bias 7, fraction 16 − 1 − 4 = 11 bits.")
n.code(["−1.25 = −1.01_2 × 2^0  → S 1, E 0 + 7 = 0111, F 01000000000 → 1 0111 01000000000 = 0xBA00",
        " 0.375 = 1.1_2 × 2^−2   → S 0, E −2 + 7 = 0101, F 10000000000 → 0 0101 10000000000 = 0x2C00"])
n.answer("(d)", "")
n.code(["0xDF807500 = 1101 1111 1000 0000 0111 0101 0000 0000",
        "  S = 1, E = 1011 1111 = 191 → 191 − 127 = 64, F = 000 0000 0111 0101 0000 0000 = 0x007500",
        "  x = −(1 + 0x7500 / 2^23) × 2^64 = −1.0035705566… × 2^64 ≈ −1.8513 × 10^19",
        "0x7F800005 = 0 11111111 000 0000 0000 0000 0000 0101 → exponent all 1s, fraction ≠ 0 → NaN",
        "−0.75 (2013-14 3(b)) = 1 01111110 1000…0 = 0xBF400000 (slide 15)"])
n.answer("(e)", "Bias: EXAM-READY box in §2. Values: table in §3 — single smallest normalized ±2^{−126} ≈ ±1.18 × 10^{−38}, largest ±(2 − 2^{−23}) × 2^{127} ≈ ±3.40 × 10^{38}; "
         "double ±2^{−1022} ≈ ±2.23 × 10^{−308} and ±(2 − 2^{−52}) × 2^{1023} ≈ ±1.80 × 10^{308} (denormals go down to 2^{−149} and 2^{−1074}).")
n.answer("(f)", "An integer k is exact when its binary form fits in the 24-bit significand (1 hidden + 23 fraction bits). Every integer up to 2^{24} = 16,777,216 fits "
         "(2^{24} itself is 1.0 × 2^{24}). 2^{24} + 1 = 1.000…0001 × 2^{24} needs 25 significant bits → it rounds to 2^{24}. So **n = 2^{24} = 16,777,216** (checked numerically).")
n.answer("(g)", "")
n.table(["Case", "Unsigned i1 < i2?", "Signed j1 < j2?"], [
    ["0 ≤ f1 < f2", "Yes — sign 0, biased exponent then fraction order = integer order", "Yes — both non-negative integers, same order"],
    ["f1 < 0 ≤ f2", "No — i1 has MSB 1, so i1 > i2", "Yes — j1 is negative, j2 non-negative"],
    ["f1 < f2 < 0", "No — sign-magnitude: |f1| > |f2| makes i1 > i2", "No — larger magnitude bits give the larger (less negative) j: j1 > j2"],
], widths_cm=[3.0, 7.2, 7.0], font_size=9)
n.p("So neither conclusion holds in general. (i) holds only when both are non-negative; (ii) fails when both are negative. Example: f1 = −3.0 (0xC0400000), f2 = −1.0 (0xBF800000): unsigned 0xC0400000 > 0xBF800000 and signed −1,069,547,520 > −1,082,130,432.")

# ================================================================== LESSON 22
n.lesson("Lesson 22 — Floating-Point Addition and the FP Adder", "Slides 17–20 (§3.5; printed 19–22)")
n.h2("1. Decimal Example (sl. 17)")
n.code(["9.999 × 10^1 + 1.610 × 10^−1   (4 significant digits)",
        "1. Align decimal points: shift the number with the smaller exponent → 0.016 × 10^1",
        "2. Add significands:     9.999 × 10^1 + 0.016 × 10^1 = 10.015 × 10^1",
        "3. Normalize & check over/underflow: 1.0015 × 10^2",
        "4. Round and renormalize if necessary: 1.002 × 10^2"])
n.h2("2. Binary Example (sl. 18)")
n.code(["1.000_2 × 2^−1 + −1.110_2 × 2^−2     (0.5 + −0.4375)",
        "1. Align: −1.110 × 2^−2 → −0.111 × 2^−1",
        "2. Add:   1.000 × 2^−1 + −0.111 × 2^−1 = 0.001 × 2^−1",
        "3. Normalize: 1.000 × 2^−4, with no over/underflow (−126 ≤ −4 ≤ 127)",
        "4. Round: 1.000 × 2^−4 (no change) = 0.0625"])
n.h2("3. Flowchart and Exception Conditions ★")
n.code(["Start",
        "1. Compare exponents; shift the significand of the smaller number right until the exponents match",
        "2. Add the significands (with signs)",
        "3. Normalize: shift the sum right & increment exponent, or shift left & decrement exponent",
        "   → Overflow or underflow?  ── Yes → exception (∞ / denormal or 0)",
        "4. Round the significand to the available bits",
        "   → Still normalized? ── No → back to step 3",
        "Done"])
n.table(["Condition", "When (single precision)"], [
    ["Overflow", "after normalizing, the exponent is > 127 (field would be 255) → result ±∞"],
    ["Underflow", "after normalizing, the exponent is < −126 → denormal or 0"],
    ["Infinity result", "an operand is ±∞ (∞ + x = ∞), or overflow"],
    ["NaN result", "an operand is NaN, or (+∞) + (−∞)"],
], widths_cm=[3.6, 13.6])
n.h2("4. FP Adder Hardware (sl. 19–20)")
n.p("The FP adder is much more complex than an integer adder. Doing it in one clock cycle would take too long (much longer than integer operations) and a slower clock would penalize all instructions, "
    "so the FP adder usually takes several cycles and can be pipelined.")
n.figure_from_pdf(CH3, 20, "Figure 22.1 — FP adder: small ALU (exponent difference), shift right, big ALU, normalize, round (sl. 20)", clip=(0.1, 0.16, 0.72, 0.93), width_cm=10.5)
n.bullets(["Step 1: the **small ALU** subtracts the exponents; the difference controls the muxes and the **shift-right** unit that aligns the smaller significand.",
           "Step 2: the **big ALU** adds the significands.",
           "Step 3: **normalize** — the leading-zero logic shifts left or right and the **increment/decrement** unit adjusts the exponent.",
           "Step 4: **rounding hardware**; if rounding de-normalizes the result, go back to step 3."])
n.exam_approach(["Convert both numbers to normalized binary (enough fraction bits).", "Align the smaller exponent to the larger one by shifting its significand right.",
                 "Add with signs, normalize, check the exponent range, round to the format's fraction bits.", "Give the final bit pattern and its decimal value as a check."])
n.practice("Lesson 22", "(a) Actual — 2016-17 7(b). (b) Actual — 2017-18 5(b). (c) Actual — 2022-23 1(a), 2018-19 8(b), 2015-16 6(a), 2013-14 3(a), 2011-12 5(a).", [
    "(a) Using the FP adder hardware, simulate −(0.25) + (0.625) by filling: binary, step 1 exponent matching, step 2 significand addition, step 3 normalization, step 4 rounding. (15)",
    "(b) 16-bit half precision with a 4-bit exponent: convert 0.75 and 1.25 and add them step by step, giving the exponent and fraction fields at every step. (15)",
    "(c) Steps of FP addition (flowchart) with an example; overflow, underflow, NaN and infinity conditions. (10–12)",
])
n.solution()
n.answer("(a)", "")
n.table(["", "−(0.25)_{10}", "(0.625)_{10}"], [
    ["Binary", "−1.000 × 2^{−2}  (1 01111101 000…0)", "1.010 × 2^{−1}  (0 01111110 010…0)"],
    ["Step 1: exponent matching", "−0.100 × 2^{−1} (shift right 1, exp −2 → −1)", "1.010 × 2^{−1} (unchanged)"],
    ["Step 2: significand addition", "1.010 + (−0.100) = 0.110 × 2^{−1}", ""],
    ["Step 3: normalization", "0.110 × 2^{−1} = 1.100 × 2^{−2}; −126 ≤ −2 ≤ 127 → no over/underflow", ""],
    ["Step 4: rounding", "1.100 × 2^{−2} (no change) = 0 01111101 1000…0 = 0x3EC00000 = 0.375", ""],
], widths_cm=[4.2, 7.0, 6.0], font_size=9)
n.answer("(b)", "Bias 7, 11 fraction bits.")
n.code(["0.75 = 1.1_2 × 2^−1  → S 0, E 0110 (6), F 10000000000   = 0x3400",
        "1.25 = 1.01_2 × 2^0  → S 0, E 0111 (7), F 01000000000   = 0x3A00",
        "Step 1 (align): exponents 6 < 7 → shift 0.75: 1.10000000000 × 2^−1 → 0.11000000000 × 2^0, E = 0111",
        "Step 2 (add):   1.01000000000 + 0.11000000000 = 10.00000000000 × 2^0",
        "Step 3 (normalize): 1.00000000000 × 2^1 → E = 1 + 7 = 1000; 1 ≤ 8 ≤ 14 → no overflow/underflow",
        "Step 4 (round): no bits were lost → F = 00000000000",
        "Result: 0 1000 00000000000 = 0x4000 = 2.0 ✓"])
n.answer("(c)", "Flowchart and condition table in §3 with the slide-18 binary example (0.5 + −0.4375 = 0.0625).")

# ================================================================== LESSON 23
n.lesson("Lesson 23 — Beyond the Short Slides (textbook insurance)", "Not on Tushar Sir's short slides — P&H §3.3–3.6. Asked: division ×4, MIPS FP code ×4, signed multiplication, guard/round/sticky, subword parallelism")
n.callout("note", "These questions are in the tracker's Outside Notes tab because the short slides do not cover them. Division and FP code were asked as recently as 2022-23 (CSE 209 1(b), CSE 305 8(a)) — ask sir whether they are in this term's syllabus.")
n.h2("1. Division Hardware and Algorithm (§3.4)")
n.p("First version: 64-bit **Divisor** register (divisor starts in the LEFT half) shifting right, 64-bit ALU, 64-bit **Remainder** register (initially the dividend), 32-bit **Quotient** shifting left. 33 repetitions:")
n.code(["1. Remainder = Remainder − Divisor",
        "2. Test Remainder:  ≥ 0 → shift Quotient left, set new rightmost bit 1",
        "                    < 0 → restore: Remainder = Remainder + Divisor; shift Quotient left, new bit 0",
        "3. Shift Divisor right 1 bit;   33rd repetition? No → step 1, Yes → Done"])
n.p("Refined version (the hardware of 2012-13 8(b)): 32-bit Divisor, **32-bit ALU**, 64-bit Remainder register that shifts left; the quotient bits enter its right half. "
    "Algorithm: shift Remainder left 1; repeat n times {left half − Divisor; if ≥ 0 keep it and shift left with new bit 1, else restore and shift left with new bit 0}; finally shift the left half right 1 bit. "
    "Then left half = remainder, right half = quotient. It needs the dividend's upper half < divisor (otherwise the quotient overflows n bits).")
n.h3("2022-23 1(b) ★ — 6-bit ALU: 1011 1100 1111 ÷ 110101 (3023 ÷ 53)")
rows, q, rm = div_v2(0b101111001111, 0b110101, 6)
n.table(["Iter", "Step (refined, 6-bit ALU)", "Divisor", "Remainder register (left | right)"],
        [[r[0], r[1], r[2], (r[3] if " " in r[3] else r[3][:-6] + " | " + r[3][-6:])] for r in rows], widths_cm=[1.0, 8.4, 2.2, 5.6], font_size=8.5)
n.formula("Quotient = 111001 = 57, Remainder = 000010 = 2   (57 × 53 + 2 = 3023 ✓)")
n.h3("2018-19 6(b) — 4-bit: 11001001 ÷ 1011 (201 ÷ 11), first version")
rows, q, rm = div_v1(0b11001001, 0b1011, 4)
n.table(["Iter", "Step", "Quotient", "Divisor", "Remainder"], [list(r) for r in rows], widths_cm=[1.0, 8.2, 2.0, 3.0, 3.0], font_size=8.2)
n.formula("Quotient = 10010 = 18, Remainder = 0011 = 3   (18 × 11 + 3 = 201 ✓)")
n.p("Note: the dividend's upper half 1100 ≥ divisor 1011, so the quotient needs 5 bits — with the refined 4-bit hardware this is a divide overflow; the first version (5 iterations) handles it.")
n.h3("2017-18 8(a) — 11010101 ÷ 1011 (213 ÷ 11), first version")
rows, q, rm = div_v1(0b11010101, 0b1011, 4)
n.table(["Iter", "Step", "Quotient", "Divisor", "Remainder"], [list(r) for r in rows], widths_cm=[1.0, 8.2, 2.0, 3.0, 3.0], font_size=8.2)
n.formula("Quotient = 10011 = 19, Remainder = 0100 = 4   (19 × 11 + 4 = 213 ✓)")
n.h2("2. Signed Multiplication (2020-21 10(c))")
n.p("Simplest method: remember the signs, convert both operands to positive (2's-complement negate the negative ones), multiply the magnitudes with the unsigned algorithm for 31 iterations, "
    "and negate the product if the original signs differed (sign = S_{A} ⊕ S_{B}). Alternatively, sign-extend the partial products and treat the last step as a subtraction (Booth's algorithm: "
    "look at multiplier bits (b_{i}, b_{i−1}): 10 → subtract multiplicand, 01 → add, 00/11 → only shift, using arithmetic right shifts) — this works directly on 2's-complement numbers.")
n.h2("3. MIPS Floating-Point Instructions and Code (§3.5)")
n.bullets(["Separate FP registers $f0–$f31; a double uses an even/odd pair ($f0/$f1 …).",
           "Arithmetic: add.s / add.d, sub.s / sub.d, mul.s / mul.d, div.s / div.d. Loads/stores: lwc1 / swc1 (single), ldc1 / sdc1 (double).",
           "Compare: c.xx.s / c.xx.d (xx = eq, lt, le) sets a condition bit; branch with bc1t (true) / bc1f (false)."])
n.h3("2022-23 (CSE 305) 8(a) = 2020-21 13(c) ★: float a, b, c; double w, x, y, z; if (a + b > c) x = (y*z)/w;")
n.code(["# a $f0, b $f1, c $f2 (single);  w $f4, x $f6, y $f8, z $f10 (double pairs)",
        "      add.s  $f3, $f0, $f1      # f3 = a + b",
        "      c.le.s $f3, $f2           # (a + b) <= c ?",
        "      bc1t   Skip               # yes → condition false, skip",
        "      mul.d  $f12, $f8, $f10    # y * z",
        "      div.d  $f6, $f12, $f4     # x = (y * z) / w",
        "Skip:"])
n.h3("2019-20 4(c) ★: double; if (a > b) c = c − (c*e)/d; else c = c + d;  (a $f2, b $f4, c $f6, d $f8, e $f10)")
n.code(["      c.le.d $f2, $f4           # a <= b ?",
        "      bc1t   Else",
        "      mul.d  $f12, $f6, $f10    # c * e",
        "      div.d  $f12, $f12, $f8    # (c * e) / d",
        "      sub.d  $f6, $f6, $f12     # c = c - (c*e)/d",
        "      j      Exit",
        "Else: add.d  $f6, $f6, $f8      # c = c + d",
        "Exit:"])
n.h3("2017-18 8(b): float convert(float cels) { return 9.0*cels/5.0 + 32.0; }  (cels in $f12, result in $f0)")
n.code(["convert: lwc1  $f16, const9($gp)   # 9.0 from static data",
        "         lwc1  $f18, const5($gp)   # 5.0",
        "         mul.s $f16, $f16, $f12    # 9.0 * cels",
        "         div.s $f16, $f16, $f18    # / 5.0",
        "         lwc1  $f18, const32($gp)  # 32.0",
        "         add.s $f0, $f16, $f18     # + 32.0",
        "         jr    $ra"])
n.h2("4. Guard, Round and Sticky Bits (2020-21 12(c))")
n.p("During alignment and normalization, bits shifted out of the significand would be lost. IEEE 754 keeps two extra bits on the right during the operation — **guard** and **round** — so that the result can be rounded "
    "as if it had been computed exactly and then rounded. Example with 3 significant decimal digits: 2.56 × 10^{0} + 2.34 × 10^{2}: with guard/round digits 2.3400 + 0.0256 = 2.3656 → rounds to 2.37; "
    "without them 2.34 + 0.02 = 2.36 (an error of 1 in the last digit). The **sticky bit** is set if any nonzero bit was shifted beyond the round bit; it tells round-to-nearest-even whether the "
    "discarded part is exactly half (…100…0) or more than half, so ties are broken correctly. Together they give results accurate to ½ unit in the last place.")
n.h2("5. Subword Parallelism (2021-22 5(c))")
n.p("A wide (64/128-bit) adder can be partitioned so that one instruction operates on many short operands at once: 16 × 8-bit, 8 × 16-bit, 4 × 32-bit or 2 × 64-bit (SIMD — MMX/SSE/AVX, ARM NEON). "
    "Image processing works on 8-bit pixels, so 16 pixels are added, averaged or saturated in one instruction; matrix multiplication uses packed multiply-add on 4 floats/doubles at a time, "
    "turning the inner loop into one quarter (or less) of the scalar instructions with the same hardware.")

n.quick_notes("Quick Notes — Arithmetic", "Revision points for Lessons 19–23.", [
    ("L19 · Add/sub overflow", [
        "Add overflow: (+)+(+) → sign 1; (−)+(−) → sign 0. Subtract: (+)−(−) → 1; (−)−(+) → 0. Never for opposite-sign add / same-sign subtract.",
        "V = O'S_{A}'S_{B}'S_{R} + O'S_{A}S_{B}S_{R}' + OS_{A}'S_{B}S_{R} + OS_{A}S_{B}'S_{R}'.",
    ]),
    ("L20 · Multiplication", [
        "First: 64-bit multiplicand ←, 32-bit multiplier →, 64-bit ALU & product; add, shift, shift × 32.",
        "Refined: 32-bit multiplicand & ALU, multiplier in right half of 64-bit product, add then shift product → (1 cycle/step).",
        "HI/LO; mult/multu → HI:LO; mul → low 32 bits. Combined mult/div: same refined datapath, product register shifts both ways.",
    ]),
    ("L21 · IEEE 754", [
        "x = (−1)^{S}(1 + F)2^{E − bias}; single 1/8/23 bias 127; double 1/11/52 bias 1023.",
        "Single 2^{−126} … (2 − 2^{−23})2^{127}; denormal 2^{−149}. ∞: E all 1s, F = 0 (0x7F800000). NaN: E all 1s, F ≠ 0.",
        "Bias → unsigned exponent → integer comparison works. Custom: bias 2^{e−1} − 1; min 2^{1−bias}; max (2 − 2^{−f})2^{2^{e}−2−bias}; denorm 2^{−f}·2^{1−bias}.",
        "−0.75 = 0xBF400000; 0xC0A00000 = −5.0; 0xDF807500 ≈ −1.85 × 10^{19}; integers exact up to 2^{24}.",
    ]),
    ("L22 · FP addition", [
        "Align (shift smaller right) → add → normalize + check over/underflow → round (→ renormalize).",
        "−0.25 + 0.625 = 1.1 × 2^{−2} = 0.375; half precision 0.75 + 1.25 = 0x4000 = 2.0.",
    ]),
    ("L23 · Textbook extras", [
        "Division: subtract, test sign, restore or set 1, shift; refined: remainder register shifts left, quotient enters right half; final left-half shift right.",
        "3023/53 = 57 r 2; 201/11 = 18 r 3; 213/11 = 19 r 4.",
        "FP code: add.s/d, mul, div, c.le.s + bc1t; doubles in even registers.",
        "Guard + round + sticky → correct rounding; subword parallelism = partitioned adder (SIMD).",
    ]),
], diagrams=[
    (CH3, 7, "Optimized multiplier (sl. 7) — same as Fig. 20.2", (0.0, 0.18, 1.0, 0.82), 12.0),
    (CH3, 20, "FP adder hardware (sl. 20) — same as Fig. 22.1", (0.1, 0.16, 0.72, 0.93), 9.0),
])
print(n.save())
