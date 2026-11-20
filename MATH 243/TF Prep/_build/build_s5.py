"""MATH243_Stat_Correlation_Regression_Notes.docx — deck 7 (L12–L15)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

from common import exam_map, new
from m243 import STAT, g, regression, spearman_ties

DECK = STAT + r"\7. Correlation and regression analysis.pdf"

n = new("Stat", "Correlation and Regression Analysis", "MATH243_Stat_Correlation_Regression_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "a regression question in every paper"),
              ("Lesson 12 — Correlation, Scatter Diagram and Pearson's r", "types, interpretation, −1 ≤ r ≤ 1"),
              ("Lesson 13 — Spearman's Rank Correlation (with Ties)", "D², tie correction"),
              ("Lesson 14 — The Two Regression Lines", "least squares, b_yx, b_xy, estimates, all TF tables"),
              ("Lesson 15 — Goodness of Fit (R²), Polynomial and Multiple Regression", "SST = SSR + SSE, quadratic fit"),
              ("Quick Notes — Correlation and Regression", "revision bullets")],
    source_note="Page numbers refer to 7. Correlation and regression analysis.pdf (17 pp.), written as p. n. Notation: "
                "S_xx = Σx² − (Σx)²/n, S_yy = Σy² − (Σy)²/n, S_xy = Σxy − ΣxΣy/n. \"TF p.\" = merged question PDF page; "
                "\"22 batch p.\" = 2023-24 paper.")

n.h1("Exam Map — What the TF Papers Ask")
st = exam_map(n, "s5")
n.callout("focus", f"{st['n']} questions, {st['marks']} marks — the largest Statistics topic, in every paper. Nine of them "
          "are the same task: from paired data find both regression lines, r and an estimate. Since 2016-17 the papers add "
          "SSR/SST/R² adequacy, rank correlation with ties (2022-23, 2023-24) and a second-degree polynomial (2023-24). "
          "Learn the S_xx, S_yy, S_xy table — it gives every answer.")

# ------------------------------------------------------------------ L12
n.lesson("Lesson 12 — Correlation, Scatter Diagram and Pearson's r", "pp. 1–5")
n.p("Correlation analysis measures the strength (degree) of the relationship between variables (fertiliser and rice "
    "production, height and weight). Positive: both increase together; negative: one increases as the other decreases; "
    "perfect: the ratio of changes is constant (p. 1). Types: positive/negative, simple/multiple, linear/non-linear.")
n.figure_from_pdf(DECK, 2, "Figure 12.1 — Scatter diagrams: high positive, high negative and no correlation (p. 2)",
                  clip=(0.08, 0.05, 0.92, 0.47), width_cm=10)
n.figure_from_pdf(DECK, 3, "Figure 12.2 — r = ±1, r close to ±1, r = 0, and Y = X² with r = 0 (p. 3)",
                  clip=(0.08, 0.17, 0.92, 0.82), width_cm=9)
n.formula(["r = Σ(x − x̄)(y − ȳ) / √[Σ(x − x̄)² Σ(y − ȳ)²] = S_{xy}/√(S_{xx}S_{yy})"])
n.bullets(["−1 ≤ r ≤ 1. r = +1 / −1: perfect positive / negative linear relation.",
           "r near ±1: strong linear relation; near 0: weak linear relation. r = 0 does not mean \"no relation\" — the "
           "relation may be curved (p. 3)."])
n.h2("Proof that −1 ≤ r ≤ 1 (p. 5)")
n.code(["Let u = (x − x̄)/√Σ(x − x̄)²,  v = (y − ȳ)/√Σ(y − ȳ)²,  so Σu² = Σv² = 1 and Σuv = r.",
        "0 ≤ Σ(u + v)² = Σu² + Σv² + 2Σuv = 2 + 2r   ⟹  r ≥ −1",
        "0 ≤ Σ(u − v)² = 2 − 2r                       ⟹  r ≤ 1"])
r = regression([50, 50, 55, 60, 65, 65, 65, 60, 60, 50], [11, 13, 14, 16, 16, 15, 15, 14, 13, 13])
n.p(f"Sales vs expenses of 10 firms (p. 4): Σ(x − x̄)² = 360, Σ(y − ȳ)² = 22, Σ(x − x̄)(y − ȳ) = 70 → r = 70/√(360 × 22) = "
    f"{g(r['r'],4)}, a fairly high positive correlation. Advertising vs sales: r = 0.865.")
rr = regression([22, 29, 15, 18, 23], [3.5, 4.0, 3.0, 4.0, 3.5])
n.practice("Lesson 12", "(a) Actual — 2023-24 Q5(b) (22 batch p. 3) — the plot is drawn in the Intro & Graphs note, Lesson 3.",
           ["(a) Prices ($) and ratings of 5 restaurants: (22, 3.5), (29, 4.0), (15, 3.0), (18, 4.0), (23, 3.5). Draw the scatter "
            "plot and interpret whether price and rating are related.  (13)"])
n.solution()
n.code([f"Σx = 107, Σy = 18, Σx² = 2403, Σy² = 65.5, Σxy = 390.5",
        f"S_xx = 2403 − 107²/5 = {g(rr['sxx'],2)};  S_yy = 65.5 − 18²/5 = {g(rr['syy'],2)};  S_xy = 390.5 − 107×18/5 = {g(rr['sxy'],2)}",
        f"r = {g(rr['sxy'],2)}/√({g(rr['sxx'],2)} × {g(rr['syy'],2)}) = {g(rr['r'],3)}"])
n.p("The points drift upward with one exception (D): a moderate positive relationship (r ≈ 0.60) — higher prices tend to "
    "go with higher ratings, but with five restaurants the evidence is weak.")

# ------------------------------------------------------------------ L13
n.lesson("Lesson 13 — Spearman's Rank Correlation (with Ties)", "pp. 5–7")
n.p("Used when only ranks are available or the characteristic cannot be measured exactly (sincerity, honesty).")
n.formula(["r_{s} = 1 − 6ΣD² / [n(n² − 1)]",
           "Ties: r_{s} = 1 − 6[ΣD² + Σ(m³ − m)/12] / [n(n² − 1)]"])
n.p("D = difference between the two ranks; tied values get the average of the ranks they occupy; m = number of times a "
    "value is repeated (one correction term per tied group, in either series). Managers: ΣD² = 14 → r_{s} = 1 − 84/990 = "
    "0.915 (high agreement). Tests: ΣD² = 44 → r_{s} = 0.733.")
n.exam_approach(["Rank each series separately (largest = highest rank or smallest = 1 — same convention for both).",
                 "Average ranks for ties; list D and D²; add the (m³ − m)/12 corrections.",
                 "Substitute; interpret sign and size."])
b = spearman_ties([15, 20, 28, 12, 40, 60, 20, 80], [40, 30, 50, 30, 20, 10, 30, 60])
s2 = spearman_ties([50, 50, 55, 60, 65, 65, 65, 60, 60, 50], [11, 13, 14, 16, 16, 15, 15, 14, 13, 13])
n.practice("Lesson 13", "(a) Actual — 2022-23 Q4(b) (TF p. 48). (b) Actual — 2023-24 Q4(b) (22 batch p. 2).",
           ["(a) Distinguish clearly between correlation and regression analysis. Marks of 8 applicants — Bangla: 15, 20, 28, "
            "12, 40, 60, 20, 80; English: 40, 30, 50, 30, 20, 10, 30, 60. Compute the rank correlation coefficient and "
            "comment.  (12)",
            "(b) What is Pearson's correlation coefficient? How do you modify the rank formula when observations are "
            "repeated? Hourly sales x: 50, 50, 55, 60, 65, 65, 65, 60, 60, 60 and expenses y: 11, 13, 14, 16, 16, 15, 15, "
            "14, 13, 13 of 10 stores: calculate the rank correlation coefficient.  (12)"])
n.solution()
n.callout("answer", "Correlation vs regression (p. 14): correlation measures the degree and direction of association and "
          "treats X and Y symmetrically (r_{xy} = r_{yx}, unit-free, −1 to 1); regression expresses the average dependence "
          "of a dependent variable on independent variable(s) through an equation, treats them asymmetrically "
          "(b_{yx} ≠ b_{xy}, in units of the data) and is used to predict. Correlation does not imply causation; "
          "regression assumes a direction of dependence.")
n.answer("(a)", "Ranks (1 = smallest).")
n.table(["Applicant", "Bangla", "R_B", "English", "R_E", "D", "D²"],
        [[c, str(x), g(a), str(y), g(bb), g(a - bb), g((a - bb) ** 2)] for c, x, y, a, bb in
         zip("ABCDEFGH", [15, 20, 28, 12, 40, 60, 20, 80], [40, 30, 50, 30, 20, 10, 30, 60], b["rx"], b["ry"])]
        + [["Total", "", "", "", "", "0", g(b["D2"])]], widths_cm=[2.4, 2.2, 2, 2.4, 2, 2, 2.4])
n.code(["Ties: Bangla 20 twice (m = 2): (2³ − 2)/12 = 0.5;  English 30 three times (m = 3): (3³ − 3)/12 = 2",
        f"r_s = 1 − 6(81.5 + 0.5 + 2)/[8(64 − 1)] = 1 − 504/504 = {g(b['rs'])}"])
n.p("r_{s} = 0: no association between the rankings in Bangla and English. (The slide on p. 7 uses the same data.)")
n.answer("(b)", "Pearson's r: §L12. Modified formula: add Σ(m³ − m)/12 to ΣD² for every tied group.")
n.table(["x", "R_x", "y", "R_y", "D²"],
        [[str(x), g(a), str(y), g(bb), g((a - bb) ** 2)] for x, y, a, bb in
         zip([50, 50, 55, 60, 65, 65, 65, 60, 60, 60], [11, 13, 14, 16, 16, 15, 15, 14, 13, 13],
             spearman_ties([50, 50, 55, 60, 65, 65, 65, 60, 60, 60], [11, 13, 14, 16, 16, 15, 15, 14, 13, 13])["rx"],
             spearman_ties([50, 50, 55, 60, 65, 65, 65, 60, 60, 60], [11, 13, 14, 16, 16, 15, 15, 14, 13, 13])["ry"])],
        widths_cm=[3, 3, 3, 3, 3])
s3 = spearman_ties([50, 50, 55, 60, 65, 65, 65, 60, 60, 60], [11, 13, 14, 16, 16, 15, 15, 14, 13, 13])
from collections import Counter as _C
_tx = [(v, m) for v, m in sorted(_C([50, 50, 55, 60, 65, 65, 65, 60, 60, 60]).items()) if m > 1]
_ty = [(v, m) for v, m in sorted(_C([11, 13, 14, 16, 16, 15, 15, 14, 13, 13]).items()) if m > 1]
n.code([f"ΣD² = {g(s3['D2'])}. Ties in x: " + ", ".join(f"{v} (m = {m})" for v, m in _tx) + "; in y: " + ", ".join(f"{v} (m = {m})" for v, m in _ty),
        "Σ(m³ − m)/12 = " + " + ".join(g((m**3-m)/12) for _, m in _tx + _ty) + f" = {g(s3['corr'])}",
        f"r_s = 1 − 6({g(s3['D2'])} + {g(s3['corr'])})/[10(100 − 1)] = {g(s3['rs'],4)}"])
n.p("A fairly high positive rank correlation (0.68): stores with higher sales tend to have higher expenses.")
n.callout("note", "The paper prints the last sales value as 60; the slide (p. 4) has 50 for firm 10. With the slide's data "
          f"r_s = {g(s2['rs'],4)} and Pearson r = 0.787. Use the paper's numbers in the exam.")

# ------------------------------------------------------------------ L14
n.lesson("Lesson 14 — The Two Regression Lines", "pp. 8–12")
n.p("Regression studies the dependence of a dependent variable on independent variable(s), to estimate or predict its "
    "average value. Objectives (p. 9): estimate the average relationship; find the effect of each independent variable; "
    "predict the dependent variable. A deterministic relation is exact; a non-deterministic one has random error ε.")
n.formula(["Y on X: ŷ = a + b_{yx}x,  b_{yx} = [nΣxy − ΣxΣy]/[nΣx² − (Σx)²] = S_{xy}/S_{xx},  a = ȳ − b_{yx}x̄",
           "X on Y: x̂ = a' + b_{xy}y,  b_{xy} = S_{xy}/S_{yy},  a' = x̄ − b_{xy}ȳ",
           "r = ±√(b_{yx}b_{xy});  b_{yx} = r σ_{y}/σ_{x},  b_{xy} = r σ_{x}/σ_{y}"])
n.p("Least squares (p. 10): choose a, b to minimise SSE = Σ(y − a − bx)²; ∂SSE/∂a = 0 and ∂SSE/∂b = 0 give the normal "
    "equations Σy = na + bΣx and Σxy = aΣx + bΣx².")
r7 = regression([13, 1, 17, 19, 14, 15, 15, 8, 13, 3], [34.4, 38.4, 30.4, 29.7, 30.1, 33.9, 32.8, 35.2, 34.9, 36.8])
n.p(f"Transmitter example (p. 11): Σx = 118, Σy = 336.6, Σx² = 1708, Σxy = 3834.3 → b = (10×3834.3 − 118×336.6)/(10×1708 − "
    f"118²) = {g(r7['byx'],4)}, a = {g(r7['ayx'],3)}; ŷ = {g(r7['ayx'],3)} − {g(-r7['byx'],4)}x; at 10 m ŷ = "
    f"{g(r7['ayx']+10*r7['byx'],2)} dB.")
n.callout("memorize", "Use the line of the variable you want to estimate: estimate y from x with Y on X; estimate x from y "
          "with X on Y. Both lines pass through (x̄, ȳ); r has the sign of the b's.")
n.exam_approach(["Table of x, y, x², y², xy (or deviations); totals; x̄, ȳ.",
                 "S_xx, S_yy, S_xy; b_yx = S_xy/S_xx, b_xy = S_xy/S_yy; intercepts from the means.",
                 "r = S_xy/√(S_xx S_yy) (check r² = b_yx b_xy); interpret.",
                 "Estimates from the correct line; state units."])


def solve(n_, lab, x, y, xn, yn, asks, comment):
    r_ = regression(x, y)
    n_.answer(lab, f"Let x = {xn}, y = {yn}; n = {r_['n']}.")
    n_.code([f"Σx = {g(r_['Sx'])}, Σy = {g(r_['Sy'])}, Σx² = {g(r_['Sxx'])}, Σy² = {g(r_['Syy'])}, Σxy = {g(r_['Sxy'])};  x̄ = {g(r_['xb'])}, ȳ = {g(r_['yb'])}",
             f"S_xx = {g(r_['sxx'])},  S_yy = {g(r_['syy'])},  S_xy = {g(r_['sxy'])}",
             f"b_yx = {g(r_['sxy'])}/{g(r_['sxx'])} = {g(r_['byx'])};   Y on X: ŷ = {g(r_['ayx'])} + ({g(r_['byx'])})x",
             f"b_xy = {g(r_['sxy'])}/{g(r_['syy'])} = {g(r_['bxy'])};   X on Y: x̂ = {g(r_['axy'])} + ({g(r_['bxy'])})y",
             f"r = {g(r_['sxy'])}/√({g(r_['sxx'])} × {g(r_['syy'])}) = {g(r_['r'])}   (check √(b_yx b_xy) = {g(math.sqrt(r_['byx']*r_['bxy']))})"]
            + [a(r_) for a in asks])
    n_.p(comment)


n.practice("Lesson 14",
           "(a) Actual — 2022-23 Q4(c) (TF p. 49). (b) Actual — 2019-20 Q6(a) (TF p. 34). (c) Actual — 2018-19 Q6(a) (TF p. 24). "
           "(d) Actual — 2021-22 Q7(a) (TF pp. 44–45). (e) Actual — 2015-16 Q7(b) (TF p. 16). (f) Actual — 2014-15 Q7(a) "
           "(TF p. 11). (g) Actual — 2013-14 Q7(a) (TF p. 8). (h) Actual — 2012-13 Q7(a) (TF p. 5). (i) Actual — 2011-12 "
           "Q7(a) (TF p. 2).",
           ["(a) Ages of husbands 22, 23, 23, 24, 26, 27, 27, 28, 30, 30 and wives 18, 20, 21, 20, 21, 22, 23, 24, 25, 26: the two "
            "regression equations; husband's age when the wife is 30; wife's age when the husband is 25; comment on r.  (13)",
            "(b) Distance to transmitter X: 13, 12, 17, 19, 14, 15, 15, 8, 13, 3 and signal strength Y: 34.4, 38.4, 30.4, 29.7, "
            "30.1, 33.9, 32.8, 35.2, 34.9, 36.8. Regression line of Y on X; predict Y at 10 m.  (17)",
            "(c) Production: mean 35.6, SD 10.5; capacity utilisation: mean 84.8, SD 8.5; r = 0.62. Regression of capacity "
            "utilisation on production; estimate production when capacity utilisation is 70 %.  (20)",
            "(d) Specific gravity x and modulus of rupture y of 15 loblolly pines (TF p. 45): both regression coefficients; "
            "compute and interpret r.  (20)",
            "(e) Years of service 10, 8, 9, 5, 7, 6, 12, 11, 13 and income ('000) 17, 12, 14, 8, 10, 9, 20, 18, 22: regression "
            "equations and r; starting income for 15 years' experience.  (17)",
            "(f) X: 42, 44, 58, 55, 89, 98, 66; Y: 56, 49, 53, 58, 65, 76, 51 — regression lines Y on X and X on Y; r.  (20)",
            "(g) Husbands 22, 25, 28, 31, 35, 32, 37, 39; wives 19, 18, 22, 29, 31, 23, 30, 33: regression equations, r; most "
            "likely age of husband when the wife is 24.  (20)",
            "(h) Economics 47, 38, 34, 44, 32, 41, 35, 32, 42, 30; Business 38, 34, 42, 39, 34, 33, 30, 41, 38, 28: regression "
            "equations and coefficients; Economics when Business = 36; Business when Economics = 44; comment on r.  (18)",
            "(i) X: 105, 112, 104, 114, 117, 108, 106, 117, 111; Y: 58, 56, 47, 46, 51, 64, 66, 50, 55 — two regression lines, r.  (20)"])
n.solution()
solve(n, "(a)", [22, 23, 23, 24, 26, 27, 27, 28, 30, 30], [18, 20, 21, 20, 21, 22, 23, 24, 25, 26], "husband's age", "wife's age",
      [lambda r_: f"Husband at wife = 30: x̂ = {g(r_['axy'])} + {g(r_['bxy'])}(30) = {g(r_['axy']+30*r_['bxy'],2)} years",
       lambda r_: f"Wife at husband = 25: ŷ = {g(r_['ayx'])} + {g(r_['byx'])}(25) = {g(r_['ayx']+25*r_['byx'],2)} years"],
      "r = 0.95: very high positive correlation — older husbands have older wives.")
solve(n, "(b)", [13, 12, 17, 19, 14, 15, 15, 8, 13, 3], [34.4, 38.4, 30.4, 29.7, 30.1, 33.9, 32.8, 35.2, 34.9, 36.8],
      "distance (m)", "signal (dB)",
      [lambda r_: f"At x = 10: ŷ = {g(r_['ayx'])} − {g(-r_['byx'])}(10) = {g(r_['ayx']+10*r_['byx'],2)} dB"],
      "Signal strength falls about 0.46 dB per metre. (With the slide's value 1 instead of 12 for the second distance the line "
      "is ŷ = 38.804 − 0.4359x and the prediction 34.44 dB.)")
byx, bxy = 0.62 * 8.5 / 10.5, 0.62 * 10.5 / 8.5
n.answer("(c)", "x = production, y = capacity utilisation.")
n.code([f"b_yx = r σ_y/σ_x = 0.62 × 8.5/10.5 = {g(byx)};  y − 84.8 = {g(byx)}(x − 35.6)  →  ŷ = {g(84.8-byx*35.6)} + {g(byx)}x",
        f"b_xy = r σ_x/σ_y = 0.62 × 10.5/8.5 = {g(bxy)};  x − 35.6 = {g(bxy)}(y − 84.8)  →  x̂ = {g(35.6-bxy*84.8)} + {g(bxy)}y",
        f"Production when y = 70: x̂ = 35.6 + {g(bxy)}(70 − 84.8) = {g(35.6+bxy*(70-84.8),2)}"])
solve(n, "(d)", [0.414, 0.383, 0.399, 0.402, 0.442, 0.422, 0.466, 0.500, 0.514, 0.530, 0.569, 0.558, 0.577, 0.572, 0.548],
      [29186, 29266, 26215, 30162, 38867, 37831, 44576, 46097, 59698, 67705, 66088, 78486, 89869, 77369, 67095],
      "specific gravity (g/cm³)", "modulus of rupture (kPa)", [],
      "b_yx ≈ 282,459 kPa per g/cm³ (an increase of 0.01 in specific gravity raises the modulus by about 2,825 kPa); "
      "b_xy ≈ 3.28 × 10⁻⁶ g/cm³ per kPa. r = 0.962: a very strong positive linear relationship — denser wood is stronger; "
      "r² = 0.926, so 92.6 % of the variation in modulus of rupture is explained by specific gravity.")
solve(n, "(e)", [10, 8, 9, 5, 7, 6, 12, 11, 13], [17, 12, 14, 8, 10, 9, 20, 18, 22], "years of service", "income ('000)",
      [lambda r_: f"At x = 15: ŷ = {g(r_['ayx'])} + {g(r_['byx'])}(15) = {g(r_['ayx']+15*r_['byx'],2)} thousand"],
      "r = 0.994: almost perfect positive correlation; recommend a starting income of about Tk 25,440.")
solve(n, "(f)", [42, 44, 58, 55, 89, 98, 66], [56, 49, 53, 58, 65, 76, 51], "X", "Y", [],
      "r = 0.84: high positive correlation.")
solve(n, "(g)", [22, 25, 28, 31, 35, 32, 37, 39], [19, 18, 22, 29, 31, 23, 30, 33], "husband's age", "wife's age",
      [lambda r_: f"Husband at wife = 24: x̂ = {g(r_['axy'])} + {g(r_['bxy'])}(24) = {g(r_['axy']+24*r_['bxy'],2)} years"],
      "r = 0.92: high positive correlation.")
solve(n, "(h)", [47, 38, 34, 44, 32, 41, 35, 32, 42, 30], [38, 34, 42, 39, 34, 33, 30, 41, 38, 28], "Economics", "Business",
      [lambda r_: f"Economics at Business = 36: x̂ = {g(r_['axy'])} + {g(r_['bxy'])}(36) = {g(r_['axy']+36*r_['bxy'],2)}",
       lambda r_: f"Business at Economics = 44: ŷ = {g(r_['ayx'])} + {g(r_['byx'])}(44) = {g(r_['ayx']+44*r_['byx'],2)}"],
      "Regression coefficients b_yx = 0.245, b_xy = 0.379; r = 0.30 — a weak positive correlation, so the estimates are not reliable.")
solve(n, "(i)", [105, 112, 104, 114, 117, 108, 106, 117, 111], [58, 56, 47, 46, 51, 64, 66, 50, 55], "X", "Y", [],
      "r = −0.45: moderate negative correlation.")

# ------------------------------------------------------------------ L15
n.lesson("Lesson 15 — Goodness of Fit (R²), Polynomial and Multiple Regression", "pp. 12–17")
n.formula(["SST = Σ(y − ȳ)² = SSR + SSE,   SSR = Σ(ŷ − ȳ)²,   SSE = Σ(y − ŷ)²",
           "R² = SSR/SST,  0 ≤ R² ≤ 1;  simple linear: R² = r²,  SSR = b_{yx}S_{xy}"])
n.p("R² is the proportion (percentage) of the total variation in y explained by the regression. Close to 1 → the model "
    "fits well; deterministic relation → SSE = 0, R² = 1. Hardness vs tensile strength (p. 14): ŷ = 14.37 + 0.4167x, "
    "R² = 0.51 — only half the variation explained, so the linear model is not very adequate.")
n.h2("Multiple and Polynomial Regression (pp. 14–17)")
n.formula(["ŷ = b_{0} + b_{1}x_{1} + b_{2}x_{2}:  Σy = nb_{0} + b_{1}Σx_{1} + b_{2}Σx_{2},  Σx_{1}y = b_{0}Σx_{1} + b_{1}Σx_{1}² + b_{2}Σx_{1}x_{2},  Σx_{2}y = …",
           "ŷ = a + bx + cx²: treat x as x_{1} and x² as x_{2}"])
X1 = np.array([24, 0, 25, 0, 5, 18, 20, 0, 15, 6.]); X2 = np.array([53, 47, 50, 52, 40, 44, 46, 45, 56, 40.])
Yr = np.array([11, 22, 7, 26, 22, 15, 9, 23, 15, 24.])
coef = np.linalg.lstsq(np.c_[np.ones(10), X1, X2], Yr, rcond=None)[0]
n.p(f"Rice (p. 15): rainfall x_{{1}}, urea x_{{2}}: least squares gives ŷ = {g(coef[0],3)} {'+' if coef[1]>=0 else '−'} "
    f"{g(abs(coef[1]),4)}x_{{1}} {'+' if coef[2]>=0 else '−'} {g(abs(coef[2]),4)}x_{{2}}.")
n.exam_approach(["Fit the line; ŷ for each x; SSR = Σ(ŷ − ȳ)² (or b S_xy), SST = S_yy, SSE = SST − SSR.",
                 "R² = SSR/SST; ≥ 0.8 adequate, around 0.5 or below doubtful.",
                 "Quadratic: compute Σx, Σx², Σx³, Σx⁴, Σy, Σxy, Σx²y; solve the three normal equations; R² = 1 − SSE/SST."])
re = regression([16, 12, 18, 4, 3], [87, 88, 89, 68, 58])
X = np.array([0, 1, 2, 3, 4, 5.]); Y = np.array([15, 25, 40, 55, 52, 43.])
c = np.polyfit(X, Y, 2)[::-1]; yh = c[0] + c[1] * X + c[2] * X ** 2
sst = ((Y - Y.mean()) ** 2).sum(); sse = ((Y - yh) ** 2).sum()
n.practice("Lesson 15", "(a) Actual — 2016-17 Q6(b) (TF p. 20) = 2020-21 Q6(a) (TF p. 37). (b) Actual — 2023-24 Q4(c) (22 batch p. 2).",
           ["(a) Experience X: 16, 12, 18, 4, 3 and performance rating Y: 87, 88, 89, 68, 58. (i) Fit a linear regression of Y "
            "on X. (ii) Find SSR and SST. (iii) Is the linear model appropriate? Justify with the coefficient of determination.  (18)",
            "(b) Briefly mention the objectives of correlation and regression analysis. Nitrogen doses x: 0, 1, 2, 3, 4, 5 "
            "(lb/acre) and yield y: 15, 25, 40, 55, 52, 43 (maunds/acre). Fit a second-degree polynomial and obtain the "
            "coefficient of determination.  (12)"])
n.solution()
yhat = re["ayx"] + re["byx"] * np.array([16, 12, 18, 4, 3.])
n.code([f"Σx = 53, Σy = 390, Σx² = 749, Σxy = 4496, Σy² = 31222;  x̄ = 10.6, ȳ = 78",
        f"S_xx = 749 − 53²/5 = {g(re['sxx'])};  S_xy = 4496 − 53×390/5 = {g(re['sxy'])};  S_yy = 31222 − 390²/5 = {g(re['syy'])}",
        f"(i)   b = {g(re['sxy'])}/{g(re['sxx'])} = {g(re['byx'])};  a = 78 − {g(re['byx'])} × 10.6 = {g(re['ayx'])};  ŷ = {g(re['ayx'])} + {g(re['byx'])}x",
        f"      fitted ŷ: " + ", ".join(g(v, 2) for v in yhat),
        f"(ii)  SSR = Σ(ŷ − ȳ)² = b S_xy = {g(re['byx'])} × {g(re['sxy'])} = {g(re['byx']*re['sxy'],2)};  SST = S_yy = {g(re['syy'])}",
        f"(iii) R² = SSR/SST = {g(re['byx']*re['sxy'],2)}/{g(re['syy'])} = {g(re['byx']*re['sxy']/re['syy'],4)}"])
n.p("About 87 % of the variation in performance rating is explained by experience, so the linear model is appropriate "
    "(SSE = 101.98 is small relative to SST).")
n.answer("(b)", "Objectives: L14 (estimate the average relationship, measure the effect of each independent variable, "
         "predict). Normal equations for ŷ = a + bx + cx² (n = 6):")
n.code(["Σx = 15, Σx² = 55, Σx³ = 225, Σx⁴ = 979, Σy = 230, Σxy = 693, Σx²y = 2587",
        "230  = 6a  + 15b  + 55c",
        "693  = 15a + 55b  + 225c",
        "2587 = 55a + 225b + 979c",
        f"Solving: a = {g(c[0],4)},  b = {g(c[1],4)},  c = {g(c[2],4)}",
        f"ŷ = {g(c[0],3)} + {g(c[1],3)}x − {g(-c[2],3)}x²",
        f"Fitted: " + ", ".join(g(v, 2) for v in yh),
        f"SST = Σ(y − ȳ)² = {g(sst,2)};  SSE = Σ(y − ŷ)² = {g(sse,2)};  R² = 1 − SSE/SST = {g(1-sse/sst,4)}"])
n.p(f"R² = {g(1-sse/sst,3)}: the quadratic explains 93 % of the variation in yield. Yield is maximum near x = −b/(2c) = "
    f"{g(-c[1]/(2*c[2]),2)} lb/acre.")
n.callout("note", "The slide (p. 17) uses the same data; its working table matches these sums.")

n.quick_notes("Quick Notes — Correlation and Regression", "Revision points for Lessons 12–15.", [
    ("L12 · Pearson r", ["r = S_xy/√(S_xx S_yy), −1 ≤ r ≤ 1 (proof with Σ(u ± v)² ≥ 0); r = 0 ≠ no relation.",
                         "Sales/expenses r = 0.787; restaurants r = 0.60."]),
    ("L13 · Rank Correlation", ["r_s = 1 − 6[ΣD² + Σ(m³ − m)/12]/[n(n² − 1)].",
                                "Bangla/English: ΣD² = 81.5, correction 2.5 → r_s = 0. Stores: r_s = 0.679 (paper data; 0.752 with the slide data)."]),
    ("L14 · Regression Lines", ["b_yx = S_xy/S_xx, b_xy = S_xy/S_yy, lines through (x̄, ȳ); r² = b_yx b_xy.",
                                "From summary data: b_yx = rσ_y/σ_x (capacity: ŷ = 66.93 + 0.502x; production at 70: 24.26).",
                                "Husband/wife 2022-23: r = 0.95, 34.86 and 21.18. Service/income: 25.44. Transmitter (paper): 34.99 dB."]),
    ("L15 · R² and Polynomial", ["SST = SSR + SSE; R² = SSR/SST = r² for a line. Experience/rating R² = 0.873.",
                                 "Quadratic: three normal equations; nitrogen ŷ = 11.536 + 21.654x − 2.982x², R² = 0.931."])])
n.save()
print("saved", n.out_path)
