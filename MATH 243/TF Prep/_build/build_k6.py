"""MATH243_KKS_Normal_Distribution_Notes.docx — Lecture 12 + uniform/normal (other distributions pp. 7–10) (L16–L17)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scipy import stats

from common import exam_map, new
from m243 import PROB, g, table_phi

N = stats.norm
L12 = PROB + r"\Lecture 12.pdf"
TP = table_phi


def ph(z):
    return f"{TP(z):.4f}"


n = new("KKS", "The Normal Distribution: Areas, Percentiles, Linear Combinations and Approximations",
        "MATH243_KKS_Normal_Distribution_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "a normal-table question in every paper since 2014-15"),
              ("Lesson 16 — Normal Distribution, Standardising and the z Table", "pdf, properties, areas, finding k, all TF numericals"),
              ("Lesson 17 — Sums of Normals, Sampling Distribution of x̄, Normal Approximation",
               "D = A − B − C, σ/√n, finite population correction, continuity correction"),
              ("Quick Notes — Normal Distribution", "revision bullets")],
    source_note="Page numbers refer to KKS Sir's Lecture 12.pdf (11 pp.) and Lecture on other distributions...pdf "
                "(uniform and normal, pp. 7–10). Table values are read from standardnormaltable.pdf (area to the left "
                "of z, z rounded to two decimals). Sums of independent normals and the sampling distribution of x̄ are "
                "textbook topics (marked). \"TF p.\" = merged question PDF page; \"22 batch p.\" = 2023-24 paper.")

n.h1("Exam Map — What the TF Papers Ask")
st = exam_map(n, "k6")
n.callout("focus", f"{st['n']} questions, {st['marks']} marks. Every paper from 2014-15 on has a normal-table "
          "numerical (11–18 marks): a count out of N, a percentage between two values, or a reverse lookup "
          "(\"replacement interval so that ≤ 10 % fail\", \"slowest 15 %\"). The 2022-23 and 2023-24 papers add theory: "
          "properties of the normal curve and why mean = mode = μ. Practise the four-line routine of Lesson 16 until a "
          "question takes five minutes.")

# ------------------------------------------------------------------ L16
n.lesson("Lesson 16 — Normal Distribution, Standardising and the z Table", "Lec 12 pp. 1–8 · other distributions pp. 7–10")
n.h2("1. Definition (Lec 12 p. 1)")
n.formula(["f(x) = [1/(σ√(2π))] e^{−(x − μ)²/(2σ²)},  −∞ < x < ∞",
           "X ~ N(μ, σ²):  E(X) = μ,  V(X) = σ²"])
n.p("Normal probability law: P(μ − σ < X < μ + σ) = 68.27 %, P(μ − 2σ < X < μ + 2σ) = 95.45 %, "
    "P(μ − 3σ < X < μ + 3σ) = 99.73 %. The normal distribution is also called the Gaussian distribution.")
n.h2("2. Properties of the Normal Curve ★ (textbook; asked 2022-23 Q4(a))")
n.numbered(["Bell-shaped and symmetric about x = μ; mean = median = mode = μ.",
            "The curve is highest at x = μ, where f(μ) = 1/(σ√(2π)).",
            "Points of inflection at x = μ ± σ (concave down between them, up outside).",
            "It approaches the x-axis asymptotically on both sides; total area under the curve is 1.",
            "Determined completely by μ (location) and σ (spread); larger σ → lower, flatter curve.",
            "A linear function a + bX of a normal variable is normal; so is a sum of independent normals.",
            "Mean deviation ≈ (4/5)σ, quartile deviation ≈ (2/3)σ; β_{1} = 0 (symmetric), β_{2} = 3 (mesokurtic)."])
n.h2("3. Mean, Mode and SD of the Normal ★ (textbook; 2022-23 Q4(a), 2023-24 Q4(a))")
n.code(["Mode: maximise f(x). ln f = const − (x − μ)²/(2σ²)",
        "   d/dx ln f = −(x − μ)/σ² = 0  ⟹  x = μ;   d²/dx² ln f = −1/σ² < 0  ⟹ maximum.  Mode = μ.",
        "",
        "Mean: put z = (x − μ)/σ, dx = σ dz:",
        "   E(X) = ∫ (μ + σz) φ(z) dz = μ ∫ φ(z) dz + σ ∫ z φ(z) dz = μ · 1 + σ · 0 = μ",
        "   (∫ z φ(z) dz = 0 because z φ(z) is an odd function)",
        "",
        "Variance: E[(X − μ)²] = σ² ∫ z² φ(z) dz.  By parts with u = z, dv = z e^(−z²/2) dz:",
        "   ∫ z² e^(−z²/2) dz = [−z e^(−z²/2)] + ∫ e^(−z²/2) dz = 0 + √(2π)",
        "   ⟹ ∫ z² φ(z) dz = 1  ⟹  V(X) = σ²,  SD = σ"])
n.h2("4. Standard Normal Variable (Lec 12 pp. 1–2)")
n.formula(["Z = (X − μ)/σ ~ N(0, 1),   φ(z) = (1/√(2π)) e^{−z²/2}", "Φ(z) = P(Z ≤ z) = area to the left of z"])
n.p("E(Z) = (1/σ)[E(X) − μ] = 0 and V(Z) = (1/σ²)V(X) = 1: the standard normal has mean 0 and variance 1, so any "
    "normal probability is read from one table.")
n.figure_from_pdf(L12, 4, "Figure 16.1 — Areas to the right of z = 1.84 and between z = −1.97 and 0.86 (Lec 12 p. 4)",
                  clip=(0.06, 0.24, 0.94, 0.50), width_cm=11)
n.h2("5. Worked Examples (Lec 12 pp. 2–6)")
n.code([f"Right of z = 1.84: 1 − 0.9671 = 0.0329.     Between −1.97 and 0.86: 0.8051 − 0.0244 = 0.7807",
        f"GPA N(2.1, 0.6²), 80 students: P(2.5 < X < 3.5) = P(0.67 < Z < 2.33) = 0.9901 − 0.7486 = 0.2415 → ≈ 19 students",
        f"N(50, 10²): P(45 < X < 62) = P(−0.5 < Z < 1.2) = 0.8849 − 0.3085 = 0.5764",
        f"Ball bearings 3.0 ± 0.01, σ = 0.005: z = ±2, scrapped = 2(0.0228) = 0.0456 → 4.56 %",
        f"N(25, 9): 30 % to the left: z = −0.525 → K = 25 − 0.525(3) = 23.425;  15 % to the right: z = 1.035 → K = 28.105"])
n.callout("note", "The slide reads Φ(0.67) as 0.7480 (that is Φ(0.668)); the table gives 0.7486, so the probability is "
          "0.2415 and the expected number 19.3 ≈ 19 (the slide's 0.2421 × 80 = 19.4 also rounds to 19, not 20).")
n.figure_from_pdf(L12, 6, "Figure 16.2 — Scrapped ball bearings: two tails of 0.0228 beyond z = ±2 (Lec 12 p. 6)",
                  clip=(0.05, 0.50, 0.95, 0.62), width_cm=12)
n.h2("6. Uniform Distribution (other distributions pp. 7–8)")
n.formula(["f(x) = 1/(B − A), A ≤ x ≤ B;   μ = (A + B)/2,  σ² = (B − A)²/12"])
n.p("Conference room, X ~ U[0, 4]: f(x) = 1/4; P(X ≥ 3) = ∫_{3}^{4} (1/4) dx = 1/4.")
n.exam_approach(["Write X ~ N(μ, σ²) with σ (not σ²) ready.",
                 "Standardise every limit: z = (x − μ)/σ, rounded to 2 decimals.",
                 "Area: left Φ(z); right 1 − Φ(z); between Φ(z_{2}) − Φ(z_{1}). Draw a small sketch with the shaded area.",
                 "Count = N × probability (round to a whole number). Reverse question: find z with the given area, then "
                 "x = μ + zσ. Two unknowns: two such equations, solve for μ and σ."])
s_ = 10 / (0.67 + 1.28); m_ = 65 + 1.28 * s_
z60, z74 = (60 - m_) / s_, (74 - m_) / s_
n.practice("Lesson 16",
           "(a) Actual — 2018-19 Q8(a) (TF p. 25). (b) Actual — 2014-15 Q8(c) (TF p. 11). (c) Actual — 2020-21 Q7(b) "
           "(TF p. 38). (d) Actual — 2022-23 Q3(c) (TF p. 48). (e) Actual — 2015-16 Q8(b) (TF p. 16). (f) Actual — "
           "2021-22 Q7(b) (TF p. 45). (g) Actual — 2023-24 Q4(a) (22 batch p. 2). (h) Actual — 2022-23 Q4(a) (TF p. 48).",
           ["(a) A factory installed 1000 tube lights with mean life 120 days, normally distributed with SD 20 days. "
            "(i) How many expire in less than 90 days? (ii) If all are replaced together, what interval should be allowed "
            "between replacements if not more than 10 % should expire before replacement?  (18)",
            "(b) A workshop produces 2000 units per day with mean weight 130 kg and SD 10 kg (normal). How many units "
            "weigh less than 142 kg?  (11)",
            "(c) Mice live on average 40 months with SD 6.3 months (normal). Find P(lives more than 32 months) and "
            "P(between 37 and 49 months).  (18)",
            "(d) A one-way trip takes on average 24 minutes, SD 3.8 minutes (normal). P(trip takes at least half an hour)? "
            "(i) Office opens at 9:00, he leaves at 8:45: what percentage of the time is he late? (ii) Time above which "
            "the slowest 15 % of trips lie. (iii) P(2 of the next 3 trips take at least half an hour).  (13)",
            "(e) Marks are normal; 10 % of students score under 65 and 25 % exceed 75. What percentage score between 60 and 74?  (12)",
            "(f) Ball bearings must be 3.0 ± 0.01 cm; diameters are N(3.0, 0.005²). On average how many are scrapped?  (15)",
            "(g) Show that the mode of the normal distribution equals its mean. Bulb life is N(800, 40²): find P(778 < X < 834).  (11)",
            "(h) Write some properties of the normal curve. Find the mean, mode and SD of a normal random variable and "
            "comment on the mean and variance of the standard normal variable.  (10)"])
n.solution()
n.answer("(a)", "X ~ N(120, 20²).")
n.code(["(i)  z = (90 − 120)/20 = −1.5;  P(X < 90) = Φ(−1.5) = 0.0668",
        "     expected number = 1000 × 0.0668 = 66.8 ≈ 67 tube lights",
        "(ii) want P(X < t) = 0.10 → z = −1.28 (table: Φ(−1.28) = 0.1003)",
        "     t = 120 − 1.28 × 20 = 94.4 days  → replace every 94 days (about 3 months)"])
n.answer("(b)", "")
n.code([f"z = (142 − 130)/10 = 1.2;  P(X < 142) = Φ(1.2) = {ph(1.2)}",
        f"number = 2000 × {ph(1.2)} = {g(2000*TP(1.2),1)} ≈ 1770 units"])
n.answer("(c)", "X ~ N(40, 6.3²).")
n.code([f"z = (32 − 40)/6.3 = −1.27;  P(X > 32) = 1 − Φ(−1.27) = 1 − {ph(-1.27)} = {g(1-TP(-1.27))}",
        f"z₁ = (37 − 40)/6.3 = −0.48, z₂ = (49 − 40)/6.3 = 1.43",
        f"P(37 < X < 49) = Φ(1.43) − Φ(−0.48) = {ph(1.43)} − {ph(-0.48)} = {g(TP(1.43)-TP(-0.48))}"])
pp = 1 - TP(1.58)
n.answer("(d)", "X ~ N(24, 3.8²).")
n.code([f"P(X ≥ 30): z = 6/3.8 = 1.58 → 1 − {ph(1.58)} = {g(pp)}",
        f"(i)   late if the trip takes more than 15 min: z = (15 − 24)/3.8 = −2.37 → P = 1 − {ph(-2.37)} = {g(1-TP(-2.37))} → {g(100*(1-TP(-2.37)),2)} % of the time",
        f"(ii)  slowest 15 %: P(X > t) = 0.15 → Φ(z) = 0.85 → z = 1.04;  t = 24 + 1.04 × 3.8 = {g(24+1.04*3.8,2)} min",
        f"(iii) Y = number of the 3 trips ≥ 30 min ~ Bin(3, {g(pp)}):  P(Y = 2) = 3({g(pp)})²({g(1-pp)}) = {g(3*pp*pp*(1-pp))}"])
n.answer("(e)", "Two unknowns: use both percentages.")
n.code(["P(X < 65) = 0.10 → (65 − μ)/σ = −1.28;     P(X > 75) = 0.25 → (75 − μ)/σ = 0.67",
        f"Subtract: 10/σ = 1.95 → σ = {g(s_)};   μ = 65 + 1.28σ = {g(m_)}",
        f"z(60) = (60 − {g(m_,2)})/{g(s_,3)} = {g(z60,2)};   z(74) = (74 − {g(m_,2)})/{g(s_,3)} = {g(z74,2)}",
        f"P(60 < X < 74) = Φ(0.48) − Φ(−2.26) = {ph(0.48)} − {ph(-2.26)} = {g(TP(0.48)-TP(-2.26))} ≈ 67 %"])
n.answer("(f)", "z = (2.99 − 3.0)/0.005 = −2 and (3.01 − 3.0)/0.005 = 2; P(scrapped) = 2Φ(−2) = 2(0.0228) = 0.0456 → "
         "4.56 % of the bearings (about 46 in every 1000).")
n.answer("(g)", "Mode = μ: the derivative proof of §3. Then X ~ N(800, 40²):")
n.code([f"z₁ = (778 − 800)/40 = −0.55,  z₂ = (834 − 800)/40 = 0.85",
        f"P(778 < X < 834) = Φ(0.85) − Φ(−0.55) = {ph(0.85)} − {ph(-0.55)} = {g(TP(0.85)-TP(-0.55))}"])
n.answer("(h)", "Properties: §2 list (give at least five). Mean, mode, SD: §3 derivations. Comment: Z = (X − μ)/σ has "
         "mean 0 and variance 1 (§4), so every normal variable reduces to N(0, 1), which is why one table serves all "
         "normal distributions.")

# ------------------------------------------------------------------ L17
n.lesson("Lesson 17 — Sums of Normals, Sampling Distribution of x̄, Normal Approximation",
         "Lec 12 pp. 6–11 · linear combinations and x̄: textbook")
n.h2("1. Linear Combinations of Independent Normals (textbook)")
n.formula(["X_{i} ~ N(μ_{i}, σ_{i}²) independent ⟹ Y = Σ a_{i}X_{i} ~ N(Σ a_{i}μ_{i}, Σ a_{i}²σ_{i}²)"])
n.callout("trap", "Variances add even when the variables are subtracted: V(A − B) = V(A) + V(B). Never subtract SDs.")
n.h2("2. Sampling Distribution of the Mean (textbook; Lec 12 p. 8 exercise 7)")
n.formula(["E(x̄) = μ,   σ_{x̄} = σ/√n  (with replacement / infinite population)",
           "Without replacement from N: σ_{x̄} = (σ/√n) √((N − n)/(N − 1))"])
n.p("If the population is normal, x̄ is exactly normal; otherwise it is approximately normal for large n (central limit "
    "theorem). For two independent samples, x̄_{2} − x̄_{1} ~ N(μ_{2} − μ_{1}, σ_{1}²/n_{1} + σ_{2}²/n_{2}).")
sd = math.sqrt(30 ** 2 / 25 + 40 ** 2 / 16)
n.p(f"Lec 12 exercise 7 (old N(5000, 40²), n = 16; improved N(5050, 30²), n = 25): x̄_{{2}} − x̄_{{1}} has mean 50, SD "
    f"√(900/25 + 1600/16) = √136 = {g(sd)}; P(difference ≥ 25) = P(Z ≥ −25/{g(sd,2)}) = P(Z ≥ −2.14) = {ph(2.14)}.")
n.h2("3. Normal Approximation to the Binomial (Lec 12 pp. 6–11)")
n.formula(["X ~ Bin(n, p) ≈ N(np, np(1 − p)) when np ≥ 5 and n(1 − p) ≥ 5",
           "Continuity correction: P(a ≤ X ≤ b) ≈ P(a − 0.5 < Y < b + 0.5)"])
n.code(["Bin(10, 0.5): exact P(2 ≤ X ≤ 4) = 0.3662",
        "  normal μ = 5, σ = √2.5 = 1.581:  P(1.5 < Y < 4.5) = P(−2.21 < Z < −0.32) = 0.3745 − 0.0136 = 0.3609",
        "Pipework failures, n = 20, p = 0.3 (μ = 6, σ = 2.049):",
        "  P(X ≥ 10) ≈ P(Y ≥ 9.5) = P(Z ≥ 1.71) = 0.0436;   P(X ≤ 4) ≈ P(Y ≤ 4.5) = P(Z ≤ −0.73) = 0.2327",
        "  Exactly 5 observed: z = (5 − 6)/2.049 = −0.49, |z| < 1.96 → no evidence against the 30 % rate"])
n.callout("note", "The slide's last line writes P(Z ≤ −0.21) for the left limit; it is z = −2.21 (area 0.0136), as used. "
          "With np = 5 exactly the approximation is borderline, which is why 0.36 differs from 0.3662.")
n.exam_approach(["Write the combination (D = A − B − C, x̄, x̄_{2} − x̄_{1}) and its mean and variance first.",
                 "Standardise with that SD (σ/√n for a mean, with the finite-population factor if sampling without replacement).",
                 "For counts out of many samples, multiply the probability by the number of samples.",
                 "Binomial → normal: check np, nq ≥ 5, apply the ±0.5 correction, then standardise."])
sdD = math.sqrt(0.1 ** 2 + 2 * 0.05 ** 2)
se = 0.048 / 6
fpc = math.sqrt((1500 - 36) / (1500 - 1))
n.practice("Lesson 17", "(a) Actual — 2016-17 Q7(b) (TF p. 21). (b) Actual — 2016-17 Q7(c) (TF p. 21).",
           ["(a) A U-shaped component is formed from parts A, B and C (Figure 17.1). The length of A is N(10, 0.1²) mm; "
            "the thicknesses of B and C are N(2, 0.05²) mm; all independent. (i) Find the mean and SD of the gap D. "
            "(ii) What is the probability that D is less than 5.9 mm?  (10)",
            "(b) The masses of 1500 ball bearings are normal with mean 22.40 g and SD 0.048 g. If 300 random samples of "
            "size 36 are drawn, find the expected mean and SD of the sampling distribution of means for sampling with and "
            "without replacement. How many samples would have means (i) between 22.39 and 22.41 g, (ii) greater than "
            "22.42 g, (iii) less than 22.38 g or more than 22.41 g?  (15)"])
QPDF = r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2\MATH 243\TF questions\MATH 243 All Merged Questions.pdf"
n.figure_from_pdf(QPDF, 21, "Figure 17.1 — The U-shaped component: D = A − B − C (2016-17 Q7(b), TF p. 21)",
                  clip=(0.30, 0.235, 0.72, 0.385), width_cm=6.5)
n.solution()
n.answer("(a)", "D = A − B − C, a linear combination of independent normals.")
n.code(["(i)  E(D) = 10 − 2 − 2 = 6 mm",
        f"     V(D) = 0.1² + 0.05² + 0.05² = 0.01 + 0.0025 + 0.0025 = 0.015;  SD = √0.015 = {g(sdD)} mm",
        f"(ii) z = (5.9 − 6)/{g(sdD)} = {g((5.9-6)/sdD,2)};  P(D < 5.9) = Φ(−0.82) = {ph(-0.82)}"])
n.answer("(b)", "μ_{x̄} = μ = 22.40 g in both cases.")
rows = []
for lab, s_e in (("with replacement", se), ("without replacement", se * fpc)):
    z1, z2 = 0.01 / s_e, 0.02 / s_e
    a = TP(z1) - TP(-z1); b = 1 - TP(z2); c = TP(-z2) + (1 - TP(z1))
    rows.append([lab, g(s_e, 5), g(z1, 2), f"{g(a)} → {g(300*a,1)}", f"{g(b)} → {g(300*b,1)}", f"{g(c)} → {g(300*c,1)}"])
n.code([f"With replacement:    σ_x̄ = 0.048/√36 = {g(se,4)} g",
        f"Without replacement: σ_x̄ = 0.008 × √((1500 − 36)/(1500 − 1)) = 0.008 × {g(fpc)} = {g(se*fpc,5)} g"])
n.table(["Sampling", "σ_{x̄}", "z for ±0.01", "(i) prob → of 300", "(ii) prob → of 300", "(iii) prob → of 300"], rows,
        widths_cm=[3.2, 1.8, 2, 3.4, 3.4, 3.4], font_size=8.5)
n.p("Working (with replacement): (i) z = ±0.01/0.008 = ±1.25, P = Φ(1.25) − Φ(−1.25) = 0.8944 − 0.1056 = 0.7888 → "
    "about 237 samples; (ii) z = 0.02/0.008 = 2.5, P = 1 − 0.9938 = 0.0062 → about 2 samples; (iii) P(x̄ < 22.38) + "
    "P(x̄ > 22.41) = 0.0062 + 0.1056 = 0.1118 → about 34 samples. Without replacement the counts are 238, 2 and 33.")

n.quick_notes("Quick Notes — Normal Distribution", "Revision points for Lessons 16–17.", [
    ("L16 · Normal and z", ["f = e^{−(x−μ)²/2σ²}/(σ√2π); mean = median = mode = μ; inflection μ ± σ; 68.27/95.45/99.73 %.",
                            "Z = (X − μ)/σ ~ N(0, 1); Φ(z) = area left; right = 1 − Φ; between = difference.",
                            "Mode: d/dx ln f = 0 → x = μ. Mean via z, odd integrand; variance by parts → σ².",
                            "Tube lights 67 and 94.4 days; units 1770; mice 0.8980, 0.6080; trip 0.0571, 99.1 %, 27.95 min, 0.0092;",
                            "marks μ = 71.56, σ = 5.13 → 67 %; bearings 4.56 %; bulbs 0.5111."]),
    ("L17 · Combinations and Approximations", ["Σa_{i}X_{i} ~ N(Σa_{i}μ_{i}, Σa_{i}²σ_{i}²): variances always add.",
                                               "σ_{x̄} = σ/√n; × √((N − n)/(N − 1)) without replacement.",
                                               "U-shape: D ~ N(6, 0.1225²), P(D < 5.9) = 0.2061. Bearings: 237, 2, 34.",
                                               "Binomial ≈ normal if np, nq ≥ 5; use ±0.5 continuity correction."])],
    diagrams=[(L12, 6, "Two-tail scrap area (Lec 12 p. 6) — same as Fig. 16.2", (0.05, 0.50, 0.95, 0.62), 11)])
n.save()
print("saved", n.out_path)
