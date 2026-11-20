"""MATH243_KKS_Hypothesis_Testing_Notes.docx — Lecture-13-20- Hypothesis.pdf (L20–L24)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy import stats

from common import exam_map, new
from m243 import PROB, g, table_phi

H = PROB + r"\Lecture-13-20- Hypothesis.pdf"
N_, T_, C_ = stats.norm, stats.t, stats.chi2
P2 = lambda z: 2 * N_.sf(abs(z))


def tc(a, df):
    return float(T_.ppf(1 - a, df))


n = new("KKS", "Tests of Hypothesis: z-test, t-test, Two-sample and Paired Tests, Proportions, Correlation, χ²",
        "MATH243_KKS_Hypothesis_Testing_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "a test of hypothesis in every paper"),
              ("Lesson 20 — Concepts: Hypotheses, Errors, Level of Significance, p-value", "H0/H1, tails, Type I/II, test statistics"),
              ("Lesson 21 — One-sample Tests of a Mean (z and t) and Confidence Intervals", "σ known / large n / small n"),
              ("Lesson 22 — Two-sample and Paired Tests of Means", "z, pooled t, Welch t, paired t, F"),
              ("Lesson 23 — Tests for a Correlation Coefficient and for Proportions", "t for r, one- and two-proportion z"),
              ("Lesson 24 — χ² Tests: Contingency Tables and Goodness of Fit", "r × p, 2 × 2, fit to a distribution"),
              ("Quick Notes — Tests of Hypothesis", "revision bullets")],
    source_note="Page numbers refer to KKS Sir's Lecture-13-20- Hypothesis.pdf (44 pp.), written as Hyp p. n. This lecture "
                "was added after the first version of these notes; it now covers the inference questions that were "
                "previously listed under Outside Notes. Goodness-of-fit χ² and the unpooled Welch degrees of freedom are "
                "only sketched in the lecture and are completed from the textbook (marked). Critical values are from the "
                "t, F, χ² and z tables in the course folder (or as printed on the paper). \"TF p.\" = merged question PDF "
                "page; \"22 batch p.\" = 2023-24 paper.")

n.h1("Exam Map — What the TF Papers Ask")
st = exam_map(n, "k8")
n.callout("focus", f"{st['n']} questions, {st['marks']} marks ({st['n_hi']} questions and {st['marks_hi']} marks since 2019-20). "
          "Every paper from 2011-12 on has one 10–20 mark test: a one-sample z or t test (most often), a χ² test (2011-12, "
          "2012-13, 2013-14, 2022-23, 2023-24), a two-sample test or a two-proportion test (2023-24). Learn the 5-step "
          "layout — hypotheses, α, test statistic, critical region, decision — and choose the test by the three "
          "questions: is σ known? is n large (≥ 30)? one sample or two?")

# ------------------------------------------------------------------ L20
n.lesson("Lesson 20 — Concepts: Hypotheses, Errors, Level of Significance, p-value", "Hyp pp. 1–6, 11–12")
n.h2("1. Hypothesis, Null and Alternative (pp. 1–2)")
n.p("A **statistical hypothesis** is a statement or assumption about a parameter, written H. The **null hypothesis** H_{0} "
    "is the hypothesis stated for possible rejection, assumed true until the data show otherwise; the **alternative "
    "hypothesis** H_{1} is the contrary statement. For a sample from f(x, θ): H_{0}: θ = θ_{0} versus H_{1}: θ ≠ θ_{0}, where θ_{0} "
    "is the specified (null) value.")
n.h2("2. Critical (Rejection) Region and Tails (pp. 2–4)")
n.p("Split the sample space S into w and S − w. If the sample point falls in w, reject H_{0} — w is the **critical (rejection) "
    "region**; S − w is the **acceptance region**.")
n.bullets(["**Two-tailed** test: critical region at both ends — H_{1}: μ ≠ μ_{0}.",
           "**One-tailed** test: critical region at one end — right tail H_{1}: μ > μ_{0}, left tail H_{1}: μ < μ_{0}.",
           "Put the claim you need evidence for in H_{1} (e.g. \"proportion defective is at most 3 %\": H_{0}: p = 0.03, H_{1}: p < 0.03; "
           "\"users increased\": H_{0}: μ_{2} − μ_{1} = 0, H_{1}: μ_{2} − μ_{1} > 0)."])
n.figure_from_pdf(H, 3, "Figure 20.1 — Acceptance and rejection regions of one-tailed and two-tailed tests (Hyp p. 3)",
                  clip=(0.10, 0.10, 0.92, 0.31), width_cm=11)
n.h2("3. Type I and Type II Errors, Level of Significance (p. 4)")
n.table(["Decision", "H_{0} true", "H_{0} false"],
        [["Accept H_{0}", "no error", "Type II error (β)"], ["Reject H_{0}", "Type I error (α)", "no error"]],
        widths_cm=[4, 6, 7.2])
n.formula(["α = P(reject H_{0} | H_{0} is true) = level of significance;   β = P(accept H_{0} | H_{0} is false)"])
n.p("A Type I error (convicting an innocent defendant, operating on a patient who does not need surgery) is usually the more "
    "serious, so tests are designed with P(Type I) ≤ a small pre-assigned α (0.10, 0.05, 0.01); then the Type II error is "
    "made as small as possible. A low α needs a lot of evidence to reject H_{0}.")
n.callout("answer", "DNA paternity (2020-21 Q8(c)). H_{0}: the man is the father; H_{a}: he is not. **Type I error**: rejecting "
          "H_{0} when it is true — concluding \"not the father\" for the real father. Since the test is 99.9 % accurate when he "
          "is the father, this happens with probability about 0.001 (a false exclusion). **Type II error**: accepting H_{0} when "
          "it is false — concluding \"is the father\" for a man who is not. The test is 100 % accurate in that case, so "
          "this error has probability 0 (a false match cannot occur).")
n.h2("4. Test Statistic and the Four Tests (pp. 5–7)")
n.formula("Test statistic = (observed value − expected value under H_{0}) / standard error")
n.table(["Test", "Statistic", "Use"],
        [["Normal (z)", "z = (u − E(u))/σ(u) ~ N(0, 1)", "σ known, or estimated from a large sample (n ≥ 30)"],
         ["t", "t = (u − E(u))/σ̂(u) ~ t_{ν}", "σ unknown, small sample (n < 30), normal population"],
         ["χ²", "Σ (O − E)²/E ~ χ²_{ν}", "distribution as a whole; independence of attributes"],
         ["F", "F = S_{1}²/S_{2}² ~ F_{ν1, ν2}", "equality of two variances (upper tail only) — ANOVA note"]], widths_cm=[2.6, 6.6, 8])
n.h2("5. p-value (pp. 11–12)")
n.p("The **p-value** is the probability, assuming H_{0} is true, of a test statistic as extreme as, or more extreme than, the one "
    "observed. Decision: p ≤ α → reject H_{0}; p > α → do not reject.")
n.formula(["right tail: p = P(Z ≥ z_{cal}) = 1 − Φ(z_{cal});  left tail: p = P(Z ≤ z_{cal})",
           "two-tailed: p = 2 P(Z ≥ |z_{cal}|) = 2[1 − Φ(|z_{cal}|)]"])
n.p("Bulb example: z_{cal} = −3.35 → p = 2(1 − 0.9996) = 0.0008 < 0.05 → reject.")
n.callout("answer", "Short notes (2022-23 Q7(a), 2023-24 Q7(a)). **Statistic vs parameter**: a statistic is a numerical "
          "summary of a sample (x̄, s); a parameter is a numerical characteristic of the population (μ, σ). **Critical vs "
          "acceptance region**: the set of sample values for which H_{0} is rejected, and its complement. **Exact vs inexact "
          "hypothesis**: an exact (simple) hypothesis fixes the parameter completely (μ = 50); an inexact (composite) one "
          "specifies a range (μ > 50, μ ≠ 50). **Unidirectional vs non-directional test**: one-tailed (H_{1}: μ > μ_{0} or "
          "μ < μ_{0}; rejection region in one tail) versus two-tailed (H_{1}: μ ≠ μ_{0}; both tails, α/2 each). **Level of "
          "significance vs p-value**: α is the pre-chosen maximum probability of a Type I error; the p-value is computed "
          "from the data — the smallest α at which H_{0} would be rejected. **Goodness of fit**: a χ² test of whether "
          "observed frequencies agree with those expected from a specified distribution. **Degrees of freedom**: the "
          "number of independent values free to vary in a statistic (n − 1 for the t-test of a mean, (r − 1)(p − 1) for a "
          "contingency table, k − 1 − m for goodness of fit with m estimated parameters).")
n.exam_approach(["Define the parameter and write H_{0} (with =) and H_{1}; the direction of H_{1} sets the tail.",
                 "Fix α; choose the test (z or t, one or two samples) and its critical value(s).",
                 "Compute the test statistic; compare with the critical value (or compute p).",
                 "Decide, then state the conclusion in the words of the problem."])
n.practice("Lesson 20", "(a) Actual — 2020-21 Q8(c) (TF p. 39). (b) Actual — 2022-23 Q7(a) (TF p. 50). (c) Actual — 2023-24 Q7(a) (22 batch p. 3).",
           ["(a) In a paper on DNA paternity testing: \"The test is 100 % accurate if the man is not the father and 99.9 % "
            "accurate if he is.\" Consider H_{0}: a particular man is the father against H_{a}: he is not. Describe Type I and Type II errors "
            "in this context.  (10)",
            "(b) Differentiate: (i) statistic and parameter, (ii) critical region and acceptance region, (iii) exact and inexact "
            "hypothesis, (iv) unidirectional and non-directional test, (v) level of significance and p-value.  (10)",
            "(c) Write short notes on goodness of fit, one-tailed and two-tailed tests, degrees of freedom, null and alternative hypothesis.  (10)"])
n.solution()
n.answer("(a)–(c)", "Model answers are the EXAM-READY ANSWER boxes of §3 and §5; for (c) add the goodness-of-fit paragraph of "
         "Lesson 24 §4 and the tail figure of §2.")

# ------------------------------------------------------------------ L21
n.lesson("Lesson 21 — One-sample Tests of a Mean (z and t) and Confidence Intervals", "Hyp pp. 7–16")
n.h2("1. σ Known, or Estimated from a Large Sample (n ≥ 30): z-test (pp. 7–13)")
n.p("Assumptions: random sample from a normal population (or n large); σ known, or s from a large sample.")
n.formula(["z = (x̄ − μ_{0})/(σ/√n)  [σ known],   z = (x̄ − μ_{0})/(s/√n)  [σ estimated, n ≥ 30]",
           "s² = [Σx² − n x̄²]/(n − 1)"])
n.table(["H_{1}", "Reject H_{0} if (α = 0.05)", "Reject H_{0} if (α = 0.01)"],
        [["μ > μ_{0}", "z > 1.645 (1.64)", "z > 2.33"], ["μ < μ_{0}", "z < −1.645", "z < −2.33"],
         ["μ ≠ μ_{0}", "|z| > 1.96", "|z| > 2.58"]], widths_cm=[3.6, 6.8, 6.8])
n.formula("100(1 − α)% CI for μ:  x̄ ± z_{α/2} σ/√n   (95 %: x̄ ± 1.96σ/√n;  99 %: x̄ ± 2.58σ/√n)")
n.p(f"Example 1 (pp. 9–10): bulbs claimed μ = 3 years, σ² = 0.5, n = 35, x̄ = 2.6: z = (2.6 − 3)/(0.7071/√35) = "
    f"{g((2.6-3)/(math.sqrt(.5)/math.sqrt(35)),3)} < −1.96 → reject; 95 % CI = 2.6 ± 1.96(0.1195) = (2.366, 2.834). "
    f"Example 2 (p. 12): IQ of 64 women, x̄ = 115.5, s = 20, H_{{1}}: μ > 110, α = 0.01: z = 5.5/2.5 = 2.2 < 2.33 → do not reject.")
n.h2("2. σ Unknown, Small Sample (n < 30): t-test (pp. 14–16)")
n.formula(["t = (x̄ − μ_{0})/(s/√n) ~ t_{n−1};   CI: x̄ ± t_{α/2, n−1} s/√n",
           "two-tailed: reject if |t| > t_{α/2, n−1};  right: t > t_{α, n−1};  left: t < −t_{α, n−1}"])
prod = [40, 35, 48, 43, 35, 39, 44, 37, 42, 38]
tp = stats.ttest_1samp(prod, 20)
n.p(f"Example (p. 15): 10 workers' production {prod}, claimed μ = 20: x̄ = {g(np.mean(prod),1)}, s = {g(np.std(prod,ddof=1),3)}, "
    f"t = {g(tp.statistic,3)} > t_{{0.025, 9}} = 2.262 → reject; the claim is false.")
n.callout("trap", "The test statistic uses s with divisor n − 1 (not n). If n ≥ 30 (or σ is given), use z; the paper's "
          "\"given t\" or \"necessary chart\" tells you which table it expects. State the d.f. whenever you use t.")
n.p("Lecture exercises — answers: (1) steel wire, σ = 150, n = 25, x̄ = 1312, H_{1}: μ > 1250, α = 0.01: z = 62/30 = 2.07 < 2.33 → do "
    "not reject. (2) scrap, σ = 1.6, n = 10, x̄ = 23.9, H_{1}: μ < 25.5: z = −1.6/0.506 = −3.16 < −2.33 → reject (modification works). "
    "(3) users, σ = 800, n = 100, x̄ = 5200: z = 2.5 > 1.645 → reject (increased). (4) steel wire, n = 25, x̄ = 110, s² = 144, μ_{0} = 120: "
    "t = −10/(12/5) = −4.17, |t| > t_{0.025, 24} = 2.064 → reject.")
n.exam_approach(["Parameter, H_{0}, H_{1}, α (as given).",
                 "Test: z if σ is known or n ≥ 30; t (n − 1 d.f.) if σ is unknown and n < 30.",
                 "Critical region for the tail of H_{1}; compute the statistic with all steps shown.",
                 "Decision and a conclusion in context; add the CI if asked (use the same table value as the test)."])
# data
d_tins = [0.44, 0.51, 0.49, 0.52, 0.45, 0.48, 0.46, 0.45, 0.47, 0.45, 0.47]
d_t9 = [50, 48, 49, 53, 52, 47, 45, 46, 51]
d_h = [63, 63, 64, 65, 66, 69, 69, 70, 70, 71]


def tline(x, mu0, tab_val, ddof_note=""):
    x = np.array(x, float); m, s, k = x.mean(), x.std(ddof=1), len(x)
    t = (m - mu0) / (s / math.sqrt(k))
    return m, s, k, t


m1, s1, k1, t1 = tline(d_t9, 47, 3.355)
m2, s2, k2, t2 = tline(d_tins, 0.5, 2.23)
m3, s3, k3, t3 = tline(d_h, 65, 2.262)
z14 = (3.45 - 4) / (0.16 / math.sqrt(10))
z16 = (61.8 - 60) / (4.9 / 10)
z18 = (2.8 - 2.4) / (0.35 / math.sqrt(40)); se18 = 0.35 / math.sqrt(40)
z19 = (38 - 40) / (5.8 / 8)
t20 = (244 - 220) / (24.5 / math.sqrt(20))
t15 = (169.4 - 153.7) / (19.7 / math.sqrt(29))
t22 = (42 - 50) / (11.9 / math.sqrt(12))
z24 = (100 - 120) / (30 / 7)
n.practice("Lesson 21",
           "(a) Actual — 2019-20 Q6(b) (TF p. 34). (b) Actual — 2016-17 Q8(b) (TF p. 21). (c) Actual — 2014-15 Q7(b) (TF p. 11). "
           "(d) Actual — 2018-19 Q8(b) = 2022-23 Q7(b) (TF pp. 25, 50). (e) Actual — 2020-21 Q8(b) (TF p. 39). (f) Actual — 2015-16 Q8(c) (TF p. 16). "
           "(g) Actual — 2022-23 Q7(c) (TF p. 50). (h) Actual — 2023-24 Q6(c) (22 batch p. 3). (i) Actual — 2021-22 Q8(a) (TF p. 45). "
           "(j) Actual — 2013-14 Q8(a) (TF p. 8). (k) Actual — 2011-12 Q8(a) (TF p. 3).",
           ["(a) A student claims that mice on a vitamin- and protein-enriched diet live about 40 months. 64 such mice have a mean "
            "life of 38 months with s = 5.8. Is there reason to believe μ < 40? Use a P-value in your conclusion.  (18)",
            "(b) A random sample of 100 recorded deaths in Bangladesh showed an average life span of 61.8 years. Assuming σ = 4.9 years, "
            "does this indicate that the mean life span is greater than 60? Use α = 0.05.  (15)",
            "(c) A bulb manufacturer claims an average life of 4 years with σ = 0.16 years. A random sample of 10 bulbs has a mean of 3.45 "
            "years. Does the sample justify the claim? Use α = 5 %.  (15)",
            "(d) The mean and SD of GPA scores of a random sample of 40 students were 2.8 and 0.35. Can we conclude that the sample comes from "
            "a group with mean 2.4? Use α = 1 % (z = ±2.58) and compute the 99 % confidence interval for the population mean.  (17 / 12)",
            "(e) A random sample of 20 servings of a cereal has mean sodium content 244 mg and SD 24.5 mg. At α = 0.05, is the "
            "average sodium content greater than 220 mg?  (15)",
            "(f) Mean weekly sale was 153.7 bars per store; after an advertising campaign the mean in 29 stores was 169.4 with SD 19.7. "
            "Was the campaign successful? α = 5 %.  (10)",
            "(g) The average waiting time to cash a cheque has been 50 minutes. A new procedure: 12 customers, mean 42 minutes, SD 11.9. Test, at 5 %, "
            "that the mean is now less than 50 (normal; t_{0.05} = 1.796 for ν = 11).  (13)",
            "(h) An online medicine shop claims a mean delivery time below 120 minutes with σ = 30. 49 orders have mean 100 minutes. Test at 0.05 "
            "(z = −1.645).  (12)",
            "(i) Heights (inches) of ten individuals: 63, 63, 64, 65, 66, 69, 69, 70, 70, 71. Discuss the suggestion that the mean height of "
            "the universe is 65 (t_{9, 0.05} = 2.262).  (17)",
            "(j) 11 tins of talcum powder weigh (lb) 0.44, 0.51, 0.49, 0.52, 0.45, 0.48, 0.46, 0.45, 0.47, 0.45, 0.47. Can the average "
            "packing be taken as 0.5 lb at 5 % (t = ±2.23)?  (20)",
            "(k) Explain Type I and Type II errors. Nine items had values 50, 48, 49, 53, 52, 47, 45, 46, 51: can this sample be regarded as "
            "from a population with mean 47 at the 5 % level (given for ν = 8, t = 3.355)?  (17)"])
n.solution()


def five(lab, hyp, alpha, stat, crit, dec, concl):
    n.answer(lab, "")
    n.code([f"H0: {hyp[0]}   H1: {hyp[1]}   α = {alpha}", f"Test statistic: {stat}", f"Critical region: {crit}", f"Decision: {dec}"])
    n.p("Conclusion: " + concl)


five("(a)", ("μ = 40", "μ < 40"), "0.05",
     f"n = 64 ≥ 30 → z = (38 − 40)/(5.8/√64) = −2/0.725 = {g(z19,3)}", "z < −1.645",
     f"p-value = P(Z ≤ {g(z19,2)}) = {g(N_.cdf(z19),4)} < 0.05 → reject H0 (z = {g(z19,2)} < −1.645)",
     "there is significant evidence that the mean life is less than 40 months; the claim of 40 months is not supported "
     f"(p = {g(N_.cdf(z19),4)}, significant even at 1 %).")
five("(b)", ("μ = 60", "μ > 60"), "0.05", f"z = (61.8 − 60)/(4.9/√100) = 1.8/0.49 = {g(z16,3)}", "z > 1.645",
     "3.67 > 1.645 → reject H0", "the mean life span today is greater than 60 years.")
five("(c)", ("μ = 4", "μ ≠ 4"), "0.05", f"σ = 0.16 known → z = (3.45 − 4)/(0.16/√10) = −0.55/0.0506 = {g(z14,2)}", "|z| > 1.96",
     "|−10.87| > 1.96 → reject H0", "the sample mean does not justify the claim; mean longevity differs from 4 years (it is "
     "less). (If the paper's chart is the t-table, use t = −10.87 against t_{0.025, 9} = 2.262 — same decision.)")
n.answer("(d)", "σ estimated from n = 40 ≥ 30 → z-test.")
n.code(["H0: μ = 2.4   H1: μ ≠ 2.4   α = 0.01, critical region |z| > 2.58",
        f"z = (2.8 − 2.4)/(0.35/√40) = 0.4/{g(se18,4)} = {g(z18,2)}   → |z| = {g(z18,2)} > 2.58 → reject H0",
        f"99% CI: 2.8 ± 2.58 × {g(se18,4)} = 2.8 ± {g(2.58*se18,3)} = ({g(2.8-2.58*se18,3)}, {g(2.8+2.58*se18,3)})"])
n.p("The sample does not come from a group with mean 2.4; the mean score lies between 2.66 and 2.94 with 99 % confidence (2.4 is outside).")
five("(e)", ("μ = 220", "μ > 220"), "0.05", f"n = 20 < 30, σ unknown → t = (244 − 220)/(24.5/√20) = 24/5.478 = {g(t20,3)}  (19 d.f.)",
     f"t > t_{{0.05, 19}} = {g(tc(.05,19),3)}", f"{g(t20,2)} > {g(tc(.05,19),3)} → reject H0",
     "the average sodium content per serving is significantly greater than 220 mg.")
five("(f)", ("μ = 153.7", "μ > 153.7"), "0.05", f"n = 29 < 30 → t = (169.4 − 153.7)/(19.7/√29) = 15.7/3.658 = {g(t15,3)}  (28 d.f.)",
     f"t > t_{{0.05, 28}} = {g(tc(.05,28),3)}", f"{g(t15,2)} > {g(tc(.05,28),3)} → reject H0", "the advertising campaign was successful (sales rose significantly).")
five("(g)", ("μ = 50", "μ < 50"), "0.05", f"t = (42 − 50)/(11.9/√12) = −8/3.435 = {g(t22,3)}  (11 d.f.)", "t < −1.796",
     f"{g(t22,2)} < −1.796 → reject H0", "the new procedure significantly reduces the mean waiting time below 50 minutes.")
five("(h)", ("μ = 120", "μ < 120"), "0.05", f"z = (100 − 120)/(30/√49) = −20/4.286 = {g(z24,3)}", "z < −1.645",
     f"{g(z24,2)} < −1.645 → reject H0", "there is enough evidence to support the claim that the mean delivery time is less than 120 minutes.")
n.answer("(i)", "")
n.code([f"x̄ = {g(m3,2)}, s = {g(s3,3)}, n = 10;  H0: μ = 65, H1: μ ≠ 65, α = 0.05",
        f"t = ({g(m3,2)} − 65)/({g(s3,3)}/√10) = {g(t3,3)}   critical |t| > 2.262 (9 d.f.)",
        f"|{g(t3,2)}| = {g(abs(t3),2)} < 2.262 → do not reject H0"])
n.p("The data are consistent with a universe mean height of 65 inches.")
n.answer("(j)", "")
n.code([f"x̄ = {g(m2,4)}, s = {g(s2,4)}, n = 11;  H0: μ = 0.5, H1: μ ≠ 0.5, α = 0.05",
        f"t = ({g(m2,4)} − 0.5)/({g(s2,4)}/√11) = {g(t2,3)}   critical |t| > 2.23 (10 d.f.)",
        f"|{g(t2,2)}| > 2.23 → reject H0"])
n.p("The average packing cannot be taken as 0.5 lb (the tins are underfilled, x̄ = 0.4773 lb).")
n.answer("(k)", "Type I and II errors: §3 of Lesson 20 (in this problem a Type I error would be wrongly concluding that the population mean is not 47).")
n.code([f"x̄ = {g(m1,3)}, s = {g(s1,3)}, n = 9;  H0: μ = 47, H1: μ ≠ 47",
        f"t = ({g(m1,3)} − 47)/({g(s1,3)}/√9) = {g(t1,3)}   with 8 d.f.",
        f"|t| = {g(abs(t1),2)} < 3.355 (printed) → do not reject H0"])
n.p(f"With the printed t = 3.355 (the 1 % two-tailed value) the sample can be regarded as from a population with mean 47. "
    f"(At 5 % the table value is {g(tc(.025,8),3)}; |t| = {g(abs(t1),2)} would then lead to rejecting H0 — state which level you are using.)")

# ------------------------------------------------------------------ L22
n.lesson("Lesson 22 — Two-sample and Paired Tests of Means", "Hyp pp. 16–31")
n.p("Two independent normal samples (n_{1}, x̄_{1}, s_{1}²) and (n_{2}, x̄_{2}, s_{2}²); H_{0}: μ_{1} = μ_{2} (μ_{1} − μ_{2} = 0). "
    "V(x̄_{1} − x̄_{2}) = V(x̄_{1}) + V(x̄_{2}) = σ_{1}²/n_{1} + σ_{2}²/n_{2} (variances add).")
n.table(["Case", "Statistic", "Distribution / critical value"],
        [["(a) σ_{1}², σ_{2}² known", "z = (x̄_{1} − x̄_{2})/√(σ_{1}²/n_{1} + σ_{2}²/n_{2})", "N(0, 1)"],
         ["(b) σ_{1}² = σ_{2}² unknown, large n", "z = (x̄_{1} − x̄_{2}) / [s√(1/n_{1} + 1/n_{2})]", "N(0, 1)"],
         ["(b) σ_{1}² = σ_{2}² unknown, small n", "t = (x̄_{1} − x̄_{2}) / [s√(1/n_{1} + 1/n_{2})]", "t with n_{1} + n_{2} − 2 d.f."],
         ["(c) unequal, large n", "z = (x̄_{1} − x̄_{2})/√(s_{1}²/n_{1} + s_{2}²/n_{2})", "N(0, 1)"],
         ["(c) unequal, small n", "t = (x̄_{1} − x̄_{2})/√(s_{1}²/n_{1} + s_{2}²/n_{2})", "t_{ν}, Welch d.f. below"],
         ["Paired data", "t = d̄ / (s_{d}/√n), d_{i} = x_{i} − y_{i}", "t_{n−1}"]], widths_cm=[4.4, 7.8, 5], font_size=8.5)
n.formula(["Pooled variance:  s² = [(n_{1} − 1)s_{1}² + (n_{2} − 1)s_{2}²] / (n_{1} + n_{2} − 2)",
           "Welch d.f.:  ν = (s_{1}²/n_{1} + s_{2}²/n_{2})² / [ (s_{1}²/n_{1})²/(n_{1} − 1) + (s_{2}²/n_{2})²/(n_{2} − 1) ]"])
n.p("Decision rules are those of Lesson 21 with the d.f. above (right tail: reject if statistic > critical; left tail: < −critical).")
n.callout("trap", "Do not use the pooled s² unless the question says (or you have tested) that the population variances are "
          "equal — test with F = larger s²/smaller s² (ANOVA note). Slide p. 21 writes V(x̄_{1} − x̄_{2}) = V(x̄_{1}) − V(x̄_{2}) by "
          "a slip; it is a plus.")
n.h2("Slide Examples")
n.code([f"z, σ known: n1 = 50, x̄1 = 105, σ1 = 10; n2 = 60, x̄2 = 100, σ2 = 12:  z = 5/√(100/50 + 144/60) = 5/2.098 = {g(5/math.sqrt(100/50+144/60),3)} (p. 18)",
        f"Tribal (12, 4.5, σ² 1) vs non-tribal (15, 3.4, σ² 1.5): z = 1.1/√(1/12 + 1.5/15) = {g(1.1/math.sqrt(1/12+1.5/15),2)} > 1.96 → reject (p. 20)",
        f"Pooled z, large: n 40, 50; x̄ 52, 48; s² 25, 36: s = √[(39·25 + 49·36)/88] = 5.58; z = 4/(5.58√(1/40 + 1/50)) = {g(4/(5.58*math.sqrt(1/40+1/50)),2)} (p. 23)",
        f"Garment workers: n 15, x̄ 350, s 18; n 10, x̄ 345, s 21: s_p = 19.23, t = 5/(19.23√(1/15 + 1/10)) = {g(5/(19.23*math.sqrt(1/15+1/10)),2)} < t_0.05,23 = 1.714 → not rejected (p. 25)",
        "Medicines A (12, 8, s² 9) vs B (10, 5, s² 16): t = 2.01 < t_0.025,20 = 2.086 → no significant difference (p. 25)"])
n.h2("Paired t-test (pp. 28–31)")
pd_ = np.array([3, 7, 7, 3, 4, 1, 4, 2, 3, 3])
n.p(f"Sales of 10 companies 2014 vs 2015: d = {pd_.tolist()}, d̄ = {g(pd_.mean())}, s_{{d}} = √[(171 − 10 × 3.7²)/9] = {g(pd_.std(ddof=1),2)}, "
    f"t = 3.7/(1.95/√10) = {g(pd_.mean()/(pd_.std(ddof=1)/math.sqrt(10)),1)} > t_{{0.025, 9}} = 2.262 → the two years differ significantly. "
    "Exercise (memory training, 9 students; H_{1}: μ_{d} > 0, d = after − before): d = −7, 14, 5, −6, −5, 3, 1, 6, −5 → "
    f"d̄ = {g(np.mean([-7,14,5,-6,-5,3,1,6,-5]),3)}, t = {g(stats.ttest_1samp([-7,14,5,-6,-5,3,1,6,-5],0).statistic,2)} < t_{{0.05, 8}} = 1.860 → the training is not shown effective.")
n.exam_approach(["Write H_{0}: μ_{1} = μ_{2}; choose the tail from the claim.",
                 "Know the variances? → z. Equal and unknown? → pooled s, z (large) or t (n_{1} + n_{2} − 2 d.f.). Unequal and unknown? → Welch.",
                 "Compute s_{p}, the standard error, the statistic; compare with the critical value; conclude."])
x1 = np.array([9, 11, 13, 11, 15, 9, 12, 14.]); x2 = np.array([10, 12, 10, 14, 9, 8, 10.])
sp2 = ((len(x1) - 1) * x1.var(ddof=1) + (len(x2) - 1) * x2.var(ddof=1)) / (len(x1) + len(x2) - 2)
tt = (x1.mean() - x2.mean()) / math.sqrt(sp2 * (1 / len(x1) + 1 / len(x2)))
z12 = 60 / math.sqrt(80 ** 2 / 500 + 90 ** 2 / 500)
n.practice("Lesson 22", "(a) Actual — 2023-24 Q7(c) (22 batch p. 4). (b) Actual — 2012-13 Q8(b) (TF p. 5).",
           ["(a) Two independent samples of 8 and 7 items had the weights (ounces): I: 9, 11, 13, 11, 15, 9, 12, 14; II: 10, 12, 10, 14, 9, 8, "
            "10. Is the difference between the sample means significant at 5 % (t_{0.05} = 2.16 for 13 d.f.)?  (13)",
            "(b) 500 women shoppers in supermarket A have mean weekly food expenditure Tk 500 with SD 80; 500 women in supermarket B "
            "have Tk 440 with SD 90. Test at the 10 % level whether the average weekly food expenditures of the two populations are equal.  (17)"])
n.solution()
n.answer("(a)", "Equal variances assumed (small samples) → pooled t.")
n.code([f"x̄₁ = {g(x1.mean())}, s₁² = {g(x1.var(ddof=1),3)};  x̄₂ = {g(x2.mean(),3)}, s₂² = {g(x2.var(ddof=1),3)}",
        f"s² = (7 × {g(x1.var(ddof=1),3)} + 6 × {g(x2.var(ddof=1),3)})/13 = {g(sp2,3)},  s = {g(math.sqrt(sp2),3)}",
        f"t = ({g(x1.mean())} − {g(x2.mean(),3)})/({g(math.sqrt(sp2),3)} √(1/8 + 1/7)) = {g(tt,3)}",
        f"H0: μ1 = μ2, H1: μ1 ≠ μ2, α = 0.05: critical |t| > 2.16;  |{g(tt,2)}| < 2.16 → do not reject H0"])
n.p("The difference between the two sample means is not significant at 5 %.")
n.answer("(b)", "n = 500 each (large): σ estimated by s; unequal variances (80² ≠ 90²) → z with separate variances.")
n.code(["H0: μ1 = μ2   H1: μ1 ≠ μ2   α = 0.10, critical |z| > 1.645",
        f"z = (500 − 440)/√(80²/500 + 90²/500) = 60/√(12.8 + 16.2) = 60/{g(math.sqrt(29),3)} = {g(z12,2)}",
        f"|{g(z12,2)}| > 1.645 → reject H0 (p ≈ 0)"])
n.p("The average weekly food expenditures of the two groups of women shoppers are not equal; supermarket A's shoppers spend more.")

# ------------------------------------------------------------------ L23
n.lesson("Lesson 23 — Tests for a Correlation Coefficient and for Proportions", "Hyp pp. 32–37")
n.h2("1. Test of ρ = 0 (pp. 32–34)")
n.formula(["H_{0}: ρ = 0 against H_{1}: ρ ≠ 0;   t = r√(n − 2)/√(1 − r²) ~ t_{n−2}"])
temp = [30, 35, 40, 45, 50, 55, 60]; rate = [1.2, 1.5, 1.7, 2.0, 2.2, 2.5, 2.8]
rt = stats.pearsonr(temp, rate)[0]
n.p(f"Temperature vs reaction rate (7 pairs): the slide uses r = 0.995, t = 0.995√5/√(1 − 0.995²) = 22.26 > t_{{0.025, 5}} = 2.571 → reject H_{{0}} "
    f"(the exact r is {g(rt,4)}, t = {g(rt*math.sqrt(5)/math.sqrt(1-rt**2),1)}, the same decision): a significant positive correlation. Voltage vs current (6 pairs, α = 0.01): "
    f"r = {g(stats.pearsonr([10,12,14,16,18,20],[2.1,2.5,2.8,3.1,3.5,3.9])[0],4)}, "
    f"t = {g(stats.pearsonr([10,12,14,16,18,20],[2.1,2.5,2.8,3.1,3.5,3.9])[0]*2/math.sqrt(1-stats.pearsonr([10,12,14,16,18,20],[2.1,2.5,2.8,3.1,3.5,3.9])[0]**2),1)} > t_{{0.005, 4}} = 4.604 → significant.")
n.h2("2. One-sample Proportion Test (pp. 34–35)")
n.formula(["H_{0}: p = p_{0};   z = (p̂ − p_{0}) / √[p_{0}(1 − p_{0})/n],  p̂ = x/n"])
n.p(f"Valves: p_{{0}} = 0.04, 8 defective in 100: p̂ = 0.08, z = 0.04/√(0.04 × 0.96/100) = {g(0.04/math.sqrt(.04*.96/100),2)} > 1.96 → the defect rate has changed (increased).")
n.h2("3. Two-sample Proportion Test (pp. 36–37)")
n.formula(["H_{0}: p_{1} = p_{2};   z = (p̂_{1} − p̂_{2}) / √[p̂(1 − p̂)(1/n_{1} + 1/n_{2})],   p̂ = (x_{1} + x_{2})/(n_{1} + n_{2})"])
pp = 15 / 350; zp = (0.06 - 0.02) / math.sqrt(pp * (1 - pp) * (1 / 200 + 1 / 150))
n.p(f"LEDs: 12/200 = 0.06 and 3/150 = 0.02; pooled p̂ = 15/350 = {g(pp,5)}; SE = {g(math.sqrt(pp*(1-pp)*(1/200+1/150)),4)}; z = {g(zp,2)} < 1.96 → no significant difference.")
n.p("Exercise answers (p. 37): (1) p̂ = 10/120 = 0.0833, H_{1}: p > 0.05: z = "
    f"{g((10/120-.05)/math.sqrt(.05*.95/120),2)} → < 1.645, not increased; (2) 9/150 vs 4/130, p̂ = 13/280: z = "
    f"{g((9/150-4/130)/math.sqrt(13/280*(1-13/280)*(1/150+1/130)),2)} → no difference; (3) 4/80 vs 0.02, H_{1}: p > 0.02: z = "
    f"{g((4/80-.02)/math.sqrt(.02*.98/80),2)} > 1.645 → increased; (4) 5/100 vs 2/120, 1 %: z = "
    f"{g((5/100-2/120)/math.sqrt(7/220*(1-7/220)*(1/100+1/120)),2)} < 2.58 → no difference.")
x_a, x_b = 16, 3
pa, pb = x_a / 500, x_b / 100; pc = (x_a + x_b) / 600
zq = (pa - pb) / math.sqrt(pc * (1 - pc) * (1 / 500 + 1 / 100))
n.exam_approach(["Proportions: p̂ = x/n; H_{0}: p = p_{0} (one sample) or p_{1} = p_{2} (two samples, pooled p̂).",
                 "z with the standard error under H_{0}; compare with 1.645 / 1.96 / 2.58 as the level and tail require.",
                 "Correlation: compute r (Correlation note), t with n − 2 d.f."])
n.practice("Lesson 23", "Actual — 2023-24 Q7(b) (22 batch p. 3).",
           ["A machine puts out 16 imperfect articles in a sample of 500. After the machine is overhauled it puts out 3 imperfect articles "
            "in a batch of 100. Has the machine improved at the 1 % level of significance (z = ±2.58)?  (12)"])
n.solution()
n.code(["H0: p1 = p2   H1: p1 > p2 (the old rate is higher, i.e. improvement)   α = 0.01",
        f"p̂1 = 16/500 = {g(pa)};  p̂2 = 3/100 = {g(pb)};  pooled p̂ = 19/600 = {g(pc,5)}",
        f"SE = √[{g(pc,5)} × {g(1-pc,5)} × (1/500 + 1/100)] = {g(math.sqrt(pc*(1-pc)*(1/500+1/100)),5)}",
        f"z = ({g(pa)} − {g(pb)})/{g(math.sqrt(pc*(1-pc)*(1/500+1/100)),5)} = {g(zq,3)}",
        f"Critical: 2.33 (one-tailed) or ±2.58 (two-tailed, as printed); {g(zq,2)} < 2.33 → do not reject H0"])
n.p("There is no significant evidence at 1 % that the overhaul reduced the proportion of imperfect articles (the "
    "sample rates are 3.2 % before and 3 % after).")

# ------------------------------------------------------------------ L24
n.lesson("Lesson 24 — χ² Tests: Contingency Tables and Goodness of Fit", "Hyp pp. 38–44 · goodness of fit: textbook")
n.h2("1. r × p Contingency Table (pp. 38–41)")
n.p("A contingency table cross-classifies two attributes A (r categories) and B (p categories), categories mutually exclusive "
    "and exhaustive. O_{ij} = observed cell frequency, R_{i}, C_{j} = row and column totals, N = total.")
n.formula(["H_{0}: no association between A and B;   E_{ij} = R_{i} C_{j} / N",
           "χ² = ΣΣ (O_{ij} − E_{ij})²/E_{ij} = ΣΣ O_{ij}²/E_{ij} − N ~ χ²_{(r−1)(p−1)}",
           "Reject H_{0} if χ² ≥ χ²_{α, (r−1)(p−1)} (one-tailed, upper tail)"])
O = np.array([[10, 40, 10], [30, 30, 20], [10, 30, 20]])
E = O.sum(1, keepdims=True) * O.sum(0, keepdims=True) / O.sum()
chi = ((O - E) ** 2 / E).sum()
n.h3("Education vs job performance (pp. 40–41) — also 2023-24 Q8(a)")
n.table(["Cell (i, j)", "O", "E", "(O − E)²/E"],
        [[f"({i+1},{j+1})", str(O[i, j]), g(E[i, j]), g((O[i, j] - E[i, j]) ** 2 / E[i, j], 2)] for i in range(3) for j in range(3)]
        + [["Total", "200", "200", f"{g(chi,2)} = χ²"]], widths_cm=[4, 3, 3, 4])
n.p(f"Expected: E_{{11}} = 60 × 50/200 = 15, E_{{21}} = 80 × 50/200 = 20, E_{{22}} = 80 × 100/200 = 40, E_{{32}} = 60 × 100/200 = 30 (the slide's list "
    f"gives 30 for E_{{21}}; the table uses the correct 20). χ² = {g(chi,2)} with (3 − 1)(3 − 1) = 4 d.f.; χ²_{{0.05, 4}} = 9.49; "
    f"{g(chi,2)} ≥ 9.49 → reject H_{{0}}: job performance is associated with educational attainment (p = {g(C_.sf(chi,4),4)}).")
n.h2("2. 2 × 2 Table (pp. 42–44)")
n.table(["", "B_{1}", "B_{2}", "Total"], [["A_{1}", "a", "b", "a + b"], ["A_{2}", "c", "d", "c + d"], ["Total", "a + c", "b + d", "N"]],
        widths_cm=[3, 4, 4, 4])
n.formula(["χ² = N(|ad − bc| − N/2)² / [(a + b)(a + c)(c + d)(b + d)] ~ χ²_{1}   (with Yates' correction)",
           "without correction:  χ² = N(ad − bc)² / [(a + b)(a + c)(c + d)(b + d)]"])
n.p("Practice problems of the lecture (pp. 43–44) — answers (Yates-corrected): smoking vs lung disease [36, 14; 18, 32]: "
    + f"χ² = {g(100*(abs(36*32-14*18)-50)**2/(50*54*50*46),2)} > 3.84 → dependent; online course [42, 18; 30, 30]: "
    + f"χ² = {g(120*(abs(42*30-18*30)-60)**2/(60*72*60*48),2)} (< 3.84, no association at 5 %); job vs gender [40, 20; 25, 35]: "
    + f"χ² = {g(120*(abs(40*35-20*25)-60)**2/(60*65*60*55),2)} > 3.84 → job type depends on gender. "
    "Exercises (p. 42): gender × major (141 students) and immunisation × mother's education (500 children) are r × p tables solved as above.")
n.h2("3. Goodness of Fit (textbook; pp. 5–6 state the statistic)")
n.formula(["χ² = Σ (O_{i} − E_{i})²/E_{i} ~ χ²_{k−1−m},   E_{i} = N p_{i}",
           "k = number of classes, m = number of parameters estimated from the data; use classes with E_{i} ≥ 5"])
n.h2("4. What \"Goodness of Fit\" Means")
n.p("It tests whether a set of observed frequencies is consistent with a theoretical distribution (a coin is fair, births are "
    "equally likely male/female, counts are Poisson). H_{0}: the data follow the specified distribution; a large χ² means "
    "the observed frequencies are far from the expected ones.")
n.exam_approach(["Contingency: row/column totals, E_{ij} = R_{i}C_{j}/N, χ² by the table, d.f. = (r − 1)(p − 1), compare with χ²_{α, d.f.}.",
                 "2 × 2: use the ad − bc formula (state whether you apply Yates' correction).",
                 "Goodness of fit: E_{i} = N p_{i} (e.g. binomial(5, 1/2) × N), χ² = Σ(O − E)²/E, d.f. = k − 1 − m.",
                 "Conclude in words (association exists / births equally probable / coin unbiased)."])
coin = ([80, 570, 1100, 900, 500, 50], [100, 500, 1000, 1000, 500, 100])
chi_c = sum((o - e) ** 2 / e for o, e in zip(*coin))
fam1 = ([28, 112, 220, 176, 80, 24], [20, 100, 200, 200, 100, 20])
fam2 = ([18, 56, 110, 88, 40, 8], [10, 50, 100, 100, 50, 10])
chi1 = sum((o - e) ** 2 / e for o, e in zip(*fam1)); chi2 = sum((o - e) ** 2 / e for o, e in zip(*fam2))
O2 = np.array([[200, 300], [280, 20]]); a, b, c, d = 200, 300, 280, 20; N2 = 800
chi_y = N2 * (abs(a * d - b * c) - N2 / 2) ** 2 / ((a + b) * (a + c) * (c + d) * (b + d))
chi_n = N2 * (a * d - b * c) ** 2 / ((a + b) * (a + c) * (c + d) * (b + d))
n.practice("Lesson 24",
           "(a) Actual — 2022-23 Q8(a) (TF p. 50). (b) Actual — 2023-24 Q8(a) (22 batch p. 4). (c) Actual — 2011-12 Q8(b) (TF p. 3). "
           "(d) Actual — 2012-13 Q7(b) (TF p. 5). (e) Actual — 2013-14 Q8(b) (TF p. 8).",
           ["(a) A drug was given to 500 of 800 people to test its efficacy against typhoid. Typhoid: drug 200, no drug 280; no typhoid: drug 300, "
            "no drug 20. Can it be concluded that the drug is effective in preventing typhoid at 5 % (χ²_{0.05, 1} = 3.84)?  (10)",
            "(b) A random sample of 200 employees (education × job performance table, TF 22 batch p. 4) — is there a relationship? Test at 5 % "
            "(χ²_{0.05, 4} = 9.49).  (15)",
            "(c) 5 coins are tossed 3200 times; the number of heads 0, 1, 2, 3, 4, 5 occurs 80, 570, 1100, 900, 500, 50 times. Test at 5 % "
            "that the coins are unbiased (χ²_{0.05, 5} = 11.07).  (18)",
            "(d) A survey of 640 families with 5 children each: boys 5, 4, 3, 2, 1, 0 → 28, 112, 220, 176, 80, 24 families. Is the result "
            "consistent with the hypothesis that male and female births are equally probable? 5 %, χ²_{0.05, 5} = 11.07.  (17)",
            "(e) A survey of 320 families with 5 children: boys 5, 4, 3, 2, 1, 0 → 18, 56, 110, 88, 40, 8 families. Same question.  (15)"])
n.solution()
n.answer("(a)", "H0: drug and typhoid are independent (the drug is not effective); H1: associated. N = 800.")
n.code([f"E(drug, typhoid) = 500 × 480/800 = 300;  E(drug, no) = 200;  E(no drug, typhoid) = 180;  E(no, no) = 120",
        f"χ² = (200 − 300)²/300 + (300 − 200)²/200 + (280 − 180)²/180 + (20 − 120)²/120",
        f"   = 33.33 + 50 + 55.56 + 83.33 = {g(chi_n,2)}   (formula N(ad − bc)²/(…) = {g(chi_n,2)})",
        f"with Yates' correction: N(|ad − bc| − N/2)²/(…) = {g(chi_y,2)}",
        f"d.f. = 1, critical 3.84: {g(chi_y,1)} > 3.84 → reject H0"])
n.p("The drug is associated with typhoid: 40 % of the treated got typhoid against 93 % of the untreated, so the drug is "
    "effective in preventing typhoid.")
n.answer("(b)", "Worked in §1: χ² = 17.51 > 9.49 with 4 d.f. → there is a relationship between educational attainment and job "
         "performance. (Excellent performers are over-represented among college graduates, 40 observed against 30 expected.)")
n.answer("(c)", "H0: the coins are unbiased, so heads ~ Bin(5, ½): probabilities 1, 5, 10, 10, 5, 1 over 32; E = 3200 × these = 100, 500, 1000, 1000, 500, 100.")
n.table(["Heads", "O", "E", "(O − E)²/E"],
        [[str(i), str(o), g(e), g((o - e) ** 2 / e, 2)] for i, (o, e) in enumerate(zip(*coin))] + [["Total", "3200", "3200", f"χ² = {g(chi_c,2)}"]],
        widths_cm=[3, 3, 3, 4])
n.p(f"d.f. = 6 − 1 = 5, χ²_{{0.05, 5}} = 11.07; χ² = {g(chi_c,2)} > 11.07 → reject H0: the coins cannot be regarded as unbiased "
    "(too few 0-head and 5-head throws, too many 1- and 3-head).")
n.answer("(d)", "H0: P(boy) = ½, so boys among 5 children ~ Bin(5, ½); E = 640 × (1, 5, 10, 10, 5, 1)/32 = 20, 100, 200, 200, 100, 20 for 5, 4, …, 0 boys.")
n.code([f"χ² = (28 − 20)²/20 + (112 − 100)²/100 + (220 − 200)²/200 + (176 − 200)²/200 + (80 − 100)²/100 + (24 − 20)²/20",
        f"   = 3.2 + 1.44 + 2 + 2.88 + 4 + 0.8 = {g(chi1,2)}",
        f"d.f. = 5;  {g(chi1,2)} > 11.07 → reject H0"])
n.p("The data are not consistent with equally probable male and female births (more boys than girls: 1.18 boys per girl).")
n.answer("(e)", "E = 320 × (1, 5, 10, 10, 5, 1)/32 = 10, 50, 100, 100, 50, 10.")
n.code([f"χ² = (18 − 10)²/10 + (56 − 50)²/50 + (110 − 100)²/100 + (88 − 100)²/100 + (40 − 50)²/50 + (8 − 10)²/10",
        f"   = 6.4 + 0.72 + 1 + 1.44 + 2 + 0.4 = {g(chi2,2)}",
        f"d.f. = 5;  {g(chi2,2)} > 11.07 → reject H0"])
n.p("Again the hypothesis of equally probable male and female births is rejected at 5 %.")

n.quick_notes("Quick Notes — Tests of Hypothesis", "Revision points for Lessons 20–24.", [
    ("L20 · Concepts", ["H0 has '='; H1 sets the tail. α = P(Type I) = P(reject H0 | true); β = P(Type II).",
                        "p-value ≤ α → reject. Two-tailed p = 2P(Z ≥ |z|).",
                        "DNA: Type I = excluding the real father (≈ 0.001); Type II = declaring a non-father the father (0)."]),
    ("L21 · One sample", ["z = (x̄ − μ0)/(σ/√n) (σ known or n ≥ 30); t = (x̄ − μ0)/(s/√n), n − 1 d.f., s with divisor n − 1.",
                          "Critical z: 1.645 (5 % one-tail), 1.96 (5 % two), 2.33 (1 % one), 2.58 (1 % two). CI x̄ ± z σ/√n.",
                          f"Results: mice z = {g(z19,2)}, reject; deaths z = {g(z16,2)}, reject; GPA z = {g(z18,2)}, CI (2.66, 2.94); cereal t = {g(t20,2)}; "
                          f"sales t = {g(t15,2)}; waiting t = {g(t22,2)}; delivery z = {g(z24,2)}; heights t = {g(t3,2)} (no); tins t = {g(t2,2)} (reject)."]),
    ("L22 · Two samples", ["Variances add: σ1²/n1 + σ2²/n2. Pooled s² = [(n1−1)s1² + (n2−1)s2²]/(n1+n2−2), t with n1 + n2 − 2 d.f.",
                           f"Paired t = d̄/(s_d/√n). Samples I/II: t = {g(tt,2)} (no difference); supermarkets z = {g(z12,2)} (differ)."]),
    ("L23 · r and proportions", ["t = r√(n−2)/√(1−r²) with n − 2 d.f.; z = (p̂ − p0)/√(p0q0/n); two-sample pooled p̂.",
                                 f"Machine overhaul: z = {g(zq,2)} (not significant)."]),
    ("L24 · χ²", ["E_ij = R_i C_j/N; χ² = Σ(O − E)²/E; d.f. (r − 1)(p − 1); 2 × 2: N(ad − bc)²/(…), Yates uses |ad − bc| − N/2.",
                  f"Typhoid χ² = {g(chi_n,2)}/{g(chi_y,2)}; 3 × 3 job table 17.51 (reject); coins {g(chi_c,2)}; families {g(chi1,2)} and {g(chi2,2)} (all reject, 11.07)."])])
n.save()
print("saved", n.out_path)
