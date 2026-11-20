"""CSE 209 term final 2023-24 (29/04/2026, 'CSE 209 (22 batch).pdf'): every question in paper order with its solution card."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pymupdf
import sol_index209 as si
import build_qsol_209 as B

PREP = B.PREP
X0, X1, TOPY, BOTY, PW, PH, NAVY = B.X0, B.X1, B.TOPY, B.BOTY, B.PW, B.PH, B.NAVY
put, wrap, best_cut = B.put, B.wrap, B.best_cut

# (section, label shown, marks, [book question numbers]) in paper order
PAPER = [
    ("A", "Q1(a)  Forwarding unit with equations (double data hazard)", 10, ["1(a)"]),
    ("A", "Q1(b)  Hazards and cycle counts for the beq/bne code", 15, ["1(b)"]),
    ("A", "Q1(c)  1-bit predictor on nested loops; perfect predictor and the 1-cycle taken-branch penalty", 10, ["1(c)"]),
    ("A", "Q2(a)  Speedup from L2 and L3 caches", 10, ["2(a)"]),
    ("A", "Q2(b)  Direct-mapped cache trace (block size, entries, replaced blocks, hit ratio, final state)", 15, ["2(b)"]),
    ("A", "Q2(c)  Larger blocks, early restart / critical word first, write buffer", 10, ["2(c)"]),
    ("A", "Q3(a)  TLB vs data cache; flow diagram for read and write", 10, ["3(a)"]),
    ("A", "Q3(b)  TLB / page-table stream with LRU", 15, ["3(b)"]),
    ("A", "Q3(c)  Cache coherence and snooping", 10, ["3(c)"]),
    ("A", "Q4(a)  Intel/AMD PC with a separate GPU; CPU-GPU memory access", 10, ["4(a)"]),
    ("A", "Q4(b)  Dual-issue schedule of the loop, IPC, loop unrolling", 15, ["4(b)"]),
    ("A", "Q4(c)  CUDA kernel, grid, thread block and their mapping to SP cores and SMs", 10, ["4(c)"]),
    ("B", "Q5(a)  MIPS-v22: datapath muxes for register numbers; encode add, addi, lw", 20, ["5(a)"]),
    ("B", "Q5(b)  4-bit ALU: X, Y, Z equations", 15, ["5(b)"]),
    ("B", "Q6(a)  Clock rate needed for 6 s with 1.2x cycles", 13, ["6(a)"]),
    ("B", "Q6(b)  MIPS code for the do-while program", 13, ["6(b)"]),
    ("B", "Q6(c)  PC-relative, immediate and base addressing", 9, ["6(c)"]),
    ("B", "Q7(a)  Multiplication hardware (two versions) and 1000 x 1011 simulation", 20, ["7(a)"]),
    ("B", "Q7(b)  Purpose of bias; smallest/largest single and double values", 15, ["7(b)"]),
    ("B", "Q8(a)  PC+4, clock cycle, upper 4 bits of PC+4, single memory", 20, ["8(a)"]),
    ("B", "Q8(b)  Hardware to add the jump instruction", 10, ["8(b)"]),
    ("B", "Q8(c)  Out-of-range beq replaced by a pair of instructions", 5, ["8(c)"]),
]


def main():
    src = pymupdf.open(si.SRC)
    H, G, T = si.index(src)
    idx = {}
    for gi, g in enumerate(G):
        for c in g["cards"]:
            if c["year"] == "2023-24" and c["course"] == "209":
                idx.setdefault(c["q"], gi)
    doc = pymupdf.open()
    st = {"page": None, "y": 0}

    def newpage():
        st["page"] = doc.new_page(width=PW, height=PH)
        st["y"] = TOPY

    # cover page (filled in at the end with page numbers)
    newpage()
    emitted, pages, missing = set(), [], []
    for sec, label, marks, qs in PAPER:
        gs = []
        for q in qs:
            if q not in idx:
                missing.append(q)
                continue
            if idx[q] not in gs:
                gs.append(idx[q])
        gs = [g for g in gs if g not in emitted]
        if not gs:
            continue
        newpage()
        pages.append((sec, label, marks, len(doc)))
        pg = st["page"]
        pg.draw_rect(pymupdf.Rect(X0, st["y"], PW - X0, st["y"] + 20), color=None, fill=(0.88, 0.92, 0.98))
        put(pg, X0 + 6, st["y"] + 14, [(f"Section {sec}  ·  ", "b", 10, NAVY), (label, "r", 9.5, (0, 0, 0)), (f"  ·  {marks} marks", "r", 9.5, (0.4, 0.4, 0.4))])
        st["y"] += 28
        for g in gs:
            emitted.add(g)
            for pno, rect in si.spans(src, G, T, g):
                y0, yend = rect.y0, rect.y1
                while yend - y0 > 6:
                    avail = BOTY - st["y"]
                    if yend - y0 <= avail + 2:
                        cut = yend
                    elif avail >= 230:
                        cut = best_cut(src[pno], y0, min(yend, y0 + avail), yend)
                    else:
                        newpage()
                        continue
                    h = cut - y0
                    clip = pymupdf.Rect(X0 + 4, y0, X1 + 4, cut)
                    st["page"].show_pdf_page(pymupdf.Rect(X0, st["y"], X0 + clip.width, st["y"] + h), src, pno, clip=clip)
                    st["y"] += h + 4
                    y0 = cut
                    if y0 < yend - 6:
                        newpage()
    # cover
    p = doc[0]
    put(p, X0, 90, [("CSE 209 — Computer Architecture", "b", 24, NAVY)])
    put(p, X0, 116, [("Term Final 2023-24 (L-2/T-2) — solved paper", "r", 14, (0.3, 0.3, 0.3))])
    y = 140
    for ln in wrap("Exam date 29/04/2026 · 210 marks · 3 hours. Section A: Q1 mandatory, any two of Q2-Q4. Section B: Q5 mandatory, any two of Q6-Q8. "
                   "Every question of the paper is solved below in paper order (the question is re-typeset in the card, followed by its solution). "
                   "Where the same question was asked in earlier papers, those cards are stacked with it and share one solution.", "r", 10, PW - 2 * X0):
        put(p, X0, y, [(ln, "r", 10, (0, 0, 0))])
        y += 14
    y += 12
    put(p, X0, y, [("Question", "b", 10.5, NAVY)])
    put(p, PW - X0 - 80, y, [("Marks", "b", 10.5, NAVY), ("   Page", "b", 10.5, NAVY)])
    y += 6
    p.draw_line((X0, y), (PW - X0, y), color=NAVY, width=0.6)
    y += 15
    cur = None
    for sec, label, marks, pno in pages:
        if sec != cur:
            cur = sec
            put(p, X0, y, [(f"Section {sec}", "b", 10, NAVY)])
            y += 15
        lab = wrap(label, "r", 9.5, PW - 2 * X0 - 110)
        put(p, X0 + 8, y, [(lab[0], "r", 9.5, (0, 0, 0))])
        put(p, PW - X0 - 72, y, [(str(marks), "r", 9.5, (0, 0, 0))])
        put(p, PW - X0 - 24, y, [(str(pno), "r", 9.5, (0, 0, 0))])
        y += 14
        for extra in lab[1:]:
            put(p, X0 + 8, y, [(extra, "r", 9.5, (0, 0, 0))])
            y += 13
    y += 14
    for ln in wrap("Solutions are taken from the CSE 209 Computer Architecture Topic-wise Solved Questions set (credited in that book to Mahdi Hasan, written with Claude Opus 5.5). "
                   "Check answers against your lecture notes before relying on them in the exam.", "r", 9, PW - 2 * X0):
        put(p, X0, y, [(ln, "r", 9, (0.4, 0.4, 0.4))])
        y += 12
    for i, pg in enumerate(doc, 1):
        put(pg, X0, 826, [("CSE 209 · Term Final 2023-24 · solved paper", "r", 8, (0.45, 0.45, 0.45))])
        put(pg, PW - X0 - 24, 826, [(f"Page {i}", "r", 8, (0.45, 0.45, 0.45))])
    out = os.path.join(PREP, "CSE209_TF_2023-24_Solved_Paper.pdf")
    doc.save(out, deflate=True, garbage=3)
    print(out, len(doc), "pages, missing:", missing)


main()
