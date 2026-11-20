"""Master list of ART-part (Tushar Sir) TF questions.  Run: python -P questions_data.py → questions.json

Page = 1-based page in 'CSE209 ALL TF QUES (TF209).pdf' (same file the RS tracker calls TF209.pdf).
'CSE 209 (22 batch).pdf' is identical to TF209 pp. 1–7; 'All Merged Questions.pdf' = TF209 pp. 8–87.
f = note file (1 Ch1, 2 ALU, 3 Ch2, 4 Ch3) or 'OUT' (Outside Notes).  g = repeat-group key.
"""
import json
import os

# (year, course, qno, question, marks, page, f, lesson, type, in_notes, group, area)
R = [
    # ---------------------------------------------------------------- 2023-24 CSE 209 (Sec B)
    ("2023-24", "CSE 209", "5(a)(ii)", "MIPS-v22 (opcode|rt|rd|rs|shamt|funct): encode add $t0,$t1,$t2; addi $t2,$t0,1; lw $t1,4($t0) in binary", 10, "5", 3, "L11", "Numerical", "✔ Solved", "encode", ""),
    ("2023-24", "CSE 209", "5(b)", "4-bit ALU: Xi, Yi, Zi for A−B−1, A+B+1, transfer A, decrement A, A OR B, A'", 15, "5", 2, "L7", "Design", "✔ Solved", "aludesign", ""),
    ("2023-24", "CSE 209", "6(a)", "A: 4 GHz, 10 s; B must run in 6 s but needs 1.2× the clock cycles — target clock rate of B?", 13, "6", 1, "L2", "Numerical", "✔ Solved", "clockrate", ""),
    ("2023-24", "CSE 209", "6(b)", "MIPS code for do { if ((a<<2) > b) {a += 2; b += a;} else {a += c; b += c;} } while (a < N)", 13, "6", 3, "L12", "Design", "✔ Solved", "mipsloop", ""),
    ("2023-24", "CSE 209", "6(c)", "Explain PC-relative, immediate and base addressing with examples", 9, "6", 3, "L16", "Theory", "✔ Solved", "addrmodes", ""),
    ("2023-24", "CSE 209", "7(a)", "Multiplication hardware: long-multiplication and parallel add/shift versions (32-bit); simulate 1000 × 1011 on each", 20, "6", 4, "L20", "Trace", "✔ Solved", "multhw", ""),
    ("2023-24", "CSE 209", "7(b)", "Purpose of a positive bias in IEEE 754; smallest and largest values in single and double precision", 15, "6", 4, "L21", "Theory", "✔ Solved", "bias", ""),
    ("2023-24", "CSE 209", "8(c)", "beq $s0,$s1,L1 is out of range — replace it by a pair of instructions with a much greater reach", 5, "7", 3, "L15", "Theory", "✔ Solved", "farbranch", ""),
    # ---------------------------------------------------------------- 2022-23 CSE 209
    ("2022-23", "CSE 209", "1(a)", "Flowchart of floating-point addition; conditions for overflow, underflow, NaN and infinity", 10, "8", 4, "L22", "Theory", "✔ Solved", "fpadd", ""),
    ("2022-23", "CSE 209", "1(b)", "6-bit ALU division: dividend 1011 1100 1111, divisor 110101 — registers at each step", 10, "8", "OUT", "", "Trace", "", "division", "Integer division (textbook §3.4, not in short slides) — solved in Ch3 notes L23"),
    ("2022-23", "CSE 209", "4", "Hardware block diagram + flowchart of the sequential and the refined multiplication algorithm", 15, "10", 4, "L20", "Design", "✔ Solved", "multhw", ""),
    ("2022-23", "CSE 209", "9(c)", "MIPS for int fun(a,b){ if(b==0) return 0; else if(b/2==0) return fun(a*4,b/8); return fun(a+a,b/4)+a; }", 10, "12", 3, "L13", "Design", "✔ Solved", "mipsrec", ""),
    ("2022-23", "CSE 209", "11(a)", "Why is the overflow bit V computed by XOR-ing the last two carry bits?", 7, "13", 2, "L9", "Theory", "✔ Solved", "overflow", ""),
    ("2022-23", "CSE 209", "11(b) NOT part", "How is the NOT operation performed in MIPS? (jal-vs-j part is in the RS tracker; marks shared)", None, "13", 3, "L12", "Theory", "✔ Solved", "", ""),
    ("2022-23", "CSE 209", "11(c)", "Addressing modes of MIPS; illustrate the calculation for each", 10, "13", 3, "L16", "Theory", "✔ Solved", "addrmodes", ""),
    ("2022-23", "CSE 209", "11(d)", "4-bit ALU Xi, Yi, Zi for −A−B−2, B + A' (1's comp of A to B), A+B, A−B, AND, XOR", 10, "13", 2, "L7", "Design", "✔ Solved", "aludesign", ""),
    ("2022-23", "CSE 209", "12(a)", "How does JIT compilation improve the performance of a Java application?", 5, "13", 3, "L18", "Theory", "✔ Solved", "java", ""),
    ("2022-23", "CSE 209", "12(b)", "Static vs dynamic linking; advantages of dynamic linking", 10, "13", 3, "L18", "Theory", "✔ Solved", "linking", ""),
    ("2022-23", "CSE 209", "12(c)(i),(iii)", "Build 0x20014924 in $t1; from PC = 0x1FFFF000 can one branch reach it? (12(c)(ii) is in RS tracker; 10 marks shared)", 7, "14", 3, "L15", "Numerical", "✔ Solved", "const32", ""),
    # ---------------------------------------------------------------- 2022-23 CSE 305 (Sec B)
    ("2022-23", "CSE 305", "5(a)", "Rachel adds lh, lhu, sh, shu for multi-language support; Ross says not all are needed — agree?", 7, "18", 3, "L14", "Theory", "✔ Solved", "", ""),
    ("2022-23", "CSE 305", "5(b)", "4-bit ALU with parallel SUBTRACTORS only: A−B, A+B, −A−B−2, B−A, XOR, AND", 14, "18", 2, "L7", "Design", "✔ Solved", "aludesign", ""),
    ("2022-23", "CSE 305", "5(c)", "Link the object files of procedures A and B; updated addresses of the first instructions", 14, "18, 20", 3, "L18", "Trace", "✔ Solved", "linkobj", ""),
    ("2022-23", "CSE 305", "6(b)", "MIPS support for synchronization, with an example", 7, "18", 3, "L17", "Theory", "✔ Solved", "sync", ""),
    ("2022-23", "CSE 305", "6(c)", "MIPS for if (x > y + 131075) x = 8;  (x in $t1, y in $t2)", 8, "19", 3, "L14", "Design", "✔ Solved", "mipsfrag", ""),
    ("2022-23", "CSE 305", "6(d)", "P1 2.7 GHz (CPI 2,1,3,2) vs P2 3.2 GHz (2,3,2,3), 1.2×10⁶ instr 20/25/40/15 %: cycles, faster, max gain if 40 % improved", 15, "19", 1, "L3", "Numerical", "✔ Solved", "cpimix", ""),
    ("2022-23", "CSE 305", "7(a)", "Define response time and throughput. Are they synonymous?", 5, "19", 1, "L2", "Theory", "✔ Solved", "resptime", ""),
    ("2022-23", "CSE 305", "7(b)", "Program uses 40 variables, MIPS has 32 registers — what does the compiler do?", 7, "19", 3, "L10", "Theory", "✔ Solved", "", ""),
    ("2022-23", "CSE 305", "7(c)", "MIPS for int f(a,b,c,d){ return func(func(a,b), c+d); }", 8, "19", 3, "L13", "Design", "✔ Solved", "mipsproc", ""),
    ("2022-23", "CSE 305", "7(d)", "Static vs dynamic linking; with diagrams, how DLLs are called (lazy linkage)", 15, "19", 3, "L18", "Theory", "✔ Solved", "linking", ""),
    ("2022-23", "CSE 305", "8(a)", "MIPS FP code: float a,b,c; double w,x,y,z; if (a+b>c) x = (y*z)/w;", 7, "19", "OUT", "", "Design", "", "fpcode", "MIPS floating-point instructions (textbook §3.5) — solved in Ch3 notes L23"),
    ("2022-23", "CSE 305", "8(b)", "32-bit FP with 19-bit fraction: precision, smallest/largest absolute values, smallest denormal", 8, "19", 4, "L21", "Numerical", "✔ Solved", "customfp", ""),
    ("2022-23", "CSE 305", "8(c)", "f1 < f2 (IEEE single): treated as unsigned, is i1 < i2? As signed, is j1 < j2?", 20, "19", 4, "L21", "Theory", "✔ Solved", "", ""),
    # ---------------------------------------------------------------- 2021-22 CSE 305 (Sec B)
    ("2021-22", "CSE 305", "5(a)", "Which design principle is behind each of five MIPS features (16-bit branch offset, 32 registers, …)?", 15, "23", 3, "L10", "Theory", "✔ Solved", "designprin", ""),
    ("2021-22", "CSE 305", "5(b)", "2 % of runtime not parallelizable, 24 cores: speedup? Can it be made 60× faster?", 10, "23–24", 1, "L4", "Numerical", "✔ Solved", "amdahl", ""),
    ("2021-22", "CSE 305", "5(c)", "How can subword parallelism accelerate matrix multiplication / image processing?", 10, "24", "OUT", "", "Theory", "", "", "Subword parallelism (textbook §3.6) — short answer in Ch3 notes L23"),
    ("2021-22", "CSE 305", "6(a)", "MIPS for recursive fib(n)", 15, "24", 3, "L13", "Design", "✔ Solved", "mipsrec", ""),
    ("2021-22", "CSE 305", "6(b)(ii)", "PC = 0x2000 0000: can a single beq/bne set PC to 0x4000 0000? ((i) is in RS tracker)", 5, "24", 3, "L15", "Numerical", "✔ Solved", "reach", ""),
    ("2021-22", "CSE 305", "6(c)", "Block diagram of 32-bit combined multiply/divide hardware with a 32-bit ALU; functions of components", 10, "24", 4, "L20", "Design", "○ Partly", "multhw", ""),
    ("2021-22", "CSE 305", "7(b)", "FLOPS: misleading as a general metric but useful for a specific part — agree?", 16, "25", 1, "L4", "Theory", "✔ Solved", "mipsmetric", ""),
    ("2021-22", "CSE 305", "8(a)", "P1 2.7 GHz (CPI 3,3,2) vs P2 3.5 GHz (2,4,1), 200,000 instr 25/60/15 %: cycles, time, CPI of C for 2×", 11, "25", 1, "L3", "Numerical", "✔ Solved", "cpimix", ""),
    ("2021-22", "CSE 305", "8(b)", "Largest n such that every integer 1…n is exactly representable in IEEE single precision", 14, "25", 4, "L21", "Numerical", "✔ Solved", "", ""),
    ("2021-22", "CSE 305", "8(c)", "Addressing modes of MIPS; illustrate the calculation for each", 10, "25", 3, "L16", "Theory", "✔ Solved", "addrmodes", ""),
    # ---------------------------------------------------------------- 2020-21 CSE 305 (Sec B)
    ("2020-21", "CSE 305", "10(a)", "Briefly explain the eight great ideas in computer architecture", 12, "30", 1, "L1", "Theory", "✔ Solved", "greatideas", ""),
    ("2020-21", "CSE 305", "10(b)", "4-bit ALU (S3–S0), 12 functions incl. A−1, A+B+1, A−B−1, A', AB', XNOR, OR: Xi, Yi, Zi with least gates", 18, "30–31", 2, "L7", "Design", "✔ Solved", "aludesign", ""),
    ("2020-21", "CSE 305", "10(c)", "Briefly describe how to perform a signed multiplication", 5, "31", "OUT", "", "Theory", "", "", "Signed multiplication (textbook §3.3) — answer in Ch3 notes L23"),
    ("2020-21", "CSE 305", "11(a)", "SPECBM101: geometric mean 28.74 — find the execution time of Program 1", 10, "32", "OUT", "", "Numerical", "", "spec", "SPEC benchmark / geometric mean (textbook §1.10) — method in Ch1 notes L4"),
    ("2020-21", "CSE 305", "11(b)", "Processor unit with scratchpad memory: micro-operations for an addition; how to make it one", 8, "32", "OUT", "", "Theory", "", "", "Processor unit with scratchpad (Mano §9.2 — before the ALU deck's §9.3)"),
    ("2020-21", "CSE 305", "11(c)", "Efficient MIPS for testFunc(a,b,c): do { if (i>b) result += c; i++; } while (i<a)", 12, "33", 3, "L12", "Design", "✔ Solved", "mipsloop", ""),
    ("2020-21", "CSE 305", "11(d)", "Illustrate how MIPS follows 'Good design demands good compromises'", 5, "33", 3, "L11", "Theory", "✔ Solved", "designprin", ""),
    ("2020-21", "CSE 305", "12(a)", "Programs A and B (mult/add/sub/div CPI 3/1/2/4): which has the higher average CPI?", 8, "33", 1, "L3", "Numerical", "✔ Solved", "cpimix", ""),
    ("2020-21", "CSE 305", "12(b)", "Encode L1: bne $t0,$t1,L3; L2: j LX; L3: addi $t0,$t1,1 (L1 = 1000, LX = 131072): formats and field values", 10, "33–34", 3, "L15", "Numerical", "✔ Solved", "encodebr", ""),
    ("2020-21", "CSE 305", "12(c)", "Importance of guard digit, round digit and sticky bit when rounding", 9, "34", "OUT", "", "Theory", "", "", "FP rounding: guard/round/sticky (textbook §3.5) — answer in Ch3 notes L23"),
    ("2020-21", "CSE 305", "12(d)", "Status module (V Z S C of A−B): circuit that decides A > B, A = B, A < B", 8, "34", 2, "L9", "Design", "✔ Solved", "statuscmp", ""),
    ("2020-21", "CSE 305", "13(a)", "32-bit FP with 24-bit fraction: why bias, value of bias, smallest/largest absolute values, smallest denormal", 16, "35", 4, "L21", "Numerical", "✔ Solved", "customfp", ""),
    ("2020-21", "CSE 305", "13(b)", "How is the address calculated in PC-relative addressing?", 7, "35", 3, "L15", "Theory", "✔ Solved", "addrmodes", ""),
    ("2020-21", "CSE 305", "13(c)", "MIPS FP code: float a,b,c; double w,x,y,z; if (a+b>c) x = (y*z)/w;", 7, "35", "OUT", "", "Design", "", "fpcode", "MIPS floating-point instructions (textbook §3.5) — solved in Ch3 notes L23"),
    ("2020-21", "CSE 305", "13(d)", "Main differences between x86 and MIPS architectures", 5, "35", 3, "L18", "Theory", "◐ Method", "risc", ""),
    # ---------------------------------------------------------------- 2019-20 CSE 305 (Sec A)
    ("2019-20", "CSE 305", "1(a)", "Logs of systems A (2 GHz) and B (2.5 GHz): compare performance on Program 1", 15, "36", 1, "L3", "Numerical", "✔ Solved", "cpimix", ""),
    ("2019-20", "CSE 305", "1(b)", "Importance of Moore's law; 'improve the most important aspect by x to get x overall' — agree? (math)", 12, "36", 1, "L4", "Theory", "✔ Solved", "amdahl", ""),
    ("2019-20", "CSE 305", "1(c)", "Advantages of DLLs in C program execution; role of JIT in Java", 8, "36", 3, "L18", "Theory", "✔ Solved", "linking", ""),
    ("2019-20", "CSE 305", "2(a)", "4-bit ALU (S3–S0): A', A'+1, A'+B, A'+B+1, A'−B−1, A'−B, A'−1, NAND, XNOR, XOR, OR — Xi, Yi, Zi, least gates", 20, "36–37", 2, "L7", "Design", "✔ Solved", "aludesign", ""),
    ("2019-20", "CSE 305", "2(b)", "Circuit with status-generator modules + gates for F = ((A>=B && C!=D) || X==0)", 15, "37", 2, "L9", "Design", "✔ Solved", "statuscmp", ""),
    ("2019-20", "CSE 305", "3(a)", "MIPS for: while (x>=−5) loop; if (x>y+131075) x=1; x = A[131075]+5", 15, "37–38", 3, "L14", "Design", "✔ Solved", "mipsfrag", ""),
    ("2019-20", "CSE 305", "3(b)", "How pseudoinstructions work (example); always write assembly yourself for a critical section?", 12, "38", 3, "L17", "Theory", "✔ Solved", "pseudo", ""),
    ("2019-20", "CSE 305", "3(c)", "Why do MIPS arithmetic instructions demand three operands? Why only 32 registers?", 8, "38", 3, "L10", "Theory", "✔ Solved", "designprin", ""),
    ("2019-20", "CSE 305", "4(a)", "16-bit FP, largest 1.11…×2^63, smallest 1.00…×2^−62: format; −110.11₂×2¹; smallest denormal", 15, "38", 4, "L21", "Numerical", "✔ Solved", "customfp", ""),
    ("2019-20", "CSE 305", "4(b)", "Why the first multiplier hardware is inefficient; changes; draw the efficient hardware", 12, "38", 4, "L20", "Design", "✔ Solved", "multhw", ""),
    ("2019-20", "CSE 305", "4(c)", "MIPS FP code (double): if (a>b) c = c−(c*e)/d; else c = c+d;", 8, "38", "OUT", "", "Design", "", "fpcode", "MIPS floating-point instructions (textbook §3.5) — solved in Ch3 notes L23"),
    # ---------------------------------------------------------------- 2018-19 CSE 305 (Sec B)
    ("2018-19", "CSE 305", "5(a)", "Hardware + flowchart of the sequential multiplication algorithm; flowchart of the refined version", 12, "44", 4, "L20", "Design", "✔ Solved", "multhw", ""),
    ("2018-19", "CSE 305", "5(b)", "16-bit FP with 4-bit exponent: represent −1.25 and 0.375", 8, "44", 4, "L21", "Numerical", "✔ Solved", "customfp", ""),
    ("2018-19", "CSE 305", "5(c)", "Decimal value of IEEE single 0xDF807500", 5, "44", 4, "L21", "Numerical", "✔ Solved", "hex2fp", ""),
    ("2018-19", "CSE 305", "5(d)", "4-bit ALU: add, transfer A, A+B', increment A, XOR, NOT, AND, OR — one typical stage", 10, "44–45", 2, "L8", "Design", "✔ Solved", "aluful", ""),
    ("2018-19", "CSE 305", "6(a)", "Addressing modes of MIPS; describe and illustrate the calculation", 15, "45", 3, "L16", "Theory", "✔ Solved", "addrmodes", ""),
    ("2018-19", "CSE 305", "6(b)", "4-bit ALU division: dividend 11001001, divisor 1011 — registers at each step", 15, "45", "OUT", "", "Trace", "", "division", "Integer division (textbook §3.4, not in short slides) — solved in Ch3 notes L23"),
    ("2018-19", "CSE 305", "6(c)", "How many MIPS instruction formats? Name and field lengths", 5, "45", 3, "L11", "Theory", "✔ Solved", "formats", ""),
    ("2018-19", "CSE 305", "7(a)", "Machine code (decimal fields) for the loop loaded at 60000 (sll/add/lw/beq/j/addi/j)", 10, "45", 3, "L15", "Numerical", "✔ Solved", "encodeloop", ""),
    ("2018-19", "CSE 305", "7(b)", "4 GHz, FP/INT/LS/BR = 160/110/10/16 M, CPI 2/1/5/2: time; FP or LS CPI for 2×; ±15 %/−20 % change", 20, "45–46", 1, "L3", "Numerical", "✔ Solved", "cpimix", ""),
    ("2018-19", "CSE 305", "7(c)", "Use of bias in FP representation; encoding of infinity", 5, "46", 4, "L21", "Theory", "✔ Solved", "bias", ""),
    ("2018-19", "CSE 305", "8(a)", "MIPS for recursive fun(a,b) computing a^b (b%2 test, fun(a*a,b/2)*a)", 20, "46", 3, "L13", "Design", "✔ Solved", "mipsrec", ""),
    ("2018-19", "CSE 305", "8(b)", "Steps of FP addition with an example; overflow/underflow conditions", 10, "46", 4, "L22", "Theory", "✔ Solved", "fpadd", ""),
    ("2018-19", "CSE 305", "8(c)", "beq $s0,$s1,30500 at address 005000 — what is the problem and the fix?", 5, "46", 3, "L15", "Theory", "✔ Solved", "farbranch", ""),
    # ---------------------------------------------------------------- 2017-18 CSE 305 (Sec B)
    ("2017-18", "CSE 305", "5(a)", "Classes A/B/C CPI 1.2/2/2.5; P1 (40,10,16) vs P2 (12,13,40): faster by how much; CPI of B for P1 2×", 15, "51–52", 1, "L3", "Numerical", "✔ Solved", "cpimix", ""),
    ("2017-18", "CSE 305", "5(b)", "16-bit half precision (4-bit exponent): convert 0.75 and 1.25 and add step by step", 15, "52", 4, "L22", "Trace", "✔ Solved", "fpadd", ""),
    ("2017-18", "CSE 305", "5(c)", "Decimal value of IEEE single 0x7F800005", 5, "52", 4, "L21", "Numerical", "✔ Solved", "hex2fp", ""),
    ("2017-18", "CSE 305", "6(a)", "4-bit ALU: add, transfer A, decrement A, A+B', XOR, AND, NOT, OR — one typical stage", 25, "52", 2, "L8", "Design", "✔ Solved", "aluful", ""),
    ("2017-18", "CSE 305", "6(b)", "For each arithmetic operation of 6(a): when is the output carry 1?", 10, "52", 2, "L6", "Theory", "✔ Solved", "carry", ""),
    ("2017-18", "CSE 305", "7(a)", "MIPS for swap(v,k) and sort(v,n) (insertion-style nested loops)", 25, "53", 3, "L13", "Design", "✔ Solved", "mipsproc", ""),
    ("2017-18", "CSE 305", "7(b)", "MIPS code to jump to the instruction at address 0x4000 0001", 10, "53", 3, "L15", "Design", "✔ Solved", "reach", ""),
    ("2017-18", "CSE 305", "8(a)", "4-bit ALU division: dividend 11010101, divisor 1011 — registers at every step", 15, "53", "OUT", "", "Trace", "", "division", "Integer division (textbook §3.4, not in short slides) — solved in Ch3 notes L23"),
    ("2017-18", "CSE 305", "8(b)", "MIPS FP code for float convert(float cels): ferh = 9.0*cels/5.0 + 32.0", 10, "53", "OUT", "", "Design", "", "fpcode", "MIPS floating-point instructions (textbook §3.5) — solved in Ch3 notes L23"),
    ("2017-18", "CSE 305", "8(c)", "How many MIPS instruction formats? Name and field lengths", 10, "53", 3, "L11", "Theory", "✔ Solved", "formats", ""),
    # ---------------------------------------------------------------- 2016-17 CSE 305
    ("2016-17", "CSE 305", "4(c)", "Compare the characteristics of typical CISC and RISC architectures (RS tracker: 'ISA (ART part)')", 6, "56", 3, "L18", "Theory", "◐ Method", "risc", ""),
    ("2016-17", "CSE 305", "5(b)", "SPEC CINT2006 table (12 programs): SPEC ratios and overall SPEC ratio", 10, "57", "OUT", "", "Numerical", "", "spec", "SPEC benchmark / geometric mean (textbook §1.10) — method in Ch1 notes L4"),
    ("2016-17", "CSE 305", "5(c)", "3 GHz, FP/INT/LS/BR = 40/80/90/15 M, CPI 1/1/3/2: time; FP CPI for 2×; +20 %/−10 % CPI change", 15, "58", 1, "L3", "Numerical", "✔ Solved", "cpimix", ""),
    ("2016-17", "CSE 305", "6(a)", "Complete the assembly from the given machine code at 1000–1020 (sll/add/lw/bne/addi/j)", 10, "58", 3, "L15", "Numerical", "✔ Solved", "encodeloop", ""),
    ("2016-17", "CSE 305", "6(b)", "MIPS support for synchronization, with an example", 10, "58", 3, "L17", "Theory", "✔ Solved", "sync", ""),
    ("2016-17", "CSE 305", "6(c)", "Which design principle behind: 16-bit immediates, 3 register operands, PC-relative branches, 32 registers, fixed register fields", 15, "58–59", 3, "L10", "Theory", "✔ Solved", "designprin", ""),
    ("2016-17", "CSE 305", "7(a)", "Illustrate the five MIPS addressing modes with an example instruction each", 20, "59", 3, "L16", "Theory", "✔ Solved", "addrmodes", ""),
    ("2016-17", "CSE 305", "7(b)", "Simulate FP addition −0.25 + 0.625 on the FP adder hardware (fill the tables)", 15, "59", 4, "L22", "Trace", "✔ Solved", "fpadd", ""),
    ("2016-17", "CSE 305", "8(a)", "Overflow conditions in the O/SA/SB/SR table for add/subtract; Boolean function for V", 10, "60", 4, "L19", "Theory", "✔ Solved", "ovtable", ""),
    ("2016-17", "CSE 305", "8(b)", "Redesign a single-bus computer so devices of different speeds can share the bus", 10, "61", "OUT", "", "Design", "", "", "Buses / I/O (not in either teacher's slides)"),
    ("2016-17", "CSE 305", "8(c)", "Simulate unsigned multiplication 0110 × 0110 on the refined (shift-right product) hardware", 15, "61–62", 4, "L20", "Trace", "✔ Solved", "multhw", ""),
    # ---------------------------------------------------------------- 2015-16 CSE 305
    ("2015-16", "CSE 305", "1(a)", "P1 3 GHz CPI 1.5, P2 2.5 GHz CPI 1.0, P3 4 GHz CPI 2.2: highest IPS; cycles & instr in 10 s; clock for −30 % time with +20 % CPI", 10, "63", 1, "L2", "Numerical", "✔ Solved", "clockrate", ""),
    ("2015-16", "CSE 305", "1(b)", "Arith/store/load/branch = 500/50/100/50, cycles 1/5/5/2, 4 GHz: time, CPI; loads halved → speedup, CPI", 10, "63", 1, "L3", "Numerical", "✔ Solved", "cpimix", ""),
    ("2015-16", "CSE 305", "1(c)", "CPI 1/12/5, 2.56 G arith, 1.28 G ld/st, 256 M branch, 2 GHz, divided by 0.7p: time on 1/2/4 processors etc.", 15, "63", 1, "L3", "Numerical", "✔ Solved", "parcpi", ""),
    ("2015-16", "CSE 305", "2(a)", "A: 10 G instr, 4 GHz, CPI 1; B: 8 G, 4 GHz, CPI 1.1 — higher MIPS? faster?", 5, "64", 1, "L4", "Numerical", "✔ Solved", "mipsmetric", ""),
    ("2015-16", "CSE 305", "5(a)", "Minimal MIPS for recursive rstrcopy(char *dest, char *source)", 25, "65–66", 3, "L14", "Design", "✔ Solved", "mipsproc", ""),
    ("2015-16", "CSE 305", "5(b)", "MIPS code to load 0001 0000 0011 1101 0000 1001 0000 0000₂ into $s0", 6, "66", 3, "L14", "Design", "✔ Solved", "const32", ""),
    ("2015-16", "CSE 305", "5(c)", "What are pseudoinstructions? Two examples", 4, "66", 3, "L17", "Theory", "✔ Solved", "pseudo", ""),
    ("2015-16", "CSE 305", "6(a)", "Steps of floating-point addition with an example", 12, "66", 4, "L22", "Theory", "✔ Solved", "fpadd", ""),
    ("2015-16", "CSE 305", "6(b)", "Addressing modes of MIPS; describe and illustrate the calculation", 15, "66", 3, "L16", "Theory", "✔ Solved", "addrmodes", ""),
    ("2015-16", "CSE 305", "6(c)", "What is a data race? MIPS instructions for it and how they work", 8, "66", 3, "L17", "Theory", "✔ Solved", "sync", ""),
    ("2015-16", "CSE 305", "7(c)", "Use of bias in FP representation; encoding of infinity", 10, "66", 4, "L21", "Theory", "✔ Solved", "bias", ""),
    # ---------------------------------------------------------------- 2014-15 CSE 305
    ("2014-15", "CSE 305", "1(c)", "Compare the characteristics of typical CISC and RISC architectures (RS tracker: 'ISA (ART part)')", 8, "68", 3, "L18", "Theory", "◐ Method", "risc", ""),
    ("2014-15", "CSE 305", "5(b)", "2 GHz, FP/INT/LS/BR = 160/110/10/16 M, CPI 2/1/5/2: time; FP CPI for 2×; LS CPI for 2×", 15, "71", 1, "L3", "Numerical", "✔ Solved", "cpimix", ""),
    ("2014-15", "CSE 305", "6(a)", "Complete the MIPS code of recurseSum(n) (fill the blanks)", 15, "71", 3, "L13", "Design", "✔ Solved", "mipsrec", ""),
    ("2014-15", "CSE 305", "6(b)", "What support does MIPS provide for synchronization?", 5, "71", 3, "L17", "Theory", "✔ Solved", "sync", ""),
    ("2014-15", "CSE 305", "6(c)", "Complete the decimal machine code of the loop at 6000 (sll/add/lw/beq/j/addi/j)", 15, "71", 3, "L15", "Numerical", "✔ Solved", "encodeloop", ""),
    ("2014-15", "CSE 305", "7(a)", "Draw the illustrations of the five MIPS addressing modes", 15, "72", 3, "L16", "Theory", "✔ Solved", "addrmodes", ""),
    ("2014-15", "CSE 305", "7(b)", "Why no blt/bge in MIPS? Program them with MIPS instructions", 10, "72", 3, "L12", "Theory", "✔ Solved", "", ""),
    ("2014-15", "CSE 305", "7(c)", "beq $s0,$s1,30500 at address 005000 — what is the problem and the fix?", 10, "72", 3, "L15", "Theory", "✔ Solved", "farbranch", ""),
    ("2014-15", "CSE 305", "8(a)", "Overflow conditions in the O/SA/SB/SR table; Boolean function for V", 12, "72", 4, "L19", "Theory", "✔ Solved", "ovtable", ""),
    ("2014-15", "CSE 305", "8(b)", "Flowchart of the sequential multiplication; draw the register-optimized refined hardware", 13, "73", 4, "L20", "Design", "✔ Solved", "multhw", ""),
    # ---------------------------------------------------------------- 2013-14 CSE 305
    ("2013-14", "CSE 305", "3(a)", "Steps for adding two binary floating-point numbers", 10, "74", 4, "L22", "Theory", "✔ Solved", "fpadd", ""),
    ("2013-14", "CSE 305", "3(b)", "IEEE 754 single-precision representation of −0.75", 10, "74", 4, "L21", "Numerical", "✔ Solved", "", ""),
    ("2013-14", "CSE 305", "3(c)", "Block diagram + flowchart for 32-bit unsigned multiplication with no separate multiplier register", 15, "74", 4, "L20", "Design", "✔ Solved", "multhw", ""),
    ("2013-14", "CSE 305", "5(a)", "What is Moore's law? Response time and throughput", 6, "75", 1, "L2", "Theory", "✔ Solved", "resptime", ""),
    ("2013-14", "CSE 305", "5(b)", "P1 3 GHz CPI 1/2/3/4 vs P2 2 GHz CPI 2/2/2/2, 200 instr 10/20/50/20 %: cycles, faster, CPI", 15, "75", 1, "L3", "Numerical", "✔ Solved", "cpimix", ""),
    ("2013-14", "CSE 305", "5(c)", "Amdahl's law: 100 s program, division 80 s — improvement in division for 4× overall?", 8, "75", 1, "L4", "Numerical", "✔ Solved", "amdahl", ""),
    ("2013-14", "CSE 305", "5(d)", "A: 10 G instr, 4 GHz, CPI 1; B: 8 G, 4 GHz, CPI 1.1 — higher MIPS? faster?", 6, "75", 1, "L4", "Numerical", "✔ Solved", "mipsmetric", ""),
    ("2013-14", "CSE 305", "6(a)", "Four MIPS design principles; steps for starting a Java application", 8, "75", 3, "L10", "Theory", "✔ Solved", "designprin", ""),
    ("2013-14", "CSE 305", "6(b)", "MIPS code and machine code for A[3] = A[1] − A[2] (base in $s0)", 12, "75", 3, "L11", "Numerical", "✔ Solved", "encode", ""),
    ("2013-14", "CSE 305", "6(c)", "MIPS for int sum(int n){ if (n<=0) return 0; else return n + sum(n−1); }", 12, "76", 3, "L13", "Design", "✔ Solved", "mipsrec", ""),
    ("2013-14", "CSE 305", "6(d)", "Branch target too far for 16 bits: how does the assembler rewrite beq $s0,$s1,L1?", 3, "76", 3, "L15", "Theory", "✔ Solved", "farbranch", ""),
    ("2013-14", "CSE 305", "7(a)", "ll and sc; MIPS code to do A[0] = X atomically", 8, "76", 3, "L17", "Design", "✔ Solved", "sync", ""),
    ("2013-14", "CSE 305", "7(b)", "Describe MIPS addressing modes", 4, "76", 3, "L16", "Theory", "✔ Solved", "addrmodes", ""),
    # ---------------------------------------------------------------- 2012-13 CSE 305
    ("2012-13", "CSE 305", "1(a)", "Jump address table: implement case/switch with it (example)", 15, "78", 3, "L13", "Design", "✔ Solved", "", ""),
    ("2012-13", "CSE 305", "1(b)", "How can you create a 32-bit constant in MIPS assembly?", 5, "78", 3, "L14", "Theory", "✔ Solved", "const32", ""),
    ("2012-13", "CSE 305", "1(c)", "Loop at 80000: immediate fields of the bne and j instructions", 8, "78", 3, "L15", "Numerical", "✔ Solved", "encodeloop", ""),
    ("2012-13", "CSE 305", "1(d)", "Why might the assembler have problems with 'Here: beq $s0,$s2,there … there:'? Fix", 7, "78", 3, "L15", "Theory", "✔ Solved", "farbranch", ""),
    ("2012-13", "CSE 305", "6(a)", "CPU times FP 50 / INT 80 / LS 50 / BR 30 s: % gain for FP −20 %; INT cut for −20 % total; branch only?", 9, "79", 1, "L4", "Numerical", "✔ Solved", "amdahl", ""),
    ("2012-13", "CSE 305", "8(a)", "Purpose of biased notation for FP exponents", 5, "81", 4, "L21", "Theory", "✔ Solved", "bias", ""),
    ("2012-13", "CSE 305", "8(b)", "Flowchart of division for the given (refined) division hardware", 12, "81", "OUT", "", "Design", "", "division", "Integer division (textbook §3.4, not in short slides) — solved in Ch3 notes L23"),
    ("2012-13", "CSE 305", "8(c)", "Describe the steps of DMA transfer", 8, "81", "OUT", "", "Theory", "", "", "I/O, DMA (not in either teacher's slides; not in RS tracker)"),
    ("2012-13", "CSE 305", "8(d)", "Crossbar network and Omega network with diagrams", 10, "81", "OUT", "", "Theory", "", "", "Interconnection networks (not in either teacher's slides; not in RS tracker)"),
    # ---------------------------------------------------------------- 2011-12 CSE 305
    ("2011-12", "CSE 305", "1(a)", "Components of a computer and the task of each", 7.5, "84", 1, "L1", "Theory", "✔ Solved", "", ""),
    ("2011-12", "CSE 305", "1(b)", "ISA classes (stack, accumulator, register-memory, load-store) with examples and block diagrams", 10, "84", "OUT", "", "Theory", "", "", "ISA classes (textbook Appendix — not in slides)"),
    ("2011-12", "CSE 305", "1(c)", "A: 250 ps, CPI 2.0; B: 500 ps, CPI 1.2 — which is faster and by how much?", 7, "84", 1, "L3", "Numerical", "✔ Solved", "cpimix", ""),
    ("2011-12", "CSE 305", "1(d)", "10 s program, 50 % FP; FP unit 5× faster — speedup?", 6, "84", 1, "L4", "Numerical", "✔ Solved", "amdahl", ""),
    ("2011-12", "CSE 305", "1(e)", "Problems with measuring performance in MIPS", 4.5, "84", 1, "L4", "Theory", "✔ Solved", "mipsmetric", ""),
    ("2011-12", "CSE 305", "2(a)", "MIPS design principles; one use of each in the MIPS ISA", 8, "84", 3, "L10", "Theory", "✔ Solved", "designprin", ""),
    ("2011-12", "CSE 305", "2(b)", "Instructions and registers used in a MIPS procedure call and their purpose", 7.5, "84", 3, "L13", "Theory", "✔ Solved", "", ""),
    ("2011-12", "CSE 305", "2(c)", "Branch target too far for 16 bits: rewrite BEQ $s0,$s1,L1", 3.5, "84", 3, "L15", "Theory", "✔ Solved", "farbranch", ""),
    ("2011-12", "CSE 305", "2(d)", "Describe MIPS addressing modes", 10, "84", 3, "L16", "Theory", "✔ Solved", "addrmodes", ""),
    ("2011-12", "CSE 305", "2(e)", "Three examples of the complexity of IA-32", 6, "84", 3, "L18", "Theory", "◐ Method", "risc", ""),
    ("2011-12", "CSE 305", "5(a)", "Flow diagram of FP addition; overflow/underflow conditions", 10, "86", 4, "L22", "Theory", "✔ Solved", "fpadd", ""),
    ("2011-12", "CSE 305", "6(a)", "First and refined multiplication hardware; improvement of the refined version", 15, "86", 4, "L20", "Design", "✔ Solved", "multhw", ""),
]

KEYS = ("year", "course", "qno", "question", "marks", "page", "file", "lesson", "type", "in_notes", "group", "area")


def rows():
    out = [dict(zip(KEYS, r)) for r in R]
    for r in out:
        ys = []
        if r["group"]:
            for o in out:
                if o is not r and o["group"] == r["group"]:
                    tag = f"{o['year']} {o['qno']}"
                    if o["year"] == "2022-23":
                        tag += f" ({o['course']})"
                    ys.append(tag)
        r["same_type"] = "; ".join(ys[:6]) + ("; …" if len(ys) > 6 else "") if ys else "—"
    return out


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    data = rows()
    with open(os.path.join(here, "questions.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(data), "rows;", Counter(r["file"] for r in data))
    print(Counter(r["year"] for r in data))
