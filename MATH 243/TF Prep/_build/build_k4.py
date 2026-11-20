"""MATH243_KKS_Joint_Distributions_Notes.docx — Lecture 8, Lecture 9 pp. 5–9, Lec 3 & 4 Problem 5 (L10–L12)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from math import comb

import sympy as sp

from common import exam_map, new
from m243 import fr, g

x, y = sp.symbols("x y", real=True)
R = sp.Rational

n = new("KKS", "Joint Distributions: Joint, Marginal and Conditional Distributions, Independence, Covariance",
        "MATH243_KKS_Joint_Distributions_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "joint pmf/pdf questions and how they are asked"),
              ("Lesson 10 — Joint pmf and pdf, Marginal Distributions", "tables, double integrals, finding k"),
              ("Lesson 11 — Conditional Distributions and Independence", "f(y | x), P(a < Y < b | X = x), independence tests"),
              ("Lesson 12 — Expectation of Two Variables and Covariance", "E(X + Y), E(XY), Cov, Var(X + Y)"),
              ("Quick Notes — Joint Distributions", "revision bullets")],
    source_note="Page numbers refer to KKS Sir's Lecture 8.pdf (11 pp.), Lecture 9.pdf (pp. 5–9) and Lecture 3 & 4.pdf "
                "(Problem 5, pp. 11–12). Covariance is not on the slides but is asked in 2023-24 Q2(b); it is taught here "
                "from the textbook and marked. \"TF p.\" = merged question PDF page; \"22 batch p.\" = 2023-24 paper.")

n.h1("Exam Map — What the TF Papers Ask")
st = exam_map(n, "k4")
n.callout("focus", f"{st['n']} questions, {st['marks']} marks ({st['marks_hi']} marks since 2019-20). Every MATH 243 "
          "paper has one 15–20-mark joint-distribution question in Section A: a discrete pens/balls table (2023-24, "
          "the same as Lecture 3 & 4 Problem 5) or a continuous density with marginals and a conditional probability "
          "(2022-23, 2020-21, 2012-13). Learn the table layout, the limits of integration for triangular regions "
          "(0 < x < y < 1), and Cov = E(XY) − E(X)E(Y).")

# ------------------------------------------------------------------ L10
n.lesson("Lesson 10 — Joint pmf and pdf, Marginal Distributions", "Lec 8 pp. 1–6 · Lec 3 & 4 pp. 11–12")
n.h2("1. Discrete Joint Distribution (Lec 8 p. 1)")
n.formula(["f(x, y) = P(X = x, Y = y)", "f(x, y) ≥ 0,   Σ_{x} Σ_{y} f(x, y) = 1,   P[(X, Y) ∈ A] = Σ Σ_{(x,y)∈A} f(x, y)"])
n.h3("Example — three tosses: X = heads, Y = tails in the last two tosses (Lec 8 pp. 1–2)")
n.code(["Outcome  HHH HHT HTH HTT THH THT TTH TTT",
        "X         3   2   2   1   2   1   1   0",
        "Y         0   1   1   2   0   1   1   2",
        "",
        "            X = 0   X = 1   X = 2   X = 3   h(y)",
        "Y = 0         0       0      1/8     1/8    2/8",
        "Y = 1         0      2/8     2/8      0     4/8",
        "Y = 2        1/8     1/8      0       0     2/8",
        "g(x)         1/8     3/8     3/8     1/8     1"])
n.h2("2. Continuous Joint Density (Lec 8 pp. 2–3)")
n.formula(["f(x, y) ≥ 0,   ∫∫ f(x, y) dx dy = 1,   P[(X, Y) ∈ A] = ∫∫_{A} f(x, y) dx dy",
           "F(x, y) = P(X ≤ x, Y ≤ y);  ∂²F/∂x∂y = f(x, y)"])
v1 = sp.integrate(sp.integrate(x ** 2 + x * y / 3, (x, 0, 1)), (y, 0, 2))
v2 = sp.integrate(sp.integrate(x * (1 + 3 * y ** 2) / 4, (x, 0, 1)), (y, R(1, 4), R(1, 2)))
n.p(f"f(x, y) = x² + xy/3 on 0 ≤ x ≤ 1, 0 ≤ y ≤ 2: ∫_{{0}}^{{2}}(1/3 + y/6)dy = [y/3 + y²/12]_{{0}}^{{2}} = {v1} → a density. "
    f"f(x, y) = x(1 + 3y²)/4 on 0 ≤ x ≤ 2, 0 ≤ y ≤ 1: P(0 < X < 1, 1/4 < Y < 1/2) = ∫(1/8 + 3y²/8)dy over (1/4, 1/2) = {v2}.")
n.h2("3. Marginal Distributions (Lec 8 pp. 4–6)")
n.formula(["Discrete: g(x) = Σ_{y} f(x, y),   h(y) = Σ_{x} f(x, y)",
           "Continuous: g(x) = ∫ f(x, y) dy,   h(y) = ∫ f(x, y) dx"])
f8 = (6 - x - y) / 8
gx8 = sp.integrate(f8, (y, 2, 4)); hy8 = sp.integrate(f8, (x, 0, 2))
p1 = sp.integrate(sp.integrate(f8, (y, 2, 3 - x)), (x, 0, 1))
p2 = sp.integrate(sp.integrate(f8, (y, 2, R(5, 2))), (x, 0, R(3, 2)))
n.p(f"f(x, y) = (6 − x − y)/8, 0 < x < 2, 2 < y < 4: g(x) = {sp.factor(gx8)} = (3 − x)/4, h(y) = (5 − y)/4; both integrate "
    f"to 1. P(X + Y < 3) = (1/8)∫_{{0}}^{{1}}∫_{{2}}^{{3−x}}(6 − x − y)dy dx = {p1}; P(X < 3/2, Y < 5/2) = {p2}.")
n.callout("trap", "For P(X + Y < 3) the region is x from 0 to 1 only (y must exceed 2, so x < 1). The slide writes "
          "the outer limit as 0 to 2 but its integrand and the answer 1/24 use 0 to 1. Always sketch the region first.")
n.h2("4. Discrete Example — Pens (Lec 3 & 4 pp. 11–12)")
n.p("Two pens from 3 blue, 2 red, 3 green; X = blue, Y = red. f(x, y) = 3Cx · 2Cy · 3C(2−x−y) / 8C2, 8C2 = 28.")
n.code(["            Y = 0    Y = 1    Y = 2    g(x)",
        "X = 0        3/28     6/28     1/28    10/28",
        "X = 1        9/28     6/28      –      15/28",
        "X = 2        3/28      –        –       3/28",
        "h(y)        15/28    12/28     1/28      1",
        "P(X + Y ≤ 1) = f(0,0) + f(1,0) + f(0,1) = (3 + 9 + 6)/28 = 9/14"])
n.callout("note", "The slide's marginal row prints P(X = 0) = P(X = 1) = P(X = 2) = 10/28 = 5/14; the correct "
          "marginal of X is 10/28, 15/28, 3/28 (read the row totals). The marginal of Y (15/28, 12/28, 1/28) is right.")
n.exam_approach(["Discrete: list every (x, y) with x + y ≤ sample size; f = product of C's ÷ total; draw the table with margins.",
                 "Continuous: sketch the region; find k from the double integral = 1.",
                 "Marginal: integrate out the other variable over its full range (which may depend on x).",
                 "Probability over a region: set the inner limits from the region boundary."])
J = {(a, b): F(comb(3, a) * comb(2, b) * comb(3, 2 - a - b), 28) for a in range(3) for b in range(3) if a + b <= 2}
gX = {a: sum(v for (aa, b), v in J.items() if aa == a) for a in range(3)}
hY = {b: sum(v for (a, bb), v in J.items() if bb == b) for b in range(3)}
EX = sum(a * v for a, v in gX.items()); EX2 = sum(a * a * v for a, v in gX.items())
EY = sum(b * v for b, v in hY.items()); EXY = sum(a * b * v for (a, b), v in J.items())
kk = 1 / sp.integrate(sp.integrate(x ** 2 + y ** 2, (x, 30, 50)), (y, 30, 50))
pa = sp.integrate(sp.integrate(kk * (x ** 2 + y ** 2), (x, 30, 40)), (y, 40, 50))
pb = sp.integrate(sp.integrate(kk * (x ** 2 + y ** 2), (x, 30, 40)), (y, 30, 40))
n.practice("Lesson 10", "(a) Actual — 2023-24 Q2(b) (22 batch p. 1). (b) Actual — 2020-21 Q5(c) (TF p. 37).",
           ["(a) From a bag of 3 red, 2 blue and 3 black pens a random sample of two pens is selected. X = number of red "
            "pens, Y = number of blue pens. (i) Plot f(x, y) versus (x, y). (ii) P[(X, Y) ∈ A], A = {(x, y): x + y ≤ 1}. "
            "(iii) Marginal distributions of X and Y. (iv) Variance of X. (v) Covariance between X and Y.  (20)",
            "(b) Tyre pressures X (right) and Y (left) have joint density f(x, y) = k(x² + y²), 30 ≤ x < 50, 30 ≤ y < 50 "
            "(target 40 psi). (i) Find k. (ii) Find P(30 ≤ X ≤ 40 and 40 ≤ Y < 50). (iii) Find the probability that both "
            "tyres are underfilled.  (10)"])
n.solution()
n.answer("(a)", "f(x, y) = 3Cx · 2Cy · 3C(2 − x − y) / 8C2 for x, y = 0, 1, 2 with x + y ≤ 2; 8C2 = 28.")
n.code(["(i) Joint pmf (plot: a vertical stick of height f at each point (x, y))",
        "            Y = 0    Y = 1    Y = 2    g(x)",
        f"X = 0        {fr(J[(0,0)])}     {fr(J[(0,1)])}     {fr(J[(0,2)])}    {fr(gX[0])}",
        f"X = 1        {fr(J[(1,0)])}     {fr(J[(1,1)])}      –      {fr(gX[1])}",
        f"X = 2        {fr(J[(2,0)])}      –        –       {fr(gX[2])}",
        f"h(y)        {fr(hY[0])}    {fr(hY[1])}     {fr(hY[2])}      1",
        "",
        "  f  ^   9/28 |       ·(1,0)",
        "     |   6/28 |  ·(0,1)  ·(1,1)",
        "     |   3/28 |  ·(0,0)          ·(2,0)",
        "     |   1/28 |         ·(0,2)",
        "     +------------------------------------> points (x, y)"])
n.code([f"(ii)  P(X + Y ≤ 1) = f(0,0) + f(0,1) + f(1,0) = 3/28 + 6/28 + 9/28 = 18/28 = {fr(sum(v for (a,b),v in J.items() if a+b<=1))}",
        f"(iii) g(0) = {fr(gX[0])}, g(1) = {fr(gX[1])}, g(2) = {fr(gX[2])};   h(0) = {fr(hY[0])}, h(1) = {fr(hY[1])}, h(2) = {fr(hY[2])}",
        f"(iv)  E(X) = 0 + 15/28 + 2(3/28) = 21/28 = {fr(EX)};  E(X²) = 15/28 + 4(3/28) = {fr(EX2)}",
        f"      Var(X) = {fr(EX2)} − ({fr(EX)})² = {fr(EX2)} − 9/16 = {fr(EX2 - EX**2)} = {g(float(EX2 - EX**2))}",
        f"(v)   E(Y) = 12/28 + 2(1/28) = {fr(EY)};  E(XY) = 1·1·f(1,1) = {fr(EXY)}",
        f"      Cov(X, Y) = E(XY) − E(X)E(Y) = {fr(EXY)} − ({fr(EX)})({fr(EY)}) = {fr(EXY - EX*EY)} = {g(float(EXY - EX*EY))}"])
n.p("The covariance is negative: with only two pens drawn, more red pens leave less room for blue ones.")
n.answer("(b)", "")
n.code(["(i)   ∫30^50 ∫30^50 (x² + y²) dx dy = 2 × 20 × ∫30^50 x² dx = 40 × (50³ − 30³)/3 = 40 × 98000/3 = 3,920,000/3",
        f"      k = 3/3,920,000 = {kk}  (≈ 7.65 × 10^−7)",
        "(ii)  ∫40^50 ∫30^40 (x² + y²) dx dy = 10 ∫30^40 x² dx + 10 ∫40^50 y² dy = 10(37000/3) + 10(61000/3) = 980000/3",
        f"      P = k × 980000/3 = 980000/3920000 = {pa} = {g(float(pa))}",
        "(iii) underfilled = below 40 psi:  ∫30^40 ∫30^40 (x² + y²) dx dy = 2 × 10 × 37000/3 = 740000/3",
        f"      P(X < 40, Y < 40) = 740000/3920000 = {pb} = {g(float(pb))}"])

# ------------------------------------------------------------------ L11
n.lesson("Lesson 11 — Conditional Distributions and Independence", "Lec 8 pp. 7–11")
n.h2("1. Conditional Distributions (Lec 8 p. 7)")
n.formula(["f(y | x) = f(x, y) / g(x),  g(x) > 0", "f(x | y) = f(x, y) / h(y),  h(y) > 0",
           "P(a < X < b | Y = y) = Σ f(x | y)  or  ∫_{a}^{b} f(x | y) dx"])
n.p("Discrete example (Lec 8 p. 8, pens table): h(1) = 6/28 + 6/28 + 0 = 3/7, so f(x | 1) = (7/3)f(x, 1): "
    "f(0 | 1) = 1/2, f(1 | 1) = 1/2, f(2 | 1) = 0.")
n.callout("note", "In the Lec 8 p. 8 table the entry f(1, 0) is printed as 3/28; the pens table (Lesson 10 §4) has 9/28. "
          "The conditional f(x | 1) does not use that cell, so the slide's answer is unaffected.")
hy = sp.integrate(R(6, 5) * (x + y ** 2), (x, 0, 1))
fxy = sp.simplify(R(6, 5) * (x + y ** 2) / hy)
n.p(f"Continuous example (Lec 8 pp. 8–9): f(x, y) = (6/5)(x + y²) on the unit square. h(y) = (6/5)(1/2 + y²); "
    f"f(x | y) = 2(x + y²)/(1 + 2y²); f(x | 0.5) = (4x + 1)/3; P(X < 0.5 | Y = 0.5) = (1/3)[2x² + x]_{{0}}^{{0.5}} = "
    f"{sp.integrate(fxy.subs(y, R(1,2)), (x, 0, R(1,2)))}.")
n.h2("2. Independence (Lec 8 pp. 9–11)")
n.formula("X, Y independent  ⟺  f(x, y) = g(x) h(y) for all (x, y)  ⟺  f(x | y) = g(x)")
n.bullets(["Table example (Lec 8 p. 10): every cell equals the product of its margins (e.g. f(2, 1) = 0.10 = 0.40 × 0.25) → independent.",
           "f(x, y) = (x + y)/8 on (0, 2)²: g(x) = (x + 1)/4, h(y) = (y + 1)/4, g h = (x + 1)(y + 1)/16 ≠ f → not independent. "
           "(The slide writes g(x) = (x + y)/4 by a slip; integrating out y gives (x + 1)/4.)"])
n.callout("trap", "For a region like 0 < x < y < 1 the variables can never be independent: the range of Y depends on x. "
          "Write the conditional range too (f(y | x) lives on x < y < 1).")
n.exam_approach(["Find the marginal of the conditioning variable (g(x) for f(y | x)).",
                 "Divide: f(y | x) = f(x, y)/g(x); state the range of y for that x.",
                 "Substitute the given x, then integrate (or sum) over the requested y-interval, clipped to the range.",
                 "Independence: compare f(x, y) with g(x)h(y) at every point (one failure is enough for \"not independent\")."])
f2a = 10 * x * y ** 2
g2a = sp.integrate(f2a, (y, x, 1)); h2a = sp.integrate(f2a, (x, 0, y)); c2a = sp.simplify(f2a / g2a)
p2a = sp.integrate(c2a.subs(x, R(1, 4)), (y, R(1, 2), 1))
n.practice("Lesson 11", "(a) Actual — 2022-23 Q2(a) (TF p. 47). (b) Actual — 2012-13 Q8(a) (TF p. 5).",
           ["(a) The joint density of (X, Y), X = unit temperature change and Y = proportion of spectrum shift, is "
            "f(x, y) = 10xy², 0 < x < y < 1. (i) Find g(x), h(y) and f(y | x). (ii) Find the probability that the spectrum "
            "shifts more than half of the total observations, given that the temperature is increased by 0.25 unit.  (15)",
            "(b) For the joint density f(x, y) = (6 − x − y)/c, 0 < x < 2, 2 < y < 4 (printed with c = 3; the "
            "normalising constant is 8), find P(1 < Y < 3 | X = 2).  (18)"])
n.solution()
n.answer("(a)", "Region: 0 < x < y < 1 (triangle above the line y = x).")
n.code(["(i)  g(x) = ∫_x^1 10xy² dy = (10x/3)(1 − x³),   0 < x < 1",
        "     h(y) = ∫_0^y 10xy² dx = 5y² · y² = 5y⁴,       0 < y < 1",
        "     f(y | x) = f(x, y)/g(x) = 10xy² / [(10x/3)(1 − x³)] = 3y²/(1 − x³),   x < y < 1",
        "(ii) X = 0.25: f(y | 0.25) = 3y²/(1 − 1/64) = (64/21)y²,  0.25 < y < 1",
        f"     P(Y > 1/2 | X = 0.25) = ∫_1/2^1 (64/21)y² dy = (64/63)(1 − 1/8) = {p2a} = {g(float(p2a))}"])
n.answer("(b)", "The constant cancels in a conditional density, so the answer is the same for c = 3 or 8.")
n.code(["f(2, y) = (4 − y)/c;  g(2) = ∫_2^4 (4 − y)/c dy = 2/c",
        "f(y | x = 2) = (4 − y)/2,  2 < y < 4",
        "P(1 < Y < 3 | X = 2) = P(2 < Y < 3 | X = 2)      (Y cannot be below 2)",
        "                     = ∫_2^3 (4 − y)/2 dy = (1/2)[4y − y²/2]_2^3 = (1/2)(7.5 − 6) = 3/4"])
n.callout("note", "x = 2 lies on the boundary of 0 < x < 2; read it as the limit x → 2 (the formula is continuous). "
          "With c = 8, ∫∫ f = 1 checks; with c = 3 the function is not a density — say so in one line.")

# ------------------------------------------------------------------ L12
n.lesson("Lesson 12 — Expectation of Two Variables and Covariance", "Lec 9 pp. 5–9 · covariance: textbook")
n.h2("1. Expected Value of a Function of (X, Y) (Lec 9 pp. 5–6)")
n.formula(["E[w(X, Y)] = Σ Σ w(x, y) f(x, y)   or   ∫∫ w(x, y) f(x, y) dx dy",
           "E(X + Y) = E(X) + E(Y);   E(aX + bY) = aE(X) + bE(Y)",
           "X, Y independent ⟹ E(XY) = E(X)E(Y)"])
n.h2("2. Worked Example (Lec 9 pp. 7–9)")
ff = 2 * (x + y - 2 * x * y)
n.code(["f(x, y) = 2(x + y − 2xy), 0 < x, y < 1",
        "g(x) = 2∫0^1 (x + y − 2xy) dy = 2(x + 1/2 − x) = 1   → E(X) = ∫0^1 x dx = 1/2;  likewise h(y) = 1, E(Y) = 1/2",
        f"E(X + Y) = ∫∫ (x + y) f dx dy = {sp.integrate(sp.integrate((x+y)*ff,(x,0,1)),(y,0,1))} = E(X) + E(Y) ✓",
        f"E(XY) = ∫∫ xy f dx dy = {sp.integrate(sp.integrate(x*y*ff,(x,0,1)),(y,0,1))} ≠ E(X)E(Y) = 1/4  → not independent"])
n.p("Note the converse: g(x)h(y) = 1 ≠ f(x, y), so the marginals being uniform does not make X and Y independent. "
    f"Example f(x, y) = 4xy on the unit square: E(X) = 4∫∫x²y = {sp.integrate(sp.integrate(4*x**2*y,(x,0,1)),(y,0,1))}, "
    f"E(Y) = {sp.integrate(sp.integrate(4*x*y**2,(x,0,1)),(y,0,1))}.")
n.callout("note", "The 4xy example on the slide does not state the range of y; it is 0 < y < 1.")
n.h2("3. Covariance and Variance of a Sum (textbook — asked 2023-24 Q2(b))")
n.formula(["Cov(X, Y) = E[(X − μ_{X})(Y − μ_{Y})] = E(XY) − E(X)E(Y)",
           "Var(aX + bY) = a²Var(X) + b²Var(Y) + 2ab Cov(X, Y)"])
n.bullets(["Cov > 0: large X goes with large Y; Cov < 0: large X with small Y; independent ⟹ Cov = 0 (not conversely).",
           "Correlation coefficient ρ = Cov(X, Y)/(σ_{X}σ_{Y}), −1 ≤ ρ ≤ 1 (the sample version is Pearson's r in the "
           "Statistics notes)."])
fxy = x + y
EXc = sp.integrate(sp.integrate(x * fxy, (x, 0, 1)), (y, 0, 1)); EXYc = sp.integrate(sp.integrate(x * y * fxy, (x, 0, 1)), (y, 0, 1))
n.exam_approach(["Find the marginals, then E(X), E(Y) (and E(X²) for a variance).",
                 "E(XY) = Σ xy f(x, y) over cells with x, y ≠ 0 (or the double integral).",
                 "Cov = E(XY) − E(X)E(Y); interpret its sign."])
n.practice("Lesson 12", "(a) Adapted — textbook Review Exercise 4.80 (other distributions p. 2). (b) Constructed.",
           ["(a) Find the covariance of X and Y with joint density f(x, y) = x + y, 0 < x < 1, 0 < y < 1.",
            "(b) For the three-toss table of Lesson 10 (X = heads, Y = tails in the last two tosses), find Cov(X, Y)."])
n.solution()
n.code([f"(a) E(X) = ∫∫ x(x + y) = {EXc}, E(Y) = {EXc} (symmetry), E(XY) = ∫∫ xy(x + y) = {EXYc}",
        f"    Cov = {EXYc} − ({EXc})² = {EXYc - EXc**2} ≈ {g(float(EXYc - EXc**2))}"])
tx = {(3, 0): F(1, 8), (2, 1): F(2, 8), (1, 2): F(1, 8), (2, 0): F(1, 8), (1, 1): F(2, 8), (0, 2): F(1, 8)}
EXt = sum(a * p for (a, b), p in tx.items()); EYt = sum(b * p for (a, b), p in tx.items()); EXYt = sum(a * b * p for (a, b), p in tx.items())
n.code([f"(b) E(X) = {fr(EXt)}, E(Y) = {fr(EYt)}, E(XY) = 2·1·(2/8) + 1·2·(1/8) + 1·1·(2/8) = {fr(EXYt)}",
        f"    Cov = {fr(EXYt)} − ({fr(EXt)})({fr(EYt)}) = {fr(EXYt - EXt*EYt)}   (more heads → fewer tails, as expected)"])

n.quick_notes("Quick Notes — Joint Distributions", "Revision points for Lessons 10–12.", [
    ("L10 · Joint and Marginal", ["f(x, y) ≥ 0, ΣΣ or ∫∫ = 1; marginals by summing/integrating out the other variable.",
                                  "Pens 3R 2B 3K, two drawn: 3/28, 6/28, 1/28 | 9/28, 6/28 | 3/28; P(X + Y ≤ 1) = 9/14.",
                                  "Var(X) = 45/112; Cov = 3/14 − 3/8 = −9/56.",
                                  "Tyres k(x² + y²) on [30, 50)²: k = 3/3,920,000; 1/4; both under 40: 37/196."]),
    ("L11 · Conditional and Independence", ["f(y | x) = f(x, y)/g(x) on the conditional range.",
                                            "10xy², 0 < x < y < 1: g = (10/3)x(1 − x³), h = 5y⁴, f(y | x) = 3y²/(1 − x³); 8/9.",
                                            "(6 − x − y)/8: f(y | 2) = (4 − y)/2; P(Y < 3 | X = 2) = 3/4.",
                                            "Independent ⟺ f = g·h everywhere; triangular regions are never independent."]),
    ("L12 · Expectation and Covariance", ["E(X + Y) = E(X) + E(Y) always; E(XY) = E(X)E(Y) if independent.",
                                          "Cov = E(XY) − E(X)E(Y); Var(X + Y) = Var X + Var Y + 2Cov.",
                                          "2(x + y − 2xy): E(XY) = 2/9 ≠ 1/4 → dependent. x + y: Cov = −1/144."])])
n.save()
print("saved", n.out_path)
