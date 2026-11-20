"""clean_slides.py <in.pdf> <out.pdf> — removes the out-of-syllabus patterns (Facade, Command, Chain of
Responsibility, Interpreter) from the combined slide PDF 'TF Prep.pdf'.

Edits (page numbers are those of the ORIGINAL file):
  1. pp. 376-386  Behavioral slides 168-178 (the Command introduction, 'Let's design a simple text-editor' …) are deleted.
                  (Slides 179-202 of that deck were already absent from the file.)
  2. p. 37        Lec 2 'Structural Patterns' list: the Façade line is removed, the list closes up, 'Seven' -> 'Six'.
  3. p. 38        Lec 2 'Behavioral Patterns' list: Interpreter, Chain of Responsibility and Command are removed,
                  the list closes up, '11' -> '8'.
  4. p. 177       Structural slide 82 (Adapter Q&A): the sentence that points to the Facade pattern is covered.
Bookmarks of later pages are shifted. The input file is never modified."""
import sys

import pymupdf

SRC, OUT = sys.argv[1], sys.argv[2]
CALIBRI, ARIAL = r"C:\Windows\Fonts\calibri.ttf", r"C:\Windows\Fonts\arial.ttf"
WHITE = (1, 1, 1)

d = pymupdf.open(SRC)


def rgb(c):
    return ((c >> 16) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255)


def spans(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                out.append(s)
    return out


def put(page, s, dy=0.0, text=None):
    font = ARIAL if "Arial" in s["font"] else CALIBRI
    page.insert_text((s["origin"][0], s["origin"][1] + dy), s["text"] if text is None else text,
                     fontname="arl" if font == ARIAL else "cal", fontfile=font,
                     fontsize=s["size"], color=rgb(s["color"]))


def lines_of(sp, x_min, y_min, y_max):
    """Group the spans of one bullet line (same y band) -> list of lists."""
    rows = {}
    for s in sp:
        if s["bbox"][0] >= x_min - 1 and y_min <= s["bbox"][1] <= y_max and s["text"] != "":
            rows.setdefault(round(s["origin"][1]), []).append(s)
    return [sorted(v, key=lambda s: s["bbox"][0]) for _, v in sorted(rows.items())]


def rebuild_list(page, sp, x0, y0, y1, drop, shift_pitch, first_line_y):
    """Redact the sub-list lines between y0..y1 (x >= x0) and re-insert the kept ones, closing the gaps."""
    rows = lines_of(sp, x0, y0, y1)
    keep = [r for r in rows if not any(any(w in s["text"] for w in drop) for s in r)]
    page.add_redact_annot(pymupdf.Rect(x0 - 2, y0 - 2, 372 if page.number == 36 else 378, y1 + 30), fill=WHITE)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
    for k, r in enumerate(keep):
        dy = (first_line_y + k * shift_pitch) - r[0]["origin"][1]
        for s in r:
            put(page, s, dy)
    return len(rows), len(keep)


# ---- page 37: structural list
p = d[36]
sp = spans(p)
n_all, n_keep = rebuild_list(p, sp, 92.0, 259.0, 477.0, ["Façade"], 31.2, [r for r in lines_of(sp, 92.0, 259.0, 477.0)][0][0]["origin"][1])
assert (n_all, n_keep) == (7, 6), (n_all, n_keep)
seven = next(s for s in sp if s["text"].startswith("Seven structural"))
p.add_redact_annot(pymupdf.Rect(seven["bbox"]), fill=WHITE)
p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
put(p, seven, text="Six structural ")

# ---- page 38: behavioral list
p = d[37]
sp = spans(p)
n_all, n_keep = rebuild_list(p, sp, 92.0, 174.0, 438.0, ["Interpreter", "Chain of Responsibility", "Command"], 24.0,
                             lines_of(sp, 92.0, 174.0, 438.0)[0][0]["origin"][1])
assert (n_all, n_keep) == (11, 8), (n_all, n_keep)
eleven = next(s for s in sp if s["text"].startswith("11 behavioral"))
p.add_redact_annot(pymupdf.Rect(eleven["bbox"]), fill=WHITE)
p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
put(p, eleven, text="8 behavioral patterns")

# ---- page 177: cover the Facade sentence (it is part of the slide image; background is white)
p = d[176]
p.draw_rect(pymupdf.Rect(247, 288, 472, 358), color=None, fill=WHITE, overlay=True)

# ---- bookmarks, then delete pages 376-386
DEL_FROM, DEL_TO = 376, 386          # 1-based, inclusive
n_del = DEL_TO - DEL_FROM + 1
toc = d.get_toc()
toc = [[l, t, (pg - n_del if pg > DEL_TO else pg)] for l, t, pg in toc if not (DEL_FROM <= pg <= DEL_TO)]
d.delete_pages(DEL_FROM - 1, DEL_TO - 1)
d.set_toc(toc)
d.save(OUT, garbage=4, deflate=True)
print("saved", OUT, "pages", d.page_count)
