"""rebuild_book.py — moves the Smart Home Hub question (22 batch / '2023-24' Q5(b), Mediator + Command)
out of chapter 04 'Behavioural Design Patterns' into chapter X1 'Design Patterns Beyond the Slides'
(out of syllabus), because the Command pattern is not in this term's syllabus.

Keeps the original PDF as _build/backup/CSE213_Topicwise_TF_Solutions_original.pdf and rewrites
CSE213_Topicwise_TF_Solutions.pdf: page numbers, contents page, contents links, bookmarks and the cover
counts are updated. Content is copied as vector PDF (no rasterising)."""
import os
import shutil

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(HERE, "..", "CSE213_Topicwise_TF_Solutions.pdf")
BAK = os.path.join(HERE, "backup", "CSE213_Topicwise_TF_Solutions_original.pdf")
os.makedirs(os.path.dirname(BAK), exist_ok=True)
if not os.path.exists(BAK):
    shutil.copy2(BOOK, BAK)
src = pymupdf.open(BAK)
W, H = src[0].rect.width, src[0].rect.height

# ---- source facts (1-based pages, y in points), checked with book_groups.py
CH4 = 103                      # chapter 04 start; the Smart Home group fills p103 y>=173 .. p106, ends p107 y=65
GROUP = [(103, 173, 796), (104, 56, 796), (105, 56, 796), (106, 56, 796)]
REST_107 = (107, 65, 796)      # what follows the group on p107 (next question group)
X1_LAST = 487                  # last page of chapter X1; chapter X2 starts on 488
X1_HEADER_FROM = 482           # a continuation page of X1 (for its running header strip)


def split_y(pno, y0, limit):
    """Largest y <= limit in page pno where no text line crosses (to cut a strip between lines)."""
    lines = []
    for b in src[pno - 1].get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            lines.append((l["bbox"][1], l["bbox"][3]))
        if b.get("type") == 1:
            lines.append((b["bbox"][1], b["bbox"][3]))
    best = y0
    for _, ly1 in lines:
        cand = ly1 + 2
        if y0 < cand <= limit and not any(a < cand < b for a, b in lines):
            best = max(best, cand)
    return best


out = pymupdf.open()
newpage = {}                    # old 1-based page -> new 1-based page


def copy(a, b):                 # copy source pages a..b (1-based, inclusive)
    for p in range(a, b + 1):
        out.insert_pdf(src, from_page=p - 1, to_page=p - 1, links=False, annots=False)
        newpage[p] = out.page_count


def strip(page, pno, y0, y1, at):
    page.show_pdf_page(pymupdf.Rect(0, at, W, at + (y1 - y0)), src, pno - 1, clip=pymupdf.Rect(0, y0, W, y1))


copy(1, CH4 - 1)
# new chapter-04 opening page: banner + title, then the start of the next question group
pg = out.new_page(width=W, height=H)
newpage[CH4] = ch4_page = out.page_count
strip(pg, CH4, 0, 172, 0)
p, y0, y1 = REST_107
cut = split_y(p, y0, y0 + (796 - 180))
strip(pg, p, y0, cut, 180)
pg = out.new_page(width=W, height=H)
newpage[107] = out.page_count
strip(pg, p, 0, 56, 0)                                   # running header of chapter 04
strip(pg, p, cut, y1, 74)
copy(108, X1_LAST)
# the moved group, at the end of chapter X1
moved_first = out.page_count + 1
for i, (p, a, b) in enumerate(GROUP):
    pg = out.new_page(width=W, height=H)
    newpage[p] = out.page_count
    strip(pg, X1_HEADER_FROM, 0, 56, 0)
    strip(pg, p, a, b, 74 if i == 0 else 56)
copy(X1_LAST + 1, src.page_count)

# ---- page numbers (printed number = page index - 4, from the first chapter page on)
for i, pg in enumerate(out, 1):
    if i >= 5:
        pg.draw_rect(pymupdf.Rect(250, 797, 345, 816), color=None, fill=(1, 1, 1))
        txt = str(i - 4)
        tw = pymupdf.get_text_length(txt, fontname="helv", fontsize=8.5)
        pg.insert_text((W / 2 - tw / 2, 810), txt, fontname="helv", fontsize=8.5, color=(0.45, 0.45, 0.45))

# ---- bookmarks
toc = [[lvl, t, ch4_page if p == CH4 else newpage[p]] for lvl, t, p in src.get_toc()]
out.set_toc(toc)
by_title = {t: p for _, t, p in toc}

# ---- contents page (page 2): replace the orange page numbers, rebuild the links
cp = out[1]
for l in list(cp.get_links()):
    cp.delete_link(l)
rows = []
for b in cp.get_text("dict")["blocks"]:
    for l in b.get("lines", []):
        title = "".join(s["text"] for s in l["spans"] if s["color"] == 0x1b263b).strip()
        nums = [s for s in l["spans"] if s["color"] == 0xe76f51 and s["text"].strip().isdigit() and s["bbox"][0] > 500]
        if title and nums and title in by_title:
            rows.append((title, nums[0], l["bbox"]))
for title, span, bbox in rows:
    r = pymupdf.Rect(span["bbox"])
    cp.add_redact_annot(r, fill=(1, 1, 1))
cp.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
for title, span, bbox in rows:
    num = str(by_title[title] - 4)
    r = pymupdf.Rect(span["bbox"])
    tw = pymupdf.get_text_length(num, fontname="hebo", fontsize=9.8)
    cp.insert_text((542 - tw, r.y1 - 2), num, fontname="hebo", fontsize=9.8, color=(0.906, 0.435, 0.318))
    cp.insert_link({"kind": pymupdf.LINK_GOTO, "from": pymupdf.Rect(bbox), "page": by_title[title] - 1})
assert len(rows) == len(toc) - 1, (len(rows), len(toc))   # every chapter except the PART II divider

# ---- cover counts: one question moves from in-syllabus to out-of-syllabus
cv = out[0]
spans = [s for b in cv.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"]]
fix = {"265": "264", "132": "133"}
hits = [s for s in spans if s["text"].strip() in fix and s["size"] > 20]
for s in hits:
    cv.add_redact_annot(pymupdf.Rect(s["bbox"]), fill=(1, 1, 1))
cv.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
for s in hits:
    c = s["color"]
    cv.insert_text((s["bbox"][0], s["bbox"][3] - 4), fix[s["text"].strip()], fontname="hebo", fontsize=s["size"],
                   color=((c >> 16) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255))
assert len(hits) == 2

out.set_metadata(src.metadata)
tmp = BOOK + ".tmp"
out.save(tmp, garbage=4, deflate=True)
out.close()
os.replace(tmp, BOOK)
print("pages", src.page_count, "->", pymupdf.open(BOOK).page_count, "| moved group now on pages", moved_first, "-", moved_first + 3)
