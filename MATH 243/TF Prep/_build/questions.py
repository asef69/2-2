"""Master list of MATH 243 TF questions (merged PDF + 22-batch paper).

Every row was read from the page image (see questions_raw.md).
part: KKS | Stat | OUT (hypothesis testing etc., not in any deck -> KKS Outside Notes) | DROP (complex variables)
note: note-file key (see NOTES), lesson: L<n> within that part.
key: question-type key used to build "Same Type Also In".
Run: python -P questions.py  -> writes questions.json and prints counts.
"""
import json
import os
from collections import Counter, defaultdict

B22 = "22 batch p."

# (year, course, qno, marks, page, part, note, lesson, type, key, question)
Q = [
    # ---------------- 2011-12 MATH 241 ----------------
    ("2011-12", "MATH 241", "5(a),(b)", 35, 2, "DROP", "", "", "", "", "Contour integrals (complex variables)"),
    ("2011-12", "MATH 241", "6(a)", 20, 2, "Stat", "s4", "L11", "Numerical", "skew_kurt",
     "Pearson's first coefficient of skewness and kurtosis, ages 21-26…51-56 (f 83, 75, 176, 130, 92, 54); comment"),
    ("2011-12", "MATH 241", "6(b)", 15, 2, "Stat", "s3", "L9", "Numerical", "cv",
     "Time study, samples A and B of 7 workers: which is more variable, which takes less time on average"),
    ("2011-12", "MATH 241", "7(a)", 20, 2, "Stat", "s5", "L14", "Numerical", "reg_lines",
     "Two regression lines and r from 9 (X, Y) pairs (X 105…111, Y 58…55)"),
    ("2011-12", "MATH 241", "7(b)(i)", 7, 2, "KKS", "k5", "L14", "Numerical", "poisson_approx",
     "Insurance: P(death) = 0.0005, 1000 policies — P(5 or more claims)"),
    ("2011-12", "MATH 241", "7(b)(ii)", 8, 2, "KKS", "k1", "L3", "Numerical", "indep_events",
     "A, B, C solve a problem with probabilities 3/7, 2/3, 4/5 independently — P(problem solved)"),
    ("2011-12", "MATH 241", "8(a)", 17, 3, "OUT", "", "", "Numerical", "t_test",
     "Type I / Type II errors; t-test: 9 items, can the population mean be 47? (5%)"),
    ("2011-12", "MATH 241", "8(b)", 18, 3, "OUT", "", "", "Numerical", "chi_fit",
     "5 coins tossed 3200 times (heads 0…5): χ² test that the coins are unbiased"),
    # ---------------- 2012-13 MATH 241 ----------------
    ("2012-13", "MATH 241", "5", 35, 4, "DROP", "", "", "", "", "Contour integrals (complex variables)"),
    ("2012-13", "MATH 241", "6(a)", 15, 5, "Stat", "s4", "L10", "Numerical", "skew_ungrouped",
     "Runs of players A and B in 10 matches: Pearson's skewness, kurtosis and Bowley's skewness for B; who is more consistent"),
    ("2012-13", "MATH 241", "6(b)", 10, 5, "KKS", "k5", "L14", "Numerical", "binom_poisson",
     "Truck tyres, 20 % blow out, next 18: P(4 to 7), P(fewer than 3), P(more than 5) by binomial and Poisson"),
    ("2012-13", "MATH 241", "6(c)", 10, 5, "KKS", "k5", "L13", "Derivation", "binom_proof",
     "Derive the mean and variance of the binomial distribution"),
    ("2012-13", "MATH 241", "7(a)", 18, 5, "Stat", "s5", "L14", "Numerical", "reg_lines",
     "Economics vs Business marks (10 students): two regression equations and coefficients; estimates; comment on r"),
    ("2012-13", "MATH 241", "7(b)", 17, 5, "OUT", "", "", "Numerical", "chi_fit",
     "640 families with 5 children: χ² test that male and female births are equally probable"),
    ("2012-13", "MATH 241", "8(a)", 18, 5, "KKS", "k4", "L11", "Numerical", "joint_cont",
     "Joint density (6 − x − y)/k on 0<x<2, 2<y<4: find P(1 < Y < 3 | X = 2)"),
    ("2012-13", "MATH 241", "8(b)", 17, 5, "OUT", "", "", "Numerical", "two_sample_z",
     "Two supermarkets, 500 shoppers each (Tk 500, sd 80 vs Tk 440, sd 90): are mean expenditures equal? (10 %)"),
    # ---------------- 2013-14 MATH 241 ----------------
    ("2013-14", "MATH 241", "5(a),(b)", 35, 7, "DROP", "", "", "", "", "Contour integrals (complex variables)"),
    ("2013-14", "MATH 241", "6(a)", 15, 7, "Stat", "s3", "L9", "Numerical", "cv",
     "Lives of refrigerator models A and B (grouped): which model has greater uniformity"),
    ("2013-14", "MATH 241", "6(b)", 20, 7, "Stat", "s4", "L11", "Numerical", "skew_kurt",
     "Coefficients of skewness and kurtosis, classes 10-20…50-60 (f 174, 86, 32, 181, 27); comment"),
    ("2013-14", "MATH 241", "7(a)", 20, 8, "Stat", "s5", "L14", "Numerical", "reg_lines",
     "Ages of husbands and wives (8 couples): two regression equations, r; husband's age when wife is 24"),
    ("2013-14", "MATH 241", "7(b)(i)", 7, 8, "KKS", "k1", "L2", "Numerical", "comb_prob",
     "3 cards drawn without replacement: P(all from different suits)"),
    ("2013-14", "MATH 241", "7(b)(ii)", 8, 8, "KKS", "k5", "L13", "Numerical", "binomial",
     "10 % defective, 12 instruments: P(at least 4 defective)"),
    ("2013-14", "MATH 241", "8(a)", 20, 8, "OUT", "", "", "Numerical", "t_test",
     "11 tins of talcum powder: can the average packing be 0.5 lb? (t-test, 5 %)"),
    ("2013-14", "MATH 241", "8(b)", 15, 8, "OUT", "", "", "Numerical", "chi_fit",
     "320 families with 5 children: χ² test of equal male/female births"),
    # ---------------- 2014-15 MATH 241 ----------------
    ("2014-15", "MATH 241", "5(a),(b)", 35, 10, "DROP", "", "", "", "", "Contour integrals (complex variables)"),
    ("2014-15", "MATH 241", "6(a)", 17, 10, "Stat", "s2", "L7", "Numerical", "missing_freq",
     "Incomplete distribution, N = 1000, median 413.11: find the two missing frequencies and the mode"),
    ("2014-15", "MATH 241", "6(b)", 18, 10, "Stat", "s4", "L11", "Numerical", "skew_kurt",
     "Karl Pearson's skewness and β1, β2, classes 10-20…50-60 (f 18, 20, 30, 22, 10)"),
    ("2014-15", "MATH 241", "7(a)", 20, 11, "Stat", "s5", "L14", "Numerical", "reg_lines",
     "Regression lines Y on X and X on Y and r (7 pairs, X 42…66, Y 56…51)"),
    ("2014-15", "MATH 241", "7(b)", 15, 11, "OUT", "", "", "Numerical", "z_test",
     "Bulbs: claimed mean 4 years, σ 0.16; sample of 10 has mean 3.45 — is the claim justified? (5 %)"),
    ("2014-15", "MATH 241", "8(a)", 12, 11, "KKS", "k1", "L2", "Numerical", "comb_prob",
     "Box of 8 red, 3 white, 9 blue; 3 drawn: P(all red), P(2 red 1 white), P(at least 1 white)"),
    ("2014-15", "MATH 241", "8(b)", 12, 11, "KKS", "k5", "L13", "Numerical", "binomial",
     "P(graduate) = 0.4; of 5 students: P(none), P(at least 1), P(all)"),
    ("2014-15", "MATH 241", "8(c)", 11, 11, "KKS", "k6", "L16", "Numerical", "normal_prob",
     "2000 units/day, weight N(130, 10²): how many weigh less than 142 kg"),
    # ---------------- 2015-16 MATH 241 ----------------
    ("2015-16", "MATH 241", "5(a),(b)", 35, 15, "DROP", "", "", "", "", "Contour integrals (complex variables)"),
    ("2015-16", "MATH 241", "6(a)", 18, 15, "Stat", "s2", "L7", "Numerical", "missing_freq",
     "Incomplete distribution, N = 1000, median 415: missing frequencies, modal value, shape"),
    ("2015-16", "MATH 241", "6(b)", 17, 15, "Stat", "s3", "L9", "Numerical", "cv",
     "Marks of students X and Y in 10 weeks: who is the better scorer, who is more consistent"),
    ("2015-16", "MATH 241", "7(a)", 18, 15, "Stat", "s4", "L11", "Numerical", "skew_kurt",
     "Coefficients of skewness and kurtosis, classes 10-20…50-60 (f 174, 86, 32, 181, 27); comment"),
    ("2015-16", "MATH 241", "7(b)", 17, 16, "Stat", "s5", "L14", "Numerical", "reg_lines",
     "Years of service vs income (9 persons): regression equations, r; starting income for 15 years' service"),
    ("2015-16", "MATH 241", "8(a)", 13, 16, "KKS", "k2", "L5", "Numerical", "cond_simple",
     "TV show: P(man) 0.25, P(woman) 0.35, P(man | wife) 0.8: P(couple), P(husband | wife does not)"),
    ("2015-16", "MATH 241", "8(b)", 12, 16, "KKS", "k6", "L16", "Numerical", "normal_prob",
     "Normal marks: 10 % under 65, 25 % above 75 — what % lie between 60 and 74"),
    ("2015-16", "MATH 241", "8(c)", 10, 16, "OUT", "", "", "Numerical", "t_test",
     "Chocolate sales: 153.7 before; 29 stores after, mean 169.4, sd 19.7 — was advertising successful? (5 %)"),
    # ---------------- 2016-17 MATH 245 ----------------
    ("2016-17", "MATH 245", "5(a),(b)", 35, 20, "DROP", "", "", "", "", "Contour integrals (complex variables)"),
    ("2016-17", "MATH 245", "6(a)", 17, 20, "Stat", "s4", "L11", "Numerical", "skew_kurt",
     "Define skewness and kurtosis; coefficients by moments, profits 10-20…50-60 (f 18, 20, 30, 22, 10)"),
    ("2016-17", "MATH 245", "6(b)", 18, 20, "Stat", "s5", "L15", "Numerical", "reg_r2",
     "Experience X vs rating Y (5 persons): fit Y on X; SSR, SST; is the linear model adequate (R²)?"),
    ("2016-17", "MATH 245", "7(a)", 10, 20, "KKS", "k1", "L3", "Numerical", "indep_events",
     "Circuit of 4 parallel paths (0.02; 0.01–0.01; 0.01–0.01; 0.02 failure probabilities): P(circuit does not operate)"),
    ("2016-17", "MATH 245", "7(b)", 10, 21, "KKS", "k6", "L17", "Numerical", "normal_linear",
     "U-shaped part: A ~ N(10, 0.1²), B, C ~ N(2, 0.05²); gap D = A − B − C: mean, sd, P(D < 5.9)"),
    ("2016-17", "MATH 245", "7(c)", 15, 21, "KKS", "k6", "L17", "Numerical", "normal_linear",
     "1500 bearings, mean 22.40 g, sd 0.048 g; 300 samples of 36: mean and sd of x̄ (with/without replacement); counts in ranges"),
    ("2016-17", "MATH 245", "8(a)", 20, 21, "KKS", "k5", "L14", "Derivation", "poisson_derive",
     "Prove b(x; n, p) → Poisson as n → ∞, p → 0; accidents p = 0.005 over 400 days: P(exactly 1), P(at most 3)"),
    ("2016-17", "MATH 245", "8(b)", 15, 21, "OUT", "", "", "Numerical", "z_test",
     "100 deaths, mean life 61.8, σ 4.9: is the mean life span greater than 60? (5 %)"),
    # ---------------- 2018-19 MATH 245 ----------------
    ("2018-19", "MATH 245", "4(a),(b)", 35, 23, "DROP", "", "", "", "", "Contour integrals (complex variables)"),
    ("2018-19", "MATH 245", "5(a)", 15, 24, "Stat", "s3", "L9", "Numerical", "cv",
     "Shares A, B, C (average price, SD, current price): which is more stable; which to dispose of"),
    ("2018-19", "MATH 245", "5(b)", 20, 24, "Stat", "s4", "L11", "Numerical", "skew_kurt",
     "What are skewness and kurtosis? γ1 and γ2, classes 10-20…50-60 (f 18, 20, 30, 22, 10)"),
    ("2018-19", "MATH 245", "6(a)", 20, 24, "Stat", "s5", "L14", "Numerical", "reg_lines",
     "Regression of capacity utilisation on production from means, SDs and r = 0.62; production when capacity is 70"),
    ("2018-19", "MATH 245", "6(b)", 15, 24, "KKS", "k2", "L5", "Numerical", "cond_simple",
     "Picnic of 20: 5 sunburnt, 8 bitten, 10 safe: P(not bitten | sunburnt), P(sunburnt | bitten)"),
    ("2018-19", "MATH 245", "7(a)", 20, 24, "KKS", "k3", "L8", "Numerical", "cdf_pdf",
     "Density function and its conditions; F(x) = x/8, x²/16 piecewise: pdf, P(X ≥ 1.5), P(X ≥ 1 | X ≤ 3)"),
    ("2018-19", "MATH 245", "7(b)", 15, 25, "KKS", "k3", "L9", "Numerical", "expectation",
     "Lot of 7 (4 good, 3 defective), sample 3: expected number of good components"),
    ("2018-19", "MATH 245", "8(a)", 18, 25, "KKS", "k6", "L16", "Numerical", "normal_prob",
     "1000 tube lights N(120, 20²): how many fail before 90 days; replacement interval so that ≤ 10 % fail"),
    ("2018-19", "MATH 245", "8(b)", 17, 25, "OUT", "", "", "Numerical", "z_test",
     "GPA: n = 40, mean 2.8, sd 0.35 vs population 2.4 (1 %); 99 % confidence interval"),
    # ---------------- 2019-20 MATH 245 ----------------
    ("2019-20", "MATH 245", "5(a)", 10, 34, "Stat", "s3", "L9", "Numerical", "cv",
     "Coefficient of variation, profits 20-30…90-100 (f 4, 8, 18, 30, 15, 10, 8, 7)"),
    ("2019-20", "MATH 245", "5(b)", 25, 34, "Stat", "s4", "L11", "Numerical", "skew_kurt",
     "Earnings 50-70…170-190 (f 4, 8, 12, 20, 6, 7, 3): four moments about assumed mean → about mean; γ1, γ2"),
    ("2019-20", "MATH 245", "6(a)", 17, 34, "Stat", "s5", "L14", "Numerical", "reg_lines",
     "Distance to transmitter vs signal strength (10 pairs): regression of Y on X; predict at 10 m"),
    ("2019-20", "MATH 245", "6(b)", 18, 34, "OUT", "", "", "Numerical", "z_test",
     "Mice diet: 64 mice, mean 38, sd 5.8 — is μ < 40? (P-value)"),
    ("2019-20", "MATH 245", "7(a)", 17, 34, "KKS", "k2", "L6", "Numerical", "bayes",
     "Truth serum (90 % / 1 %, 5 % guilty): P(innocent | serum says guilty)"),
    ("2019-20", "MATH 245", "7(b)", 18, 35, "KKS", "k3", "L9", "Numerical", "exp_function",
     "f(x) = e^{−x}, x > 0: expected value of g(X) = e^{2X/3}"),
    ("2019-20", "MATH 245", "8(a)", 10, 35, "KKS", "k5", "L14", "Numerical", "poisson_approx",
     "Bubbles in glass, 1 in 1000; sample of 8000: P(fewer than 7) (Poisson approximation)"),
    ("2019-20", "MATH 245", "8(b)", 25, 35, "KKS", "k3", "L8", "Numerical", "exponential",
     "Fire-station calls, exponential with rate 1.8/day: five parts (15-min call, memoryless, 10-h shift, 4 shifts, 10 % point)"),
    # ---------------- 2020-21 MATH 245 ----------------
    ("2020-21", "MATH 245", "5(a)", 10, 37, "Stat", "s3", "L9", "Numerical", "cv",
     "Daily wages of factories A and B (grouped): higher average wage; greater variability"),
    ("2020-21", "MATH 245", "5(b)", 15, 37, "Stat", "s4", "L10", "Numerical", "bowley_kelly",
     "Weights 30-40…80-90 (f 18, 37, 45, 27, 15, 8): Bowley's and Kelly's skewness; merits and drawbacks"),
    ("2020-21", "MATH 245", "5(c)", 10, 37, "KKS", "k4", "L10", "Numerical", "joint_cont",
     "Tyre pressures f = k(x² + y²), 30 ≤ x, y < 50: k; P(30 ≤ X ≤ 40, 40 ≤ Y < 50); P(both underfilled)"),
    ("2020-21", "MATH 245", "6(a)", 15, 37, "Stat", "s5", "L15", "Numerical", "reg_r2",
     "Experience X vs rating Y (5 persons): fit Y on X; SSR and SST"),
    ("2020-21", "MATH 245", "6(b)", 10, 38, "KKS", "k3", "L8", "Numerical", "cdf_pdf",
     "Measurement error f = k(3 − x)², −1 ≤ x ≤ 1: k; P(X < 1/2); P(|X| > 0.8)"),
    ("2020-21", "MATH 245", "6(c)", 10, 38, "KKS", "k5", "L15", "Numerical", "geometric",
     "Valium, 2/3 of users women: 5th prescription is the first / the third for a woman"),
    ("2020-21", "MATH 245", "7(a)", 17, 38, "KKS", "k5", "L13", "Numerical", "binomial",
     "Diode failure 0.03, 200 diodes: mean, variance, P(board works = no failures)"),
    ("2020-21", "MATH 245", "7(b)", 18, 38, "KKS", "k6", "L16", "Numerical", "normal_prob",
     "Mice lifetimes N(40, 6.3²): P(> 32 months), P(37 to 49 months)"),
    ("2020-21", "MATH 245", "8(a)", 10, 38, "KKS", "k3", "L9", "Numerical", "exp_function",
     "Hospital stay Y = X + 4, f(x) = 32/(x + 4)³, x > 0: average stay E(Y)"),
    ("2020-21", "MATH 245", "8(b)", 15, 39, "OUT", "", "", "Numerical", "t_test",
     "Cereal sodium: n = 20, mean 244, sd 24.5 — is μ > 220? (5 %)"),
    ("2020-21", "MATH 245", "8(c)", 10, 39, "OUT", "", "", "Theory", "type_errors",
     "DNA paternity testing: describe Type I and Type II errors"),
    # ---------------- 2021-22 MATH 245 ----------------
    ("2021-22", "MATH 245", "5(a)", 18, 44, "Stat", "s2", "L6", "Numerical", "ogive_median",
     "Monthly wages 1900-2400 (7 classes): suitable diagram, median from graph and formula; workers earning 2000–2170"),
    ("2021-22", "MATH 245", "5(b)", 17, 44, "Stat", "s1", "L2", "Theory", "freq_table",
     "(i) 34 observations 201–337, 7 classes of width 20 from 199.5: class limits and marks; (ii) same mean, SD, skewness — kurtosis"),
    ("2021-22", "MATH 245", "6(a)", 10, 44, "KKS", "k5", "L15", "Numerical", "hypergeom",
     "500 lottery tickets, 200 pay off; buy 5: P(win back at least the cost of 3)"),
    ("2021-22", "MATH 245", "6(b)", 10, 44, "KKS", "k5", "L15", "Numerical", "multinomial",
     "Delegates by air/bus/auto/train (0.4, 0.2, 0.3, 0.1): P(3, 3, 1, 2 among 9)"),
    ("2021-22", "MATH 245", "6(c)", 15, 44, "KKS", "k5", "L15", "Numerical", "hypergeom",
     "5 cars, 2 blemished; agency receives 3: probability distribution and F(x) of the number blemished"),
    ("2021-22", "MATH 245", "7(a)", 20, "44–45", "Stat", "s5", "L14", "Numerical", "reg_lines",
     "Loblolly pines (15): specific gravity vs modulus of rupture — both regression coefficients; r and interpretation"),
    ("2021-22", "MATH 245", "7(b)", 15, 45, "KKS", "k6", "L16", "Numerical", "normal_prob",
     "Ball bearings 3.0 ± 0.01 cm, N(3.0, 0.005²): how many are scrapped"),
    ("2021-22", "MATH 245", "8(a)", 17, 45, "OUT", "", "", "Numerical", "t_test",
     "Heights of 10 individuals: is the mean height 65? (t9 = 2.262)"),
    ("2021-22", "MATH 245", "8(b)", 18, 45, "KKS", "k7", "L18", "Numerical", "anova1",
     "Salesmen A, B, C weekly sales: one-way ANOVA (F(2,11) = 3.98)"),
    # ---------------- 2022-23 MATH 243 ----------------
    ("2022-23", "MATH 243", "1(a)", 8, 47, "KKS", "k2", "L6", "Numerical", "transfer",
     "Bag 1 (4W, 3B) → one ball moved unseen to bag 2 (3W, 5B): P(black from bag 2)"),
    ("2022-23", "MATH 243", "1(b)", 15, 47, "KKS", "k2", "L6", "Numerical", "bayes",
     "Machines B1, B2, B3 (30/45/25 %, defective 2/3/2 %): P(Bi | defective)"),
    ("2022-23", "MATH 243", "1(c)", 12, 47, "KKS", "k3", "L8", "Numerical", "exponential",
     "DVD component f = (1/2000)e^{−x/2000}: CDF; P(lasts > 1000 h); P(fails before 2000 h)"),
    ("2022-23", "MATH 243", "2(a)", 15, 47, "KKS", "k4", "L11", "Numerical", "joint_cont",
     "f(x, y) = 10xy², 0 < x < y < 1: g(x), h(y), f(y|x); P(Y > 1/2 | X = 0.25)"),
    ("2022-23", "MATH 243", "2(b)", 10, 48, "KKS", "k3", "L9", "Numerical", "exp_function",
     "Clearance time Y = 3X − 2, X with f = (1/4)e^{−x/4}: mean and variance of Y"),
    ("2022-23", "MATH 243", "2(c)", 10, 48, "KKS", "k3", "L9", "Numerical", "chebyshev",
     "f = 6x(1 − x): P(μ − 2σ < X < μ + 2σ) compared with Chebyshev"),
    ("2022-23", "MATH 243", "3(a)", 10, 48, "KKS", "k5", "L14", "Derivation", "poisson_derive",
     "Bernoulli and Poisson processes; derive the Poisson distribution"),
    ("2022-23", "MATH 243", "3(b)", 12, 48, "KKS", "k5", "L14", "Numerical", "poisson_approx",
     "Variance of Poisson; 1 in 1000 returns has an error, 10,000 examined: P(6, 7 or 8 errors)"),
    ("2022-23", "MATH 243", "3(c)", 13, 48, "KKS", "k6", "L16", "Numerical", "normal_prob",
     "Lawyer's trip N(24, 3.8²): P(≥ 30 min), % late, slowest 15 %, P(2 of next 3 trips ≥ 30 min)"),
    ("2022-23", "MATH 243", "4(a)", 10, 48, "KKS", "k6", "L16", "Derivation", "normal_theory",
     "Properties of the normal curve; mean, mode and SD of the normal; mean and variance of the standard normal"),
    ("2022-23", "MATH 243", "4(b)", 12, 48, "Stat", "s5", "L13", "Numerical", "rank_corr",
     "Correlation vs regression; rank correlation, Bangla vs English marks of 8 applicants (ties)"),
    ("2022-23", "MATH 243", "4(c)", 13, 49, "Stat", "s5", "L14", "Numerical", "reg_lines",
     "Ages of 10 husbands and wives: two regression equations; husband at wife 30, wife at husband 25; comment on r"),
    ("2022-23", "MATH 243", "5(a)", 10, 49, "Stat", "s1", "L1", "Theory", "stat_data",
     "Statistical data: meaning, how produced, why needed, sources in Bangladesh"),
    ("2022-23", "MATH 243", "5(b)", 15, 49, "Stat", "s1", "L2", "Design", "freq_table",
     "Insulation thickness (60 values): frequency table by Sturges' rule; histogram and cumulative frequency graph"),
    ("2022-23", "MATH 243", "5(c)", 10, 49, "Stat", "s3", "L9", "Numerical", "cv",
     "Bulb lives, companies A and B (grouped): which company's bulbs to prefer"),
    ("2022-23", "MATH 243", "6(a)", 10, 50, "Stat", "s4", "L11", "Theory", "define_measures",
     "Define and illustrate SD, variance, skewness, kurtosis, moments"),
    ("2022-23", "MATH 243", "6(b)", 10, 50, "Stat", "s1", "L4", "Design", "stem_leaf",
     "Lengths of 12 pencils: stem-and-leaf plot; median, mode, range"),
    ("2022-23", "MATH 243", "6(c)", 15, 50, "Stat", "s4", "L11", "Numerical", "skew_kurt",
     "Profits 10-20…50-60 (f 18, 20, 30, 22, 10): four moments about assumed mean → about mean; γ1, γ2"),
    ("2022-23", "MATH 243", "7(a)", 10, 50, "OUT", "", "", "Theory", "test_concepts",
     "Differentiate: statistic/parameter, critical/acceptance region, exact/inexact hypothesis, uni/non-directional test, level of significance/p-value"),
    ("2022-23", "MATH 243", "7(b)", 12, 50, "OUT", "", "", "Numerical", "z_test",
     "GPA: n = 40, mean 2.8, sd 0.35 vs 2.4; 99 % CI"),
    ("2022-23", "MATH 243", "7(c)", 13, 50, "OUT", "", "", "Numerical", "t_test",
     "Bank waiting time: n = 12, mean 42, sd 11.9 — is μ < 50? (t11 = 1.796)"),
    ("2022-23", "MATH 243", "8(a)", 10, 50, "OUT", "", "", "Numerical", "chi_indep",
     "Drug vs typhoid 2×2 table: χ² test of effectiveness (χ²1 = 3.84)"),
    ("2022-23", "MATH 243", "8(b)", 10, 51, "KKS", "k7", "L18", "Numerical", "anova1",
     "Lifetimes of 4 brands of bulbs (3 each): one-way ANOVA at 5 % and 1 %"),
    ("2022-23", "MATH 243", "8(c)", 15, 51, "KKS", "k7", "L19", "Numerical", "anova2",
     "Four corn types in five blocks: two-way ANOVA for blocks and corn types (5 %)"),
    # ---------------- 2023-24 MATH 243 (22 batch paper) ----------------
    ("2023-24", "MATH 243", "1(a)", 6, B22 + "1", "KKS", "k1", "L3", "Theory", "indep_events",
     "Can two events be mutually exclusive and independent at the same time? Justify"),
    ("2023-24", "MATH 243", "1(b)", 12, B22 + "1", "KKS", "k2", "L6", "Numerical", "transfer",
     "Multiplication law; box A (5W, 7R) → one ball moved to box B (3W, 8R): P(red from B)"),
    ("2023-24", "MATH 243", "1(c)", 17, B22 + "1", "KKS", "k2", "L6", "Numerical", "bayes",
     "Party support 45/40/15 %, turnout 65/80/50 %: P(A), P(B), P(C) | did not vote"),
    ("2023-24", "MATH 243", "2(a)", 15, B22 + "1", "KKS", "k3", "L8", "Numerical", "exponential",
     "F(x) = 1 − e^{−8x}: P(wait < 12 minutes) using the CDF and using the pdf"),
    ("2023-24", "MATH 243", "2(b)", 20, B22 + "1", "KKS", "k4", "L10", "Numerical", "joint_discrete",
     "Pens 3 red, 2 blue, 3 black, choose 2: joint pmf plot, P(X + Y ≤ 1), marginals, Var(X), Cov(X, Y)"),
    ("2023-24", "MATH 243", "3(a)", 11, B22 + "2", "KKS", "k3", "L9", "Numerical", "chebyshev",
     "Chebyshev's theorem; 70 jobs, 1000 applicants, mean 60, sd 6: can a score of 84 get a job?"),
    ("2023-24", "MATH 243", "3(b)", 12, B22 + "2", "KKS", "k5", "L14", "Derivation", "poisson_derive",
     "Relation between binomial and Poisson; 0.5 calls/min: P(2 calls in 5 minutes)"),
    ("2023-24", "MATH 243", "3(c)", 12, B22 + "2", "KKS", "k5", "L13", "Numerical", "binomial",
     "P(recover) 0.4, 15 patients: P(at least 10 survive), P(3 to 8 survive), P(exactly 5 die)"),
    ("2023-24", "MATH 243", "4(a)", 11, B22 + "2", "KKS", "k6", "L16", "Numerical", "normal_theory",
     "Show mode of normal = μ; bulbs N(800, 40²): P(778 < X < 834)"),
    ("2023-24", "MATH 243", "4(b)", 12, B22 + "2", "Stat", "s5", "L13", "Numerical", "rank_corr",
     "Pearson's r; rank correlation with repeated ranks — sales and expenses of 10 stores"),
    ("2023-24", "MATH 243", "4(c)", 12, B22 + "2", "Stat", "s5", "L15", "Numerical", "reg_r2",
     "Objectives of correlation/regression; second-degree polynomial for nitrogen vs yield; coefficient of determination"),
    ("2023-24", "MATH 243", "5(a)", 10, B22 + "3", "Stat", "s1", "L4", "Design", "stem_leaf",
     "What is a stem-and-leaf plot; how to create one, with an example"),
    ("2023-24", "MATH 243", "5(b)", 13, B22 + "3", "Stat", "s5", "L12", "Design", "scatter",
     "Scatter plot of price vs rating for 5 restaurants; is there a relationship?"),
    ("2023-24", "MATH 243", "5(c)", 12, B22 + "3", "Stat", "s3", "L9", "Numerical", "corrected",
     "Mean 60, SD 20 of 200 items; 3 and 67 taken instead of 13 and 17: corrected mean, SD, CV"),
    ("2023-24", "MATH 243", "6(a)", 13, B22 + "3", "Stat", "s4", "L11", "Numerical", "skew_kurt",
     "Marks 0-10…60-70 (f 8, 12, 20, 30, 15, 10, 5): four central moments, β1, β2; comment"),
    ("2023-24", "MATH 243", "6(b)", 10, B22 + "3", "OUT", "", "", "Theory", "clt",
     "Central limit theorem: meaning, algorithm, applications in computer science"),
    ("2023-24", "MATH 243", "6(c)", 12, B22 + "3", "OUT", "", "", "Numerical", "z_test",
     "Stratified random sampling (example); delivery time claim < 120 min, σ 30, n 49, mean 100 (z = −1.645)"),
    ("2023-24", "MATH 243", "7(a)", 10, B22 + "3", "OUT", "", "", "Theory", "test_concepts",
     "Short notes: goodness of fit, one-/two-tailed tests, degrees of freedom, null/alternative hypothesis"),
    ("2023-24", "MATH 243", "7(b)", 12, B22 + "3", "OUT", "", "", "Numerical", "two_prop",
     "Machine: 16/500 imperfect before, 3/100 after overhaul — improved? (1 %)"),
    ("2023-24", "MATH 243", "7(c)", 13, B22 + "4", "OUT", "", "", "Numerical", "two_sample_t",
     "Two samples of 8 and 7 weights: is the difference of means significant? (t13 = 2.16)"),
    ("2023-24", "MATH 243", "8(a)", 15, B22 + "4", "OUT", "", "", "Numerical", "chi_indep",
     "Education vs job performance 3×3 table, 200 employees: χ² test (χ²0.05,4 = 9.49)"),
    ("2023-24", "MATH 243", "8(b)", 20, B22 + "4", "KKS", "k7", "L18", "Numerical", "anova1",
     "Retail prices in 3 cities (4 shops each): one-way ANOVA (F0.05(2, 9) = 4.26)"),
]

FIELDS = ["year", "course", "qno", "marks", "page", "part", "note", "lesson", "type", "key", "question"]


# Lecture-13-20- Hypothesis.pdf (added later) now covers inference: those questions join the KKS part (note k8).
HYP_LESSON = {"type_errors": "L20", "test_concepts": "L20", "z_test": "L21", "t_test": "L21",
              "two_sample_z": "L22", "two_sample_t": "L22", "two_prop": "L23",
              "chi_fit": "L24", "chi_indep": "L24"}


def rows():
    out = []
    for r in Q:
        d = dict(zip(FIELDS, r))
        if d["part"] == "OUT" and d["key"] in HYP_LESSON:
            d["part"], d["note"], d["lesson"] = "KKS", "k8", HYP_LESSON[d["key"]]
        out.append(d)
    return out


def same_type(rows_):
    by = defaultdict(list)
    for r in rows_:
        if r["key"]:
            by[r["key"]].append(r)
    for r in rows_:
        others = [o for o in by.get(r["key"], []) if o is not r]
        others.sort(key=lambda o: o["year"], reverse=True)
        r["same_type"] = "; ".join(f"{o['year']} {o['qno']}" for o in others) or "—"
    return rows_


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    rs = same_type(rows())
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "questions.json"), "w", encoding="utf-8") as f:
        json.dump(rs, f, ensure_ascii=False, indent=1)
    c = Counter((r["year"], r["part"]) for r in rs)
    for y in sorted({r["year"] for r in rs}):
        print(y, {p: c[(y, p)] for p in ("KKS", "Stat", "OUT", "DROP") if c[(y, p)]},
              "marks KKS+Stat+OUT =", sum(r["marks"] for r in rs if r["year"] == y and r["part"] != "DROP"))
    print("total", Counter(r["part"] for r in rs))
