"""MATH243_KKS_Random_Variables_Notes.docx — Lectures 6, 7, 9 (pp. 1–5) + Chebyshev (L7–L9)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from math import comb, exp

import sympy as sp

from common import exam_map, new
from m243 import PROB, fr, g

x = sp.symbols("x", real=True)
OTHER = PROB + r"\Lecture on other distributions...pdf"


def S(e):
    return g(float(e))


n = new("KKS", "Random Variables: pmf, pdf, CDF, Expectation, Variance and Chebyshev",
        "MATH243_KKS_Random_Variables_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "pdf/CDF, exponential and expectation questions"),
              ("Lesson 7 — Random Variables and the Probability Mass Function", "discrete/continuous, pmf conditions, k-problems"),
              ("Lesson 8 — Density Function and Distribution Function (CDF)", "pdf, F(x), continuous k-problems, exponential"),
              ("Lesson 9 — Expectation, Variance and Chebyshev's Theorem", "E(X), V(X), E[g(X)], aX + b, Chebyshev"),
              ("Quick Notes — Random Variables", "revision bullets")],
    source_note="Page numbers refer to KKS Sir's Lecture 6.pdf (7 pp.), Lecture 7.pdf (8 pp.), Lecture 9.pdf (9 pp.) and "
                "Lecture on other distributions...pdf (10 pp. of Walpole, Myers, Myers & Ye, 9th ed.; Chebyshev on p. 1). "
                "The exponential distribution is asked in TF but is not in the lectures; it is taught here from the "
                "textbook and marked. \"TF p.\" = page of the merged question PDF; \"22 batch p.\" = 2023-24 paper.")

n.h1("Exam Map — What the TF Papers Ask")
st = exam_map(n, "k3")
n.callout("focus", f"{st['n']} questions, {st['marks']} marks — {st['n_hi']} of them ({st['marks_hi']} marks) since "
          "2019-20, so this is the heaviest probability note. Three types repeat: (1) find k / the CDF / a probability "
          "from a density; (2) exponential waiting times (2019-20, 2022-23, 2023-24); (3) E[g(X)], mean and variance "
          "of aX + b, and Chebyshev (2022-23, 2023-24). Learn the integration steps and the three formulas "
          "E(X) = ∫x f, V(X) = E(X²) − μ², F(x) = ∫f.")

# ------------------------------------------------------------------ L7
n.lesson("Lesson 7 — Random Variables and the Probability Mass Function", "Lec 6 pp. 1–7")
n.h2("1. Random Variable (Lec 6 p. 1)")
n.p("A **random variable** is a variable whose values are numbers that arise from chance, so that they cannot be "
    "predicted exactly in advance. It can be viewed as a function from the sample space to the real numbers. "
    "Example: a committee of 2 from 4 male and 3 female teachers; Y = number of males takes the values 2 (M, M), "
    "1 (M, F), 0 (F, F).")
n.table(["Type", "Definition", "Examples"],
        [["Discrete", "finite or countable set of isolated values", "telephone calls per day; under-five children in a family"],
         ["Continuous", "any value in an interval", "weight of a six-month-old baby; life of an electric bulb"]],
        widths_cm=[2.6, 6.6, 8])
n.h2("2. Probability Distribution (Lec 6 p. 2)")
n.p("A probability distribution associates each value (or class) of a random variable with its probability. Discrete "
    "examples: Bernoulli, binomial, Poisson. Continuous examples: uniform, normal, exponential.")
n.h3("Example 1 — black balls: 10 balls, 4 black, 3 drawn without replacement (Lec 6 pp. 2–3)")
n.code(["f(x) = 4Cx × 6C(3−x) / 10C3,  10C3 = 120",
        "x     :    0        1        2        3",
        "f(x)  :  20/120   60/120   36/120   4/120     (total 1)"])
n.h3("Example 2 — number of runs in three tosses (Lec 6 pp. 3–4)")
n.p("A run is a maximal block of identical consecutive outcomes. HHH, TTT → 1 run; HHT, HTT, THH, TTH → 2 runs; "
    "HTH, THT → 3 runs. So P(X = 1) = 2/8, P(X = 2) = 4/8, P(X = 3) = 2/8.")
n.callout("note", "The slide's outcome table lists THH twice; the eighth outcome is THT (3 runs). The final "
          "distribution 2/8, 4/8, 2/8 is correct.")
n.h2("3. The pmf and its Conditions (Lec 6 p. 4)")
n.formula(["f(x) = P(X = x)", "(1) f(x) ≥ 0   (2) Σ f(x) = 1"])
n.table(["Function", "Check", "pmf?"],
        [["(2x − 1)/8, x = 0, 1, 2, 3", "sum = (−1 + 1 + 3 + 5)/8 = 1, but f(0) = −1/8 < 0", "No"],
         ["(3x + 6)/21, x = 1, 2", "9/21 + 12/21 = 1, all positive", "Yes"],
         ["(x + 1)/16, x = 0, 1, 2, 3", "(1 + 2 + 3 + 4)/16 = 10/16 ≠ 1", "No"]], widths_cm=[5, 9.2, 3])
n.callout("note", "The slide prints (b) as \"(3x=6)/8\"; its own sum 9/21 + 12/21 shows the function is (3x + 6)/21.")
n.h2("4. Finding k (Lec 6 pp. 5–7)")
k = F(1, 10)
n.p("X = 0, …, 7 with P = 0, k, 2k, 2k, 3k, k², 2k², 7k² + k. Σ = 10k² + 9k = 1 → (10k − 1)(k + 1) = 0 → k = 1/10 "
    "(k = −1 is impossible).")
n.code([f"P(X ≤ 6) = 1 − P(X = 7) = 1 − (7k² + k) = 1 − 17/100 = 83/100",
        f"P(3 < X ≤ 6) = P(4) + P(5) + P(6) = 3k + k² + 2k² = 0.30 + 0.01 + 0.02 = 33/100"])
n.p("Geometric-type pmf f(x) = α(3/4)^{x}, x = 0, 1, 2, …: Σ = α/(1 − 3/4) = 4α = 1 → α = 1/4, so f(x) = (1/4)(3/4)^{x} "
    "and P(X ≤ 3) = (1/4)(1 + 3/4 + 9/16 + 27/64) = 175/256. (The slide writes (1/4)(1/4)^{x} by a slip.)")
ex = []
for lab, vals, fun in (("kx; x = 1, 2, 3, 4", [1, 2, 3, 4], lambda v: v),
                       ("k(x² + 1); x = 0, 1, 2, 4", [0, 1, 2, 4], lambda v: v * v + 1),
                       ("k(x + 2); x = −1, 0, 1, 2, 4", [-1, 0, 1, 2, 4], lambda v: v + 2)):
    tot = sum(fun(v) for v in vals)
    ex.append((lab, vals, fun, tot))
n.h3("Exercises of Lecture 6 (p. 7) — answers")
n.table(["pmf", "Σ → k", "Probabilities asked"],
        [[ex[0][0], f"{ex[0][3]}k = 1 → k = 1/{ex[0][3]}", "P(X = 3) = 3/10; P(X > 2) = 7/10"],
         [ex[1][0], f"{ex[1][3]}k = 1 → k = 1/{ex[1][3]}", "P(X = 2) = 5/25 = 0.2; P(X ≥ 2) = 22/25; P(X ≤ 1) = 3/25"],
         [ex[2][0], f"{ex[2][3]}k = 1 → k = 1/{ex[2][3]}", "P(X < 1) = 3/16; P(X ≥ 0) = 15/16"]], widths_cm=[4.8, 4, 8.4])
n.exam_approach(["List the possible values of X and find each probability (counting, or by formula).",
                 "Check f(x) ≥ 0 and Σ f(x) = 1; solve Σ f(x) = 1 for an unknown constant, rejecting negative roots.",
                 "Add the required f(x); use the complement when it is shorter."])
n.practice("Lesson 7", "Constructed (Lec 6 exercise types).",
           ["(a) Two pens are chosen from 3 red and 5 black. Find the distribution of X = number of red pens.",
            "(b) f(x) = c(x + 1)², x = 0, 1, 2. Find c and P(X ≥ 1)."])
n.solution()
n.answer("(a)", "8C2 = 28. f(0) = 5C2/28 = 10/28, f(1) = 3 × 5/28 = 15/28, f(2) = 3C2/28 = 3/28 (sum 1).")
n.answer("(b)", "c(1 + 4 + 9) = 1 → c = 1/14; P(X ≥ 1) = 1 − 1/14 = 13/14.")

# ------------------------------------------------------------------ L8
n.lesson("Lesson 8 — Density Function and Distribution Function (CDF)", "Lec 7 pp. 1–8 · exponential: textbook")
n.h2("1. Discrete CDF (Lec 7 pp. 1–3)")
n.formula("F(x) = P(X ≤ x) = Σ_{t ≤ x} f(t)")
n.p("F is non-decreasing, 0 ≤ F(x) ≤ 1, F(−∞) = 0, F(∞) = 1, and it is a step function for a discrete X.")
n.code(["Black balls:     x < 0: 0 | 0 ≤ x < 1: 20/120 | 1 ≤ x < 2: 80/120 | 2 ≤ x < 3: 116/120 | x ≥ 3: 1",
        "Heads in 3 tosses: x < 0: 0 | [0,1): 1/8 | [1,2): 4/8 | [2,3): 7/8 | x ≥ 3: 1",
        "Fair die:        F(x) = k/6 on [k, k + 1), k = 1, …, 5;  0 for x < 1;  1 for x ≥ 6",
        "Bernoulli(p):    0 for x < 0;  1 − p on [0, 1);  1 for x ≥ 1"])
n.h2("2. Probability Density Function (Lec 7 pp. 4–5)")
n.callout("answer", "A probability density function f(x) of a continuous random variable X is a non-negative function "
          "whose total area under the curve (over the whole range of x) equals one; probabilities are areas under the "
          "curve. Conditions: (1) f(x) ≥ 0 for all x; (2) ∫_{−∞}^{∞} f(x) dx = 1; then (3) P(a < X < b) = ∫_{a}^{b} f(x) dx. "
          "For a continuous X, P(X = a) = 0, so < and ≤ give the same probability. (2018-19 Q7(a))")
n.p("Example (Lec 7 pp. 4–5): f(x) = kx, 0 < x < 4: k[x²/2]_{0}^{4} = 8k = 1 → k = 1/8; P(1 < X < 2) = [x²/16]_{1}^{2} = 3/16; "
    "P(X > 2) = [x²/16]_{2}^{4} = 3/4. Example: f(x) = (2/27)(1 + x), 2 < x < 5: ∫ = (2/27)[x + x²/2]_{2}^{5} = 1; "
    "P(X < 4) = (2/27)(12 − 4) = 16/27; P(3 < X < 4) = (2/27)(12 − 7.5) = 1/3.")
e1 = sp.Rational(3, 16) * (4 - x ** 2)
e2 = sp.Rational(1, 12) * (x ** 2 + 1)
e3 = sp.Rational(1, 2) * x ** 2 * sp.exp(-x)
n.h3("Exercises of Lecture 7 (p. 6) — answers")
n.table(["pdf", "k", "Probabilities"],
        [["k(4 − x²), 0 ≤ x ≤ 2", "∫ = 16/3 → k = 3/16",
          f"P(X = 1) = 0; P(0.5 ≤ X ≤ 1.5) = {S(sp.integrate(e1,(x,0.5,1.5)))}; P(X ≥ 1) = {S(sp.integrate(e1,(x,1,2)))}"],
         ["k(x² + 1), 0 ≤ x ≤ 3", "∫ = 12 → k = 1/12",
          f"P(X ≥ 2) = {S(sp.integrate(e2,(x,2,3)))}; P(1 ≤ X ≤ 1.5) = {S(sp.integrate(e2,(x,1,1.5)))}; P(X ≤ 2) = {S(sp.integrate(e2,(x,0,2)))}"],
         ["kx²e^{−x}, x ≥ 0", "∫ = 2! → k = 1/2",
          f"P(X ≤ 1) = 1 − 2.5e^{{−1}} = {S(sp.integrate(e3,(x,0,1)))}; P(1 ≤ X ≤ 3) = {S(sp.integrate(e3,(x,1,3)))}; P(X ≥ 2) = 5e^{{−2}} = {S(sp.integrate(e3,(x,2,sp.oo)))}"]],
        widths_cm=[4, 3.6, 9.6], font_size=8.5)
n.h2("3. Continuous CDF (Lec 7 pp. 6–8)")
n.formula(["F(x) = P(X ≤ x) = ∫_{−∞}^{x} f(t) dt,   f(x) = F'(x)", "P(a < X < b) = F(b) − F(a)"])
n.p("For f(x) = (2/27)(1 + x) on (2, 5): F(x) = (2/27)∫_{2}^{x}(1 + t)dt = (x² + 2x − 8)/27 on 2 < x < 5 (0 below, 1 above). "
    "F(3) = 7/27, F(4) = 16/27, F(4) − F(3) = 9/27 = 1/3 = P(3 < X < 4) ✓.")
n.p("Triangular density f(x) = x on (0, 1], 2 − x on (1, 2]: F(x) = x²/2 for 0 < x ≤ 1, and "
    "F(x) = ∫_{0}^{1}t dt + ∫_{1}^{x}(2 − t)dt = 2x − x²/2 − 1 for 1 < x ≤ 2; F = 0 for x ≤ 0 and 1 for x > 2.")
n.callout("trap", "For a piecewise density, the CDF on a later piece must include the whole area of the earlier "
          "pieces (the \"∫_{0}^{1} t dt = 1/2\" term). Going the other way, the pdf from a piecewise F is F'(x) on each piece.")
n.h2("4. The Exponential Distribution (textbook — asked 2019-20, 2022-23, 2023-24)")
n.formula(["f(x) = λe^{−λx}, x ≥ 0  (λ = rate; mean β = 1/λ)",
           "F(x) = 1 − e^{−λx},   P(X > x) = e^{−λx}", "E(X) = 1/λ,  V(X) = 1/λ²"])
n.bullets(["Memoryless: P(X > s + t | X > s) = e^{−λ(s+t)}/e^{−λs} = e^{−λt} = P(X > t). The time already waited does not matter.",
           "If calls arrive as a Poisson process with rate λ per unit time, the waiting time between calls is "
           "exponential with the same λ, and \"no call in t\" = P(Poisson count 0) = e^{−λt}.",
           "Keep the units consistent: change the rate to per hour (or per minute) before substituting t."])
n.exam_approach(["Find k from ∫ f = 1 over the stated range.",
                 "Probability = integral over the requested interval (limits clipped to the range of X).",
                 "CDF: integrate from the lower end of the range to x, piece by piece; state F for every range of x.",
                 "Exponential: write λ in the right units, then use P(X ≤ t) = 1 − e^{−λt}.",
                 "Conditional: P(A | B) = P(A ∩ B)/P(B) with both found from F."])
k6b = sp.Rational(1, 1) / sp.integrate((3 - x) ** 2, (x, -1, 1))
lam = 1.8 / 24
n.practice("Lesson 8", "(a) Actual — 2018-19 Q7(a) (TF p. 24). (b) Actual — 2020-21 Q6(b) (TF p. 38). "
           "(c) Actual — 2022-23 Q1(c) (TF p. 47). (d) Actual — 2023-24 Q2(a) (22 batch p. 1). "
           "(e) Actual — 2019-20 Q8(b) (TF p. 35).",
           ["(a) What is a density function and what conditions must it satisfy? F(x) = 0 (x ≤ 0), x/8 (0 < x < 2), "
            "x²/16 (2 ≤ x < 4), 1 (x ≥ 4). (i) Find the pdf of X. (ii) Find P(X ≥ 1.5) and P(X ≥ 1 | X ≤ 3).  (20)",
            "(b) The measurement error X has density f(x) = k(3 − x)², −1 ≤ x ≤ 1. (i) Find k. (ii) P(X < 1/2). (iii) The "
            "error is undesirable if its magnitude exceeds 0.8: find that probability.  (10)",
            "(c) Time to failure (hours) has f(x) = (1/2000)e^{−x/2000}, x ≥ 0. (i) Find the CDF. (ii) P(lasts more than "
            "1000 hours). (iii) P(fails before 2000 hours).  (12)",
            "(d) The waiting time X (hours) between speeders has F(x) = 1 − e^{−8x}, x ≥ 0. Find the probability of waiting "
            "less than 12 minutes, using the CDF and using the pdf.  (15)",
            "(e) Calls to a fire station: exponential inter-call times, rate 1.8 per day. (i) P(a call in the next 15 minutes). "
            "(ii) No call so far in the shift, 15 minutes left: P(a call in the next 15 minutes). (iii) P(no calls in a "
            "10-hour shift). (iv) P(no calls in four successive shifts). (v) In 10 % of shifts there is a call in the "
            "first x hours: find x to one decimal place.  (25)"])
n.solution()
n.answer("(a)", "Definition and conditions as in the EXAM-READY ANSWER of §2.")
n.code(["(i)  f(x) = F'(x):  1/8 for 0 < x < 2;  x/8 for 2 ≤ x < 4;  0 elsewhere",
        "     check: ∫0^2 1/8 dx + ∫2^4 x/8 dx = 1/4 + (16 − 4)/16 = 1/4 + 3/4 = 1 ✓",
        "(ii) P(X ≥ 1.5) = 1 − F(1.5) = 1 − 1.5/8 = 13/16 = 0.8125",
        "     P(X ≥ 1 | X ≤ 3) = P(1 ≤ X ≤ 3)/P(X ≤ 3) = [F(3) − F(1)]/F(3)",
        "                      = (9/16 − 1/8)/(9/16) = (7/16)/(9/16) = 7/9 = 0.7778"])
n.callout("note", "F jumps from 2/8 = 1/4 to 2²/16 = 1/4 at x = 2, so it is continuous there — the pdf is valid.")
n.answer("(b)", "")
n.code([f"(i)   ∫_-1^1 (3 − x)² dx = [−(3 − x)³/3]_-1^1 = (64 − 8)/3 = 56/3  →  k = {k6b}",
        f"(ii)  P(X < 1/2) = (3/56)[−(3 − x)³/3]_-1^1/2 = (1/56)[64 − 15.625] = {sp.integrate(k6b*(3-x)**2,(x,-1,sp.Rational(1,2)))} = {S(sp.integrate(k6b*(3-x)**2,(x,-1,sp.Rational(1,2))))}",
        f"(iii) P(|X| > 0.8) = 1 − P(−0.8 ≤ X ≤ 0.8) = 1 − (1/56)[3.8³ − 2.2³]",
        f"                   = 1 − (1/56)(54.872 − 10.648) = 1 − 44.224/56 = {S(1-sp.integrate(k6b*(3-x)**2,(x,-0.8,0.8)))}"])
n.answer("(c)", "Exponential with mean 2000 h (λ = 1/2000).")
n.code(["(i)   F(x) = ∫0^x (1/2000)e^(−t/2000) dt = 1 − e^(−x/2000) for x ≥ 0;  F(x) = 0 for x < 0",
        f"(ii)  P(X > 1000) = 1 − F(1000) = e^(−0.5) = {g(exp(-0.5))}",
        f"(iii) P(X < 2000) = F(2000) = 1 − e^(−1) = {g(1-exp(-1))}"])
n.answer("(d)", "12 minutes = 0.2 hour.")
n.code([f"CDF:  P(X < 0.2) = F(0.2) = 1 − e^(−8×0.2) = 1 − e^(−1.6) = {g(1-exp(-1.6))}",
        "pdf:  f(x) = F'(x) = 8e^(−8x), x ≥ 0",
        f"      P(X < 0.2) = ∫0^0.2 8e^(−8x) dx = [−e^(−8x)]0^0.2 = 1 − e^(−1.6) = {g(1-exp(-1.6))}"])
n.answer("(e)", "Rate λ = 1.8 per day = 1.8/24 = 0.075 per hour.")
n.code([f"(i)   15 min = 1/96 day:  P(X ≤ 1/96) = 1 − e^(−1.8/96) = 1 − e^(−0.01875) = {g(1-exp(-1.8/96))}",
        f"(ii)  Memoryless: P(X ≤ s + t | X > s) = 1 − e^(−λt) — the same {g(1-exp(-1.8/96))}",
        f"(iii) 10 h:  P(no call) = P(X > 10) = e^(−0.075×10) = e^(−0.75) = {g(exp(-0.75))}",
        f"(iv)  four independent shifts: (e^(−0.75))⁴ = e^(−3) = {g(exp(-3))}",
        f"(v)   P(X ≤ x) = 0.10  →  1 − e^(−0.075x) = 0.10  →  x = −ln 0.9 / 0.075 = {g(-math.log(0.9)/lam)} h ≈ 1.4 h"])

# ------------------------------------------------------------------ L9
n.lesson("Lesson 9 — Expectation, Variance and Chebyshev's Theorem", "Lec 9 pp. 1–5 · other distributions p. 1–2")
n.h2("1. Definitions and Rules (Lec 9 p. 1)")
n.formula(["E(X) = Σ x f(x)   or   ∫ x f(x) dx", "E[W(X)] = Σ W(x) f(x)   or   ∫ W(x) f(x) dx",
           "V(X) = E[(X − μ)²] = E(X²) − μ²,   σ = √V(X)"])
n.bullets(["E(c) = c; E(cW(X)) = cE(W(X)); E[W_{1}(X) + W_{2}(X)] = E[W_{1}(X)] + E[W_{2}(X)].",
           "Hence E(aX + b) = aE(X) + b and V(aX + b) = a²V(X) (textbook — the constant shift does not change the spread)."])
n.h2("2. Worked Examples (Lec 9 pp. 1–5)")
n.code(["x    :  −3     −2     0      1      2",
        "f(x) :  0.10   0.30   0.15   0.40   0.05",
        "E(X)  = −0.3 − 0.6 + 0 + 0.4 + 0.1 = −0.4",
        "E(X²) = 0.9 + 1.2 + 0 + 0.4 + 0.2 = 2.7",
        "V(X)  = 2.7 − (−0.4)² = 2.54,   σ = √2.54 = 1.59"])
n.bullets(["Insurance: gain 2500 w.p. 0.97, 2500 − 25000 = −22500 w.p. 0.03 → E = 2425 − 675 = Tk 1750.",
           "f(x) = 2(1 − x), 0 < x < 1: E(X) = 2∫(x − x²)dx = 1/3; E(X²) = 2∫(x² − x³)dx = 1/6; V = 1/6 − 1/9 = 1/18.",
           "Poisson f(x) = e^{−m}m^{x}/x!: E(X) = e^{−m} m Σ m^{x−1}/(x − 1)! = e^{−m} m e^{m} = m.",
           "Markers: 4 good, 3 defective, sample 3: f(x) = 4Cx·3C(3−x)/35 = 1/35, 12/35, 18/35, 4/35 → E(X) = 60/35 = 12/7 ≈ 1.71.",
           "Coin game: +5 for HHH or TTT (2/8), −3 otherwise (6/8): E = 5(2/8) − 3(6/8) = −1 → loses Tk 1. With 0 for two "
           "heads: E = 5(2/8) + 0(3/8) − 3(3/8) = 1/8 = Tk 0.125."])
n.callout("note", "The slide prints the coin-game sum as \"5(2/3)\"; it is 5 × 2/8, and the answer −1 is right.")
n.h2("3. Chebyshev's Theorem (other distributions p. 1)")
n.formula(["P(μ − kσ < X < μ + kσ) ≥ 1 − 1/k²", "equivalently  P(|X − μ| ≥ kσ) ≤ 1/k²"])
n.p("It holds for every distribution (distribution-free), so the bound is weak: k = 2 → at least 3/4 within 2σ; "
    "k = 3 → at least 8/9. Example 4.27: μ = 8, σ² = 9: P(−4 < X < 20) = P(8 − 4·3 < X < 8 + 4·3) ≥ 15/16; "
    "P(|X − 8| ≥ 6) = P(|X − 8| ≥ 2·3) ≤ 1/4.")
n.h3("Proof (textbook, review exercise 4.79)")
n.code(["σ² = ∫ (x − μ)² f(x) dx  ≥  ∫_{|x−μ| ≥ kσ} (x − μ)² f(x) dx      (drop the middle part, integrand ≥ 0)",
        "                     ≥  ∫_{|x−μ| ≥ kσ} k²σ² f(x) dx = k²σ² P(|X − μ| ≥ kσ)",
        "⟹  P(|X − μ| ≥ kσ) ≤ 1/k²   ⟹  P(|X − μ| < kσ) ≥ 1 − 1/k²   ∎"])
n.exam_approach(["Write E(X) and E(X²) as sums/integrals over the range; integrate carefully (use ∫_{0}^{∞}x^{n}e^{−x}dx = n!).",
                 "V(X) = E(X²) − [E(X)]²; for Y = aX + b use E(Y) = aE(X) + b, V(Y) = a²V(X).",
                 "E[g(X)] = ∫ g(x) f(x) dx — do not compute g(E(X)).",
                 "Chebyshev: write the interval as μ ± kσ, find k, then the bound 1 − 1/k² (or 1/k² for the tails)."])
mu2c, sd2c = 0.5, math.sqrt(1 / 20)
p2c = float(sp.integrate(6 * x * (1 - x), (x, 0.5 - 2 * sd2c, 0.5 + 2 * sd2c)))
n.practice("Lesson 9", "(a) Actual — 2018-19 Q7(b) (TF p. 25). (b) Actual — 2019-20 Q7(b) (TF p. 35). "
           "(c) Actual — 2020-21 Q8(a) (TF p. 38). (d) Actual — 2022-23 Q2(b) (TF p. 48). (e) Actual — 2022-23 Q2(c) "
           "(TF p. 48). (f) Actual — 2023-24 Q3(a) (22 batch p. 2).",
           ["(a) A lot of 7 components (4 good, 3 defective) is sampled; 3 are taken. Find the expected number of good "
            "components in the sample.  (15)",
            "(b) X has density f(x) = e^{−x}, x > 0. Find the expected value of g(X) = e^{2X/3}.  (18)",
            "(c) Hospital stay Y = X + 4 days, where f(x) = 32/(x + 4)³, x > 0. Find the average stay.  (10)",
            "(d) Clearance time Y = 3X − 2 minutes, where f(x) = (1/4)e^{−x/4}, x > 0. Find the mean and variance of Y.  (10)",
            "(e) Compute P(μ − 2σ < X < μ + 2σ) for f(x) = 6x(1 − x), 0 < x < 1, and compare with Chebyshev's theorem.  (10)",
            "(f) State Chebyshev's theorem. 1000 applicants sit a test for 70 jobs; mean 60, SD 6, distribution "
            "symmetric about the mean. Can a person who scores 84 count on getting a job?  (11)"])
n.solution()
n.answer("(a)", "X = number of good components; hypergeometric f(x) = 4Cx · 3C(3−x) / 7C3, 7C3 = 35.")
n.code(["x     :   0      1       2       3",
        "f(x)  :  1/35  12/35   18/35   4/35",
        "E(X) = 0(1/35) + 1(12/35) + 2(18/35) + 3(4/35) = (12 + 36 + 12)/35 = 60/35 = 12/7 ≈ 1.714"])
n.p("Check with the hypergeometric mean nM/N = 3 × 4/7 = 12/7 ✓.")
n.answer("(b)", "")
n.formula("E(e^{2X/3}) = ∫_{0}^{∞} e^{2x/3} e^{−x} dx = ∫_{0}^{∞} e^{−x/3} dx = [−3e^{−x/3}]_{0}^{∞} = 3")
n.answer("(c)", "First check ∫_{0}^{∞} 32(x + 4)^{−3} dx = [−16(x + 4)^{−2}]_{0}^{∞} = 16/16 = 1 ✓.")
n.code(["E(X) = ∫0^∞ x · 32/(x + 4)³ dx,  put u = x + 4:",
        "     = 32 ∫4^∞ (u − 4)/u³ du = 32 [ −1/u + 2/u² ]4^∞ = 32 (1/4 − 2/16) = 32 × 1/8 = 4",
        "E(Y) = E(X) + 4 = 8 days"])
n.answer("(d)", "X is exponential with mean 4: E(X) = ∫x(1/4)e^{−x/4}dx = 4, E(X²) = 2 × 4² = 32, V(X) = 32 − 16 = 16.")
n.code(["E(Y) = 3E(X) − 2 = 12 − 2 = 10 minutes",
        "V(Y) = 3² V(X) = 9 × 16 = 144  (σ_Y = 12 minutes)"])
n.answer("(e)", "")
n.code(["μ  = ∫0^1 x·6x(1 − x) dx = 6(1/3 − 1/4) = 1/2",
        "E(X²) = ∫0^1 x²·6x(1 − x) dx = 6(1/4 − 1/5) = 3/10,   σ² = 3/10 − 1/4 = 1/20,  σ = 0.2236",
        f"μ ± 2σ = 0.5 ± 0.4472 → (0.0528, 0.9472)  (inside (0, 1))",
        f"P = ∫ 6x(1 − x) dx = [3x² − 2x³] over (0.0528, 0.9472) = 11√5/25 = {g(p2c)}",
        "Chebyshev (k = 2): P ≥ 1 − 1/4 = 0.75"])
n.p(f"The exact probability {g(p2c, 3)} is far above the Chebyshev lower bound 0.75 — the theorem is true but "
    "conservative because it uses no information about the shape of the distribution.")
n.answer("(f)", "Chebyshev: for any k > 0, P(μ − kσ < X < μ + kσ) ≥ 1 − 1/k². Here 84 = 60 + 4 × 6, so k = 4.")
n.code(["P(36 < X < 84) ≥ 1 − 1/16 = 15/16  →  P(|X − 60| ≥ 24) ≤ 1/16",
        "Symmetric about the mean → P(X ≥ 84) ≤ (1/2)(1/16) = 1/32",
        "Number of applicants scoring 84 or more ≤ 1000/32 = 31.25, i.e. at most 31 people"])
n.p("Since at most about 31 of the 1000 applicants can score 84 or above and there are 70 jobs, a person scoring 84 "
    "is within the top 70 and can count on getting a job.")

n.quick_notes("Quick Notes — Random Variables", "Revision points for Lessons 7–9.", [
    ("L7 · pmf", ["Random variable = numerical outcome of chance; discrete (countable) or continuous (interval).",
                  "pmf: f(x) ≥ 0 and Σ f(x) = 1; solve Σ = 1 for k (k-table: k = 1/10; α(3/4)^{x}: α = 1/4)."]),
    ("L8 · pdf, CDF, Exponential", ["pdf: f ≥ 0, ∫ f = 1, P(a < X < b) = ∫_{a}^{b} f; P(X = a) = 0.",
                                    "CDF F(x) = ∫_{−∞}^{x} f; f = F'; P(a < X < b) = F(b) − F(a); carry earlier pieces' area.",
                                    "Exponential: F = 1 − e^{−λx}, mean 1/λ, memoryless; convert λ to the units of t.",
                                    "Fire station: 0.0186, 0.0186, e^{−0.75} = 0.4724, e^{−3} = 0.0498, x = 1.4 h."]),
    ("L9 · Expectation, Chebyshev", ["E(X) = Σxf or ∫xf; V = E(X²) − μ²; E(aX + b) = aE + b; V(aX + b) = a²V.",
                                     "E(e^{2X/3}) for e^{−x}: 3. Hospital stay: E(X) = 4, E(Y) = 8. Y = 3X − 2: 10 and 144.",
                                     "Chebyshev: P(|X − μ| < kσ) ≥ 1 − 1/k²; 6x(1 − x): exact 0.9839 vs 0.75.",
                                     "Jobs: 84 = μ + 4σ → at most 1/32 of 1000 ≈ 31 above → yes, gets a job."])])
n.save()
print("saved", n.out_path)
