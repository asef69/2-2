"""MATH243_KKS_ANOVA_Notes.docx — 8. Lecture-12-ANOVA (KKS Sir's part) (L18–L19)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy import stats

from common import exam_map, new
from m243 import anova1, anova2, g

n = new("KKS", "Analysis of Variance: F-test for Two Variances, One-way and Two-way ANOVA",
        "MATH243_KKS_ANOVA_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "an ANOVA question in every paper since 2021-22"),
              ("Lesson 18 — F-test for Two Variances and One-way ANOVA", "assumptions, CT/ST/SB/SW, table, pairwise t"),
              ("Lesson 19 — Two-way ANOVA (One Observation per Cell)", "blocks × treatments (textbook)"),
              ("Quick Notes — ANOVA", "revision bullets")],
    source_note="Page numbers refer to 8. Lecture- 12- ANOVA(KKS Sir_s Part).pdf (10 pp.), written as ANOVA p. n. "
                "Critical values come from 8.1 F-Distribution-Table.pdf and 8.2 t-table.pdf. Two-way ANOVA (asked "
                "2022-23 Q8(c)) is not on the slides; Lesson 19 teaches it from the textbook (marked). \"TF p.\" = merged "
                "question PDF page; \"22 batch p.\" = 2023-24 paper.")

n.h1("Exam Map — What the TF Papers Ask")
st = exam_map(n, "k7")
n.callout("focus", f"{st['n']} questions, {st['marks']} marks, all since 2021-22: one-way ANOVA (18–20 marks) in "
          "three consecutive papers, plus a two-way ANOVA in 2022-23. The computation is mechanical — G, CT, ST, SB, "
          "SW, the ANOVA table, compare F with the table value. Practise it until it takes ten minutes, and memorise "
          "the two-way extension.")

# ------------------------------------------------------------------ L18
n.lesson("Lesson 18 — F-test for Two Variances and One-way ANOVA", "ANOVA pp. 1–10")
n.h2("1. Comparing Two Population Variances (ANOVA pp. 1–3)")
n.p("Assumptions: independent samples; normal populations; random sampling; quantitative (interval/ratio) data; "
    "under H_{0} the variances are equal.")
n.formula(["H_{0}: σ_{1}² = σ_{2}²;   F = S_{1}²/S_{2}² (larger sample variance on top)",
           "Reject H_{0} if F ≥ F_{α, (n1−1), (n2−1)} (one-tailed) or F_{α/2, …} (two-tailed)"])
n.p("Lammers Limos: U.S. 25 (n = 7) x̄ = 58.29, s = 8.9947; I-75 (n = 8) x̄ = 59.00, s = 4.3753. F = 8.9947²/4.3753² = "
    "4.23 > F_{0.05, 6, 7} = 3.87 (two-tailed at α = 0.10) → reject H_{0}: the variation in driving time differs.")
ex = [([52, 55, 50, 54, 53, 56, 51, 57], [48, 49, 47, 50, 46, 51, 45, 49, 48, 47], "two-tailed α = 0.05"),
      ([102, 110, 98, 115, 95, 108, 112], [100, 101, 99, 98, 102, 100, 101, 99, 100], "H1: σ_A² > σ_B², α = 0.05"),
      ([23, 28, 22, 29, 24, 30, 21, 27], [25, 26, 24, 25, 26, 25], "H1: σ_B² > σ_A² (A more consistent), α = 0.05")]
rows = []
for a, b, h in ex:
    va, vb = stats.tvar(a), stats.tvar(b)
    big, small, d1, d2 = (va, vb, len(a) - 1, len(b) - 1) if va >= vb else (vb, va, len(b) - 1, len(a) - 1)
    alpha = 0.025 if "two" in h else 0.05
    fc = stats.f.ppf(1 - alpha, d1, d2)
    rows.append([h, f"{g(va)} / {g(vb)}", f"{g(big/small)}", f"F({d1},{d2}) = {g(fc,2)}", "reject H0" if big / small > fc else "do not reject"])
n.h3("Exercises (ANOVA pp. 3–4) — answers (s² with divisor n − 1)")
n.table(["Exercise", "s² (first / second)", "F", "Critical", "Decision"], rows, widths_cm=[5.2, 3.2, 2, 3.4, 3.4], font_size=8.5)
n.h2("2. One-way ANOVA (ANOVA pp. 4–6)")
n.p("k independent samples from k normal populations with a common variance σ². H_{0}: μ_{1} = … = μ_{k}; H_{1}: at least "
    "two means differ.")
n.formula(["G = ΣΣ x_{ij},  N = Σ n_{i},  CT = G²/N",
           "ST = ΣΣ x_{ij}² − CT,  SB = Σ T_{i}²/n_{i} − CT,  SW = ST − SB",
           "F = [SB/(k − 1)] / [SW/(N − k)] ~ F_{(k−1), (N−k)}"])
n.code(["Source      SS     d.f.     MS              F",
        "Between     SB     k − 1    MSB = SB/(k−1)   MSB/MSW",
        "Within      SW     N − k    MSW = SW/(N−k)",
        "Total       ST     N − 1"])
r = anova1([[72, 75, 78, 74, 76], [65, 68, 70, 72, 69], [78, 82, 85, 88, 90]])
n.h3("Reactor example (ANOVA pp. 6–9)")
n.code([f"T = 375, 344, 423; means 75, 68.8, 84.6; G = 1142; N = 15; CT = 1142²/15 = {g(r['CT'],2)}",
        f"SB = 375²/5 + 344²/5 + 423²/5 − CT = {g(r['SB'],2)}",
        f"Σx² = {g(r['sumsq'])};  ST = {g(r['ST'],2)};  SW = {g(r['SW'],2)}",
        f"F = ({g(r['SB'],2)}/2)/({g(r['SW'],2)}/12) = {g(r['MSB'],2)}/{g(r['MSW'],2)} = {g(r['F'],2)}  >  F0.05,2,12 = 3.89 → reject H0"])
n.callout("note", "The slide gives Σx² = 87713, ST = 768.73, SW = 135.20 and F = 28.10. Adding the 15 squares gives "
          "87716, so ST = 771.73, SW = 138.00, MSE = 11.5 and F = 27.55. The decision does not change. Its pairwise "
          "t values (2.91, 4.51, 7.42) use MSE = 11.27; with 11.5 they are 2.89, 4.48, 7.37 — all still > 2.179.")
n.h2("3. Pairwise Comparisons (ANOVA pp. 8–9)")
n.formula(["t = |x̄_{i} − x̄_{j}| / √(MSE (1/n_{i} + 1/n_{j})),   MSE = SW/(N − k)",
           "Reject μ_{i} = μ_{j} if |t| ≥ t_{α/2, N−k}"])
n.exam_approach(["State H0, H1 and α. Compute T_{i}, n_{i}, G, N, CT.",
                 "ST from Σx² (code the data, e.g. divide by 100, if numbers are large — F does not change).",
                 "SB from Σ T_{i}²/n_{i}; SW = ST − SB; build the ANOVA table with d.f. and mean squares.",
                 "F = MSB/MSW; compare with F_{α,(k−1),(N−k)}; conclude in words. Pairwise t only if H0 is rejected."])
q1 = anova1([[300, 400, 300, 500, 0], [600, 300, 300, 400], [700, 300, 400, 600, 500]])
q2 = anova1([[20, 19, 21], [25, 23, 21], [24, 20, 22], [23, 20, 20]])
q3 = anova1([[15, 18, 23, 24], [23, 19, 18, 24], [19, 16, 22, 31]])


def tab(a):
    return [["Between", g(a["SB"], 2), str(a["df1"]), g(a["MSB"], 2), g(a["F"], 3)],
            ["Within", g(a["SW"], 2), str(a["df2"]), g(a["MSW"], 2), ""],
            ["Total", g(a["ST"], 2), str(a["N"] - 1), "", ""]]


n.practice("Lesson 18", "(a) Actual — 2021-22 Q8(b) (TF p. 45). (b) Actual — 2022-23 Q8(b) (TF p. 51). "
           "(c) Actual — 2023-24 Q8(b) (22 batch p. 4).",
           ["(a) Salesmen A, B, C: weekly sales (Tk thousand) A: 300, 400, 300, 500, 0; B: 600, 300, 300, 400; "
            "C: 700, 300, 400, 600, 500. Test whether the average sales differ (F_{(2, 11)} at 5 % = 3.98).  (18)",
            "(b) Lifetimes of four brands of bulbs: A 20, 19, 21; B 25, 23, 21; C 24, 20, 22; D 23, 20, 20. Test at 5 % and "
            "1 % whether the mean lifetimes differ.  (10)",
            "(c) Retail prices (Tk) of a commodity in shops of three big cities: A 15, 18, 23, 24; B 23, 19, 18, 24; "
            "C 19, 16, 22, 31. Carry out the analysis of variance to decide whether prices differ between the cities. Do the average prices differ? (F_{0.05}(2, 9) = 4.26)  (20)"])
n.solution()
n.answer("(a)", "Code x/100: A 3, 4, 3, 5, 0 (T = 15); B 6, 3, 3, 4 (T = 16); C 7, 3, 4, 6, 5 (T = 25); N = 14, G = 56.")
n.code(["CT = 56²/14 = 224;  Σx² = 59 + 70 + 135 = 264;  ST = 264 − 224 = 40",
        "SB = 15²/5 + 16²/4 + 25²/5 − 224 = 45 + 64 + 125 − 224 = 10;  SW = 40 − 10 = 30",
        "(in original units multiply sums of squares by 100² = 10,000: SB = 100,000, SW = 300,000)"])
n.table(["Source", "SS (Tk thousand²)", "d.f.", "MS", "F"], tab(q1), widths_cm=[3, 4, 2, 4, 4.2])
n.p(f"F = {g(q1['F'],3)} < F_{{0.05}}(2, 11) = 3.98 → do not reject H_{{0}}: no significant difference in average sales.")
n.answer("(b)", "T = 60, 69, 66, 63; G = 258, N = 12, CT = 258²/12 = 5547; Σx² = 5586.")
n.table(["Source", "SS", "d.f.", "MS", "F"], tab(q2), widths_cm=[3, 4, 2, 4, 4.2])
n.p(f"F = {g(q2['F'],3)} < F_{{0.05}}(3, 8) = 4.07 and < F_{{0.01}}(3, 8) = 7.59 → the mean lifetimes do not differ "
    "significantly at either level.")
n.answer("(c)", "T = 80, 84, 88; G = 252, N = 12, CT = 5292; Σx² = 5506.")
n.table(["Source", "SS", "d.f.", "MS", "F"], tab(q3), widths_cm=[3, 4, 2, 4, 4.2])
n.p(f"F = {g(q3['F'],3)} < 4.26 → do not reject H_{{0}}; the average prices in the three cities are the same.")

# ------------------------------------------------------------------ L19
a2 = anova2([[12, 15, 10, 14], [15, 19, 12, 11], [14, 18, 15, 12], [11, 16, 12, 16], [16, 17, 11, 14]])
n.lesson("Lesson 19 — Two-way ANOVA (One Observation per Cell)", "textbook — asked 2022-23 Q8(c)")
n.p("r blocks (rows) × c treatments (columns), one observation per cell. Two hypotheses: no block effect and no "
    "treatment effect.")
n.formula(["CT = G²/N,  ST = Σx² − CT,  SR = ΣR_{i}²/c − CT,  SC = ΣC_{j}²/r − CT,  SE = ST − SR − SC",
           "F_{rows} = [SR/(r − 1)]/[SE/((r − 1)(c − 1))],  F_{cols} = [SC/(c − 1)]/[SE/((r − 1)(c − 1))]"])
n.exam_approach(["Row totals R_{i}, column totals C_{j}, grand total G, N = rc.",
                 "CT, ST, SR, SC, SE as above; d.f. r − 1, c − 1, (r − 1)(c − 1), N − 1.",
                 "Two F ratios, each against F_{α} with its own numerator d.f. and the error d.f.; conclude for blocks and for treatments."])
n.practice("Lesson 19", "Actual — 2022-23 Q8(c) (TF p. 51).",
           ["Yields of four types of corn I–IV in five blocks A–E: A 12, 15, 10, 14; B 15, 19, 12, 11; C 14, 18, 15, 12; "
            "D 11, 16, 12, 16; E 16, 17, 11, 14. Test at 5 % whether there are differences due to blocks and due to corn "
            "types.  (15)"])
n.solution()
n.code([f"Block totals R: 51, 57, 59, 55, 58;  corn totals C: 68, 85, 60, 67;  G = 280, N = 20, CT = 280²/20 = 3920",
        f"Σx² = {g(a2['sumsq'])} → ST = {g(a2['ST'],2)}",
        f"SR = (51² + 57² + 59² + 55² + 58²)/4 − 3920 = {g(a2['SR'],2)}",
        f"SC = (68² + 85² + 60² + 67²)/5 − 3920 = {g(a2['SC'],2)}",
        f"SE = {g(a2['ST'],2)} − {g(a2['SR'],2)} − {g(a2['SC'],2)} = {g(a2['SE'],2)}"])
n.table(["Source", "SS", "d.f.", "MS", "F", "F_{0.05}"],
        [["Blocks", g(a2["SR"], 2), "4", g(a2["MSR"], 3), g(a2["FR"], 3), g(a2["FR05"], 2)],
         ["Corn types", g(a2["SC"], 2), "3", g(a2["MSC"], 3), g(a2["FC"], 3), g(a2["FC05"], 2)],
         ["Error", g(a2["SE"], 2), "12", g(a2["MSE"], 3), "", ""],
         ["Total", g(a2["ST"], 2), "19", "", "", ""]], widths_cm=[3, 2.6, 1.6, 2.8, 2.8, 2.6])
n.p("Blocks: F = 0.65 < 3.26 → no significant block difference. Corn types: F = 5.83 > 3.49 → the corn types differ "
    "significantly at 5 %.")

n.quick_notes("Quick Notes — ANOVA", "Revision points for Lessons 18–19.", [
    ("L18 · F-test and One-way", ["F = larger s²/smaller s²; two-tailed uses α/2. Limos 4.23 > 3.87.",
                                  "CT = G²/N; ST = Σx² − CT; SB = ΣT²/n − CT; SW = ST − SB; F = MSB/MSW.",
                                  "Reactor F = 27.55 (slide 28.10 from a Σx² slip). Salesmen 1.83 < 3.98; bulbs 1.67 < 4.07; cities 0.17 < 4.26.",
                                  "Pairwise t = |x̄_i − x̄_j|/√(MSE(1/n_i + 1/n_j)) vs t_{α/2, N−k}."]),
    ("L19 · Two-way", ["SR = ΣR²/c − CT, SC = ΣC²/r − CT, SE = ST − SR − SC; error d.f. (r − 1)(c − 1).",
                       "Corn: blocks F = 0.65 (n.s.), types F = 5.83 > 3.49 (significant)."])])
n.save()
print("saved", n.out_path)
