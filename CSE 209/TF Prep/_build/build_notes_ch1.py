"""Build CSE209_ART_Ch1_Performance_Notes.docx  (Lessons 1–4).   python -P build_notes_ch1.py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CH1, exam_map, marks_since, new

n = new("Chapter 1 · Computer Abstractions, Technology and Performance", "CSE209_ART_Ch1_Performance_Notes.docx")
n.front_matter(
    contents=[
        ("Exam Map — What the TF Papers Ask", "performance questions and how much they matter"),
        ("Lesson 1 — Computers, Abstraction and the Eight Great Ideas", "classes, PostPC, great ideas, levels, components, ISA/ABI"),
        ("Lesson 2 — Defining Performance: Response Time, Throughput, CPU Time", "relative performance, clocking, clock-rate problems"),
        ("Lesson 3 — CPI, Instruction Mix and the Performance Equation", "IC × CPI × Tc, weighted CPI, 'how much must CPI improve'"),
        ("Lesson 4 — Amdahl's Law, the MIPS Pitfall and Benchmarks", "Amdahl, parallel speedup limit, MIPS/FLOPS, SPEC (textbook)"),
        ("Quick Notes — Performance", "merged revision notes + key diagrams"),
    ],
    source_note="Slide numbers refer to Chapter_01.pdf (Tushar Sir, 28 slides, P&H 5th ed. Chapter 1). "
                "\"TF p.\" is the page in CSE209 ALL TF QUES (TF209).pdf — the same file the RS tracker uses. "
                "SPEC benchmarks are not on the slides; they are added at the end of Lesson 4 (marked textbook) because two older papers ask them.")

# ------------------------------------------------------------------ exam map
n.h1("Exam Map — What the TF Papers Ask")
n.p("Every Tushar-Sir-part question that this deck answers (★ = 2019-20 or later):")
exam_map(n, 1, extra_rows=[
    ["Related (RS tracker)", "—", "Eight great ideas behind given design decisions: 2020-21 Q1, 2016-17 5(a), 2014-15 5(a) — mapped in Lesson 1", "", "L1"],
    ["Outside (this file)", "—", "SPEC ratio / geometric mean: 2016-17 5(b), 2020-21 11(a) — solved in Lesson 4 (textbook)", "", "L4"],
])
n.callout("focus", f"Performance is asked in almost every paper ({marks_since(1)} marks since 2019-20, plus 2023-24 6(a)). "
          "Two question types dominate: (1) the CPU-time / CPI table — 'which machine is faster, by how much, how much must the CPI of class X improve' "
          "(asked 11 times), and (2) Amdahl's law — 'improve one part by n, what is the overall speedup / is k× possible' (6 times). "
          "Learn Lesson 3's recipe and Lesson 4's formula first; they are pure marks. Theory (response time vs throughput, great ideas, MIPS pitfall) is short and repeats word for word.")

# ================================================================== LESSON 1
n.lesson("Lesson 1 — Computers, Abstraction and the Eight Great Ideas", "Slides 1–13 (Chapter 1 §1.1–1.4)")
n.h2("1. Why Computers Keep Changing (sl. 2)")
n.p("Progress in computer technology is underpinned by **Moore's Law**: the number of transistors on a chip doubles about every 18–24 months. "
    "Cheaper, faster hardware makes new applications feasible (computers in cars, cell phones, the human genome project, the Web, search engines), so computers are pervasive.")
n.h2("2. Classes of Computers (sl. 3–4)")
n.table(["Class", "What it is", "Design pressure"], [
    ["Personal computer", "General purpose, runs a variety of software", "Cost / performance trade-off"],
    ["Server", "Network based; small servers up to building-sized", "High capacity, performance, reliability"],
    ["Supercomputer", "High-end scientific and engineering calculations", "Highest capability; tiny share of the market"],
    ["Embedded computer", "Hidden as a component of a system (car, TV, router)", "Stringent power / performance / cost constraints"],
], widths_cm=[3.4, 7.4, 6.4])
n.h2("3. The PostPC Era (sl. 5–6)")
n.bullets([
    "**Personal Mobile Device (PMD)**: battery operated, connected to the Internet, costs hundreds of dollars — smart phones, tablets, electronic glasses. Slide 5's chart: smart-phone sales overtook PC sales around 2011.",
    "**Cloud computing**: Warehouse-Scale Computers (WSC) provide **Software as a Service (SaaS)**. Part of the software runs on the PMD, part in the cloud (Amazon, Google).",
])
n.h2("4. What Determines Performance (sl. 7–8)")
n.table(["Hardware or software component", "How it affects performance"], [
    ["Algorithm", "Number of source-level operations executed"],
    ["Programming language, compiler, architecture", "Number of machine instructions executed per operation"],
    ["Processor and memory system", "How fast instructions are executed"],
    ["I/O system (including the OS)", "How fast I/O operations are executed"],
], widths_cm=[6.5, 10.7])
n.h2("5. Eight Great Ideas in Computer Architecture (sl. 9) ★")
n.table(["Great idea", "Meaning", "Typical example"], [
    ["Design for Moore's Law", "Design for where technology will be when the product ships, not where it is when design starts", "Plan for a chip that will have 2× the transistors in 2 years"],
    ["Use abstraction to simplify design", "Hide lower-level detail behind a simpler model at each level", "ISA hides the implementation; procedures hide their bodies"],
    ["Make the common case fast", "Speed up the frequent case rather than the rare case", "Small immediates in instructions; PC-relative branches"],
    ["Performance via parallelism", "Do several operations at the same time", "Multicore, 31 adders in a fast multiplier, GPUs"],
    ["Performance via pipelining", "Overlap the steps of successive operations (a special case of parallelism)", "5-stage MIPS pipeline; code reordering to avoid load-use stalls"],
    ["Performance via prediction", "Guess and start working; recover if wrong — cheaper on average than waiting", "Branch prediction, prefetching"],
    ["Hierarchy of memories", "Fastest, smallest, most expensive memory at the top; slowest, largest, cheapest at the bottom", "Registers → caches → DRAM → disk; separate I- and D-caches"],
    ["Dependability via redundancy", "Spare components take over when one fails", "RAID disks, ECC memory"],
], widths_cm=[3.8, 7.0, 6.4], font_size=9)
n.callout("note", "The RS tracker holds three 'which great idea is behind this design' questions (2020-21 Q1, 2016-17 5(a), 2014-15 5(a)). "
          "They are answered from this table: single-cycle design replaced (pipelining / make the common case fast), prefetching (prediction), "
          "PC-relative branches (make the common case fast), on-chip caches (hierarchy of memories), 31 adders (parallelism), procedures (abstraction), "
          "code reordering (pipelining), separate data/instruction caches (hierarchy of memories / parallelism), GPUs after the power wall (parallelism).")
n.h2("6. Below Your Program and Levels of Program Code (sl. 10–11)")
n.bullets([
    "**Application software** — written in a high-level language (HLL).",
    "**System software** — the **compiler** translates HLL code to machine code; the **operating system** handles input/output, manages memory and storage, and schedules tasks and shares resources.",
    "**Hardware** — processor, memory, I/O controllers.",
])
n.p("Three levels of program code: **high-level language** (close to the problem domain; gives productivity and portability) → **assembly language** "
    "(textual representation of instructions) → **hardware representation** (binary digits encoding instructions and data). The compiler does the first step, the assembler the second.")
n.figure_from_pdf(CH1, 11, "Figure 1.1 — Levels of program code: C swap → compiler → MIPS assembly → assembler → binary (sl. 11)",
                  clip=(0.6, 0.18, 0.99, 0.93), width_cm=8.0)
n.h2("7. Components of a Computer (sl. 12) ★")
n.p("The same five components exist in every computer — desktop, server or embedded:")
n.table(["Component", "Task"], [
    ["Input", "Brings data into the computer (keyboard, mouse, network adapter, disk read)"],
    ["Output", "Sends results out (display, printer, network adapter, disk write)"],
    ["Memory", "Holds programs while they run and the data they need (DRAM, caches); storage devices (disk, flash) keep them permanently"],
    ["Datapath", "Performs the arithmetic and moves data (ALU, registers) — part of the processor"],
    ["Control", "Tells the datapath, memory and I/O what to do according to the instructions — part of the processor"],
], widths_cm=[3.0, 14.2])
n.p("Processor (CPU) = datapath + control. I/O includes user-interface devices (display, keyboard, mouse), storage devices (hard disk, CD/DVD, flash) and network adapters (for communicating with other computers).")
n.figure_from_pdf(CH1, 12, "Figure 1.2 — The BIG picture: input, output, memory, datapath, control (sl. 12)",
                  clip=(0.03, 0.27, 0.48, 0.83), width_cm=8.5)
n.h2("8. Abstractions: ISA, ABI, Implementation (sl. 13)")
n.bullets([
    "Abstraction helps us deal with complexity by hiding lower-level detail.",
    "**Instruction set architecture (ISA)** — the hardware/software interface: everything a programmer needs to know to write correct machine-language programs (instructions, registers, memory access, I/O).",
    "**Application binary interface (ABI)** — the ISA (user portion) plus the operating-system interface; it defines binary portability across computers.",
    "**Implementation** — the hardware that obeys the ISA. Many implementations (different cost/performance) can share one ISA.",
])
n.exam_approach([
    "Great-ideas questions: name the idea, give one sentence of meaning, then link the given design to it ('…therefore idea X').",
    "Components question: list all five, one task each, and say processor = datapath + control.",
    "Moore's law: state it (transistors double every 18–24 months) and its importance — designers must design for the technology at shipping time.",
])
n.practice("Lesson 1", "(a) Actual — 2020-21 10(a). (b) Actual — 2011-12 1(a). (c) Adapted — RS-tracker 2020-21 Q1. (d) Actual part — 2019-20 1(b) (first half).", [
    "(a) Briefly explain the eight great ideas in computer architecture. (12)",
    "(b) What are the components of a computer? Mention the task of each of these components. (7.5)",
    "(c) Which great idea is behind: (i) code reordering to avoid using a load result in the next instruction; (ii) different caches for data and instructions; (iii) GPUs gaining popularity after CPUs hit the power limit?",
    "(d) What is the importance of Moore's law?",
])
n.solution()
n.answer("(a)", "Write the eight rows of the table in §5 — name, one-line meaning and one example each. That is the full 12-mark answer; draw the small symbol (rocket, pyramid…) only if time permits.")
n.answer("(b)", "Table in §7: input, output, memory, datapath, control — with one task each; processor = datapath + control; I/O covers UI devices, storage and network.")
n.answer("(c)", "(i) Performance via pipelining — reordering removes a load-use stall so the pipeline stays full. "
         "(ii) Hierarchy of memories (split L1 caches let fetch and data access proceed in the same cycle — also parallelism). "
         "(iii) Performance via parallelism — when the clock can no longer rise because of power, performance must come from many cores working together.")
n.answer("(d)", "Moore's law (transistor count doubles every 18–24 months) is the engine behind cheaper and faster hardware. Its importance for a designer is the first great idea: "
         "a design takes years, so architects must design for the transistor budget that will exist when the product ships, and it explains why new applications become feasible every few years.")

# ================================================================== LESSON 2
n.lesson("Lesson 2 — Defining Performance: Response Time, Throughput, CPU Time", "Slides 14–20 (§1.6)")
n.h2("1. What Does 'Best Performance' Mean? (sl. 14)")
n.p("The airplane example: the Concorde has the highest cruising speed, the Boeing 747 the largest passenger capacity and the largest passengers × mph. "
    "'Best' depends on the metric — for a single passenger, speed (time); for an airline, total passengers moved per hour (throughput).")
n.figure_from_pdf(CH1, 14, "Figure 2.1 — Which airplane has the best performance? It depends on the metric (sl. 14)",
                  clip=(0.07, 0.24, 0.98, 0.97), width_cm=10.5)
n.h2("2. Response Time and Throughput (sl. 15) ★")
n.table(["Term", "Definition", "Unit"], [
    ["Response time (execution time, latency)", "How long it takes to do one task, from start to completion", "seconds per task"],
    ["Throughput (bandwidth)", "Total work done per unit time", "tasks / transactions per hour"],
], widths_cm=[4.6, 9.0, 3.6])
n.bullets([
    "**Replacing the processor with a faster one** decreases response time and therefore also increases throughput.",
    "**Adding more processors** (each task still runs on one processor) increases throughput but does not shorten the response time of one task — unless tasks were waiting in a queue, in which case response time also falls.",
    "Chapter 1 focuses on response time.",
])
n.callout("answer", "Response time and throughput are **not synonymous**. Response time is the time to complete one task; throughput is the number of tasks completed per unit time. "
          "Improving one need not improve the other: adding processors raises throughput while each job takes as long as before; a faster processor improves both.")
n.h2("3. Relative Performance (sl. 16)")
n.formula(["Performance = 1 / Execution time",
           "'X is n times faster than Y':  Perf_{X} / Perf_{Y} = Time_{Y} / Time_{X} = n"])
n.p("Example: a program takes 10 s on A and 15 s on B → Time_{B} / Time_{A} = 15/10 = 1.5, so A is 1.5 times faster than B.")
n.h2("4. Elapsed Time vs CPU Time (sl. 17)")
n.bullets([
    "**Elapsed time** = total response time including everything — processing, I/O, OS overhead, idle time. It determines system performance.",
    "**CPU time** = time the CPU spends computing for this job; it excludes I/O waiting and other jobs' shares. CPU time = user CPU time + system CPU time.",
    "Different programs are affected differently by CPU and system performance.",
])
n.h2("5. CPU Clocking (sl. 18)")
n.p("Digital hardware is driven by a constant-rate clock. In every cycle data are transferred and computed, then state is updated at the clock edge.")
n.figure_from_pdf(CH1, 18, "Figure 2.2 — Clock period: data transfer and computation, then state update (sl. 18)",
                  clip=(0.08, 0.32, 0.92, 0.62), width_cm=11.0)
n.formula(["Clock period T_{c} = duration of one cycle   (250 ps = 0.25 ns = 250 × 10^{−12} s)",
           "Clock rate f = 1 / T_{c} = cycles per second   (4.0 GHz = 4000 MHz = 4.0 × 10^{9} Hz)"])
n.h2("6. CPU Time (sl. 19–20) ★")
n.formula(["CPU time = CPU clock cycles × Clock cycle time = CPU clock cycles / Clock rate"])
n.p("Performance improves by reducing the number of clock cycles or by increasing the clock rate. The hardware designer must often trade one against the other: "
    "a faster clock may need more (simpler) cycles per task.")
n.h3("Worked example (sl. 20)")
n.p("Computer A: 2 GHz clock, 10 s CPU time. Design B to run in 6 s; B can have a faster clock but then needs 1.2 × the clock cycles. How fast must B's clock be?")
n.code(["Clock cycles_A = CPU time_A × Clock rate_A = 10 s × 2 GHz = 20 × 10^9",
        "Clock rate_B   = Clock cycles_B / CPU time_B = 1.2 × 20 × 10^9 / 6 s",
        "               = 24 × 10^9 / 6 = 4 × 10^9 Hz = 4 GHz"])
n.callout("trap", "The 1.2 multiplies the number of **cycles**, not the time. First get cycles_A from A's time and clock, then scale, then divide by B's target time.")
n.exam_approach([
    "Write the formula you use first: CPU time = cycles / clock rate.",
    "Find the unknown machine's cycle count from the known one (× the given factor).",
    "Divide by the target time to get the clock rate; state the answer in GHz.",
    "For 'which is faster' compare times (or IPS = clock rate / CPI), and give the ratio 'X is n times faster'.",
])
n.practice("Lesson 2", "(a) Actual — 2023-24 6(a). (b) Actual — 2015-16 1(a). (c) Actual — 2022-23 (CSE 305) 7(a). (d) Actual — 2013-14 5(a).", [
    "(a) Our favorite program runs in 10 s on computer A, which has a 4 GHz clock. Computer B must run it in 6 s; a substantial clock-rate increase is possible but makes B need 1.2 times as many clock cycles as A. What clock rate should we target? (13)",
    "(b) P1: 3 GHz, CPI 1.5; P2: 2.5 GHz, CPI 1.0; P3: 4.0 GHz, CPI 2.2. (i) Highest performance in instructions per second? (ii) Each runs a program in 10 s — number of cycles and instructions? (iii) We reduce the execution time by 30 % but the CPI rises by 20 %. What clock rate is needed? (10)",
    "(c) Define response time and throughput. Are these two terms synonymous? (5)",
    "(d) What is Moore's law? What do you mean by response time and throughput? (6)",
])
n.solution()
n.answer("(a)", "")
n.code(["Cycles_A = 10 s × 4 × 10^9 = 40 × 10^9 cycles",
        "Cycles_B = 1.2 × 40 × 10^9 = 48 × 10^9 cycles",
        "Clock_B  = 48 × 10^9 / 6 s = 8 × 10^9 Hz"])
n.formula("Target clock rate for B = 8 GHz (2× A's clock for 1.67× the speed)")
n.answer("(b)", "Instructions per second = clock rate / CPI.")
n.table(["", "P1", "P2", "P3"], [
    ["(i) IPS = f / CPI", "3/1.5 = 2.0 × 10^9", "2.5/1.0 = 2.5 × 10^9", "4/2.2 = 1.82 × 10^9"],
    ["(ii) cycles = 10 s × f", "3.0 × 10^10", "2.5 × 10^10", "4.0 × 10^10"],
    ["(ii) instructions = cycles / CPI", "2.0 × 10^10", "2.5 × 10^10", "1.82 × 10^10"],
    ["(iii) new f = f × 1.2 / 0.7", "5.14 GHz", "4.29 GHz", "6.86 GHz"],
], widths_cm=[5.2, 4.0, 4.0, 4.0])
n.p("(i) **P2** has the highest performance (2.5 × 10^9 instructions/s). "
    "(iii) Time = IC × CPI / f. New time = 0.7 × old, new CPI = 1.2 × old, IC unchanged → 0.7 = 1.2 / (f_{new}/f_{old}) → f_{new} = (1.2/0.7) f_{old} = 1.714 f_{old}.")
n.answer("(c)", "Model answer in the EXAM-READY box of §2: not synonymous; define both; a faster CPU improves both, extra processors improve only throughput.")
n.answer("(d)", "Moore's law: the number of transistors on an integrated circuit doubles roughly every 18–24 months (Lesson 1). Response time and throughput: §2.")

# ================================================================== LESSON 3
n.lesson("Lesson 3 — CPI, Instruction Mix and the Performance Equation", "Slides 21–25 (§1.6)")
n.callout("focus", "The most-asked numerical type of the ART part: 2022-23 6(d), 2021-22 8(a), 2020-21 12(a), 2019-20 1(a), 2018-19 7(b), 2017-18 5(a), 2016-17 5(c), 2015-16 1(b)–(c), 2014-15 5(b), 2013-14 5(b), 2011-12 1(c). Every one is solved below.")
n.h2("1. Instruction Count and CPI (sl. 21)")
n.formula(["Clock cycles = Instruction count × Cycles per instruction",
           "CPU time = IC × CPI × T_{c} = IC × CPI / Clock rate"])
n.bullets([
    "**Instruction count (IC)** is determined by the program, the ISA and the compiler.",
    "**Average CPI** is determined by the CPU hardware. If instructions have different CPIs, the average CPI depends on the instruction mix.",
])
n.h2("2. CPI Example (sl. 22)")
n.p("A: cycle time 250 ps, CPI 2.0; B: cycle time 500 ps, CPI 1.2; same ISA (same IC = I). Which is faster, and by how much?")
n.code(["CPU time_A = I × 2.0 × 250 ps = I × 500 ps",
        "CPU time_B = I × 1.2 × 500 ps = I × 600 ps",
        "Time_B / Time_A = 600 / 500 = 1.2   →  A is 1.2 times faster"])
n.h2("3. CPI in More Detail — Weighted Average (sl. 23)")
n.formula(["Clock cycles = Σ_{i} (CPI_{i} × IC_{i})",
           "CPI = Clock cycles / IC = Σ_{i} CPI_{i} × (IC_{i} / IC)      (IC_{i}/IC = relative frequency)"])
n.h2("4. Worked Example: Two Code Sequences (sl. 24)")
n.table(["Class", "A", "B", "C"], [["CPI for class", "1", "2", "3"], ["IC in sequence 1", "2", "1", "2"], ["IC in sequence 2", "4", "1", "1"]],
        widths_cm=[5.0, 2.5, 2.5, 2.5])
n.code(["Sequence 1: IC = 5, cycles = 2×1 + 1×2 + 2×3 = 10, CPI = 10/5 = 2.0",
        "Sequence 2: IC = 6, cycles = 4×1 + 1×2 + 1×3 = 9,  CPI = 9/6  = 1.5",
        "Sequence 2 executes MORE instructions but is FASTER (9 < 10 cycles)."])
n.callout("trap", "Never compare machines by IC alone or by CPI alone. Only the product IC × CPI × T_{c} (time) decides.")
n.h2("5. Performance Summary — The BIG Picture (sl. 25)")
n.formula("CPU time = (Instructions / Program) × (Clock cycles / Instruction) × (Seconds / Clock cycle)")
n.table(["Factor", "Affects"], [
    ["Algorithm", "IC, possibly CPI"], ["Programming language", "IC, CPI"], ["Compiler", "IC, CPI"],
    ["Instruction set architecture", "IC, CPI, T_{c}"],
], widths_cm=[7.0, 10.2])
n.h2("6. The 'How Much Must CPI Improve?' Recipe")
n.numbered([
    "Compute total cycles = Σ IC_{i} × CPI_{i} (keep 10^{6} as a common unit).",
    "Target cycles = old cycles / k for 'k times faster' (same clock).",
    "Cycles that the improved class may use = target − (cycles of all other classes).",
    "If that number is ≤ 0 → **impossible**, even with CPI = 0 for that class. Otherwise new CPI = allowed cycles / IC of the class; improvement factor = old CPI / new CPI.",
])
n.exam_approach([
    "Make a table: class | IC | CPI | IC × CPI. Sum the last column.",
    "Time = cycles / clock rate. With different clocks compare times, not cycles.",
    "Average CPI = total cycles / total IC.",
    "For CPI-improvement questions use the recipe in §6 and say 'impossible' with the negative number as proof.",
    "For percentage changes multiply each CPI by (1 ± p) before summing; report new time, change in % and speedup.",
])
n.practice("Lesson 3", "(a) Actual — 2018-19 7(b) (same table as 2014-15 5(b), 2 GHz). (b) Actual — 2016-17 5(c). (c) Actual — 2022-23 (CSE 305) 6(d). "
           "(d) Actual — 2021-22 8(a). (e) Actual — 2019-20 1(a). (f) Actual — 2017-18 5(a).", [
    "(a) A 4 GHz processor runs a program with FP / INT / L/S / BRANCH = 160 / 110 / 10 / 16 million instructions and CPI 2 / 1 / 5 / 2. "
    "(i) Execution time? (ii) How much must the CPI of FP improve for the program to run 2× faster? (iii) Of L/S? (iv) Change in time if CPI of INT and BRANCH rise 15 % and CPI of FP and L/S fall 20 %? (20)",
    "(b) 3 GHz; FP / INT / L/S / BRANCH = 40 / 80 / 90 / 15 million, CPI 1 / 1 / 3 / 2. (i) Execution time. (ii) FP CPI for 2×? (iii) Change if CPI of INT and FP rise 20 % and of L/S and Branch fall 10 %. (15)",
    "(c) P1: 2.7 GHz, CPI (A, B, C, D) = 2, 1, 3, 2; P2: 3.2 GHz, CPI 2, 3, 2, 3. 1.2 × 10^6 instructions: 20 % A, 25 % B, 40 % C, 15 % D. (i) Clock cycles on each. (ii) Which is faster, by how much? (iii) 40 % of the code is improved — maximum possible improvement factor? (15)",
    "(d) 200,000 instructions: 25 % A, 60 % B, 15 % C. P1 2.7 GHz, CPI 3/3/2; P2 3.5 GHz, CPI 2/4/1. (i) Total cycles, (ii) execution times, which is faster, (iii) CPI improvement of class C for 2× in the better one. (11)",
    "(e) Logs: on A (2 GHz) Program 1 uses Mul 4, Mul 4, Div 5, Div 5, Add 2 cycles; on B (2.5 GHz) Mul 5, Mul 5, Div 6, Div 6, Add 3 cycles (other entries belong to other programs or OS I/O). Compare the performance on Program 1. (15)",
    "(f) CPIs of A, B, C = 1.2, 2, 2.5. P1 has 40, 10, 16 and P2 12, 13, 40 instructions of A, B, C. (i) Which executes faster, by how much? (ii) CPI improvement of B for P1 to run 2× faster? (15)",
])
n.solution()
n.answer("(a)", "")
n.table(["Class", "IC (×10^6)", "CPI", "Cycles (×10^6)", "(iv) new CPI", "(iv) cycles"], [
    ["FP", "160", "2", "320", "1.6", "256"], ["INT", "110", "1", "110", "1.15", "126.5"], ["L/S", "10", "5", "50", "4.0", "40"],
    ["BRANCH", "16", "2", "32", "2.3", "36.8"], ["Total", "296", "", "512", "", "459.3"],
], widths_cm=[2.4, 2.6, 1.6, 3.2, 2.8, 2.8], first_col_bold=True)
n.code(["(i)   T = 512 × 10^6 / 4 × 10^9 = 0.128 s              (2014-15 5(b) at 2 GHz: 0.256 s)",
        "(ii)  2× faster → 256 × 10^6 cycles. Others use 110 + 50 + 32 = 192 → FP may use 64",
        "      CPI_FP = 64 / 160 = 0.4  → FP CPI must improve 2 / 0.4 = 5 times",
        "(iii) Others use 320 + 110 + 32 = 462 > 256 → impossible: even CPI_LS = 0 is not enough",
        "(iv)  T = 459.3 × 10^6 / 4 × 10^9 = 0.1148 s → 10.3 % less time (speedup 1.115)"])
n.answer("(b)", "Cycles = 40×1 + 80×1 + 90×3 + 15×2 = 420 × 10^6 → T = 420 × 10^6 / 3 × 10^9 = **0.14 s**. "
         "(ii) 2× → 210 × 10^6 cycles; the non-FP classes alone need 80 + 270 + 30 = 380 × 10^6 > 210 → **impossible**. "
         "(iii) New cycles = 40×1.2 + 80×1.2 + 90×2.7 + 15×1.8 = 48 + 96 + 243 + 27 = 414 × 10^6 → T = 0.138 s: **improved by 1.43 %** (speedup 1.014).")
n.answer("(c)", "IC: A 240,000; B 300,000; C 480,000; D 180,000.")
n.code(["P1 cycles = 240k×2 + 300k×1 + 480k×3 + 180k×2 = 2.58 × 10^6   → T1 = 2.58e6 / 2.7e9 = 0.956 ms",
        "P2 cycles = 240k×2 + 300k×3 + 480k×2 + 180k×3 = 2.88 × 10^6   → T2 = 2.88e6 / 3.2e9 = 0.900 ms",
        "P2 is faster: 0.956 / 0.900 = 1.06 times",
        "(iii) Amdahl: if 40 % of the time is improved infinitely, Speedup_max = 1 / (1 − 0.4) = 1.67"])
n.answer("(d)", "A = 50,000, B = 120,000, C = 30,000 instructions.")
n.code(["P1 cycles = 50k×3 + 120k×3 + 30k×2 = 570,000 → T = 570,000 / 2.7 GHz = 211.1 µs",
        "P2 cycles = 50k×2 + 120k×4 + 30k×1 = 610,000 → T = 610,000 / 3.5 GHz = 174.3 µs",
        "P2 is faster by 211.1 / 174.3 = 1.21",
        "(iii) 2× in P2 → 305,000 cycles; A and B alone need 100k + 480k = 580k > 305k → impossible"])
n.answer("(e)", "CPU time counts only Program 1's own operations — ignore the other programs and the OS I/O overhead lines.")
n.code(["A: cycles = 4 + 4 + 5 + 5 + 2 = 20 → T_A = 20 / 2 GHz   = 10 ns",
        "B: cycles = 5 + 5 + 6 + 6 + 3 = 25 → T_B = 25 / 2.5 GHz = 10 ns",
        "Performance_A / Performance_B = T_B / T_A = 1 → equal performance on Program 1"])
n.callout("trap", "2019-20 1(a) is built to trap you: B has the faster clock but needs more cycles; and adding the I/O lines (elapsed time) would give a different answer. CPU time is the right measure for 'performance of the processor on Program 1' — say so.")
n.answer("(f)", "Cycles P1 = 40×1.2 + 10×2 + 16×2.5 = 48 + 20 + 40 = 108; P2 = 12×1.2 + 13×2 + 40×2.5 = 14.4 + 26 + 100 = 140.4. "
         "Same machine (same clock) → P1 is faster by 140.4 / 108 = **1.3 times**. (ii) P1 2× faster → 54 cycles; A and C alone use 88 → **impossible**.")
n.h2("More Solved TF Questions — Lesson 3")
n.answer("2013-14 5(b)", "200 instructions: A 20, B 40, C 100, D 40. P1 (3 GHz, CPI 1/2/3/4): 20 + 80 + 300 + 160 = **560 cycles**, CPI = 2.8, T = 560 / 3 GHz = 186.7 ns. "
         "P2 (2 GHz, CPI 2): **400 cycles**, CPI = 2.0, T = 200 ns. P1 is faster by 200 / 186.7 = 1.07 (fewer cycles do not win alone — P2's clock is slower).")
n.answer("2015-16 1(b)", "Cycles = 500×1 + 50×5 + 100×5 + 50×2 = 1350; IC = 700. (i) T = 1350 / 4 GHz = **337.5 ns**. (ii) CPI = 1350/700 = **1.93**. "
         "(iii) Loads halved → 50 loads: cycles = 1100, IC = 650 → CPI = 1.69; speedup = 1350/1100 = **1.23**.")
n.answer("2015-16 1(c)", "Per processor: arithmetic and load/store counts are divided by 0.7p; branches stay 256 M. Clock 2 GHz.")
n.table(["p", "Arith (×10^9)", "L/S (×10^9)", "Cycles = A×1 + LS×12 + 0.256×5", "Time", "Speedup", "(ii) CPI_A = 2"], [
    ["1", "2.560", "1.280", "2.56 + 15.36 + 1.28 = 19.2 × 10^9", "9.60 s", "1", "10.88 s"],
    ["2", "1.829", "0.914", "1.829 + 10.971 + 1.28 = 14.08 × 10^9", "7.04 s", "1.36", "7.95 s"],
    ["4", "0.914", "0.457", "0.914 + 5.486 + 1.28 = 7.68 × 10^9", "3.84 s", "2.50", "4.30 s"],
], widths_cm=[0.8, 2.0, 1.9, 5.4, 1.6, 1.6, 2.4], font_size=8.5)
n.p("(iii) One processor must finish in 3.84 s = 7.68 × 10^9 cycles: 2.56 + 1.28 × CPI_{LS} + 1.28 = 7.68 → CPI_{LS} = **3** (reduce from 12 to 3, i.e. by 75 %).")
n.answer("2020-21 12(a)", "Program A: IC = 2+1+4+2 = 9, cycles = 2×3 + 1×1 + 4×2 + 2×4 = 23 → CPI = 2.56. Program B: IC = 10, cycles = 3×3 + 2×1 + 3×2 + 2×4 = 25 → CPI = 2.50. **Program A** has the higher average CPI.")
n.answer("2011-12 1(c)", "Exactly slide 22: A takes I × 2.0 × 250 ps = 500I ps, B takes I × 1.2 × 500 ps = 600I ps → **A is 1.2 times faster**.")

# ================================================================== LESSON 4
n.lesson("Lesson 4 — Amdahl's Law, the MIPS Pitfall and Benchmarks", "Slides 26–28 (§1.9–1.10) + SPEC (textbook §1.10)")
n.h2("1. Pitfall: Amdahl's Law (sl. 26) ★")
n.p("Pitfall: improving one aspect of a computer and expecting a proportional improvement in overall performance.")
n.formula(["T_{improved} = T_{affected} / improvement factor + T_{unaffected}",
           "Speedup = 1 / ((1 − f) + f / n)        f = fraction of time improved, n = factor",
           "Upper limit (n → ∞):  Speedup_{max} = 1 / (1 − f)"])
n.h3("Slide example")
n.code(["Multiply takes 80 s of a 100 s program. How much must multiply improve for 5× overall?",
        "Target 100/5 = 20 s:   20 = 80/n + 20   →  80/n = 0   →  can't be done!",
        "For 4× overall (2013-14 5(c), with division instead of multiply):",
        "   25 = 80/n + 20  →  80/n = 5  →  n = 16   (division must become 16× faster)"])
n.p("Corollary: **make the common case fast** — the unaffected part sets the ceiling.")
n.callout("answer", "2019-20 1(b): 'To increase overall performance by x, identify the most important aspect and improve it by x' — **Disagree**. "
          "If that aspect takes a fraction f < 1 of the time, Speedup = 1/((1 − f) + f/x), which is less than x for every x > 1 because the unimproved part (1 − f) still takes the same time. "
          "Example: f = 0.8, x = 4 → Speedup = 1/(0.2 + 0.2) = 2.5, not 4; and for x = 5 the overall limit is only 1/0.2 = 5 as x → ∞. Overall speedup x is reached only if f = 1.")
n.h3("Amdahl and parallel processors")
n.p("With p processors the parallel fraction f runs p times faster: Speedup = 1 / ((1 − f) + f/p). The serial fraction limits the speedup to 1/(1 − f) no matter how many cores are added.")
n.h2("2. Pitfall: MIPS as a Performance Metric (sl. 27) ★")
n.formula(["MIPS = Instruction count / (Execution time × 10^{6}) = Clock rate / (CPI × 10^{6})"])
n.p("MIPS (millions of instructions per second) does not account for:")
n.bullets([
    "differences in ISAs between computers (one machine may need more instructions for the same work);",
    "differences in complexity between instructions (a 'simple' instruction counts the same as a complex one);",
    "CPI varies between programs on the same CPU, so one machine has no single MIPS rating.",
])
n.p("Hence a machine with a higher MIPS rating can be slower. Execution time is the only reliable measure.")
n.callout("note", "FLOPS (floating-point operations per second) has the same weakness as MIPS: it ignores integer, memory and branch work and depends on the FP instruction set. "
          "It is misleading as a general metric, but it is a fair measure of one part — the FP unit — or of FP-dominated programs (scientific computing, GPUs).")
n.h2("3. Concluding Remarks (sl. 28)")
n.bullets([
    "Cost/performance is improving because of underlying technology development.",
    "Hierarchical layers of abstraction exist in both hardware and software.",
    "The ISA is the hardware/software interface.",
    "**Execution time is the best performance measure.**",
    "Power is a limiting factor — so parallelism is now used to improve performance.",
])
n.h2("4. Benchmarks: SPEC Ratio (textbook §1.10 — not on the slides)")
n.p("SPEC CPU benchmarks report, for each program i, SPECratio_{i} = Reference time_{i} / Execution time_{i}. The overall figure is the **geometric mean**: "
    "(Π SPECratio_{i})^{1/n}. The geometric mean gives the same ranking whichever machine is used as the reference.")
n.exam_approach([
    "Amdahl: write T_{new} = T_{aff}/n + T_{unaff}; solve for the unknown; if it needs 0 or negative time → 'impossible'.",
    "Parallel speedup: S = 1/((1 − f) + f/p); limit 1/(1 − f) answers 'is k× possible?'.",
    "MIPS rating: compute MIPS = f/(CPI × 10^{6}) AND execution time; show they rank the machines differently.",
    "SPEC: ratio per program, then geometric mean; for a missing time solve GM^{n} = Π ratios.",
])
n.practice("Lesson 4", "(a) Actual — 2021-22 5(b). (b) Actual — 2012-13 6(a). (c) Actual — 2011-12 1(d). (d) Actual — 2015-16 2(a) = 2013-14 5(d). "
           "(e) Actual — 2021-22 7(b). (f) Actual — 2016-17 5(b) and 2020-21 11(a) (Outside-Notes questions, textbook).", [
    "(a) 2 % of a program's runtime is not parallelizable. It runs on 24 cores with no overheads. (i) Parallel speedup? (ii) Is it possible to make the program 60 times faster? (10)",
    "(b) CPU times: FP 50 s, INT 80 s, L/S 50 s, Branch 30 s (total 210 s). (i) % total reduction if FP time drops 20 %? (ii) If only INT improves, by how much must INT time fall for a 20 % total reduction? (iii) Can branch alone give 20 %? (9)",
    "(c) A program runs 10 s and spends 50 % in FP instructions; the FP unit becomes 5× faster. Speedup? (6)",
    "(d) A: 10 billion instructions, 4 GHz, CPI 1. B: 8 billion, 4 GHz, CPI 1.1. (i) Which has the higher MIPS rating? (ii) Which is faster? (5/6)",
    "(e) Your partner says FLOPS is misleading for general performance but useful for a specific part or type of processor. Agree or disagree? (16)",
    "(f) (i) Find the SPEC ratio of the server from the 12-program SPECint2006 table. (ii) SPECBM101: geometric mean 28.74; times of programs 2–6 are 527, 586, 109, 470, 275 s (refs 10490, 12100, 20720, 7020, 6900); ref of program 1 is 9770 s. Execution time of program 1?",
])
n.solution()
n.answer("(a)", "(i) S = 1 / (0.02 + 0.98/24) = 1 / (0.02 + 0.04083) = **16.44**. (ii) Limit = 1/0.02 = **50** < 60 → impossible with this program, however many cores. "
         "It could be reached only by shrinking the serial part (re-designing the algorithm so that < 1/60 ≈ 1.67 % is serial) or by making the serial part itself faster (a faster core).")
n.answer("(b)", "(i) FP saves 0.2 × 50 = 10 s → 200 s: total reduced by 10/210 = **4.76 %**. (ii) 20 % of 210 = 42 s must come from INT: 42/80 = **52.5 %** reduction of INT time. "
         "(iii) Branch takes only 30 s < 42 s → **no**, even if branch time became zero.")
n.answer("(c)", "T_{new} = 5/5 + 5 = 6 s → speedup = 10/6 = **1.67**.")
n.answer("(d)", "MIPS_A = 4 × 10^9 / (1 × 10^6) = 4000; MIPS_B = 4 × 10^9 / (1.1 × 10^6) = 3636 → **A has the higher MIPS**. "
         "Time_A = 10 × 10^9 × 1 / 4 × 10^9 = 2.5 s; Time_B = 8 × 10^9 × 1.1 / 4 × 10^9 = 2.2 s → **B is faster** (1.14×). MIPS ranks them the wrong way because B executes fewer instructions.")
n.answer("(e)", "**Agree.** FLOPS counts only floating-point operations per second, so (1) programs dominated by integer, memory or branch work are not measured at all; "
         "(2) different ISAs offer different FP operations (a fused multiply-add counts as one or two), so FLOPS of different machines are not comparable; "
         "(3) like MIPS (sl. 27), FLOPS varies from program to program on the same machine. Execution time of real programs is the only general measure. "
         "But for a specific part — the FP unit or a GPU — or for FP-heavy workloads (matrix multiply, scientific simulation, deep learning), peak and sustained FLOPS directly tell how fast that part does its job, so it is a useful specialised metric.")
n.answer("(f)", "(i) Ratios: perlbench 41.40, bzip2 25.73, gcc 38.70, mcf 68.57, gobmk 31.13, hmmer 88.86, sjeng 35.59, libquantum 10360, h264ref 58.39, "
         "omnetpp 52.52, astar 36.00, xalancbmk 80.23 → geometric mean = (Π ratios)^{1/12} = **73.7**. "
         "(ii) Ratios 2–6: 19.91, 20.65, 190.09, 14.94, 25.09. 28.74^{6} = ratio_{1} × Π(others) → ratio_{1} = 19.25 → T_{1} = 9770 / 19.25 = **507.6 s**.")

# ------------------------------------------------------------------ quick notes
n.quick_notes("Quick Notes — Performance", "Revision points for Lessons 1–4.", [
    ("L1 · Abstraction and Great Ideas", [
        "Classes: PC (cost/perf), server (capacity, reliability), supercomputer (highest capability), embedded (power/perf/cost). PostPC: PMD + cloud (WSC, SaaS).",
        "Performance factors: algorithm → ops; language/compiler/ISA → instructions per op; processor+memory → speed of instructions; I/O+OS → I/O speed.",
        "8 ideas: Moore's law · abstraction · common case fast · parallelism · pipelining · prediction · memory hierarchy · redundancy.",
        "Five components: input, output, memory, datapath, control (CPU = datapath + control).",
        "ISA = HW/SW interface; ABI = ISA + OS interface; implementation = hardware obeying the ISA.",
    ]),
    ("L2 · Defining Performance", [
        "Response time = time for one task; throughput = tasks per unit time — not synonymous.",
        "Perf = 1/T; X is n× faster than Y ⇔ T_{Y} / T_{X} = n. CPU time (user + system) excludes I/O and other jobs.",
        "CPU time = cycles × T_{c} = cycles / f. Example: A 4 GHz 10 s, B 6 s with 1.2× cycles → 8 GHz.",
    ]),
    ("L3 · CPI and the Performance Equation", [
        "CPU time = IC × CPI × T_{c}; cycles = Σ CPI_{i} × IC_{i}; CPI = cycles / IC.",
        "IC: program, ISA, compiler. CPI: hardware + mix. T_{c}: hardware (ISA affects all three).",
        "'k× faster by improving class X': allowed cycles = old/k − others; ≤ 0 → impossible; else CPI_{new} = allowed / IC_{X}.",
        "2019-20 1(a): A 20 cycles/2 GHz = 10 ns, B 25/2.5 GHz = 10 ns → equal.",
    ]),
    ("L4 · Amdahl, MIPS, SPEC", [
        "T_{new} = T_{aff}/n + T_{unaff}; S = 1/((1−f) + f/n); S_{max} = 1/(1−f). 80 s of 100 s: 5× impossible, 4× needs 16×.",
        "2 % serial on 24 cores → 16.44; limit 50 → 60× impossible.",
        "MIPS = f/(CPI × 10^6): ignores ISA differences, instruction complexity, program variation. FLOPS has the same flaws but is fine for FP units.",
        "SPECratio = ref/exec; overall = geometric mean.",
    ]),
], diagrams=[
    (CH1, 12, "Components of a computer — the BIG picture (sl. 12) — same as Fig. 1.2", (0.03, 0.27, 0.48, 0.83), 8.0),
])
print(n.save())
