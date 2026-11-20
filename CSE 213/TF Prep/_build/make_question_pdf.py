"""make_question_pdf.py — builds CSE213_Topicwise_TF_Questions.pdf from CSE213_Topicwise_TF_Solutions.pdf
by cutting out the question cards (coral-edged boxes), 'REPEATED' banners and chapter titles, and dropping
every SOLUTION panel. Strips are copied as vector content (no rasterising), stacked onto new A4 pages."""
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "CSE213_Topicwise_TF_Solutions.pdf")
OUT = os.path.join(HERE, "..", "CSE213_Topicwise_TF_Questions.pdf")
CORAL = (0.906, 0.435, 0.318)
HEAD = re.compile(r"^\d{4}\D\d{4} • Q")

src = pymupdf.open(SRC)
toc = src.get_toc()
chapter_start = {p: t for _, t, p in toc}          # 1-based page -> chapter title
W, H = src[0].rect.width, src[0].rect.height
TOP, BOTTOM, GAP = 34, H - 40, 6


def close(c, ref, tol=0.02):
    return c is not None and all(abs(a - b) < tol for a, b in zip(c, ref))


def strips(pno):
    """Vertical regions (y0, y1) of page pno (0-based) that belong to questions or headings."""
    pg = src[pno]
    rs = []
    for dr in pg.get_drawings():
        r = dr["rect"]
        if close(dr.get("fill"), CORAL) and r.width > 400 and r.height > 10:
            rs.append([r.y0 - 2, r.y1 + 2])
    for b in pg.get_text("blocks"):
        if b[4].lstrip().startswith("REPEATED"):
            rs.append([b[1] - 7, b[3] + 7])
    if pno + 1 in chapter_start:                    # chapter banner + title
        title_bottom = max((b[3] for b in pg.get_text("blocks")
                            if b[1] < 150 and chapter_start[pno + 1][:12].upper() in b[4].upper().replace("\n", " ")),
                           default=135)
        rs.append([26, title_bottom + 8])
    # pages assembled from strips (rebuild_book.py) can report drawings that lie outside the visible page
    rs = [[max(y0, 0), min(y1, H)] for y0, y1 in rs if y1 > 0 and y0 < H and min(y1, H) - max(y0, 0) > 4]
    rs.sort()
    merged = []
    for y0, y1 in rs:
        if merged and y0 <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], y1)
        else:
            merged.append([y0, y1])
    return merged


out = pymupdf.open()
page, y = None, None
out_toc = []
n_cards = 0


def new_page():
    global page, y
    page = out.new_page(width=W, height=H)
    y = TOP


def place(pno, y0, y1, keep_next=0):
    global y
    h = y1 - y0
    if page is None or y + h + keep_next > BOTTOM:
        new_page()
    page.show_pdf_page(pymupdf.Rect(0, y, W, y + h), src, pno, clip=pymupdf.Rect(0, y0, W, y1))
    y += h + GAP


# ---- title page
new_page()
page.insert_text((60, 300), "CSE 213 — Software Engineering", fontsize=26, fontname="hebo", color=(0.11, 0.15, 0.23))
page.insert_text((60, 335), "Topic-wise Term-Final Questions (in-syllabus, questions only)", fontsize=15, fontname="helv",
                 color=(0.2, 0.3, 0.45))
page.insert_text((60, 370), "Same order and question IDs as CSE213_Topicwise_TF_Solutions.pdf.", fontsize=11, fontname="helv")
page.insert_text((60, 388), "Solve each question first, then check the solution book.", fontsize=11, fontname="helv")
y = BOTTOM + 1                                       # force new page

pending = None
PART2 = next(p for _, t, p in toc if t.startswith("PART II"))   # out-of-syllabus part starts here
for pno in range(3, PART2 - 1):                # skip cover, contents, 'how to read'
    if pno + 1 in chapter_start:
        new_page()
        out_toc.append([1, chapter_start[pno + 1], out.page_count])
        if chapter_start[pno + 1].startswith("PART II"):
            page.show_pdf_page(page.rect, src, pno)  # full part-divider page
            y = BOTTOM + 1
            continue
    ss = strips(pno)
    if pending:                                      # banner held back from the previous page
        nxt = ss[0][1] - ss[0][0] if ss else 0
        place(*pending, keep_next=min(nxt, 200) + GAP)
        pending = None
    for k, (y0, y1) in enumerate(ss):
        lone_banner = (y1 - y0) < 30
        if lone_banner and k == len(ss) - 1:
            pending = (pno, y0, y1)
            continue
        nxt = ss[k + 1][1] - ss[k + 1][0] if lone_banner and k + 1 < len(ss) else 0
        place(pno, y0, y1, keep_next=min(nxt, 200) + (GAP if nxt else 0))

for i, pg in enumerate(out, 1):
    if i > 1:
        pg.insert_text((W / 2 - 8, H - 22), str(i - 1), fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
out.set_toc(out_toc)
out.set_metadata({"title": "CSE 213 Software Engineering – Topic-wise Term-Final Questions"})
out.save(OUT, garbage=4, deflate=True)

# ---- verification: every question header in the source appears in the output
def headers(doc, start):
    hs = []
    for p in doc.pages(start):
        for b in p.get_text("blocks"):
            t = b[4].strip()
            if HEAD.match(t):
                hs.append(t.split("|")[0].split("\n")[0])
    return hs


a, b = headers(src.__class__(SRC), 3), headers(pymupdf.open(OUT), 0)
a = a[:len([h for p in src.pages(3, PART2 - 1) for h in [bb[4] for bb in p.get_text("blocks")] if HEAD.match(h.strip())])]
print("pages", out.page_count, "| question headers: source", len(a), "output", len(b))
missing = [h for h in a if h not in b]
print("missing:", missing[:10])
sys.exit(1 if missing else 0)
