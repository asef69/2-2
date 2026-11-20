"""General step-by-step method sheet: pipeline / data hazard / stall-cycle maths and memory-hierarchy maths.
Every worked example is computed by sims209.py (so the numbers in the PDF are checked, not typed by hand)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
                                KeepTogether, PageBreak)
from sims209 import I, pipe, cache, tlb, predictor

PREP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(PREP, "CSE209_General_Steps_Pipeline_and_Memory.pdf")
F = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("S", F + r"\segoeui.ttf"))
pdfmetrics.registerFont(TTFont("S-B", F + r"\segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("S-I", F + r"\segoeuii.ttf"))
pdfmetrics.registerFont(TTFont("S-BI", F + r"\segoeuiz.ttf"))
pdfmetrics.registerFont(TTFont("C", F + r"\consola.ttf"))
pdfmetrics.registerFont(TTFont("C-B", F + r"\consolab.ttf"))
pdfmetrics.registerFontFamily("S", normal="S", bold="S-B", italic="S-I", boldItalic="S-BI")
pdfmetrics.registerFontFamily("C", normal="C", bold="C-B", italic="C", boldItalic="C-B")

NAVY = colors.Color(0.12, 0.22, 0.39)
PALE = colors.Color(0.88, 0.92, 0.98)
YEL = colors.Color(1, 0.97, 0.84)
REDP = colors.Color(0.99, 0.91, 0.91)
GRN = colors.Color(0.9, 0.97, 0.9)
GREY = colors.Color(0.45, 0.45, 0.45)

body = ParagraphStyle("body", fontName="S", fontSize=9.2, leading=12.8, spaceAfter=3)
small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=11, textColor=GREY)
cell = ParagraphStyle("cell", parent=body, fontSize=8.4, leading=11, spaceAfter=0)
cellb = ParagraphStyle("cellb", parent=cell, fontName="S-B")
code = ParagraphStyle("code", parent=body, fontName="C", fontSize=8.2, leading=10.5, spaceAfter=0)
h1 = ParagraphStyle("h1", fontName="S-B", fontSize=15, leading=19, textColor=colors.white)
h2 = ParagraphStyle("h2", fontName="S-B", fontSize=11.2, leading=14, textColor=NAVY, spaceBefore=7, spaceAfter=3, keepWithNext=1)
h2n = ParagraphStyle("h2n", parent=h2, keepWithNext=0)
h3 = ParagraphStyle("h3", fontName="S-B", fontSize=9.6, leading=12.5, textColor=NAVY, spaceBefore=4, spaceAfter=2, keepWithNext=1)
bul = ParagraphStyle("bul", parent=body, leftIndent=12, bulletIndent=2, spaceAfter=1.5)
W = A4[0] - 3.2 * cm


def P(t, s=body):
    return Paragraph(t, s)


def bullets(items, style=bul):
    return [Paragraph(t, style, bulletText="•") for t in items]


def steps(items):
    return [Paragraph(t, bul, bulletText=f"{i}.") for i, t in enumerate(items, 1)]


def box(title, flow, bg=PALE, edge=NAVY):
    inner = [Paragraph(f"<b>{title}</b>", ParagraphStyle("bt", parent=body, textColor=edge, spaceAfter=2))] if title else []
    inner += flow if isinstance(flow, list) else [flow]
    t = Table([[f] for f in inner], colWidths=[W], splitByRow=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), 0.8, edge),
                           ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                           ("TOPPADDING", (0, 0), (-1, 0), 5), ("BOTTOMPADDING", (0, -1), (-1, -1), 5)]))
    return t


def banner(text):
    t = Table([[Paragraph(text, h1)]], colWidths=[W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("LEFTPADDING", (0, 0), (-1, -1), 9),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return t


def grid(head, rows, widths, hdr=NAVY, zebra=True, extra=(), tw=None):
    data = [[Paragraph(f"<b>{h}</b>", ParagraphStyle("th", parent=cell, textColor=colors.white)) for h in head]]
    for r in rows:
        data.append([c if not isinstance(c, str) else Paragraph(c, cell) for c in r])
    t = Table(data, colWidths=[w * (tw or W) for w in widths], repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), hdr), ("GRID", (0, 0), (-1, -1), 0.4, colors.Color(0.7, 0.74, 0.8)),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0:
                st.append(("BACKGROUND", (0, i), (-1, i), colors.Color(0.95, 0.96, 0.98)))
    t.setStyle(TableStyle(st + list(extra)))
    return t


def asm(lines):
    t = Table([[Paragraph(l.replace(" ", "&nbsp;"), code)] for l in lines], colWidths=[W * 0.5])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.Color(0.96, 0.96, 0.96)), ("BOX", (0, 0), (-1, -1), 0.4, GREY),
                           ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    return t


# ---------------------------------------------------------------- pipeline diagram
STG = {"IF": colors.Color(0.80, 0.90, 1), "ID": colors.Color(0.82, 0.95, 0.82), "EX": colors.Color(1, 0.93, 0.75),
       "MEM": colors.Color(0.95, 0.85, 0.95), "WB": colors.Color(0.86, 0.86, 0.86)}


def diagram(res, show=None, flushed=True):
    res = res[:show] if show else res
    ncyc = res[-1]["ex"] + 2
    cw = min(0.62 * cm, (W - 4.4 * cm) / ncyc)
    head = [""] + [str(c) for c in range(1, ncyc + 1)]
    data = [[Paragraph(f"<b>{h}</b>", ParagraphStyle("d0", fontName="S-B", fontSize=6.8, alignment=1)) for h in head]]
    sty = [("FONTSIZE", (0, 0), (-1, -1), 6.5), ("GRID", (1, 0), (-1, -1), 0.3, colors.Color(0.75, 0.75, 0.75)),
           ("TOPPADDING", (0, 0), (-1, -1), 1.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2), ("LEFTPADDING", (0, 0), (-1, -1), 1),
           ("RIGHTPADDING", (0, 0), (-1, -1), 1), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]
    cs = ParagraphStyle("dc", fontName="S-B", fontSize=6.3, alignment=1, leading=7)
    rows = []
    for k, r in enumerate(res):
        row = [Paragraph(r["txt"].replace(" ", "&nbsp;") + (f"&nbsp;&nbsp;<font color='#b00000'>({r['stalls']} stall)</font>" if r["stalls"] else ""),
                         ParagraphStyle("dl", fontName="C", fontSize=6.8, leading=8))] + [""] * ncyc
        rowi = len(data) + len(rows)
        for c in range(r["fetch"], r["idf"]):
            row[c] = Paragraph("IF", cs)
            sty.append(("BACKGROUND", (c, rowi), (c, rowi), colors.Color(1, 0.8, 0.8) if c > r["fetch"] else STG["IF"]))
        for c in range(r["idf"], r["ex"]):
            row[c] = Paragraph("ID", cs)
            sty.append(("BACKGROUND", (c, rowi), (c, rowi), colors.Color(1, 0.8, 0.8) if c > r["idf"] else STG["ID"]))
        for nm, c in (("EX", r["ex"]), ("MEM", r["ex"] + 1), ("WB", r["ex"] + 2)):
            if c <= ncyc:
                row[c] = Paragraph(nm, cs)
                sty.append(("BACKGROUND", (c, rowi), (c, rowi), STG[nm]))
        rows.append(row)
        if flushed and r["taken"] and k + 1 < len(res):
            fr = [Paragraph("(wrong-path instr, flushed)", ParagraphStyle("df", fontName="S-I", fontSize=6.5, leading=8, textColor=GREY))] + [""] * ncyc
            ri2 = len(data) + len(rows)
            for c in range(r["idf"], r["ex"]):
                fr[c] = Paragraph("IF", cs)
                sty.append(("BACKGROUND", (c, ri2), (c, ri2), colors.Color(0.9, 0.9, 0.9)))
            rows.append(fr)
    data += rows
    t = Table(data, colWidths=[4.4 * cm] + [cw] * ncyc)
    t.setStyle(TableStyle(sty))
    return t


def stalls_line(tot):
    return (f"N = {tot['n']},  stalls = {tot['stalls']},  taken-branch penalty = {tot['penalty']}  →  cycles = N + 4 + stalls + penalty = "
            f"{tot['n']} + 4 + {tot['stalls']} + {tot['penalty']} = <b>{tot['total']}</b>")


def tick(b):
    return "HIT" if b else "MISS"


# ---------------------------------------------------------------- examples (all computed)
A = [I("lw  $t0, 0($s0)", "lw", "$t0", ["$s0"]), I("add $t1, $t0, $s1", "alu", "$t1", ["$t0", "$s1"]),
     I("sub $t2, $t1, $s2", "alu", "$t2", ["$t1", "$s2"]), I("and $t3, $t2, $t0", "alu", "$t3", ["$t2", "$t0"]),
     I("sw  $t3, 4($s0)", "sw", None, ["$s0"], ["$t3"])]
rA1, tA1 = pipe(A, True, True)
rA2, tA2 = pipe(A, False, True)
rA3, tA3 = pipe(A, False, False)
assert (tA1["total"], tA2["total"], tA3["total"]) == (10, 17, 21)

LOOP = [("lw  $t0, 0($a0)", "lw", "$t0", ["$a0"], []), ("add $t1, $t0, $t2", "alu", "$t1", ["$t0", "$t2"], []),
        ("sw  $t1, 0($a0)", "sw", None, ["$a0"], ["$t1"]), ("addi $a0, $a0, 4", "alu", "$a0", ["$a0"], []),
        ("addi $a1, $a1, -1", "alu", "$a1", ["$a1"], []), ("bne $a1, $zero, Loop", "br", None, ["$a1"], [])]
seq = []
for k in range(3):
    for t, op, d, s, ds in LOOP:
        seq.append(I(t, op, d, s, ds, taken=(op == "br" and k < 2)))
rL, tL = pipe(seq, True)
assert tL["total"] == 30 and tL["stalls"] == 6 and tL["penalty"] == 2

C1, st1, h1_ = cache([22, 26, 22, 26, 16, 3, 16, 18], 1, 8)
assert h1_ == 3
C2, st2, h2_ = cache([12, 20, 28, 36, 76, 12, 140, 20, 52, 76], 16, 4)
S3 = [0, 5, 8, 0, 4, 5, 8, 0]
C3, st3, h3_ = cache(S3, 1, 2, 2)
_, _, h3dm = cache(S3, 1, 4, 1)
PT = {5: 2, 3: 6, 7: 1}
T1 = tlb([0x5010, 0x3FF8, 0x5ABC, 0x7000, 0x3004, 0x9120], 12, 2, PT)
pred1 = predictor([1, 1, 1, 0] * 3, 1, 0)
assert pred1 == 6

story = []
add = story.append

# ================================================================= page 1
add(banner("CSE 209 — General Steps for Pipeline and Memory-Hierarchy Calculations"))
add(Spacer(1, 4))
add(P("A method sheet for the two question families that carry the most calculation marks in the term final: "
      "<b>(A)</b> pipeline, data hazard and stall-cycle counting, and <b>(B)</b> memory-hierarchy maths (cache address breakdown and traces, AMAT and CPI, "
      "TLB and page tables). Each part gives the master formulas, a numbered procedure, a fully worked example, and the traps that lose marks. "
      "Exam-style numbers in the examples are my own, not taken from any past paper; every figure was produced and cross-checked by a small program. "
      "For worked past-paper answers use the topic-wise solved set and the Question+Solution PDFs.", body))
add(Spacer(1, 3))
add(box("Master formulas at a glance", [grid(
    ["Pipeline (5-stage MIPS)", "Memory hierarchy"],
    [[
        "<b>Cycles, no stalls</b> = N + 4 (N instructions)<br/>"
        "<b>Total cycles</b> = N + 4 + stall cycles + branch-penalty cycles<br/>"
        "<b>CPI</b> = total cycles / N ≈ 1 + stalls per instruction<br/>"
        "<b>Time</b> = IC × CPI × clock period<br/>"
        "<b>Stalls with forwarding</b>: load→use 1; ALU→ALU 0; ALU→branch 1; load→branch 2 (branch decided in ID)<br/>"
        "<b>Stalls with no forwarding</b> (reg-file write 1st half, read 2nd half): distance 1 → 2, distance 2 → 1, ≥ 3 → 0 "
        "(no half-cycle trick: 3, 2, 1)<br/>"
        "<b>Taken-branch penalty</b> = (stage where decided) − 1 : ID 1, EX 2, MEM 3. Predict-not-taken and correct → 0",
        "<b>Offset bits</b> = log<sub>2</sub>(block bytes);  <b>index bits</b> = log<sub>2</sub>(sets);  <b>tag</b> = address bits − index − offset<br/>"
        "<b>Block number</b> = floor(byte address / block size);  <b>index</b> = block number mod sets;  <b>tag</b> = floor(block number / sets)<br/>"
        "<b>Cache bits</b> = entries × (valid + tag + 8 × block bytes)  [+ dirty bit if write-back]<br/>"
        "<b>Hit ratio</b> = hits / accesses<br/>"
        "<b>AMAT</b> = hit time + miss rate × miss penalty (nest it for L2, L3)<br/>"
        "<b>CPI</b> = base CPI + memory-stall cycles per instruction<br/>"
        "<b>Page</b>: offset = log<sub>2</sub>(page size);  VPN bits = VA bits − offset;  page-table size = 2<sup>VPN bits</sup> × PTE size",
    ]], [0.5, 0.5], zebra=False, tw=W - 16)], PALE))

# ================================================================= PART A
add(Spacer(1, 6))
add(banner("PART A — Pipeline, data hazards and stall cycles"))

add(P("A.1  Know the machine before counting", h2))
add(P("Unless the question says otherwise, assume the textbook 5-stage pipe: IF, ID, EX, MEM, WB; one instruction enters per cycle. "
      "With no stall, the first instruction finishes in cycle 5 and each later one a cycle after, so <b>N instructions take N + 4 cycles</b>. "
      "Only <b>RAW</b> (read-after-write) hazards occur in this in-order pipe; WAR and WAW do not. "
      "Always read the stated assumptions first: <i>forwarding or not</i>, <i>where the branch is decided</i>, <i>branch predictor</i>, "
      "and <i>whether the register file writes in the first half and reads in the second half of a cycle</i>.", body))
add(grid(["Hazard type", "Cause", "Typical cure"],
         [["Structural", "Two instructions need the same hardware in the same cycle (single memory port)", "Separate I- and D-memory, or stall"],
          ["Data (RAW)", "An instruction needs a register that an earlier, unfinished instruction will write", "Forwarding; one stall after a load; compiler reordering"],
          ["Control", "The next PC depends on a branch not yet resolved", "Stall, predict not-taken / dynamic prediction, decide the branch early (ID), delayed branch"]],
         [0.14, 0.50, 0.36]))

add(P("A.2  Step-by-step procedure for a code sequence", h2n))
add(box("Procedure", steps([
    "<b>Write the instructions in order</b> and number them 1…N. Next to each, note its destination register and its source registers (for sw, the base is a source needed in EX and the stored register is data needed in MEM).",
    "<b>Find every RAW dependence.</b> For each instruction, look back for the nearest earlier writer of each source register. Only the nearest writer matters. Ignore $zero.",
    "<b>Classify each dependence</b> by producer type (ALU or load) and consumer type (ALU, load/store address, branch) and by distance (how many instructions apart).",
    "<b>Apply the stall table</b> for the given machine (forwarding / no forwarding / branch stage). Stalls delay everything after them, so apply them in program order, and re-measure distances in cycles, not instructions, when there is no forwarding.",
    "<b>Add control penalty</b>: count taken branches that were not predicted. Penalty each = stage the branch is decided in minus 1.",
    "<b>Total</b> = N + 4 + stalls + penalties. Cross-check by drawing the diagram; the answer is the cycle in which the last instruction's WB happens.",
    "<b>Derived numbers</b>: CPI = cycles / N; speedup = cycles<sub>old</sub> / cycles<sub>new</sub> (same clock) or time<sub>old</sub> / time<sub>new</sub>; IPC = N / cycles.",
]), PALE))
add(Spacer(1, 3))
add(grid(["Producer → consumer", "With forwarding", "No forwarding, split-cycle reg file", "No forwarding, no split-cycle"],
         [["ALU → next instruction (distance 1)", "0", "2", "3"],
          ["ALU → distance 2", "0", "1", "2"],
          ["ALU → distance 3", "0", "0", "1"],
          ["lw → next instruction that uses it (distance 1)", "1", "2", "3"],
          ["lw → distance 2", "0", "1", "2"],
          ["ALU → branch decided in ID (distance 1)", "1", "2", "3"],
          ["lw → branch decided in ID (distance 1)", "2", "2", "3"],
          ["lw → sw data (stored register)", "0 (MEM-to-MEM forwarding)", "as ALU row", "as ALU row"]],
         [0.37, 0.19, 0.24, 0.20]))
add(P("Rows for distance 2 and 3 assume no earlier stall pushed the instructions further apart; recount after each stall. "
      "A <b>load-use</b> stall cannot be removed by forwarding because the data is only available at the end of MEM; "
      "the compiler removes it by moving an independent instruction into the slot.", small))

add(P("A.3  Worked example 1 — same code three ways", h2))
add(P("Code (assume branch logic is not involved):", body))
add(asm([r["txt"] for r in rA1]))
add(Spacer(1, 3))
add(P("<b>Dependences:</b> add needs $t0 from lw (load-use, distance 1); sub needs $t1 from add (ALU, distance 1); "
      "and needs $t2 from sub (distance 1) and $t0 from lw (distance 3); sw stores $t3 from and (distance 1). N = 5, so the ideal is 5 + 4 = 9 cycles.", body))
add(P("(a) With forwarding", h3))
add(P("Only the load-use pair stalls: 1 stall.", body))
add(diagram(rA1))
add(P(stalls_line(tA1), body))
add(P("(b) No forwarding; register file writes in the first half and reads in the second half", h3))
add(P("Every adjacent dependent pair costs 2 stalls (add after lw, sub after add, and after sub, sw after and). "
      "The second source of and ($t0) is ready long before, so it adds nothing.", body))
add(diagram(rA2))
add(P(stalls_line(tA2), body))
add(P("(c) No forwarding and no split-cycle", h3))
add(P("A reader must wait until the cycle after WB: 3 stalls per adjacent pair → 12 stalls, "
      + stalls_line(tA3).split("→ ", 1)[1] + ".", body))
add(P(f"<b>Speedups:</b> (b) → (a) is {tA2['total']}/{tA1['total']} = {tA2['total'] / tA1['total']:.2f}; (c) → (a) is {tA3['total']}/{tA1['total']} = {tA3['total'] / tA1['total']:.2f}.", body))

add(P("A.4  Loops and branches — the iteration method", h2))
add(box(None, steps([
    "Write one iteration. Find stalls <b>inside</b> the iteration (data) and the stalls on the closing branch (ALU→branch or load→branch).",
    "Decide how many times the branch is <b>taken</b> and how often the predictor is <b>wrong</b>. Predict-not-taken: every taken branch costs the penalty (1 cycle if decided in ID); the final not-taken exit costs nothing.",
    "<b>Cycles = (instructions per iteration × iterations) + 4 + (stalls per iteration × iterations) + (penalty × taken-and-mispredicted branches).</b> The +4 fill is paid once for the whole run, not per iteration.",
    "Check the iteration boundary: the first instruction of the next iteration may depend on the last one(s) of this one, but after a taken branch the pipeline has already been refilled, so there is normally no extra data stall across the boundary unless the code really has one.",
]), PALE))
add(Spacer(1, 3))
add(P("<b>Worked example 2.</b> Loop run for 3 iterations. Forwarding on, branch decided in ID, predict not-taken.", body))
add(asm([t for t, *_ in LOOP]))
add(Spacer(1, 3))
add(P("Inside one iteration: lw → add is a load-use pair (1 stall). add → sw: forwarding, 0. addi $a1 is immediately followed by bne reading $a1: ALU → branch in ID, 1 stall. "
      "So 2 stalls per iteration. The branch is taken in iterations 1 and 2 (penalty 1 each) and falls through in iteration 3.", body))
add(diagram(rL, show=7))
add(P("The diagram shows iteration 1 and the first instruction of iteration 2 (the grey row is the wrongly fetched instruction that gets flushed).", small))
add(P(f"Cycles = 6 × 3 + 4 + 2 × 3 + 1 × 2 = 18 + 4 + 6 + 2 = <b>{tL['total']}</b>.  CPI = {tL['total']}/18 = {tL['total'] / 18:.2f}.", body))

add(P("A.5  Branch prediction and dependence on frequencies", h2))
add(grid(["Scheme", "Rule", "Cost per branch"],
         [["Stall always", "Wait until the branch is decided", "penalty on every branch"],
          ["Predict not-taken", "Keep fetching sequentially; flush if taken", "penalty only when taken"],
          ["Perfect predictor", "Always right", "0 misprediction penalty (if the target is only known after ID, a correctly predicted taken branch can still cost 1 cycle: read the question)"],
          ["1-bit dynamic", "State = last outcome; predict the same again", "wrong twice per run of an inner loop: on the exit and on the first pass of the next run"],
          ["2-bit saturating", "Needs two wrong guesses in a row to change prediction", "wrong once per inner-loop run after warm-up (only the exit)"]],
         [0.18, 0.37, 0.45]))
add(Spacer(1, 3))
add(P(f"<b>Inner loop of 4 iterations run 3 times</b> (outcomes T T T N, T T T N, T T T N), 1-bit predictor starting at not-taken: mispredictions = {pred1} out of 12 "
      f"(first pass of each run and the exit of each run). With a long inner loop of n iterations the 1-bit accuracy is (n − 2)/n per run, the 2-bit accuracy (n − 1)/n after warm-up. "
      "Always state the initial predictor state you assume.", body))
add(box("CPI from instruction frequencies", [
    P("<b>CPI = 1 + Σ (frequency of the event × stall cycles per event).</b> Example (my numbers): 25% loads, 40% of loads are followed by a dependent instruction (1 stall); "
      "15% branches, 60% of them taken with predict-not-taken and branch decided in ID (1 cycle):", body),
    P("CPI = 1 + 0.25 × 0.40 × 1 + 0.15 × 0.60 × 1 = 1 + 0.10 + 0.09 = <b>1.19</b>.  "
      "", body)], YEL, colors.Color(0.7, 0.55, 0.1)))

add(P("A.6  Forwarding and hazard-detection conditions (they are asked as equations)", h2))
add(grid(["Case", "Condition", "Action"],
         [["EX hazard (forward from EX/MEM)", "EX/MEM.RegWrite and EX/MEM.Rd ≠ 0 and EX/MEM.Rd = ID/EX.Rs  (same for Rt)", "ForwardA = 10 (ForwardB = 10)"],
          ["MEM hazard (forward from MEM/WB)", "MEM/WB.RegWrite and MEM/WB.Rd ≠ 0 and <b>not</b> the EX-hazard condition for the same source and MEM/WB.Rd = ID/EX.Rs  (same for Rt)", "ForwardA = 01 (ForwardB = 01)"],
          ["No hazard", "neither condition", "ForwardA = 00 (read from the register file)"],
          ["Load-use stall", "ID/EX.MemRead and (ID/EX.Rt = IF/ID.Rs or ID/EX.Rt = IF/ID.Rt)", "Hold PC and IF/ID; zero the control signals going into ID/EX (insert a bubble)"]],
         [0.22, 0.52, 0.26]))
add(P("The EX hazard takes priority over the MEM hazard when both match (the newer value wins). For a double data hazard (two earlier instructions write the same register that a third reads) the "
      "second term in the MEM-hazard condition is what keeps the older value from overriding the newer one.", small))

add(box("Common traps (pipeline)", bullets([
    "Using N × 5 instead of N + 4. The +4 is paid once.",
    "Counting a stall for a dependence on an instruction that is 3 or more instructions behind with forwarding on (it never stalls), or counting the load-use stall as 2 (it is 1 with forwarding).",
    "Forgetting that a stall also moves the later instructions, so distance in <i>cycles</i> grows and later dependences can disappear when there is no forwarding.",
    "Charging a penalty for the not-taken exit of a loop with predict-not-taken, or forgetting the penalty on the taken ones.",
    "Taking the branch decision stage from memory: read it from the question (ID in the improved pipeline, MEM in the original).",
    "Mixing up IPC and CPI, or using cycles rather than time when the clock rates differ.",
]), REDP, colors.Color(0.65, 0.1, 0.1)))

# ================================================================= PART B
add(PageBreak())
add(banner("PART B — Memory hierarchy maths"))

add(P("B.1  Address breakdown (direct-mapped, set-associative, fully associative)", h2n))
add(box("Procedure", steps([
    "<b>Check the unit of the addresses</b>: byte address or word address? Word-addressed streams need a different block-number formula. The offset has a byte part (2 bits for 4-byte words) and a word part.",
    "<b>Block size</b> = 2<sup>b</sup> bytes → offset = b bits. <b>Number of sets</b> = entries ÷ ways = 2<sup>s</sup> → index = s bits (direct-mapped: sets = entries; fully associative: 1 set, no index).",
    "<b>Tag</b> = address bits − index − offset.",
    "<b>Total storage</b> = entries × (1 valid + tag + 8 × block bytes) bits, plus 1 dirty bit per entry for write-back, plus LRU bits if asked. "
    "Overhead ratio = (valid + tag [+ dirty]) / (8 × block bytes).",
    "<b>For a trace</b>: block number = floor(byte address / block bytes); set = block number mod sets; tag = floor(block number / sets). Then run the table below.",
]), PALE))
add(Spacer(1, 3))
add(P("<b>Example (size).</b> 32-bit addresses, direct-mapped, 16 KB of data, 4-word (16-byte) blocks. Entries = 16 KB / 16 B = 1024 → index 10 bits; offset = 4 bits; tag = 32 − 10 − 4 = 18 bits. "
      "Bits per entry = 1 + 18 + 128 = 147; total = 147 × 1024 = 150 528 bits = 147 Kbit, against 128 Kbit of data (about 15% overhead).", body))

add(P("B.2  Tracing a stream — the table method", h2))
add(grid(["Step", "Do this for every access"],
         [["1", "Convert to block number (floor(addr / block size)). For word addresses: floor(word addr / words per block)."],
          ["2", "Index (set) = block number mod number of sets; tag = floor(block number / number of sets)."],
          ["3", "Look at that index. <b>Valid and same tag → HIT.</b> Otherwise <b>MISS</b>: fetch the whole block; if the index was occupied by another tag, say which block was replaced (direct-mapped) or choose the victim by the policy (LRU: least recently <i>used</i>, where a hit also updates recency)."],
          ["4", "Keep a running 'cache contents' list per index so the final state and the replaced blocks come straight from it."],
          ["5", "Hit ratio = hits / accesses; miss ratio = 1 − hit ratio."]],
         [0.07, 0.93]))
add(Spacer(1, 4))


def trace_table(rows, cols, unit_hdr, show_blk=True):
    head = ["#", unit_hdr] + (["Block"] if show_blk else []) + ["Index", "Tag", "H/M", "Replaced"]
    data = []
    for i, r in enumerate(rows, 1):
        data.append([str(i), str(r["addr"])] + ([str(r["blk"])] if show_blk else []) + [str(r["idx"]), str(r["tag"]),
                    "<b>HIT</b>" if r["hit"] else "<font color='#b00000'><b>MISS</b></font>", r["note"] or "—"])
    wid = [0.05, 0.10] + ([0.09] if show_blk else []) + [0.09, 0.08, 0.10, 0.49 - (0 if show_blk else 0)]
    s = sum(wid)
    return grid(head, data, [w / s for w in wid])


add(P("<b>Example 1 — direct-mapped, 8 one-word blocks, word addresses</b> 22, 26, 22, 26, 16, 3, 16, 18. Index = address mod 8, tag = address ÷ 8.", body))
add(trace_table(C1, None, "Word addr"))
fin = "; ".join(f"index {i}: block {st1[i][0] * 8 + i}" for i in range(8) if st1[i])
add(P(f"Hits = {h1_}, misses = {8 - h1_}, hit ratio = {h1_}/8 = {h1_ / 8:.3f}. Final contents: {fin}. "
      "Address 18 maps to index 2, which holds 26 (tag 3), so 26 is replaced.", body))

add(Spacer(1, 3))
add(P("<b>Example 2 — direct-mapped, 4 entries, 16-byte blocks, byte addresses</b> 12, 20, 28, 36, 76, 12, 140, 20, 52, 76. "
      "Block = addr ÷ 16, index = block mod 4, tag = block ÷ 4. Note that 20 and 28 lie in the same block (spatial locality).", body))
add(trace_table(C2, None, "Byte addr"))
fin2 = "; ".join(f"index {i}: block {st2[i][0] * 4 + i} (tag {st2[i][0]})" for i in range(4) if st2[i])
add(P(f"Hits = {h2_}, hit ratio = {h2_}/10 = {h2_ / 10:.1f}. Final contents: {fin2}. "
      "The second 20 hits because block 1 was never evicted. Most misses are <i>conflict</i> misses: blocks 0, 4 and 8 all map to index 0 and keep evicting each other.", body))

add(Spacer(1, 3))
add(P("<b>Example 3 — 2-way set-associative, LRU, 4 one-word blocks (2 sets)</b>, word addresses 0, 5, 8, 0, 4, 5, 8, 0. Set = address mod 2; on a miss in a full set the least recently used block is replaced.", body))
add(trace_table(C3, None, "Word addr"))
fin3 = "; ".join(f"set {i} (LRU → MRU): " + ", ".join(str(t * 2 + i) for t in st3[i]) for i in range(2))
add(P(f"Hits = {h3_}, hit ratio = {h3_}/8 = {h3_ / 8:.3f}. Final contents: {fin3}. "
      f"A direct-mapped cache with the same 4 blocks would give only {h3dm} hit here, because 0, 4 and 8 all map to index 0.", body))
add(box("Common traps (cache traces)", bullets([
    "Using the byte address as the block number: divide by the block size first. A byte stream with 16-byte blocks needs addr ÷ 16.",
    "Marking a hit when the index matches but the tag does not.",
    "Forgetting that a hit under LRU still makes that block the most recently used.",
    "Giving a list of 'replaced blocks' by tag only; say the block number (tag × sets + index).",
    "Counting a miss as a replacement when the index was still empty (a cold miss replaces nothing).",
]), REDP, colors.Color(0.65, 0.1, 0.1)))

add(P("B.3  AMAT, CPI with memory stalls and speedup", h2n))
add(box("Procedure", steps([
    "<b>Put everything in the same unit</b>: cycles (convert ns to cycles with cycles = ns × clock rate in GHz, or ns ÷ cycle time in ns).",
    "<b>Single level:</b> AMAT = hit time + miss rate × miss penalty.",
    "<b>Multi-level:</b> AMAT = HT<sub>1</sub> + MR<sub>1</sub> × (HT<sub>2</sub> + MR<sub>2</sub> × (HT<sub>3</sub> + MR<sub>3</sub> × MP<sub>mem</sub>)). Use <b>local</b> miss rates in the nesting; "
    "a <b>global</b> miss rate = product of the local rates down to that level.",
    "<b>CPI with cache stalls:</b> CPI = base CPI + (instruction accesses per instruction × I-miss rate + data accesses per instruction × D-miss rate) × miss penalty. "
    "One instruction fetch per instruction, plus load/store frequency of data accesses.",
    "<b>Multi-level stalls:</b> stall cycles per instruction = accesses per instruction × [MR<sub>1</sub> × L2 time + (global MR<sub>2</sub>) × memory time]. "
    "Only count each level's own time for the accesses that actually reach it.",
    "<b>Speedup</b> = (old AMAT or CPI or time) ÷ (new); when the clock changes, compare <b>times</b>, not cycles.",
]), PALE))
add(Spacer(1, 3))
_amat_hdr = P("<b>Example (AMAT with L2 and L3).</b> L1 hit time 1 cycle, L1 miss rate 5%, main memory 100 cycles. L2 hit time 10 cycles, local miss rate 20%. "
      "L3 hit time 30 cycles, local miss rate 50%.", body)
amat1 = 1 + 0.05 * 100
amat2 = 1 + 0.05 * (10 + 0.2 * 100)
amat3 = 1 + 0.05 * (10 + 0.2 * (30 + 0.5 * 100))
add(KeepTogether([_amat_hdr, grid(["Configuration", "Calculation", "AMAT"],
         [["L1 only", "1 + 0.05 × 100", f"{amat1:.2f} cycles"],
          ["L1 + L2", "1 + 0.05 × (10 + 0.2 × 100) = 1 + 0.05 × 30", f"{amat2:.2f} cycles"],
          ["L1 + L2 + L3", "1 + 0.05 × (10 + 0.2 × (30 + 0.5 × 100)) = 1 + 0.05 × (10 + 0.2 × 80) = 1 + 0.05 × 26", f"{amat3:.2f} cycles"]],
         [0.2, 0.62, 0.18])]))
add(P(f"Speedup from adding L2 = {amat1:.2f}/{amat2:.2f} = {amat1 / amat2:.2f}; from L2 + L3 = {amat1:.2f}/{amat3:.2f} = {amat1 / amat3:.2f}; "
      f"L3 on top of L2 = {amat2:.2f}/{amat3:.2f} = {amat2 / amat3:.2f}.", body))
add(Spacer(1, 3))
add(P("<b>Example (CPI with a second-level cache; classic textbook numbers).</b> Base CPI 1.0, clock 5 GHz (0.2 ns), main memory 100 ns, L1 miss rate 2% per instruction, "
      "L2 access 5 ns, global miss rate to memory 0.5%.", body))
mp_mem = 100 / 0.2
mp_l2 = 5 / 0.2
cpi1 = 1 + 0.02 * mp_mem
cpi2 = 1 + 0.02 * mp_l2 + 0.005 * mp_mem
add(P(f"Miss penalties in cycles: memory = 100 / 0.2 = {mp_mem:.0f}; L2 = 5 / 0.2 = {mp_l2:.0f}. "
      f"L1 only: CPI = 1 + 0.02 × {mp_mem:.0f} = {cpi1:.1f}. "
      f"With L2: CPI = 1 + 0.02 × {mp_l2:.0f} + 0.005 × {mp_mem:.0f} = 1 + {0.02 * mp_l2:.1f} + {0.005 * mp_mem:.1f} = {cpi2:.1f}. "
      f"Speedup = {cpi1:.1f} / {cpi2:.1f} = {cpi1 / cpi2:.2f}.", body))

add(P("B.4  Miss penalty from the memory organisation, block size and write policy", h2))
add(grid(["Memory organisation (4-word block)", "Miss penalty (1 cycle address + 15 cycles per DRAM access + 1 cycle per word transferred)"],
         [["One word wide", "1 + 4 × 15 + 4 × 1 = 65 cycles"],
          ["Four words wide (wide bus)", "1 + 1 × 15 + 1 × 1 = 17 cycles"],
          ["Four interleaved banks, one-word bus", "1 + 1 × 15 + 4 × 1 = 20 cycles"]],
         [0.35, 0.65]))
add(P("General form: <b>miss penalty = address cycles + (DRAM accesses × access time) + (transfers × transfer time)</b>. "
      "Larger blocks lower the miss rate (spatial locality) until the cache has too few blocks (more conflicts) and the miss penalty grows; "
      "<b>early restart</b> and <b>critical word first</b> cut the penalty seen by the CPU without changing the block size.", body))
add(grid(["Policy", "On a write hit", "On a write miss", "Notes"],
         [["Write-through", "Update cache and memory", "No-write-allocate (usually)", "Needs a write buffer; CPI stalls only if the buffer fills"],
          ["Write-back", "Update cache, set dirty bit", "Write-allocate (usually)", "Dirty block written to memory when replaced; needs a dirty bit"]],
         [0.15, 0.25, 0.25, 0.35]))

add(P("B.5  Virtual memory, page tables and the TLB", h2n))
add(box("Procedure", steps([
    "<b>Split the virtual address</b>: page offset = log<sub>2</sub>(page size); virtual page number (VPN) = remaining bits. Physical address = physical page number (PPN) followed by the same offset.",
    "<b>Page-table size</b> = 2<sup>VPN bits</sup> × PTE size (one-level table). Example: 32-bit VA, 4 KB pages, 4-byte PTE → VPN 20 bits → 2<sup>20</sup> × 4 B = 4 MB.",
    "<b>Per access, look in the TLB first.</b> TLB hit → PPN from the TLB. TLB miss → read the page table: valid → load into the TLB (evict by LRU if full); not valid → <b>page fault</b> (OS brings the page from disk).",
    "<b>Track the TLB contents in recency order</b> (LRU first) after every access, as for a cache. Reference to a TLB-resident page is a hit and makes it most recent.",
    "<b>With a cache</b>: translate first (physical cache), then split the physical address into tag / index / offset for the cache lookup. Three cases to name: TLB hit + cache hit, TLB miss + page-table hit, page fault.",
]), PALE))
add(Spacer(1, 3))
add(P("<b>Example.</b> 4 KB pages (12-bit offset), fully associative TLB with 2 entries and LRU. Page table (valid pages): VPN 5 → PPN 2, VPN 3 → PPN 6, VPN 7 → PPN 1; VPN 9 not in memory. "
      "Stream of virtual addresses (hex):", body))
rows = []
for i, r in enumerate(T1, 1):
    pa = f"0x{r['pa']:X}" if r["pa"] is not None else "—"
    colr = "#b00000" if "fault" in r["res"] else ("#1a6b1a" if r["res"] == "TLB hit" else "#333333")
    rows.append([str(i), f"0x{r['va']:X}", str(r["vpn"]), f"0x{r['off']:X}", f"<font color='{colr}'><b>{r['res']}</b></font>",
                 str(r["ppn"]) if r["ppn"] is not None else "—", pa, "[" + ", ".join(map(str, r["tlb"])) + "]"])
add(grid(["#", "VA", "VPN", "Offset", "Result", "PPN", "PA", "TLB after (LRU → MRU)"], rows, [0.05, 0.11, 0.07, 0.10, 0.27, 0.06, 0.11, 0.23]))
add(P("TLB hits = 1 of 6; 4 misses served from the page table; 1 page fault (VPN 9). The 5th access (VPN 3) misses because the 4th access evicted VPN 3, the least recently used entry at that time.", body))
add(box("Common traps (memory)", bullets([
    "Mixing local and global miss rates when nesting AMAT. Use local rates in the nested formula.",
    "Forgetting the instruction fetch: every instruction makes one memory access, plus one more for each load/store.",
    "Not converting ns into cycles before multiplying by the miss rate.",
    "Using the page size where the block size belongs (or the reverse) in the address split.",
    "Treating a page fault as a TLB miss: a page fault is a page-table miss and costs millions of cycles, a TLB miss only tens.",
    "Giving the speedup the wrong way round: speedup = old ÷ new.",
]), REDP, colors.Color(0.65, 0.1, 0.1)))

# ================================================================= PART C
add(Spacer(1, 8))
add(banner("PART C — Exam-hall checklist"))
add(P("C.1  Before you calculate", h2))
add(box(None, bullets([
    "Underline the assumptions: forwarding on/off, branch stage, predictor, split-cycle register file, byte/word addresses, block and page sizes, units (ns, cycles, GHz).",
    "Write the formula in symbols first, then substitute. Marks are given for the setup even if the arithmetic slips.",
    "Draw the pipeline diagram or the cache table instead of reasoning in your head; it is the fastest way to check yourself.",
    "State your assumption in one line whenever the question is silent (e.g. 'branch decided in ID, predict not-taken').",
    "Always end with a sentence: the unit and what the number means (cycles, CPI, hit ratio, speedup).",
]), PALE))
add(P("C.2  Quick decision map", h2))
add(grid(["The question says…", "Do this"],
         [["'How many cycles does this code take?'", "N + 4 + stalls + penalties; draw the diagram to confirm (A.2)"],
          ["'Rewrite to remove the stalls' / 'reorder'", "Find the load-use or ALU→branch pair, move an independent instruction between them; recount"],
          ["'Hazards in this code' / 'show the forwarding paths'", "List each RAW pair, name the producer stage and the consumer stage, give the forwarding path (EX/MEM → EX, MEM/WB → EX, MEM/WB → MEM for sw)"],
          ["'CPI / speedup with …'", "Sum of frequency × penalty (A.5) or AMAT/CPI formulas (B.3); then old ÷ new"],
          ["'Block size, index, tag bits' / 'total cache size'", "B.1 formulas; give entries, offset, index, tag, then bits per entry and total"],
          ["'Hit/miss for this address stream'", "Trace table (B.2); report hit ratio and the final contents"],
          ["'AMAT / speedup from L2, L3'", "Nest local miss rates (B.3), compare AMATs"],
          ["'Page table size / TLB sequence'", "B.5: VPN bits, PTE size; TLB table in LRU order, name page faults"]],
         [0.38, 0.62]))
add(Spacer(1, 4))
add(P("Where to practise next: <b>CSE209_RS_TF_Practice_Tracker.xlsx</b> (Pipelining and Memory tabs, last five papers) and the matching question+solution PDF, "
      "then the full solved paper <b>CSE209_TF_2023-24_Solved_Paper.pdf</b> (Q1(a), Q1(b), Q1(c), Q2(a), Q2(b) and Q3(b) are exactly these topics).", small))


def deco(canv, doc):
    canv.saveState()
    canv.setFont("S", 8)
    canv.setFillColor(GREY)
    canv.drawString(1.6 * cm, 1.0 * cm, "CSE 209 · General steps: pipeline hazards, stalls and memory-hierarchy maths")
    canv.drawRightString(A4[0] - 1.6 * cm, 1.0 * cm, f"Page {doc.page}")
    canv.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=1.4 * cm, bottomMargin=1.6 * cm,
                      title="CSE 209 General Steps: Pipeline and Memory Hierarchy", author="")
doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")], onPage=deco)])
doc.build(story)
print(OUT, os.path.getsize(OUT) // 1024, "KB")
