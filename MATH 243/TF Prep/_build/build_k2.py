"""MATH243_KKS_Conditional_Bayes_Notes.docx — Lecture 5 (L5–L6)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F

from common import exam_map, new
from m243 import fr, g

n = new("KKS", "Conditional Probability, Total Probability and Bayes' Theorem",
        "MATH243_KKS_Conditional_Bayes_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "Bayes and transfer-of-ball questions every recent year"),
              ("Lesson 5 — Conditional Probability and the Multiplication Law", "P(A | B), TV couple, dice, picnic"),
              ("Lesson 6 — Total Probability and Bayes' Theorem", "proof, tree/table method, all TF Bayes questions"),
              ("Quick Notes — Conditional Probability and Bayes", "revision bullets")],
    source_note="Page numbers refer to Lecture 5.pdf (KKS Sir, 7 pp.), written as Lec 5 p. n. \"TF p.\" = page of "
                "MATH 243 All Merged Questions.pdf; \"22 batch p.\" = page of MATH 243 (22 batch).pdf (2023-24).")

n.h1("Exam Map — What the TF Papers Ask")
st = exam_map(n, "k2")
n.callout("focus", f"{st['n']} questions, {st['marks']} marks; {st['n_hi']} of them ({st['marks_hi']} marks) are from "
          "2019-20 onward. A Bayes question (three sources → P(source | event)) appeared in 2019-20, 2022-23 and "
          "2023-24, and a \"ball transferred from one bag to another\" question in both MATH 243 papers. This is the most "
          "reliable 20–30 marks of Section A: learn the table method of Lesson 6 until it is automatic.")

# ------------------------------------------------------------------ L5
n.lesson("Lesson 5 — Conditional Probability and the Multiplication Law", "Lec 5 pp. 1–4")
n.h2("1. Definition (Lec 5 p. 1)")
n.p("The probability of A when it is known that B has occurred is the **conditional probability** P(A | B), read "
    "\"probability of A given B\". In general P(A | B) ≠ P(A).")
n.formula(["P(A | B) = P(A ∩ B) / P(B),   P(B) ≠ 0", "P(B | A) = P(A ∩ B) / P(A),   P(A) ≠ 0"])
n.h2("2. Multiplication Law (Lec 5 pp. 1–2)")
n.formula(["P(A ∩ B) = P(A) P(B | A) = P(B) P(A | B)",
           "P(A_{1} ∩ A_{2} ∩ A_{3}) = P(A_{1}) P(A_{2} | A_{1}) P(A_{3} | A_{1} ∩ A_{2})"])
n.callout("answer", "Multiplication law of probability: for two events A and B, the probability of their simultaneous "
          "occurrence equals the unconditional probability of one of them multiplied by the conditional probability "
          "of the other given that the first has occurred: P(A ∩ B) = P(A)P(B | A). For k events, "
          "P(A_{1} ∩ … ∩ A_{k}) = P(A_{1})P(A_{2} | A_{1}) … P(A_{k} | A_{1} ∩ … ∩ A_{k−1}). If A and B are independent "
          "it reduces to P(A ∩ B) = P(A)P(B). (Asked as the theory part of 2023-24 Q1(b).)")
n.h2("3. Worked Examples (Lec 5 pp. 2–4)")
n.h3("Problem 1 — two dice: sum ≥ 10 given a 5 on the first die")
n.p("A = {(4,6), (5,5), (5,6), (6,4), (6,5), (6,6)}, B = {(5,1), …, (5,6)}, A ∩ B = {(5,5), (5,6)}. "
    "P(A | B) = (2/36)/(6/36) = 1/3.")
n.h3("Problem 2 — TV show: P(H) = 0.4, P(W) = 0.5, P(H | W) = 0.7")
n.code(["(a) P(couple) = P(W ∩ H) = P(W) P(H | W) = 0.5 × 0.7 = 0.35",
        "(b) P(W | H)  = P(W ∩ H) / P(H) = 0.35 / 0.40 = 0.875",
        "(c) P(W ∪ H)  = P(W) + P(H) − P(W ∩ H) = 0.5 + 0.4 − 0.35 = 0.55"])
n.callout("note", "The slide writes \"0.40 + 0.50 − 0.35\" in (c); the order does not matter, 0.55 is right.")
n.h3("Problem 3 — toss until a head or three tosses")
n.p("S = {H, TH, TTH, TTT} with probabilities 1/2, 1/4, 1/8, 1/8. A = tossed three times = {TTH, TTT}; B = no head on "
    "the first toss = {TH, TTH, TTT}; P(A ∩ B) = 1/4, P(B) = 1/2, so P(A | B) = 1/2.")
n.h3("Problem 4 — disabled: equal males and females, 5 % of males and 2 % of females disabled")
n.p("P(M ∩ D) = 0.5 × 0.05 = 0.025, so P(D | M) = 0.025/0.5 = 0.05 — the conditional probability is just the "
    "given rate.")
n.callout("trap", "P(A | B) and P(B | A) are different numbers (0.7 vs 0.875 above). Always write which event is the "
          "condition before you divide, and divide by the probability of the condition.")
n.exam_approach(["Name the events with letters and write down every given number in symbols (P(H | W) = 0.8 …).",
                 "Find the joint probability first: P(A ∩ B) = P(B)P(A | B).",
                 "Any other conditional = joint ÷ probability of the new condition; complements via P(A ∩ B^{c}) = P(A) − P(A ∩ B).",
                 "Check that every probability lies in [0, 1] and that P(A ∩ B) ≤ min(P(A), P(B))."])
both = 0.35 * 0.8
n.practice("Lesson 5", "(a) Actual — 2015-16 Q8(a) (TF p. 16). (b) Actual — 2018-19 Q6(b) (TF p. 24).",
           ["(a) The probability that a married man watches a certain television show is 0.25 and that a married woman "
            "watches it is 0.35. The probability that a man watches the show, given that his wife does, is 0.8. Find "
            "the probability that (i) a married couple watches the show, (ii) a husband watches the show given that "
            "his wife does not.  (13)",
            "(b) A group of 20 students went on a picnic. 5 got sunburnt, 8 got bitten by mosquitoes and 10 returned home "
            "safely without any mishap. What is the probability that (i) a boy who got sunburnt was ignored by the "
            "mosquitoes, (ii) a mosquito-bitten boy also got sunburnt?  (15)"])
n.solution()
n.answer("(a)", "Let H = husband watches, W = wife watches: P(H) = 0.25, P(W) = 0.35, P(H | W) = 0.8.")
n.code([f"(i)  P(H ∩ W) = P(W) P(H | W) = 0.35 × 0.8 = {g(both)}",
        "(ii) P(H | W^c) = P(H ∩ W^c) / P(W^c) = [P(H) − P(H ∩ W)] / [1 − P(W)]",
        f"                = (0.25 − {g(both)}) / 0.65 = {g((0.25-both)/0.65)}   ← negative!"])
n.callout("trap", "As printed, the data are inconsistent: P(H ∩ W) = 0.28 is larger than P(H) = 0.25, which is "
          "impossible, so (ii) comes out negative. Write (i) = 0.28, then state that the given numbers cannot all be "
          "true. The question is the textbook problem with P(H) = 0.4, P(W) = 0.5, P(H | W) = 0.7 (Lec 5 p. 2); with "
          "those numbers (ii) = (0.4 − 0.35)/0.5 = 0.10. If P(H) were, e.g., 0.35, (ii) would be (0.35 − 0.28)/0.65 = 0.1077.",
          ["Ask the invigilator, or answer with a clearly stated corrected figure — examiners give credit for spotting it."])
n.answer("(b)", "Let S = sunburnt, M = bitten. Mishap = S ∪ M, so n(S ∪ M) = 20 − 10 = 10.")
n.code(["n(S ∩ M) = n(S) + n(M) − n(S ∪ M) = 5 + 8 − 10 = 3",
        "              M      M^c    Total",
        "S             3       2       5",
        "S^c           5      10      15",
        "Total         8      12      20",
        "(i)  P(M^c | S) = n(S ∩ M^c)/n(S) = 2/5 = 0.4",
        "(ii) P(S | M)   = n(S ∩ M)/n(M)   = 3/8 = 0.375"])

# ------------------------------------------------------------------ L6
n.lesson("Lesson 6 — Total Probability and Bayes' Theorem", "Lec 5 pp. 4–7")
n.h2("1. Theorem of Total Probability (Lec 5 p. 4)")
n.p("If A_{1}, …, A_{k} are mutually exclusive and exhaustive (a partition of S), then for any event D, "
    "D = (D ∩ A_{1}) ∪ … ∪ (D ∩ A_{k}) with disjoint pieces, so")
n.formula("P(D) = Σ P(A_{i}) P(D | A_{i})")
n.h2("2. Bayes' Theorem and its Proof (Lec 5 pp. 4–5)")
n.formula(["P(A | B) = P(B | A)P(A) / [P(B | A)P(A) + P(B | A^{c})P(A^{c})]",
           "P(A_{i} | D) = P(A_{i})P(D | A_{i}) / Σ_{j} P(A_{j})P(D | A_{j})"])
n.numbered(["From the definition, P(B | A) = P(A ∩ B)/P(A), so P(A ∩ B) = P(B | A)P(A) …(1).",
            "B = (B ∩ A) ∪ (B ∩ A^{c}) with disjoint parts, so P(B) = P(B | A)P(A) + P(B | A^{c})P(A^{c}) …(2) "
            "(total probability).",
            "P(A | B) = P(A ∩ B)/P(B); substitute (1) in the numerator and (2) in the denominator. ∎"])
n.callout("trap", "The slide's middle step (p. 5) writes P(B | A)P(A)/P(A) by a slip; the denominator there must be "
          "P(B). Write the proof in the three steps above.")
n.h2("3. The Table Method for Every Bayes Question")
n.code(["Source A_i | prior P(A_i) | likelihood P(D | A_i) | joint P(A_i)P(D | A_i) | posterior = joint / P(D)",
        "-----------------------------------------------------------------------------------------------",
        "   ...     |    ...      |         ...           |           ...           |        ...",
        "Total      |     1       |                       |     P(D) = Σ joint      |         1"])
n.callout("memorize", "Prior × likelihood = joint; Σ joint = P(D) (total probability); posterior = joint / P(D). "
          "The posteriors must add to 1 — use that as a check.")
n.h2("4. Worked Examples (Lec 5 pp. 5–6)")
n.h3("Problem 1 — blood test: 90 % detection, 5 % false positive, 1 % prevalence")
n.formula(f"P(D | +) = (0.01 × 0.90) / (0.01 × 0.90 + 0.99 × 0.05) = 0.009 / 0.0585 = {g(0.009/0.0585)}")
n.p("Only about 15 % of positives are diseased: a rare disease gives many false positives.")
n.h3("Problem 2 — coin chooses the container: I has 2 W 7 B, II has 5 W 6 B")
n.formula(f"P(H | W) = (½)(2/9) / [(½)(2/9) + (½)(5/11)] = {fr(F(1,2)*F(2,9)/(F(1,2)*F(2,9)+F(1,2)*F(5,11)))}")
n.h3("Practice problems at the end of Lecture 5 (pp. 6–7) — answers")
rows = []
for name, pri, lik, ask in (("Problem 3: car 30 %, walk 30 %, bus 40 %; late 3 %, 10 %, 7 %", [0.3, 0.3, 0.4], [0.03, 0.10, 0.07], ["car", "walk", "bus"]),
                            ("Problem 3 (centres): A 50 %, B 20 %, C 30 %; positive 2 %, 12 %, 6 %", [0.5, 0.2, 0.3], [0.02, 0.12, 0.06], ["A", "B", "C"]),
                            ("Problems 4 and 5: 40 %, 35 %, 25 %; 80 %, 70 %, 90 %", [0.4, 0.35, 0.25], [0.8, 0.7, 0.9], ["1st", "2nd", "3rd"])):
    pd = sum(a * b for a, b in zip(pri, lik))
    post = ", ".join(f"{s}: {g(a * b / pd)}" for s, a, b in zip(ask, pri, lik))
    rows.append([name, g(pd), post])
n.table(["Problem", "P(event)", "Posteriors"], rows, widths_cm=[7.8, 2.2, 7.2], font_size=9)
n.h2("5. Transferring a Ball — Total Probability (textbook, asked 2022-23 and 2023-24)")
n.p("A ball moved unseen from bag 1 to bag 2 creates two cases (the moved ball is W or B). Condition on the case, "
    "then use total probability for the second draw.")
n.exam_approach(["Define the partition (machines, parties, colour of the moved ball, guilty/innocent) and the observed event D.",
                 "Fill the prior × likelihood table; add the joints to get P(D).",
                 "Posterior of each source = its joint ÷ P(D); check that the posteriors sum to 1.",
                 "Read each percentage carefully and take complements where the event is the opposite one (\"did not vote\" "
                 "uses 1 − turnout)."])
# --- actual questions
pr, nv = [0.45, 0.40, 0.15], [0.35, 0.20, 0.50]
pn = sum(a * b for a, b in zip(pr, nv))
pr2, d2 = [0.30, 0.45, 0.25], [0.02, 0.03, 0.02]
pd2 = sum(a * b for a, b in zip(pr2, d2))
pg = 0.05 * 0.9 + 0.95 * 0.01
n.practice("Lesson 6", "(a) Actual — 2022-23 Q1(a) (TF p. 47). (b) Actual — 2023-24 Q1(b) (22 batch p. 1). "
           "(c) Actual — 2022-23 Q1(b) (TF p. 47). (d) Actual — 2023-24 Q1(c) (22 batch p. 1). "
           "(e) Actual — 2019-20 Q7(a) (TF p. 34).",
           ["(a) One bag contains 4 white and 3 black balls, a second bag 3 white and 5 black. One ball is drawn from the "
            "first bag and placed unseen in the second. What is the probability that a ball now drawn from the second "
            "bag is black?  (8)",
            "(b) Define the multiplication law of probability. Box A has 5 white and 7 red balls, box B has 3 white and "
            "8 red. One ball is transferred from A to B unseen, then a ball is drawn from B. What is the probability "
            "that it is red?  (12)",
            "(c) Machines B_{1}, B_{2}, B_{3} make 30 %, 45 % and 25 % of the products; 2 %, 3 % and 2 % of their products "
            "are defective. A finished product is selected at random and is defective. What is the probability that it "
            "was made by machine B_{i}, i = 1, 2, 3?  (15)",
            "(d) 45 % of a city support party A, 40 % party B and 15 % other parties C. In elections 65 % of A, 80 % of B "
            "and 50 % of C supporters vote. A person chosen at random did not vote in the last election. What is the "
            "probability that he is a supporter of A? B? C?  (17)",
            "(e) A truth serum judges 90 % of guilty suspects properly (10 % of the guilty are found innocent); innocent "
            "suspects are misjudged 1 % of the time. If the suspect comes from a group of which only 5 % have committed a "
            "crime and the serum indicates guilty, what is the probability that he is innocent?  (17)"])
n.solution()
n.answer("(a)", "Let W_{1}, B_{1} = colour of the moved ball; Bk = black drawn from bag 2.")
n.code(["Case W1: P(W1) = 4/7, bag 2 becomes 4W 5B → P(Bk | W1) = 5/9",
        "Case B1: P(B1) = 3/7, bag 2 becomes 3W 6B → P(Bk | B1) = 6/9",
        f"P(Bk) = (4/7)(5/9) + (3/7)(6/9) = 20/63 + 18/63 = {fr(F(38,63))} = {g(38/63)}"])
n.answer("(b)", "Multiplication law as in Lesson 5 §2. Then condition on the colour of the transferred ball:")
n.code(["Case W: P(W) = 5/12, box B becomes 4W 8R → P(R | W) = 8/12",
        "Case R: P(R) = 7/12, box B becomes 3W 9R → P(R | R) = 9/12",
        f"P(red from B) = (5/12)(8/12) + (7/12)(9/12) = 40/144 + 63/144 = {fr(F(103,144))} = {g(103/144)}"])
n.answer("(c)", "D = defective.")
n.table(["Machine", "Prior P(B_{i})", "P(D | B_{i})", "Joint", "P(B_{i} | D)"],
        [[f"B{i+1}", g(a), g(b), g(a*b), f"{g(a*b)}/{g(pd2)} = {g(a*b/pd2)}"] for i, (a, b) in enumerate(zip(pr2, d2))]
        + [["Total", "1", "", f"P(D) = {g(pd2)}", "1"]], widths_cm=[2.5, 3, 3, 3.5, 5.2])
n.formula(f"P(B1 | D) = {g(0.006/pd2)}, P(B2 | D) = {g(0.0135/pd2)}, P(B3 | D) = {g(0.005/pd2)}  (= 12/49, 27/49, 10/49)")
n.answer("(d)", "N = did not vote; P(N | A) = 1 − 0.65 = 0.35, P(N | B) = 0.20, P(N | C) = 0.50.")
n.table(["Party", "Prior", "P(N | party)", "Joint", "P(party | N)"],
        [[s, g(a), g(b), g(a*b), f"{g(a*b)}/{g(pn)} = {g(a*b/pn)}"] for s, a, b in zip("ABC", pr, nv)]
        + [["Total", "1", "", f"P(N) = {g(pn)}", "1"]], widths_cm=[2.5, 3, 3, 3.5, 5.2])
n.formula(f"P(A | N) = {g(0.1575/pn)}, P(B | N) = {g(0.08/pn)}, P(C | N) = {g(0.075/pn)}")
n.answer("(e)", "G = guilty (prior 0.05), I = innocent (0.95); J = serum says guilty: P(J | G) = 0.90, P(J | I) = 0.01.")
n.code([f"P(J) = 0.05 × 0.90 + 0.95 × 0.01 = 0.045 + 0.0095 = {g(pg)}",
        f"P(I | J) = 0.0095 / {g(pg)} = {g(0.0095/pg)}"])
n.formula(f"P(innocent | judged guilty) ≈ {g(0.0095/pg, 3)}")

n.quick_notes("Quick Notes — Conditional Probability and Bayes", "Revision points for Lessons 5–6.", [
    ("L5 · Conditional Probability", ["P(A | B) = P(A ∩ B)/P(B). Multiplication law: P(A ∩ B) = P(A)P(B | A).",
                                      "Three events: P(A_{1})P(A_{2} | A_{1})P(A_{3} | A_{1} ∩ A_{2}).",
                                      "TV couple (0.4, 0.5, 0.7): both 0.35, P(W | H) = 0.875, at least one 0.55.",
                                      "Check P(A ∩ B) ≤ min(P(A), P(B)) — 2015-16 Q8(a) data fail this test.",
                                      "Picnic: both = 5 + 8 − 10 = 3 → 2/5 and 3/8."]),
    ("L6 · Total Probability and Bayes", ["P(D) = Σ P(A_{i})P(D | A_{i}); P(A_{i} | D) = joint/P(D).",
                                          "Proof: definition → total probability → substitute.",
                                          "Blood test 0.15; machines 12/49, 27/49, 10/49; parties 0.504, 0.256, 0.24 (P(N) = 0.3125).",
                                          "Truth serum: P(J) = 0.0545, P(innocent | J) = 0.1743.",
                                          "Transfer: 4W3B → 3W5B gives 38/63; 5W7R → 3W8R gives 103/144."])])
n.save()
print("saved", n.out_path)
