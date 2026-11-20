"""MATH243_Stat_Central_Tendency_Notes.docx — deck 2 (L5–L7)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import exam_map, new
from m243 import STAT, Grouped, g

DECK = STAT + r"\2. Central Tendency.pdf"
cl = lambda a, h, k: [(a + i * h, a + (i + 1) * h) for i in range(k)]

n = new("Stat", "Measures of Central Tendency: Mean, Median, Quartiles, Mode", "MATH243_Stat_Central_Tendency_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "missing frequencies and graphical median"),
              ("Lesson 5 — Arithmetic, Geometric and Harmonic Means", "direct and short-cut (step-deviation) method"),
              ("Lesson 6 — Median, Quartiles, Deciles, Percentiles and the Ogive", "positional averages, graphical median"),
              ("Lesson 7 — Mode, Empirical Relation and Missing Frequencies", "Δ formula, Mode = 3Md − 2Mean, two unknown frequencies"),
              ("Quick Notes — Central Tendency", "revision bullets")],
    source_note="Page numbers refer to 2. Central Tendency.pdf (26 pp.), written as p. n. \"TF p.\" = merged question PDF "
                "page. Mean, median and mode of grouped data are also needed inside every skewness question (Skewness, "
                "Moments and Kurtosis note).")

n.h1("Exam Map — What the TF Papers Ask")
st = exam_map(n, "s2")
n.callout("focus", f"{st['n']} direct questions ({st['marks']} marks), but grouped mean/median/mode appear inside every "
          "skewness and CV question too, so this deck supports about a third of the Statistics marks. The \"missing "
          "frequencies from the median\" problem was asked in 2014-15 and 2015-16 with the same table; the ogive-median "
          "problem in 2021-22. Know the median and mode formulas by heart.")

# ------------------------------------------------------------------ L5
n.lesson("Lesson 5 — Arithmetic, Geometric and Harmonic Means", "pp. 1–6, 22")
n.p("A measure of central tendency is a single value around which the data tend to cluster; it represents the whole "
    "data and makes comparison easy. Types: arithmetic mean, median, mode, geometric mean, harmonic mean (p. 1).")
n.formula(["Ungrouped: x̄ = Σx_{i}/N;   frequency distribution: x̄ = Σf_{i}x_{i}/N",
           "Short-cut: x̄ = A + (Σf_{i}d_{i}/N) × h,  d_{i} = (x_{i} − A)/h"])
n.p("A = assumed mean (the middle mid-value), h = class width, x_{i} = mid-values, N = Σf.")
G = Grouped(cl(0, 20, 7), [4, 26, 22, 10, 9, 6, 3], A=70)
n.table(G.headers(1, name="Marks"), G.rows(1), widths_cm=[3, 2.4, 2.4, 4, 5.4])
n.p(f"Marks of 80 students (p. 4): x̄ = 70 + (−56/80) × 20 = {g(G.mean)}. Other slide examples: incomes of 10 employees "
    "Σ = 44,940 → Tk 4494; discrete table → 320/25 = 12.8; 0–50 table → 25 + (−2/50)10 = 24.6; heights (boundaries "
    "129.5–164.5) → 147 + (−33/100)5 = 145.35; practice answers 69.18 and 51.75.")
n.formula(["G.M. = antilog(Σf log x / N);   H.M. = N / Σ(f/x)"])
n.callout("trap", "With limits like 130–134, 135–139 use boundaries 129.5–134.5 … for the median/mode L and h, but the "
          "mid-values (132, 137, …) are the same either way.")

# ------------------------------------------------------------------ L6
n.lesson("Lesson 6 — Median, Quartiles, Deciles, Percentiles and the Ogive", "pp. 7–18")
n.h2("1. Median (pp. 7–13)")
n.p("Ungrouped: arrange in order; N odd → ((N + 1)/2)-th value; N even → mean of the (N/2)-th and (N/2 + 1)-th values "
    "(weights 39 … 61 → 44; ten mothers → (43 + 44)/2 = 43.5).")
n.formula("Median = L + [(N/2 − p.c.f.)/f] × h")
n.p("L = lower boundary of the median class (where the (N/2)-th value lies), p.c.f. = cumulative frequency before it, "
    "f = its frequency, h = width.")
n.figure_from_pdf(DECK, 9, "Figure 6.1 — Locating the median class (75th value) and applying the formula (p. 9)",
                  clip=(0.03, 0.05, 0.97, 0.88), width_cm=10)
n.p("Slide answers: weights 54.44; overtime 20 + (50 − 31)/35 × 5 = 22.71 hrs (50 % work up to 22.71 hrs); profits "
    "30 + (62.5 − 40)/36 × 10 = 36.25 crore; heights 144.5 + (50 − 48)/24 × 5 = 144.92; days absent 10 + (327.5 − 224)/241 "
    "× 5 = 12.15; practice 49.09 and 47.58.")
n.callout("note", "The profit example (p. 11) prints 36.5; the formula gives 30 + 22.5/36 × 10 = 36.25 crore.")
n.h2("2. Quartiles, Deciles, Percentiles (pp. 15–18)")
n.formula(["Q_{i} = L + [(iN/4 − p.c.f.)/f] h,  D_{i}: iN/10,  P_{i}: iN/100"])
n.p("Profits of 100 companies: Q_{1} = 40 + (25 − 12)/18 × 10 = 47.22; Q_{2} = 50 + (50 − 30)/30 × 10 = 56.67; "
    "Q_{3} = 60 + (75 − 60)/15 × 10 = 70 lakhs (25 % earn 47.22 lakhs or less). Overtime Q_{1} = 18.5.")
n.h2("3. Graphical Median from the Ogive (textbook; asked 2021-22 Q5(a))")
n.p("Draw the less-than ogive (upper boundary, cumulative frequency). Mark N/2 on the y-axis, go horizontally to the curve "
    "and drop to the x-axis: that x is the median. (Drawing both less-than and more-than ogives, they cross at the median.)")
n.exam_approach(["Cumulative frequency column; position N/2 (or iN/4); locate the class.",
                 "Substitute L, p.c.f., f, h in the formula; one line of arithmetic.",
                 "Interpret: \"50 % of … are below …\"."])
Gw = Grouped([(1900, 1950), (1950, 2000), (2000, 2050), (2050, 2100), (2100, 2150), (2150, 2200), (2200, 2400)],
             [6, 10, 22, 30, 16, 12, 15], h=50)
cf = Gw.cum()
med = 2050 + (Gw.N / 2 - 38) / 30 * 50
n.practice("Lesson 6", "(a) Actual — 2021-22 Q5(a) (TF p. 44).",
           ["(a) Monthly wages of workers: 1900–1950: 6, 1950–2000: 10, 2000–2050: 22, 2050–2100: 30, 2100–2150: 16, "
            "2150–2200: 12, 2200–2400: 15. Draw a suitable diagram, read the median from the graph and verify it by "
            "formula. How many workers earned monthly wages between 2000 and 2170 Tk?  (18)"])
n.solution()
n.table(["Wages", "f", "Less than", "c.f."],
        [[f"{a}–{b}", str(f), str(b), str(c)] for (a, b), f, c in zip(Gw.classes, Gw.f, cf)], widths_cm=[4, 3, 4, 3])
n.p("Suitable diagram: the less-than ogive — plot (1900, 0), (1950, 6), (2000, 16), (2050, 38), (2100, 68), (2150, 84), "
    "(2200, 96), (2400, 111) and join. (The last class is wider, which an ogive handles without adjustment; a histogram "
    "would need height 15/4 per 50 Tk.)")
n.code([f"N = {Gw.N}; N/2 = {Gw.N/2} → on the ogive, across from 55.5 the curve is at about Tk 2079.",
        f"Formula: median class 2050–2100 (c.f. 38 → 68):",
        f"Median = 2050 + (55.5 − 38)/30 × 50 = 2050 + 29.17 = {g(med,2)} Tk",
        "Between 2000 and 2170: 22 + 30 + 16 + (2170 − 2150)/50 × 12 = 68 + 4.8 = 72.8 ≈ 73 workers",
        "(graphically: c.f. at 2170 ≈ 88.8 minus c.f. at 2000 = 16 → 72.8)"])

# ------------------------------------------------------------------ L7
n.lesson("Lesson 7 — Mode, Empirical Relation and Missing Frequencies", "pp. 19–26")
n.formula(["Mode = L + [Δ_{1}/(Δ_{1} + Δ_{2})] × h",
           "Δ_{1} = f_{modal} − f_{pre-modal},  Δ_{2} = f_{modal} − f_{post-modal}",
           "Empirical relation (moderately skewed): Mode = 3 Median − 2 Mean"])
n.p("Weights 30–90 (f 18, 37, 45, 27, 15, 8): Mode = 50 + 8/(8 + 18) × 10 = 53.08. Marks (7, 32, 56, 106, 180, 164, 86, 44): "
    "Mode = 40 + 74/(74 + 16) × 10 = 48.22. Sales practice: 64.4. Ungrouped: the most frequent value (5, 8, 10, 8, 5, 8 → 8).")
n.p("Empirical-relation examples (pp. 23–25): weights median 54.44, mode 53.08 → mean = (3 × 54.44 − 53.08)/2 = 55.12; "
    "marks mean 56, median 40 + (40 − 30)/22 × 20 = 49.09 → mode = 3(49.09) − 2(56) = 35.27; heights mean 145.35, "
    "median 144.92 → mode 144.06.")
n.h2("Missing Frequencies (p. 26 practice 2)")
n.p("With the total N and the median (and/or mode) given, write one equation from Σf = N and one from the median (or mode) "
    "formula, then solve. Practice 2 (median 33.5, mode 34, N = 230): f = 60, 100, 40.")
n.exam_approach(["Let the unknowns be f_{1}, f_{2}; Σf = N gives f_{1} + f_{2} = …",
                 "Decide which class contains the given median; write the median equation with p.c.f. containing f_{1} if it lies above.",
                 "Solve, round to whole numbers, check the median, then find the mode by the Δ formula and comment on the shape "
                 "(compare mean, median, mode)."])
res = []
for med_, fx in ((413.11, None), (415, None)):
    x = round(500 - 102 - (med_ - 400) * 326 / 25)
    y = 475 - x
    Gm = Grouped(cl(300, 25, 8), [5, 17, 80, x, 326, y, 88, 9])
    res.append((med_, x, y, Gm))
n.practice("Lesson 7", "(a) Actual — 2014-15 Q6(a) (TF p. 10). (b) Actual — 2015-16 Q6(a) (TF p. 15).",
           ["(a) Incomplete distribution with total frequency 1000 and median 413.11: 300–325: 5, 325–350: 17, 350–375: 80, "
            "375–400: ?, 400–425: 326, 425–450: ?, 450–475: 88, 475–500: 9. Estimate the missing frequencies and find the mode.  (17)",
            "(b) The same table with median 415. Estimate the missing frequencies, find the modal value and comment on the "
            "shape of the distribution.  (18)"])
n.solution()
for lab, (med_, x, y, Gm) in zip("ab", res):
    mo, d = Gm.mode()
    n.answer(f"({lab})", f"Let f_{{4}} = x (375–400) and f_{{6}} = y (425–450).")
    n.code([f"Σf = 5 + 17 + 80 + x + 326 + y + 88 + 9 = 525 + x + y = 1000  →  x + y = 475",
            f"Median {g(med_)} lies in 400–425; p.c.f. = 5 + 17 + 80 + x = 102 + x;  N/2 = 500",
            f"{g(med_)} = 400 + (500 − 102 − x)/326 × 25  →  398 − x = {g((med_-400)*326/25,3)}  →  x ≈ {x},  y = 475 − {x} = {y}",
            f"Mode: modal class 400–425, Δ1 = 326 − {x} = {d['d1']}, Δ2 = 326 − {y} = {d['d2']}",
            f"Mode = 400 + {d['d1']}/({d['d1']} + {d['d2']}) × 25 = {g(mo,2)}"])
    if lab == "b":
        n.p(f"Mean (short-cut, A = 412.5) = {g(Gm.mean,2)}. Mean {g(Gm.mean,2)} < median 415 < mode {g(mo,2)}: the "
            "distribution is slightly negatively skewed (longer tail to the left), though nearly symmetric.")

n.quick_notes("Quick Notes — Central Tendency", "Revision points for Lessons 5–7.", [
    ("L5 · Means", ["x̄ = A + (Σfd/N)h, d = (x − A)/h. Marks 80 students → 56; heights → 145.35.",
                    "G.M. = antilog(Σf log x/N); H.M. = N/Σ(f/x)."]),
    ("L6 · Median and Quartiles", ["Median = L + (N/2 − pcf)/f × h; Q_{i}: iN/4; D_{i}: iN/10; P_{i}: iN/100.",
                                   "Ogive: across from N/2 to the curve, down to x. Wages: median 2079.17; 2000–2170: 72.8 ≈ 73."]),
    ("L7 · Mode and Missing Frequencies", ["Mode = L + Δ1/(Δ1 + Δ2) × h; Mode = 3Md − 2Mean.",
                                           "Median 413.11 → 227, 248, mode 413.98; median 415 → 202, 273, mode 417.51 (slight negative skew)."])])
n.save()
print("saved", n.out_path)
