"""Hakim Sir — Lec05 The Regulars → CSE211_Hakim_Regular_Languages_Notes.docx (Lessons 10–14). Checks: re_designs.py."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import new_notes, exam_map_rows, fig, PRACT_NOTE, PDF
from re_designs import thompson, gnfa, DFA_RE, option_report, OPTS, star_flaw_demo

n = new_notes("H", "Regular Operations, Closure Properties and Regular Expressions",
              "CSE211_Hakim_Regular_Languages_Notes.docx")
K = (0.03, 0.11, 0.97, 0.93)


def S(x):  # Kleene star as ∗ so it never collides with italic markup
    return x.replace("*", "∗").replace("|", " ∪ ")


def thom_table(r, sig, title):
    nf, e = thompson(r, sig)
    lines = [f"{title}: start {nf.start}, accept {sorted(nf.accept)[0]}  (ε written as ε)"]
    row = []
    for (p, a, q) in e:
        row.append(f"{p} −{a or 'ε'}→ {q}")
    for i in range(0, len(row), 5):
        lines.append("   " + "    ".join(row[i:i + 5]))
    n.code(lines, size=8.5)


n.front_matter(
    contents=[
        ("Exam Map — What the TF Papers Ask", "closure proofs, REs and conversions in every paper"),
        ("Lesson 10 — Regular Operations and Closure under ∪, ∘, ∗", "definitions, NFA constructions, ∅∗ = {ε}, the star-construction trap"),
        ("Lesson 11 — More Closure: Complement, Intersection, Difference, Reverse", "flip a DFA (not an NFA), product construction"),
        ("Lesson 12 — Regular Expressions", "syntax, semantics, writing, describing, simplifying, choosing"),
        ("Lesson 13 — RE → NFA (Thompson's Construction)", "base cases + plug-in constructions"),
        ("Lesson 14 — DFA → RE (GNFA State Ripping) and Kleene's Theorem", "GNFA rules, the rip formula, proofs"),
        ("Quick Notes — Regular Languages", "revision bullets + key diagrams"),
    ],
    source_note=("Slide numbers refer to the PDF pages of Lec05 - The Regulars.pdf (111 pages). Every regular expression in "
                 "the solutions was compared by a program with the language definition on all strings up to length 10 "
                 "(3–6 for larger alphabets); GNFA results and Thompson NFAs were generated and tested the same way. "
                 "RE notation: ∪ union, ∗ star, ⁺ one-or-more, Σ = (0 ∪ 1) or (a ∪ b). " + PRACT_NOTE))

n.h1("Exam Map — What the TF Papers Ask")
rows, cnt = exam_map_rows("H", {10, 11, 12, 13, 14})
n.table(["Session", "Questions on regular operations, closure and REs"], rows, widths_cm=[2.6, 14.6], font_size=8)
n.callout("focus", ("The richest block of Section A (~25 % of its marks). Most repeated: (1) **write / choose / simplify "
                    "REs** — every paper; 'which option is correct' in 2023-24, 2022-23, 2021-22; (2) **closure "
                    "constructions explained** — union δ (2019-20, 2021-22), star construction and its flawed variant "
                    "(2023-24, Jan-2020, 2016-17), concatenation (2023-24, 2016-17, 2011-12, 2012-13); (3) **complement "
                    "by flipping a DFA, and why it fails for an NFA** — 2022-23, 2021-22, 2017-18, 2015-16; (4) ∅∗ = {ε} "
                    "— 2022-23, 2021-22, 2016-17, Jan-2020; (5) RE → NFA by basic principles and DFA → RE."))

# ---------------------------------------------------------------- L10
n.lesson("Lesson 10 — Regular Operations and Closure under ∪, ∘, ∗", "Slides 1–37 (Lec05)")
n.h2("1. The Three Regular Operations (sl. 4–13)")
n.formula(["A ∪ B = { x | x ∈ A or x ∈ B }", "A ∘ B = { xy | x ∈ A and y ∈ B }",
           "A∗ = { x1x2…xk | k ≥ 0 and each xi ∈ A }"])
n.p("Example (sl. 8–11): A = {good, bad}, B = {boy, girl}: A ∪ B has 4 strings, A ∘ B = {goodboy, goodgirl, badboy, "
    "badgirl}; {ab, c}∗ = {ε, ab, c, abab, abc, cab, cc, …}. Operations on languages are operations on sets of strings, "
    "not on machines; closure proofs ask whether a machine for the result can be built (sl. 6).")
n.callout("answer", ("Why is ∅∗ = {ε}? (2022-23 Q3(c), 2021-22 Q3(a), 2016-17 Q2(c)) By definition A∗ = {ε} ∪ A ∪ AA ∪ … "
                     "is the set of concatenations of k ≥ 0 strings of A. Choosing k = 0 concatenates nothing, which gives "
                     "the empty string; this needs no member of A, so ε ∈ A∗ for every A, even A = ∅. For k ≥ 1 we must pick "
                     "a string from ∅ — impossible — so those terms are empty. Hence ∅∗ = {ε} ∪ ∅ ∪ ∅ ∪ … = {ε} (sl. 12–13). "
                     "Analogy: x⁰ = 1 even for x = 0; the empty product is the identity of concatenation, which is ε. "
                     "Consequence: the star NFA must accept ε, which is why its new start state is accepting."))
n.h2("2. Regular Languages and Closure (sl. 14–18)")
n.p("A language is **regular** if some DFA (equivalently, some NFA) recognises it. A class is **closed** under an operation "
    "if applying it to members gives a member (ℕ is closed under +, not under −). Theorem: regular languages are closed "
    "under ∪, ∘ and ∗; the proofs use NFAs because ε-moves make them simple (sl. 16–17).")
n.h2("3. Union (sl. 19–24)")
fig(n, "H5", 23, "Figure 10.1 — Union: new start state with ε-moves to N1 and N2 (sl. 23)", clip=(0.1, 0.1, 0.9, 0.8), width_cm=8)
n.code(["N1 = (Q1, Σ, δ1, q1, F1), N2 = (Q2, Σ, δ2, q2, F2) → N = (Q, Σ, δ, q0, F) for A1 ∪ A2:",
        "  Q = {q0} ∪ Q1 ∪ Q2        q0 new start        F = F1 ∪ F2",
        "            ⎧ δ1(q, a)      q ∈ Q1",
        "  δ(q, a) = ⎨ δ2(q, a)      q ∈ Q2",
        "            ⎪ {q1, q2}      q = q0 and a = ε",
        "            ⎩ ∅             q = q0 and a ≠ ε"])
n.h2("4. Concatenation (sl. 25–29)")
fig(n, "H5", 27, "Figure 10.2 — Concatenation: ε from every accepting state of N1 to the start of N2 (sl. 27)", clip=K, width_cm=11)
n.code(["N for A1 ∘ A2:  Q = Q1 ∪ Q2,  start q1,  F = F2",
        "            ⎧ δ1(q, a)            q ∈ Q1, q ∉ F1",
        "  δ(q, a) = ⎨ δ1(q, a)            q ∈ F1, a ≠ ε",
        "            ⎪ δ1(q, a) ∪ {q2}     q ∈ F1, a = ε",
        "            ⎩ δ2(q, a)            q ∈ Q2"])
n.p("At an accepting state of N1 the machine *guesses* the split point w = xy (sl. 29).")
n.h2("5. Star (sl. 30–33)")
fig(n, "H5", 32, "Figure 10.3 — Star: new accepting start state; ε from accepting states back to the old start (sl. 32)", clip=K, width_cm=9)
n.code(["N for A1∗:  Q = {q0} ∪ Q1,  start q0 (new),  F = {q0} ∪ F1",
        "            ⎧ δ1(q, a)            q ∈ Q1, q ∉ F1",
        "  δ(q, a) = ⎨ δ1(q, a)            q ∈ F1, a ≠ ε",
        "            ⎪ δ1(q, a) ∪ {q1}     q ∈ F1, a = ε      ← jump back: start the next piece",
        "            ⎪ {q1}                q = q0, a = ε      ← enter N1",
        "            ⎩ ∅                   q = q0, a ≠ ε      ← q0 reads nothing itself"])
n.callout("trap", ("Why a NEW start state? Making the old start q1 accepting (instead of adding q0) breaks the "
                   "construction whenever N1 can return to q1 after reading a non-empty string that is not in A. Example "
                   "(checked by program): N1 has q1 looping on a and q1 −b→ q2 (accepting); A = a∗b. A∗ = (a∗b)∗ — every "
                   "non-empty member ends in b. With q1 accepting and q2 −ε→ q1, the machine accepts a, aa, ba — none in "
                   "A∗. The fresh q0 has no incoming edges, so accepting it adds only ε."))
n.h2("6. Proof Template (sl. 34–37)")
n.numbered(["Start with machines for the input languages.", "Describe the operation to simulate.",
            "Build the new automaton (the construction is the heart).",
            "Argue both directions: L(N) ⊆ L (accepts nothing extra) and L ⊆ L(N) (accepts everything required)."])
n.h2("Exam Approach")
n.numbered(["Draw the picture (box N1, box N2, new states, ε arrows) and write Q, start, F, δ by cases.",
            "Justify each case: what it keeps from N1/N2, what it adds, why nothing extra is accepted.",
            "For 'finite or infinite' questions: ∘ of finite sets is finite; ∗ of a set containing a non-empty string is infinite."])
n.practice("Lesson 10", "(a) Actual — 2021-22 Q4(b), 2019-20 Q3(c). (b) Actual — Jan-2020 Q3(b). (c) Actual — 2023-24 Q3(b), 2016-17 Q4(a). "
           "(d) Actual — 2023-24 Q1(c). (e) Actual — 2021-22 Q2(c). (f) Actual — 2015-16 Q2(b) / 2016-17 Q4(b) / 2011-12 Q5(b).",
           ["(a) N1 recognises L1 and N2 recognises L2; we build N for L1 ∪ L2. Explain how we get the start state, the "
            "accept states, and the transitions from the start state (cases, reasons, destinations). Write δ. (12–15)",
            "(b) For N recognising L1∗ the transition function is defined by five cases (q ∈ Q1, q ∉ F1 / q ∈ F1, a ≠ ε / "
            "q ∈ F1, a = ε / q = q0, a = ε / q = q0, a ≠ ε). Explain each in plain English, stressing its purpose. (20)",
            "(c) Someone suggests making the original start state accepting instead of adding a new start state for the star "
            "construction. Why is this a bad idea? Give a counterexample. (13)",
            "(d) Draw NFAs for the concatenation of {w ∈ {0,1}∗ | w contains at least three 1s} with ∅, using the closure "
            "construction. (10)",
            "(e) L1 = {a, aa, aaa}, L2 = {a, ab, aab, aabb}, L3 = {number of b's is a multiple of 3}: finite or infinite — "
            "L1∗ ∘ L2∗, L1 ∘ (L1 ∪ L2), L2 ∘ L3? (6)",
            "(f) Prove that the class of regular languages is closed under the regular operations (concatenation, star). (15)"])
n.solution()
n.answer("(a)", "**Start state:** a new state q0 — neither N1's nor N2's start can serve, because the machine must be free "
         "to run either machine from the beginning. **Accept states:** F = F1 ∪ F2 — w ∈ L1 ∪ L2 iff N1 or N2 accepts it. "
         "**From q0:** on ε go to {q1, q2} (guess which machine will accept); on any real symbol a, δ(q0, a) = ∅ (q0 "
         "reads nothing; the first symbol is read inside N1 or N2). All other transitions are copied unchanged. δ: as in §3. "
         "Correctness: an accepting run of N starts q0 −ε→ qi and is then an accepting run of Ni, so L(N) ⊆ L1 ∪ L2; "
         "conversely choose the branch of the machine that accepts.")
n.answer("(b)", "Case 1 (q ∈ Q1, q ∉ F1): ordinary states behave exactly as in N1. Case 2 (q ∈ F1, a ≠ ε): accepting states "
         "keep their old moves, so a piece of A may continue to a longer piece. Case 3 (q ∈ F1, a = ε): additionally jump "
         "back to q1 — one piece of A is finished, start the next one (this gives A∘A, A∘A∘A, …). Case 4 (q = q0, a = ε): "
         "the new start enters N1 to read the first piece. Case 5 (q = q0, a ≠ ε): q0 itself reads nothing (∅), so q0 "
         "contributes only ε. q0 is accepting so that ε ∈ A∗ (k = 0 pieces).")
n.answer("(c)", "See the TRAP in §5: making q1 accepting accepts every string that brings N1 back to q1, even if it is "
         "not a concatenation of members of A. Counterexample A = a∗b: the flawed machine accepts a (and aa, ba), "
         "but a ∉ (a∗b)∗. The idea works only if q1 has no incoming transitions.")
n.answer("(d)", "N1 for 'at least three 1s': p0 −1→ p1 −1→ p2 −1→ p3, every state loops on 0, p3 loops on 0 and 1, F1 = {p3}. "
         "N2 for ∅: a single non-accepting start state r0 with no transitions. Concatenation: start p0, add p3 −ε→ r0, "
         "F = F2 = ∅. The result has no accepting state, so it recognises ∅ — as it must: L ∘ ∅ = ∅ for every L, "
         "because a string xy needs some y ∈ ∅.")
n.code(["p0 (start) −1→ p1 −1→ p2 −1→ p3;  p0,p1,p2 loop on 0;  p3 loops on 0,1;  p3 −ε→ r0;  r0: no moves",
        "accepting states: none  ⇒  L(N) = ∅"])
n.answer("(e)", "L1∗ ∘ L2∗: **infinite** (L1∗ already contains a, aa, aaa, aaaa, …). L1 ∘ (L1 ∪ L2): **finite** — L1 ∪ L2 has "
         "6 strings, so at most 3 × 6 = 18 concatenations. L2 ∘ L3: **infinite** — L3 is infinite (ε, bbb, bbbbbb, …) and "
         "L2 is non-empty, so a·b^(3k) gives infinitely many strings.")
n.answer("(f)", "Union: §3. Concatenation: §4 — if w = xy with x ∈ A1, y ∈ A2, N runs N1 on x, takes the ε-move from an "
         "accepting state of N1 to q2, and runs N2 on y; conversely every accepting run of N must cross from F1 to q2 "
         "exactly once (the only edges into Q2), splitting w into x ∈ A1 and y ∈ A2. Star: §5 — w = x1…xk with xi ∈ A is "
         "accepted by entering N1, running each xi and jumping back by ε; ε is accepted by q0; conversely each jump back "
         "marks the end of a piece in A. Since NFAs recognise exactly the regular languages, the class is closed.")

# ---------------------------------------------------------------- L11
n.lesson("Lesson 11 — More Closure: Complement, Intersection, Difference, Reverse", "Slides 38–60 (Lec05)")
n.h2("1. Complement (sl. 38–43)")
n.p("Ā = Σ∗ − A. If M = (Q, Σ, δ, q0, F) is a DFA for A, then M′ = (Q, Σ, δ, q0, Q − F) recognises Ā: every input follows "
    "exactly one complete path, which ends in F iff it does not end in Q − F. The DFA must be **complete** — add a dead "
    "state first, otherwise a string that 'gets stuck' would be rejected by both machines (sl. 42).")
fig(n, "H5", 43, "Figure 11.1 — Complementing a DFA: strings ending in 0 → ε or strings ending in 1 (sl. 43)", clip=K, width_cm=11)
n.callout("answer", ("Why flipping fails for an NFA (2022-23 Q3(b), 2021-22 Q1(c), 2017-18 Q2(a), 2015-16 Q3(b)): an NFA accepts "
                     "if SOME branch ends in an accepting state. After flipping, it accepts if some branch ends in a "
                     "(formerly) non-accepting state. A string can have one branch of each kind, so it is accepted by both "
                     "machines. Example over {a}: q0 (start, accepting) loops on a and also q0 −a→ q1 (non-accepting, no "
                     "moves). L(N) = a∗, so the complement is ∅. Flipped: q0 non-accepting, q1 accepting: it accepts a, aa, "
                     "… (branch that jumps to q1 on the last a) — not ∅. Strings rejected because every branch dies are "
                     "also rejected after flipping. Correct method: convert the NFA to a DFA (subset construction), "
                     "complete it, then flip."))
n.h2("2. Intersection: Product Construction and De Morgan (sl. 44–50)")
n.formula(["Q = Q1 × Q2,   q0 = (q1, q2),   δ((r1, r2), a) = (δ1(r1, a), δ2(r2, a))",
           "A ∩ B: F = F1 × F2        A ∪ B: F = (F1 × Q2) ∪ (Q1 × F2)"])
n.p("A state (r, s) means 'after the same prefix, M1 is in r and M2 is in s' — running two programs side by side (sl. 48). "
    "Algebraic proof: A ∩ B = complement of (Ā ∪ B̄) — complement, union, complement (sl. 49–50).")
n.h2("3. Difference and Reverse (sl. 51–57)")
n.p("A − B = A ∩ B̄ (sl. 51–52). Reverse: reverse every arrow of a DFA for A, make the old start the only accepting state, "
    "and add a new start with ε-moves to all old accepting states — an NFA for A^R (reversal can create nondeterminism) "
    "(sl. 53–57).")
fig(n, "H5", 57, "Figure 11.2 — Reversing a DFA gives an NFA (sl. 57)", clip=K, width_cm=10)
n.h2("4. Closure as a Proof Shortcut (sl. 58–60)")
n.p("'Contains 101 but does not end in 11' = L1 − L2 with both regular ⇒ regular, with no diagram. Likewise 'contains "
    "101 and has even length' = A ∩ B.")
n.h2("Exam Approach")
n.numbered(["Complement: make the DFA complete, flip F. For NFAs: convert first.",
            "Intersection / union of DFAs: product states, list only the reachable pairs, choose F by AND / OR.",
            "Closure-based regularity: express L with ∪, ∩, −, complement, reverse of known regular languages."])
n.practice("Lesson 11", "(a) Actual — 2017-18 Q2(a) / 2021-22 Q1(c). (b) Actual — 2022-23 Q4(a). (c) Actual — 2013-14 Q5(a). "
           "(d) Actual — 2013-14 Q8(a). (e) Actual — 2013-14 Q8(c).",
           ["(a) Given a DFA D for L over Σ, how can you readily find the DFA for Σ∗ − L? Why does it work? Is there any "
            "scenario in which it will not work? Does it work for NFAs? (9–10)",
            "(b) D1: s0 (start, accepting) −0,1→ s1, s1 loops on 0,1. D2: q1 (start) loops on 0, q1 −1→ q2, q2 loops on 1, "
            "q2 −0→ q3, q3 −0,1→ q2; q2, q3 accepting. We build D for L(D1) ∪ L(D2) from basic principles. (i) What is L(D1)? "
            "(ii) Draw the start state of D and two states reachable from it. (10)",
            "(c) Prove that regular languages are closed under L1 − L2 = {w | w ∈ L1 but w ∉ L2}. (8)",
            "(d) M1, M2 are DFAs for L1, L2. Describe the steps to construct a DFA for L1 ∪ L2. (7)",
            "(e) Show a counter-example to disprove: every subset of a regular language is also regular. (6)"])
n.solution()
n.answer("(a)", "Swap accepting and non-accepting states: M′ = (Q, Σ, δ, q0, Q − F). It works because a DFA has exactly "
         "one run on every input, ending in exactly one state, which is in F or in Q − F. It fails if the DFA is not "
         "complete (missing transitions: stuck strings are rejected by both) — add a dead state first; and the alphabet "
         "must be the full Σ. It does not work for NFAs — see the EXAM-READY ANSWER in §1 and its example.")
n.answer("(b)", "(i) D1 accepts only the empty string: L(D1) = {ε}. (ii) Product: start (s0, q1); on 0 → (s1, q1); on 1 → "
         "(s1, q2). (s0, q1) is accepting (s0 ∈ F1); (s1, q2) is accepting (q2 ∈ F2); (s1, q1) is not. From then on s1 never "
         "changes, so D behaves like D2: L(D) = {ε} ∪ L(D2), where L(D2) = strings with at least one 1 and an even number "
         "of 0s after the last 1.")
n.code(["(s0,q1) start,* −0→ (s1,q1)        (s1,q1) −0→ (s1,q1), −1→ (s1,q2)",
        "        −1→ (s1,q2)*        (s1,q2) −1→ (s1,q2), −0→ (s1,q3)*"])
n.answer("(c)", "L1 − L2 = L1 ∩ (complement of L2). If L2 is regular its complement is regular (flip a complete DFA); "
         "the intersection of two regular languages is regular (product construction with F = F1 × (Q2 − F2)). "
         "Directly: one product DFA with accepting pairs (r, s), r ∈ F1, s ∉ F2.")
n.answer("(d)", "1. States Q1 × Q2. 2. Start (q0¹, q0²). 3. δ((r, s), a) = (δ1(r, a), δ2(s, a)). 4. Accept (r, s) if "
         "r ∈ F1 **or** s ∈ F2. 5. Keep only pairs reachable from the start. Both DFAs must be complete over the same Σ.")
n.answer("(e)", "Σ∗ = {0,1}∗ is regular, but its subset {0^n1^n | n ≥ 0} is not regular (pumping lemma, Lesson 16). So "
         "regular languages are not closed under taking subsets. (Every language over Σ is a subset of the regular "
         "language Σ∗.)")

# ---------------------------------------------------------------- L12
n.lesson("Lesson 12 — Regular Expressions", "Slides 61–84 (Lec05)")
n.h2("1. Definition, Semantics, Precedence (sl. 61–68)")
n.p("R is a regular expression if R is a (a ∈ Σ), ε, ∅, (R1 ∪ R2), (R1 ∘ R2) or (R1∗), where R1, R2 are REs (sl. 64). "
    "L(a) = {a}, L(ε) = {ε}, L(∅) = ∅, L(R1 ∪ R2) = L(R1) ∪ L(R2), L(R1R2) = L(R1)L(R2), L(R1∗) = L(R1)∗ (sl. 65). "
    "Shorthands: Σ, R⁺ = RR∗, R? = R ∪ ε, R^k, [0-9] (sl. 66). Precedence: star, then concatenation, then union: "
    "0 ∪ 10∗ = 0 ∪ (1(0∗)) (sl. 68).")
n.h2("2. Examples (sl. 69–84)")
n.table(["RE", "Language"],
        [["0∗10∗", "exactly one 1"], ["Σ∗1Σ∗", "at least one 1"], ["1∗∅", "∅ (anything ∘ ∅ = ∅)"], ["∅∗", "{ε}"],
         ["Σ∗1Σ∗1Σ∗", "at least two 1s"], ["(0 ∪ 1)∗00", "ends in 00"], ["(ΣΣ)∗", "even length"],
         ["(0 ∪ 1(01∗0)∗1)∗", "binary multiples of 3 (and ε) — Lesson 14"]], widths_cm=[6.5, 10.7])
n.callout("memorize", ["Identities (sl. 83–84): R ∪ ∅ = R · Rε = R · R ∪ R = R · (R∗)∗ = R∗ · R∅ = ∅ · ∅∗ = {ε}. "
                       "Also (R ∪ S)∗ = (R∗S∗)∗, and (R1 ∪ R2)∗ ≠ R1∗ ∪ R2∗ in general."][0])
n.p("REs are not unique (sl. 104): (0 ∪ 1)∗1, 0∗1(1 ∪ 00∗1)∗ and Σ∗1 all describe 'ends in 1'.")
n.h2("3. How to Write an RE")
n.numbered(["Find the structure: blocks (a+b+), a mandatory part with free parts around it (Σ∗ x Σ∗), counts mod k "
            "(b∗(ab∗ab∗ab∗)∗), or 'forbidden pattern' (build from allowed blocks).",
            "For 'A and B' (e.g. contains a and c) list the orders and take the union.",
            "For 'not P' it is often easier to describe the allowed blocks, or to build a DFA and convert (Lesson 14).",
            "Test: two members, two non-members, and ε."])
n.callout("answer", ("Why do we need REs if automata describe the same languages? (2007-08 Q4(c)) REs are a compact, "
                     "algebraic, declarative notation: easy to write and read in one line, easy to type into tools "
                     "(grep, lexers, search/replace, input validation), and easy to combine and transform algebraically. "
                     "Automata are the implementation; REs are the specification. Kleene's theorem lets us convert "
                     "mechanically between them."))
n.h2("Exam Approach — Choosing Among RE Options")
n.numbered(["For each option find a shortest string that it wrongly accepts (false positive) or wrongly rejects (false "
            "negative). One counterexample per wrong option is enough.",
            "For the correct option argue both directions in one sentence each.",
            "Careful with overlapping occurrences: aaa contains aa twice."])

n.practice("Lesson 12 — writing REs", "(a) Actual — 2019-20 Q4(b). (b) Actual — 2017-18 Q4(b). (c) Actual — 2016-17 Q3(b). "
           "(d) Actual — 2014-15 Q3(b). (e) Actual — 2008-09 Q7(b), 2012-13 Q6(c), 2006-07 Q1(b), Jan-2020 Q2(c).",
           ["(a) Over {a, b}: (i) number of a's divisible by three; (ii) no more than three a's; (iii) exactly one "
            "occurrence of the substring aaa. (15)",
            "(b) (i) Σ = {a,b,c}, each symbol occurs at least once; (ii) {a^n b^m | n ≥ 3, m odd}; (iii) {a^n b^m | n + m "
            "odd}; (iv) {vwv | v, w ∈ {a,b}∗, |v| = 2}; (v) {w | #a(w) mod 3 = 0}. (20)",
            "(c) (i) alternating 0s and 1s; (ii) over {a,b,c} at least one a and at least one b; (iii) every pair of "
            "adjacent 0s appears before any pair of adjacent 1s. (4 + 4 + 7)",
            "(d) (i) decimal numbers divisible by 5 (no leading 0 except '0'); (ii) odd number of 0s or odd number of 1s; "
            "(iii) binary strings not containing 101. (4 + 3 + 3)",
            "(e) At least one a and one c over {a,b,c}; no two consecutive 0s or no two consecutive 1s; even number of 1s; "
            "alternating 0s and 1s; strings whose last two symbols are NOT equal."])
n.solution()
n.code(S("""(a) (i)   b*(ab*ab*ab*)*
    (ii)  b*(a|ε)b*(a|ε)b*(a|ε)b*
    (iii) (b|ab|aab)*aaa(b|ba|baa)*        — the only aaa block, other a-blocks have length ≤ 2
(b) (i)   union of the 6 orders:  Σ*aΣ*bΣ*cΣ* | Σ*aΣ*cΣ*bΣ* | Σ*bΣ*aΣ*cΣ* | Σ*bΣ*cΣ*aΣ* | Σ*cΣ*aΣ*bΣ* | Σ*cΣ*bΣ*aΣ*
    (ii)  aaaa*b(bb)*
    (iii) (aa)*a(bb)* | (aa)*b(bb)*        — exactly one of n, m is odd
    (iv)  aa(a|b)*aa | ab(a|b)*ab | ba(a|b)*ba | bb(a|b)*bb
    (v)   b*(ab*ab*ab*)*
(c) (i)   (1|ε)(01)*(0|ε)
    (ii)  Σ*aΣ*bΣ* | Σ*bΣ*aΣ*               (Σ = a|b|c)
    (iii) (0|10)*(1|ε)(1|01)*(0|ε)         — a part without 11, then a part without 00
(d) (i)   0 | 5 | [1-9][0-9]*(0|5)
    (ii)  1*0(1*01*0)*1* | 0*1(0*10*1)*0*
    (iii) 0*(1+00+)*(ε|1+|1+0)              — after a block of 1s, at least two 0s unless the string ends
(e)       Σ*aΣ*cΣ* | Σ*cΣ*aΣ*  ;   (1|01)*(0|ε) | (0|10)*(1|ε)  ;   0*(10*10*)*  ;   (1|ε)(01)*(0|ε)
          ε | 0 | 1 | (0|1)*(01|10)"""), size=8.5)
n.p("Each line was checked against its definition on all strings up to length 10 (length 6 over {a, b, c}, length 3 for "
    "decimal numbers).")

n.practice("Lesson 12 — describing, simplifying, choosing", "(f) Actual — 2006-07 Q4(b), 2007-08 Q2(b), Jan-2020 Q4(a). "
           "(g) Actual — 2019-20 Q2(b). (h) Actual — Jan-2020 Q3(a). (i) Actual — 2021-22 Q3(d). (j) Actual — 2022-23 Q4(c). "
           "(k) Actual — 2023-24 Q4(b). (l) Actual — 2009-10 Q4. (m) Actual — 2013-14 Q5(b). (n) Actual — 2015-16 Q3(a).",
           ["(f) Describe: 0∗10∗; Σ∗1Σ∗; 1∗(01⁺)∗; (ΣΣΣ)∗; 0Σ∗0 ∪ 1Σ∗1 ∪ 0 ∪ 1; 01 ∪ 10; (0 ∪ ε)1∗; (01 ∪ 010)∗; "
            "(0 ∪ 1)∗; (0Σ∗) ∪ (Σ∗1); (1 + ε)(00∗1)∗0∗.",
            "(g) Rewrite more simply: (i) ∅∗ ∪ a∗ ∪ b∗ ∪ (a ∪ b)∗; (ii) ((a∗b∗)∗(b∗a∗)∗)∗; (iii) (a∗b)∗ ∪ (b∗a)∗. (15)",
            "(h) Evaluate: ∅∗∅∗∅∗∅∗; ∅∗ ∪ {ε}; (∅∗ ∪ 1){0,1}; (11)∗∅(00)∗; (∅∗ ∪ 0){0,1,11}. (10)",
            "(i) Strings having two consecutive 0s as well as two consecutive 1s: A. (0+1)∗0011(0+1)∗ + (0+1)∗1100(0+1)∗; "
            "B. (0+1)∗(00(0+1)∗11 + 11(0+1)∗00)(0+1)∗; C. (0+1)∗00(0+1)∗ + (0+1)∗11(0+1)∗; D. 00(0+1)∗11 + 11(0+1)∗00. (12)",
            "(j) DFA q0 (start) loops on 0, q0 −1→ q1 (accepting), q1 loops on 1, q1 −0→ q0. Options: A. 0∗1(1 + 00∗1)∗; "
            "B. 0∗1∗1 + 11∗0∗1; C. (0 + 1)∗1. (10)",
            "(k) At most one occurrence of aa: A. (b+ab)∗(ε+a+aa)(b+ab)∗; B. (b+ab)∗(ε+a+aa)(b+ba)∗; C. (b+ab)∗(ε+a)(b+ba)∗; "
            "D. (b+ba)∗(ε+a+aa)(b+ba)∗. (12)",
            "(l) L1 = 1(1 ∪ 0)∗000, L2 = (1(01)∗0)∗. Are 1000, 1000101010, 10000111000100000 in L1 ∘ L2? (10)",
            "(m) Counter-example to (R1 ∪ R2)∗ = R1∗ ∪ R2∗.",
            "(n) DFA and RE for: begins with 1 and ends with 0; length ≥ 3 with third symbol 0; even number of 0s or exactly "
            "two 1s; any string except 11 and 111; at least two 0s and at most one 1. (18)"])
n.solution()
n.table(["RE", "Language"],
        [["0∗10∗", "exactly one 1"], ["Σ∗1Σ∗", "at least one 1"], ["1∗(01⁺)∗", "every 0 is followed by at least one 1 (no 00, does not end in 0)"],
         ["(ΣΣΣ)∗", "length a multiple of 3"], ["0Σ∗0 ∪ 1Σ∗1 ∪ 0 ∪ 1", "non-empty, starts and ends with the same symbol"],
         ["01 ∪ 10", "{01, 10}"], ["(0 ∪ ε)1∗", "0 optionally, then any 1s: {ε, 0, 1, 01, 11, 011, …}"],
         ["(01 ∪ 010)∗", "concatenations of blocks 01 and 010"], ["(0 ∪ 1)∗", "all binary strings"],
         ["(0Σ∗) ∪ (Σ∗1)", "starts with 0 or ends with 1"], ["(1 + ε)(00∗1)∗0∗", "no two consecutive 1s (checked)"]],
        widths_cm=[5.5, 11.7], font_size=9)
n.answer("(g)", "(i) (a ∪ b)∗ — it contains every other term (∅∗ = {ε}, a∗, b∗ ⊆ (a ∪ b)∗). (ii) (a ∪ b)∗ — a∗b∗ contains a "
         "and b, so (a∗b∗)∗ is already everything; the rest cannot add more. (iii) (a ∪ b)∗ — (a∗b)∗ = ε plus strings "
         "ending in b, (b∗a)∗ = ε plus strings ending in a; together every string.")
n.answer("(h)", "∅∗∅∗∅∗∅∗ = {ε}{ε}{ε}{ε} = {ε}; ∅∗ ∪ {ε} = {ε}; (∅∗ ∪ 1){0,1} = {ε, 1}{0, 1} = {0, 1, 10, 11}; "
         "(11)∗∅(00)∗ = ∅ (a ∅ factor kills a concatenation); (∅∗ ∪ 0){0,1,11} = {ε, 0}{0, 1, 11} = {0, 1, 11, 00, 01, 011}.")
rep = option_report("21_3d")
n.answer("(i)", "**B** only. A misses 001011 (00 and 11 not adjacent as 0011/1100); C accepts 00 (needs only one of the "
         "pairs); D misses 00110 (must start and end with the pairs). B: some 00 then later some 11, or 11 then later 00 — "
         "exactly 'contains both'.")
n.answer("(j)", "The DFA accepts exactly the strings ending in 1. **A and C** are correct. A: 0∗1 reaches q1, then each "
         "further piece is 1 (stay) or 00∗1 (go to q0 and back) — always ends in 1. B is wrong: it misses 0101 (and 1011).")
n.answer("(k)", "**B** only. A accepts aaab (two overlapping aa in aaa) and misses aaba (after aa, the right part (b+ab)∗ "
         "cannot end with a). C misses aa itself. D accepts baaa and misses abaa. B: left part (b+ab)∗ has no aa and ends "
         "with b, middle has at most one aa, right part (b+ba)∗ starts with b — so no aa crosses a boundary.")
n.answer("(l)", "L2 strings are built from blocks 1(01)∗0 = 10, 1010, … so they never contain 00 and are empty or end in "
         "10. 1000: L1 = 1000, L2 = ε ✓. 1000101010: 1000 ∘ 101010 (= 1·01·01·0) ✓. 10000111000100000 ends in 00000, so its "
         "L2 part must be ε; the whole string starts with 1 and ends with 000, so it is in L1 ✓. All three belong.")
n.answer("(m)", "R1 = a, R2 = b: ab ∈ (a ∪ b)∗ but ab ∉ a∗ ∪ b∗.")
n.answer("(n)", "REs (DFAs follow the Lesson 4 recipe; Sipser Ex. 1.6/1.18):")
n.code(S("""begins 1, ends 0          1(0|1)*0
3rd symbol 0               (0|1)(0|1)0(0|1)*
even 0s or exactly two 1s  (1*01*0)*1* | 0*10*10*
except 11 and 111          ε | 0 | 1 | 00 | 01 | 10 | 0(0|1)(0|1) | 10(0|1) | 110 | (0|1)(0|1)(0|1)(0|1)(0|1)*
≥ two 0s and ≤ one 1       000* | 1000* | 0100* | 000*10*"""), size=8.5)
n.code(["DFAs (sketch):  begins 1 ends 0: s −1→ A, s −0→ dead; A −0→ B*, A −1→ A; B −0→ B, B −1→ A",
        "third symbol 0: s −Σ→ t −Σ→ u; u −0→ OK* (loops Σ), u −1→ dead",
        "even 0s or exactly two 1s: product of parity-of-0s (2) and count-of-1s capped at 3 (4) → 8 states",
        "except 11,111: count prefix 1s: ε*,1*,11,111 states; any 0 → ok*; 1111 → ok*",
        "≥2 zeros, ≤1 one: (zeros 0/1/2+) × (ones 0/1) + dead on the second 1"], size=8.5)

# ---------------------------------------------------------------- L13
n.lesson("Lesson 13 — RE → NFA (Thompson's Construction)", "Slides 85–93 (Lec05)")
n.p("Kleene's theorem: a language is regular iff some RE describes it (sl. 85–86). Lemma 1 (RE → NFA) is proved by "
    "structural induction on the RE: NFAs for the base cases a, ε, ∅, then plug the NFAs of the parts into the union, "
    "concatenation and star constructions of Lesson 10 (sl. 87–90).")
fig(n, "H5", 89, "Figure 13.1 — Base cases: a, ε, ∅ (sl. 89)", clip=K, width_cm=9)
fig(n, "H5", 93, "Figure 13.2 — (ab ∪ a)∗ built step by step (sl. 91–93)", clip=K, width_cm=11)
n.h2("Exam Approach — 'Using the Basic Principles'")
n.numbered(["Parse the RE (star binds tightest, then concatenation, then union).",
            "Draw the tiny NFA for each symbol (2 states, one arrow).",
            "Combine inside-out: concatenation = ε from accept of the first to start of the second; union = new start with "
            "two ε; star = new accepting start + ε back from accept states.",
            "Do not 'optimise' unless allowed — the examiner checks the construction steps. Label the final start/accept."])
n.practice("Lesson 13", "(a) Actual — 2019-20 Q3(a). (b) Actual — 2017-18 Q2(c). (c) Actual — 2008-09 Q7(c). (d) Actual — 2021-22 Q2(b).",
           ["(a) Construct the NFA for ((a∗)a)∗ using the basic principles. (5)",
            "(b) Using the techniques of the closure proofs, draw the NFA for (a ∪ b)∗aba. (8)",
            "(c) Convert (0 + 1)∗1(0 + 1) to an ε-NFA. (4⅓)",
            "(d) Using the basic principles convert (((00)∗(11)) ∪ 01)∗ into an NFA. (10)"])
n.solution()
n.p("Each answer below is the exact Thompson-style construction (one 2-state NFA per symbol, ε-glue for ∘, new start for "
    "∪, new accepting start + back-ε for ∗). The edge lists were generated and tested against the RE on all strings up to "
    "length 8.")
thom_table("((a*)a)*", "ab", "(a) ((a∗)a)∗")
thom_table("(a|b)*aba", "ab", "(b) (a ∪ b)∗aba")
thom_table("(0|1)*1(0|1)", "01", "(c) (0 + 1)∗1(0 + 1)")
thom_table("((00)*(11)|01)*", "01", "(d) (((00)∗(11)) ∪ 01)∗")
n.p("Reading (b): s1 −a→ s2, s3 −b→ s4, union s5 → s1/s3, star s7 (start, accepting) → s5, then ε to the chain for a, b, a. "
    "A compact equivalent (allowed only if the question does not insist on basic principles): q0 loops on a, b; "
    "q0 −a→ q1 −b→ q2 −a→ q3.")

# ---------------------------------------------------------------- L14
n.lesson("Lesson 14 — DFA → RE (GNFA State Ripping) and Kleene's Theorem", "Slides 94–111 (Lec05)")
n.h2("1. GNFA (sl. 94–99)")
n.p("A generalised NFA has whole REs on its arrows: qi −R→ qj means 'read a block matching R'. Sipser's normal form: "
    "(1) the start state has arrows to every other state and none coming in; (2) a single accept state, arrows in from "
    "everywhere, none out; (3) start ≠ accept; (4) between all other states (including self-loops) exactly one arrow. "
    "Prepare a DFA: new start with ε to the old start; new accept with ε from old accepting states; missing arrows labelled "
    "∅; parallel arrows merged with ∪ (sl. 97–99).")
n.h2("2. Ripping a State (sl. 100–103)")
n.formula("R_{new}(qi, qj) = R(qi, qj) ∪ R(qi, q_{rip}) (R(q_{rip}, q_{rip}))∗ R(q_{rip}, qj)")
fig(n, "H5", 102, "Figure 14.1 — Before and after ripping q_rip (sl. 102)", clip=K, width_cm=11)
n.p("Algorithm Convert(G): if G has 2 states return the label qstart → qaccept; otherwise rip any internal state, repair "
    "every remaining pair (qi, qj) with the formula, and recurse (sl. 103). The result is correct but not necessarily the "
    "prettiest RE (sl. 104).")
n.h2("3. Worked Example: Binary Multiples of 3 (sl. 105–109)")
steps, res = gnfa(*DFA_RE["div3"][:4], order=["q2", "q1", "q0"])
lines = ["Rip q2:  R(q1,q1) = ∅ ∪ 0 1∗ 0 = 01∗0",
         "Rip q1:  R(q0,q0) = 0 ∪ 1 (01∗0)∗ 1",
         "Rip q0:  R(qs,qa) = ε (0 ∪ 1(01∗0)∗1)∗ ε  =  (0 ∪ 1(01∗0)∗1)∗",
         "Sanity: 11 = 3 and 1001 = 9 match 1(…)∗1."]
n.code(lines)
fig(n, "H5", 109, "Figure 14.2 — Final GNFA (sl. 109)", clip=K, width_cm=10)
n.h2("4. Kleene's Theorem — Proof Answers (2012-13 Q8(b), 2008-09 Q7(a))")
n.callout("answer", ("Theorem: L is regular ⇔ L = L(R) for some RE R. (⇐) Structural induction on R (Lesson 13): base "
                     "cases a, ε, ∅ have NFAs; if R1, R2 have NFAs then so do R1 ∪ R2, R1R2, R1∗ by the closure "
                     "constructions; NFAs recognise regular languages. (⇒) Let L = L(A) for a DFA A. Convert A into a GNFA "
                     "(new start, single new accept, ∅ for missing arrows, ∪ for parallel ones). Rip internal states one "
                     "at a time with R_new(qi,qj) = R(qi,qj) ∪ R(qi,q_rip)R(q_rip,q_rip)∗R(q_rip,qj). Claim: ripping keeps "
                     "the language — any computation of the old GNFA that passes through q_rip enters it from some qi, "
                     "loops some times and leaves to some qj, which the new label qi → qj matches; conversely every string "
                     "matched by a new label is read by a path of the old GNFA. By induction on the number of states, "
                     "when 2 states remain the single label R satisfies L(R) = L(A)."))
n.h2("Exam Approach — DFA → RE")
n.numbered(["Add qs −ε→ start and accepting −ε→ qa. Merge parallel arrows with ∪.",
            "Rip states with few arrows first (or follow the order the question gives).",
            "For each ripped state list every pair (in-arrow, out-arrow) and write the new label; keep old labels with ∪.",
            "Simplify only with safe identities (εR = R, R ∪ ∅ = R). Check with 2 strings."])
n.practice("Lesson 14", "(a) Actual — 2013-14 Q6(c). (b) Actual — 2012-13 Q7(b). (c) Actual — 2011-12 Q7(c).",
           ["(a) Construct a regular expression from the NFA: q0 (start, accepting) −a→ q1; q1 −b→ q0; q1 −a→ q2; q2 loops on a; "
            "q2 −b→ q0. (8)",
            "(b) Convert the DFA to an RE: 1 (start) −a→ 2, 2 −a→ 1, 2 loops on b, 1 −b→ 3, 3 −b→ 1, 3 −a→ 2; accepting 2 and 3. (7⅓)",
            "(c) Derive the RE for the automaton: 1 (start) −a,b→ 2, 2 loops on a, 2 −b→ 3, 3 −a→ 1, 3 −b→ 2; all of 1, 2, 3 "
            "accepting. (7⅓)"])
n.solution()
n.answer("(a)", "Rip q2: R(q1, q0) = b ∪ a a∗ b. Rip q1: R(q0, q0) = a(b ∪ aa∗b) = aa∗b. Rip q0 (start and accepting, with "
         "qs, qa added): R(qs, qa) = (aa∗b)∗. In words: blocks of one or more a's each followed by a single b. (Program "
         "result ((a(b ∪ aa∗b))∗) — same language, checked.)")
steps, res = gnfa(*DFA_RE["12_7b"][:4], order=["3", "2", "1"])
n.answer("(b)", "Add qs −ε→ 1 and 2, 3 −ε→ qa. Rip 3: R(1,1) = bb, R(1,2) = a ∪ ba, R(1,qa) = b. Rip 2 (loop b): "
         "R(1,1) = bb ∪ (a ∪ ba)b∗a, R(1,qa) = b ∪ (a ∪ ba)b∗. Rip 1:")
n.formula(S("(bb | (a|ba)b*a)* (b | (a|ba)b*)"))
n.p("Checked against the DFA on all strings up to length 9.")
n.answer("(c)", "All three states are accepting and every state has a move on both a and b (1: a,b; 2: a, b; 3: a, b), "
         "so the DFA is complete and accepts every string: **(a ∪ b)∗**. A blind GNFA run gives the longer "
         "((a∪b)(a∪bb)∗ba)∗(ε ∪ (a∪b)(a∪bb)∗(ε∪b)) — the same language; look before you rip!")

n.quick_notes("Quick Notes — Regular Languages", "Revision points for Lessons 10–14.", [
    ("L10 · Regular operations", ["A ∪ B, A ∘ B, A∗ (k ≥ 0 pieces). ∅∗ = {ε}; L∅ = ∅; L{ε} = L.",
                                  "Union: new start, ε to both starts, F = F1 ∪ F2, δ(q0, a≠ε) = ∅.",
                                  "Concat: ε from F1 to q2, F = F2. Star: new accepting start, ε to q1, ε from F1 to q1.",
                                  "Old start made accepting = wrong (A = a∗b accepts a). Finite ∘ finite = finite."]),
    ("L11 · Other closures", ["Complement: complete DFA, flip F. NFA flip fails (q0 loop a + q0 −a→ q1).",
                              "Product Q1 × Q2: AND → F1×F2, OR → either. A − B = A ∩ B̄. Reverse: reverse arrows → NFA.",
                              "Subsets of regular languages need not be regular ({0^n1^n} ⊂ Σ∗)."]),
    ("L12 · REs", ["Precedence ∗, ∘, ∪. R∅ = ∅, Rε = R, (R∗)∗ = R∗.", "Counts mod 3: b∗(ab∗ab∗ab∗)∗. ≤ k: (a|ε) pattern.",
                   "Contains both X and Y: union of the two orders. Forbidden pattern: allowed blocks.",
                   "Option questions: one counterexample per wrong option; watch overlaps (aaa has two aa)."]),
    ("L13 · RE → NFA", ["Base: a, ε, ∅. Inductive: plug into ∪, ∘, ∗ constructions (Thompson). Draw inside-out."]),
    ("L14 · DFA → RE", ["GNFA: new start/accept, ∅ for missing, ∪ for parallel arrows.",
                        "R_new = R(i,j) ∪ R(i,rip)R(rip,rip)∗R(rip,j). Div-by-3: (0 ∪ 1(01∗0)∗1)∗.",
                        "Kleene: RE ⇔ NFA ⇔ DFA."]),
], diagrams=[(PDF["H5"], 32, "Star construction (sl. 32) — Fig. 10.3", K, 8),
             (PDF["H5"], 102, "Ripping a state (sl. 102) — Fig. 14.1", K, 10)])
print(n.save())
