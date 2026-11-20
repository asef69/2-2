"""Build CSE209_ART_ALU_Design_Notes.docx  (Lessons 5–9).   python -P build_notes_alu.py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ALU, exam_map, marks_since, new

n = new("ALU Design · Arithmetic, Logic and Status Circuits (Mano ch. 9)", "CSE209_ART_ALU_Design_Notes.docx")
n.front_matter(
    contents=[
        ("Exam Map — What the TF Papers Ask", "ALU questions and how much they matter"),
        ("Lesson 5 — Adders and the ALU Block", "half adder, full adder, parallel adder, ALU inputs and selection lines"),
        ("Lesson 6 — The Arithmetic Circuit: Function Table and Output Carry", "B-input logic, Table 9-1, when Cout = 1"),
        ("Lesson 7 — Designing an Arithmetic Unit: the X/Y/Z Method", "identities, recipe, five TF designs solved and verified"),
        ("Lesson 8 — Logic Circuit and the Complete ALU", "mux design, efficient design, Table 9-4, one typical stage"),
        ("Lesson 9 — Status Register, Overflow and Comparator Circuits", "C, S, Z, V; why V = XOR of last carries; comparison circuits"),
        ("Quick Notes — ALU Design", "merged revision notes + key diagrams"),
    ],
    source_note="Slide numbers refer to ALU Design.pdf (Tushar Sir, 23 slides, from Mano, Digital Logic and Computer Design §9.3–9.7). "
                "Every ALU design in these notes was checked by simulating all 256 input pairs (A, B) of a 4-bit ALU for every selection code "
                "(script _build/verify.py).")

n.h1("Exam Map — What the TF Papers Ask")
n.p("Every Tushar-Sir-part question that this deck answers (★ = 2019-20 or later):")
exam_map(n, 2)
n.callout("focus", f"The ALU design question — 'derive X_{{i}}, Y_{{i}}, Z_{{i}} for the parallel adders of an ALU that performs this table' — is asked in **every paper from 2017-18 to 2023-24** "
          f"(7 times, 10–25 marks each; {marks_since(2)} marks since 2019-20). It is the single most valuable topic of the ART part. "
          "Master Lesson 7's recipe and its identity table, then practise the five solved designs cold. Lesson 9 (status bits) gives a further 8–15 marks most years.")

# ================================================================== LESSON 5
n.lesson("Lesson 5 — Adders and the ALU Block", "Slides 1–5 (ALU Design)")
n.h2("1. What an ALU Is (sl. 2)")
n.p("An Arithmetic Logic Unit performs both arithmetic and logic micro-operations on two n-bit inputs A and B and produces F.")
n.figure_from_pdf(ALU, 2, "Figure 5.1 — Block diagram of a 4-bit ALU (sl. 2)", clip=(0.02, 0.27, 1.0, 0.92), width_cm=12.5)
n.table(["Signal", "Name", "Job"], [
    ["s2", "Mode select", "Chooses arithmetic (s2 = 0) or logic (s2 = 1) operation"],
    ["s1 s0", "Function select", "Chooses which operation inside the mode"],
    ["C_{in}", "Input carry", "Adds 1 to arithmetic results — doubles the number of arithmetic variants"],
    ["C_{out}", "Output carry", "Carry out of the most significant stage (used by the status register)"],
], widths_cm=[2.2, 3.5, 11.5])
n.h2("2. Half Adder and Full Adder (sl. 4–5)")
n.table(["x", "y", "C", "S"], [["0", "0", "0", "0"], ["0", "1", "0", "1"], ["1", "0", "0", "1"], ["1", "1", "1", "0"]], widths_cm=[1.5] * 4)
n.formula(["Half adder:  S = x'y + xy' = x ⊕ y,    C = xy",
           "Full adder:  S = x'y'z + x'yz' + xy'z' + xyz = x ⊕ y ⊕ z,    C = xy + xz + yz"])
n.figure_from_pdf(ALU, 5, "Figure 5.2 — Full adder: truth table, equations and gate circuit (two half adders + OR) (sl. 5)", clip=(0.0, 0.15, 1.0, 1.0), width_cm=12.5)
n.h2("3. Parallel Adder (sl. 3)")
n.p("An n-bit parallel adder is n full adders in cascade: the carry out of stage i is the carry in of stage i + 1. C_{1} is the input carry, C_{n+1} the output carry.")
n.figure_from_pdf(ALU, 3, "Figure 5.3 — 4-bit parallel adder built from full adders (sl. 3)", clip=(0.04, 0.3, 0.97, 1.0), width_cm=11.5)
n.callout("memorize", "The full adder of stage i always computes F_{i} = X_{i} ⊕ Y_{i} ⊕ Z_{i} and C_{i+1} = X_{i}Y_{i} + X_{i}Z_{i} + Y_{i}Z_{i}. "
          "An ALU is built by putting small combinational circuits in front of this adder that decide what X_{i}, Y_{i} and the carry Z_{i} are.")
n.practice("Lesson 5", "Constructed (adder basics).", [
    "(a) Add A = 0111 and B = 0110 on a 4-bit parallel adder with C_{1} = 0. Give every carry and the result.",
    "(b) Show that a full adder can be built from two half adders and an OR gate.",
])
n.solution()
n.answer("(a)", "Bit 1 is the LSB; C_{1} = 0.")
n.code(["Stage     1    2    3    4",
        "A_i       1    1    1    0       (A = 0111, bit 1 = LSB)",
        "B_i       0    1    1    0       (B = 0110)",
        "C_i       0    0    1    1",
        "F_i       1    0    1    1  → F = 1101,  C_5 = 0",
        "Unsigned: 7 + 6 = 13 = 1101 ✓.  Signed 4-bit: +7 + 6 = +13 → overflow (result looks −3)"])
n.answer("(b)", "HA1 adds x and y: S1 = x ⊕ y, C1 = xy. HA2 adds S1 and z: S = x ⊕ y ⊕ z, C2 = (x ⊕ y)z. OR: C = xy + (x ⊕ y)z = xy + xz + yz — exactly the circuit on slide 5.")

# ================================================================== LESSON 6
n.lesson("Lesson 6 — The Arithmetic Circuit: Function Table and Output Carry", "Slides 6–11 (ALU Design)")
n.h2("1. Eight Operations From One Parallel Adder (sl. 6–7)")
n.p("Keep A on the X inputs and change only what goes into the Y inputs (B, B', all 0s or all 1s) and the input carry:")
n.table(["Y input", "C_{in} = 0", "C_{in} = 1"], [
    ["B", "F = A + B (addition)", "F = A + B + 1 (add with carry)"],
    ["B' (1's complement)", "F = A + B' (A plus 1's complement of B = A − B − 1)", "F = A + B' + 1 = A − B (subtraction)"],
    ["All 0s", "F = A (transfer A)", "F = A + 1 (increment)"],
    ["All 1s (= −1)", "F = A − 1 (decrement)", "F = A − 1 + 1 = A (transfer A)"],
], widths_cm=[3.4, 6.9, 6.9])
n.figure_from_pdf(ALU, 6, "Figure 6.1 — Addition, add with carry, A plus 1's complement of B, subtraction (sl. 6)", clip=(0.08, 0.13, 0.95, 1.0), width_cm=10.0)
n.h2("2. True/Complement, One/Zero Circuit (sl. 8)")
n.p("One gate pair per bit chooses what reaches Y_{i}:")
n.formula(["X_{i} = A_{i}         Y_{i} = B_{i}s_{0} + B_{i}'s_{1}         (s_{1}s_{0}: 00 → 0, 01 → B_{i}, 10 → B_{i}', 11 → 1)"])
n.figure_from_pdf(ALU, 8, "Figure 6.2 — True/complement, one/zero circuit (Fig. 9-7) (sl. 8)", clip=(0.02, 0.15, 1.0, 0.9), width_cm=12.0)
n.h2("3. The Complete Arithmetic Circuit and Its Function Table (sl. 9–10)")
n.figure_from_pdf(ALU, 9, "Figure 6.3 — 4-bit arithmetic circuit (Fig. 9-8): B-input logic (red box) in front of four full adders (sl. 9)", clip=(0.0, 0.12, 0.42, 1.0), width_cm=8.0)
n.table(["s1", "s0", "C_{in}", "Y equals", "Output", "Function"], [
    ["0", "0", "0", "0", "F = A", "Transfer A"], ["0", "0", "1", "0", "F = A + 1", "Increment A"],
    ["0", "1", "0", "B", "F = A + B", "Add B to A"], ["0", "1", "1", "B", "F = A + B + 1", "Add B to A plus 1"],
    ["1", "0", "0", "B'", "F = A + B'", "Add 1's complement of B to A"], ["1", "0", "1", "B'", "F = A + B' + 1", "Add 2's complement of B to A (A − B)"],
    ["1", "1", "0", "All 1s", "F = A − 1", "Decrement A"], ["1", "1", "1", "All 1s", "F = A", "Transfer A"],
], widths_cm=[1.0, 1.0, 1.3, 2.1, 3.4, 8.4])
n.p("Table 9-1 (sl. 10). The generic picture (sl. 9, right): selection variables + A + B → combinational circuit → X, Y → n-bit parallel adder (with C_{in}). Every design question in Lesson 7 only redesigns that combinational circuit.")
n.h2("4. When Is the Output Carry 1? (sl. 11) ★")
n.table(["s1 s0 C_{in}", "Function", "C_{out} = 1 if", "Comment (n-bit unsigned)"], [
    ["000", "F = A", "never", "C_{out} is always 0"],
    ["001", "F = A + 1", "A = 2^{n} − 1", "C_{out} = 1 and F = 0 if A = 2^{n} − 1 (all 1s)"],
    ["010", "F = A + B", "A + B ≥ 2^{n}", "overflow (unsigned) when C_{out} = 1"],
    ["011", "F = A + B + 1", "A + B ≥ 2^{n} − 1", "overflow when C_{out} = 1"],
    ["100", "F = A − B − 1", "A > B", "if C_{out} = 0 then A ≤ B and F = 1's complement of (B − A)"],
    ["101", "F = A − B", "A ≥ B", "if C_{out} = 0 then A < B and F = 2's complement of (B − A)"],
    ["110", "F = A − 1", "A ≠ 0", "C_{out} = 1 except when A = 0"],
    ["111", "F = A", "always", "C_{out} is always 1"],
], widths_cm=[2.3, 3.2, 3.2, 8.5])
n.p("Reason: the adder really computes A + Y + C_{in} on n bits. For A − B − 1 = A + B' = A + (2^{n} − 1 − B): the sum reaches 2^{n} exactly when A − B − 1 ≥ 0, i.e. A > B. "
    "For A − 1 = A + (2^{n} − 1): the sum reaches 2^{n} when A ≥ 1.")
n.callout("trap", "In subtraction a carry of 1 means **no borrow** (A ≥ B). Do not read C_{out} = 1 as 'overflow' for the subtract rows.")
n.exam_approach([
    "Rewrite each operation as A + Y + C_{in} with Y ∈ {B, B', 0, 1s}.",
    "For carry questions compute when the true sum A + Y + C_{in} ≥ 2^{n} and translate back (A ≥ B, A ≠ 0 …).",
    "Quote Table 9-1 / 9-2 rows exactly; the examiner checks the conditions.",
])
n.practice("Lesson 6", "(a) Actual — 2017-18 6(b). (b) Constructed.", [
    "(a) For each arithmetic operation of 2017-18 6(a) — Addition (A + B), Transfer A, Decrement A, Add 1's complement of B to A — find the condition under which the output carry is 1. (10)",
    "(b) A = 0101, B = 0011. Compute A − B on the arithmetic circuit (s1 s0 C_{in} = 101) and B − A (swap inputs). Interpret C_{out} each time.",
])
n.solution()
n.table(["Operation", "Adder computes", "C_{out} = 1 when (4-bit)", "Example"], [
    ["Addition", "A + B", "A + B ≥ 16 (unsigned overflow)", "1001 + 1000: C_{out} = 1"],
    ["Transfer A", "A + 0 + 0", "never — C_{out} = 0 always", "—"],
    ["Decrement A", "A + 1111", "A ≠ 0", "0000 + 1111 = 1111, C_{out} = 0"],
    ["A + B'", "A + (15 − B)", "A > B", "0101 + 1100 = 1 0001: C_{out} = 1 (5 > 3)"],
], widths_cm=[3.0, 3.2, 5.6, 5.4])
n.code(["A − B: 0101 + 1100 + 1 = 1 0010 → F = 0010 (= 2), Cout = 1 → A ≥ B, result is A − B",
        "B − A: 0011 + 1010 + 1 = 0 1110 → F = 1110, Cout = 0 → B < A, F = 2's complement of 2 (−2)"])

# ================================================================== LESSON 7
n.lesson("Lesson 7 — Designing an Arithmetic Unit: the X/Y/Z Method", "Slides 12–14 (ALU Design) + method used by every TF design question")
n.h2("1. The Slide Design Example: Adder/Subtractor (sl. 12–14)")
n.p("Design: one selection variable s; s = 0 → F = A + B; s = 1 → F = A − B by taking the 2's complement of B.")
n.table(["s", "A_{i}", "B_{i}", "X_{i}", "Y_{i}"], [
    ["0", "0", "0", "0", "0"], ["0", "0", "1", "0", "1"], ["0", "1", "0", "1", "0"], ["0", "1", "1", "1", "1"],
    ["1", "0", "0", "0", "1"], ["1", "0", "1", "0", "0"], ["1", "1", "0", "1", "1"], ["1", "1", "1", "1", "0"],
], widths_cm=[1.4] * 5)
n.formula(["X_{i} = A_{i}        Y_{i} = B_{i} ⊕ s        C_{in} = s"])
n.figure_from_pdf(ALU, 14, "Figure 7.1 — Truth table, equations and the 4-bit adder/subtractor (Fig. 9-10) (sl. 14)", clip=(0.0, 0.33, 1.0, 1.0), width_cm=13.0)
n.h2("2. Identities You Need (n-bit 2's complement, A' = 1's complement)")
n.table(["Wanted F", "Write it as X + Y + C_{in}", "X", "Y", "C_{in}"], [
    ["A + B", "A + B + 0", "A", "B", "0"], ["A + B + 1", "A + B + 1", "A", "B", "1"],
    ["A − B", "A + B' + 1", "A", "B'", "1"], ["A − B − 1", "A + B' + 0", "A", "B'", "0"],
    ["A", "A + 0 + 0  (or A + 1s + 1)", "A", "0 (1s)", "0 (1)"], ["A + 1", "A + 0 + 1", "A", "0", "1"],
    ["A − 1", "A + 1111 + 0", "A", "1s", "0"], ["B − A", "A' + B + 1", "A'", "B", "1"],
    ["A' (+ ...)", "A' + Y + C", "A'", "as needed", "as needed"], ["−A − B − 2", "A' + B'  (−A = A' + 1, −B = B' + 1)", "A'", "B'", "0"],
    ["B + A' (add 1's comp. of A to B)", "A' + B + 0", "A'", "B", "0"],
], widths_cm=[4.4, 5.6, 1.9, 2.5, 2.8], font_size=9)
n.h3("Logic functions from the adder (all carries forced to 0, so F_{i} = X_{i} ⊕ Y_{i})")
n.table(["Wanted F_{i}", "X_{i}", "Y_{i}", "Check"], [
    ["A (transfer)", "A", "0", "A ⊕ 0 = A"], ["A' (NOT)", "A", "1", "A ⊕ 1 = A'"],
    ["A ⊕ B (XOR)", "A", "B", "—"], ["A ⊙ B (XNOR)", "A", "B'", "A ⊕ B' = (A ⊕ B)'"],
    ["A + B (OR)", "A + B", "0", "OR the B bit into X"], ["AB (AND)", "A + B'", "B'", "B = 0 → 1 ⊕ 1 = 0; B = 1 → A ⊕ 0 = A"],
    ["AB'", "A + B", "B", "B = 1 → 1 ⊕ 1 = 0; B = 0 → A"], ["(AB)' (NAND)", "A' + B'", "0", "De Morgan"],
    ["A + B via A' (OR)", "A'B'", "1", "(A'B')' = A + B"],
], widths_cm=[3.6, 2.6, 1.6, 9.4])
n.callout("memorize", "Carry masking: the carry into every stage is Z_{i} = s_{2}'C_{i} (mode bit = 0 for arithmetic). In logic mode s_{2} = 1 kills all carries, "
          "so each full adder becomes an XOR gate: F_{i} = X_{i} ⊕ Y_{i}. The input carry C_{1} is a function of the selection lines only.")
n.h2("3. The Recipe (use it for every TF design)")
n.numbered([
    "For every arithmetic row write F as X + Y + C_{in}; choose X ∈ {A, A'}, Y ∈ {0, B, B', 1s}. Where two choices exist (transfer A), pick the one that makes the equations simpler.",
    "For every logic row choose X_{i}, Y_{i} from the logic table so that X_{i} ⊕ Y_{i} is the wanted function. Try to reuse the Y column of the arithmetic rows.",
    "Make the design table: selection bits → X_{i}, Y_{i}, C_{in}. Treat unused selection codes and the 'x' bits as don't-cares.",
    "Read off the equations (Karnaugh map or inspection on B_{i} and the s bits). Look for XOR forms such as B_{i} ⊕ s_{0}.",
    "Write Z_{i} = s_{mode}' C_{i} and C_{1} = (expression of the s bits). Draw one typical stage: X-logic, Y-logic, AND gate for Z_{i}, full adder.",
    "Check two rows by substitution (one arithmetic, one logic) in the script.",
])
n.h2("4. ★ Worked TF Designs (all verified by simulation)")
# ---- 2023-24 5(b)
n.h3("A. 2023-24 5(b) (15 marks)")
n.p("S2 S1 S0: 000 A − B − 1 · 001 A + B + 1 · 010 transfer A · 011 decrement A · 10x A OR B · 11x A'.")
n.table(["S2 S1 S0", "Function", "X_{i}", "Y_{i}", "C_{in}"], [
    ["000", "A − B − 1 = A + B'", "A", "B'", "0"], ["001", "A + B + 1", "A", "B", "1"],
    ["010", "Transfer A = A + 1s + 1", "A", "1", "1"], ["011", "A − 1 = A + 1s", "A", "1", "0"],
    ["10x", "A OR B", "A + B", "0", "— (carries 0)"], ["11x", "A'", "A", "1", "— (carries 0)"],
], widths_cm=[2.2, 5.6, 2.4, 2.0, 5.0])
n.p("Arithmetic Y: S1 = 0 → B' (S0 = 0) or B (S0 = 1), i.e. B_{i} ⊙ S0; S1 = 1 → 1. Choosing 'A + 1s + 1' for transfer A makes the S1 = 1 rows both Y = 1.")
n.formula(["X_{i} = A_{i} + S2·S1'·B_{i}",
           "Y_{i} = S1 + S2'·(B_{i} ⊙ S0)",
           "C_{in} = S2'·(S1 ⊕ S0)        Z_{i} = S2'·C_{i}"])
n.p("Check: 011 → Y = 1, C_{in} = 0 → A + 1111 = A − 1 ✓. 11x → X = A, Y = 1, carries 0 → F = A ⊕ 1 = A' ✓.")
# ---- 2022-23 11(d)
n.h3("B. 2022-23 11(d) (10 marks)")
n.p("S2 S1 S0: 000 −A − B − 2 · 001 add 1's complement of A to B · 010 A + B · 011 A − B · 10x A AND B · 11x A XOR B.")
n.table(["S2 S1 S0", "Function", "X_{i}", "Y_{i}", "C_{in}"], [
    ["000", "−A − B − 2 = A' + B'", "A'", "B'", "0"], ["001", "B + A'", "A'", "B", "0"],
    ["010", "A + B", "A", "B", "0"], ["011", "A − B = A + B' + 1", "A", "B'", "1"],
    ["10x", "A AND B", "A + B'", "B'", "—"], ["11x", "A XOR B", "A", "B", "—"],
], widths_cm=[2.2, 5.6, 2.4, 2.0, 5.0])
n.formula(["X_{i} = (A_{i} ⊕ S2'S1') + S2·S1'·B_{i}'",
           "Y_{i} = B_{i} ⊙ (S1 ⊕ S2'S0)",
           "C_{in} = S2'·S1·S0        Z_{i} = S2'·C_{i}"])
n.p("Why: arithmetic X is A' exactly when S1 = 0 (A ⊕ S1'); Y is B when S1 ⊕ S0 = 1, else B'. In logic mode S0 is a don't-care, so the term S2'S0 removes it: Y = B (S1 = 1) or B' (S1 = 0) as required.")
# ---- 2022-23 305 5(b)
n.h3("C. 2022-23 (CSE 305) 5(b) — parallel SUBTRACTORS only (14 marks)")
n.p("A full subtractor gives D_{i} = X_{i} ⊕ Y_{i} ⊕ Z_{i} and borrow B_{i+1} = X_{i}'Y_{i} + X_{i}'Z_{i} + Y_{i}Z_{i}; the unit computes **F = X − Y − B_{in}**. "
    "So rewrite every operation as X − Y − borrow, using −B' = B + 1 (because B' = −B − 1).")
n.table(["S2 S1 S0", "Function", "As X − Y − B_{in}", "X_{i}", "Y_{i}", "B_{in}"], [
    ["000", "A − B", "A − B − 0", "A", "B", "0"], ["001", "A + B", "A − B' − 1 = A + B + 1 − 1", "A", "B'", "1"],
    ["010", "−A − B − 2", "A' − B − 1 = (−A − 1) − B − 1", "A'", "B", "1"], ["011", "B − A", "A' − B' = (−A − 1) − (−B − 1)", "A'", "B'", "0"],
    ["100", "A XOR B", "borrows 0: D = X ⊕ Y", "A", "B", "—"], ["110", "A AND B", "borrows 0", "A + B'", "B'", "—"],
], widths_cm=[2.0, 2.5, 6.0, 1.8, 1.6, 1.6], font_size=9)
n.formula(["X_{i} = (A_{i} ⊕ S2'S1) + S2·S1·B_{i}'",
           "Y_{i} = B_{i} ⊕ (S0 + S2·S1)",
           "B_{in} = S2'·(S1 ⊕ S0)        Z_{i} (borrow into stage i) = S2'·B_{i}"])
n.callout("note", "With borrows forced to 0 a subtractor stage is also just X ⊕ Y, so the logic part is designed exactly as for adders. Codes 101 and 111 are unused (don't-cares).")
# ---- 2020-21 10(b)
n.h3("D. 2020-21 10(b) — four selection lines, least gates (18 marks)")
n.table(["S3 S2 S1 S0", "Function", "X_{i}", "Y_{i}", "C_{in}"], [
    ["0000", "A", "A", "0", "0"], ["0001", "A − 1", "A", "1", "0"], ["0010", "A + B + 1", "A", "B", "1"], ["0011", "A + B", "A", "B", "0"],
    ["0100", "A − B", "A", "B'", "1"], ["0101", "A − B − 1", "A", "B'", "0"], ["0110", "A + 1", "A", "0", "1"], ["0111", "A (as A + 0 + 0)", "A", "0", "0"],
    ["100x", "A'", "A", "1", "—"], ["101x", "AB'", "A + B", "B", "—"], ["110x", "A ⊙ B (XNOR)", "A", "B'", "—"], ["111x", "A + B (OR)", "A + B", "0", "—"],
], widths_cm=[2.4, 4.4, 2.4, 2.0, 2.0])
n.p("Y depends only on S2 S1 (and S0 when S2S1 = 00): 00 → S0 in arithmetic, 1 in logic → (S0 + S3); 01 → B; 10 → B'; 11 → 0. X needs B only in rows 101x and 111x (S3 = 1, S1 = 1).")
n.formula(["X_{i} = A_{i} + S3·S1·B_{i}",
           "Y_{i} = S2'S1'(S0 + S3) + S2'S1·B_{i} + S2S1'·B_{i}'",
           "C_{in} = S3'·S0'·(S2 + S1)        Z_{i} = S3'·C_{i}"])
# ---- 2019-20 2(a)
n.h3("E. 2019-20 2(a) — arithmetic on A' (20 marks)")
n.table(["S3 S2 S1 S0", "Function", "X_{i}", "Y_{i}", "C_{in}"], [
    ["0000 / 0001", "A' / A' + 1", "A'", "0", "S0"], ["0010 / 0011", "A' + B / A' + B + 1", "A'", "B", "S0"],
    ["0100 / 0101", "A' − B − 1 / A' − B", "A'", "B'", "S0"], ["0110 / 0111", "A' − 1 / A'", "A'", "1", "S0"],
    ["100x", "(AB)' NAND", "A' + B'", "0", "—"], ["101x", "A ⊙ B XNOR", "A'", "B", "—"],
    ["110x", "A ⊕ B XOR", "A'", "B'", "—"], ["111x", "A + B OR", "A'B'", "1", "—"],
], widths_cm=[2.6, 4.4, 2.2, 1.8, 2.0])
n.p("This is Table 9-1 with A' in place of A and (S2, S1) in place of (s1, s0). The logic rows were chosen so that Y keeps the same pattern 0, B, B', 1 — so Y needs no S3 at all.")
n.formula(["Y_{i} = S1·B_{i} + S2·B_{i}'          (same for both modes)",
           "X_{i} = A_{i}'·(S3S2S1B_{i})' + S3·S2'·S1'·B_{i}'",
           "C_{in} = S3'·S0        Z_{i} = S3'·C_{i}"])
n.p("Check NAND (100x): X = A' + B', Y = 0 → F = A' + B' = (AB)' ✓. OR (111x): X = A'B', Y = 1 → F = (A'B')' = A + B ✓.")
n.h2("5. Drawing One Typical Stage")
n.code(["            S-lines ─────────┬─────────────────┬──────────────┐",
        "                             ▼                 ▼              ▼",
        "   A_i ──────────►  ┌──────────────┐   ┌──────────────┐   ┌─────┐",
        "   B_i ──────────►  │ X-logic      │   │ Y-logic      │   │ AND │◄── C_i",
        "                    │ (gates of    │   │ (gates of    │   └──┬──┘   (S_mode' input)",
        "                    │  X_i eqn)    │   │  Y_i eqn)    │      │ Z_i",
        "                    └──────┬───────┘   └──────┬───────┘      │",
        "                           X_i                Y_i            │",
        "                           ▼                  ▼              ▼",
        "                        ┌──────────── Full adder ────────────────┐",
        "                        └──────────┬───────────────────┬─────────┘",
        "                                  F_i                C_{i+1} → next stage",
        "   Stage 1 only: C_1 = C_in expression of the S-lines"])
n.exam_approach([
    "Write the design table first (S bits | function | X | Y | C_{in}) — most marks are for it.",
    "Reuse identities: −A = A' + 1, A − B = A + B' + 1, −A − B − 2 = A' + B', B − A = A' + B + 1.",
    "Choose logic-row X, Y so that Y keeps the arithmetic pattern — fewer gates.",
    "Give X_{i}, Y_{i}, C_{in}, Z_{i}; draw one stage; verify one row.",
    "For subtractor-only designs use −B' = B + 1 and the borrow-in as C_{in}.",
])
n.practice("Lesson 7", "(a) Actual — 2023-24 5(b). (b) Actual — 2022-23 11(d). (c) Actual — 2022-23 (CSE 305) 5(b). (d) Actual — 2020-21 10(b). (e) Actual — 2019-20 2(a).", [
    "(a)–(e) The five specifications are exactly those of §4 A–E. Cover the solutions and redo each one: design table → equations → one stage.",
])
n.solution()
n.answer("(a)–(e)", "§4 A–E above. Each set of equations was simulated for all 4-bit A, B and every selection code — all outputs matched the required functions.")

# ================================================================== LESSON 8
n.lesson("Lesson 8 — Logic Circuit and the Complete ALU", "Slides 15–20 (ALU Design)")
n.h2("1. Logic Circuit With a Multiplexer (sl. 15)")
n.p("The direct design: compute OR, XOR, AND and NOT of each bit pair and pick one with a 4-to-1 mux controlled by s1 s0.")
n.table(["s1 s0", "Output", "Operation"], [["00", "F_{i} = A_{i} + B_{i}", "OR"], ["01", "F_{i} = A_{i} ⊕ B_{i}", "XOR"], ["10", "F_{i} = A_{i}B_{i}", "AND"], ["11", "F_{i} = A_{i}'", "NOT"]], widths_cm=[2.0, 4.5, 3.0])
n.figure_from_pdf(ALU, 15, "Figure 8.1 — One stage of the logic circuit (Fig. 9-11) (sl. 15)", clip=(0.05, 0.12, 0.92, 1.0), width_cm=11.5)
n.h2("2. Combining Logic and Arithmetic (sl. 16)")
n.p("One arithmetic stage and one logic stage, followed by a 2-to-1 mux controlled by the mode bit s2 (0 = arithmetic, 1 = logic).")
n.figure_from_pdf(ALU, 16, "Figure 8.2 — Combining logic and arithmetic circuits (Fig. 9-12) (sl. 16)", clip=(0.1, 0.13, 0.95, 1.0), width_cm=11.0)
n.h2("3. The More Efficient Design (sl. 17–20) ★")
n.numbered([
    "Design the arithmetic section independently of the logic section.",
    "Find which logic operations the arithmetic circuit already produces when all input carries are 0.",
    "Modify the arithmetic circuit to obtain the required logic operations.",
])
n.p("With carries 0 each full adder gives F_{i} = X_{i} ⊕ Y_{i}. With X_{i} = A_{i} and the arithmetic Y_{i} (0, B, B', 1) that already produces (Table 9-3):")
n.table(["s2 s1 s0", "X_{i}", "Y_{i}", "C_{i}", "F_{i} = X_{i} ⊕ Y_{i}", "Operation", "Required"], [
    ["1 0 0", "A_{i}", "0", "0", "A_{i}", "Transfer A", "OR"], ["1 0 1", "A_{i}", "B_{i}", "0", "A_{i} ⊕ B_{i}", "XOR", "XOR"],
    ["1 1 0", "A_{i}", "B_{i}'", "0", "A_{i} ⊙ B_{i}", "Equivalence", "AND"], ["1 1 1", "A_{i}", "1", "0", "A_{i}'", "NOT", "NOT"],
], widths_cm=[1.9, 1.6, 1.4, 1.2, 3.4, 3.0, 2.2])
n.p("XOR and NOT are free. For OR, OR B_{i} into X_{i} in row 100 (X = A + B, Y = 0). For AND, OR B_{i}' into X_{i} in row 110 (X = A + B', Y = B' gives (A + B') ⊕ B' = AB). Carries are masked by s2:")
n.formula(["X_{i} = A_{i} + s2·s1'·s0'·B_{i} + s2·s1·s0'·B_{i}'",
           "Y_{i} = s0·B_{i} + s1·B_{i}'",
           "Z_{i} = s2'·C_{i}"])
n.figure_from_pdf(ALU, 19, "Figure 8.3 — Logic diagram of the ALU (Fig. 9-13), first two stages (sl. 19)", clip=(0.12, 0.1, 0.72, 1.0), width_cm=11.5)
n.table(["s2 s1 s0 C_{in}", "Output", "Function"], [
    ["0 0 0 0", "F = A", "Transfer A"], ["0 0 0 1", "F = A + 1", "Increment A"], ["0 0 1 0", "F = A + B", "Addition"], ["0 0 1 1", "F = A + B + 1", "Add with carry"],
    ["0 1 0 0", "F = A − B − 1", "Subtract with borrow"], ["0 1 0 1", "F = A − B", "Subtraction"], ["0 1 1 0", "F = A − 1", "Decrement A"], ["0 1 1 1", "F = A", "Transfer A"],
    ["1 0 0 X", "F = A ∨ B", "OR"], ["1 0 1 X", "F = A ⊕ B", "XOR"], ["1 1 0 X", "F = A ∧ B", "AND"], ["1 1 1 X", "F = A'", "Complement A"],
], widths_cm=[3.4, 4.0, 5.0])
n.p("Table 9-4 (sl. 20) — the function table of the ALU of Fig. 9-13 (checked by simulation).")
n.exam_approach([
    "'Design an ALU … draw one typical stage': use the efficient method — arithmetic first, then get logic from X ⊕ Y with carries masked.",
    "Without a C_{in} line in the question, C_{in} must come from the selection bits (here 0 for every arithmetic row, or a product term).",
    "Draw: X-logic gates, Y-logic gates, AND gate (s2', C_{i}) → Z_{i}, full adder, F_{i}, C_{i+1}.",
])
n.practice("Lesson 8", "(a) Actual — 2018-19 5(d). (b) Actual — 2017-18 6(a).", [
    "(a) 4-bit ALU, S2 S1 S0: 000 Addition, 001 Transfer A, 010 Add 1's complement of B to A, 011 Increment A, 100 XOR, 101 NOT, 110 AND, 111 OR. Draw one typical stage. (10)",
    "(b) 4-bit ALU, S2 S1 S0: 000 Addition, 001 Transfer A, 010 Decrement A, 011 Add 1's complement of B to A, 100 XOR, 101 AND, 110 NOT, 111 OR. Draw one typical stage. (25)",
])
n.solution()
n.answer("(a)", "")
n.table(["S2 S1 S0", "Function", "X_{i}", "Y_{i}", "C_{in}"], [
    ["000", "A + B", "A", "B", "0"], ["001", "Transfer A", "A", "0", "0"], ["010", "A + B'", "A", "B'", "0"], ["011", "A + 1", "A", "0", "1"],
    ["100", "XOR", "A", "B", "—"], ["101", "NOT", "A", "1", "—"], ["110", "AND", "A + B'", "B'", "—"], ["111", "OR", "A + B", "0", "—"],
], widths_cm=[2.2, 3.8, 2.2, 2.0, 2.0])
n.formula(["X_{i} = A_{i} + S2·S1·(S0 ⊙ B_{i})",
           "Y_{i} = S0'·(B_{i} ⊕ S1) + S2·S1'·S0",
           "C_{in} = S2'·S1·S0        Z_{i} = S2'·C_{i}"])
n.p("S0 ⊙ B_{i} gives B_{i}' for 110 (AND) and B_{i} for 111 (OR). Y is B, 0, B', 0 in arithmetic; logic needs B, 1, B', 0 — only row 101 differs, hence the extra term S2S1'S0.")
n.answer("(b)", "No input carry is listed, so C_{in} = 0 in every arithmetic row (A + B, A, A − 1 = A + 1s, A + B').")
n.table(["S2 S1 S0", "Function", "X_{i}", "Y_{i}"], [
    ["000", "A + B", "A", "B"], ["001", "Transfer A", "A", "0"], ["010", "Decrement A", "A", "1"], ["011", "A + B'", "A", "B'"],
    ["100", "XOR", "A", "B"], ["101", "AND", "A + B'", "B'"], ["110", "NOT", "A", "1"], ["111", "OR", "A + B", "0"],
], widths_cm=[2.2, 3.8, 2.2, 2.0])
n.formula(["X_{i} = A_{i} + S2·S0·(S1 ⊙ B_{i})",
           "Y_{i} = S1'S0'·B_{i} + S1·S0' + S0·B_{i}'·(S2 ⊕ S1)",
           "C_{in} = 0        Z_{i} = S2'·C_{i}"])
n.p("Y rows 00 and 10 are the same in both modes (B and 1); rows 01 and 11 swap between 0 and B' — the XOR (S2 ⊕ S1) selects B' for 011 and 101 only. One typical stage: Fig. in Lesson 7 §5 with these X/Y gates.")

# ================================================================== LESSON 9
n.lesson("Lesson 9 — Status Register, Overflow and Comparator Circuits", "Slides 21–22 (ALU Design)")
n.h2("1. The Four Status Bits (sl. 21–22)")
n.table(["Bit", "Set when", "Hardware (8-bit ALU)"], [
    ["C (carry)", "Output carry of the ALU is 1", "C = C_{9} = C_{out}"],
    ["S (sign)", "Most significant bit of the result is 1", "S = F_{8}"],
    ["Z (zero)", "Result is all 0s", "Z = (F_{1} + F_{2} + … + F_{8})' — an 8-input NOR"],
    ["V (overflow)", "C_{8} ⊕ C_{9} = 1: signed result > 127 or < −128", "XOR of the carry into and out of the sign stage"],
], widths_cm=[2.6, 7.4, 7.2])
n.figure_from_pdf(ALU, 22, "Figure 9.1 — Setting the bits of the status register (Fig. 9-14) (sl. 22)", clip=(0.18, 0.17, 0.92, 0.98), width_cm=12.0)
n.h2("2. Why V = XOR of the Last Two Carries ★")
n.p("Let C_{n} be the carry into the sign stage and C_{n+1} the carry out of it (C_{8}, C_{9} for 8 bits).")
n.table(["Operand signs", "Carry out C_{n+1}", "Sign of result", "Overflow?"], [
    ["+ and + (MSBs 0, 0)", "always 0", "= C_{n}", "yes exactly when C_{n} = 1 (result looks negative)"],
    ["− and − (MSBs 1, 1)", "always 1", "= C_{n}", "yes exactly when C_{n} = 0 (result looks positive)"],
    ["+ and − (MSBs 0, 1)", "= C_{n}", "—", "never (|sum| ≤ larger operand)"],
], widths_cm=[3.8, 3.4, 3.0, 7.0])
n.p("In both overflow cases the two carries differ, and whenever they are equal there is no overflow. Hence V = C_{n} ⊕ C_{n+1}. "
    "Examples (4 bits): 0111 + 0001 = 1000 — carry into MSB 1, out 0 → V = 1 (+7 + 1 = +8 out of range). 1000 + 1111 = (1)0111 — into 0, out 1 → V = 1 (−8 − 1 = −9).")
n.h2("3. Comparing A and B With the Status Bits of A − B")
n.p("The status module of the TF questions computes A − B = A + B' + 1 and outputs V, Z, S, C.")
n.table(["Relation", "Unsigned A, B", "Signed (2's complement) A, B"], [
    ["A = B", "Z = 1", "Z = 1"], ["A ≠ B", "Z = 0", "Z = 0"],
    ["A < B", "C = 0 (a borrow occurred)", "S ⊕ V = 1"], ["A ≥ B", "C = 1", "S ⊕ V = 0"],
    ["A > B", "C·Z' = 1", "(S ⊕ V)'·Z' = 1"], ["A ≤ B", "C' + Z = 1", "(S ⊕ V) + Z = 1"],
], widths_cm=[2.8, 6.2, 8.2])
n.callout("trap", "For signed numbers S alone is wrong: if A − B overflows the sign bit is flipped. That is why the test is S ⊕ V. State whether you treat A, B as signed or unsigned.")
n.exam_approach([
    "Decide signed or unsigned (TF status-module questions mean 2's complement unless they say otherwise; mention both if unsure).",
    "Feed A and B to a module; take Z for equality and S ⊕ V (or C) for order.",
    "Tests against 0: tie the second input to 0000 and use Z.",
    "Combine with AND/OR/NOT exactly as the C condition says; draw modules as boxes with V Z S C outputs.",
])
n.practice("Lesson 9", "(a) Actual — 2022-23 11(a). (b) Actual — 2020-21 12(d). (c) Actual — 2019-20 2(b).", [
    "(a) Why is the overflow bit (V) computed by XOR-ing the last two carry bits in binary arithmetic operations? (7)",
    "(b) A module takes two 4-bit inputs A and B and outputs only V, Z, S, C for A − B. Draw the complete circuit that decides whether A > B, A = B or A < B. (8)",
    "(c) Implement F = 1 if ((A >= B && C != D) || X == 0) else 0 with basic gates and status-generator modules (4-bit A, B, C, D, X). (15)",
])
n.solution()
n.answer("(a)", "§2: list the three sign cases, show that overflow happens exactly when the carry into the sign position differs from the carry out of it, give the two 4-bit examples, conclude V = C_{n} ⊕ C_{n+1} (C_{8} ⊕ C_{9} on slide 21).")
n.answer("(b)", "Signed (2's complement) A, B:")
n.code(["        A ─┐  ┌──────────┐",
        "           ├─►│  STATUS  │── V ──┐",
        "        B ─┘  │ (A − B)  │── S ──┴─[XOR]── L ─────────────► A < B  = S ⊕ V",
        "              │          │── Z ───────────────────────────► A = B  = Z",
        "              └──────────┘── C (unused)",
        "        L ──[NOT]──┐",
        "        Z ──[NOT]──┴─[AND]────────────────────────────────► A > B  = (S ⊕ V)'·Z'"])
n.p("Unsigned version: A < B = C', A = B = Z, A > B = C·Z'. (Gates: one XOR, two NOT, one AND for the signed version.)")
n.answer("(c)", "Three modules: M1(A, B), M2(C, D), M3(X, 0000).")
n.code(["  M1: A − B →  A >= B   = (S1 ⊕ V1)'        (signed; unsigned: C1)",
        "  M2: C − D →  C != D   = Z2'",
        "  M3: X − 0 →  X == 0   = Z3",
        "",
        "  S1 ──┐",
        "  V1 ──┴─[XNOR]──┐",
        "  Z2 ──[NOT]─────┴─[AND]──┐",
        "  Z3 ─────────────────────┴─[OR]──► F = (S1 ⊙ V1)·Z2' + Z3"])
n.p("Gate count: one XNOR, one NOT, one AND, one OR plus three modules. (If the numbers are unsigned replace the XNOR by C1.)")

n.quick_notes("Quick Notes — ALU Design", "Revision points for Lessons 5–9.", [
    ("L5 · Adders", [
        "HA: S = x ⊕ y, C = xy. FA: S = x ⊕ y ⊕ z, C = xy + xz + yz. Parallel adder = FAs in cascade.",
        "ALU inputs: A, B, s2 (mode), s1 s0 (function), C_{in}; outputs F, C_{out}.",
    ]),
    ("L6 · Arithmetic circuit", [
        "Y = 0, B, B', 1s (Y_{i} = B_{i}s0 + B_{i}'s1); with C_{in} = 0/1 → 8 functions (Table 9-1).",
        "C_{out} = 1: A + B ≥ 2^{n}; A + 1 when A = all 1s; A − B − 1 when A > B; A − B when A ≥ B; A − 1 when A ≠ 0.",
    ]),
    ("L7 · X/Y/Z design", [
        "A − B = A + B' + 1; A − B − 1 = A + B'; A − 1 = A + 1s; −A − B − 2 = A' + B'; B − A = A' + B + 1.",
        "Logic (carries 0): XOR (A, B); XNOR (A, B'); NOT (A, 1); OR (A + B, 0); AND (A + B', B'); AB' (A + B, B); NAND (A' + B', 0).",
        "Z_{i} = s_{mode}'C_{i}; C_{1} from S bits. Subtractors: F = X − Y − B_{in}, use −B' = B + 1.",
    ]),
    ("L8 · Complete ALU", [
        "Efficient design: arithmetic first; logic from X ⊕ Y; X_{i} = A_{i} + s2s1's0'B_{i} + s2s1s0'B_{i}', Y_{i} = s0B_{i} + s1B_{i}', Z_{i} = s2'C_{i}.",
        "Table 9-4: 8 arithmetic (s2 = 0, Cin) + OR, XOR, AND, complement.",
    ]),
    ("L9 · Status bits", [
        "C = carry out; S = MSB; Z = NOR of all F bits; V = C_{n} ⊕ C_{n+1}.",
        "After A − B: equal Z; signed A < B = S ⊕ V; unsigned A < B = C'.",
    ]),
], diagrams=[
    (ALU, 14, "Adder/subtractor (Fig. 9-10) — same as Fig. 7.1", (0.0, 0.33, 1.0, 1.0), 12.0),
    (ALU, 22, "Status register (Fig. 9-14) — same as Fig. 9.1", (0.18, 0.17, 0.92, 0.98), 11.0),
])
print(n.save())
