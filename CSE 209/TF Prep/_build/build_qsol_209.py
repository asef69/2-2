"""Question + solution PDFs per teacher (ART, RS): rows from the practice trackers, solution cards cut from the solved set."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl, pymupdf
import sol_index209 as si

PREP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = r"C:\Windows\Fonts"
FONTS = {"r": F + r"\segoeui.ttf", "b": F + r"\segoeuib.ttf", "s": F + r"\seguisym.ttf"}
PW, PH = 595.28, 841.89
X0, X1 = 44, 551
TOPY, BOTY = 40, 800
NAVY = (0.12, 0.22, 0.39)
_fc = {}


def font(k):
    if k not in _fc:
        _fc[k] = pymupdf.Font(fontfile=FONTS[k])
    return _fc[k]


def put(page, x, y, parts):
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
        if name in ("How to Use", "Dashboard"):
            continue
        ws = wb[name]
        hdr = [c.value for c in ws[3]]
        rows = [dict(zip(hdr, r)) for r in ws.iter_rows(min_row=4, values_only=True) if r[0] is not None]
        if name == "Outside Notes":
            tabs.append(dict(name=name, title="Questions outside the short slides (answered from the textbook)", rows=rows, note="", outside=True))
            continue
        note = re.search(r"Note file: (\S+)", ws.cell(2, 1).value or "")
        tabs.append(dict(name=name, title=ws.cell(1, 1).value, rows=rows, outside=False,
                         note=note.group(1).replace(".docx", ".pdf") if note else ""))
    return tabs


def find_groups(row, cardidx):
    y, q = row["Year"], str(row["Ques No."])
    course = re.sub(r"\D", "", str(row["Course"]))
    base = re.match(r"\d+", q).group(0)
    sub = re.match(r"\d+\(([a-z])\)", q)
    cands = [(cq, gs) for (cy, cc, cq), gs in cardidx.items() if cy == y and cc == course and re.match(r"\d+", cq).group(0) == base]
    exact = [gs for cq, gs in cands if cq == q]
    if exact:
        return sorted(set(g for gs in exact for g in gs))
    pick = []
    for cq, gs in cands:
        if sub is None:
            pick += gs
            continue
        letter = sub.group(1)
        m = re.match(r"\d+\(([a-z])[–-]([a-z])\)", cq)
        if (m and m.group(1) <= letter <= m.group(2)) or cq.startswith(f"{base}({letter})"):
            pick += gs
    return sorted(set(pick))


def best_cut(page, y0, limit, yend):
    """largest whitespace row in (y0+80, limit]; falls back to limit."""
    occ = []
    for b in page.get_text("dict")["blocks"]:
        for l in (b.get("lines") or []):
            occ.append((l["bbox"][1], l["bbox"][3]))
        if b["type"] == 1:
            occ.append((b["bbox"][1], b["bbox"][3]))
    for d in page.get_drawings():
        r = d["rect"]
        if r.width < 480 and r.height < 120:
            occ.append((r.y0, r.y1))
    occ = sorted((a, b) for a, b in occ if b > y0 and a < limit + 1)
    merged = []
    for a, b in occ:
        if merged and a <= merged[-1][1] + 1.5:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    best = None
    for (a1, b1), (a2, b2) in zip(merged, merged[1:]):
        mid = (b1 + a2) / 2
        if y0 + 80 < mid <= limit and a2 - b1 >= 2.5:
            best = mid
    return best if best is not None else limit


def build(teacher, xlsx, out):
    src = pymupdf.open(si.SRC)
    H, G, T = si.index(src)
    cardidx = {}
    for gi, g in enumerate(G):
        for c in g["cards"]:
            cardidx.setdefault((c["year"], c["course"], c["q"]), []).append(gi)
    tabs = [t for t in load(os.path.join(PREP, xlsx)) if t["rows"]]
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

    p = newpage()
    put(p, X0, 90, [("CSE 209 — " + teacher, "b", 24, NAVY)])
    put(p, X0, 114, [("Term-Final question bank with solutions", "r", 13, (0.3, 0.3, 0.3))])
    y = 138
    intro = (f"{total} questions from the 2019-20, 2020-21, 2021-22, 2022-23 and 2023-24 papers (the last five term finals), grouped by the practice-tracker tabs and lessons. "
             "Each entry has a header line from the tracker (number, exam year, question number, marks, priority, type, lesson), followed by the question "
             "and its worked solution. Where the same question was asked in several papers, the stacked cards share one solution and later entries point back to it.")
    for ln in wrap(intro, "r", 10, PW - 2 * X0):
        put(p, X0, y, [(ln, "r", 10, (0, 0, 0))])
        y += 14
    y += 6
    for ln in wrap("Priority: every question here is High (2019-20 onward); Medium and Low apply only to older papers.", "r", 10, PW - 2 * X0):
        put(p, X0, y, [(ln, "r", 10, (0, 0, 0))])
        y += 14
    y += 10
    put(p, X0, y, [("Tab", "b", 10.5, NAVY)])
    put(p, 420, y, [("Questions", "b", 10.5, NAVY)])
    y += 6
    p.draw_line((X0, y), (PW - X0, y), color=NAVY, width=0.6)
    y += 14
    for t in tabs:
        put(p, X0, y, [(t["name"], "r", 10.5, (0, 0, 0))])
        put(p, 440, y, [(str(len(t["rows"])), "r", 10.5, (0, 0, 0))])
        y += 16
    y += 14
    credit = ("Solutions are taken from the CSE 209 Computer Architecture Topic-wise Solved Questions set (credited in that book to Mahdi Hasan, "
              "written with Claude Opus 5.5). Check any answer against your lecture notes and the note PDFs in the notes folder before relying on it in the exam.")
    for ln in wrap(credit, "r", 9, PW - 2 * X0):
        put(p, X0, y, [(ln, "r", 9, (0.4, 0.4, 0.4))])
        y += 12

    emitted, n, missing = {}, 0, []
    stars = {"High": "★★★", "Medium": "★★", "Low": "★"}
    for t in tabs:
        p = newpage()
        p.draw_rect(pymupdf.Rect(X0, TOPY, PW - X0, TOPY + 34), color=None, fill=NAVY)
        tl = wrap(f"{t['name']} — {t['title']}", "b", 13, PW - 2 * X0 - 16)
        put(p, X0 + 8, TOPY + (15 if len(tl) == 1 else 13), [(tl[0], "b", 13, (1, 1, 1))])
        if len(tl) > 1:
            put(p, X0 + 8, TOPY + 28, [(tl[1], "b", 13, (1, 1, 1))])
        note = ("Notes: " + t["note"]) if t["note"] else "Textbook topics: check with sir whether they are in this term's syllabus."
        put(p, X0, TOPY + 50, [(note, "r", 8.5, (0.4, 0.4, 0.4))])
        st["y"] = TOPY + 62
        for r in t["rows"]:
            n += 1
            gs = find_groups(r, cardidx)
            marks = f"{r['Marks']:g} marks" if isinstance(r.get("Marks"), (int, float)) else "marks n/p"
            if t["outside"]:
                head = [(f"{n}.  ", "b", 10, NAVY), (f"{r['Year']} · Q{r['Ques No.']} · {marks} · {r.get('Topic Area') or ''}", "r", 9.5, (0, 0, 0))]
            else:
                pr = str(r["Priority"]).split()[-1]
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
                    missing.append((r["Year"], r["Course"], r["Ques No."]))
                    msg, col = "Solution not found in the solved set - see the note PDF named above.", (0.7, 0, 0)
                else:
                    msg, col = f"Same question - solution already given under #{min(prior)}.", (0.2, 0.2, 0.2)
                put(st["page"], X0 + 6, st["y"] + 4, [(msg, "r", 9.5, col)])
                st["y"] += 22
                continue
            first = True
            for g in todo:
                for pno, rect in si.spans(src, G, T, g):
                    y0, yend = rect.y0, rect.y1
                    while yend - y0 > 6:
                        lead = 24 if first else 0
                        avail = BOTY - st["y"] - lead
                        if yend - y0 <= avail + 2:
                            cut = yend
                        elif avail >= 230:
                            cut = best_cut(src[pno], y0, min(yend, y0 + avail), yend)
                        else:
                            newpage()
                            continue
                        h = cut - y0
                        clip = pymupdf.Rect(X0 + 4, y0, X1 + 4, cut)
                        if first:
                            header_bar(head)
                            first = False
                        tgt = pymupdf.Rect(X0, st["y"], X0 + clip.width, st["y"] + h)
                        st["page"].show_pdf_page(tgt, src, pno, clip=clip)
                        st["y"] += h + 4
                        y0 = cut
                        if y0 < yend - 6:
                            newpage()
            st["y"] += 10
    for i, pg in enumerate(doc, 1):
        put(pg, X0, 826, [(f"CSE 209 · {teacher} · TF questions with solutions", "r", 8, (0.45, 0.45, 0.45))])
        put(pg, PW - X0 - 24, 826, [(f"Page {i}", "r", 8, (0.45, 0.45, 0.45))])
    doc.save(out, deflate=True, garbage=3)
    print(out, total, "questions,", len(doc), "pages,", os.path.getsize(out) // 1024, "KB; unmatched:", missing)


if __name__ == "__main__":
    build("Tushar Sir (ART)", "CSE209_ART_TF_Practice_Tracker.xlsx", os.path.join(PREP, "CSE209_ART_TF_Questions_Solutions.pdf"))
    build("Rifat Sir (RS)", "CSE209_RS_TF_Practice_Tracker.xlsx", os.path.join(PREP, "CSE209_RS_TF_Questions_Solutions.pdf"))
