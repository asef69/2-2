"""Solutions, part 2 (Ch2 MIPS ISA)."""
import answers_asm as A

S = {}
code = lambda text: ["| " + ln for ln in text.split("\n")]

ADDR_TABLE = ("T", ["Mode", "Operand / target", "Calculation", "Example"], [
    ["1. Immediate", "constant in the instruction", "sign-extend(imm16)", "addi $s3,$s3,4"],
    ["2. Register", "a register", "R[rs], R[rt]", "add $t0,$s1,$s2"],
    ["3. Base (displacement)", "memory word", "address = R[rs] + sign-extend(imm16)", "lw $t0,32($s3)"],
    ["4. PC-relative", "branch target", "PC + 4 + sign-extend(imm16) × 4", "beq $s0,$s1,L1"],
    ["5. Pseudo-direct", "jump target", "(PC+4)[31:28] : addr26 : 00", "j Loop"]], [20, 22, 34, 24])

S[("2023-24", "CSE 209", "5(a)(ii)")] = dict(
    q="MIPS-v22: R-type = opcode(6) | rt(5) | rd(5) | rs(5) | shamt(5) | funct(6); I-type = opcode(6) | rt(5) | rs(5) | constant(16). $t0, $t1, $t2 = 2, 3, 4; shamt = funct = 0. Translate to binary: add $t0,$t1,$t2 (opcode 0; $t0 destination, $t1 source 1, $t2 source 2); addi $t2,$t0,1 (opcode 6); lw $t1,4($t0) (opcode 5).",
    s=["The field order is the question's, not standard MIPS. In I-type rt is the destination (addi, lw).",
       "| add  $t0,$t1,$t2: op 0 | rt=$t2=4 | rd=$t0=2 | rs=$t1=3 | 0 | 0",
       "|    000000 00100 00010 00011 00000 000000 = 0x00821800",
       "| addi $t2,$t0,1:   op 6 | rt=$t2=4 | rs=$t0=2 | 1",
       "|    000110 00100 00010 0000000000000001 = 0x18820001",
       "| lw   $t1,4($t0):  op 5 | rt=$t1=3 | rs=$t0=2 | 4",
       "|    000101 00011 00010 0000000000000100 = 0x14620004",
       "A: Machine words 0x00821800, 0x18820001, 0x14620004."])
S[("2023-24", "CSE 209", "6(b)")] = dict(
    q="MIPS for: int a=5, b=10, c=2; int N=30; do { if ((a<<2) > b) { a += 2; b += a; } else { a += c; b += c; } } while (a < N); return 0;   ($t0=a, $t1=b, $t2=c, $t3=N)",
    s=["(a << 2) > b ⇔ b < (a << 2), so slt with the operands swapped. Test the opposite condition to skip the then-part."] + code(A.DOWHILE_2324) +
      ["A: Simulated: ends with a = 31, b = 121, like the C program."])
S[("2023-24", "CSE 209", "6(c)")] = dict(
    q="Explain PC-relative addressing mode, immediate addressing mode and base addressing mode with examples.",
    s=["**PC-relative** — the 16-bit field of beq/bne is a word offset from PC + 4: target = PC + 4 + offset×4. Example: beq at 80012 with offset 2 → 80016 + 8 = 80024.",
       "**Immediate** — the operand is the 16-bit constant in the instruction (sign-extended): addi $s3,$s3,4.",
       "**Base (displacement)** — memory address = register + sign-extended 16-bit constant: lw $t0,32($s3) with $s3 = 1000 → address 1032."])
S[("2023-24", "CSE 209", "8(c)")] = dict(
    q="beq $s0,$s1,L1 where L1 is out of branching range. Replace the beq by a pair of instructions that offers a much greater branching distance.",
    s=["The 16-bit branch offset reaches only ±32 K words. Invert the condition and use a jump (26-bit field, reaches the whole 256 MB block):",
       "| bne $s0, $s1, L2     # skip the jump when NOT equal",
       "| j   L1               # far target",
       "| L2: ...",
       "A: Same behaviour: control reaches L1 exactly when $s0 = $s1."])
S[("2022-23", "CSE 209", "9(c)")] = dict(
    q="MIPS for: int fun(int a, int b) { if (b == 0) return 0; else if (b / 2 == 0) return fun(a*4, b/8); return fun(a+a, b/4) + a; }",
    s=["a in $a0, b in $a1. b/2, b/4, b/8 by sra (b ≥ 0 assumed). The value a must survive the second call, so it is saved on the stack."] + code(A.FUN_2223) +
      ["A: Simulated against the C function for 6 argument pairs — all equal."])
S[("2022-23", "CSE 209", "11(b) NOT part")] = dict(
    q="How is the NOT operation performed in MIPS assembly? (The jal-versus-j part of 11(b) is in the RS tracker.)",
    s=["MIPS has no NOT instruction; it has the three-operand NOR (a NOR b = NOT(a OR b)).",
       "| nor $t0, $t1, $zero     # $t0 = ~($t1 | 0) = ~$t1",
       "A: NOR with $zero gives NOT, so no separate instruction is needed (simplicity favours regularity)."])
S[("2022-23", "CSE 209", "11(c)")] = dict(
    q="What are the different addressing modes of MIPS? Illustrate the calculation process for each.",
    s=[ADDR_TABLE,
       "| Immediate    | op | rs | rt |  imm16  |  operand = imm16",
       "| Register     | op | rs | rt | rd | .. | funct |  operand = R[rs], R[rt]",
       "| Base         | op | rs | rt |  addr16 |  R[rs] + addr16 → memory",
       "| PC-relative  | op | rs | rt |  addr16 |  PC+4 + addr16×4 → memory (instruction)",
       "| Pseudodirect | op |      addr26       |  PC+4[31:28] : addr26 : 00",
       "Numbers: lw $t0,32($s3), $s3 = 1000 → 1032. beq at 80012, offset 2 → 80024. j 20000 at 80020 → 0000 : 20000×4 = 80000."])
S[("2022-23", "CSE 209", "12(a)")] = dict(
    q="How does Just-In-Time (JIT) compilation improve the performance of a Java application?",
    s=["Java is compiled to portable bytecodes that the JVM interprets — portable but slow. The JIT compiler finds the **hot** (frequently executed) methods while the program runs and compiles them once to native code for the host machine; later calls run at native speed.",
       "A: The program keeps Java's portability but approaches compiled-code performance; the compile cost is paid only for hot code."])
S[("2022-23", "CSE 209", "12(b)")] = dict(
    q="What is the main difference between static linking and dynamic linking? What are the advantages of using dynamic linking?",
    s=["**Static**: all library routines that may be called are copied into the executable at link time. **Dynamic**: a library routine is linked and loaded only when it is first called.",
       "Advantages of dynamic linking: (1) avoids image bloat from statically linking every (transitively) referenced library; (2) automatically picks up new library versions; (3) one library copy is shared in memory by many programs.",
       "A: Dynamic linking uses lazy linkage — the first call goes through a stub to the dynamic linker, which maps the routine and patches the indirection so later calls jump directly."])
S[("2022-23", "CSE 209", "12(c)(i),(iii)")] = dict(
    q="(i) Write MIPS that creates the 32-bit constant 0010 0000 0000 0001 0100 1001 0010 0100₂ in $t1. (iii) If PC = 0x1FFFF000, can a single branch instruction reach the address equal to that constant? (12(c)(ii) is in the RS tracker.)",
    s=["The constant is 0x2001 4924.",
       "| lui $t1, 0x2001          # 8193: upper 16 bits",
       "| ori $t1, $t1, 0x4924     # 18724: lower 16 bits",
       "(iii) PC + 4 = 0x1FFFF004. Offset = (0x20014924 − 0x1FFFF004)/4 = 0x5648 = 22 088 words ≤ 32 767.",
       "A: **Yes**, a branch can reach it (the target is word-aligned and 22 088 words away, inside ±32 K)."])
S[("2022-23", "CSE 305", "5(a)")] = dict(
    q="Rachel adds lh, lhu, sh and shu for multi-language support. Ross argues she does not need all four. Do you agree with Ross?",
    s=["Stores write only the rightmost 16 bits, so there is nothing to sign- or zero-extend: shu would do exactly what sh does.",
       "For loads the extension matters: lhu (zero-extend) is what characters need; lh (sign-extend) is for signed 16-bit integers.",
       "A: **Agree with Ross** — lh, lhu and sh are enough; shu is redundant."])
S[("2022-23", "CSE 305", "5(c)")] = dict(
    q="Assemble the object files of procedures A (text 0x150, data 0x40: lw $a0,0($gp) needs X; jal 0 needs B) and B (text 0x350, data 0x50: sw $a1,0($gp) needs Y; jal 0 needs A). Find the updated addresses of the first few instructions of the executable. Memory map: text at 0x00400000, static data at 0x10000000, $gp = 0x10008000.",
    s=["Executable: text size 0x150 + 0x350 = 0x4A0, data size 0x40 + 0x50 = 0x90. A's text starts at 0x00400000, B's at 0x00400150; X = 0x10000000, Y = 0x10000040.",
       ("T", ["Address", "Instruction", "Patched value"], [
           ["0x00400000", "lw $a0, 0x8000($gp)", "X − $gp = 0x10000000 − 0x10008000 = −0x8000"],
           ["0x00400004", "jal 0x00400150", "field = 0x00400150 / 4 = 0x100054"],
           ["0x00400150", "sw $a1, 0x8040($gp)", "Y − $gp = 0x10000040 − 0x10008000 = −0x7FC0 = 0x8040"],
           ["0x00400154", "jal 0x00400000", "field = 0x100000"],
           ["0x10000000 / 0x10000040", "(X) / (Y)", "A's data / B's data"]], [22, 28, 50]),
       "A: Linker steps: merge segments, resolve labels (X, Y, A, B), patch location-dependent references."])
S[("2022-23", "CSE 305", "6(b)")] = dict(
    q="What support does the MIPS instruction-set architecture provide for synchronization? Explain with an example.",
    s=["Two processors sharing memory need an **atomic** read-modify-write, otherwise a data race occurs (result depends on access order). MIPS provides **load linked** `ll rt, off(rs)` and **store conditional** `sc rt, off(rs)`: sc stores only if the location was not changed since the ll and returns 1 in rt (success) or 0 (failure).",
       "| try: add $t0, $zero, $s4   # copy exchange value",
       "|      ll  $t1, 0($s1)       # load linked",
       "|      sc  $t0, 0($s1)       # store conditional",
       "|      beq $t0, $zero, try   # retry if the store failed",
       "|      add $s4, $zero, $t1   # old value into $s4",
       "A: This is an atomic swap — usable to acquire a lock."])
S[("2022-23", "CSE 305", "6(c)")] = dict(
    q="MIPS for: if (x > y + 131075) x = 8;  with x in $t1 and y in $t2.",
    s=["131075 = 0x00020003 does not fit a 16-bit immediate, so build it with lui/ori."] + code(A.FRAG_2223_305) +
      ["A: Simulated for four (x, y) pairs — correct."])
S[("2022-23", "CSE 305", "7(b)")] = dict(
    q="Chandler's program uses 40 variables but MIPS has only 32 registers. What does the compiler do?",
    s=["It performs register allocation: the most frequently used variables stay in registers and the rest live in memory (the stack frame). When one is needed it is loaded with lw and written back with sw — **spilling registers**.",
       "A: The compiler spills the least frequently used variables, because each spill costs extra instructions and slower memory accesses."])
S[("2022-23", "CSE 305", "7(c)")] = dict(
    q="Translate int f(int a, int b, int c, int d) { return func(func(a, b), c + d); } into MIPS (use lower-numbered $t registers first). func is int func(int a, int b).",
    s=["c + d must be saved before the first call because $t registers are not preserved by the callee."] + code(A.F_NESTED_2223) +
      ["A: Simulated with a test func — result matches func(func(a,b), c+d)."])
S[("2022-23", "CSE 305", "7(d)")] = dict(
    q="Write about the main difference between static linking and dynamic linking. With the necessary diagrams, explain how dynamically linked libraries (DLLs) are called.",
    s=["Static vs dynamic: see 2022-23 12(b). **Lazy linkage** (how a DLL is called):",
       "1. The first call to a library routine jumps through an **indirection table** to a **stub**.",
       "2. The stub loads the routine ID and jumps to the **dynamic linker/loader**.",
       "3. The linker finds the routine, maps it into memory (the dynamically mapped code) and changes the indirect address.",
       "4. Later calls go through the table straight to the DLL routine — no linker involved.",
       ("IMG", "ch2_64", "Lazy linkage: (a) first call via stub and linker; (b) subsequent calls jump directly (Ch. 2, sl. 64)")])
S[("2021-22", "CSE 305", "5(a)")] = dict(
    q="Which design principle (simplicity favours regularity; smaller is faster; good design demands good compromise; make the common case faster) is behind each: (i) keeping a conditional branch's offset in 16 bits; (ii) keeping 32 registers rather than many more; (iii) consistent instruction format — always three registers for R-type; (iv) multiple instruction formats for flexibility; (v) reduced instruction set, complex instructions (pseudo bgt, bge, move) translated into basic ones.",
    s=[("T", ["", "Principle", "Why"], [
        ["(i)", "Good design demands good compromises (also common case)", "a 16-bit offset keeps the instruction 32 bits; most targets are near"],
        ["(ii)", "Smaller is faster", "a larger register file has longer wires and slower access; 5-bit fields fit 32 bits"],
        ["(iii)", "Simplicity favours regularity", "same hardware path for every arithmetic instruction"],
        ["(iv)", "Good design demands good compromises", "three formats keep every instruction 32 bits; op, rs, rt stay aligned"],
        ["(v)", "Simplicity favours regularity (and common case fast)", "few simple instructions; the assembler expands pseudoinstructions via $at"]], [8, 40, 52])])
S[("2021-22", "CSE 305", "6(a)")] = dict(
    q="MIPS assembly for: int fib(int n) { if (n==0) return 0; else if (n==1) return 1; else return fib(n−1) + fib(n−2); }",
    s=["slti n < 2 handles both base cases (return n). Two recursive calls: fib(n−1) is kept on the stack across the second call."] + code(A.FIB_2122) +
      ["A: Simulated: fib(0..12) = 0, 1, 1, 2, 3, 5, 8, 13, … 144."])
S[("2021-22", "CSE 305", "6(b)(ii)")] = dict(
    q="PC = 0x2000 0000. Is it possible to use a single branch (beq/bne) instruction to set the PC to 0x4000 0000? ((i) about j is in the RS tracker.)",
    s=["Branch target = PC + 4 + offset × 4 with a 16-bit signed offset: reach ±32 K words (±128 KB).",
       "Distance = (0x40000000 − 0x20000004)/4 = 0x07FFFFFF ≈ 134 million words ≫ 32 767.",
       "A: **No.** Use lui $t0, 0x4000 and jr $t0 (a j also fails: top four bits 0010 ≠ 0100)."])
S[("2021-22", "CSE 305", "8(c)")] = dict(
    q="What are the different addressing modes of MIPS? Illustrate the calculation process for each addressing mode.",
    s=[ADDR_TABLE, ("IMG", "ch2_55", "MIPS addressing mode summary (Ch. 2, sl. 55)"),
       "Examples: lw $t0,32($s3) → $s3 + 32; beq at 80012, offset 2 → 80024; j 20000 → (PC+4)[31:28] : 20000×4."])
S[("2020-21", "CSE 305", "11(c)")] = dict(
    q="Write the equivalent efficient sequence of MIPS instructions for: int testFunc(int a, int b, int c) { int i=0, result=0; do { if (i>b) result += c; i++; } while (i<a); return result; }  ($s1 = i, $s2 = result).",
    s=["a, b, c arrive in $a0, $a1, $a2. i > b ⇔ b < i."] + code(A.TESTFUNC_2021) +
      ["A: Simulated on four argument sets — equals the C function."])
S[("2020-21", "CSE 305", "11(d)")] = dict(
    q="Provide an illustrative example of how MIPS follows the design principle \"Good design demands good compromises\".",
    s=["MIPS wants every instruction to be 32 bits (regularity), but lw/sw/addi need a constant plus two registers while add needs three registers. Instead of one format with a tiny constant or longer instructions, MIPS adds the **I-format**: the 16-bit constant reuses the rd + shamt + funct bits.",
       "A: Decoding becomes slightly harder (the opcode decides the format), but all instructions stay 32 bits and op, rs, rt keep the same positions — a good compromise."])
S[("2020-21", "CSE 305", "12(b)")] = dict(
    q="MIPS code L1: bne $t0,$t1,L3; L2: j LX; L3: addi $t0,$t1,1. Opcodes: j = 2, bne = 5, addi = 8; $t0 = 8, $t1 = 9; addresses L1 = 1000, L2 = 1004, L3 = 1008, LX = 131072. Give the format name and field values of each instruction. (Example: add $s1,$s2,$s3 at 0400 is R-format: 0 | 18 | 19 | 17 | 0 | 0.)",
    s=["| 1000 L1: bne $t0,$t1,L3   I-format | 5 | 8 | 9 | 1 |      offset = (1008 − 1004)/4 = 1",
       "| 1004 L2: j LX            J-format | 2 | 32768 |           131072 / 4 = 32768",
       "| 1008 L3: addi $t0,$t1,1  I-format | 8 | 9 | 8 | 1 |      rs = $t1 = 9, rt = $t0 = 8"])
S[("2020-21", "CSE 305", "13(b)")] = dict(
    q="How is the address calculation performed in PC-relative addressing?",
    s=["Target = PC + 4 + sign-extended 16-bit offset × 4. The PC has already been incremented by 4 when the branch executes; the offset counts words, so it is shifted left by 2; a branch adder adds it.",
       "A: Example: beq at 80012 with offset 2 → 80016 + 8 = 80024."])
S[("2020-21", "CSE 305", "13(d)")] = dict(
    q="What are the main differences between x86 architecture and MIPS architecture?",
    s=[("T", ["Feature", "MIPS (RISC)", "x86 (CISC)"], [
        ["Instruction length", "fixed 32 bits, 3 formats", "variable 1–15 bytes"],
        ["Operands", "registers only (load/store)", "register or memory operand"],
        ["Operands per ALU instr.", "3", "2 (destination = a source)"],
        ["Registers", "32 general purpose", "8 (IA-32)"],
        ["Addressing modes", "5", "many (scaled index, segments)"],
        ["Conditions", "slt / beq / bne", "condition codes"],
        ["Implementation", "easy to pipeline, hardwired", "microcoded / translated to micro-ops"],
        ["Code size", "larger", "denser"]], [24, 38, 38])])
S[("2019-20", "CSE 305", "1(c)")] = dict(
    q="What are the advantages of using Dynamically Linked Libraries (DLL) during a C program execution? What is the role of JIT in Java program execution?",
    s=["**DLL advantages**: no image bloat from statically linking every library; new library versions are picked up automatically; one library copy is shared by many programs; a library is loaded only if called.",
       "**JIT**: compiles the bytecodes of hot methods into native code while the program runs, so later calls run at native speed (see 2022-23 12(a))."])
S[("2019-20", "CSE 305", "3(a)")] = dict(
    q="Write equivalent MIPS for: (i) sum = 0; x = 100; while (x >= −5) { sum = sum + x; x = x − 1; }  (ii) if (x > y + 131075) x = 1;  (iii) x = A[131075] + 5;",
    s=["(i) sum = $s0, x = $s1. (ii) x = $s0, y = $s1. (iii) x = $s0, base of A = $s2.",
       "(i)"] + code(A.FRAG1_1920) + ["(ii) 131075 = 0x00020003 needs lui/ori."] + code(A.FRAG2_1920) +
      ["(iii) 131075 × 4 = 524 300 = 0x0008000C does not fit a 16-bit offset."] + code(A.FRAG3_1920) +
      ["A: All three simulated (sum = 5035 for (i); correct branch outcomes for (ii); A[131075] + 5 for (iii))."])
S[("2019-20", "CSE 305", "3(b)")] = dict(
    q="With an appropriate example, briefly describe how pseudoinstructions work. For a critical section where performance matters, is it always a good idea to write the assembly yourself? Justify.",
    s=["Pseudoinstructions are accepted by the assembler but not implemented in hardware; each is translated to one or more real instructions, using register **$at**:",
       "| move $t0,$t1        →  add $t0,$zero,$t1",
       "| blt  $t0,$t1,L      →  slt $at,$t0,$t1 ;  bne $at,$zero,L",
       "A: **Not always a good idea.** Modern compilers schedule code for modern processors better than most programmers, and more hand-written lines mean more errors and lower productivity (fallacy, Ch. 2 sl. 66). Profile first; hand-code only a small hot spot that the compiler measurably handles badly."])
S[("2019-20", "CSE 305", "3(c)")] = dict(
    q="Why does the MIPS multiplication operation always strictly demand three operands? Why has the number of registers in MIPS been restricted to 32?",
    s=["**Three operands** — simplicity favours regularity: every arithmetic instruction has two sources and one destination, so the decoder, register-file ports and datapath are the same for all (mul rd,rs,rt writes the low 32 bits to rd).",
       "**32 registers** — smaller is faster: a bigger register file has longer wires and slower access; more registers would also need wider register fields that do not fit three operands in a 32-bit instruction."])
