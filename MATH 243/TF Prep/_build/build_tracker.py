"""Builds MATH243_KKS_TF_Practice_Tracker.xlsx and MATH243_Stat_TF_Practice_Tracker.xlsx from questions.json."""
import os
import sys

sys.path.insert(0, r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2\_tfprep")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tracker_lib import build_tracker

from common import questions

OUT = r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2\MATH 243\TF Prep"
QPDF = "MATH 243 All Merged Questions.pdf (22 batch = MATH 243 (22 batch).pdf)"
OLD = "MATH 243 = current code; MATH 245 (2016-17 to 2021-22) and MATH 241 (2011-12 to 2015-16) = old Complex Variables & Statistics papers — only their statistics/probability parts are listed."

TOPIC = {
    "L1": "Events, axioms, addition rule — Lec 1 pp. 2–6, Lec 2 pp. 1–2", "L2": "Counting, classical probability — Lec 2 pp. 2–8",
    "L3": "Multiplication rule, independence, odds — Lec 2 pp. 8–9, Lec 3&4 pp. 1–6", "L4": "Joint probability table — Lec 3&4 pp. 6–12",
    "L5": "Conditional probability — Lec 5 pp. 1–4", "L6": "Total probability, Bayes — Lec 5 pp. 4–7",
    "L7": "Random variables, pmf — Lec 6", "L8": "pdf, CDF, exponential — Lec 7 (+ textbook)",
    "L9": "Expectation, variance, Chebyshev — Lec 9 pp. 1–5, other dist. p. 1", "L10": "Joint pmf/pdf, marginals — Lec 8 pp. 1–6",
    "L11": "Conditional distributions, independence — Lec 8 pp. 7–11", "L12": "E(XY), covariance — Lec 9 pp. 5–9",
    "L13": "Binomial — Lec 10", "L14": "Poisson, binomial limit — Lec 11", "L15": "Multinomial, hypergeometric, geometric — other dist. pp. 3–6",
    "L16": "Normal, z table — Lec 12 pp. 1–8", "L17": "Sums of normals, x̄, normal approx. — Lec 12 pp. 6–11 (+ textbook)",
    "L20": "Hypotheses, errors, p-value — Hyp pp. 1–6, 11–12", "L21": "One-sample z and t tests, CI — Hyp pp. 7–16",
    "L22": "Two-sample and paired tests — Hyp pp. 16–31", "L23": "Tests for r and proportions — Hyp pp. 32–37",
    "L24": "χ² contingency / goodness of fit — Hyp pp. 38–44",
    "L18": "F-test, one-way ANOVA — ANOVA pp. 1–10", "L19": "Two-way ANOVA — textbook",
}
STOPIC = {
    "L1": "Statistics, data, sampling — 1.1 Stat L1", "L2": "Frequency distributions, Sturges — 1.2 Stat L2",
    "L3": "Histogram, ogive, charts — Graphical 1–2", "L4": "Stem-and-leaf, boxplot — Graphical 2 pp. 8–18",
    "L5": "Means — Central Tendency pp. 1–6", "L6": "Median, quartiles, ogive — Central Tendency pp. 7–18",
    "L7": "Mode, missing frequencies — Central Tendency pp. 19–26", "L8": "Range, QD, MD — Dispersion pp. 1–8",
    "L9": "SD, CV, consistency — Dispersion pp. 9–23", "L10": "Pearson/Bowley/Kelly skewness — Skewness pp. 1–7",
    "L11": "Moments, β1, β2, kurtosis — Skewness pp. 8–15", "L12": "Correlation, scatter — Correlation pp. 1–5",
    "L13": "Rank correlation — Correlation pp. 5–7", "L14": "Regression lines — Correlation pp. 8–12",
    "L15": "R², polynomial, multiple — Correlation pp. 12–17",
}
METHOD = {"stat_data", "define_measures", "normal_theory", "test_concepts", "type_errors"}
PARTIAL = set()

KKS_TABS = [("k1", "1 Probability Basics", "Lec 1–4 — Sets, Counting, Rules, Odds, Joint Tables", "MATH243_KKS_Probability_Basics_Notes.docx"),
            ("k2", "2 Conditional + Bayes", "Lec 5 — Conditional Probability and Bayes' Theorem", "MATH243_KKS_Conditional_Bayes_Notes.docx"),
            ("k3", "3 Random Variables", "Lec 6, 7, 9 — pmf, pdf, CDF, Expectation, Chebyshev", "MATH243_KKS_Random_Variables_Notes.docx"),
            ("k4", "4 Joint Distributions", "Lec 8–9 — Joint, Marginal, Conditional, Covariance", "MATH243_KKS_Joint_Distributions_Notes.docx"),
            ("k5", "5 Discrete Distributions", "Lec 10–11 — Binomial, Poisson, Multinomial, Hypergeometric", "MATH243_KKS_Discrete_Distributions_Notes.docx"),
            ("k6", "6 Normal Distribution", "Lec 12 — Normal Distribution and Approximations", "MATH243_KKS_Normal_Distribution_Notes.docx"),
            ("k7", "7 ANOVA", "ANOVA (KKS Sir's part) — F-test, One-way and Two-way", "MATH243_KKS_ANOVA_Notes.docx"),
            ("k8", "8 Hypothesis Testing", "Lecture 13–20 — z, t, Two-sample, Proportion, χ² Tests", "MATH243_KKS_Hypothesis_Testing_Notes.docx")]
STAT_TABS = [("s1", "1 Intro + Graphs", "Decks 1.1, 1.2, 5, 6 — Data, Frequency Tables, Graphs", "MATH243_Stat_Intro_Graphs_Notes.docx"),
             ("s2", "2 Central Tendency", "Deck 2 — Mean, Median, Quartiles, Mode", "MATH243_Stat_Central_Tendency_Notes.docx"),
             ("s3", "3 Dispersion", "Deck 3 — Range, QD, MD, SD, CV", "MATH243_Stat_Dispersion_Notes.docx"),
             ("s4", "4 Skewness + Moments", "Deck 4 — Skewness, Moments and Kurtosis", "MATH243_Stat_Skewness_Moments_Kurtosis_Notes.docx"),
             ("s5", "5 Correlation + Regression", "Deck 7 — Correlation and Regression Analysis", "MATH243_Stat_Correlation_Regression_Notes.docx")]


def row(q, topics):
    return dict(year=q["year"], course=q["course"], qno=q["qno"], question=q["question"],
                topic=topics[q["lesson"]], lesson=q["lesson"], marks=q["marks"], page=q["page"], type=q["type"],
                in_notes="◐ Method" if q["key"] in METHOD else "✔ Solved", same_type=q["same_type"])


def tabs(spec, topics):
    out = []
    for key, sheet, title, nf in spec:
        out.append(dict(sheet=sheet, title=title, note_file=nf,
                        rows=[row(q, topics) for q in questions(key) if int(q["year"][:4]) >= FROM]))
    return out


FROM = 2018  # trackers list only papers from the 2018-19 session onward
allq = [q for q in questions() if int(q["year"][:4]) >= FROM]
outside = [dict(year=q["year"], course=q["course"], qno=q["qno"], question=q["question"],
                area={"t_test": "t-test (one sample)", "z_test": "z-test / confidence interval", "chi_fit": "χ² goodness of fit",
                      "chi_indep": "χ² test of independence", "two_sample_z": "two-sample z-test", "two_sample_t": "two-sample t-test",
                      "two_prop": "two-proportion test", "type_errors": "Type I / II errors", "test_concepts": "hypothesis-testing concepts",
                      "clt": "central limit theorem"}.get(q["key"], q["key"]), marks=q["marks"], page=q["page"])
           for q in allq if q["part"] == "OUT"]

build_tracker(os.path.join(OUT, "MATH243_KKS_TF_Practice_Tracker.xlsx"), course="MATH 243",
              part_name="KKS Sir — Probability & ANOVA", part_short="KKS", qpdf=QPDF, tabs=tabs(KKS_TABS, TOPIC),
              outside=outside, high_from="2019-20", old_codes=OLD,
              notes_extra=["Tracker lists papers from the 2018-19 session onward only (older papers are left out on purpose; they are still solved in the notes).",
                           "Outside Notes: only the central-limit-theorem question (2023-24 Q6(b)) — not in any slide deck; hypothesis "
                           "testing is now covered by tab 8 (Lecture-13-20- Hypothesis.pdf).",
                           "Complex-variable questions of the old MATH 241/245 papers are not listed."])
build_tracker(os.path.join(OUT, "MATH243_Stat_TF_Practice_Tracker.xlsx"), course="MATH 243",
              part_name="Statistics (descriptive) part", part_short="Stat", qpdf=QPDF, tabs=tabs(STAT_TABS, STOPIC),
              outside=None, high_from="2019-20", old_codes=OLD,
              notes_extra=["Tracker lists papers from the 2018-19 session onward only (older papers are left out on purpose; they are still solved in the notes).",
                           "Inference questions (tests, χ², CI) are in the KKS tracker, tab 8."])

# coverage print
import collections
c = collections.Counter((q["year"], q["part"]) for q in allq)
sys.stdout.reconfigure(encoding="utf-8")
for y in sorted({q["year"] for q in allq}):
    print(y, "KKS", c[(y, "KKS")], "Stat", c[(y, "Stat")], "Outside", c[(y, "OUT")], "dropped", c[(y, "DROP")])
