"""MATH243_KKS_Discrete_Distributions_Notes.docx — Lectures 10, 11, other distributions pp. 3–6 (L13–L15)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from math import comb, exp, factorial

from scipy import stats

from common import exam_map, new
from m243 import fr, g

B, P = stats.binom, stats.poisson


def bp(k, n_, p):
    return B.pmf(k, n_, p)


n = new("KKS", "Discrete Distributions: Bernoulli, Binomial, Poisson, Multinomial, Hypergeometric",
        "MATH243_KKS_Discrete_Distributions_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "binomial and Poisson in almost every paper"),
              ("Lesson 13 — Bernoulli and Binomial Distributions", "pmf, proofs of mean and variance, numericals"),
              ("Lesson 14 — Poisson Distribution and the Poisson Approximation", "pmf, mean = variance, limit proof, approximations"),
              ("Lesson 15 — Multinomial, Hypergeometric and Geometric Distributions", "other distributions + TF questions"),
              ("Quick Notes — Discrete Distributions", "revision bullets")],
    source_note="Page numbers refer to KKS Sir's Lecture 10.pdf (4 pp.), Lecture 11.pdf (5 pp.) and Lecture on other "
                "distributions...pdf (Walpole 9th ed. extracts: multinomial pp. 3–4, exercises pp. 4–6, hypergeometric "
                "introduction p. 6). The hypergeometric pmf and the geometric/negative-binomial distributions are completed "
                "from the textbook and marked. \"TF p.\" = merged question PDF page; \"22 batch p.\" = 2023-24 paper.")

n.h1("Exam Map — What the TF Papers Ask")
st = exam_map(n, "k5")
n.callout("focus", f"{st['n']} questions, {st['marks']} marks — the most frequently asked probability topic "
          f"({st['n_hi']} questions since 2019-20). Three things are certain to come: (1) a binomial numerical with "
          "\"at least / from a to b\"; (2) a Poisson numerical, usually as an approximation to the binomial with "
          "λ = np; (3) a derivation — mean and variance of the binomial, or the Poisson as a limit of the binomial "
          "(2012-13, 2016-17, 2022-23, 2023-24). Learn the two derivations word-perfect.")

# ------------------------------------------------------------------ L13
n.lesson("Lesson 13 — Bernoulli and Binomial Distributions", "Lec 10 pp. 1–4")
n.h2("1. Binomial Experiment (Lec 10 p. 1)")
n.p("An experiment with two outcomes (success, failure), repeated n times independently, with the same probability "
    "p of success in each trial, is a binomial experiment. X = number of successes.")
n.formula(["X ~ Binomial(n, p):  P(X = x) = nCx p^{x} (1 − p)^{n−x},  x = 0, 1, …, n",
           "E(X) = np,   V(X) = np(1 − p)"])
n.p("n = 1 gives the **Bernoulli** distribution: P(X = x) = p^{x}(1 − p)^{1−x}, x = 0, 1, with E(X) = p, V(X) = p(1 − p).")
n.h2("2. The Proofs (Lec 10 p. 1 asks them; standard working) ★")
n.code(["Bernoulli:  Σ f = (1 − p) + p = 1;  E(X) = 0(1 − p) + 1·p = p;  E(X²) = p;  V(X) = p − p² = p(1 − p)",
        "",
        "Binomial total:  Σ_{x=0}^{n} nCx p^x q^(n−x) = (p + q)^n = 1^n = 1      (q = 1 − p, binomial theorem)",
        "",
        "Mean:  E(X) = Σ x · n!/(x!(n−x)!) p^x q^(n−x)          (the x = 0 term is 0)",
        "            = np Σ_{x=1}^{n} (n−1)!/((x−1)!(n−x)!) p^(x−1) q^(n−x)",
        "            = np Σ_{y=0}^{n−1} (n−1)Cy p^y q^(n−1−y)    (y = x − 1)",
        "            = np (p + q)^(n−1) = np",
        "",
        "E[X(X−1)] = Σ x(x−1) n!/(x!(n−x)!) p^x q^(n−x)",
        "          = n(n−1)p² Σ_{y=0}^{n−2} (n−2)Cy p^y q^(n−2−y) = n(n−1)p²",
        "E(X²) = E[X(X−1)] + E(X) = n(n−1)p² + np",
        "V(X) = E(X²) − (np)² = n²p² − np² + np − n²p² = np(1 − p) = npq"])
n.callout("memorize", "Trick for both binomial and Poisson variances: find E[X(X − 1)] first (the x(x − 1) cancels "
          "with x!), then V = E[X(X − 1)] + E(X) − [E(X)]².")
n.h2("3. Worked Examples (Lec 10 pp. 2–3)")
n.code([f"Recover p = 0.9, n = 7:  P(X = 5) = 7C5 (0.9)^5 (0.1)^2 = {g(bp(5,7,0.9))};   E(X) = 7 × 0.9 = 6.3 patients",
        f"Trucks out of city p = 0.25, n = 5:",
        f"   P(X ≥ 3) = 5C3(.25)³(.75)² + 5C4(.25)⁴(.75) + (.25)⁵ = {g(B.sf(2,5,.25))}",
        f"   P(X > 3) = P(4) + P(5) = {g(B.sf(3,5,.25))};   E(X) = 5 × 0.25 = 1.25 (125 of 500 trucks)"])
n.bullets(["Interval words: at most 2 → X ≤ 2; less than 2 → X ≤ 1; P(1 ≤ X < 3) = P(1) + P(2); P(1 < X < 3) = P(2).",
           "Given E(X) = 5 and V(X) = 2: 1 − p = 2/5, p = 3/5, n = 5/p = 25/3. Since n must be an integer, such a "
           "binomial cannot exist — the slide stops at n = 25/3; say so in an answer."])
ex2 = [B.cdf(1, 20, .05), B.sf(2, 20, .05), B.cdf(5, 20, .05) - B.cdf(1, 20, .05)]
n.h3("Exercises of Lecture 10 (p. 4) — answers")
n.table(["Exercise", "Answer"],
        [["10 tosses, exactly 7 heads", f"10C7/2^{{10}} = 120/1024 = {g(bp(7,10,.5))}"],
         ["20 items, p = 0.05: at most 1; at least 3; between 2 and 5", f"{g(ex2[0])}; {g(ex2[1])}; P(2 ≤ X ≤ 5) = {g(ex2[2])}"],
         ["15 patients, p = 0.6: at least 10; mean, variance", f"{g(B.sf(9,15,.6))}; 9 and 3.6"]], widths_cm=[8.6, 8.6])
n.exam_approach(["Define X and the success, check the four binomial conditions, write X ~ Bin(n, p).",
                 "Translate the words into an inequality on X.",
                 "Use the complement when the requested side has more terms (\"at least 1\" = 1 − P(0)).",
                 "Write every term nCx p^{x}q^{n−x} explicitly, then the sum; keep 4 decimals."])
n.practice("Lesson 13", "(a) Actual — 2023-24 Q3(c) (22 batch p. 2). (b) Actual — 2014-15 Q8(b) (TF p. 11). "
           "(c) Actual — 2013-14 Q7(b)(ii) (TF p. 8). (d) Actual — 2020-21 Q7(a) (TF p. 38). (e) Actual — 2012-13 Q6(c) (TF p. 5).",
           ["(a) The probability that a person recovers from a rare blood disease is 0.4. If 15 people are known to have "
            "contracted it, find the probability that (i) at least 10 survive, (ii) from 3 to 8 survive, (iii) exactly 5 die.  (12)",
            "(b) The probability that an entering college student will graduate is 0.4. Out of 5 students find the "
            "probability that (i) none, (ii) at least 1, (iii) all will graduate.  (12)",
            "(c) 10 % of the instruments produced are defective. Find the probability that out of 12, at least 4 are defective.  (8)",
            "(d) The probability of a diode failure is 0.03 and a board contains 200 diodes. (i) Mean number of failures? "
            "(ii) Variance? (iii) The board works only if no diode is defective: P(board works)?  (17)",
            "(e) Derive the mean and variance of the binomial distribution.  (10)"])
n.solution()
p3 = [bp(k, 15, .4) for k in range(16)]
n.answer("(a)", "X = number who survive (recover), X ~ Bin(15, 0.4), q = 0.6.")
n.code([f"(i)   P(X ≥ 10) = Σ_{{x=10}}^{{15}} 15Cx (0.4)^x (0.6)^(15−x)",
        "            = " + " + ".join(g(p3[k]) for k in range(10, 16)) + f" = {g(sum(p3[10:]))}",
        f"(ii)  P(3 ≤ X ≤ 8) = " + " + ".join(g(p3[k]) for k in range(3, 9)) + f" = {g(sum(p3[3:9]))}",
        f"(iii) 5 die ⟺ 10 survive:  P(X = 10) = 15C10 (0.4)^10 (0.6)^5 = 3003 × 1.048576e−4 × 0.07776 = {g(p3[10])}"])
n.answer("(b)", "X ~ Bin(5, 0.4).")
n.code([f"(i) P(0) = 0.6^5 = {g(0.6**5)}   (ii) P(X ≥ 1) = 1 − 0.6^5 = {g(1-0.6**5)}   (iii) P(5) = 0.4^5 = {g(0.4**5)}"])
p4 = [bp(k, 12, .1) for k in range(4)]
n.answer("(c)", "X ~ Bin(12, 0.1): P(X ≥ 4) = 1 − [P(0) + P(1) + P(2) + P(3)].")
n.code([f"P(0) = 0.9^12 = {g(p4[0])};  P(1) = 12(0.1)(0.9)^11 = {g(p4[1])};  P(2) = 66(0.01)(0.9)^10 = {g(p4[2])};  "
        f"P(3) = 220(0.001)(0.9)^9 = {g(p4[3])}",
        f"P(X ≥ 4) = 1 − {g(sum(p4))} = {g(1-sum(p4))}"])
n.answer("(d)", "X = failures ~ Bin(200, 0.03).")
n.code(["(i)   E(X) = np = 200 × 0.03 = 6",
        "(ii)  V(X) = np(1 − p) = 6 × 0.97 = 5.82",
        f"(iii) P(X = 0) = 0.97^200 = {g(0.97**200)}   (Poisson λ = 6: e^−6 = {g(exp(-6))}, close)"])
n.answer("(e)", "The derivation in §2 (total = 1, E(X) = np via the y = x − 1 shift, V(X) = npq via E[X(X − 1)]).")

# ------------------------------------------------------------------ L14
n.lesson("Lesson 14 — Poisson Distribution and the Poisson Approximation", "Lec 11 pp. 1–5")
n.h2("1. The Poisson Distribution (Lec 11 p. 1)")
n.formula(["X ~ Poisson(λ):  f(x) = e^{−λ} λ^{x} / x!,  x = 0, 1, 2, …", "E(X) = V(X) = λ"])
n.p("λ = mean number of successes in a given time interval or region; X = number of successes in it. Used for counts "
    "of rare events (calls per interval, accidents per week, defects per item).")
n.h2("2. Proof that Mean = Variance (Lec 11 p. 1) ★")
n.code(["Σ f(x) = e^−λ Σ λ^x/x! = e^−λ e^λ = 1",
        "E(X) = Σ_{x=1}^∞ x e^−λ λ^x/x! = λ e^−λ Σ_{x=1}^∞ λ^(x−1)/(x−1)! = λ e^−λ e^λ = λ",
        "E[X(X−1)] = Σ_{x=2}^∞ x(x−1) e^−λ λ^x/x! = λ² e^−λ Σ_{x=2}^∞ λ^(x−2)/(x−2)! = λ²",
        "V(X) = E[X(X−1)] + E(X) − [E(X)]² = λ² + λ − λ² = λ"])
n.h2("3. Poisson as a Limit of the Binomial ★ (Lec 11 p. 3 states it; proof: textbook)")
n.code(["Let n → ∞, p → 0 with np = λ fixed, i.e. p = λ/n.",
        "b(x; n, p) = n!/(x!(n−x)!) (λ/n)^x (1 − λ/n)^(n−x)",
        "           = (λ^x/x!) · [n(n−1)…(n−x+1)/n^x] · (1 − λ/n)^n · (1 − λ/n)^(−x)",
        "As n → ∞:  n(n−1)…(n−x+1)/n^x = (1)(1 − 1/n)…(1 − (x−1)/n) → 1",
        "           (1 − λ/n)^n → e^−λ,      (1 − λ/n)^(−x) → 1",
        "Hence b(x; n, p) → e^−λ λ^x / x! = p(x; λ)   ∎"])
n.callout("answer", "Bernoulli process: a sequence of independent trials, each a success with the same probability p; "
          "the number of successes in n trials is binomial. Poisson process: events occur randomly in continuous time "
          "(or space) such that (i) counts in non-overlapping intervals are independent, (ii) the probability of one "
          "event in a short interval of length h is about λh, proportional to h, and (iii) the probability of two or "
          "more events in it is negligible. Dividing an interval of length t into n small sub-intervals turns the "
          "Poisson process into a Bernoulli process with p = λt/n; letting n → ∞ gives the Poisson distribution with "
          "mean λt (the limit above). Relation: Poisson(np) is the limit of Binomial(n, p) when n is large and p small. "
          "(2022-23 Q3(a), 2023-24 Q3(b), 2016-17 Q8(a))")
n.h2("4. Worked Examples (Lec 11 pp. 1–4)")
n.code([f"Calls, λ = 3 per 10 min:  P(0) = e^−3 = {g(P.pmf(0,3))};  P(1) = 3e^−3 = {g(P.pmf(1,3))};  "
        f"P(X ≥ 2) = 1 − 0.0498 − 0.1494 = {g(P.sf(1,3))}",
        "P(X = 1) = P(X = 2):  e^−λ λ = e^−λ λ²/2  →  λ = 2;  mean 2, SD √2",
        f"Beakers n = 250, p = 0.012:  binomial P(2) = {g(bp(2,250,.012))};  Poisson λ = 3: P(2) = 9e^−3/2 = {g(P.pmf(2,3))}",
        f"Accidents p = 0.005, 400 days (λ = 2):  P(1) = 2e^−2 = {g(P.pmf(1,2))};  P(X ≤ 3) = {g(P.cdf(3,2))}",
        f"Bubbles 1 in 1000, n = 8000 (λ = 8):  P(X < 7) = Σ_0^6 e^−8 8^x/x! = {g(P.cdf(6,8))}"])
rows = []
for lab, lam, qs in (("λ = 4 per hour: P(7), P(0)", 4, [("P(7)", P.pmf(7, 4)), ("P(0)", P.pmf(0, 4))]),
                     ("λ = 2 per week: P(≤ 1), P(≥ 2)", 2, [("≤ 1", P.cdf(1, 2)), ("≥ 2", P.sf(1, 2))]),
                     ("λ = 6 per hour: P(4 to 8), P(> 10)", 6, [("4–8", P.cdf(8, 6) - P.cdf(3, 6)), ("> 10", P.sf(10, 6))]),
                     ("1000 × 0.002 (λ = 2): P(3), P(≤ 3), P(≥ 3)", 2, [("3", P.pmf(3, 2)), ("≤ 3", P.cdf(3, 2)), ("≥ 3", P.sf(2, 2))]),
                     ("500 × 0.01 (λ = 5): P(4), P(≤ 4), P(≥ 6)", 5, [("4", P.pmf(4, 5)), ("≤ 4", P.cdf(4, 5)), ("≥ 6", P.sf(5, 5))]),
                     ("600 × 0.005 (λ = 3): P(2), P(≤ 2), P(≥ 4)", 3, [("2", P.pmf(2, 3)), ("≤ 2", P.cdf(2, 3)), ("≥ 4", P.sf(3, 3))]),
                     ("2000 × 0.001 (λ = 2): P(3), P(≤ 3), P(≥ 3)", 2, [("3", P.pmf(3, 2)), ("≤ 3", P.cdf(3, 2)), ("≥ 3", P.sf(2, 2))]),
                     ("8000 × 0.0005 (λ = 4): P(2), P(≤ 2), P(≥ 3)", 4, [("2", P.pmf(2, 4)), ("≤ 2", P.cdf(2, 4)), ("≥ 3", P.sf(2, 4))])):
    rows.append([lab, "; ".join(f"{a} = {g(b)}" for a, b in qs)])
n.h3("Exercises of Lecture 11 (pp. 2–5) — answers")
n.table(["Exercise", "Answers"], rows, widths_cm=[8.6, 8.6], font_size=9)
n.callout("trap", "Scale λ to the interval asked: 0.5 calls per minute → λ = 2.5 for a five-minute period. And use "
          "the Poisson approximation only when n is large and p small (np moderate); otherwise compute the binomial.")
n.exam_approach(["Identify the count and its mean λ for the stated interval (λ = np for an approximation).",
                 "Write f(x) = e^{−λ}λ^{x}/x! for each x needed; use 1 − Σ for \"at least\".",
                 "When asked for both binomial and Poisson, compute both and comment on how close they are.",
                 "Derivations: Σ f = 1, E(X) by cancelling x with x!, V(X) via E[X(X − 1)]; limit proof with p = λ/n."])
p6 = [P.pmf(k, 10) for k in (6, 7, 8)]
bb = [B.cdf(7, 18, .2) - B.cdf(3, 18, .2), B.cdf(2, 18, .2), B.sf(5, 18, .2)]
pp_ = [P.cdf(7, 3.6) - P.cdf(3, 3.6), P.cdf(2, 3.6), P.sf(5, 3.6)]
n.practice("Lesson 14", "(a) Actual — 2022-23 Q3(b) (TF p. 48). (b) Actual — 2023-24 Q3(b) (22 batch p. 2). "
           "(c) Actual — 2016-17 Q8(a) (TF p. 21). (d) Actual — 2019-20 Q8(a) (TF p. 35). (e) Actual — 2011-12 Q7(b)(i) "
           "(TF p. 2). (f) Actual — 2012-13 Q6(b) (TF p. 5).",
           ["(a) Calculate the variance of a Poisson random variable. On average 1 person in 1000 makes a numerical error "
            "in his or her tax return. If 10,000 returns are examined, find the probability that 6, 7 or 8 contain an error.  (12)",
            "(b) Establish the relation between the binomial and Poisson distributions. Calls arrive at a mean rate of 0.5 "
            "per minute. Find the probability that two calls arrive in a particular five-minute period.  (12)",
            "(c) Prove that b(x; n, p) → p(x; μ) when n → ∞, p → 0 and np → μ. Accidents occur on a day with probability "
            "0.005, independently. Find the probability that in 400 days (i) there is an accident on one day, (ii) there "
            "are at most three days with an accident.  (20)",
            "(d) On average 1 in every 1000 glass items has bubbles. What is the probability that a random sample of 8000 "
            "yields fewer than 7 items with bubbles?  (10)",
            "(e) P(an insured person dies within a year) = 0.0005. If 1000 such persons are insured, find the probability "
            "that the company receives 5 or more claims in a year.  (7)",
            "(f) 20 % of trucks fail the test run with a blowout. Of the next 18 trucks, find the probability, by both the "
            "binomial and the Poisson distribution, that (i) from 4 to 7, (ii) fewer than 3, (iii) more than 5 have blowouts.  (10)"])
n.solution()
n.answer("(a)", "Variance = λ (proof in §2). Here λ = np = 10,000 × 0.001 = 10.")
n.code([f"P(6) = e^−10 10^6/6! = {g(p6[0])};  P(7) = e^−10 10^7/7! = {g(p6[1])};  P(8) = e^−10 10^8/8! = {g(p6[2])}",
        f"P(6 or 7 or 8) = {g(sum(p6))}"])
n.answer("(b)", "Relation: §3 (the Poisson is the limit of the binomial with λ = np). For five minutes λ = 0.5 × 5 = 2.5.")
n.formula(f"P(X = 2) = e^{{−2.5}}(2.5)²/2! = 3.125 × 0.082085 = {g(P.pmf(2,2.5))}")
n.answer("(c)", "Proof in §3. λ = np = 400 × 0.005 = 2.")
n.code([f"(i)  P(X = 1) = 2e^−2 = {g(P.pmf(1,2))}",
        f"(ii) P(X ≤ 3) = e^−2 (1 + 2 + 2²/2! + 2³/3!) = e^−2 (1 + 2 + 2 + 1.3333) = 6.3333 × 0.135335 = {g(P.cdf(3,2))}"])
n.answer("(d)", "n = 8000, p = 0.001 → λ = 8.")
n.code(["P(X < 7) = e^−8 [1 + 8 + 8²/2! + 8³/3! + 8⁴/4! + 8⁵/5! + 8⁶/6!]",
        "         = 0.00033546 × [1 + 8 + 32 + 85.333 + 170.667 + 273.067 + 364.089]",
        f"         = 0.00033546 × 934.156 = {g(P.cdf(6,8))}"])
n.answer("(e)", "λ = 1000 × 0.0005 = 0.5.")
n.code([f"P(X ≥ 5) = 1 − e^−0.5 [1 + 0.5 + 0.125 + 0.020833 + 0.0026042] = 1 − 0.606531 × 1.6484375 = {P.sf(4,.5):.6f}",
        f"(exact binomial: {B.sf(4,1000,.0005):.6f}; about 1.7 chances in 10,000)"])
n.answer("(f)", "Binomial X ~ Bin(18, 0.2); Poisson λ = np = 3.6.")
n.table(["Part", "Binomial", "Poisson (λ = 3.6)"],
        [["(i) 4 ≤ X ≤ 7", g(bb[0]), g(pp_[0])], ["(ii) X ≤ 2", g(bb[1]), g(pp_[1])], ["(iii) X ≥ 6", g(bb[2]), g(pp_[2])]],
        widths_cm=[5, 6, 6.2])
n.p("Individual binomial terms: P(0) = 0.0180, P(1) = 0.0811, P(2) = 0.1723, P(4) = 0.2153, P(5) = 0.1507, P(6) = 0.0816, "
    "P(7) = 0.0350. The Poisson values differ by 0.02–0.03 because p = 0.2 is not small.")

# ------------------------------------------------------------------ L15
n.lesson("Lesson 15 — Multinomial, Hypergeometric and Geometric Distributions",
         "other distributions pp. 3–6 · hypergeometric pmf and geometric: textbook")
n.h2("1. Multinomial Distribution (other distributions pp. 3–4)")
n.p("Each of n independent trials ends in one of k outcomes E_{1}, …, E_{k} with probabilities p_{1}, …, p_{k} (Σp_{i} = 1). "
    "The number of orders giving x_{1} of E_{1}, …, x_{k} of E_{k} is n!/(x_{1}!…x_{k}!), each with probability Π p_{i}^{x_{i}}.")
n.formula("f(x_{1}, …, x_{k}) = [n! / (x_{1}! x_{2}! … x_{k}!)] p_{1}^{x_{1}} p_{2}^{x_{2}} … p_{k}^{x_{k}},  Σx_{i} = n")
n.p(f"Example 5.7 (runways 2/9, 1/6, 11/18; 6 planes as 2, 1, 3): 6!/(2!1!3!) (2/9)²(1/6)(11/18)³ = 60 × 0.04938 × "
    f"0.16667 × 0.22822 = {g(60*(2/9)**2*(1/6)*(11/18)**3)}.")
n.h2("2. Hypergeometric Distribution (other distributions p. 6; pmf: textbook)")
n.p("Sampling **without replacement** from a lot of N items of which k are successes (defectives, winning tickets): "
    "trials are not independent, so the binomial does not apply exactly.")
n.formula(["h(x; N, n, k) = kCx · (N − k)C(n − x) / NCn",
           "E(X) = nk/N,   V(X) = [(N − n)/(N − 1)] · n (k/N)(1 − k/N)"])
n.p("When N is large compared with n, h(x; N, n, k) ≈ b(x; n, k/N).")
n.h2("3. Geometric and Negative Binomial (textbook)")
n.formula(["Geometric (first success on trial x): g(x; p) = p q^{x−1},  x = 1, 2, …",
           "Negative binomial (k-th success on trial x): b*(x; k, p) = (x−1)C(k−1) p^{k} q^{x−k}"])
n.exam_approach(["Classify: fixed n with replacement/independent → binomial; without replacement from a finite lot → "
                 "hypergeometric; more than two outcomes → multinomial; \"the x-th trial is the first/k-th success\" → "
                 "geometric/negative binomial.",
                 "Write the formula with the numbers substituted before multiplying.",
                 "Distribution + F(x): list f(x) for every x, then cumulative sums as a step function."])
hyp = [F(comb(200, i) * comb(300, 5 - i), comb(500, 5)) for i in range(6)]
mult = factorial(9) / (factorial(3) * factorial(3) * factorial(1) * factorial(2)) * 0.4 ** 3 * 0.2 ** 3 * 0.3 * 0.1 ** 2
car = [F(comb(2, i) * comb(3, 3 - i), comb(5, 3)) for i in range(3)]
n.practice("Lesson 15", "(a) Actual — 2021-22 Q6(b) (TF p. 44). (b) Actual — 2021-22 Q6(a) (TF p. 44). "
           "(c) Actual — 2021-22 Q6(c) (TF p. 44). (d) Actual — 2020-21 Q6(c) (TF p. 38).",
           ["(a) Delegates arrive by air, bus, automobile or train with probabilities 0.4, 0.2, 0.3, 0.1. What is the "
            "probability that among 9 delegates 3 arrived by air, 3 by bus, 1 by automobile and 2 by train?  (10)",
            "(b) 500 lottery tickets are sold; 200 of them pay off at least the cost of the ticket. You buy 5 tickets. "
            "Find the probability that you win back at least the cost of 3 tickets.  (10)",
            "(c) A shipment of 5 cars contains 2 with slight paint blemishes. An agency receives 3 at random. Find the "
            "probability distribution and F(x) of X = number of blemished cars received.  (15)",
            "(d) Two-thirds of Valium users are women. Find the probability that on a given day the fifth prescription "
            "written by a doctor is (i) the first prescribing Valium for a woman, (ii) the third prescribing Valium for a woman.  (10)"])
n.solution()
n.answer("(a)", "Multinomial with n = 9.")
n.formula(f"f = 9!/(3! 3! 1! 2!) (0.4)³(0.2)³(0.3)(0.1)² = 5040 × 0.064 × 0.008 × 0.3 × 0.01 = {g(mult,5)}")
n.answer("(b)", "X = winning tickets among 5; N = 500, k = 200, n = 5 (without replacement).")
n.code(["P(X ≥ 3) = [200C3·300C2 + 200C4·300C1 + 200C5·300C0] / 500C5",
        "         = " + " + ".join(g(float(hyp[i])) for i in (3, 4, 5)) + f" = {g(float(sum(hyp[3:])))}",
        f"Binomial check (N large, p = 200/500 = 0.4): P(X ≥ 3) = {g(B.sf(2,5,.4))} — almost the same"])
n.answer("(c)", "Hypergeometric N = 5, k = 2, n = 3; 5C3 = 10. X can be 0, 1, 2.")
n.code([f"f(0) = 2C0·3C3/10 = {fr(car[0])};   f(1) = 2C1·3C2/10 = 6/10 = {fr(car[1])};   f(2) = 2C2·3C1/10 = {fr(car[2])}",
        "F(x) = 0 for x < 0;  1/10 for 0 ≤ x < 1;  7/10 for 1 ≤ x < 2;  1 for x ≥ 2"])
n.answer("(d)", "Each prescription is for a woman with p = 2/3, independently (q = 1/3).")
n.code([f"(i)  geometric: P(first woman on 5th) = q⁴ p = (1/3)⁴(2/3) = 2/243 = {g(2/243)}",
        f"(ii) negative binomial, k = 3, x = 5: 4C2 (2/3)³(1/3)² = 6 × 8/27 × 1/9 = 16/81 = {g(16/81)}"])

n.quick_notes("Quick Notes — Discrete Distributions", "Revision points for Lessons 13–15.", [
    ("L13 · Binomial", ["nCx p^{x}q^{n−x}; mean np; variance npq (prove via y = x − 1 and E[X(X − 1)]).",
                        "Bernoulli: p, p(1 − p). E = 5, V = 2 gives n = 25/3 — impossible binomial.",
                        "Bin(15, 0.4): P(≥ 10) = 0.0338, P(3–8) = 0.8778, P(10) = 0.0245. Bin(12, 0.1): P(≥ 4) = 0.0256.",
                        "Diodes: mean 6, var 5.82, P(0) = 0.97^{200} = 0.00226."]),
    ("L14 · Poisson", ["e^{−λ}λ^{x}/x!; mean = variance = λ; limit of Bin(n, λ/n) as n → ∞.",
                       "λ = np when n large, p small; scale λ to the interval (0.5/min × 5 = 2.5).",
                       "Tax returns λ = 10: 0.2657. Accidents λ = 2: 0.2707, 0.8571. Bubbles λ = 8: 0.3134. Claims λ = 0.5: 0.00017."]),
    ("L15 · Other Discrete", ["Multinomial n!/(Πx_{i}!) Πp_{i}^{x_{i}}; delegates 0.00774.",
                              "Hypergeometric kCx(N−k)C(n−x)/NCn, mean nk/N; lottery 0.3167; cars 1/10, 6/10, 3/10.",
                              "Geometric pq^{x−1}; negative binomial (x−1)C(k−1)p^{k}q^{x−k}; Valium 2/243, 16/81."])])
n.save()
print("saved", n.out_path)
