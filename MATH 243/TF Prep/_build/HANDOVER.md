# MATH 243 TF kit — hand-over (session stopped at usage limit, 2026-10-16)

Nothing is built yet: no notes, no tracker, no questions.json. This file holds what I read so far.

## Done
- Read _tfprep/FORMAT_SPEC.md, notes_lib.py, tracker_lib.py, tools.py.
- Read the gold reference: CSE209_Control_Unit_Notes (full), SingleCycle notes (first ~25 KB), and the RS tracker.
- Read every probability lecture (1, 2, 3&4, 5–12, "other distributions") as text.
- Read stats decks 1.1, 1.2, 5, 6 (scanned, rendered), 2 Central Tendency, 3 Dispersion, 4 Skewness/Moments/Kurtosis.
- Read the 22-batch paper (2023-24, 5 pp.) visually, and merged-PDF pages 1–17 (text) and 49–54 (images).

## Not done
- Stats 7 (Correlation & regression) and 8 (ANOVA, KKS Sir): not read yet.
- Merged-PDF pp. 18–48 still need a visual read. Those page images did not load in this session, so re-render them and read them. The text layer is garbage on many pages.
- Classify questions, solve them, check the numbers in Python, build notes and trackers, convert to PDF and look at the pages.

## Teachers / part tags
- Probability lectures: Lecture 1 names "Course Teacher 1: Kanchan Kumar Sen, PhD (DU Statistics)". The ANOVA deck says "KKS Sir's part", so tag = **KKS**.
- Stats decks 1.1/1.2/5/6 have PDF author metadata "Md. Nahid Hasan" (metadata only, not on the pages). Decks 2/3/4 have "DOLLY" and deck 7 has "user". No teacher name has been seen on any stats page, so use **Stat** unless the papers show a name. The ANOVA deck is KKS even though it sits in stats/. Decide which tracker it belongs in (probably KKS).
- Course textbook: Walpole, Myers, Myers & Ye, 9th ed.

## Question-paper facts (verified)
- Merged PDF, 54 pp. Old papers are **MATH 241 (Complex Variables and Statistics)**: Section A = complex variables (out of scope), Section B = statistics + some probability. Seen so far: 2011-12 (pp. 1–3), 2012-13 (pp. 4–5), 2013-14 (pp. 6–8), 2014-15 (pp. 9–11, plus a t-table on p. 12 and a z-table on p. 13), 2015-16 (pp. 14–16, plus a table on p. 17).
- Duplicate pages: 23–27 are identical to 28–32 (checked by comparing the page text). Count those questions once.
- Pages 49–51 are a MATH 243/CSE paper (year still to be read from its cover page, around p. 47–48). Section A ends with 4(c), regression on husband/wife ages (13 marks). Section B:
  - 5(a) statistical data and its sources in BD (10)
  - 5(b) thickness data, Sturges' rule frequency table, histogram, ogive (15)
  - 5(c) bulb life, Company A vs B (10)
  - 6(a) define SD, variance, skewness, kurtosis, moments (10)
  - 6(b) stem-and-leaf of 12 pencils, median/mode/range (10)
  - 6(c) profits 10-20…50-60 (18, 20, 30, 22, 10): first four moments, γ1, γ2 (15). This is the same data as Stats deck 4 p. 11.
  - 7(a) concept pairs (10)
  - 7(b) GPA z-test + 99% CI (12)
  - 7(c) bank waiting-time t-test (13)
  - 8(a) drug/typhoid χ² 2×2 (10)
  - 8(b) one-way ANOVA, 4 bulb brands (10)
  - 8(c) two-way ANOVA, corn × blocks (15)
  - Pages 52–54 are z/F tables.
- 22-batch paper = **2023-24 MATH 243**, L-2/T-II, dated 21/05/2026. Give its rows page "22 batch p.N". Section A:
  - 1(a) mutually exclusive vs independent (6)
  - 1(b) multiplication law, ball transferred between boxes (12)
  - 1(c) Bayes, party A/B/C, 45/40/15 % support, 65/80/50 % turnout (17)
  - 2(a) CDF 1−e^{−8x}, P(wait < 12 min) (15)
  - 2(b) pens 3 red, 2 blue, 3 black, choose 2: joint pmf, P(x+y≤1), marginals, Var X, Cov (20)
  - 3(a) Chebyshev, 70 jobs, mean 60, SD 6, score 84 (11). This is textbook Ex. 4.76 from the "other distributions" PDF.
  - 3(b) binomial→Poisson relation, 0.5 calls/min, P(2 calls in 5 min) (12)
  - 3(c) binomial n=15, p=0.4 (12)
  - 4(a) mode of normal = μ; bulbs N(800, 40), P(778<X<834) (11)
  - 4(b) Pearson r; rank correlation with ties, sales/expenses (12)
  - 4(c) 2nd-degree polynomial fit, nitrogen/yield, R² (12)

  Section B:
  - 5(a) stem-and-leaf (10)
  - 5(b) scatter plot, price vs rating (13)
  - 5(c) corrected mean/SD/CV, n=200 (12)
  - 6(a) moments, β1, β2, marks 0-70 (13)
  - 6(b) CLT (10)
  - 6(c) stratified sampling + z-test, delivery time (12)
  - 7(a) short notes on tests (10)
  - 7(b) two-proportion test (12)
  - 7(c) two-sample t-test (13)
  - 8(a) χ² independence 3×3 (15)
  - 8(b) one-way ANOVA, 3 cities (20)
- So **Section A ≠ probability only**: correlation and regression appear in Section A (2023-24 Q4(b),(c), and 4(c) on p. 49). Hypothesis tests (z, t, χ², proportions) appear in Section B, but no deck covers them yet (decks are descriptive stats + correlation + ANOVA). Put them in Outside Notes unless deck 7 or 8 covers them. Lecture 12 p. 11 does a z-test for a proportion as a side example.

## Slide content map (for lesson planning)
- Prob L1: syllabus, sample space, events, set operations, axioms, addition rule.
- L2: random experiment, equally likely events, De Morgan, permutations and combinations (committee problems), classical probability, multiplication rule.
- L3&4: odds (X/Y solving problems, independent and dependent cases), joint probability, 2×2 tables, machines A/B (Bayes-like), pens joint pmf (3 blue, 2 red, 3 green). This is the same type as 2023-24 2(b).
- L5: conditional probability, TV-show couple problem (also in old papers), Bayes' theorem with proof, blood test, urns, transport problems.
- L6: random variables, pmf checks, k-value tables, α(3/4)^x.
- L7: CDF (discrete and continuous), pdf k-problems, F(x) for piecewise densities.
- L8: joint pmf/pdf, marginals, conditional (incl. (6−x−y)/8 on 0<x<2, 2<y<4, which is the old-paper P(1<Y<3|x=2) type), independence.
- L9: expectation, variance, insurance gain, E(X+Y), E(XY).
- L10: Bernoulli/binomial (proofs of mean/var asked), truck example.
- L11: Poisson, mean=var proof, Poisson approximation to binomial.
- L12: normal, z-table use, finding k, continuity correction, normal approximation to binomial.
- "Other distributions": Chebyshev, multinomial, hypergeometric intro, uniform, normal exercises (Walpole pp. 137–186).
- Stat 1.1: statistics, variables, levels of measurement, sampling methods (random/systematic/stratified/cluster).
- 1.2: grouped frequency distribution (record temps, 7 classes), cumulative frequency.
- 5: histogram, frequency polygon, ogive, relative frequency graphs, distribution shapes.
- 6: bar, Pareto, time series, pie, dotplot, stem-and-leaf (incl. back-to-back), five-number summary, boxplot, modified boxplot / outliers.
- 2 Central tendency: AM (shortcut), median, quartiles/deciles/percentiles, mode (Δ formula), GM, HM, empirical relation, missing-frequency problem (p. 26).
- 3 Dispersion: range, QD, MD, variance/SD with **divisor N**, the ±σ coverage rule, CV, empirical relations QD = (2/3)σ and MD = (4/5)σ.
- 4: Pearson SK = (mean−mode)/σ, Bowley, Kelly, raw→central moments, β1, β2, γ1, γ2, kurtosis types.

## Repeat types already spotted in old MATH 241 papers
- Pearson skewness + kurtosis from grouped data (2011-12 6(a), 2013-14 6(b), 2014-15 6(b), 2015-16 7(a)).
- Missing frequencies from median 413.11 / 415 (2014-15 6(a), 2015-16 6(a)).
- Which sample is more consistent, CV (2011-12 6(b), 2013-14 6(a), 2015-16 6(b)).
- Two regression lines + r (2011-12 7(a), 2013-14 7(a), 2014-15 7(a), 2015-16 7(b)).
- Binomial / Poisson numericals.
- TV-show conditional probability (2015-16 8(a)).
- Normal % between marks (2014-15 8(c), 2015-16 8(b)).
- χ² 5-children families (2012-13, 2013-14).
- t-tests (several years).

## Session 2 progress (resumed)
- Read Stat 7 (Correlation & regression, 17 pp.): types of correlation, scatter diagrams (pp. 1–3); Pearson r, sales/expenses example r from Σxy=70, Σx²=360, Σy²=22 (p. 4); proof −1≤r≤1 (p. 5); Spearman rank, managers example ΣD²=14 (pp. 5–6), tests example ΣD²=44 (p. 6); ties correction, Bangla/English ΣD²=81.5 (p. 7); regression concepts (pp. 8–9); least squares normal equations (p. 10); transmitter example Σx=118, Σy=336.6, Σx²=1708, Σxy=3834.3 (p. 11); Y on X vs X on Y, SST=SSE+SSR, R² (pp. 12–14); hardness/strength exercise (p. 14); multiple regression rice/rainfall/urea (pp. 14–16); 2nd-degree polynomial nitrogen 0–5 → 15,25,40,55,52,43 (p. 17) = 2023-24 Q4(c) data.
- Read Stat 8 ANOVA (KKS, 10 pp.): F-test two variances, assumptions, decision table (pp. 1–2); Lammers Limos F=4.23 vs F0.05,6,7=3.87 (pp. 2–3); exercises (pp. 3–4); one-way ANOVA CT/SB/ST/SW (pp. 4–5); reactor example F=28.10 (pp. 6–7); pairwise t with MSE, t0.025,12=2.179 (pp. 8–9); exercises (pp. 9–10). NO two-way ANOVA in the deck → teach as textbook.

## Decisions (session 2)
- All merged pages read. Papers: 2011-12, 2012-13, 2013-14, 2014-15, 2015-16 (MATH 241), 2016-17, 2018-19, 2019-20, 2020-21, 2021-22 (MATH 245), 2022-23 (MATH 243, pp. 47–51), 2023-24 (22 batch file). No 2017-18 paper. pp. 28–32 duplicate 23–27. Complex-variable questions (old Section A + old Q5 contour) are dropped: other subject.
- Two trackers / part tags: **KKS** = probability lectures + ANOVA deck (KKS Sir's own); **Stat** = stats decks 1.1–7. Hypothesis tests / CI / χ² / CLT (not in any deck) → KKS Outside Notes (inference sits with ANOVA).
- Assign by topic, not by section letter (Section A of MATH 243 also carries correlation/regression).
- 2019-20 6(a) transmitter: paper prints X2 = 12, deck p.11 prints 1 (Σx=118 matches 1). Solve the paper's data, note the deck version.
- Raw question list: _build/questions_raw.md → questions.py → questions.json.
- [done] questions.py / questions.json written (57 KKS, 43 Stat, 24 Outside, 7 dropped complex). Marks per paper check out (105 / 140 / 280).
- [done] m243.py helper (grouped tables, moments, regression, Spearman with ties, ANOVA 1- and 2-way).
- NEXT: check_kks.py (all KKS numbers) → build_k1…k7; check_stat.py → build_s1…s5; build_tracker.py; PDF check.
- [done] check_kks.py → check_kks_output.txt (all KKS answers). Flags: 2015-16 8(a) data inconsistent (P(H∩W)=0.28 > P(H)=0.25); ANOVA deck reactor example has Σx²=87713 but true 87716 (F = 27.55, not 28.10).
- [done] build_k1 (Probability Basics, L1–L4), build_k2 (Conditional & Bayes, L5–L6) → notes/. k1 PDF checked visually.
- Note files plan — KKS: k1 Basics L1–4 · k2 Cond/Bayes L5–6 · k3 Random Variables L7–9 · k4 Joint L10–12 · k5 Discrete L13–15 · k6 Normal L16–17 · k7 ANOVA L18–19. Stat: s1 Intro & Graphs L1–4 · s2 Central Tendency L5–7 · s3 Dispersion L8–9 · s4 Skewness/Moments/Kurtosis L10–11 · s5 Correlation & Regression L12–15.
- [done] build_k3 (Random Variables L7–9), build_k4 (Joint L10–12).
- [done] build_k5 (Discrete L13–15), build_k6 (Normal L16–17; PDF made in scratchpad, its figure crops still need a visual check).
- NEXT: build_k7 (ANOVA L18–19: one-way + pairwise t, two-way corn ×blocks textbook; numbers in check_kks_output.txt), then check_stat.py + build_s1…s5, build_tracker.py (Outside = part OUT), PDF checks, final report.
- Fix in k6: GPA example line uses 0.7486 (table) — fine. The slide's reactor Σx² is wrong (87713 vs 87716) → note it in k7.
- [done] build_k7 (ANOVA L18–19); k6 figure crops fixed.
- [done] build_s1 (Intro & Graphs L1–4, crops fixed), build_s2 (Central Tendency L5–7), build_s3 (Dispersion L8–9), build_s4 (Skew/Moments L10–11). check_stat.py → check_stat_output.txt. NEXT: build_s5 (Correlation & Regression L12–15), tracker, PDF checks.
- [done] build_s5 (Correlation & Regression L12–15). NEXT: build_tracker.py, PDF checks, report.
- [done] build_tracker.py → MATH243_KKS_TF_Practice_Tracker.xlsx (57 rows + 24 Outside) and MATH243_Stat_TF_Practice_Tracker.xlsx (43 rows). All 12 notes converted to PDF and spot-checked; figure crops fixed (k6, s1, s5).
- KIT COMPLETE.
- [update 2026-10-23] New file MATH 243/probability/Lecture-13-20- Hypothesis.pdf (44 pp.: hypothesis tests, z/t, two-sample, paired, r test, proportions, χ²). Added build_k8.py → MATH243_KKS_Hypothesis_Testing_Notes.docx (L20–L24); questions.py remaps the 23 inference questions from OUT to KKS note k8; tracker has tab "8 Hypothesis Testing" (KKS now 80 questions); Outside Notes keeps only 2023-24 Q6(b) CLT. Other lectures unchanged.
- [2026-10-23] notes converted to PDF in notes/ and the .docx files removed; to edit a note, rerun its build_*.py (outputs .docx) and reconvert with topdf.ps1.
- [2026-10-26] trackers now list only papers 2018-19 to 2023-24 (FROM=2018 in build_tracker.py); notes still cover all years.
