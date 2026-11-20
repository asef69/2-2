"""MATH243_Stat_Skewness_Moments_Kurtosis_Notes.docx — deck 4 (L10–L11)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

from common import exam_map, new
from m243 import STAT, Grouped, g

DECK = STAT + r"\4. Skewness, Moments and Kurtosis.pdf"
cl = lambda a, h, k: [(a + i * h, a + (i + 1) * h) for i in range(k)]

n = new("Stat", "Skewness, Moments and Kurtosis", "MATH243_Stat_Skewness_Moments_Kurtosis_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "the single most repeated Statistics question"),
              ("Lesson 10 — Skewness: Pearson, Bowley and Kelly Coefficients", "shapes, three coefficients, interpretation"),
              ("Lesson 11 — Moments, β₁, β₂, γ₁, γ₂ and Kurtosis", "raw → central moments, kurtosis, all TF tables solved"),
              ("Quick Notes — Skewness, Moments and Kurtosis", "revision bullets")],
    source_note="Page numbers refer to 4. Skewness, Moments and Kurtosis.pdf (15 pp.), written as p. n. Grouped working "
                "uses the slide method: d = (x − A)/h, μ'_r = (Σfd^{r}/N)h^{r}. \"TF p.\" = merged question PDF page; "
                "\"22 batch p.\" = 2023-24 paper.")

n.h1("Exam Map — What the TF Papers Ask")
st = exam_map(n, "s4")
n.callout("focus", f"{st['n']} questions, {st['marks']} marks — asked in every one of the 12 papers, usually for 15–25 "
          "marks. The table 10–20 … 50–60 with f = 18, 20, 30, 22, 10 alone appeared in 2014-15, 2016-17, 2018-19 and "
          "2022-23, and 174, 86, 32, 181, 27 in 2013-14 and 2015-16. The answer is always the same five-column table "
          "(f, d, fd, fd², fd³, fd⁴), the four raw moments, conversion to central moments, then β₁, β₂ (γ₁, γ₂) and a "
          "comment. Do it until it takes 15 minutes.")

# ------------------------------------------------------------------ L10
n.lesson("Lesson 10 — Skewness: Pearson, Bowley and Kelly Coefficients", "pp. 1–7")
n.p("Central tendency gives the centre and dispersion the spread, but neither describes how the data are arranged about the "
    "centre. **Skewness** is lack of symmetry: measures of variation give the amount of variation, skewness gives its "
    "direction (p. 1).")
n.figure_from_pdf(DECK, 1, "Figure 10.1 — Symmetric, positively and negatively skewed distributions (p. 1)",
                  clip=(0.08, 0.47, 0.92, 0.80), width_cm=10)
n.bullets(["Symmetric: mean = median = mode.", "Positively skewed: mean > median > mode (long right tail).",
           "Negatively skewed: mode > median > mean (long left tail)."])
n.formula(["Pearson: Sk_{P} = (Mean − Mode)/σ   (or 3(Mean − Median)/σ)",
           "Bowley: Sk_{B} = (Q_{3} + Q_{1} − 2Q_{2})/(Q_{3} − Q_{1})",
           "Kelly: Sk_{K} = (P_{90} − 2P_{50} + P_{10})/(P_{90} − P_{10}) = (D_{9} − 2D_{5} + D_{1})/(D_{9} − D_{1})"])
n.p("Sign: > 0 positive, < 0 negative, 0 symmetric. Bowley lies in −1 to +1 (quartile based); Pearson is usually within ±1 "
    "(theoretically ±3 with the median form).")
n.h3("Slide examples (pp. 3–5)")
n.table(["Data", "Mean", "Mode", "σ", "Sk_{P}", "Comment"],
        [["Profits 100–240 (N = 1000)", "177.86", "190.56", "25.2", "−0.504", "moderately negatively skewed"],
         ["Rejects 21–55 (N = 120)", "36.96", "37.21", "6.736", "−0.037", "slightly skewed to the left"],
         ["Ages 20–55 (N = 100)", "37.25", "36.67", "8.29", "0.07", "slightly positively skewed"]],
        widths_cm=[4.2, 1.8, 1.8, 1.6, 1.8, 6], font_size=8.5)
n.p("Practice answers (pp. 6–7): 46.4/48.89/24.56/−0.101; 25.9/24.07/10.963/0.167; 33.156/32.63/17.08/0.031; "
    "4781.5/4866.67/340.4/−0.25; −0.267; 30.1/27.73/10.45/0.227; 23.1/22.5/6.49/0.092; −0.023; −0.026; −0.572.")
n.callout("answer", "Merits and drawbacks (2020-21 Q5(b)): Bowley's coefficient uses only the quartiles, so it is easy to "
          "compute, works for open-ended classes and is not affected by extreme values, but it ignores the 50 % of the "
          "data outside Q₁–Q₃. Kelly's coefficient uses P₁₀ and P₉₀, so it covers the central 80 % — more of the data than "
          "Bowley — while still ignoring the extreme 10 % at each end. Pearson's coefficient uses every observation "
          "through the mean and σ but needs a well-defined mode (fails for bimodal data). Moment measures (γ₁) use all the "
          "data and are the most reliable.")
n.exam_approach(["Find mean, σ (step deviation) and mode (Δ formula), or median when the mode is ill-defined.",
                 "Bowley/Kelly: cumulative frequencies, then Q1, Q2, Q3 (or D1, D5, D9) by the positional formula.",
                 "Substitute; state the sign and size (|Sk| < 0.1 nearly symmetric, 0.1–0.5 moderate, > 0.5 marked)."])
Gw = Grouped(cl(30, 10, 6), [18, 37, 45, 27, 15, 8], A=65)
q1, q2, q3 = (Gw.quantile(i)[0] for i in (1, 2, 3))
d1, d5, d9 = (Gw.quantile(i, 10)[0] for i in (1, 5, 9))
runsB = np.array([54, 78, 55, 66, 63, 69, 74, 64, 59, 85.])
rb = np.sort(runsB); mB = rb.mean(); dev = rb - mB
m2, m3, m4 = (dev ** 2).mean(), (dev ** 3).mean(), (dev ** 4).mean()
runsA = np.array([55, 80, 78, 49, 52, 76, 78, 76, 62, 76.])
n.practice("Lesson 10", "(a) Actual — 2020-21 Q5(b) (TF p. 37). (b) Actual — 2012-13 Q6(a) (TF p. 5).",
           ["(a) Weights 30–40 … 80–90 with frequencies 18, 37, 45, 27, 15, 8. Calculate Bowley's and Kelly's coefficients "
            "of skewness, interpret, and discuss the merits and drawbacks of the methods.  (15)",
            "(b) Runs of A in 10 matches: 55, 80, 78, 49, 52, 76, 78, 76, 62, 76; of B: 54, 78, 55, 66, 63, 69, 74, 64, 59, 85. "
            "(i) Pearson's coefficient of skewness and kurtosis and Bowley's coefficient of skewness for B only; comment on "
            "the shape. (ii) If consistency is the criterion for a prize, who should get it?  (15)"])
n.solution()
n.answer("(a)", "N = 150; cumulative frequencies 18, 55, 100, 127, 142, 150.")
n.code([f"Q1: N/4 = 37.5 → class 40–50:  Q1 = 40 + (37.5 − 18)/37 × 10 = {g(q1,3)}",
        f"Q2: N/2 = 75 → class 50–60:    Q2 = 50 + (75 − 55)/45 × 10 = {g(q2,3)}",
        f"Q3: 3N/4 = 112.5 → class 60–70: Q3 = 60 + (112.5 − 100)/27 × 10 = {g(q3,3)}",
        f"Sk_B = ({g(q3,3)} + {g(q1,3)} − 2 × {g(q2,3)})/({g(q3,3)} − {g(q1,3)}) = {g((q3+q1-2*q2)/(q3-q1),4)}",
        f"D1: N/10 = 15 → class 30–40:   D1 = 30 + 15/18 × 10 = {g(d1,3)}",
        f"D5 = median = {g(d5,3)}",
        f"D9: 9N/10 = 135 → class 70–80: D9 = 70 + (135 − 127)/15 × 10 = {g(d9,3)}",
        f"Sk_K = ({g(d9,3)} − 2 × {g(d5,3)} + {g(d1,3)})/({g(d9,3)} − {g(d1,3)}) = {g((d9+d1-2*d5)/(d9-d1),4)}"])
n.p("Both coefficients are positive: the distribution is slightly positively skewed (longer upper tail). Kelly's value "
    "(0.13) is larger than Bowley's (0.05) because it also reflects the long upper tail between Q₃ and D₉, which Bowley "
    "ignores. Merits/drawbacks: model answer above.")
n.answer("(b)", "B sorted: " + ", ".join(g(v) for v in rb) + f"; n = 10, Σx = 667, x̄ = {g(mB)}.")
n.code([f"Σ(x − x̄)² = 900.1 → σ = √(900.1/10) = {g(np.sqrt(m2),3)};  median = (64 + 66)/2 = 65",
        "No value repeats, so the mode is not defined → use Pearson's second coefficient:",
        f"Sk_P = 3(Mean − Median)/σ = 3(66.7 − 65)/{g(np.sqrt(m2),3)} = {g(3*(mB-65)/np.sqrt(m2),3)}",
        f"Moments about the mean: m2 = {g(m2,2)}, m3 = Σ(x − x̄)³/10 = {g(m3,2)}, m4 = Σ(x − x̄)⁴/10 = {g(m4,1)}",
        f"Kurtosis β2 = m4/m2² = {g(m4,1)}/{g(m2,2)}² = {g(m4/m2**2,3)}   (γ1 = m3/m2^1.5 = {g(m3/m2**1.5,3)})",
        "Q1 = value at (n + 1)/4 = 2.75th = 55 + 0.75(59 − 55) = 58;  Q3 = 8.25th = 74 + 0.25(78 − 74) = 75",
        "Sk_B = (75 + 58 − 2 × 65)/(75 − 58) = 3/17 = 0.176"])
n.p(f"B's runs are moderately positively skewed (Sk_{{P}} = 0.54, Sk_{{B}} = 0.18) and platykurtic (β_{{2}} = 2.22 < 3). "
    f"(ii) A: x̄ = 68.2, σ = 11.65, C.V. = 17.08 %; B: x̄ = 66.7, σ = 9.49, C.V. = 14.22 %. B is more consistent → the prize goes to B.")

# ------------------------------------------------------------------ L11
n.lesson("Lesson 11 — Moments, β₁, β₂, γ₁, γ₂ and Kurtosis", "pp. 8–15")
n.h2("1. Moments (p. 8)")
n.formula(["Raw (about A): μ'_{r} = Σf(x − A)^{r}/N = (Σfd^{r}/N) h^{r}",
           "Central (about x̄): μ_{r} = Σf(x − x̄)^{r}/N;  μ_{1} = 0, μ_{2} = σ²"])
n.h2("2. Raw → Central Moments (pp. 9–10)")
n.formula(["μ_{2} = μ'_{2} − μ'_{1}²", "μ_{3} = μ'_{3} − 3μ'_{2}μ'_{1} + 2μ'_{1}³",
           "μ_{4} = μ'_{4} − 4μ'_{3}μ'_{1} + 6μ'_{2}μ'_{1}² − 3μ'_{1}⁴"])
n.p("Proof idea (p. 9): write x − x̄ = (x − A) − (x̄ − A) with x̄ − A = μ'_{1}, expand by the binomial theorem and average term "
    "by term, e.g. μ_{2} = μ'_{2} − 2μ'_{1}μ'_{1} + μ'_{1}² = μ'_{2} − μ'_{1}².")
n.h2("3. Moment Measures of Skewness and Kurtosis (pp. 12–13)")
n.formula(["β_{1} = μ_{3}²/μ_{2}³,  γ_{1} = μ_{3}/μ_{2}^{3/2}  (sign gives the direction)",
           "β_{2} = μ_{4}/μ_{2}²,  γ_{2} = β_{2} − 3"])
n.bullets(["Kurtosis = degree of peakedness relative to the normal curve.",
           "β_{2} > 3 (γ_{2} > 0): leptokurtic (more peaked); β_{2} = 3: mesokurtic (normal); β_{2} < 3: platykurtic (flatter)."])
n.figure_from_pdf(DECK, 12, "Figure 11.1 — Leptokurtic, mesokurtic and platykurtic curves (p. 12)",
                  clip=(0.08, 0.48, 0.95, 0.70), width_cm=9)
n.callout("answer", "Definitions (2022-23 Q6(a), 2016-17 Q6(a), 2018-19 Q5(b)): Variance σ² — the mean of the squared "
          "deviations from the mean, Σf(x − x̄)²/N; SD σ — its positive square root, in the units of the data (e.g. wages "
          "with σ = Tk 8 vary about Tk 8 around the mean). Moments — μ_r = Σf(x − x̄)^{r}/N; the first four describe "
          "location, spread, asymmetry and peakedness. Skewness — departure from symmetry (income distributions are "
          "positively skewed). Kurtosis — peakedness relative to the normal curve (exam marks crowded at the mean → "
          "leptokurtic).")
n.exam_approach(["Table: class, x, f, d = (x − A)/h, fd, fd², fd³, fd⁴; totals.",
                 "μ'_{1…4} = (Σfd^{r}/N)h^{r}.",
                 "μ_{2}, μ_{3}, μ_{4} by the conversion formulas (keep 4 decimals; μ'_{1} is negative when Σfd < 0).",
                 "β_{1}, β_{2}, γ_{1}, γ_{2}; comment on skewness (sign of μ_{3}) and kurtosis (β_{2} vs 3).",
                 "If Pearson's coefficient is asked, also give mean, mode, σ and (mean − mode)/σ."])


def full(n_, G, name, pearson=True, note=""):
    n_.table(G.headers(4, name=name), G.rows(4), widths_cm=[2.4, 1.8, 1.6, 1.6, 1.9, 2.1, 2.3, 3.5], font_size=8.5)
    (m1, m2, m3, m4), (_, u2, u3, u4) = G.central()
    b1, b2, g1, g2 = G.beta_gamma()
    N_, h = G.N, G.h
    lines = [f"μ'1 = ({g(G.s[1])}/{N_}) × {g(h)} = {g(m1)};   μ'2 = ({g(G.s[2])}/{N_}) × {g(h)}² = {g(m2)}",
             f"μ'3 = ({g(G.s[3])}/{N_}) × {g(h)}³ = {g(m3)};   μ'4 = ({g(G.s[4])}/{N_}) × {g(h)}⁴ = {g(m4)}",
             f"μ2 = {g(m2)} − ({g(m1)})² = {g(u2)}",
             f"μ3 = {g(m3)} − 3({g(m2)})({g(m1)}) + 2({g(m1)})³ = {g(u3)}",
             f"μ4 = {g(m4)} − 4({g(m3)})({g(m1)}) + 6({g(m2)})({g(m1)})² − 3({g(m1)})⁴ = {g(u4,2)}",
             f"β1 = μ3²/μ2³ = {g(b1)};  γ1 = μ3/μ2^1.5 = {g(g1)};   β2 = μ4/μ2² = {g(b2)};  γ2 = {g(g2)}"]
    if pearson:
        mo, dd = G.mode()
        lines.append(f"Mean = {g(G.A)} + ({g(G.s[1])}/{N_})({g(h)}) = {g(G.mean)};  σ = √μ2 = {g(G.sd)};  "
                     f"Mode = {g(dd['L'])} + {dd['d1']}/({dd['d1']} + {dd['d2']}) × {g(h)} = {g(mo)}")
        lines.append(f"Pearson Sk = (Mean − Mode)/σ = ({g(G.mean)} − {g(mo)})/{g(G.sd)} = {g((G.mean-mo)/G.sd)}")
    n_.code(lines)
    sk = "positively" if u3 > 0 else "negatively"
    kt = "platykurtic (flatter than normal)" if b2 < 3 else "leptokurtic (more peaked than normal)"
    n_.p(f"Comment: μ_{{3}} {'>' if u3 > 0 else '<'} 0 so the distribution is {sk} skewed "
         f"({'only slightly' if abs(g1) < 0.2 else 'moderately'}, γ_{{1}} = {g(g1,3)}), and β_{{2}} = {g(b2,3)} < 3 → {kt}. {note}"
         if b2 < 3 else
         f"Comment: {sk} skewed (γ_{{1}} = {g(g1,3)}); β_{{2}} = {g(b2,3)} > 3 → {kt}. {note}")


G1 = Grouped(cl(10, 10, 5), [18, 20, 30, 22, 10], A=35)
G2 = Grouped(cl(10, 10, 5), [174, 86, 32, 181, 27], A=35)
G3 = Grouped(cl(50, 20, 7), [4, 8, 12, 20, 6, 7, 3], A=120)
G4 = Grouped(cl(0, 10, 7), [8, 12, 20, 30, 15, 10, 5], A=35)
G5 = Grouped(cl(20.5, 6, 6), [83, 75, 176, 130, 92, 54], A=41.5)
n.practice("Lesson 11",
           "(a) Actual — 2022-23 Q6(c) (TF p. 50); same table: 2018-19 Q5(b), 2016-17 Q6(a), 2014-15 Q6(b). "
           "(b) Actual — 2019-20 Q5(b) (TF p. 34). (c) Actual — 2023-24 Q6(a) (22 batch p. 3). (d) Actual — 2015-16 Q7(a) "
           "(TF p. 15) = 2013-14 Q6(b). (e) Actual — 2011-12 Q6(a) (TF p. 2).",
           ["(a) Profits (lakhs) 10–20, 20–30, 30–40, 40–50, 50–60 with 18, 20, 30, 22, 10 companies. Calculate the first four "
            "moments about an assumed mean, convert them to moments about the mean, compute γ₁ and γ₂ (β₁, β₂, Pearson's "
            "coefficient) and comment.  (15–20)",
            "(b) Earnings (Tk) 50–70 … 170–190 with 4, 8, 12, 20, 6, 7, 3 employees: first four moments about an assumed "
            "mean, moments about the mean, γ₁ and γ₂.  (25)",
            "(c) Marks 0–10 … 60–70 with 8, 12, 20, 30, 15, 10, 5 students: first four moments about the mean, β₁, β₂ and "
            "comment.  (13)",
            "(d) Classes 10–20 … 50–60 with frequencies 174, 86, 32, 181, 27: coefficients of skewness and kurtosis; comment.  (18)",
            "(e) Ages 21–26, 27–32, 33–38, 39–44, 45–50, 51–56 with 83, 75, 176, 130, 92, 54 persons: Pearson's first "
            "coefficient of skewness and kurtosis; comment.  (20)"])
n.solution()
n.answer("(a)", "A = 35, h = 10, N = 100.")
full(n, G1, "Profit", note="This matches the slide example on p. 11 (μ₄ = 47327.5).")
n.answer("(b)", "A = 120, h = 20, N = 60 (slide example pp. 14–15).")
full(n, G3, "Earnings", pearson=False, note="The slide's γ₁ = 0.1693, γ₂ = −0.44 agree.")
n.answer("(c)", "A = 35, h = 10, N = 100.")
full(n, G4, "Marks", pearson=False)
n.answer("(d)", "A = 35, h = 10, N = 500.")
full(n, G2, "Class", note="The frequencies have two peaks (174 and 181), so the mode is ill-defined and Pearson's value "
     "(−0.99, using the Δ formula in 40–50) contradicts the moment measure; quote the moment coefficient γ₁ = 0.097 "
     "(nearly symmetric) and β₂ = 1.39 (strongly platykurtic — a U-/bimodal shape).")
n.answer("(e)", "Inclusive classes → boundaries 20.5–26.5, …, 50.5–56.5; mid-values 23.5, 29.5, …, 53.5; A = 41.5, h = 6, N = 610.")
full(n, G5, "Age")

n.quick_notes("Quick Notes — Skewness, Moments and Kurtosis", "Revision points for Lessons 10–11.", [
    ("L10 · Skewness", ["Sk_P = (Mean − Mode)/σ or 3(Mean − Median)/σ; Bowley (Q3 + Q1 − 2Q2)/(Q3 − Q1); Kelly with D1, D5, D9.",
                        "Weights: Bowley 0.052, Kelly 0.129 (slightly positive). Runs B: Sk_P 0.54, Bowley 0.18, β2 2.22; B wins (C.V. 14.2 %)."]),
    ("L11 · Moments and Kurtosis", ["μ'_r = (Σfd^r/N)h^r; μ2 = μ'2 − μ'1²; μ3 = μ'3 − 3μ'2μ'1 + 2μ'1³; μ4 = μ'4 − 4μ'3μ'1 + 6μ'2μ'1² − 3μ'1⁴.",
                                    "β1 = μ3²/μ2³, γ1 = μ3/μ2^{3/2}; β2 = μ4/μ2², γ2 = β2 − 3; β2 < 3 platy, > 3 lepto.",
                                    "18-20-30-22-10: μ2 152.04, μ3 21.31, μ4 47327.5, γ1 0.011, β2 2.05.",
                                    "Earnings: γ1 0.169, γ2 −0.443. Marks 0–70: β1 0.0053, β2 2.52. 174…27: γ1 0.097, β2 1.39. Ages: Sk_P 0.136, β2 2.21."])])
n.save()
print("saved", n.out_path)
