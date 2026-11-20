"""Solutions, part 1 (Ch1 performance + ALU).  Item syntax:
  "text"          paragraph (**bold**, *italic*, _{sub}, ^{sup})
  "| code"        monospace line (consecutive lines form one block)
  "A: text"       highlighted answer
  ("T", [hdr], [[row]...], [col widths in %])   table
"""
S = {}

# ============================================================ CH1
S[("2023-24", "CSE 209", "6(a)")] = dict(
    q="Our favourite program runs in 10 s on computer A (4 GHz clock). The designer wants computer B to run it in 6 s; a substantial clock-rate increase is possible but makes B need 1.2 times as many clock cycles as A. What clock rate should we tell the designer to target?",
    s=["Cycles_{A} = CPU time × clock rate = 10 s × 4×10^{9} = 40×10^{9}.",
       "Cycles_{B} = 1.2 × 40×10^{9} = 48×10^{9}.",
       "Clock rate_{B} = Cycles_{B} / CPU time_{B} = 48×10^{9} / 6 s = 8×10^{9} Hz.",
       "A: Target clock rate of B = **8 GHz**."])
S[("2022-23", "CSE 305", "6(d)")] = dict(
    q="P1 (2.7 GHz, CPI of classes A,B,C,D = 2,1,3,2) and P2 (3.2 GHz, CPI 2,3,2,3) implement the same ISA. A program of 1.2×10^{6} instructions has 20 % class A, 25 % B, 40 % C, 15 % D. (i) Clock cycles on each. (ii) Which is faster and by how much? (iii) If 40 % of the code is improved, what is the maximum possible improvement factor?",
    s=["Instructions: A 240 000, B 300 000, C 480 000, D 180 000.",
       "| P1 cycles = 240k×2 + 300k×1 + 480k×3 + 180k×2 = 2.58×10^6   T1 = 2.58e6 / 2.7e9 = 0.956 ms",
       "| P2 cycles = 240k×2 + 300k×3 + 480k×2 + 180k×3 = 2.88×10^6   T2 = 2.88e6 / 3.2e9 = 0.900 ms",
       "A: (i) 2.58×10^{6} and 2.88×10^{6} cycles. (ii) **P2 is faster** by 0.956/0.900 = 1.06×.",
       "(iii) Amdahl with an infinitely fast improved part: S_{max} = 1/(1 − 0.4) = **1.67**."])
S[("2022-23", "CSE 305", "7(a)")] = dict(
    q="Define response time and throughput. Are these two terms synonymous?",
    s=["**Response time** (execution time, latency) is the time to complete one task, from start to finish. **Throughput** is the total work done per unit time (tasks or transactions per hour).",
       "A: **Not synonymous.** A faster processor lowers response time and so also raises throughput; extra processors raise throughput (more tasks at once) but leave the response time of a single task unchanged."])
S[("2021-22", "CSE 305", "5(b)")] = dict(
    q="2 % of a program's runtime is not parallelizable. It runs on 24 cores of the same speed with no extra overhead. (i) What is the parallel speedup for 24 cores? (ii) Is it possible to make the program 60 times faster? If yes, how; if not, why?",
    s=["Amdahl: Speedup = 1 / ((1 − f) + f/p), f = 0.98, p = 24.",
       "| S = 1 / (0.02 + 0.98/24) = 1 / (0.02 + 0.04083) = 16.44",
       "A: (i) **16.44**.",
       "(ii) The limit is 1/0.02 = 50 < 60, so **no** — not by adding cores. It becomes possible only by making the serial part smaller (< 1/60 ≈ 1.67 % of the time, by redesigning the algorithm) or by running the serial part on a faster core."])
S[("2021-22", "CSE 305", "7(b)")] = dict(
    q="Your research partner says FLOPS is a misleading metric for the general performance of a processor but could still be useful for a specific part or type of processor. Do you agree? Explain in detail.",
    s=["**Agree.** FLOPS counts only floating-point operations per second:",
       "• Integer, memory and branch work is not measured at all, so programs dominated by it look slow although they are not.",
       "• Different ISAs have different FP operations (fused multiply-add counts as one or two), so FLOPS of different machines are not comparable.",
       "• Like MIPS, it varies from program to program on one machine; execution time of real programs is the only general measure.",
       "A: For a **specific part** — the FP unit, a GPU, a vector unit — or for FP-dominated work (matrix multiply, simulation, deep learning) FLOPS directly measures how fast that part does its job, so it is a useful specialised metric."])
S[("2021-22", "CSE 305", "8(a)")] = dict(
    q="200 000 instructions: 25 % class A, 60 % B, 15 % C. P1 2.7 GHz (CPI 3,3,2), P2 3.5 GHz (CPI 2,4,1). (i) Total clock cycles on both. (ii) Execution times; which is faster? (iii) By how much must the CPI of class C improve so the program runs 2× faster on the better implementation?",
    s=["A = 50 000, B = 120 000, C = 30 000 instructions.",
       "| P1 = 50k×3 + 120k×3 + 30k×2 = 570 000 cycles → T = 570 000 / 2.7 GHz = 211.1 µs",
       "| P2 = 50k×2 + 120k×4 + 30k×1 = 610 000 cycles → T = 610 000 / 3.5 GHz = 174.3 µs",
       "A: P2 is faster (211.1/174.3 = 1.21×).",
       "(iii) 2× in P2 → 305 000 cycles. Classes A and B alone need 100 000 + 480 000 = 580 000 > 305 000, so even CPI_{C} = 0 is not enough: **impossible**."])
S[("2020-21", "CSE 305", "10(a)")] = dict(
    q="Briefly explain the eight great ideas in computer architecture.",
    s=[("T", ["Idea", "Meaning", "Example"], [
        ["Design for Moore's law", "design for the transistor budget available when the product ships", "plan for 2× transistors in 2 years"],
        ["Use abstraction", "hide lower-level detail behind a simpler model", "ISA hides implementation"],
        ["Make the common case fast", "speed up the frequent case", "immediates, PC-relative branches"],
        ["Performance via parallelism", "do several operations at once", "multicore, 31 adders in a multiplier"],
        ["Performance via pipelining", "overlap steps of successive operations", "5-stage MIPS pipeline"],
        ["Performance via prediction", "guess, start, recover if wrong", "branch prediction, prefetching"],
        ["Hierarchy of memories", "fast/small/expensive on top, slow/large/cheap below", "registers → cache → DRAM → disk"],
        ["Dependability via redundancy", "spare components take over on failure", "RAID, ECC"]], [22, 46, 32])])
S[("2020-21", "CSE 305", "12(a)")] = dict(
    q="Instruction types with CPI: multiplication 3, addition 1, subtraction 2, division 4. Program A has 2, 1, 4, 2 instructions; program B has 3, 2, 3, 2. Which program has the higher average clock cycles per instruction?",
    s=["CPI = Σ IC_{i}·CPI_{i} / Σ IC_{i}.",
       "| A: cycles = 2×3 + 1×1 + 4×2 + 2×4 = 23, IC = 9  → CPI = 2.56",
       "| B: cycles = 3×3 + 2×1 + 3×2 + 2×4 = 25, IC = 10 → CPI = 2.50",
       "A: **Program A** has the higher average CPI (2.56 vs 2.50); B still needs more total cycles because it executes more instructions."])
S[("2019-20", "CSE 305", "1(a)")] = dict(
    q="Program 1 is run on systems A (2 GHz) and B (2.5 GHz). Logs of A: Mul 4, Mul 4, Div 5, Div 5, Add 2 cycles for Program 1 (other entries belong to Programs 2–3 or are OS I/O overhead); logs of B: Mul 5, Mul 5, Div 6, Div 6, Add 3 for Program 1. Compare their performance on the execution time of Program 1.",
    s=["Only Program 1's own operations count (CPU time); the other programs' lines and the OS I/O overhead are ignored.",
       "| A: cycles = 4+4+5+5+2 = 20 → T_A = 20 / 2 GHz   = 10 ns",
       "| B: cycles = 5+5+6+6+3 = 25 → T_B = 25 / 2.5 GHz = 10 ns",
       "A: Performance_{A}/Performance_{B} = T_{B}/T_{A} = 1 — the two systems perform **equally** on Program 1. B's faster clock is cancelled by its extra cycles."])
S[("2019-20", "CSE 305", "1(b)")] = dict(
    q="What is the importance of Moore's law? \"To increase the overall performance of a computer by x, identify the most important aspect and improve its performance by x.\" Agree or disagree? Justify with mathematics.",
    s=["**Moore's law**: transistor count doubles about every 18–24 months. It makes hardware cheaper and faster and is why designers must design for the technology available when the product ships.",
       "**Disagree** (Amdahl's law). If the improved aspect takes fraction f < 1 of the time:",
       "| Speedup = 1 / ((1 − f) + f/x)  < x   for every x > 1",
       "Example: f = 0.8, x = 4 → 1/(0.2 + 0.2) = 2.5, not 4. Even x → ∞ gives only 1/(1 − f) = 5. Overall speedup x is reached only when f = 1.",
       "A: The unimproved part (1 − f) sets a ceiling; improve the **common case** (largest f) but expect less than x."])

# ============================================================ ALU
S[("2023-24", "CSE 209", "5(b)")] = dict(
    q="Design a 4-bit ALU (A, B; selection S2 S1 S0) with parallel adders: 000 F = A − B − 1; 001 F = A + B + 1; 010 transfer A; 011 decrement A; 10x F = A OR B; 11x F = A'. Devise the input equations X_{i}, Y_{i}, Z_{i}.",
    s=[("T", ["S2 S1 S0", "Function", "X_{i}", "Y_{i}", "C_{in}"], [
        ["000", "A − B − 1 = A + B'", "A", "B'", "0"], ["001", "A + B + 1", "A", "B", "1"],
        ["010", "transfer A = A + 1s + 1", "A", "1", "1"], ["011", "A − 1 = A + 1s", "A", "1", "0"],
        ["10x", "A OR B", "A + B", "0", "(carries 0)"], ["11x", "A'", "A", "1", "(carries 0)"]], [14, 34, 18, 14, 20]),
       "In logic mode (S2 = 1) all carries are forced to 0, so F_{i} = X_{i} ⊕ Y_{i}.",
       "| X_i = A_i + S2·S1'·B_i",
       "| Y_i = S1 + S2'·(B_i ⊙ S0)         (B_i ⊙ S0 = B_i' for S0 = 0, B_i for S0 = 1)",
       "| C_in = S2'·(S1 ⊕ S0)              Z_i = S2'·C_i",
       "A: Check: 011 → Y = 1, C_{in} = 0 → A + 1111 = A − 1 ✓; 11x → X = A, Y = 1 → A ⊕ 1 = A' ✓. (All six functions verified by simulation for every A, B.)"])
S[("2022-23", "CSE 209", "11(a)")] = dict(
    q="Why is the overflow bit (V) computed by XOR-ing the last two carry bits in binary arithmetic operations?",
    s=["Let C_{n} be the carry into the sign position and C_{n+1} the carry out of it.",
       ("T", ["Operand signs", "C_{n+1}", "Sign of result", "Overflow when"], [
           ["+ and + (MSBs 0,0)", "always 0", "= C_{n}", "C_{n} = 1 (result looks negative)"],
           ["− and − (MSBs 1,1)", "always 1", "= C_{n}", "C_{n} = 0 (result looks positive)"],
           ["+ and −", "= C_{n}", "—", "never"]], [26, 18, 18, 38]),
       "In both overflow cases the two carries differ; when they are equal there is no overflow.",
       "A: V = C_{n} ⊕ C_{n+1} (C_{8} ⊕ C_{9} for 8 bits). Examples (4 bits): 0111 + 0001 = 1000 — carry in 1, out 0 → V = 1; 1000 + 1111 = (1)0111 — in 0, out 1 → V = 1."])
S[("2022-23", "CSE 209", "11(d)")] = dict(
    q="Design a 4-bit ALU, selection S2 S1 S0: 000 −A − B − 2; 001 add 1's complement of A to B; 010 A + B; 011 A − B; 10x A AND B; 11x A XOR B. Derive X_{i}, Y_{i}, Z_{i}.",
    s=[("T", ["S2 S1 S0", "Function", "X_{i}", "Y_{i}", "C_{in}"], [
        ["000", "−A − B − 2 = A' + B'", "A'", "B'", "0"], ["001", "B + A'", "A'", "B", "0"],
        ["010", "A + B", "A", "B", "0"], ["011", "A − B = A + B' + 1", "A", "B'", "1"],
        ["10x", "A AND B", "A + B'", "B'", "—"], ["11x", "A XOR B", "A", "B", "—"]], [14, 34, 18, 14, 20]),
       "AND from the adder with carries 0: (A + B') ⊕ B' = AB (B = 0 → 1⊕1 = 0; B = 1 → A⊕0 = A).",
       "| X_i = (A_i ⊕ S2'S1') + S2·S1'·B_i'",
       "| Y_i = B_i ⊙ (S1 ⊕ S2'S0)",
       "| C_in = S2'·S1·S0                  Z_i = S2'·C_i",
       "A: Verified by simulation for all 4-bit A, B and every code."])
S[("2022-23", "CSE 305", "5(b)")] = dict(
    q="Design a 4-bit ALU using only parallel SUBTRACTORS and logic gates; S2 S1 S0: 000 A − B; 001 A + B; 010 −A − B − 2; 011 B − A; 100 A XOR B; 110 A AND B.",
    s=["A full-subtractor stage gives D = X ⊕ Y ⊕ Z, borrow = X'Y + X'Z + YZ: the unit computes **F = X − Y − B_{in}**. Use −B' = B + 1.",
       ("T", ["S2 S1 S0", "F", "as X − Y − B_{in}", "X_{i}", "Y_{i}", "B_{in}"], [
           ["000", "A − B", "A − B − 0", "A", "B", "0"], ["001", "A + B", "A − B' − 1", "A", "B'", "1"],
           ["010", "−A − B − 2", "A' − B − 1", "A'", "B", "1"], ["011", "B − A", "A' − B'", "A'", "B'", "0"],
           ["100", "A XOR B", "borrows 0", "A", "B", "—"], ["110", "A AND B", "borrows 0", "A + B'", "B'", "—"]], [13, 17, 25, 15, 15, 15]),
       "| X_i = (A_i ⊕ S2'S1) + S2·S1·B_i'",
       "| Y_i = B_i ⊕ (S0 + S2·S1)",
       "| B_in = S2'·(S1 ⊕ S0)              borrow into stage i: Z_i = S2'·B_i",
       "A: Codes 101 and 111 are unused (don't-cares). Verified by simulation."])
S[("2020-21", "CSE 305", "10(b)")] = dict(
    q="Design a 4-bit ALU with selection S3 S2 S1 S0: 0000 A; 0001 A−1; 0010 A+B+1; 0011 A+B; 0100 A−B; 0101 A−B−1; 0110 A+1; 0111 A; 100x A'; 101x AB'; 110x A ⊙ B; 111x A ∨ B. Derive X_{i}, Y_{i}, Z_{i} with the least number of gates.",
    s=[("T", ["S3 S2 S1 S0", "Function", "X_{i}", "Y_{i}", "C_{in}"], [
        ["0000", "A", "A", "0", "0"], ["0001", "A − 1", "A", "1", "0"], ["0010", "A + B + 1", "A", "B", "1"], ["0011", "A + B", "A", "B", "0"],
        ["0100", "A − B", "A", "B'", "1"], ["0101", "A − B − 1", "A", "B'", "0"], ["0110", "A + 1", "A", "0", "1"], ["0111", "A", "A", "0", "0"],
        ["100x", "A'", "A", "1", "—"], ["101x", "AB'", "A + B", "B", "—"], ["110x", "A ⊙ B", "A", "B'", "—"], ["111x", "A ∨ B", "A + B", "0", "—"]], [16, 28, 18, 14, 14]),
       "| X_i = A_i + S3·S1·B_i",
       "| Y_i = S2'S1'(S0 + S3) + S2'S1·B_i + S2S1'·B_i'",
       "| C_in = S3'·S0'·(S2 + S1)          Z_i = S3'·C_i",
       "A: Verified by simulation for all 4-bit inputs and all 16 codes."])
S[("2020-21", "CSE 305", "12(d)")] = dict(
    q="A module takes two 4-bit inputs and shows only V, Z, S, C of the subtraction (second input from the first). If the first input is A and the second B, draw the complete circuit that determines whether A > B, A = B or A < B.",
    s=["Feed A (first) and B (second); the module computes A − B = A + B' + 1 (signed 2's complement).",
       "| A = B  :  Z",
       "| A < B  :  S ⊕ V          (S alone is wrong if the subtraction overflows)",
       "| A > B  :  (S ⊕ V)' · Z'   = NOR(S ⊕ V, Z)",
       "Gates: one XOR (S, V), the equality output is Z itself, and one NOR (S⊕V, Z) for A > B.",
       "A: For unsigned inputs use A < B = C', A = B = Z, A > B = C·Z'."])
S[("2019-20", "CSE 305", "2(a)")] = dict(
    q="4-bit ALU, S3 S2 S1 S0: 0000 A'; 0001 A'+1; 0010 A'+B; 0011 A'+B+1; 0100 A'−B−1; 0101 A'−B; 0110 A'−1; 0111 A'; 100x (AB)'; 101x A ⊙ B; 110x A ⊕ B; 111x A ∨ B. Derive X_{i}, Y_{i}, Z_{i} using the least gates.",
    s=["This is the standard arithmetic table with A' in place of A. Logic rows are chosen so that Y keeps the pattern 0, B, B', 1.",
       ("T", ["S3 S2 S1 S0", "Function", "X_{i}", "Y_{i}", "C_{in}"], [
           ["000x / 001x…", "A', A'+B, A'−B−1, A'−1 (+1 for odd S0)", "A'", "0, B, B', 1", "S0"],
           ["100x", "(AB)' NAND", "A' + B'", "0", "—"], ["101x", "A ⊙ B XNOR", "A'", "B", "—"],
           ["110x", "A ⊕ B XOR", "A'", "B'", "—"], ["111x", "A ∨ B OR", "A'B'", "1", "—"]], [16, 36, 16, 16, 16]),
       "| Y_i = S1·B_i + S2·B_i'",
       "| X_i = A_i'·(S3·S2·S1·B_i)' + S3·S2'·S1'·B_i'",
       "| C_in = S3'·S0                    Z_i = S3'·C_i",
       "A: Check NAND (100x): X = A' + B', Y = 0 → A' + B' = (AB)' ✓; OR (111x): X = A'B', Y = 1 → (A'B')' = A + B ✓. Verified by simulation."])
S[("2019-20", "CSE 305", "2(b)")] = dict(
    q="Implement the hardware for F = 1 if ((A ≥ B && C ≠ D) || X == 0) else 0, with 4-bit A, B, C, D, X, basic gates and status-generator modules (each shows V, Z, S, C of 2nd input subtracted from 1st). Just draw the circuit.",
    s=["Three modules: M1(A, B), M2(C, D), M3(X, 0000).",
       "| A >= B  = (S1 ⊕ V1)'        from M1  (signed; unsigned: C1)",
       "| C != D  = Z2'                from M2",
       "| X == 0  = Z3                 from M3",
       "| F = (S1 ⊙ V1) · Z2' + Z3",
       "A: Gates: one XNOR (S1, V1), one NOT (Z2), one AND, one OR plus the three modules."])
