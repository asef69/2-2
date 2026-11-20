"""MATH243_Stat_Intro_Graphs_Notes.docx — decks 1.1, 1.2, 5, 6 (L1–L4)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

from common import exam_map, new
from m243 import STAT, g

D11, D12 = STAT + r"\1.1 Stat L1.pdf", STAT + r"\1.2 Stat L2.pdf"
D5, D6 = STAT + r"\5. Graphical Representation Stat.pdf", STAT + r"\6. Graphical representation 2.pdf"

n = new("Stat", "Introduction, Frequency Distributions and Graphical Representation",
        "MATH243_Stat_Intro_Graphs_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "data, frequency tables, stem-and-leaf, diagrams"),
              ("Lesson 1 — Statistics, Data, Variables and Sampling", "descriptive vs inferential, scales, sampling methods"),
              ("Lesson 2 — Grouped Frequency Distributions", "classes, Sturges' rule, boundaries, cumulative frequency"),
              ("Lesson 3 — Histogram, Frequency Polygon, Ogive and Other Charts", "graphs, reading the median from the ogive, shapes"),
              ("Lesson 4 — Stem-and-Leaf Plots, Five-Number Summary and Boxplots", "stem-and-leaf, quartiles, boxplot, outliers"),
              ("Quick Notes — Introduction and Graphs", "revision bullets")],
    source_note="The four decks are scanned textbook pages (Bluman, Elementary Statistics). Page numbers: 1.1 Stat L1.pdf "
                "(15 pp.) = \"L1 p.\", 1.2 Stat L2.pdf (5 pp.) = \"L2 p.\", 5. Graphical Representation Stat.pdf (11 pp.) = "
                "\"G1 p.\", 6. Graphical representation 2.pdf (18 pp.) = \"G2 p.\". \"TF p.\" = merged question PDF page; "
                "\"22 batch p.\" = 2023-24 paper.")

n.h1("Exam Map — What the TF Papers Ask")
st = exam_map(n, "s1")
n.callout("focus", f"{st['n']} questions, {st['marks']} marks — all from 2021-22 onward, so this \"easy\" deck is now a "
          "regular Section B opener: build a frequency table with Sturges' rule and draw the histogram/ogive (15 marks), "
          "a stem-and-leaf plot with median/mode/range (10), and short theory on statistical data. Graph-reading (median "
          "from the ogive) is also asked — see Lesson 6 of the Central Tendency note.")

# ------------------------------------------------------------------ L1
n.lesson("Lesson 1 — Statistics, Data, Variables and Sampling", "L1 pp. 1–15")
n.h2("1. Basic Terms (L1 pp. 1–2)")
n.bullets(["**Statistics** — the science of conducting studies to collect, organise, summarise, analyse and draw "
           "conclusions from data.",
           "**Variable** — a characteristic that can take different values; **data** — the values (measurements or "
           "observations) a variable takes; a **data set** is a collection of data values, each one a datum. "
           "**Random variables** — variables whose values are determined by chance.",
           "**Population** — all subjects being studied; **census** — data from every subject; **sample** — a group of "
           "subjects selected from the population. A sample that does not represent the population is **biased**."])
n.h2("2. Descriptive and Inferential Statistics (L1 pp. 3–4)")
n.bullets(["**Descriptive statistics** — collection, organisation, summarisation and presentation of data (e.g. the census "
           "results as averages, charts, tables).",
           "**Inferential statistics** — generalising from samples to populations: estimation, hypothesis testing, "
           "relationships among variables, prediction. It uses probability.",
           "Example 1-1: average lottery jackpot → descriptive; \"older people on a high-calorie diet double their memory "
           "loss risk\" → inferential; average Valentine's spending from 9317 consumers → descriptive; laughter and pain "
           "tolerance → inferential."])
n.h2("3. Types of Variables (L1 pp. 5–6)")
n.code(["Variables",
        " ├─ Qualitative (categorical: gender, religion, location)",
        " └─ Quantitative (counted or measured: age, height, weight)",
        "      ├─ Discrete (countable: children in a family, calls per day)",
        "      └─ Continuous (measured, any value in an interval: temperature, weight)"])
n.p("Example 1-2: hurricane wind speed — continuous; baggage weight — continuous; pages in a book — discrete; money "
    "spent — discrete (smallest unit is a cent).")
n.h2("4. Levels of Measurement (L1 pp. 7–9)")
n.table(["Level", "Property", "Examples"],
        [["Nominal", "mutually exclusive categories, no order", "zip code, gender, colour, religion"],
         ["Ordinal", "ordered categories; differences not precise", "grades A–F, small/medium/large, rankings"],
         ["Interval", "precise differences; no true zero", "temperature (°F), IQ"],
         ["Ratio", "interval + true zero; ratios meaningful", "height, weight, age, salary"]], widths_cm=[2.6, 6.8, 7.8])
n.p("Example 1-4: ages of patients — ratio; movie ratings — ordinal; shirt colours — nominal; hot-tub temperatures — interval.")
n.h2("5. Sampling Methods (L1 pp. 10–15)")
n.table(["Method", "How the sample is chosen"],
        [["Random", "every member has an equal chance; numbered population + random numbers (table or computer)"],
         ["Systematic", "number the population, pick a random start in 1…k, then every k-th member (k = N/n, e.g. 2000/50 = 40)"],
         ["Stratified", "divide into subgroups (strata) by a relevant characteristic, then randomly sample from each stratum"],
         ["Cluster", "divide into clusters (e.g. areas, buildings), randomly select whole clusters and use all their members"]],
        widths_cm=[3, 14.2])
n.p("Example 1-5: records from one of 10 hospitals — cluster; students grouped by gender, major and GPA then sampled — "
    "stratified; numbered subscribers + random numbers — random; every 10th bottle — systematic. **Sampling error** is the "
    "difference between a sample result and the population result.")
n.figure_from_pdf(D11, 14, "Figure 1.1 — Stratified and cluster sampling, with the summary of sampling methods (L1 p. 14)",
                  clip=(0.08, 0.05, 0.92, 0.70), width_cm=10)
n.h2("6. Statistical Data and their Sources (textbook — 2022-23 Q5(a))")
n.callout("answer", "Statistical data are numerical facts collected in a systematic way for a definite purpose, in a "
          "form that can be compared and analysed (aggregates, not single isolated figures). They are produced by "
          "censuses, sample surveys, experiments and the administrative records of organisations; data collected first-"
          "hand are primary, data taken from published sources are secondary. We need them to describe a situation, "
          "compare groups, find relationships, forecast and make policy and business decisions on evidence instead of "
          "guesswork. Usual sources in Bangladesh: the Bangladesh Bureau of Statistics (Population and Housing Census, "
          "Household Income and Expenditure Survey, Labour Force Survey, Statistical Yearbook), Bangladesh Bank (monetary "
          "and trade statistics), ministries and directorates (DGHS health bulletins, Ministry of Education/BANBEIS), "
          "BIDS and other research institutes, BDHS (demographic and health survey), and international bodies (World "
          "Bank, UN agencies).")
n.practice("Lesson 1", "(a) Actual — 2022-23 Q5(a) (TF p. 49). (b) Adapted — L1 p. 15 Example 1-5.",
           ["(a) What do you mean by statistical data? How are they produced? Why do you need statistical data? What are "
            "the usual sources of statistical data in Bangladesh?  (10)",
            "(b) Explain stratified random sampling with an example."])
n.solution()
n.answer("(a)", "Model answer in §6.")
n.answer("(b)", "The population is divided into non-overlapping, internally similar subgroups (strata) and a simple random "
         "sample is drawn from each stratum, usually in proportion to its size. Example: to estimate average delivery "
         "time of an online medicine shop, divide orders by zone (Dhaka North, Dhaka South, outside Dhaka) and randomly "
         "select orders from each zone, so every zone is represented. (Asked with a z-test in 2023-24 Q6(c).)")

# ------------------------------------------------------------------ L2
n.lesson("Lesson 2 — Grouped Frequency Distributions", "L2 pp. 2–5")
n.h2("1. Constructing a Grouped Frequency Distribution (L2 pp. 2–4)")
n.numbered(["Range R = highest − lowest value.",
            "Choose the number of classes k (5–20; Sturges' rule k = 1 + 3.322 log_{10} N).",
            "Width = R/k, **rounded up** (4.9 → 5).",
            "Start at the lowest value (or a convenient number below it); lower limits go up by the width; upper limit "
            "= next lower limit − 1 unit.",
            "Class boundaries = limits ± 0.5 unit (no gaps). Class mark (midpoint) = (lower + upper)/2.",
            "Tally, count the frequencies, check that they total N."])
n.p("Example 2-2 — record high temperatures of the 50 states, 7 classes: H = 134, L = 100, R = 34, width = 34/7 = 4.9 → 5.")
n.table(["Class limits", "Boundaries", "Frequency", "Cumulative (less than upper boundary)"],
        [["100–104", "99.5–104.5", "2", "2"], ["105–109", "104.5–109.5", "8", "10"], ["110–114", "109.5–114.5", "18", "28"],
         ["115–119", "114.5–119.5", "13", "41"], ["120–124", "119.5–124.5", "7", "48"], ["125–129", "124.5–129.5", "1", "49"],
         ["130–134", "129.5–134.5", "1", "50"]], widths_cm=[3.4, 3.6, 3, 7.2])
n.h2("2. Cumulative Frequency (L2 pp. 4–5)")
n.p("Cumulative frequency = number of values less than or equal to a class's upper boundary (running total). Here 28 "
    "temperatures are ≤ 114.5 °F and 48 are ≤ 124.5 °F. When the range is small, an ungrouped distribution (one value per "
    "class) is used instead.")
n.exam_approach(["N, min, max, R; k by Sturges (round to a whole number); width = R/k rounded up.",
                 "Write limits, boundaries and class marks in one table; tally; total = N.",
                 "Add a cumulative-frequency column if a cumulative graph is asked."])
t = [18, 21, 22, 29, 25, 31, 37, 38, 41, 39, 44, 48, 54, 56, 56, 57, 47, 38, 35, 36, 29, 37, 32, 42, 43, 40, 48, 36, 37, 37,
     36, 38, 40, 41, 44, 39, 38, 34, 24, 32, 39, 44, 42, 30, 37, 30, 42, 37, 34, 37, 32, 24, 42, 36, 49, 39, 23, 34, 36, 40]
edges = [17.5 + 6 * i for i in range(8)]
freq = np.histogram(t, bins=edges)[0]
cum = np.cumsum(freq)
n.practice("Lesson 2", "(a) Actual — 2022-23 Q5(b) (TF p. 49). (b) Actual — 2021-22 Q5(b) (TF p. 44).",
           ["(a) The thickness (mm) of insulation in 60 transformer windings is recorded (table on TF p. 49). (i) Make a "
            "frequency table using Sturges' rule K = 1 + 3.322 log N. (ii) Draw a frequency histogram and a cumulative "
            "frequency graph.  (15)",
            "(b) (i) A sample of 34 observations recorded to the nearest integer ranges from 201 to 337. Seven classes of "
            "width 20 are used, the first beginning at 199.5: find the class limits and class marks. (ii) Two distributions "
            "have the same mean, SD and skewness. Find (comment on) their kurtosis.  (17)"])
n.solution()
n.answer("(a)", f"N = 60, smallest 18, largest 57, R = 39. K = 1 + 3.322 log 60 = 1 + 3.322(1.7782) = 6.91 ≈ 7 classes; "
         "width = 39/7 = 5.57 → 6. Start at 18 (boundary 17.5).")
n.table(["Limits", "Boundaries", "Class mark", "Frequency", "Cumulative"],
        [[f"{int(a+0.5)}–{int(b-0.5)}", f"{a}–{b}", g((a + b) / 2), str(f), str(c)]
         for a, b, f, c in zip(edges[:-1], edges[1:], freq, cum)] + [["Total", "", "", "60", ""]],
        widths_cm=[3, 3.6, 3, 3, 3.4])
n.p("(ii) Histogram: boundaries 17.5, 23.5, …, 59.5 on the x-axis, bars of heights 4, 5, 10, 25, 9, 3, 4 with no gaps. "
    "Cumulative frequency graph (ogive): plot (17.5, 0), (23.5, 4), (29.5, 9), (35.5, 19), (41.5, 44), (47.5, 53), "
    "(53.5, 56), (59.5, 60) and join by straight lines. The distribution peaks in 35.5–41.5 mm.")
n.code(["Freq",
        " 25 |              ████",
        " 20 |              ████",
        " 15 |              ████",
        " 10 |         ████ ████",
        "  5 |    ████ ████ ████ ████      ████",
        "  0 +─████─████─████─████─████─████─████──→ thickness (mm)",
        "    17.5 23.5 29.5 35.5 41.5 47.5 53.5 59.5"])
n.answer("(b)", "(i) Boundaries 199.5–219.5, 219.5–239.5, …, 319.5–339.5; class limits 200–219, 220–239, 240–259, 260–279, "
         "280–299, 300–319, 320–339; class marks 209.5, 229.5, 249.5, 269.5, 289.5, 309.5, 329.5 (the range 201–337 "
         "fits inside).")
n.p("(ii) Mean, SD and skewness fix the location, spread and symmetry only. Kurtosis β_{2} = μ_{4}/μ_{2}² depends on the "
    "fourth moment, which these three measures do not determine, so the two distributions can still differ in "
    "peakedness: one may be leptokurtic (β_{2} > 3) and the other platykurtic (β_{2} < 3). Compute β_{2} for each to "
    "compare (see the Skewness, Moments and Kurtosis note).")

# ------------------------------------------------------------------ L3
n.lesson("Lesson 3 — Histogram, Frequency Polygon, Ogive and Other Charts", "G1 pp. 1–11 · G2 pp. 1–8")
n.h2("1. The Three Basic Graphs (G1 pp. 1–5)")
n.bullets(["**Histogram** — contiguous vertical bars on the class boundaries; heights = frequencies.",
           "**Frequency polygon** — points (class midpoint, frequency) joined by lines; close it on the x-axis one class "
           "width beyond each end.",
           "**Ogive** (cumulative frequency graph) — points (upper boundary, cumulative frequency), starting at (first lower "
           "boundary, 0). Read \"how many below x\" by going up from x to the curve and across."])
n.figure_from_pdf(D5, 1, "Figure 3.1 — Histogram of the record high temperatures (G1 p. 1)", clip=(0.0, 0.52, 0.72, 0.84), width_cm=10)
n.figure_from_pdf(D5, 5, "Figure 3.2 — Ogive; 28 values lie below 114.5 °F (G1 p. 5)", clip=(0.04, 0.39, 0.96, 0.68), width_cm=10)
n.h2("2. Relative Frequency Graphs (G1 pp. 6–9)")
n.p("Divide each frequency by N (proportions summing to 1) and draw the same three graphs; used to compare data sets of "
    "different sizes. Runners' miles (N = 20): relative frequencies 0.05, 0.10, 0.15, 0.25, 0.20, 0.15, 0.10; cumulative "
    "0.05, 0.15, 0.30, 0.55, 0.75, 0.90, 1.00.")
n.h2("3. Distribution Shapes (G1 pp. 9–11)")
n.p("Bell-shaped, uniform, J-shaped, reverse J-shaped, right (positively) skewed — tail to the right, left (negatively) "
    "skewed, bimodal, U-shaped. Look for peaks, gaps, outliers and the side of the longer tail.")
n.figure_from_pdf(D5, 10, "Figure 3.3 — Distribution shapes (G1 p. 10)", clip=(0.02, 0.02, 0.98, 0.98), width_cm=8.5)
n.h2("4. Other Graphs (G2 pp. 1–8)")
n.table(["Graph", "Use / construction"],
        [["Bar graph", "categorical data; bars separated, horizontal or vertical"],
         ["Pareto chart", "categorical frequencies as bars arranged from largest to smallest (police calls)"],
         ["Time series graph", "data over time, points joined in order; compound graph for two series"],
         ["Pie graph", "parts of a whole; angle = (f/n) × 360°, % = (f/n) × 100 (snack foods 134°, 98°, 52°, 46°, 30°)"],
         ["Dotplot", "each value as a dot above a number line; repeats stacked (named storms)"]], widths_cm=[3.6, 13.6])
n.h2("5. Scatter Plot (textbook; asked 2023-24 Q5(b))")
n.p("For paired quantitative data (x, y): plot each pair as a point. The pattern shows the direction (positive/negative), "
    "form (linear/curved) and strength of the relationship and any outliers. It is the first step of correlation "
    "analysis (Correlation & Regression note).")
n.exam_approach(["Histogram/polygon/ogive: use boundaries (histogram, ogive) or midpoints (polygon) — label both axes.",
                 "Ogive median: locate N/2 on the y-axis, go across to the curve and down to the x-axis.",
                 "Pie: angles must sum to 360°. Scatter: one point per pair, then describe direction and strength."])
n.practice("Lesson 3", "(a) Actual — 2023-24 Q5(b) (22 batch p. 3).",
           ["(a) Explain the scatter plot briefly with an example. Prices ($) and ratings (out of 5) of 5 restaurants: "
            "A (22, 3.5), B (29, 4.0), C (15, 3.0), D (18, 4.0), E (23, 3.5). Plot them and interpret whether there is a "
            "relationship between price and rating.  (13)"])
n.solution()
n.code(["Rating",
        " 4.0 |        • D(18)            • B(29)",
        " 3.5 |              • A(22) • E(23)",
        " 3.0 |  • C(15)",
        "     +----+----+----+----+----+----→ Price ($)",
        "         15   18   21   24   27   30"])
n.p("The points rise from left to right on the whole: dearer restaurants tend to have higher ratings, a weak-to-moderate "
    "positive relationship (r = 0.60). D is an exception (cheap but rated 4.0), so price is not a strong predictor of "
    "rating with only five points.")

# ------------------------------------------------------------------ L4
n.lesson("Lesson 4 — Stem-and-Leaf Plots, Five-Number Summary and Boxplots", "G2 pp. 8–18")
n.h2("1. Stem-and-Leaf Plot (G2 pp. 8–12)")
n.p("A stem-and-leaf plot uses part of each value as the stem and the rest as the leaf (34 → stem 3, leaf 4; 356 → 35 | 6). "
    "It sorts and graphs the data at once while keeping the actual values.")
n.numbered(["Arrange the data in order (helpful, not essential).", "Split each value into leading digit(s) = stem and trailing digit = leaf.",
            "Write the stems in a column and the leaves (in order) beside them; leave an empty row for a stem with no data."])
n.figure_from_pdf(D6, 10, "Figure 4.1 — Stem-and-leaf plot of 20 days' cardiograms (G2 p. 10)", clip=(0.32, 0.29, 0.78, 0.47), width_cm=8)
n.p("Classes of five (Example 2-15: car thefts, stems 5, 5, 6, 6, 7, 7 for 50–54, 55–59, …) and back-to-back plots for two "
    "data sets sharing the same stems (Example 2-16: Atlanta vs Philadelphia buildings).")
n.h2("2. Five-Number Summary and Boxplot (G2 pp. 13–18)")
n.p("Minimum, Q_{1}, median, Q_{3}, maximum. Boxplot: a box from Q_{1} to Q_{3} with a line at the median, whiskers to the "
    "minimum and maximum. Meteorites: 30, 39, 47, 48, 78, 89, 138, 164, 215, 296 → median 83.5, Q_{1} = 47, Q_{3} = 164.")
n.figure_from_pdf(D6, 15, "Figure 4.2 — Boxplot for the meteorite data (G2 p. 15)", clip=(0.04, 0.37, 0.96, 0.56), width_cm=11)
n.bullets(["Median near the centre of the box and equal whiskers → approximately symmetric.",
           "Median left of centre / right whisker longer → positively skewed; the opposite → negatively skewed.",
           "Comparing two boxplots on one axis: medians compare averages, box lengths (IQR) compare variability "
           "(real cheese 67.5/200/275 vs substitute 215/265/300).",
           "Modified boxplot: whiskers stop at the last value within 1.5 IQR; mild outliers lie beyond Q ± 1.5 IQR, "
           "extreme outliers beyond Q ± 3 IQR."])
n.exam_approach(["Sort the data; choose stems so there are 5–10 rows; write leaves in order; add a key (17 | 2 = 17.2).",
                 "Median = middle value (average of the two middle ones when n is even); mode = most frequent leaf; "
                 "range = max − min.",
                 "Boxplot: five-number summary first, then the scaled axis and the box."])
p = sorted([17.2, 16.4, 18.6, 17.4, 17.5, 19.0, 17.4, 16.8, 19.0, 17.8, 18.8, 18.7])
n.practice("Lesson 4", "(a) Actual — 2022-23 Q6(b) (TF p. 50). (b) Actual — 2023-24 Q5(a) (22 batch p. 3).",
           ["(a) Lengths (cm) of 12 pencils: 17.2, 16.4, 18.6, 17.4, 17.5, 19.0, 17.4, 16.8, 19.0, 17.8, 18.8, 18.7. Use a "
            "stem-and-leaf plot to display the data. Hence find the median, mode and range.  (10)",
            "(b) What do you mean by stem-and-leaf plots? How do you create one? Explain with examples.  (10)"])
n.solution()
n.answer("(a)", "Ordered: " + ", ".join(g(v) for v in p) + ". Stem = whole centimetres, leaf = tenths (key 17 | 2 = 17.2 cm).")
n.code(["16 | 4 8", "17 | 2 4 4 5 8", "18 | 6 7 8", "19 | 0 0"])
n.p(f"n = 12 (even): median = (6th + 7th)/2 = (17.5 + 17.8)/2 = {g(np.median(p))} cm. Mode: 17.4 and 19.0 each occur twice "
    "→ bimodal (17.4 cm and 19.0 cm). Range = 19.0 − 16.4 = 2.6 cm.")
n.answer("(b)", "Definition and the three steps in §1, with the cardiogram example (Figure 4.1) or the pencil example "
         "above. Mention its advantage over a grouped frequency table: the original values are kept.")

n.quick_notes("Quick Notes — Introduction and Graphs", "Revision points for Lessons 1–4.", [
    ("L1 · Basics", ["Descriptive = organise/summarise; inferential = sample → population (uses probability).",
                     "Qualitative vs quantitative (discrete/continuous). Nominal < ordinal < interval < ratio (true zero).",
                     "Random, systematic (every k-th), stratified (sample each stratum), cluster (whole groups)."]),
    ("L2 · Frequency Tables", ["Sturges k = 1 + 3.322 log N; width = range/k rounded up; boundaries ± 0.5 unit.",
                               "Thickness: k ≈ 7, width 6, f = 4, 5, 10, 25, 9, 3, 4. 34 values 201–337: marks 209.5 … 329.5."]),
    ("L3 · Graphs", ["Histogram (boundaries), polygon (midpoints), ogive (upper boundary, cumulative f).",
                     "Shapes: bell, uniform, J, reverse J, right/left skewed, bimodal, U. Pie angle = f/n × 360°.",
                     "Scatter plot: direction, form, strength; restaurants weakly positive."]),
    ("L4 · Stem-and-Leaf and Boxplot", ["Pencils: 16|4 8, 17|2 4 4 5 8, 18|6 7 8, 19|0 0; median 17.65, modes 17.4 & 19.0, range 2.6.",
                                        "Five-number summary → boxplot; outliers beyond 1.5 IQR (mild) and 3 IQR (extreme)."])])
n.save()
print("saved", n.out_path)
