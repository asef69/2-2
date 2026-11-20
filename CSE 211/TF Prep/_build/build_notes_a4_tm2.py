"""Atif Sir — Lecture 5 (Turing Machine 2) → CSE211_Atif_TM_Techniques_Notes.docx (Lessons 14–15). Checks: tm_designs.py."""
import os, sys, itertools; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import new_notes, exam_map_rows, fig, PRACT_NOTE, PDF
from tm_designs import M, BL

n = new_notes("A", "Programming Techniques for Turing Machines · Bit-Manipulation Machines", "CSE211_Atif_TM_Techniques_Notes.docx")
K = (0.03, 0.1, 0.97, 0.95)


def tm(key, title, note=None, size=8):
    t = M[key]
    n.code([title] + t.lines() + [f"start {t.start}; halting/accepting {sorted(t.accept)}; ⊔ blank; x/y = checked 0/1 (or X,Y,p,q as stated)" + (f"; {note}" if note else "")], size=size)


def run(key, w):
    q, s, st = M[key].run(w)
    return f"{w}  →  tape {s.replace(BL, '⊔')}  ({st} moves, halted in {q})"


n.front_matter(
    contents=[
        ("Exam Map — What the TF Papers Ask", "the 15-mark bit-manipulation TM since 2017-18"),
        ("Lesson 14 — Storage in the State, Tracks, Subroutines", "01∗ + 10∗, w c w, multiple tracks vs multiple tapes"),
        ("Lesson 15 — Bit-Manipulation TMs: XOR, AND, OR, NOT, Equality, Addition, 2's Complement", "the one design pattern behind all of them"),
        ("Quick Notes — TM Techniques", "revision bullets + key diagrams"),
    ],
    source_note=("Slide numbers refer to the PDF pages of Lecture - 5 (Turing Machine 2).pdf (133 pages; beamer builds). "
                 "Every machine was run by a simulator against its specification on all inputs up to the stated length "
                 "(bit-string machines: all equal-length pairs up to 4 bits, strings up to 6). Notation: unchecked bits "
                 "0/1, checked bits x (a 0) and y (a 1); ⊔ = blank. The slides draw checking as a second track ([∗, a]); "
                 "x/y are the same idea written as single symbols. " + PRACT_NOTE))

n.h1("Exam Map — What the TF Papers Ask")
rows, cnt = exam_map_rows("A", {14, 15})
n.table(["Session", "Questions on TM techniques / bit manipulation"], rows, widths_cm=[2.6, 14.6], font_size=8.5)
n.callout("focus", ("★★★: every paper since 2017-18 has ONE 15-mark TM question of this kind — OR (2017-18), XOR (Jan-2020), AND "
                    "(2019-20), 2's complement (2021-22), NOT/complement after c (2022-23), equality flag (2023-24). All "
                    "are the same pattern: mark a bit, remember it in the state, run to the end, write the result, "
                    "return. Master Lesson 15's template; the 2006-08 versions (XOR/addition, 10 marks) are in it too. "
                    "'Proof idea: multi-track ⇒ single-track' (2011-12) is Lesson 14."))

# ---------------------------------------------------------- L14
n.lesson("Lesson 14 — Storage in the State, Tracks, Subroutines", "Slides 1–83, 132–133")
n.p("A TM is exactly as powerful as a conventional computer. The tricks below add only notational convenience — none extends the "
    "basic model (sl. 2).")
n.h2("1. Storage in the State (sl. 3–26)")
n.p("The finite control can hold a finite amount of data: think of the state as a tuple [q, A, B, C] (sl. 3–6). Example: "
    "M = (Q, {0,1}, {0,1,B}, δ, [q0,B], {[q1,B]}) remembers the first symbol it sees and checks that it never occurs again — "
    "L = 01∗ + 10∗. States {q0, q1} × {0, 1, B}: control q0 'first symbol not yet read', q1 'checking'; data = the "
    "remembered symbol.")
n.code(["1. δ([q0,B], a) = ([q1,a], a, R)   a ∈ {0,1}       remember the first symbol, move on",
        "2. δ([q1,a], ā)  = ([q1,a], ā, R)                  skip the other symbol (ā = complement)",
        "3. δ([q1,a], B)  = ([q1,B], B, R)                  blank reached: accept [q1,B]",
        "No rule for δ([q1,a], a): a second occurrence → halt without accepting.   (01111 accepted, 01101 rejected)"], size=8.5)
tm("store", "The same machine in single-letter state names (q1_0 = [q1,0], q1_1 = [q1,1], q1B = [q1,B]):")
n.h2("2. Multiple Tracks (sl. 27–83)")
n.p("Think of the tape as several tracks; the tape alphabet is a tuple with one component per track, e.g. [X, Y, Z]. "
    "Tracks do not add power; a common use is data on one track and a check mark on another. Example: "
    "L_wcw = {wcw | w ∈ (0+1)⁺}. Γ = {B, ∗} × {0, 1, c, B} — the first track holds the check mark ∗, the second the symbol; "
    "states {q1…q9} × {0, 1, B}, start [q1, B], accept [q9, B]; 14 rules:")
n.code(["1. [q1,B],[B,a] → [q2,a],[∗,a],R     pick up the first unchecked symbol a, check it",
        "2. [q2,a],[B,b] → R                  move right looking for c",
        "3. [q2,a],[B,c] → [q3,a],R           c found",
        "4. [q3,a],[∗,b] → R                  skip checked symbols",
        "5. [q3,a],[B,a] → [q4,B],[∗,a],L     first unchecked symbol equals a: check it, go left",
        "6. [q4,B],[∗,a] → L    7. [q4,B],[B,c] → [q5,B],L",
        "8. [q5,B],[B,a] → [q6,B],L           left block not finished",
        "9. [q6,B],[B,a] → L    10. [q6,B],[∗,a] → [q1,B],R     back to the first unchecked symbol",
        "11. [q5,B],[∗,a] → [q7,B],R          left block finished: check the right block",
        "12. [q7,B],[B,c] → [q8,B],R    13. [q8,B],[∗,a] → R    14. [q8,B],[B,B] → [q9,B],R  accept",
        "No rule when the next unchecked symbol differs, or an unchecked symbol is left after c ⇒ halt, reject."], size=8)
tm("wcw", "Single-symbol version (x/y = checked 0/1; q2a, q3a remember the symbol a):")
n.p("Trace on 011c011 (the slide animation, sl. 57–83): the machine checks 0 on the left, finds the matching 0 right of c, "
    "returns, checks 1, 1, then verifies no unchecked symbol remains — accept.")
n.callout("answer", ("Proof idea: every multi-track TM has an equivalent single-track TM (2011-12 Q1(b)). A k-track TM has tape "
                     "alphabet Γ1 × … × Γk. Define a single-track TM whose tape symbols are the k-tuples themselves (a finite "
                     "set), with Σ-symbols identified with [a, B, …, B]. Every move of the k-track machine reads and writes a "
                     "whole tuple, which is one symbol of the new alphabet — so the same δ works unchanged. Hence tracks only "
                     "give a convenient view of a larger alphabet and add no power. (Contrast: multiple TAPES have independent "
                     "heads — Lesson 16.)"))
n.h2("3. Subroutines (sl. 132–133)")
n.p("A subroutine is a set of states with a start state and a 'return' state with no moves. A 'call' is a transition to its "
    "start state. A TM has no return-address mechanism, so if several states call the same subroutine, make a copy of its states "
    "for each caller, each copy returning to a different state.")
n.practice("Lesson 14", "(a) Actual — 2011-12 Q1(b). (b) Constructed (slides). (c) Constructed (slides).",
           ["(a) Give the proof idea that every multi-track TM has an equivalent single-track TM. (7)",
            "(b) Design a TM that remembers in its finite control the first symbol of its input and accepts exactly the "
            "strings 01∗ + 10∗.",
            "(c) Using a second track for check marks, design a TM for {wcw | w ∈ (0+1)⁺} and give its rules."])
n.solution()
n.answer("(a)", "EXAM-READY ANSWER in §2.")
n.answer("(b)", "§1 with the 3-rule machine and the table above (verified on all strings up to length 9).")
n.answer("(c)", "§2: 14 rules / the single-symbol table (verified on all strings up to length 7 — exactly the strings wcw are accepted).")

# ---------------------------------------------------------- L15
n.lesson("Lesson 15 — Bit-Manipulation TMs", "Slides 84–131 (binary addition) + TF problems")
n.h2("1. The Template (binary addition, sl. 84–131)")
n.p("Tape w1 c w2 c ⊔⊔⊔ with w1, w2 equal-length binary numbers, **LSB first** ('for convenience'); the sum is written to the "
    "right of the second c. States are tuples [q, a, b, carry]: after reading a bit of w1 the state remembers it, then the "
    "bit of w2, then the machine runs to the first blank, writes the result and the new carry goes into the state, returns "
    "to the left end, and repeats. When the first c is met in q0 all bits are done: run to the end and write the carry.")
n.table(["Phase", "State", "Action"],
        [["1", "q0 [carry]", "skip checked bits; read the first unchecked bit a of w1, check it, remember a, go right"],
         ["2", "q1/s[a]", "move right over bits to the first c"],
         ["3", "q2/t[a]", "skip checked bits of w2; read the first unchecked bit b, check it, remember a, b"],
         ["4", "q3/u[a,b]", "run right to the first blank; write f(a, b, carry); remember the new carry"],
         ["5", "q4–q6/v", "run left to the blank before w1"],
         ["6", "q7/w", "q0 reads c: all of w1 done — run to the end, write the final carry, halt"]],
        widths_cm=[1.6, 3.4, 12.2], font_size=9)
fig(n, "A5", 122, "Figure 15.1 — The slide's rule 7: write the sum bit s and remember the carry c_out (sl. 122)", clip=K, width_cm=11)
fig(n, "A5", 111, "Figure 15.2 — Tape after the whole run on 101 c 011 c: sum 1101 (LSB first) (sl. 111)", clip=K, width_cm=11)
tm("add", "Addition TM (LSB first): states p_c = scanning for the next unchecked bit of w1 with carry c; s,t,u remember a,b; v returns", size=7.5)
n.p("Run: " + run("add", "101c011c") + ". (101 = 5 and 011 = 3 read LSB first: 1+0·2+1·4 = 5, 0+1·2+1·4 = 6 → 5 + 6 = 11 = 1011; "
    "LSB first '1101' ✓ — verified for all pairs up to 4 bits.)")
n.h2("2. Bitwise XOR / AND / OR (★★★ 2017-18, Jan-2020, 2019-20)")
n.p("Same template without carry: f(a, b) = a ⊕ b, a ∧ b or a ∨ b, written after the second separator in the order of "
    "the bits. Tape w1 c w2 c (c or # as the separator). Only the table of f changes — the machine below is generated from "
    "f and verified for every pair of equal-length strings up to 4 bits for all three operations.")
n.table(["a", "b", "XOR", "AND", "OR"], [[a, b, str(int(a) ^ int(b)), str(int(a) & int(b)), str(int(a) | int(b))] for a in "01" for b in "01"],
        widths_cm=[2, 2, 2.5, 2.5, 2.5])
tm("xor_c", "TM for XOR on w1 c w2 c (result after the second c): for AND/OR replace the written bit by f(a, b)", size=7.5)
n.p("Examples: " + run("xor_c", "1011c0110c").replace("  →", " →") + "   ·   " + run("and_c", "1011c0110c") + "   ·   "
    + run("or_#", "1011#0110#"))
n.h2("3. XOR with the Result Replacing the Second Number (2006-07 Q11, 2008-09 Q3)")
n.p("Tape w1#w2; the result overwrites w2 (p = result 0, q = result 1 as temporary marks so a processed bit of w2 is not "
    "read again), then w1 and the separator are erased and p/q turned into 0/1. For 0010#1011 the output is 1001 "
    "(the question's example; 1011#0010 gives 1001 too).")
tm("xor_inplace", "TM for w1#w2 → w1 ⊕ w2 (only the result left)", size=7.5)
n.p("Runs: " + run("xor_inplace", "0010#1011") + "   ·   " + run("xor_inplace", "1011#0010"))
n.h2("4. Complement: w c → w c w̄ (★★★ 2022-23 Q10)")
n.p("Mark the first unchecked bit (x/y), remember its complement, run to the first blank and write it, return; when q0 meets c "
    "all bits are done: walk back left restoring x → 0, y → 1 and halt.")
tm("notw", "TM that appends the bitwise NOT of w after the c", size=8)
n.p("Run: " + run("notw", "10110c"))
n.h2("5. Equality Flag: w1 c w2 c → write 0 if w1 = w2, else 1 (★★★ 2023-24 Q9)")
n.p("Compare bit pairs: remember a, check it, compare with the first unchecked bit of w2. Equal → check it and return; "
    "different → run to the end and write 1; all pairs equal (q0 reaches c) → run to the end and write 0.")
tm("eq", "TM writing 0 after the second c if w1 = w2, else 1", size=8)
n.p("Runs: " + run("eq", "101c101c") + "   ·   " + run("eq", "101c100c"))
n.h2("6. Signed Magnitude → 2's Complement (★★★ 2021-22 Q9)")
n.p("A signed-magnitude number has sign bit s followed by the magnitude m. If s = 0 (non-negative) the 2's-complement "
    "form is identical — halt. If s = 1 the 2's-complement form keeps s = 1 and replaces the magnitude bits by their "
    "2's complement: invert every magnitude bit and add 1 (carry out of the top is dropped). The sign bit is marked S while "
    "processing so that the increment cannot propagate into it.")
tm("twos", "TM for signed magnitude → 2's complement", size=8)
n.p("Runs: " + run("twos", "01101") + "   ·   " + run("twos", "1011") + "   ·   " + run("twos", "1000")
    + "   (−3 = 1011 in signed magnitude → 1101 in 2's complement ✓; −0 = 1000 → 1000.)")
n.h2("Exam Approach — The 15-Mark TM Design")
n.numbered(["Fix the tape format (separator, LSB or MSB first, where the answer goes); say 'assume equal length' if the question does.",
            "State the idea in 3–4 lines: one round = one bit position; the bit is remembered in the state.",
            "Name the states by role: scan for the next unchecked bit (q0), carry the bit right (s_a), find the partner (t_a), "
            "write at the end (u), return (v).",
            "Write the rules in a table (all symbols covered by one row); draw or list the diagram.",
            "Trace the small example given in the question, ID by ID or tape by tape."])
n.callout("trap", "Do not read a bit twice: always CHECK (mark) it. Return to the LEFT END via the blank. Make the final step "
          "explicit (halt state / write the carry). Equal-length numbers are an assumption in the question — use it.")
n.practice("Lesson 15", "(a) Actual — 2017-18 Q9. (b) Actual — Jan-2020 Q9. (c) Actual — 2019-20 Q9. (d) Actual — 2022-23 Q10. "
           "(e) Actual — 2023-24 Q9. (f) Actual — 2021-22 Q9. (g) Actual — 2007-08 Q8. (h) Actual — 2006-07 Q11, 2008-09 Q3(b)–(c).",
           ["(a) TM taking two numbers N1 and N2 of equal length in binary and computing their logical OR; the tape initially "
            "holds N1#N2#, where # is a separator; terminate with the OR after the second # (multiple tracks and storage in "
            "the state allowed). (15)",
            "(b) The same for XOR with tape w1 c w2 c. (15)",
            "(c) The same for AND with tape w1 c w2 c. (15)",
            "(d) Tape wc (w a binary string): design a TM that inserts the bitwise NOT of w after the c. (15)",
            "(e) Tape w1 c w2 c (equal length): write 0 after the second c if w1 = w2 and 1 otherwise. (15)",
            "(f) Design a TM that converts a signed-magnitude binary number whose MSB is 1 to 2's complement. (15)",
            "(g) TM that adds two equal-length binary numbers separated by a comma; only the sum remains. (10)",
            "(h) TM computing the XOR of two equal-length binary numbers separated by '#' and replacing the second number "
            "by the result; simulate 1011#0010. (10 + 8)"])
n.solution()
n.answer("(a)–(c)", "§2 with f = OR / XOR / AND — the machines above (verified for all pairs up to 4 bits). Working principle: "
         "check the leftmost unchecked bit of N1, remember it; at the second number check its leftmost unchecked bit; at the "
         "first blank write a ∨ b (a ⊕ b, a ∧ b); return; stop at the separator.")
n.answer("(d)", "§4 machine. wc = 10110c → 10110c01001.")
n.answer("(e)", "§5 machine. 101c101c → …c0; 101c100c → …c1.")
n.answer("(f)", "§6 machine.")
n.answer("(g)", "§1 (the addition machine, LSB first, sum after the second c; delete w1 c w2 c afterwards by a final sweep if only "
         "the sum may remain). If the numbers are MSB first, first reverse them or perform the addition from the right "
         "ends by marking bits from the right instead of the left — the machine is the mirror image.")
n.answer("(h)", "§3 machine. Simulation of 1011#0010: the helper marks x/y are written on w1, the results p/q on w2; "
         "after the 4 rounds the tape holds xyxy#pqqp ... then the clean-up erases w1 and #, giving 1001 (86 moves).")
n.quick_notes("Quick Notes — TM Techniques", "Revision points for Lessons 14–15.", [
    ("L14 · Techniques", ["Storage in the state: state = [q, data]; 01∗+10∗ remembers the first symbol.",
                          "Tracks = tuples as tape symbols; no extra power (single-track proof: use the tuples as symbols).",
                          "wcw: 14 rules, check marks ∗; subroutines = copies of state sets."]),
    ("L15 · Bit manipulation", ["Pattern: check bit a, remember; find partner b, check; run to blank; write f(a,b); return to left blank; repeat; halt at the separator.",
                                "Addition LSB first: state [q, a, b, carry]; write the final carry at the end.",
                                "NOT after c: write complement, finally restore x→0, y→1. Equality: mismatch → write 1, match to the end → write 0.",
                                "2's complement of signed magnitude: if s = 1 invert magnitude and add 1 (mark the sign S)."]),
], diagrams=[(PDF["A5"], 122, "Rule 7 of the addition TM (sl. 122)", K, 10)])
print(n.save())
