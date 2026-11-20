"""Question + solution PDFs per teacher: rows from the practice trackers, solution cards cut from the solved set."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl, pymupdf
import sol_index as si

PREP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = r"C:\Windows\Fonts"
FONTS = {"r": F + r"\segoeui.ttf", "b": F + r"\segoeuib.ttf", "s": F + r"\seguisym.ttf"}
PW, PH = 595.28, 841.89
X0, X1 = 38, 557
TOPY, BOTY = 40, 800
NAVY = (0.12, 0.22, 0.39)
_fc = {}


def font(k):
    if k not in _fc:
        _fc[k] = pymupdf.Font(fontfile=FONTS[k])
    return _fc[k]


def put(page, x, y, parts):
    """parts: [(text, fontkey, size, rgb)]; y = baseline."""
    for t, k, sz, col in parts:
        if not t:
            continue
        page.insert_text((x, y), t, fontsize=sz, fontname="F" + k, fontfile=FONTS[k], color=col)
        x += font(k).text_length(t, fontsize=sz)
    return x


def wrap(text, k, sz, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if font(k).text_length(t, fontsize=sz) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def load(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    tabs = []
    for name in wb.sheetnames:
        if name in ("How to Use", "Dashboard", "Outside Notes"):
            continue
        ws = wb[name]
        hdr = [c.value for c in ws[3]]
        rows = [dict(zip(hdr, r)) for r in ws.iter_rows(min_row=4, values_only=True) if r[0] is not None]
        note = re.search(r"Note file: (\S+)", ws.cell(2, 1).value or "")
        tabs.append(dict(name=name, title=ws.cell(1, 1).value, rows=rows,
                         note=note.group(1).replace(".docx", ".pdf") if note else ""))
    return tabs


def find_groups(row, cardidx):
    y, q = row["Year"], str(row["Ques No."])
    if (y, q) in cardidx:
        return sorted(set(cardidx[(y, q)]))
    base = q.split("(")[0]
    sub = re.match(r"\w+\(([a-z])\)", q)
    cands = [(cq, gs) for (cy, cq), gs in cardidx.items() if cy == y and cq.split("(")[0] == base]
    pick = []
    for cq, gs in cands:
        if sub is None:
            pick += gs
            continue
        letter = sub.group(1)
        m = re.match(r"\w+\(([a-z])[–-]([a-z])\)", cq)
        if (m and m.group(1) <= letter <= m.group(2)) or cq.startswith(f"{base}({letter})"):
            pick += gs
    if not pick:
        pick = [g for _, gs in cands for g in gs]
    return sorted(set(pick))


def build(teacher, xlsx, out):
    src = pymupdf.open(si.SRC)
    H, G = si.index(src)
    cardidx = {}
    for gi, g in enumerate(G):
        for c in g["cards"]:
            cardidx.setdefault((c["year"], c["q"]), []).append(gi)
    tabs = load(os.path.join(PREP, xlsx))
    total = sum(len(t["rows"]) for t in tabs)
    doc = pymupdf.open()
    st = {"page": None, "y": 0}

    def newpage():
        st["page"] = doc.new_page(width=PW, height=PH)
        st["y"] = TOPY
        return st["page"]

    def header_bar(head):
        pg = st["page"]
        pg.draw_rect(pymupdf.Rect(X0, st["y"], PW - X0, st["y"] + 18), color=None, fill=(0.88, 0.92, 0.98))
        put(pg, X0 + 6, st["y"] + 13, head)
        st["y"] += 24

    # ---- title page
    p = newpage()
    put(p, X0, 90, [("CSE 211 — " + teacher, "b", 24, NAVY)])
    put(p, X0, 114, [("Term-Final question bank with solutions", "r", 13, (0.3, 0.3, 0.3))])
    y = 138
    intro = (f"{total} questions from the 2017-18, 2019-20, Jan-2020, 2021-22, 2022-23 and 2023-24 papers, grouped by the practice-tracker tabs and lessons. "
             "Each entry has a header line from the tracker (number, exam year, question number, marks, priority, lesson), followed by the question "
             "and its worked solution. Where the same question was asked in several papers, the stacked cards share one solution and later entries point back to it.")
    for ln in wrap(intro, "r", 10, PW - 2 * X0):
        put(p, X0, y, [(ln, "r", 10, (0, 0, 0))])
        y += 14
    y += 6
    for ln in wrap("Priority: High = 2019-20 onward; Medium = the question type repeats in another paper; Low = appears once.", "r", 10, PW - 2 * X0):
        put(p, X0, y, [(ln, "r", 10, (0, 0, 0))])
        y += 14
    y += 10
    put(p, X0, y, [("Tab", "b", 10.5, NAVY)])
    put(p, 420, y, [("Questions", "b", 10.5, NAVY)])
    y += 6
    p.draw_line((X0, y), (PW - X0, y), color=NAVY, width=0.6)
    y += 14
    for t in tabs:
        if t["rows"]:
            put(p, X0, y, [(t["name"], "r", 10.5, (0, 0, 0))])
            put(p, 440, y, [(str(len(t["rows"])), "r", 10.5, (0, 0, 0))])
            y += 16
    y += 14
    credit = ("Solutions are taken from the CSE 211 Theory of Computation Topic-wise Solved Questions set (credited in that book to Mahdi Hasan, "
              "written with Claude Opus 5.5). Check any answer against your lecture notes and the note PDFs in the notes folder before relying on it in the exam.")
    for ln in wrap(credit, "r", 9, PW - 2 * X0):
        put(p, X0, y, [(ln, "r", 9, (0.4, 0.4, 0.4))])
        y += 12

    emitted, n = {}, 0
    stars = {"High": "★★★", "Medium": "★★", "Low": "★"}
    missing = []
    for t in tabs:
        if not t["rows"]:
            continue
        p = newpage()
        p.draw_rect(pymupdf.Rect(X0, TOPY, PW - X0, TOPY + 34), color=None, fill=NAVY)
        tl = wrap(f"{t['name']} — {t['title']}", "b", 13, PW - 2 * X0 - 16)
        put(p, X0 + 8, TOPY + (15 if len(tl) == 1 else 13), [(tl[0], "b", 13, (1, 1, 1))])
        if len(tl) > 1:
            put(p, X0 + 8, TOPY + 28, [(tl[1], "b", 13, (1, 1, 1))])
        put(p, X0, TOPY + 50, [("Notes: " + t["note"], "r", 8.5, (0.4, 0.4, 0.4))])
        st["y"] = TOPY + 62
        for r in t["rows"]:
            n += 1
            gs = find_groups(r, cardidx)
            pr = str(r["Priority"]).split()[-1]
            marks = f"{r['Marks']} marks" if r["Marks"] is not None else "marks n/p"
            head = [(f"{n}.  ", "b", 10, NAVY), (f"{r['Year']} · Q{r['Ques No.']} · {marks} · ", "r", 9.5, (0, 0, 0)),
                    (stars.get(pr, ""), "s", 9.5, (0.75, 0.45, 0.0)), (f" {pr} · {r['Type']} · {r['Lesson']}", "r", 9.5, (0, 0, 0))]
            todo = [g for g in gs if g not in emitted]
            prior = [emitted[g] for g in gs if g in emitted]
            for g in gs:
                emitted.setdefault(g, n)
            if not gs or not todo:
                if st["page"] is None or st["y"] + 50 > BOTY:
                    newpage()
                header_bar(head)
                if not gs:
                    missing.append((r["Year"], r["Ques No."]))
                    msg, col = "Solution not found in the solved set — see the note PDF named above.", (0.7, 0, 0)
                else:
                    msg, col = f"Same question — solution already given under #{min(prior)}.", (0.2, 0.2, 0.2)
                put(st["page"], X0 + 6, st["y"] + 4, [(msg, "r", 9.5, col)])
                st["y"] += 22
                continue
            first = True
            for g in todo:
                for pno, rect in si.spans(src, G, g):
                    clip = pymupdf.Rect(X0, rect.y0, X1, rect.y1)
                    h, w = clip.height, clip.width
                    lead = 24 if first else 0
                    if st["y"] + lead + min(h, 130) > BOTY:
                        newpage()
                    if first:
                        header_bar(head)
                        first = False
                    sc = 1.0
                    if st["y"] + h > BOTY:
                        if BOTY - st["y"] < 0.55 * h and h <= BOTY - TOPY:
                            newpage()
                        if st["y"] + h > BOTY:
                            sc = (BOTY - st["y"]) / h
                    tgt = pymupdf.Rect(X0, st["y"], X0 + w * sc, st["y"] + h * sc)
                    st["page"].show_pdf_page(tgt, src, pno, clip=clip)
                    st["y"] += h * sc + 4
            st["y"] += 10
    for i, pg in enumerate(doc, 1):
        put(pg, X0, 826, [(f"CSE 211 · {teacher} · TF questions with solutions", "r", 8, (0.45, 0.45, 0.45))])
        put(pg, PW - X0 - 24, 826, [(f"Page {i}", "r", 8, (0.45, 0.45, 0.45))])
    doc.save(out, deflate=True, garbage=3)
    print(out, total, "questions,", len(doc), "pages,", os.path.getsize(out) // 1024, "KB; unmatched:", missing)


if __name__ == "__main__":
    build("Hakim Sir", "CSE211_Hakim_TF_Practice_Tracker.xlsx", os.path.join(PREP, "CSE211_Hakim_TF_Questions_Solutions.pdf"))
    build("Atif Sir", "CSE211_Atif_TF_Practice_Tracker.xlsx", os.path.join(PREP, "CSE211_Atif_TF_Questions_Solutions.pdf"))
