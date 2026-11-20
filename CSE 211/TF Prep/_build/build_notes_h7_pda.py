"""Hakim Sir — lec_08_pda → CSE211_Hakim_PDA_Notes.docx (Lessons 22–24). PDAs verified in pda_designs.py."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import new_notes, fig, PRACT_NOTE, PDF, load, fmt_marks
from pda_designs import P

n = new_notes("H", "Pushdown Automata — Design", "CSE211_Hakim_PDA_Notes.docx")
K = (0.03, 0.1, 0.97, 0.95)


def plist(key, title):
    lines = [title] + P[key].lines() + ["(label: input, pop → push; ε = nothing; Z = bottom marker; accept = final state, input consumed)"]
    n.code(lines, size=8.5)


def trace(key, w):
    t = P[key].trace(w)
    s = " ⊢ ".join(f"({q}, {r}, {st})" for q, r, st in t)
    n.code([f"Accepting computation on {w}:"] + [s[i:i + 105] for i in range(0, len(s), 105)], size=8.5)


n.front_matter(
    contents=[
        ("Exam Map — What the TF Papers Ask", "where the PDA questions are tracked"),
        ("Lesson 22 — Why a Stack; the PDA and Its Computations", "6-tuple, labels a, b → c, configurations, 0^n1^n"),
        ("Lesson 23 — Nondeterminism and Design Patterns", "guess the midpoint, guess the branch, design checklist"),
        ("Lesson 24 — Ten Worked PDA Designs and TF Problems", "count/match, store/reverse, i = j or i = k, nested blocks"),
        ("Quick Notes — PDA Design", "revision bullets + key diagrams"),
    ],
    source_note=("Slide numbers refer to the PDF pages of lec_08_pda.pdf (71 pages). Sipser notation is used: a transition "
                 "'a, b → c' reads a, pops b, pushes c (ε = nothing). Every PDA in this note was run by a simulator on all "
                 "strings up to length 7 (4–5 for larger alphabets) against the language definition. " + PRACT_NOTE))

n.h1("Exam Map — What the TF Papers Ask")
qs = [q for q in load()["questions"] if q["teacher"] == "A" and q["lesson"] in (5, 6, 7, 8, 9, 10) and q["key"].startswith("pda")]
rows = {}
for q in qs:
    rows.setdefault(q["year"], []).append(f"Q{q['qno']} {q['question']} ({fmt_marks(q['marks'])})")
import re
order = sorted(rows, key=lambda y: int(re.match(r"\d{4}", y).group()), reverse=True)
n.table(["Session", "PDA questions (all tracked in Atif Sir's tracker, tab 2)"], [[y, " · ".join(rows[y])] for y in order],
        widths_cm=[2.6, 14.6], font_size=8.5)
n.callout("focus", ("PDA topics are taught by BOTH teachers. In every past paper the PDA questions sat in the Turing-machine "
                    "section, so the tracker lists them under Atif Sir's part (PDA tab) and this note has no tracker rows of "
                    "its own — it is the design workshop for them. The ★★★ design questions are i = j or i = k (2022-23, "
                    "Jan-2020; 2013-14 had j = k), nested/sequential blocks a^nb^mc^md^n and a^nb^nc^md^m (2023-24, "
                    "2017-18), and ARITH (2021-22, 2019-20). Lesson 24 solves the first two in Hakim Sir's notation; "
                    "ARITH, traces and conversions are in the Atif PDA note."))

# ------------------------------------------------------------ L22
n.lesson("Lesson 22 — Why a Stack; the PDA and Its Computations", "Slides 1–28")
n.h2("1. Why a Stack? (sl. 4–10)")
n.p("A = {0^n1^n} needs unbounded memory: a DFA has finitely many states and cannot store n. A stack (last in, first out; "
    "push and pop only at the top) can push one marker per 0 and pop one per 1, detecting mismatch or wrong order. The "
    "stack height records #0 − #1 (sl. 8). Bad strings fail: 001 ends with a 0 left on the stack; 011 needs a pop from an "
    "empty stack; 0101 has a 0 after the 1-phase began — no legal move (sl. 10).")
fig(n, "H8", 7, "Figure 22.1 — PDA architecture: read-only input, finite control, stack (sl. 7)", clip=K, width_cm=10)
n.h2("2. Formal Definition (sl. 11–21)")
n.formula(["P = (Q, Σ, Γ, δ, q0, F)", "δ : Q × Σε × Γε → P(Q × Γε)"])
n.p("Q states, Σ input alphabet, Γ stack alphabet (may contain input symbols, bookkeeping symbols, a bottom marker $ / Z), "
    "q0 start, F accepting states. (r, c) ∈ δ(q, a, b): move q → r, read a (unless ε), pop b (unless ε), push c (unless ε). "
    "δ returns a SET — the PDA is nondeterministic (sl. 16–19).")
n.table(["Label", "Meaning"], [["0, ε → 0", "read 0, pop nothing, push 0"], ["1, 0 → ε", "read 1, pop 0, push nothing"],
                               ["ε, ε → $", "read nothing, push the bottom marker"], ["ε, $ → ε", "remove the marker"]],
        widths_cm=[4, 13.2])
n.callout("memorize", "Pop/push combinations (sl. 17): X → Y replace; X → ε pop; ε → Y push; ε → ε no stack change. "
          "ε in the input position = no input read; ε is an instruction 'do nothing here', not a symbol (sl. 21).")
n.h2("3. Configurations and Acceptance (sl. 22–24)")
n.p("Configuration (q, w, s): state, unread input, stack with top on the left. One step: if (r, c) ∈ δ(q, a, b) then "
    "(q, aw, bs) ⊢ (r, w, cs). Acceptance by final state: (q0, w, ε) ⊢∗ (qf, ε, s) for some qf ∈ F — the whole input must be "
    "consumed and SOME branch must end in an accepting state (stack contents irrelevant). Acceptance by empty stack is the "
    "other convention; both recognise the same class (Atif Lec 3).")
n.h2("4. A Complete PDA for 0^n1^n (sl. 26–28)")
fig(n, "H8", 26, "Figure 22.2 — PDA for {0^n1^n | n ≥ 0} (sl. 26)", clip=K, width_cm=10)
n.code(["(qpush, 0011, ε) ⊢ (qpush, 011, 0) ⊢ (qpush, 11, 00) ⊢ (qpop, 1, 0) ⊢ (qpop, ε, ε) ⊢ (qacc, ε, ε)",
        "The direct qpush → qacc ε-move handles n = 0."])
n.p("Correctness (sl. 27): every 0^n1^n pushes n and pops n markers; conversely an accepting run reads only 0s while "
    "pushing, then only 1s while popping, each 1 matching one earlier 0.")
n.practice("Lesson 22", "(a) Constructed (concept check, sl. 69). (b) Constructed.",
           ["(a) Why does δ return a set? What does 1, 0 → ε mean? Can a PDA accept with a non-empty stack under final-state "
            "acceptance? Why must the entire input be consumed?",
            "(b) Trace the PDA of Figure 22.2 on 001 and on 0101 and explain why each is rejected."])
n.solution()
n.answer("(a)", "A set because the PDA may have several possible moves (nondeterminism: guess a midpoint, a branch). "
         "1, 0 → ε: read 1 and pop a 0. Yes — final-state acceptance ignores the stack. The whole input must be read, "
         "otherwise a machine could accept after seeing only a prefix (e.g. accept 0011… after 01).")
n.answer("(b)", "001: (qpush, 001, ε) ⊢ (qpush, 01, 0) ⊢ (qpush, 1, 00) ⊢ (qpop, ε, 0) — input finished but the only way to "
         "qacc needs the stack empty in the drawn PDA's sense (the extra 0 cannot be matched): no accepting branch. "
         "0101: after (qpop, 01, ε) the next symbol 0 has no move in qpop — every branch dies.")

# ------------------------------------------------------------ L23
n.lesson("Lesson 23 — Nondeterminism and Design Patterns", "Slides 29–43")
n.h2("1. Guess the Midpoint: ww^R (sl. 30–33)")
n.p("B = {ww^R}: push the first half, at the midpoint switch to matching — but no delimiter marks the midpoint. A "
    "nondeterministic ε-move guesses it; wrong guesses simply die (sl. 31).")
fig(n, "H8", 32, "Figure 23.1 — PDA for {ww^R}: the ε-move guesses the midpoint (sl. 32)", clip=K, width_cm=10)
n.code(["(qpush, 0110, ε) ⊢ (qpush, 110, 0) ⊢ (qpush, 10, 10) ⊢ (qmatch, 10, 10) [guess] ⊢ (qmatch, 0, 0) ⊢ (qmatch, ε, ε) ⊢ (qacc, ε, ε)"],
       size=8.5)
n.p("With a delimiter, {w#w^R}, the boundary is visible and no guess is needed — a deterministic PDA suffices (sl. 34). "
    "For D = {0^i1^j2^k | i = j or j = k} the PDA branches nondeterministically into 'check i = j' or 'check j = k': "
    "**branching implements union** (sl. 35).")
n.h2("2. Design Patterns (sl. 37–39)")
n.table(["Pattern", "Stack use", "Typical languages"],
        [["Count and match", "push per symbol, pop per matching symbol", "a^nb^n, a^ib^jc^k with i = j"],
         ["Store and reverse", "push symbols, pop and compare", "w#w^R, ww^R, palindromes"],
         ["Guess a boundary", "ε-move to the next phase at any time", "midpoints, which condition of a union, decompositions"]],
        widths_cm=[3.6, 6.6, 7.0], font_size=9)
n.h2("3. Checklist and Common Mistakes (sl. 40–43)")
n.numbered(["What must survive an unbounded distance? What does each stack symbol mean?",
            "When do you push, when pop? Is the phase boundary visible or guessed?",
            "Which wrong orders must have no transition? How are ε and empty input handled?",
            "Why can no string outside L reach an accepting state?"])
n.callout("trap", "Accepting while input remains; forgetting n = 0 (ε); popping without checking the symbol; transitions that "
          "allow the wrong order; treating nondeterminism as 'one arbitrary choice' (it is 'accept if SOME branch "
          "accepts'); confusing ε with a stack symbol (sl. 41). Nondeterminism strictly increases PDA power (unlike FAs), "
          "and one stack still cannot do {0^n1^n2^n} (sl. 42–43).")

# ------------------------------------------------------------ L24
n.lesson("Lesson 24 — Ten Worked PDA Designs and TF Problems", "Slides 44–71")
n.p("Convention (sl. 45): bottom marker Z pushed first; accept by final state, with the accepting move taken only when Z is "
    "visible again. Push for the part to remember, pop for the part that must match, let wrong order/count get stuck.")
n.table(["#", "Language", "Stack strategy (sl.)"],
        [["1", "a^nb^(2n)", "push X per a; read b's in pairs, the second b of each pair pops (46–47)"],
         ["2", "a^ib^j, i ≤ j", "push per a; each early b pops; after Z is visible extra b's are free (48–49)"],
         ["3", "a^ib^jc^k, i = k", "push per a, ignore b's, pop per c (50–51)"],
         ["4", "w#w^R", "push before #, pop and compare after (52–53)"],
         ["5", "palindromes", "push, guess middle (ε for even, consume one symbol for odd), match (54–55)"],
         ["6", "balanced parentheses", "push per (, pop per ) (56–57)"],
         ["7", "#0 = #1", "stack holds the current imbalance; opposite symbol cancels (58–59)"],
         ["8", "a^ib^jc^k, i = j or j = k", "branch: check i = j (ignore c's) or j = k (ignore a's) (60–61)"],
         ["9", "a^nb^mc^md^n", "push A's, then B's; pop B's on c's, A's on d's — LIFO nesting (62–63)"],
         ["10", "a^ib^jc^(i+j)", "push per a and per b; pop per c (64–65)"]], widths_cm=[0.8, 4.6, 11.8], font_size=9)
fig(n, "H8", 60, "Figure 24.1 — PDA for a^ib^jc^k with i = j or j = k (sl. 60)", clip=K, width_cm=12)
fig(n, "H8", 62, "Figure 24.2 — PDA for a^nb^mc^md^n (sl. 62)", clip=K, width_cm=11)
n.h2("Exam Approach — PDA Design")
n.numbered(["Write the stack strategy in one sentence before drawing anything.",
            "Draw states for phases (push / skip / pop), the Z marker move first, the Z-visible accepting move last.",
            "Unions → ε-branches at the start. Unmarked boundaries → ε-moves between phases.",
            "Trace one member to acceptance and say why one non-member dies."])
n.practice("Lesson 24", "(a) Actual — 2022-23 Q8 / Jan-2020 Q8 (also tracked in Atif's tab). (b) Actual — 2023-24 Q8. "
           "(c) Actual — 2017-18 Q8. (d) Constructed — in-class problems (sl. 68).",
           ["(a) Design a PDA that recognises L = {a^ib^jc^k | i, j, k ≥ 0 and (i = j or i = k)}. Draw its transition diagram. (15)",
            "(b) Design a PDA for L = {a^nb^mc^md^n | n ≥ 1, m ≥ 1}. Draw its transition diagram. (15)",
            "(c) Design a PDA for L = {a^nb^nc^md^m | n ≥ 1, m ≥ 1}. (15)",
            "(d) Stack strategies for a^nb^(2n), 0^i1^j (i ≤ j), w#w^R, 0^i1^j2^k (i = k), palindromes — is nondeterminism "
            "genuinely useful in each?"])
n.solution()
n.answer("(a)", "Strategy: branch at the start. Branch 1 (i = j): push X per a, pop X per b, when Z is visible read any "
         "c's. Branch 2 (i = k): push X per a, read b's without touching the stack, pop X per c. Accept when Z is visible "
         "at the end of a branch.")
plist("ij_or_ik", "PDA for i = j or i = k (states: s → q → p-branch / r-branch):")
trace("ij_or_ik", "aabcc")
n.p("aabcc has i = k = 2: branch 2 accepts. aabbc: branch 1 accepts. aabc: both branches die (i ≠ j, i ≠ k).")
n.answer("(b)", "Strategy: nested dependency — push A per a; the first b pushes B on top of A's; pop B per c; pop A per d. "
         "LIFO forces all c's to match b's before any d meets an a (sl. 62–63). n, m ≥ 1 is enforced because the first b "
         "must see an A and the first c must see a B.")
plist("anbmcmdn", "PDA for a^nb^mc^md^n, n, m ≥ 1:")
trace("anbmcmdn", "aabbccdd")
n.answer("(c)", "Strategy: sequential blocks — push X per a, pop X per b; when Z reappears the first c pushes a new "
         "counter (Y above Z), further c's push Y, d's pop Y; accept when Z is visible after the d's.")
plist("anbncmdm", "PDA for a^nb^nc^md^m, n, m ≥ 1:")
n.answer("(d)", "a^nb^(2n): push X per a, pop every second b — deterministic. 0^i1^j, i ≤ j: push per 0, pop per 1, then "
         "allow extra 1s on Z — deterministic. w#w^R: deterministic (the # marks the middle). 0^i1^j2^k, i = k: the end of "
         "the 0-block is visible, deterministic in principle. Palindromes: nondeterminism is essential — the middle must "
         "be guessed (and whether the length is odd).")

n.quick_notes("Quick Notes — PDA Design", "Revision points for Lessons 22–24.", [
    ("L22 · PDA", ["P = (Q, Σ, Γ, δ, q0, F), δ : Q × Σε × Γε → P(Q × Γε). Label a, b → c = read a, pop b, push c.",
                   "Configuration (q, w, s), top on the left. Accept: input consumed, some branch in F.",
                   "0^n1^n: push per 0, pop per 1; ε-move qpush → qacc for n = 0."]),
    ("L23 · Nondeterminism", ["ww^R: ε-move guesses the midpoint; w#w^R needs no guess.",
                              "Union = branch at the start. Patterns: count/match, store/reverse, guess boundary.",
                              "Mistakes: accept with input left, forget ε, pop without checking, wrong order allowed."]),
    ("L24 · Designs", ["i = j or i = k: branch 1 pop on b's (c free); branch 2 b's free, pop on c's.",
                       "a^nb^mc^md^n: push A's then B's; pop B on c, A on d. a^nb^nc^md^m: two counters in sequence.",
                       "#0 = #1: stack stores the imbalance. a^ib^jc^(i+j): push per a and b, pop per c."]),
], diagrams=[(PDF["H8"], 32, "PDA for ww^R (sl. 32)", K, 9), (PDF["H8"], 60, "PDA for i = j or j = k (sl. 60)", K, 11)])
print(n.save())
