"""Hakim Sir — Lec03 DFA → CSE211_Hakim_DFA_Notes.docx (Lessons 3–5). All tables come from dfa_designs.py (verified)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import new_notes, exam_map_rows, fig, PRACT_NOTE, PDF
from dfa_designs import D, xustaeter

n = new_notes("H", "Deterministic Finite Automata", "CSE211_Hakim_DFA_Notes.docx")
CL = (0.04, 0.13, 0.96, 0.86)  # usual diagram area of a Lec03 slide


def tab(key, names=None, note=None):
    lines = D[key].table(names)
    lines.append("(→ start state, * accepting state" + (", " + note if note else "") + ")")
    n.code(lines)


n.front_matter(
    contents=[
        ("Exam Map — What the TF Papers Ask", "DFA design is in every single paper"),
        ("Lesson 3 — The DFA as a Mathematical Object", "state, 5-tuple, δ, acceptance, ε / ∅ / {ε}, dead states"),
        ("Lesson 4 — Designing DFAs: Remember the Right Thing", "design recipe, substrings, remainders (mod 3/4/5), constraints"),
        ("Lesson 5 — Advanced DFAs and Reading DFAs", "product construction, sliding window, runs, sum-with-reset, describing a given DFA"),
        ("Quick Notes — DFA", "revision bullets + key diagrams"),
    ],
    source_note=("Slide numbers refer to the PDF pages of Lec03 - DFA.pdf (42 pages). Every DFA in the solutions was "
                 "checked by a small program that runs it on all strings up to length 9 (6 for larger alphabets) and "
                 "compares with the language definition. " + PRACT_NOTE))

n.h1("Exam Map — What the TF Papers Ask")
rows, cnt = exam_map_rows("H", {3, 4, 5})
n.table(["Session", "DFA questions"], rows, widths_cm=[2.6, 14.6], font_size=8.5)
n.callout("focus", ("DFA design appears in all 17 papers — usually two parts per paper, 10–20 marks each. Most repeated, in "
                    "order: (1) remainder DFAs (binary/base-3 value mod 3, 4, 5; #a mod 3) — 2019-20, 2017-18, 2015-16, "
                    "2014-15, 2012-13, 2010-11, 2008-09; (2) running sum with a reset symbol R — 2022-23, 2019-20, 2014-15; "
                    "(3) substring / pattern constraints (no aa or bb, no aab, no 110, awa) — 2023-24, 2022-23, 2021-22, "
                    "2010-11; (4) runs of a symbol — 2023-24, 2022-23; (5) describe the language of a given DFA — 2022-23 "
                    "(20 marks), Jan-2020, 2015-16. Learn the design recipe in Lesson 4 first, then the remainder trick."))

# ---------------------------------------------------------------- Lesson 3
n.lesson("Lesson 3 — The DFA as a Mathematical Object", "Slides 1–20 (Lec03 §3A, §3B)")
n.h2("1. What Is a State? (sl. 4–7)")
n.p("A system reads a sequence of events and cannot remember all of them. A **state is a compressed summary of the past**: "
    "it keeps exactly the information needed to decide future behaviour and forgets the rest (sl. 5). A machine can be "
    "communicated by a drawing (good for intuition) or by a mathematical specification (good for proofs); a transition "
    "table is one convenient way to write the transition function (sl. 6–7).")
n.callout("answer", ("Role of a state (2019-20 Q2(a), 2007-08 Q2(c)): a state is the automaton's only memory. It classifies "
                     "all inputs read so far into finitely many groups, so that two inputs in the same group behave "
                     "identically on every continuation. Capacity: an FA has a **finite** number of states, so it can "
                     "remember only a bounded amount of information (e.g. a remainder, a parity, the last k symbols). It "
                     "cannot have infinite capacity — with infinitely many states it would no longer be a finite "
                     "automaton (it could recognise any language, one state per string, and could not be built). "
                     "Unbounded memory needs a stack (PDA) or a tape (TM)."))
n.h2("2. Formal Definition (sl. 8–9)")
n.formula(["M = (Q, Σ, δ, q0, F)", "δ : Q × Σ → Q"])
n.bullets(["Q — finite set of states; Σ — finite input alphabet;",
           "δ — transition function: exactly one next state for every (state, symbol);",
           "q0 ∈ Q — start state; F ⊆ Q — set of accepting (final) states."])
n.h2("3. Running Example: Even Number of 1s (sl. 10–14)")
n.p("EVEN1 = {w ∈ {0,1}* : w contains an even number of 1s}. Members: ε, 0, 11, 1010; non-members: 1, 10, 111. "
    "Remember only the parity: qE (even so far), qO (odd so far).")
fig(n, "H3", 11, "Figure 3.1 — DFA for an even number of 1s (sl. 11)", clip=(0.15, 0.18, 0.85, 0.62), width_cm=8)
n.code(["Q = {qE, qO}, Σ = {0,1}, q0 = qE, F = {qE}",
        "      0    1",
        "→*qE  qE   qO",
        "  qO  qO   qE"])
n.p("**Deterministic** (sl. 13): for every (q, a) ∈ Q × Σ there is exactly one δ(q, a) — no guessing, no ambiguity, no "
    "missing transition. 'A DFA is finite memory plus a deterministic update rule' (sl. 14).")
n.h2("4. Acceptance and the Language of a DFA (sl. 16–18)")
n.p("M accepts w = w1w2…wn if there is a sequence of states r0, r1, …, rn with (1) r0 = q0, (2) δ(ri, wi+1) = ri+1 for "
    "0 ≤ i ≤ n − 1, (3) rn ∈ F. L(M) = {w ∈ Σ* : M accepts w}; M recognises L when L(M) = L, i.e. w ∈ L ⇒ accept and "
    "w ∉ L ⇒ reject. Extended transition function (textbook): δ̂(q, ε) = q, δ̂(q, xa) = δ(δ̂(q, x), a); M accepts w iff "
    "δ̂(q0, w) ∈ F.")
n.callout("memorize", "A DFA accepts ε exactly when q0 ∈ F (it reads nothing and stays in q0) (sl. 18).")
n.h2("5. ε, ∅ and {ε}; Dead States (sl. 19–20)")
n.table(["Notation", "Meaning", "Size"], [["ε", "the empty string", "length 0"], ["∅", "the empty language", "0 strings"],
                                          ["{ε}", "language containing only the empty string", "1 string"]],
        widths_cm=[2.5, 10.2, 4.5])
n.p("A **dead state** (trap) is a non-accepting state with all transitions looping to itself. Once entered, success is "
    "impossible. Adding one keeps δ total, so the machine stays deterministic and complete (sl. 20). In exam diagrams "
    "you may omit it if you say 'missing transitions go to a dead state'.")
n.h2("6. Transition Table Size (2023-24 Q2(c))")
n.p("The table has one row per state and one column per input symbol: |Q| rows × |Σ| columns. Accepting states are only "
    "*marked* (* or a double circle) — changing which or how many states accept never changes the number of rows or "
    "columns. (Making more states accepting may let you merge states and so *reduce* |Q|, but that is a different "
    "DFA.)")
n.h2("Exam Approach — Formal Description")
n.numbered(["Write the 5-tuple with every component listed explicitly.",
            "Give δ as a full table; add a dead state for missing transitions.",
            "Mark the start state (→) and accepting states (*).",
            "If asked 'what language', trace short strings first, then describe in one sentence."])
n.practice("Lesson 3", "(a) Actual — 2015-16 Q1(a). (b) Actual — 2023-24 Q2(c). (c) Actual — 2006-07 Q2(b) (verification part).",
           ["(a) Formally define a Finite State Machine. Formally describe the FSM F1 of Figure 1.a: a −0→ b, b −0→ b, "
            "b −1→ c, a −1→ d, d −0→ e; start a; accepting c and e. (8⅓)",
            "(b) Does the number of accepting states in a DFA have any effect on the number of rows and columns in its "
            "transition table? Explain. (5)",
            "(c) For the DFA of even 0s and odd 1s (Lesson 5, §1) find δ̂(EE, 11010)."])
n.solution()
n.answer("(a)", "An FSM (DFA) is a 5-tuple M = (Q, Σ, δ, q0, F) as in §2. For F1:")
tab("F1", names={"a": "a", "b": "b", "c": "c", "d": "d", "e": "e", "X": "X"},
    note="X = dead state added for the missing transitions")
n.p("Q = {a, b, c, d, e} (+ dead state X), Σ = {0, 1}, q0 = a, F = {c, e}. The figure leaves some transitions undefined; "
    "formally δ must be total, so all missing moves go to X.")
n.answer("(b)", "No. Rows = |Q|, columns = |Σ|; accepting states are marked inside the existing rows. See §6.")
n.answer("(c)", "δ̂(EE, 1) = EO, δ̂(EE, 11) = EE, δ̂(EE, 110) = OE, δ̂(EE, 1101) = OO, δ̂(EE, 11010) = EO ∈ F → accepted "
         "(11010 has two 0s and three 1s ✓).")

# ---------------------------------------------------------------- Lesson 4
n.lesson("Lesson 4 — Designing DFAs: Remember the Right Thing", "Slides 21–29 (Lec03 §3C) + TF design problems")
n.h2("1. The Design Recipe (sl. 22)")
n.numbered(["Decide what information must be remembered — the hardest step: *what finite information is enough?*",
            "Make one state for each possible memory situation.",
            "Define how each input symbol updates that information.",
            "Mark the accepting states. Then add a dead state if needed and test a few members and non-members."])
n.h2("2. Example 1 — Strings Containing 001 (sl. 23–24)")
n.p("Remember the longest suffix of the input so far that is a prefix of 001: nothing useful (q), 0 (q0), 00 (q00), seen 001 "
    "(q001). Note q00 −0→ q00 (the last two symbols are still 00) and q0 −1→ q (a 1 after a single 0 destroys progress).")
fig(n, "H3", 24, "Figure 4.1 — DFA for strings containing 001 (sl. 24)", clip=(0.12, 0.22, 0.95, 0.62), width_cm=11)
n.h2("3. Example 2 — Binary Numbers Divisible by 3 (sl. 25–27)")
n.p("Appending bit b to a number with value v gives 2v + b. So only the remainder r = v mod 3 matters and "
    "**r → (2r + b) mod 3**. A separate start state qs (no bit read) keeps ε out of the language.")
fig(n, "H3", 27, "Figure 4.2 — DFA for binary multiples of 3 (sl. 27)", clip=(0.04, 0.12, 0.96, 0.66), width_cm=12)
n.callout("memorize", ["Remainder DFA for base b and modulus m: states r0 … r(m−1) (+ start qs); "
                       "δ(r, d) = (b·r + d) mod m; accept the wanted remainders. Works for any base and modulus.",
                       "Σ* contains ε, Σ+ does not (sl. 25)."][0], extra=["Σ* contains ε, Σ+ = Σ* − {ε} (sl. 25). With the "
                       "separate start state qs the DFA rejects ε; without it (start = r0) it accepts ε."])
n.h2("4. Example 3 — Valid Football Scores (sl. 28–29)")
n.p("Σ = {0, d, −} (d = any nonzero digit); L = {x−y : nonnegative integers with no leading zeros}. Remember: first or "
    "second score; whether the current score started with 0 (then it must end) or with d; whether the single hyphen is used.")
fig(n, "H3", 29, "Figure 4.3 — DFA for valid football scores (sl. 29)", clip=(0.04, 0.12, 0.98, 0.95), width_cm=12)
n.h2("Exam Approach — DFA Design")
n.numbered(["Write 2–3 members and non-members (the paper often gives them — test them at the end).",
            "Name the memory: remainder, parity, last k symbols, length so far, which pattern progress, 'bad thing seen'.",
            "States = values of that memory (+ start state if ε needs special treatment, + dead state).",
            "Fill the table row by row — every state needs a move on every symbol.",
            "Check: ε, one member, one non-member; then state the meaning of each state in one line (examiners ask for the "
            "'idea')."])
n.callout("trap", "For 'divisible' languages decide whether ε is in the language (usually not: add qs). For 'begins with' "
          "languages the wrong first symbol goes to a dead state. A 'does not contain' DFA = complement of the 'contains' "
          "DFA: flip accepting states of a complete DFA.")

n.practice("Lesson 4", "(a) Actual — 2015-16 Q2(a) / 2008-09 Q6(a). (b) Actual — 2014-15 Q2(b). (c) Actual — 2012-13 Q7(c), "
           "2017-18 Q2(b). (d) Actual — 2019-20 Q2(c). (e) Actual — 2010-11 Q2.",
           ["(a) Design a DFA that takes a binary string and recognises numbers NOT divisible by 3 (e.g. rejects 1111 = 15, "
            "accepts 111 = 7). Explain your idea. (8⅓) — and the DFA for multiples of 3. (9)",
            "(b) Design a DFA which accepts all and only the binary number strings divisible by 4. Explain. (13⅓)",
            "(c) DFA for binary strings whose value is a multiple of 5; DFAs for strings beginning with 1 that are (i) a "
            "multiple of 5 (101, 1010, 1111 in; 0, 100, 0101, 111 out), (ii) a power of 2. (8 + 17)",
            "(d) Design a DFA which accepts the base-3 numbers (digits 0, 1, 2) which are not divisible by 4. (15)",
            "(e) DFA over {a, b} accepting strings with n mod 3 = 1, n = number of a's; transition diagram and mathematical "
            "representation. (10)"])
n.solution()
nm = {f"r{i}": f"r{i}" for i in range(5)}
nm.update({"s": "qs", "dead": "dead"})
n.answer("(a)", "Idea: reading bits left to right, the value doubles and adds the bit, so keep r = value mod 3 and use "
         "r → (2r + b) mod 3. qs = nothing read. Not divisible ⇒ accept r1, r2; divisible ⇒ accept r0.")
tab("not3", nm, note="r = value mod 3; for multiples of 3 make only r0 accepting")
n.p("Trace 111: qs →1 r1 →1 r0 (3) →1 r1 (7) → accept ✓. Trace 1111: … r1 →1 r0 (15) → reject ✓.")
n.answer("(b)", "Same idea with m = 4: r → (2r + b) mod 4.")
tab("mod4", nm)
n.p("Why it works: v mod 4 depends only on the last two bits. Minimising: r1 ≡ r3 (both go to r2 on 0 and to r1/r3 on 1) "
    "and qs ≡ r2 (both non-accepting, both go to r0 on 0 and to r1 on 1), so 3 states suffice: {qs, r2} = 'nothing yet "
    "or ends in 10', {r1, r3} = 'ends in 1', {r0} = 'ends in 00 (or is 0)'. Example: 1100 (12): qs→r1→r3→r2→r0 ✓.")
n.answer("(c)", "Multiple of 5: r → (2r + b) mod 5, accept r0:")
tab("mod5", nm)
n.p("Beginning with 1: the start state goes to dead on 0, otherwise the same table. Trace 1111: qs→r1→r3→r2→r0 accept "
    "(15) ✓; 111: …→r2 reject ✓; 0101 → dead ✓.")
tab("mod5_lead1", nm, note="2017-18 Q2(b)(i)")
n.p("(ii) Powers of 2 written with a leading 1 are exactly 10*: ")
tab("pow2", {"s": "qs", "A": "A", "dead": "dead"}, note="A = '1 followed by 0s'")
n.answer("(d)", "Base 3: appending digit d gives 3v + d, so r → (3r + d) mod 4. Not divisible ⇒ accept r1, r2, r3.")
tab("b3_not4", nm)
n.p("Check: 11₃ = 4 → qs→r1→r0 reject ✓; 12₃ = 5 → qs→r1→r1 accept ✓; 102₃ = 11 → qs→r1→r3→r3 accept ✓.")
n.answer("(e)", "Only the number of a's mod 3 matters; b's do not change it.")
tab("10_2", {"r0": "r0", "r1": "r1", "r2": "r2"})
n.p("M = ({r0, r1, r2}, {a, b}, δ, r0, {r1}) with δ as in the table (ri = 'number of a's ≡ i mod 3').")

n.h2("More Lesson 4 Practice — Pattern Constraints")
n.practice("Lesson 4 (patterns)", "(f) Actual — 2022-23 Q1(c). (g) Actual — 2021-22 Q1(b). (h) Actual — 2023-24 Q2(b). "
           "(i) Actual — 2010-11 Q4. (j) Actual — 2006-07 Q1(a). (k) Actual — 2007-08 Q1(b). (l) Actual — 2009-10 Q2. "
           "(m) Actual — 2011-12 Q5(c).",
           ["(f) Construct a DFA for {w ∈ {a,b}* | w has neither aa nor bb as a substring}; give the transition table. (13)",
            "(g) DFA with not more than five states over {a, b} accepting strings that begin with a but do not contain aab. (10)",
            "(h) Show that L = {awa | w ∈ {a,b}*} is regular by constructing a DFA for it. (15)",
            "(i) DFA for strings over {0,1} not containing 110; regular expression for the language. (7 + 3)",
            "(j) DFA for strings that start with 0 and have odd length, or start with 1 and have even length; diagram and "
            "table. (10)",
            "(k) DFA over {a, b} in which each a is followed by at least one b; design steps and table. (8)",
            "(l) DFA over {a, b} accepting strings in which the symbol that starts the string never occurs three times "
            "consecutively (abaab, baaabba accepted; abaaab, bbbaa rejected). (10)",
            "(m) DFA for {w | |w| ≤ 5} over {0, 1}. (5⅓)"])
n.solution()
n.answer("(f)", "Remember the last symbol (and whether we have started). Seeing it again → dead.")
tab("22_1c", {"S": "S", "A": "A", "B": "B", "D": "D"}, note="A = last symbol a, B = last symbol b, D = dead")
n.p("L = alternating strings: ε, a, b, ab, ba, aba, … Trace abab: S→A→B→A→B accept; abba: …→B→D reject ✓.")
n.answer("(g)", "States: S (nothing read), A (last symbol a, previous not a), AA (last two aa), B (last symbol b), D (dead). "
         "Wrong first symbol b → D; aa followed by b → D. Exactly 5 states.")
tab("21_1b", {"S": "S", "A": "A", "AA": "AA", "B": "B", "D": "D"})
n.p("Trace abaa: S→A→B→A→AA accept ✓; aab: S→A→AA→D reject ✓; ba → D ✓.")
n.answer("(h)", "Need: first symbol a, length ≥ 2, last symbol a. After the first a, remember whether the last symbol read "
         "was a (Q, accepting) or b (P).")
tab("23_2b", {"S": "S", "P": "P", "Q": "Q", "D": "D"})
n.p("aa: S→P→Q accept (w = ε) ✓; a: S→P reject ✓; abba: S→P→P→P→Q accept ✓; b… → D. Since a DFA exists, L is regular.")
n.answer("(i)", "Track the suffix: q (no progress), q1 (last 1), q11 (last 11); q11 −0→ D. Once 11 has appeared, only 1s can "
         "follow.")
tab("10_4", {"q": "q", "q1": "q1", "q11": "q11", "D": "D"})
n.formula("RE: (0 ∪ 10)∗1∗")
n.p("Before the first 11 the string is built from blocks 0 and 10; after the first 11 only 1s may follow (checked by "
    "program against all strings up to length 12).")
n.answer("(j)", "Remember the first symbol and the parity of the length.")
tab("06_1a", {"s": "s", "0odd": "0odd", "0even": "0even", "1odd": "1odd", "1even": "1even"})
n.answer("(k)", "Interpret 'followed by' as 'immediately followed by': L = (b ∪ ab)*. q1 = an a is waiting for its b.")
tab("07_1b", {"q0": "q0", "q1": "q1", "d": "d"})
n.callout("note", "If the examiner means 'followed somewhere later by a b', the condition only fails when the string ends "
          "in a: then the DFA has q0 (last symbol b or ε, accepting) and q1 (last symbol a, non-accepting) with "
          "q0 −a→ q1, q1 −a→ q1, both −b→ q0. State your interpretation.")
n.answer("(l)", "After the first symbol x, count the current run of x's (0, 1, 2); a third x in a row → dead. The other "
         "symbol resets the count.")
tab("09_2", {q: q for q in ["s", "A0", "A1", "A2", "B0", "B1", "B2", "D"]},
    note="Ai = first symbol a, current run of a's = i; Bi likewise for b")
n.p("abaab: s→A1→A0→A1→A2→A0 accept ✓; abaaab: …→A2 −a→ D reject ✓; bbbaa: s→B1→B2→D reject ✓.")
n.answer("(m)", "Count the length up to 6: states q0 … q5 accepting, q6 = dead (all lengths ≥ 6).")
tab("11_5c", {**{f"q{i}": f"q{i}" for i in range(7)}})

# ---------------------------------------------------------------- Lesson 5
n.lesson("Lesson 5 — Advanced DFAs and Reading DFAs", "Slides 30–42 (Lec03 §3D) + TF problems")
n.h2("1. Product Construction: Two Conditions at Once (sl. 31–32)")
n.p("L = {w : even number of 0s AND length a multiple of 3}. Track two independent things: parity of 0s (2 values) and "
    "length mod 3 (3 values) → 2 × 3 = 6 states (p, l). Accept only (E, 0).")
fig(n, "H3", 32, "Figure 5.1 — Product DFA: parity of 0s × length mod 3 (sl. 32)", clip=(0.2, 0.12, 0.85, 0.98), width_cm=9)
n.callout("memorize", "Product construction: states Q1 × Q2, start (q1, q2), δ((r, s), a) = (δ1(r, a), δ2(s, a)). "
          "AND → accept F1 × F2; OR → accept pairs with r ∈ F1 or s ∈ F2. Number of states = |Q1|·|Q2|.")
n.h2("2. The k-th Symbol from the End (sl. 33–34)")
n.p("L = {w : the 2nd symbol from the right is 1}. Remember the last 2 symbols (sliding window): q00, q01, q10, q11; "
    "start q00 (pretend leading zeros); accept q10, q11. From q01 on 0 the window becomes 10.")
fig(n, "H3", 34, "Figure 5.2 — Sliding-window DFA (sl. 34)", clip=(0.25, 0.12, 0.75, 0.95), width_cm=7)
n.p("In general the k-th symbol from the end needs 2^k states — a DFA cannot 'guess' where the end is (an NFA can, with "
    "k + 1 states — Lesson 9).")
n.h2("3. Pattern Interference, Sets of Seen Symbols, Comments (sl. 35–40)")
n.bullets(["Contains ab but not ba over {a, b} = a+b+: states S, A, B, AB, Dead (sl. 35–36).",
           "No symbol repeated over {a, b, c}: state = set of symbols already seen (∅, a, b, c, ab, ac, bc, abc) + D; all "
           "except D accept (sl. 37–38).",
           "Exactly one C comment /*…*/ over {/, *, x}: q0 −/→ q1 −*→ q2 (inside), q2 −*→ q3, q3 −*→ q3, q3 −x→ q2, "
           "q3 −/→ q4 (accept); everything else → d (sl. 39–40)."])
fig(n, "H3", 36, "Figure 5.3 — Contains ab but not ba (sl. 36)", clip=(0.2, 0.12, 0.85, 0.85), width_cm=8)
fig(n, "H3", 40, "Figure 5.4 — DFA for one C-style comment (sl. 40)", clip=(0.1, 0.12, 0.95, 0.62), width_cm=11)
n.h2("4. Running Sum with Reset (TF favourite)")
n.p("Σ = {0, 1, 2, …, R}: keep only the sum mod m; a digit d moves r → (r + d) mod m; R moves every state to r0. The "
    "actual sum is unbounded, so 'remember the actual sum' needs infinitely many states — not a finite automaton.")
n.h2("5. Reading a Given DFA")
n.numbered(["Find the dead states and the accepting states.",
            "Give each state a meaning ('last symbol was a', 'one a pending', 'counter = 2').",
            "Trace the shortest accepted strings; look for the loops that pump them.",
            "Write the language in English and, if easy, as a regular expression. Check one non-member."])
n.h2("Exam Approach — Two Conditions / Counting")
n.numbered(["Split the condition into independent parts; DFA for each.",
            "Combine by the product construction (states = pairs); AND/OR decides the accepting pairs.",
            "For runs, keep (number of completed qualifying runs, length of the current run) — cap counters at the largest "
            "value that matters."])

n.practice("Lesson 5", "(a) Actual — 2019-20 Q1(c). (b) Actual — 2014-15 Q1(a)–(b). (c) Actual — 2022-23 Q1(b). "
           "(d) Actual — 2016-17 Q2(a). (e) Actual — 2006-07 Q2(b). (f) Actual — 2013-14 Q5(c).",
           ["(a) DFA with alphabet {0, 1, 2, R} that keeps a running count of the sum of the numerical symbols, resets "
            "to 0 on R, and accepts if the sum is 1 or 2 modulo 5. State diagram only. (15)",
            "(b) DFA over {0, 1, 2, 3, R}: sum a multiple of 3, reset on R. Then with alphabet {0, 1, 2, R} you use the "
            "states to remember the actual sums — show how; what is the problem? (10 + 13⅓)",
            "(c) For the sum-mod-3 automaton with reset, a classmate claims two states suffice: 'remainder 0' and "
            "'remainder non-zero'. Comment analytically. (12)",
            "(d) DFA over {a, b, 1, 2} accepting strings whose number of a's is divisible by 3 and whose digit sum is "
            "even (ε, aab12a1, 121 accepted; aaab12a1, 1121 rejected). (17)",
            "(e) DFA for strings with an even number of 0s and an odd number of 1s. (8)",
            "(f) DFA for L = {w ∈ {a,b}* | w = a^p b^q, p + q even}. (10⅓)"])
n.solution()
rn = {f"r{i}": f"r{i}" for i in range(5)}
n.answer("(a)", "State ri = (sum since the last R) mod 5. Digit d: ri → r(i+d mod 5); R: every state → r0. Accept r1, r2.")
tab("19_1c", rn)
n.p("Trace 2R12: r0→r2→r0→r1→r3 → reject (sum 3) ✓; 2R2R1 → r1 accept ✓.")
n.answer("(b)", "Same with m = 3 and digits 0–3, accept r0:")
tab("14_1a", rn)
n.p("Remembering actual sums: states s0, s1, s2, … with si −d→ s(i+d), si −R→ s0, accepting s0, s3, s6, …. The sum can "
    "grow without bound, so the diagram needs **infinitely many states** — it is not a finite automaton and cannot be "
    "drawn completely. Only the remainder mod 3 is needed for the decision, so states {s0, s3, s6, …} can be merged into "
    "r0, etc., giving the 3-state DFA.")
n.answer("(c)", "The claim is false. Use the inputs 1 and 2: both would go to 'non-zero'. Append 2: 12 has sum 3 (accept) "
                "but 22 has sum 4 (reject). A DFA in the same state after 1 and after 2 must give the same answer on "
                "both continuations — contradiction. Formally, the remainders 0, 1, 2 are pairwise distinguishable "
                "(0 vs 1 by suffix ε, 1 vs 2 by suffix 2, 0 vs 2 by ε), so any DFA needs at least 3 states "
                "(Myhill–Nerode). The 2-state machine also cannot define its next state: from 'non-zero' on input 1 the "
                "result is non-zero for remainder 1 but zero for remainder 2.")
tab("22_1b", rn, note="the correct 3-state DFA")
n.answer("(d)", "Product of 'a's mod 3' (0, 1, 2) and 'digit-sum parity' (E, O): 6 states kE/kO. a: k → k+1 mod 3; b: no "
         "change; 1: flip parity; 2: keep parity. Accept 0E only.")
tab("16_2a", {q: q for q in ["0E", "0O", "1E", "1O", "2E", "2O"]})
n.p("aab12a1: 0E→1E→2E→2E→2O→2O→0O→0E accept ✓. 1121: 0E→0O→0E→0E→0O reject ✓.")
n.answer("(e)", "States = (parity of 0s, parity of 1s); start EE; accept EO.")
tab("06_2b", {q: q for q in ["EE", "EO", "OE", "OO"]})
n.answer("(f)", "Remember: still in the a-block or already in the b-block, and the parity of the length; an a after a b → dead.")
tab("13_5c", {q: q for q in ["Ea", "Oa", "Eb", "Ob", "D"]})
n.p("ε, aa, ab, abbb accepted; a, aab rejected; ba → D ✓.")

n.h2("More Lesson 5 Practice — Runs and Reading DFAs")
n.practice("Lesson 5 (runs, reading)", "(g) Actual — 2022-23 Q3(a). (h) Actual — 2023-24 Q1(b). (i) Actual — 2022-23 Q2(a). "
           "(j) Actual — Jan-2020 Q2(a). (k) Actual — 2015-16 Q1(b)–(e).",
           ["(g) DFA accepting binary strings such that none of their runs of 0s has an even length ≥ 2 (0001100 rejected; "
            "01110001, 11111 accepted); give your design idea. (15)",
            "(h) A run is a maximal substring of length ≥ 2 of one symbol. DFA over {a, b} for strings with at most two runs "
            "of a's of length exactly three. (17)",
            "(i) Describe informally the languages accepted by the five automata of 2022-23 Q2(a). (20)",
            "(j) State informally the language accepted by the 5-state DFA of Jan-2020 Q2(a). (7)",
            "(k) What language does F1 recognise? F2 = F1 + δ(d, 1) = d? Can F1 be changed (same numbers of states and "
            "transitions) so that |L(F3)| = |L(F1)| + 1? |L(R1)| = 5 but your DFA accepts 1000 random strings — is the "
            "DFA wrong? (4 + 4 + 4 + 3)"])
n.solution()
n.answer("(g)", "Idea: only the parity of the current run of 0s matters, and only when the run ends. N = not inside a run "
         "(last symbol 1 or start), O = inside a run of odd length, E = inside a run of even length ≥ 2. A 1 or the end of "
         "input closes the run: from E that is fatal (1 → D; E is non-accepting).")
tab("22_3a", {q: q for q in ["N", "O", "E", "D"]})
n.p("0001100: N→O→E→O→N→N→O→E end in E → reject ✓. 01110001: …→O→N … runs 1 and 3 → ends N accept ✓.")
n.answer("(h)", "State (k, c): k = number of completed a-runs of length exactly 3 (0, 1, 2), c = length of the current "
         "a-run capped at 4 (4 means ≥ 4). On a: c → min(c + 1, 4). On b: if c = 3 then k → k + 1 (k = 3 → dead), "
         "c → 0. At the end the current run also counts, so (k, c) is accepting iff k + [c = 3] ≤ 2. "
         "15 states + dead = 16; a minimisation program confirms 16 is minimal.")
names = {q: q for q in D["23_1b"].states}
tab("23_1b", names, note="state 'k,c'; e.g. aaabaaabaaa ends in (2,3) → 3 runs → reject")
n.p("Note: a single a or a length-2 run never counts; aaaa is a run of length 4, not 3.")
n.answer("(i)", "Reading the five diagrams (states named by position; missing arrows go to the sink):")
n.table(["FA", "Behaviour", "Language"],
        [["i", "a moves start → accepting top; from top b returns, a goes to a state that only leads to the sink", "(ab)*a — alternating, starting and ending with a"],
         ["ii", "upper branch a⁺ then b to an accepting state; lower branch a single b; any further symbol → sink", "a*b = {b, ab, aab, …}"],
         ["iii", "a = +1, b = −1 on a counter 0–2; start is the only accepting state; leaving 0…2 → sink", "balanced strings (a = '(' , b = ')') with nesting depth ≤ 2, e.g. ε, ab, aabb, abaabb"],
         ["iv", "from the centre (start, accepting) ba or ab returns to the centre; aa/bb patterns → sink", "(ab ∪ ba)*"],
         ["v", "alternation until the first aa or bb; after aa a later b accepts, after bb a later a accepts; accept state loops", "strings containing aab or bba"]],
        widths_cm=[1.2, 9.0, 7.0], font_size=9)
n.p("Each description was checked by running the drawn automaton on all strings up to length 9.")
n.answer("(j)", "q1/q3 mean 'last symbol 0' (q3: last two 00); q2/q4 mean 'last symbol 1' (q4: last two 11). "
         "L = strings of length ≥ 2 whose last two symbols are equal = (0 ∪ 1)*(00 ∪ 11).")
n.answer("(k)", "L(F1) = {0^n1 | n ≥ 1} ∪ {10} = 0⁺1 ∪ {10}. With δ(d, 1) = d: L(F2) = 0⁺1 ∪ 1⁺0. "
         "|L(F1)| is countably infinite (ℵ0), so |L(F1)| + 1 = |L(F1)|: the 'increase by exactly 1' cannot be measured "
         "by cardinality. As sets it is possible to add exactly one string without changing the numbers of states or "
         "transitions — e.g. make d accepting: L(F3) = L(F1) ∪ {1}. "
         "Last part: yes, the brother is right. L(R1) has only 5 strings, but the DFA accepted 1000 different strings, so "
         "L(D1) ⊋ L(R1) and D1 is not equivalent to R1.")

n.h2("Lesson 5 Extra — State Modelling: the Planet Xustaeter (2016-17 Q1)")
n.p("Stones of three colours R, G, B. When two stones of different colours touch, both are destroyed and two stones of the "
    "third colour appear (e.g. R-event: G + B → 2R). The planet fails when all stones have one colour. State = (r, g, b) "
    "with r + g + b = N. Classes: **failed** (N,0,0)…; **must-fail**: every path reaches failure; **can't-fail**: no "
    "path reaches failure; **might-fail**: some paths do, some don't.")
n.callout("memorize", "Invariant: an event changes each difference r − g, g − b by 0 or ±3, so the differences mod 3 never "
          "change. Failure (N, 0, 0) has two equal counts mod 3. Hence a state might reach failure only if two of its "
          "counts are congruent mod 3.")
for N in (3, 4):
    S, succ, cls = xustaeter(N)
    lines = [f"N = {N}:  (r,g,b)    class        successors (R-, G-, B-events)"]
    for s in S:
        lines.append(f"  {str(s).replace(' ', ''):<10} {cls[s]:<12} {' '.join(str(t).replace(' ', '') for t in succ(s)) or '—'}")
    n.code(lines, size=8.5)
n.p("(c) Symmetry: renaming colours does not change behaviour, so states that are permutations of each other behave "
    "alike. Reduced scheme: one node per multiset {x, y, z} (sorted counts), with an edge {x,y,z} → {x',y',z'} if some "
    "event maps a representative to a representative.")
S, succ, cls = xustaeter(6)
red = {}
for s in S:
    k = tuple(sorted(s))
    red.setdefault(k, set()).update(tuple(sorted(t)) for t in succ(s))
lines = ["N = 6, reduced {x≤y≤z}  class        successors"]
for k in sorted(red):
    c = cls[next(s for s in S if tuple(sorted(s)) == k)]
    lines.append(f"  {str(k).replace(' ', ''):<10} {c:<12} {' '.join(str(t).replace(' ', '') for t in sorted(red[k])) or '—'}")
n.code(lines, size=8.5)
n.p("For N = 6: must-fail none (besides the failed states); might-fail {0,3,3}, {1,1,4}, {2,2,2}; can't-fail {0,1,5}, "
    "{0,2,4}, {1,2,3}. (Computed by search; consistent with the mod-3 invariant.)")

# ---------------------------------------------------------------- quick notes
n.quick_notes("Quick Notes — DFA", "Revision points for Lessons 3–5.", [
    ("L3 · DFA definition", ["M = (Q, Σ, δ, q0, F), δ : Q × Σ → Q total; exactly one move per (state, symbol).",
                             "Accept iff δ̂(q0, w) ∈ F; accepts ε iff q0 ∈ F. Dead state keeps δ total.",
                             "State = compressed summary of the past; finitely many → finite memory.",
                             "Table = |Q| rows × |Σ| columns; accepting states are only marked."]),
    ("L4 · Design", ["Recipe: what to remember → one state per situation → update rule → accepting states → test.",
                     "Contains pattern: states = longest suffix that is a prefix of the pattern; 'does not contain' = flip.",
                     "Remainder DFA: r → (b·r + d) mod m; separate start state if ε must be rejected.",
                     "Binary mod 4: depends only on the last two bits (3 states after minimising: qs ≡ r2, r1 ≡ r3).",
                     "begins with x: wrong first symbol → dead. awa: track first symbol and last symbol."]),
    ("L5 · Advanced", ["Product: Q1 × Q2, AND → F1 × F2, OR → either coordinate accepting.",
                       "k-th from end: 2^k states for a DFA (sliding window).",
                       "Sum with reset R: keep sum mod m, R → r0; 'actual sums' → infinitely many states.",
                       "Two-state 'zero / non-zero' fails: remainders 1 and 2 are distinguishable (suffix 2).",
                       "Runs: (completed qualifying runs, current run length capped).",
                       "Reading a DFA: dead states, meaning of each state, shortest accepted strings, loops."]),
], diagrams=[(PDF["H3"], 27, "Binary multiples of 3 (sl. 27) — same as Fig. 4.2", (0.04, 0.12, 0.96, 0.66), 11),
             (PDF["H3"], 32, "Product construction (sl. 32) — same as Fig. 5.1", (0.2, 0.12, 0.85, 0.98), 8)])
print(n.save())
