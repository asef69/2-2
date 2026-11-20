# Reading log — Tushar Sir's decks (slide no. = PDF page)

## Chapter_01.pdf (28 slides) — Computer Abstractions and Technology (P&H 5e)
- 1 title · 2 computer revolution (Moore's law) · 3–4 classes: PC, server, supercomputer, embedded · 5–6 PostPC era (chart; PMD, cloud, WSC, SaaS)
- 7 what you will learn · 8 understanding performance (algorithm / language-compiler-architecture / processor+memory / I/O)
- 9 eight great ideas (Moore, abstraction, common case, parallelism, pipelining, prediction, hierarchy, redundancy)
- 10 below your program (app / system sw: compiler, OS / hardware) · 11 levels of code (HLL → asm → binary; swap example)
- 12 components (input, output, memory, datapath, control; I/O devices) · 13 abstractions: ISA, ABI, implementation
- 14 airplane example · 15 response time vs throughput · 16 Perf = 1/T; "X is n times faster"; 10 s vs 15 s → 1.5
- 17 elapsed vs CPU time (user + system) · 18 clocking: period 250 ps, 4 GHz
- 19 CPU time = cycles × Tc = cycles / f · 20 example A 2 GHz 10 s, B 6 s with 1.2× cycles → 4 GHz
- 21 cycles = IC × CPI; CPU time = IC × CPI × Tc · 22 A 250 ps CPI 2.0 vs B 500 ps CPI 1.2 → A 1.2× faster
- 23 weighted CPI formula · 24 classes A/B/C CPI 1/2/3; seq1 IC 5 → 10 cycles CPI 2.0; seq2 IC 6 → 9, CPI 1.5
- 25 performance summary (Instructions/Program × Cycles/Instr × s/cycle; algorithm/lang/compiler/ISA effects)
- 26 Amdahl: T_improved = T_aff/n + T_unaff; multiply 80/100 s, 5× overall impossible; make common case fast
- 27 MIPS pitfall: MIPS = IC/(T×10^6) = f/(CPI×10^6) · 28 concluding remarks (power is a limiting factor)
- NOT in deck: SPEC, power wall formula, multicore section.

## ALU Design.pdf (23 slides) — Mano, Digital Logic & Computer Design ch 9.3–9.7
- 1 title · 2 4-bit ALU block (A, B, s2 mode, s1 s0 function, Cin, Cout, F) · 3 4-bit parallel adder (FA cascade C1…C5)
- 4 half adder S = x'y + xy', C = xy · 5 full adder S = x'y'z + x'yz' + xy'z' + xyz, C = xy + xz + yz
- 6 (a) A+B (b) A+B+1 (c) A+B' (d) A+B'+1 = A−B · 7 (e) A (f) A+1 (g) A + all 1s = A−1 (h) A+all1s+1 = A
- 8 Fig 9-7 true/complement one/zero circuit: Yi = Bi s0 + Bi' s1 (table 00→0, 01→B, 10→B', 11→1)
- 9 Fig 9-8 logic diagram of arithmetic circuit; generic block: selection vars → comb. circuit → X, Y → parallel adder
- 10 Table 9-1 function table (s1 s0 Cin → 8 functions) · 11 Table 9-2 when Cout = 1 for each function
- 12–14 design example adder/subtractor: Xi = Ai, Yi = Bi ⊕ s, Cin = s; Fig 9-10 4-bit adder/subtractor
- 15 Fig 9-11 one logic stage: mux of OR, XOR, AND, NOT (s1 s0) · 16 Fig 9-12 combining arithmetic + logic stage with mux on s2
- 17–18 more efficient design: logic ops from arithmetic circuit with carries 0 (Table 9-3: s2=1: Xi⊕Yi with Yi=0,B,B',1 → A, A⊕B, A⊙B, A')
  modify: Xi = Ai + s2 s1' s0' Bi + s2 s1 s0' Bi', Yi = s0 Bi + s1 Bi', Zi = s2' Ci
- 19 Fig 9-13 ALU logic diagram · 20 Table 9-4 ALU function table (12 functions)
- 21 status register C, S, Z, V (V = C8 ⊕ C9; 8-bit → >127 or < −128) · 22 Fig 9-14 status bits (Z = NOR of outputs)
- 23 references Mano 9.3–9.7. NOT in deck: scratchpad/processor unit (Mano 9.2), shifter.

## Chapter_02.pdf (69 slides) — Instructions: Language of the Computer
- 2–3 instruction set, MIPS · 4–5 arithmetic, DP1 simplicity favours regularity; f=(g+h)−(i+j)
- 6–7 register operands, 32×32 file, DP2 smaller is faster · 8 memory operands, byte addressing, aligned, big-endian
- 9–10 lw/sw examples g=h+A[8] (offset 32), A[12]=h+A[8] · 11 registers vs memory, spilling
- 12 immediates addi, DP3 make the common case fast · 13 $zero
- 14 unsigned range · 15–16 2's complement range, special values · 17 negation · 18 sign extension (addi, lb/lh, beq/bne)
- 19 instruction encoding, register numbers ($t0–$t7 8–15, $t8–$t9 24–25, $s0–$s7 16–23)
- 20–21 R-format (op rs rt rd shamt funct; 6 5 5 5 5 6); add $t0,$s1,$s2 = 0x02324020
- 22 hex · 23 I-format, DP4 good design demands good compromises
- 24 logical ops table (sll srl and andi or ori nor) · 25 shifts · 26 AND mask · 27 OR · 28 NOT via nor
- 29 beq bne j · 30 if-else compile · 31 while loop (save[i]==k) · 32 basic blocks
- 33 slt slti · 34 why no blt/bge · 35 signed vs unsigned (slt vs sltu)
- 36 procedure steps · 37 register usage ($a0–$a3 4–7, $v0–$v1 2–3, $gp 28, $sp 29, $fp 30, $ra 31)
- 38 jal / jr · 39–40 leaf_example · 41 non-leaf · 42–43 fact · 44 stack frame · 45 memory layout (text 0x00400000, static 0x10000000, $gp 0x10008000, $sp 0x7ffffffc)
- 46 character data · 47 lb lh lbu lhu sb sh · 48–49 strcpy · 50 32-bit constants lui/ori (lhi $s0,61; ori 2304)
- 51 branch addressing PC-relative · 52 jump addressing pseudo-direct · 53 target addressing example (Loop at 80000; bne offset 2; j 20000)
- 54 branching far away (beq → bne + j) · 55 addressing mode summary (immediate, register, base, PC-relative, pseudodirect)
- 56 synchronization, data race · 57 ll / sc, atomic swap · 58 translation & startup (compiler→assembler→linker→loader)
- 59 pseudoinstructions (move, blt; $at) · 60 object module parts · 61 linking · 62 loading · 63 dynamic linking · 64 lazy linkage
- 65 Java (JVM, JIT) · 66 fallacies: powerful instruction ⇒ performance; assembly for performance · 67 backward compatibility (x86 instruction count chart)
- 68 pitfalls: increment by 4; pointer to automatic variable · 69 concluding: 4 design principles, MIPS typical RISC c.f. x86

## Chapter_03_Arithmetic-shortslide.pdf (20 slides; printed numbers differ from PDF page from p17 on)
- 2 intro · 3 integer addition 7+6, overflow rules · 4 subtraction, overflow rules
- 5 long multiplication 1000×1001 = 1001000; first multiplier hardware (64-bit multiplicand shift-left, 64-bit ALU, multiplier shift-right)
- 6 flowchart (test Multiplier0, add, shift, 32 repetitions) · 7 optimized multiplier (32-bit ALU, 64-bit product, shift right) · 8 HI/LO, mult, multu, mul
- 9 floating point, normalized · 10 IEEE 754-1985 single/double · 11 format x = (−1)^S (1+F) 2^(E−bias), bias 127/1023
- 12 single range ±1.2e−38 … ±3.4e38 · 13 double range ±2.2e−308 … ±1.8e308 · 14 precision ~6 / ~16 decimal digits
- 15 −0.75 → 0xBF400000 · 16 0xC0A00000 → −5.0 · 17 decimal FP add 9.999e1 + 1.610e−1 = 1.002e2 · 18 binary 0.5 + (−0.4375) = 0.0625
- 19 FP adder multi-cycle · 20 FP adder hardware (4 steps)
- NOT in deck: division, Booth/signed multiplication, FP multiplication, MIPS FP instructions, guard/round/sticky, subword parallelism.
