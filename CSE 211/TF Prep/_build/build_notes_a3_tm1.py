"""Atif Sir — Lecture 4 (Turing Machine 1) → CSE211_Atif_TM_Basics_Notes.docx (Lessons 11–13). Checks: tm_designs.py."""
import os, sys, itertools; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import new_notes, exam_map_rows, fig, PRACT_NOTE, PDF
from tm_designs import M, BL

n = new_notes("A", "Turing Machines — Definition and Design", "CSE211_Atif_TM_Basics_Notes.docx")
K = (0.03, 0.12, 0.97, 0.92)


def tm(key, title, note=None):
    t = M[key]
    n.code([title] + t.lines() + [f"start {t.start}; accepting/halting {sorted(t.accept)}; ⊔ = blank; 'same' = write the symbol read" + (f"; {note}" if note else "")], size=8)


def tr(key, w, limit=40):
    ids = M[key].trace(w, limit)
    s = " ⊢ ".join(ids)
    n.code([f"IDs on {w}:"] + [s[i:i + 108] for i in range(0, len(s), 108)], size=8)


n.front_matter(
    contents=[
        ("Exam Map — What the TF Papers Ask", "TM design: one 7–20 mark question per paper"),
        ("Lesson 11 — The Turing Machine: Definition, IDs, Language", "7-tuple, tape, moves, ID notation, halting, RE languages"),
        ("Lesson 12 — Designing Language-Deciding TMs", "marking technique: 0^n1^n, a^nb^nc^n, w−w, equal counts"),
        ("Lesson 13 — TMs Computing Functions", "monus, unary subtraction, increment, parity output"),
        ("Quick Notes — TM Basics", "revision bullets + key diagrams"),
    ],
    source_note=("Slide numbers refer to the PDF pages of Lecture - 4 (Turing Machine 1).pdf (123 pages; beamer builds). "
                 "Hopcroft notation: M = (Q, Σ, Γ, δ, q0, B, F), δ(q, X) = (p, Y, D), D ∈ {L, R}, blank B (printed ⊔ in "
                 "the machines below to avoid confusion with the symbol B). IDs are written X1…Xi−1 q Xi…Xn. Every TM in "
                 "the solutions was run by a simulator on all strings up to length 9 (7–8 for larger alphabets) and its "
                 "output compared with the specification. Bit-manipulation TMs (XOR/AND/OR/NOT/…) are in the next note. "
                 + PRACT_NOTE))

n.h1("Exam Map — What the TF Papers Ask")
rows, cnt = exam_map_rows("A", {11, 12, 13})
n.table(["Session", "TM design questions from this lecture"], rows, widths_cm=[2.6, 14.6], font_size=8.5)
n.callout("focus", ("A TM design question appears in every paper (7–20 marks). Since 2017-18 the 15-mark one is always a "
                    "BIT-MANIPULATION machine (next note); before that the favourites were {0^n1^n}, {a^nb^nc^n}, "
                    "{w−w}, equal 0s/1s, unary subtraction (monus) and binary increment. Learn the marking technique "
                    "(Lesson 12) and be able to write the transition table and the ID trace of {0^n1^n}."))

# ---------------------------------------------------------- L11
n.lesson("Lesson 11 — The Turing Machine: Definition, IDs, Language", "Slides 1–41, 116–123")
n.h2("1. Why Turing Machines? (sl. 2–5)")
n.p("Neither FAs nor PDAs are general models of computers — they cannot even recognise {a^nb^nc^n}. A TM (Turing, 1912–54) "
    "is a finite automaton with a single infinite tape on which it can read and write.")
n.h2("2. The Machine (sl. 6–26)")
n.numbered(["A finite control in one of finitely many states.", "A tape of cells, each holding one symbol of a finite alphabet.",
            "Initially the input (finite string over Σ) is on the tape, all other cells (infinite in both directions) hold the "
            "blank B. B is a tape symbol, not an input symbol.", "A head scanning one cell, initially the leftmost input cell.",
            "One move depends on state and scanned symbol: change state (maybe the same), write a symbol (maybe the same), "
            "move the head one cell left or right — it must move, it cannot stay."])
n.formula(["M = (Q, Σ, Γ, δ, q0, B, F)", "δ(q, X) = (p, Y, D)  — next state, symbol written, direction"])
n.p("Γ is the set of all tape symbols with Σ ⊆ Γ and B ∈ Γ − Σ; q0 start; F accepting states.")
n.callout("answer", ("Formal notation of a TM (2008-09 Q3(a), 2009-10 Q12(a)): the 7-tuple above, with Q finite states, Σ finite "
                     "input alphabet (not containing B), Γ finite tape alphabet ⊇ Σ ∪ {B}, δ : Q × Γ → Q × Γ × {L, R} a "
                     "partial function (undefined = the machine halts), q0 ∈ Q start state, B ∈ Γ the blank, F ⊆ Q accepting "
                     "states."))
n.h2("3. Instantaneous Descriptions (sl. 27–41)")
n.p("After finitely many moves only finitely many cells have been visited, so an ID shows only the cells between the "
    "leftmost and rightmost non-blank (plus the scanned cell): **X1X2…Xi−1 q XiXi+1…Xn** — state q, head on Xi. ⊢ one move.")
n.code(["δ(q, Xi) = (p, Y, L):  X1…Xi−1 q Xi Xi+1…Xn  ⊢  X1…Xi−2 p Xi−1 Y Xi+1…Xn",
        "δ(q, Xi) = (p, Y, R):  X1…Xi−1 q Xi Xi+1…Xn  ⊢  X1…Xi−1 Y p Xi+1…Xn",
        "Boundary cases:  i = 1, move L:  q X1…Xn ⊢ p B Y X2…Xn      i = n, move R:  X1…Xn−1 q Xn ⊢ X1…Xn−1 Y p B",
        "A blank written at the end (or start) joins the infinite blanks and disappears from the ID."], size=8.5)
n.h2("4. Language, Halting, RE (sl. 116–123)")
n.p("L(M) = {w ∈ Σ∗ | q0 w ⊢∗ α p β for some p ∈ F}. A TM **halts** when it is in a state scanning a symbol with no defined move. "
    "Languages accepted by TMs are the **recursively enumerable (RE)** languages; a TM that accepts L and halts on every input "
    "decides L (recursive language, Lesson 19). The monus machine (Lesson 13) was designed to compute a function, so its seventh "
    "component F is omitted; it halts on every input (sl. 121–123).")
n.callout("answer", ("Answers to the 'TM facts' questions (2013-14 Q3(a)): (i) Can a TM write the blank? Yes — Γ contains B and "
                     "δ may write it (e.g. erasing a symbol); it simply must not be an input symbol. (ii) Can Γ = Σ? No — "
                     "B ∈ Γ but B ∉ Σ, so Γ ⊋ Σ always. (iii) Can the head be at the same location in two successive steps? "
                     "No in the basic model: every move is L or R (the S 'stay' option exists only in multitape TMs and does "
                     "not add power). (iv) Can a TM have a single state? Yes: a one-state TM is legal (the state is both start and accepting, or "
                     "just a halting state). It can only apply the same rule to every scanned symbol, so it recognises trivial "
                     "languages: if the single state q0 is accepting, the start ID q0w already has an accepting state, so L = Σ∗; "
                     "if it is not accepting, no ID ever has one, so L = ∅. So yes, it is allowed, but it is useless for "
                     "anything else — a single state cannot count or compare."))
n.h2("Exam Approach")
n.numbered(["Formal parts: list Q, Σ, Γ, δ (as a table), q0, B, F.",
            "Tracing: write each ID as left-tape · state · scanned symbol · right-tape, one line per move.",
            "'Describe L(M)' for a given rule set: follow the loop of states on a few strings and generalise."])
n.practice("Lesson 11", "(a) Actual — 2006-07 Q12. (b) Actual — 2007-08 Q11. (c) Actual — 2013-14 Q3(a). (d) Actual — 2008-09 Q3(a).",
           ["(a) What is the language of a Turing machine? Define recursive language. M = ({q0,q1,qf}, {0,1}, {0,1,B}, δ, q0, B, {qf}) "
            "with δ(q0,0) = (q1,1,R), δ(q0,B) = (qf,B,R), δ(q1,1) = (q0,0,R), δ(q1,B) = (qf,B,R). Describe L(M). (10)",
            "(b) Recursive, RE and non-RE languages? M as above with δ(q0,0) = (q0,B,R), δ(q0,1) = (q1,B,R), δ(q1,1) = (q1,B,R), "
            "δ(q1,B) = (qf,B,R). Describe L(M). (6 + 4)",
            "(c) Answer and explain: can a TM ever write the blank symbol? Can Γ equal Σ? Can the head be in the same cell in two "
            "successive steps? Can a TM have just one state? (7)",
            "(d) Give the formal notation of the Turing machine. (2⅓)"])
n.solution()
n.answer("(a)", "L(M) = {w | q0w ⊢∗ α qf β}. Recursive: L = L(M) for a TM that halts on every input. For the given M: "
         "q0 reads 0 → q1 (writes 1), q1 reads 1 → q0 (writes 0): the machine alternates, consuming 0, 1, 0, 1, …; it "
         "accepts in qf when it meets the blank in q0 (after an even number of symbols) or in q1 (after an odd number). "
         "**L(M) = (01)∗(0 ∪ ε)** — strings alternating 0,1,0,1,… starting with 0 (ε, 0, 01, 010, 0101, …); any other "
         "string reaches a state with no move and halts non-accepting. (The tape ends up complemented, but the "
         "language is what is accepted.) Check: 011: q0 0→q1, q1 1→q0, q0 1: no move → reject.")
n.answer("(b)", "Definitions: Lesson 19. M erases a block of 0's in q0 (writing B), then on the first 1 goes to q1 and erases "
         "1's, accepting at the blank. **L(M) = 0∗1⁺ = {0^m1^k | m ≥ 0, k ≥ 1}** — ε is rejected (q0 on B has no move). "
         "Checked by simulation on all strings up to length 9.")
n.answer("(c)", "EXAM-READY ANSWER in §4; shortest form: yes / no / no / yes (single state both start and accepting; e.g. "
         "accepts {w} only trivially).")
n.answer("(d)", "EXAM-READY ANSWER in §2.")

# ---------------------------------------------------------- L12
n.lesson("Lesson 12 — Designing Language-Deciding TMs", "Slides 42–70 + TF problems")
n.h2("1. The Marking Technique: {0^n1^n | n ≥ 1} (sl. 42–65)")
n.p("Repeatedly change the leftmost 0 to X, move right over 0s and Ys to the first 1, change it to Y, move back left to the "
    "rightmost X, step right and repeat. When no 0 is left (the next symbol is Y), check that only Ys remain up to the "
    "blank. The tape visited always matches X∗0∗Y∗1∗ (sl. 47). Any other shape ⇒ no move ⇒ halt without accepting.")
fig(n, "A4", 46, "Figure 12.1 — Transition table of the 0^n1^n TM (sl. 46)", clip=(0.05, 0.2, 0.95, 0.88), width_cm=11)
tm("0n1n", "TM for {0^n1^n | n ≥ 1}:", "q0 = start of a round, q1 = seek a 1, q2 = return, q3 = final check")
tr("0n1n", "0011")
n.p("On 0010 the machine reaches X X Y 0 q1 ⊔ and has no move for ⊔ in q1 (sl. 64–65) — rejected.")
fig(n, "A4", 105, "Figure 12.2 — Transition diagram of the same TM; arcs X/YD (sl. 105)", clip=(0.03, 0.12, 0.97, 0.9), width_cm=12)
n.p("Diagram notation (sl. 66–67): an arc q → p labelled X/YD means δ(q, X) = (p, Y, D); ← is L, → is R; double circle = accepting; "
    "the blank symbol is B unless stated otherwise.")
n.h2("Exam Approach — Deciding a Language")
n.numbered(["Describe the working principle in 2–4 sentences first (the examiner gives marks for it).",
            "Choose marking symbols; one round = one matched group; state what the tape looks like between rounds.",
            "Give the table / diagram; make every non-accepting situation simply have no move.",
            "Trace one member (IDs) and one non-member."])
n.practice("Lesson 12", "(a) Actual — 2006-07 Q10, 2007-08 Q7, 2011-12-style. (b) Actual — 2015-16 Q7(a). (c) Actual — 2013-14 Q2(a). "
           "(d) Actual — 2009-10 Q12(b). (e) Actual — 2016-17 Q6(c). (f) Actual — 2014-15 Q8(b), 2012-13 Q3(b). "
           "(g) Actual — 2010-11 Q11(b). (h) Actual — 2009-10 Q12(a).",
           ["(a) Build a TM for {0^n1^n | n ≥ 1} (or ≥ 0); transition diagram/table; IDs on 0011. (10)",
            "(b) Design a TM for {a^nb^nc^n | n ≥ 1}; briefly describe the working principle. (13)",
            "(c) Build a TM to recognise L = {0^N1^N0^N | N ≥ 0}. (7)",
            "(d) TM deciding {a^nc^nb^nd^n | n ≥ 0}. (7)",
            "(e) Define a TM for the set of strings with an equal number of 0s and 1s. (10)",
            "(f) Draw the state diagram of a TM that decides {w−w | w ∈ {a,b}∗}; and a high-level description with state "
            "diagram for {w−w−w | w ∈ {a,b}∗}. (7)",
            "(g) State diagram and configurations (on aaaab) of a TM deciding {a^(2^n) b | n ≥ 0} (the input aaaab has four a's). (8⅓)",
            "(h) Write out in full a TM that scans right until it finds two consecutive a's and then halts, alphabet {a, b, ⊔, ▷}. (3)"])
n.solution()
n.answer("(a)", "§1. For n ≥ 0 add δ(q0, ⊔) = (q4, ⊔, R).")
n.answer("(b)", "Principle: change the leftmost a to X, then the first b to Y, then the first c to Z, return to X, repeat. When "
         "no a is left, verify only Ys and Zs remain up to the blank. 'Rounds' pair one a, one b and one c.")
tm("anbncn", "TM for {a^nb^nc^n | n ≥ 1}:", "q3 = return left, q4–q5 = final check")
tr("anbncn", "aabbcc", 80)
n.answer("(c)", "Same idea with the third block of 0s marked Z; N = 0 is accepted by δ(q0, ⊔) = (q6, ⊔, R).")
tm("0n1n0n", "TM for {0^N1^N0^N | N ≥ 0}:")
n.answer("(d)", "Round: mark an a (A), the first unmarked c (C), the first unmarked b (B), the first unmarked d (D); return to "
         "the last A and repeat. When no a is left the next symbol must be C and the rest must be C∗B∗D∗ then blank.")
tm("ancnbndn", "TM for {a^nc^nb^nd^n | n ≥ 0}:")
n.answer("(e)", "Pair off: mark a 0 (X) and match it with an unmarked 1 (Y), or the other way round; repeat until a sweep finds no "
         "unmarked symbol. Accept when q0 reaches the blank having seen only X, Y.")
tm("eq01", "TM for equal numbers of 0s and 1s:", "q1 looks for a 1, q2 for a 0, q3 returns to the left end")
n.answer("(f)", "Compare the pieces symbol by symbol: mark the first unmarked symbol of w (X for a, Y for b), remember it in the "
         "state, skip to the first unmarked symbol after '−', check it is the same and mark it, return and repeat; "
         "finally check that no unmarked symbol is left after '−'.")
tm("w-w", "TM for {w−w}:", "sa/sb remember a/b; ta/tb check the right copy")
n.p("For {w−w−w}: the same round marks one symbol in EACH of the three blocks (the remembered symbol must match in blocks 2 "
    "and 3) — states sa/sb → ta/tb → ua/ub → va/vb → back; when q0 reaches the first '−' check that blocks 2 and 3 are "
    "fully marked.")
tm("w-w-w", "TM for {w−w−w}:")
n.answer("(g)", "Principle: sweep right crossing out every second a; the number of a's must be even in every sweep (or exactly "
         "one a remains) — powers of two are exactly the numbers that stay even until they reach 1. Our machine (states s, t, r) "
         "keeps the 1st, 3rd, 5th … a and crosses out the 2nd, 4th, …; if a sweep ends at b with an odd number > 1 of a's it "
         "halts without accepting; if a single a remains it accepts.")
tm("pow2", "TM for {a^(2^n) b | n ≥ 0}:")
tr("pow2", "aaaab", 60)
n.answer("(h)", "q0 on b stays (moves right), on a goes to q1; q1 on a accepts (two a's in a row) and on b returns to q0.")
tm("aa", "TM that scans right until it finds two consecutive a's:", "halts in qa on reading the second a; if no aa the head runs off the input and halts at ⊔ with no move")

# ---------------------------------------------------------- L13
n.lesson("Lesson 13 — TMs Computing Functions", "Slides 71–115 + TF problems")
n.p("Turing's original view: integer-valued functions with integers in unary (blocks of one symbol). The machine changes the "
    "lengths of blocks or builds new ones. The final tape contents (with infinite blanks around) is the output.")
n.h2("1. Monus m ∸ n = max(m − n, 0) (sl. 72–115)")
n.p("Input 0^m 1 0^n; output 0^(m∸n). M repeatedly finds the leftmost 0, replaces it by a blank, searches right for the 1 and "
    "on past it to a 0 which it replaces by 1; then returns left (sl. 75). Two exits: (1) searching right for a 0 it meets a "
    "blank — the n zeros are used up and n + 1 of the m zeros have been blanked; M turns the n + 1 ones into one 0 and n "
    "blanks (m ≥ n); (2) the first m zeros are all gone — the result is 0 and the rest is blanked (sl. 76).")
fig(n, "A4", 106, "Figure 13.1 — Transition diagram and table of the monus TM (sl. 105–106)", clip=(0.02, 0.2, 0.98, 0.95), width_cm=12)
tm("monus", "Monus TM (same states as the slides):", "q0 start of a round, q1 find 1, q2 find 0, q3 return, q4 clean up, q5 erase all, q6 halt")
tr("monus", "0000100", 90)
n.h2("Exam Approach — Function TMs")
n.numbered(["Fix the input/output format (unary 0^m 1 0^n, 1^a 0 1^b, binary #N, …).",
            "Describe one round and the invariant; list the exits (finished, one input exhausted).",
            "Give the table; check with the smallest cases (0, 1 or equal arguments).",
            "Check the final tape is clean (only the answer, rest blank)."])
n.practice("Lesson 13", "(a) Actual — 2015-16 Q8(a). (b) Actual — 2011-12 Q1(a). (c) Actual — 2016-17 Q5(b). "
           "(d) Actual — 2011-12 Q3(a) / 2012-13 Q3(c). (e) Constructed (slides' 4 ∸ 2 and 2 ∸ 4 traces).",
           ["(a) Design a TM that computes a ∸ b = max(b − a, 0). Initially the tape contains a followed by b, both written "
            "as consecutive 1s separated by a 0; at the end only the answer, as consecutive 1s, remains. Describe the working "
            "principle. (13)",
            "(b) Design a TM computing x − y (x ≥ y) with N represented in unary as 1^(N+1). Assume the tape holds 1^(x+1) 0 "
            "1^(y+1) and the answer is 1^(x−y+1). (8⅓)",
            "(c) TM that adds 1 to a binary number N. The tape holds # followed by N (e.g. #101) with the head on #; halt "
            "after converting N to N + 1; you may replace # by 0 or 1. Explain the principle. (20)",
            "(d) TM that, starting on #w (w ∈ {0,1}∗), writes #0^n if |w| = n is even and #1^n if n is odd. (8⅓)",
            "(e) Run the monus TM on 0^4 1 0^2 and on 0^2 1 0^4."])
n.solution()
n.answer("(a)", "Principle: pair off ones. Mark (X) the leftmost unmarked 1 of a, go right over the 0, mark the first unmarked 1 "
         "of b, return and repeat. If a's ones run out first (the machine reads 0 in q0) erase all Xs and the 0, keeping the "
         "remaining ones: they number b − a. If b runs out first (q2 reads blank) then b ≤ a: erase everything — the answer is "
         "the empty tape (0). The result 1^(b−a) is contiguous.")
tm("monus1", "TM for max(b − a, 0):", "q1 walk to the 0, q2 find an unmarked b-one, q3 return, q9–q11 clean up when a is exhausted, q7 erase all")
n.answer("(b)", "Same pairing: each round marks one 1 of the x-block and one 1 of the y-block. The y-block has y + 1 ones; "
         "after them the machine discovers the y-block is exhausted. If the x-block still has an unmarked 1 it was marked "
         "wrongly in the last round (the over-marked X); the clean-up erases the markers and turns the last two "
         "(or one, when x = y) marked cells of the left block into 1s so that exactly x − y + 1 ones remain.")
tm("unsub", "TM for 1^(x+1) 0 1^(y+1) → 1^(x−y+1):")
n.answer("(c)", "Principle (binary increment): go to the right end; flip trailing 1s to 0 moving left; the first 0 becomes 1 and "
         "the machine halts; if the # is reached (all 1s), replace # by 1.")
tm("inc", "TM adding 1 to a binary number written after #:")
n.p("#101 → q0 on #, q1 skips 101, blank → q2 on 1 → 0 (left), 0 → 1: #110 ✓; #111 → #000 and then # → 1: 1000 ✓ "
    "(checked on all N up to length 6).")
n.answer("(d)", "Pass 1 (left to right): flip a parity state between 'even' and 'odd' while skipping symbols. At the blank, move "
         "left and overwrite every symbol with 0 (even) or 1 (odd) until # is reached; halt. The parity is stored in the "
         "state (storage in the finite control).")
tm("parity", "TM for #w → #0^n (n even) / #1^n (n odd):")
n.answer("(e)", "4 ∸ 2 = 2: tape ends 00; 2 ∸ 4 = 0: tape ends blank (exit 2: all remaining 1s and 0s are blanked). "
         "Both runs were checked by simulation (all m, n up to 7).")

n.quick_notes("Quick Notes — TM Basics", "Revision points for Lessons 11–13.", [
    ("L11 · Definition", ["M = (Q, Σ, Γ, δ, q0, B, F); δ(q, X) = (p, Y, D), D ∈ {L, R}; head must move; B ∈ Γ − Σ.",
                          "ID: X1…Xi−1 q Xi…Xn; boundary cases: left of X1, blank written at an end disappears.",
                          "L(M): reach an accepting state; halt = no move; RE = TM-accepted languages. Γ ≠ Σ; blank may be written."]),
    ("L12 · Deciders", ["Marking: X/Y/Z for matched symbols; one round per group; accept when only marks remain.",
                        "0^n1^n: 5 states q0–q4 (q0: 0→X; q1 over 0,Y; 1→Y; q2 back; q3 check Y∗⊔).",
                        "a^nb^nc^n: X, Y, Z; w−w: remember a/b in the state; equal counts: X + opposite Y; 2^n: cross out every 2nd a."]),
    ("L13 · Functions", ["Monus 0^m10^n: erase leftmost 0, find 1, turn first 0 after it into 1, return; exits: blank (m ≥ n) or no 0 left (result 0).",
                         "Increment: right end, 1→0 leftwards, first 0 (or #) → 1. Parity: state flips, rewrite symbols with the parity digit."]),
], diagrams=[(PDF["A4"], 105, "0^n1^n TM diagram (sl. 105)", K, 11)])
print(n.save())
