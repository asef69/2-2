"""MATH243_Stat_Dispersion_Notes.docx — deck 3 (L8–L9)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import exam_map, new
from m243 import STAT, Grouped, g, summary

DECK = STAT + r"\3. Measures of Dispersion.pdf"
cl = lambda a, h, k: [(a + i * h, a + (i + 1) * h) for i in range(k)]

n = new("Stat", "Measures of Dispersion: Range, Quartile and Mean Deviation, Variance, SD, CV",
        "MATH243_Stat_Dispersion_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "consistency / uniformity questions in almost every paper"),
              ("Lesson 8 — Range, Quartile Deviation and Mean Deviation", "absolute measures, empirical relations"),
              ("Lesson 9 — Variance, Standard Deviation and Coefficient of Variation", "grouped/ungrouped, CV comparisons, corrections"),
              ("Quick Notes — Dispersion", "revision bullets")],
    source_note="Page numbers refer to 3. Measures of Dispersion.pdf (25 pp.), written as p. n. The slides use divisor N "
                "for the variance (σ² = Σ(x − x̄)²/N); these notes follow them. \"TF p.\" = merged question PDF page; "
                "\"22 batch p.\" = 2023-24 paper.")

n.h1("Exam Map — What the TF Papers Ask")
st = exam_map(n, "s3")
n.callout("focus", f"{st['n']} questions, {st['marks']} marks — a \"which is more consistent / uniform / stable?\" question "
          "in 8 of the 12 papers. The method never changes: mean and SD for each group, CV = σ/x̄ × 100, the smaller CV is "
          "the more consistent. 2023-24 added the \"wrongly copied items\" correction. Master the grouped step-deviation "
          "table first — it is reused for skewness and moments.")

# ------------------------------------------------------------------ L8
n.lesson("Lesson 8 — Range, Quartile Deviation and Mean Deviation", "pp. 1–8, 24–25")
n.p("Dispersion measures how far individual values deviate from the central value. Batsman 1 (49, 50, 55, 54) and batsman 2 "
    "(10, 68, 90, 40) both average 52, but batsman 1 is far more consistent — the mean alone cannot show it (p. 1).")
n.bullets(["**Absolute** measures are in the units of the data (range, QD, MD, variance, SD).",
           "**Relative** measures are ratios to an average, unit-free (coefficient of variation) — used to compare groups."])
n.h2("1. Range (p. 2)")
n.p("R = L − S. Share prices 200–250: R = 250 − 160 = 90 Tk; grouped: upper limit of the last class − lower limit of the "
    "first (60 − 10 = 50). Limitation: depends only on the two extremes (three different series with R = 40).")
n.h2("2. Quartile Deviation (pp. 3–5)")
n.formula("Q.D. = (Q_{3} − Q_{1})/2")
n.p("Profits of 100 companies: Q_{1} = 47.22, Q_{3} = 70 → middle 50 % lie in a range of 22.78 lakhs; Q.D. = 11.39 lakhs. "
    "Limitation: ignores the first and last 25 % of the data.")
n.h2("3. Mean Deviation (pp. 5–8)")
n.formula(["M.D. = Σ|x − x̄|/N  (ungrouped),   Σf|x − x̄|/N  (grouped)"])
n.p("Batsman 1: Σ|x − 52| = 3 + 2 + 3 + 2 = 10 → M.D. = 2.5; batsman 2: 42 + 16 + 38 + 12 = 108 → 27. Sales (3, 6, 11, 3, 2): "
    "x̄ = 33, Σf|x − x̄| = 204 → M.D. = 8.16 lakhs. Marks (6, 5, 8, 15, 7, 6, 3): x̄ = 33.4, Σf|x − x̄| = 659.2 → 13.18. Practice: 6.3. "
    "Limitation: signs are ignored (otherwise the deviations sum to zero).")
n.h2("4. Empirical Relations (pp. 24–25)")
n.formula(["Q.D. = (2/3)σ,   M.D. = (4/5)σ,   Q.D. = (5/6) M.D."])
n.p("Profits (8, 12, 20, 6, 4): σ = 11.14 → M.D. ≈ 0.8 × 11.14 = 8.91. Marks example: M.D. 13.18 → Q.D. ≈ 10.98.")
n.callout("trap", "These relations hold only for (near) normal distributions; compute directly whenever the data are given.")

# ------------------------------------------------------------------ L9
n.lesson("Lesson 9 — Variance, Standard Deviation and Coefficient of Variation", "pp. 9–23")
n.formula(["σ² = Σ(x − x̄)²/N = Σx²/N − x̄²",
           "Grouped: σ² = [Σfd²/N − (Σfd/N)²] × h²,   σ = √σ²",
           "C.V. = (σ/x̄) × 100 %"])
G = Grouped(cl(10, 10, 5), [8, 12, 20, 6, 4], A=35)
n.table(G.headers(2, name="Profit"), G.rows(2), widths_cm=[2.6, 2.2, 2, 3.6, 3.2, 3.6])
n.p(f"σ² = [66/50 − (−14/50)²] × 10² = 1.2416 × 100 = {g(G.var,2)}; σ = {g(G.sd,3)}; x̄ = 35 + (−14/50)10 = 32.2; "
    f"C.V. = {g(G.cv,2)} % (pp. 10, 13, 20). Weekly wages of 10 workers: Σ(x − 1323)² = 622 → σ² = 62.2, σ = 7.89 (pp. 9, 12). "
    "Rejects (boundaries 20.5–55.5, f 5, 15, 28, 42, 15, 12, 3): x̄ = 36.96, σ = 6.74, C.V. = 18.2 % (pp. 15, 22).")
n.h2("1. Coverage of x̄ ± kσ (pp. 16–17)")
n.p("For a near-normal distribution x̄ ± σ covers 68.27 %, x̄ ± 2σ 95.45 %, x̄ ± 3σ 99.73 % of the observations. Breaking "
    "strength (f 3, 24, 27, 21, 5): x̄ = 49.025, σ = 1.96 → x̄ ± 2σ = 45.1 to 52.95 ≈ 45 to 53, containing about 76 of the 80 "
    "pieces (95 %).")
n.h2("2. Coefficient of Variation (pp. 17–23)")
n.p("C.V. compares variability of data with different units or different means: height (40 in, sd 5) C.V. 12.5 % vs weight "
    "(10 kg, sd 2) 20 % → weight varies more; systolic 11.5 % vs diastolic 13.3 %. Share prices: Dhaka σ = 8.33, x̄ = 115, "
    "C.V. 7.24 %; Chittagong σ = 10.09, x̄ = 119, C.V. 8.48 % → Dhaka is safer.")
n.callout("memorize", "Smaller C.V. → more consistent / uniform / stable. Higher mean → better average (better scorer, "
          "longer life). If both differ, state each conclusion separately.")
n.h2("3. Correcting Wrong Items (textbook; asked 2023-24 Q5(c))")
n.formula(["Correct Σx = N x̄ − (wrong values) + (right values)",
           "Correct Σx² = N(σ² + x̄²) − Σ(wrong)² + Σ(right)²"])
n.exam_approach(["Grouped: mid-values, A (middle mid-value), d = (x − A)/h, columns f, fd, fd²; totals.",
                 "x̄ = A + (Σfd/N)h; σ = h√(Σfd²/N − (Σfd/N)²); C.V. = σ/x̄ × 100.",
                 "Ungrouped: x̄, then Σ(x − x̄)² in a table (or Σx² − N x̄²); σ with divisor N.",
                 "Conclude in a sentence for each part of the question."])

# ---- practice
A_t, B_t = summary([130, 124, 119, 134, 142, 130, 141]), summary([132, 144, 136, 143, 132, 133, 140])
X_m, Y_m = summary([58, 59, 60, 54, 65, 66, 52, 75, 69, 52]), summary([87, 89, 78, 71, 73, 84, 65, 66, 56, 46])
fa, fb = Grouped(cl(0, 2, 6), [5, 16, 13, 7, 5, 4], A=7), Grouped(cl(0, 2, 6), [2, 7, 12, 19, 9, 1], A=7)
wa, wb = Grouped(cl(20, 10, 7), [15, 30, 44, 60, 30, 14, 7], A=55), Grouped(cl(20, 10, 7), [25, 40, 60, 35, 20, 15, 5], A=55)
ba, bb = Grouped(cl(1700, 200, 5), [10, 16, 20, 8, 6], A=2200), Grouped(cl(1700, 200, 5), [3, 40, 12, 3, 2], A=2200)
pc = Grouped(cl(20, 10, 8), [4, 8, 18, 30, 15, 10, 8, 7], A=65)
n.practice("Lesson 9",
           "(a) Actual — 2023-24 Q5(c) (22 batch p. 3). (b) Actual — 2022-23 Q5(c) (TF p. 49). (c) Actual — 2020-21 Q5(a) "
           "(TF p. 37). (d) Actual — 2019-20 Q5(a) (TF p. 34). (e) Actual — 2018-19 Q5(a) (TF p. 24). (f) Actual — 2015-16 "
           "Q6(b) (TF p. 15). (g) Actual — 2013-14 Q6(a) (TF p. 7). (h) Actual — 2011-12 Q6(b) (TF p. 2).",
           ["(a) The mean and SD of 200 items are 60 and 20. Two items were wrongly taken as 3 and 67 instead of 13 and 17. "
            "Find the correct mean, SD and coefficient of variation.  (12)",
            "(b) Bulb lives (hours) — Company A: 1700–1900: 10, 1900–2100: 16, 2100–2300: 20, 2300–2500: 8, 2500–2700: 6; "
            "Company B: 3, 40, 12, 3, 2. If prices are the same, which company's bulbs would you prefer? Justify.  (10)",
            "(c) Daily wages 20–30 … 80–90: Factory A 15, 30, 44, 60, 30, 14, 7; Factory B 25, 40, 60, 35, 20, 15, 5. Which "
            "factory pays higher average wages? Which has greater variability?  (10)",
            "(d) Coefficient of variation of profits 20–30 … 90–100 (f 4, 8, 18, 30, 15, 10, 8, 7).  (10)",
            "(e) Shares A, B, C: average price 18, 22.50, 24; SD 5.40, 4.50, 6.00; current price 36, 34.75, 39. (i) Which share "
            "is more stable? (ii) Holding all three, which would you dispose of now and why?  (15)",
            "(f) Marks in 10 weeks — X: 58, 59, 60, 54, 65, 66, 52, 75, 69, 52; Y: 87, 89, 78, 71, 73, 84, 65, 66, 56, 46. "
            "(i) Who is the better scorer? (ii) Who is more consistent?  (17)",
            "(g) Lives of refrigerators (years) 0–2 … 10–12 — Model A: 5, 16, 13, 7, 5, 4; Model B: 2, 7, 12, 19, 9, 1. "
            "Which model has greater uniformity?  (15)",
            "(h) Times (min) of 7 workers — A: 130, 124, 119, 134, 142, 130, 141; B: 132, 144, 136, 143, 132, 133, 140. Which "
            "sample is more variable and which takes less time on average?  (15)"])
n.solution()
S1 = 200 * 60 - 70 + 30
S2 = 200 * (400 + 3600) - (9 + 4489) + (169 + 289)
cm, cs = S1 / 200, math.sqrt(S2 / 200 - (S1 / 200) ** 2)
n.answer("(a)", "")
n.code(["Wrong Σx = 200 × 60 = 12000;  correct Σx = 12000 − (3 + 67) + (13 + 17) = 11960  →  x̄ = 11960/200 = 59.8",
        "Wrong Σx² = N(σ² + x̄²) = 200(400 + 3600) = 800000",
        "Correct Σx² = 800000 − (3² + 67²) + (13² + 17²) = 800000 − 4498 + 458 = 795960",
        f"σ² = 795960/200 − 59.8² = 3979.8 − 3576.04 = {g(S2/200-cm**2,2)}  →  σ = {g(cs,3)}",
        f"C.V. = {g(cs,3)}/59.8 × 100 = {g(cs/cm*100,2)} %"])


def two(n_, ga, gb, nm, unit=""):
    for lab, G_ in (("A", ga), ("B", gb)):
        n_.table(G_.headers(2, name=nm) , G_.rows(2), widths_cm=[3, 2.4, 2, 3.4, 3, 3.4], font_size=8.5)
        n_.p(f"{lab}: x̄ = {g(G_.A)} + ({g(G_.s[1])}/{G_.N}) × {g(G_.h)} = {g(G_.mean,3)}{unit};  σ = {g(G_.h)} × "
             f"√({g(G_.s[2])}/{G_.N} − ({g(G_.s[1])}/{G_.N})²) = {g(G_.sd,3)};  C.V. = {g(G_.cv,2)} %")


n.answer("(b)", "")
two(n, ba, bb, "Life (h)", " h")
n.p(f"A lasts longer on average ({g(ba.mean,1)} h vs {g(bb.mean,1)} h) but B is more uniform (C.V. {g(bb.cv,2)} % vs "
    f"{g(ba.cv,2)} %). At the same price prefer **A** for the longer average life; prefer B only if dependable, uniform life "
    "matters more than average life.")
n.answer("(c)", "")
two(n, wa, wb, "Wages")
n.p(f"(i) Factory A pays the higher average wage ({g(wa.mean,2)} vs {g(wb.mean,2)}). (ii) Absolute variability: σ_A = "
    f"{g(wa.sd,2)}, σ_B = {g(wb.sd,2)}; relative: C.V._A = {g(wa.cv,2)} % < C.V._B = {g(wb.cv,2)} % → Factory B has greater "
    "variability in wages.")
n.answer("(d)", "")
n.table(pc.headers(2, name="Profits"), pc.rows(2), widths_cm=[3, 2.4, 2, 3.4, 3, 3.4], font_size=8.5)
n.p(f"x̄ = 65 + (−59/100)10 = {g(pc.mean,2)};  σ = 10√(343/100 − 0.59²) = {g(pc.sd,3)};  C.V. = {g(pc.cv,2)} %.")
n.answer("(e)", "C.V. = SD/average × 100: A = 5.40/18 × 100 = 30 %; B = 4.50/22.50 × 100 = 20 %; C = 6/24 × 100 = 25 %.")
n.p("(i) B has the smallest C.V., so its price is the most stable. (ii) Compare the current price with the average: A is "
    "36/18 = 2.00 times its average, B 34.75/22.5 = 1.54, C 39/24 = 1.63. Share A is far above its average and also the "
    "least stable, so it is the one to sell now (its price is likely to fall back); keep B.")
n.answer("(f)", "")
n.code([f"X: Σx = 610, x̄ = 61.0, Σ(x − x̄)² = {g(X_m['ss'])}, σ = √({g(X_m['ss'])}/10) = {g(X_m['sd'],3)}, C.V. = {g(X_m['cv'],2)} %",
        f"Y: Σx = 715, x̄ = 71.5, Σ(x − x̄)² = {g(Y_m['ss'])}, σ = √({g(Y_m['ss'])}/10) = {g(Y_m['sd'],3)}, C.V. = {g(Y_m['cv'],2)} %"])
n.p("(i) Y is the better scorer (higher mean 71.5). (ii) X is more consistent (smaller C.V. 11.89 % < 18.29 %).")
n.answer("(g)", "")
two(n, fa, fb, "Life (yr)", " yr")
n.p(f"C.V._B = {g(fb.cv,2)} % < C.V._A = {g(fa.cv,2)} % → Model B has greater uniformity (and also a longer mean life).")
n.answer("(h)", "")
n.code([f"A: x̄ = 920/7 = {g(A_t['mean'],3)}, Σ(x − x̄)² = {g(A_t['ss'],3)}, σ = {g(A_t['sd'],3)}, C.V. = {g(A_t['cv'],2)} %",
        f"B: x̄ = 960/7 = {g(B_t['mean'],3)}, Σ(x − x̄)² = {g(B_t['ss'],3)}, σ = {g(B_t['sd'],3)}, C.V. = {g(B_t['cv'],2)} %"])
n.p("Sample A is more variable (C.V. 5.92 % > 3.50 %) and takes less time on average (131.4 < 137.1 minutes).")

n.quick_notes("Quick Notes — Dispersion", "Revision points for Lessons 8–9.", [
    ("L8 · Range, QD, MD", ["R = L − S; Q.D. = (Q3 − Q1)/2 (profits 11.39); M.D. = Σf|x − x̄|/N.",
                            "Empirical: Q.D. = 2σ/3, M.D. = 4σ/5, Q.D. = 5 M.D./6."]),
    ("L9 · SD and CV", ["σ = h√(Σfd²/N − (Σfd/N)²) (divisor N); C.V. = σ/x̄ × 100; smaller C.V. = more consistent.",
                        "Corrections: fix Σx and Σx² then recompute (59.8, 20.09, 33.6 %).",
                        "Bulbs: A mean 2146.7 C.V. 11.0 %, B 2070 C.V. 7.65 %. Wages: A higher mean, B more variable.",
                        "Shares: CV 30/20/25 % → B stable, sell A. Fridges: B more uniform. Marks: Y better, X consistent."])])
n.save()
print("saved", n.out_path)
