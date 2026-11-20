"""MATH243_KKS_Probability_Basics_Notes.docx — Lectures 1, 2, 3 & 4 (L1–L4)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from math import comb

from common import exam_map, new
from m243 import PROB, fr, g

QPDF = r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2\MATH 243\TF questions\MATH 243 All Merged Questions.pdf"

n = new("KKS", "Probability Basics: Sets, Counting, Rules, Odds and Joint Tables",
        "MATH243_KKS_Probability_Basics_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "counting, independence and set-rule questions"),
              ("Lesson 1 — Sample Space, Events and the Probability Rules", "set operations, De Morgan, axioms, addition rule"),
              ("Lesson 2 — Counting: Permutations, Combinations, Classical Probability", "nPr, nCr, committees, cards, balls"),
              ("Lesson 3 — Multiplication Rule, Independence and Odds", "independent vs dependent, circuits, odds"),
              ("Lesson 4 — Joint Probability and the 2 × 2 Table", "joint/marginal table, newspaper and machine problems"),
              ("Quick Notes — Probability Basics", "revision bullets")],
    source_note="Page numbers refer to the KKS Sir lecture PDFs: Lecture 1.pdf (6 pp.), Lecture 2.pdf (9 pp.) and "
                "Lecture 3 & 4.pdf (12 pp.), written as Lec 1 p. 3 etc. \"TF p.\" is the page of MATH 243 All Merged "
                "Questions.pdf; \"22 batch p.\" is the page of MATH 243 (22 batch).pdf (the 2023-24 paper).")

# ------------------------------------------------------------------ exam map
n.h1("Exam Map — What the TF Papers Ask")
st = exam_map(n, "k1")
n.callout("focus", f"{st['n']} questions ({st['marks']} marks) in 11 papers. These are short parts (6–12 marks) "
          "that usually open Section A: counting with nCr, P(at least one) = 1 − P(none), and the question "
          "\"can two events be both mutually exclusive and independent?\" (2023-24). Learn the complement trick and "
          "the series/parallel rule first; they also feed every later lesson.")

# ------------------------------------------------------------------ L1
n.lesson("Lesson 1 — Sample Space, Events and the Probability Rules", "Lec 1 pp. 2–6 · Lec 2 pp. 1–2")
n.h2("1. What Probability Measures (Lec 1 p. 2)")
n.p("Probability measures uncertainty. It is a number between 0 and 1: 0 means the event cannot happen, 1 means it "
    "certainly happens. We use it when the exact outcome of an experiment cannot be predicted but the set of "
    "possible outcomes is known.")
n.table(["Experiment", "Event", "Probability"],
        [["Toss a fair coin", "Head", "1/2 = 0.5"],
         ["Roll a die", "a 4  /  an even number", "1/6  /  3/6 = 0.5"],
         ["Class of 30 (12 girls, 18 boys)", "select a girl / a boy", "12/30 = 0.4  /  18/30 = 0.6"],
         ["MCQ with 4 options, guessing", "correct / wrong", "1/4 = 0.25  /  3/4 = 0.75"]],
        widths_cm=[5.5, 5.5, 6.2])
n.h2("2. Random Experiment, Sample Space and Events (Lec 2 p. 1, Lec 1 pp. 2–3)")
n.p("A **random experiment** has three properties: (a) all possible outcomes are known in advance; (b) the outcome "
    "of any one performance is not known in advance; (c) it can be repeated under identical conditions "
    "(coin toss, die roll, drawing a card, choosing a student at random).")
n.bullets(["**Sample space S** — the set of all possible outcomes. Die: S = {1, 2, 3, 4, 5, 6}; card: the 52 cards; "
           "baby's sex: {Male, Female}; coin: {H, T}.",
           "**Event** — any subset of S. Even number on a die: A = {2, 4, 6}; head: B = {H}; a king: C = {K♥, K♦, K♣, K♠}.",
           "**Equally likely events** — events with the same chance of occurring (head and tail of a fair coin; "
           "faces 1 and 2 of a fair die)."])
n.h2("3. Set Operations (Lec 1 pp. 3–5)")
n.p("With S = {1, …, 6}, A = {2, 4, 6} (even) and B = {1, 2} (less than 3):")
n.table(["Operation", "Meaning", "Example"],
        [["A ∪ B", "A or B or both", "{1, 2, 4, 6}"],
         ["A ∩ B", "A and B together", "{2}"],
         ["A^{c}", "everything in S except A", "{1, 3, 5}"],
         ["∅", "empty set (impossible event)", "rolling a 7"],
         ["Disjoint (mutually exclusive)", "A ∩ B = ∅ — cannot happen together", "{1} and {3}; {1, 2} and {3, 4}"]],
        widths_cm=[4.2, 6.5, 6.5])
n.h3("De Morgan's laws (Lec 2 p. 2)")
n.formula(["(A ∪ B)^{c} = A^{c} ∩ B^{c}", "(A ∩ B)^{c} = A^{c} ∪ B^{c}"])
n.p("Example 1: S = {1, …, 6}, A = {1, 2, 3, 4}, B = {3, 4, 5, 6}. A ∪ B = S, so (A ∪ B)^{c} = ∅; check: "
    "A^{c} = {5, 6}, B^{c} = {1, 2}, A^{c} ∩ B^{c} = ∅ ✓.  Example 2: S = {a, b, c, d, e}, A = {a, b, c}, B = {b, d}: "
    "A ∩ B = {b}, (A ∩ B)^{c} = {a, c, d, e}; A^{c} ∪ B^{c} = {d, e} ∪ {a, c, e} = {a, c, d, e} ✓.")
n.h2("4. The Axioms and the Addition Rule (Lec 1 pp. 4–6)")
n.numbered(["**Non-negativity:** P(A) ≥ 0 (P(7 on a die) = 0, never negative).",
            "**Total probability:** P(S) = 1 (P(1) + … + P(6) = 1).",
            "**Additivity for disjoint events:** P(A ∪ B) = P(A) + P(B) when A ∩ B = ∅ (P(1 or 2) = 1/6 + 1/6 = 2/6)."])
n.formula(["P(A ∪ B) = P(A) + P(B) − P(A ∩ B)", "P(A^{c}) = 1 − P(A)"])
n.p("Die: P(A ∪ B) = 3/6 + 2/6 − 1/6 = 4/6. Cricket (Lec 1 p. 6): P(play) = 0.4, P(watch) = 0.7, P(both) = 0.35 → "
    "P(play or watch) = 0.4 + 0.7 − 0.35 = 0.75.")
n.callout("trap", "Add probabilities only for disjoint events. For overlapping events the intersection is counted "
          "twice, so subtract it once. \"At least one\" is almost always easier as 1 − P(none).")
n.exam_approach(["Write S and the event as sets (or as counts n(A), n(S)).",
                 "Decide: union (or) → addition rule; intersection (and) → multiplication rule (Lesson 3); "
                 "\"not\" or \"at least one\" → complement.",
                 "Use De Morgan to turn P(neither) into 1 − P(A ∪ B)."])
n.practice("Lesson 1", "(a) Adapted — Lec 1 p. 6. (b) Adapted — Lec 3 & 4 p. 7. (c) Constructed.",
           ["(a) 40 % of students play cricket, 70 % watch it and 35 % do both. What percentage do neither?",
            "(b) 60 % study Mathematics, 50 % Physics, 30 % both. Find P(M or P), P(M but not P), P(neither).",
            "(c) Show with De Morgan that P(A^{c} ∩ B^{c}) = 1 − P(A) − P(B) + P(A ∩ B)."])
n.solution()
n.answer("(a)", "P(play ∪ watch) = 0.4 + 0.7 − 0.35 = 0.75, so P(neither) = 1 − 0.75 = 0.25 → 25 %.")
n.answer("(b)", "P(M ∪ P) = 0.6 + 0.5 − 0.3 = 0.8; P(M ∩ P^{c}) = P(M) − P(M ∩ P) = 0.6 − 0.3 = 0.3; "
         "P(neither) = 1 − 0.8 = 0.2.")
n.answer("(c)", "A^{c} ∩ B^{c} = (A ∪ B)^{c}, so P(A^{c} ∩ B^{c}) = 1 − P(A ∪ B) = 1 − [P(A) + P(B) − P(A ∩ B)].")

# ------------------------------------------------------------------ L2
n.lesson("Lesson 2 — Counting: Permutations, Combinations, Classical Probability", "Lec 2 pp. 2–8")
n.h2("1. Permutations — Order Matters (Lec 2 pp. 2–3)")
n.formula("nPr = n! / (n − r)!")
n.table(["Example", "Working", "Answer"],
        [["Arrange 3 books A, B, C", "3P3 = 3!/0!", "6 (ABC, ACB, BAC, BCA, CAB, CBA)"],
         ["Select and arrange 2 of 4 students", "4P2 = 4!/2!", "12"],
         ["President, VP, secretary from 5 members", "5P3 = 5!/2!", "60"]], widths_cm=[6.2, 4.5, 6.5])
n.h2("2. Combinations — Order Does Not Matter (Lec 2 pp. 3–5)")
n.formula("nCr = n! / (r! (n − r)!)")
n.table(["Problem", "Working", "Answer"],
        [["Choose 2 of 3 books", "3C2", "3"],
         ["Committee of 3 from 5", "5C3", "10"],
         ["3 men from 8 and 2 women from 12", "8C3 × 12C2 = 56 × 66", "3696"],
         ["5 from 6 men + 4 women, at least 1 woman", "10C5 − 6C5 = 252 − 6", "246"],
         ["5 from 6 M + 4 W, ≥ 1 woman and ≥ 2 men", "6C2·4C3 + 6C3·4C2 + 6C4·4C1 = 60 + 120 + 60", "240"],
         ["5-card hands with exactly one ace", "4C1 × 48C4 = 4 × 194580", "778320"]], widths_cm=[6.2, 6.5, 4.5])
n.callout("memorize", "\"Independent choices multiply\" (men AND women: 8C3 × 12C2). \"At least\" = total − the "
          "complement case, or add the separate splits.")
n.h2("3. Approaches to Probability (Lec 2 p. 5)")
n.bullets(["**Classical** — equally likely outcomes: P(A) = n(A)/n(S).",
           "**Relative frequency** — long-run proportion of times A occurs in repeated trials.",
           "**Subjective** — a personal degree of belief (used when no repetition is possible)."])
n.formula("P(A) = n(A) / n(S)   (classical)")
n.h2("4. Worked Examples (Lec 2 pp. 5–8)")
n.bullets(["Heart from 52 cards: 13/52 = 1/4.",
           "Bag 4 white, 6 red: P(R) = 6/10 = 3/5, P(W) = 4/10 = 2/5 → not equally likely.",
           "Die: P(even) = 3/6, P(> 4) = 2/6, P(odd and < 4) = 2/6; even and odd are equally likely (both 1/2).",
           "Two children S = {BB, BG, GB, GG}: P(both boys) = 1/4, P(at least one girl) = 3/4, P(at most one boy) = 3/4, "
           "P(exactly one girl) = P(exactly one boy) = 1/2, P(same sex) = 1/2."])
n.exam_approach(["Decide whether order matters (arrangement → P; selection → C).",
                 "Count the sample space: n(S) = NCr for drawing r items at once.",
                 "Count the favourable cases as a product of C's, one per colour/type.",
                 "For \"at least one\", use 1 − P(none). Simplify the fraction and give a decimal."])
q20 = comb(20, 3)
n.practice("Lesson 2", "(a) Actual — 2014-15 Q8(a) (TF p. 11). (b) Actual — 2013-14 Q7(b)(i) (TF p. 8). "
           "(c) Adapted — Lec 3 & 4 p. 7.",
           ["(a) A box contains 8 red, 3 white and 9 blue balls. Three balls are drawn at random. Find the probability "
            "that (i) all 3 are red, (ii) 2 are red and 1 is white, (iii) at least 1 is white.  (12)",
            "(b) 3 cards are drawn one after another without replacement from a deck of 52. Find the probability that "
            "they come from different suits.  (7)",
            "(c) A bag has 3 red, 4 green and 5 blue balls; two are drawn. Find P(both red), P(one red one green), "
            "P(at least one blue)."])
n.solution()
n.answer("(a)", f"Total balls 20, n(S) = 20C3 = {q20}.")
n.code([f"(i)   P(3 red)        = 8C3 / 20C3          = {comb(8,3)}/{q20}  = {fr(F(comb(8,3),q20))}  = {g(comb(8,3)/q20)}",
        f"(ii)  P(2 red, 1 white) = 8C2 × 3C1 / 20C3  = {comb(8,2)*3}/{q20} = {fr(F(comb(8,2)*3,q20))}  = {g(comb(8,2)*3/q20)}",
        f"(iii) P(no white)     = 17C3 / 20C3         = {comb(17,3)}/{q20} = {fr(F(comb(17,3),q20))}",
        f"      P(at least 1 white) = 1 − {fr(F(comb(17,3),q20))} = {fr(1-F(comb(17,3),q20))} = {g(1-comb(17,3)/q20)}"])
n.answer("(b)", "Sequential multiplication rule: the first card can be anything (52/52); the second must avoid the "
         "first card's suit (39 of the remaining 51); the third must avoid both suits (26 of 50).")
n.formula(f"P = (52/52)(39/51)(26/50) = {fr(F(39*26,51*50))} = {g(39*26/(51*50))}")
n.answer("(c)", "12C2 = 66. P(both red) = 3C2/66 = 3/66 = 1/22; P(one red, one green) = (3C1 × 4C1)/66 = 12/66 = 2/11; "
         "P(at least one blue) = 1 − 7C2/66 = 1 − 21/66 = 15/22.")

# ------------------------------------------------------------------ L3
n.lesson("Lesson 3 — Multiplication Rule, Independence and Odds", "Lec 2 pp. 8–9 · Lec 3 & 4 pp. 1–6")
n.h2("1. Multiplication Rule (Lec 2 pp. 8–9)")
n.formula(["Independent:  P(A ∩ B) = P(A) · P(B)", "Dependent:   P(A ∩ B) = P(A) · P(B | A)"])
n.p("Coin and die: P(H ∩ 4) = (1/2)(1/6) = 1/12 — the same as counting 1 of the 12 outcomes. Without replacement "
    "(3 red, 2 blue): P(red then red) = (3/5)(2/4) = 3/10 = 3C2/5C2. Two aces without replacement: (4/52)(3/51) = 1/221.")
n.h2("2. Independent vs Mutually Exclusive ★ (textbook, asked 2023-24 Q1(a))")
n.table(["", "Mutually exclusive (disjoint)", "Independent"],
        [["Definition", "A ∩ B = ∅, so P(A ∩ B) = 0", "P(A ∩ B) = P(A)P(B); P(B | A) = P(B)"],
         ["Meaning", "if A happens, B cannot", "A happening does not change the chance of B"],
         ["Addition", "P(A ∪ B) = P(A) + P(B)", "P(A ∪ B) = P(A) + P(B) − P(A)P(B)"]], widths_cm=[3, 7, 7.2])
n.callout("answer", "Two events with positive probabilities cannot be both mutually exclusive and independent. If they "
          "are mutually exclusive, P(A ∩ B) = 0; if independent, P(A ∩ B) = P(A)P(B) > 0 when P(A), P(B) > 0. The two "
          "conditions agree only if P(A) = 0 or P(B) = 0. Intuitively, disjoint events are strongly dependent: "
          "knowing A happened tells us B did not, so P(B | A) = 0 ≠ P(B). Example: one die, A = {1}, B = {2}: "
          "P(A ∩ B) = 0 but P(A)P(B) = 1/36.")
n.h2("3. Several Independent Events — P(at least one) and Circuits (textbook)")
n.formula(["P(at least one of A_{1}, …, A_{k}) = 1 − Π (1 − P(A_{i}))",
           "Series: works if all work  ·  Parallel: fails only if all branches fail"])
n.figure_from_pdf(QPDF, 20, "Figure 3.1 — Circuit of 2016-17 Q7(a): four parallel paths with failure probabilities (TF p. 20)",
                  clip=(0.36, 0.69, 0.64, 0.84), width_cm=6.5)
n.h2("4. Odds (Lec 3 & 4 pp. 1–2)")
n.formula(["Odds in favour of A = P(A) / P(A^{c}) = n(A) : n(A^{c})", "If odds in favour are a : b, P(A) = a/(a + b)"])
n.bullets(["Odds in favour and odds against are reciprocals.",
           "Red:blue odds 3 : 7 → P(red) = 3/10 = 0.3, P(blue) = 0.7. Odds 5 : 3 → P(A) = 5/8.",
           "P(win) = 0.2 → odds against = 0.8/0.2 = 4 : 1 (for every 1 chance of winning there are 4 of losing)."])
n.h3("Worked example — X and Y solve a problem (Lec 3 & 4 pp. 2–5)")
n.p("Odds against X are 8 : 6 → P(X) = 6/14 = 3/7, P(X^{c}) = 4/7. Odds in favour of Y are 14 : 16 → P(Y) = 7/15, "
    "P(Y^{c}) = 8/15.")
n.table(["Asked", "Independent case", "Dependent case, P(Y | X) = 0.6"],
        [["Both solve", "(3/7)(7/15) = 1/5", "(3/7)(3/5) = 9/35"],
         ["At least one (= either)", "1 − (4/7)(8/15) = 73/105", "3/7 + 7/15 − 9/35 = 67/105"],
         ["Neither", "(4/7)(8/15) = 32/105", "1 − 67/105 = 38/105"],
         ["Exactly one", "73/105 − 21/105 = 52/105", "67/105 − 27/105 = 40/105"]], widths_cm=[4, 6.2, 7])
n.callout("trap", "In the dependent case you may not multiply P(X^{c})P(Y^{c}) — use the complement of the union. "
          "\"Odds against 8 : 6\" means P(fail) = 8/14, not 8/6.")
n.exam_approach(["Turn odds into probabilities first: a : b → a/(a + b).",
                 "Independent → multiply; at least one → 1 − product of failures.",
                 "Circuits: series branch works with Π p_{works}; a parallel block fails with Π q_{fails}.",
                 "Dependent → use P(A)P(B | A) and the addition rule."])
qs = 1 - 0.99 * 0.99
pfail = 0.02 * qs * qs * 0.02
n.practice("Lesson 3", "(a) Actual — 2023-24 Q1(a) (22 batch p. 1). (b) Actual — 2011-12 Q7(b)(ii) (TF p. 2). "
           "(c) Actual — 2016-17 Q7(a) (TF p. 20).",
           ["(a) Can two events be mutually exclusive and independent simultaneously? Justify your answer.  (6)",
            "(b) The probabilities that A, B and C can solve a problem are 3/7, 2/3 and 4/5. If all try independently, "
            "find the probability that the problem will be solved.  (8)",
            "(c) The circuit (Figure 3.1) operates iff there is a path of functional devices from left to right. Devices "
            "fail independently with the probabilities shown. What is the probability that the circuit does not operate?  (10)"])
n.solution()
n.answer("(a)", "No (unless one event has probability 0) — model answer in the callout of §2.")
n.answer("(b)", "Solved means at least one solves it.")
n.formula(f"P = 1 − (1 − 3/7)(1 − 2/3)(1 − 4/5) = 1 − (4/7)(1/3)(1/5) = 1 − 4/105 = {fr(1-F(4,105))} ≈ {g(1-4/105)}")
n.answer("(c)", "The four paths are in parallel, so the circuit fails only if every path fails.")
n.code(["Path 1 (one device):  P(fail) = 0.02",
        f"Path 2 (two in series): works only if both work = 0.99 × 0.99 = 0.9801 → P(fail) = 1 − 0.9801 = {g(qs)}",
        f"Path 3 (two in series): P(fail) = {g(qs)}",
        "Path 4 (one device):  P(fail) = 0.02",
        f"P(circuit does not operate) = 0.02 × {g(qs)} × {g(qs)} × 0.02 = {pfail:.4e}"])
n.formula(f"P(not operate) ≈ 1.584 × 10^{{−7}}")

# ------------------------------------------------------------------ L4
n.lesson("Lesson 4 — Joint Probability and the 2 × 2 Table", "Lec 3 & 4 pp. 6–12")
n.h2("1. Joint Probability (Lec 3 & 4 p. 6)")
n.p("Joint probability P(A ∩ B) is the probability that A and B happen at the same time: P(A)P(B) if independent, "
    "P(A)P(B | A) (or P(B)P(A | B)) if dependent.")
n.h2("2. The Joint Probability Table (Lec 3 & 4 p. 8)")
n.code(["            Y = yes        Y = no         Total",
        "X = yes   P(X ∩ Y)     P(X ∩ Y^c)      P(X)",
        "X = no    P(X^c ∩ Y)   P(X^c ∩ Y^c)    P(X^c)",
        "Total       P(Y)         P(Y^c)          1"])
n.p("Each cell is a joint probability; the row and column totals are the marginal probabilities. Fill the table from "
    "the given numbers, then read any answer from it. The same table can hold counts n(·) that are divided by n(S).")
n.h2("3. Worked Problems (Lec 3 & 4 pp. 8–11)")
n.h3("Problem 1 — newspapers: 100 employees, 75 read English, 50 Bangla, 40 both")
n.code(["            E      E^c    Total",
        "B          40      10      50",
        "B^c        35      15      50",
        "Total      75      25     100"])
n.p("(a) P(E) = 0.75; (b) P(E ∪ B) = 0.75 + 0.50 − 0.40 = 0.85; (c) none: 1 − 0.85 = 0.15; (d) Bangla only: "
    "(50 − 40)/100 = 0.10.")
n.h3("Problem 2 — ring and necklace")
n.p("P(R) = 0.20, P(N) = 0.30, P(neither) = 0.60: P(R ∪ N) = 1 − 0.60 = 0.40; P(R ∩ N) = 0.20 + 0.30 − 0.40 = 0.10.")
n.h3("Problem 3 — 10 men and 20 women, half of each with brown eyes")
n.p("n(M ∩ B) = 5, n(B) = 15: P(M ∪ B) = 10/30 + 15/30 − 5/30 = 20/30 = 2/3. (The slide writes P(M) as 1/10 by a slip; "
    "it is 10/30 = 1/3, and the final 2/3 is correct.)")
n.h3("Problem 4 — machines A (40 %) and B (60 %), defective 5 % and 10 %")
n.code(["               Defective (Y)     Good (Y^c)       Total",
        "Machine A    0.4×0.05 = 0.02   0.4×0.95 = 0.38    0.40",
        "Machine B    0.6×0.10 = 0.06   0.6×0.90 = 0.54    0.60",
        "Total            0.08              0.92           1"])
n.p("P(defective) = 0.08; P(A | defective) = 0.02/0.08 = 0.25; P(good and from B) = 0.54. This is already Bayes' "
    "theorem (Lesson 6) in table form.")
n.callout("note", "Problem 5 of the lecture (two pens from 3 blue, 2 red, 3 green → joint pmf of X = blue, Y = red) "
          "is the discrete joint distribution of Lesson 10 in the Joint Distributions note; 2023-24 Q2(b) asks the "
          "same problem with red/blue/black pens.")
n.exam_approach(["Draw the 2 × 2 table with totals; put the given numbers in.",
                 "Fill the gaps by subtraction (each row and column must add up).",
                 "Answer \"or\" with the addition rule, \"only\" with a single cell, \"given\" with cell ÷ total."])
n.practice("Lesson 4", "(a) Constructed. (b) Adapted — Lec 3 & 4 p. 10.",
           ["(a) In a class 45 % like tea, 35 % like coffee and 25 % like neither. Find P(both) and P(tea only).",
            "(b) Machine A makes 30 % and B 70 % of items; 4 % of A's and 2 % of B's items are defective. Build the joint "
            "table and find P(defective) and P(A | defective)."])
n.solution()
n.answer("(a)", "P(T ∪ C) = 1 − 0.25 = 0.75; P(T ∩ C) = 0.45 + 0.35 − 0.75 = 0.05; P(tea only) = 0.45 − 0.05 = 0.40.")
n.answer("(b)", "Cells: A ∩ D = 0.3 × 0.04 = 0.012, A ∩ D^{c} = 0.288, B ∩ D = 0.7 × 0.02 = 0.014, B ∩ D^{c} = 0.686. "
         "P(D) = 0.012 + 0.014 = 0.026; P(A | D) = 0.012/0.026 = 0.4615.")

# ------------------------------------------------------------------ quick notes
n.quick_notes("Quick Notes — Probability Basics", "Revision points for Lessons 1–4.", [
    ("L1 · Events and Rules", ["Random experiment: outcomes known, result unknown, repeatable. S = all outcomes; event ⊆ S.",
                               "De Morgan: (A ∪ B)^{c} = A^{c} ∩ B^{c}; (A ∩ B)^{c} = A^{c} ∪ B^{c}.",
                               "Axioms: P(A) ≥ 0, P(S) = 1, additivity for disjoint events.",
                               "P(A ∪ B) = P(A) + P(B) − P(A ∩ B); P(A^{c}) = 1 − P(A)."]),
    ("L2 · Counting", ["nPr = n!/(n − r)! (order matters); nCr = n!/(r!(n − r)!) (selection).",
                       "P(A) = n(A)/n(S); independent choices multiply; at least = total − complement.",
                       "Box 8R 3W 9B, 3 drawn: 14/285, 7/95, 23/57. Different suits: 169/425 = 0.3976."]),
    ("L3 · Multiplication, Independence, Odds", ["Independent: P(A ∩ B) = P(A)P(B); dependent: P(A)P(B | A).",
                                                 "Mutually exclusive + independent only if one probability is 0.",
                                                 "P(at least one) = 1 − Π(1 − p_{i}); parallel fails if all fail.",
                                                 "Odds a : b in favour → P = a/(a + b)."]),
    ("L4 · Joint Table", ["2 × 2 table of joint probabilities; margins = totals.",
                          "Machine A/B: cells P(machine)·P(defect | machine); P(A | D) = cell / column total."])])
n.save()
print("saved", n.out_path)
