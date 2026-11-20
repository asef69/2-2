"""
tools.py — helpers for reading course material.

  python -P tools.py text   <pdf> [first] [last]          page-by-page text (1-based, inclusive)
  python -P tools.py render <pdf> <outdir> [first] [last] [--dpi 110]
                                                          PNG per page → view with the Read tool
                                                          (use for scanned papers / diagram slides)
  python -P tools.py sheet  <pdf> <out.png> <first> <last> [--cols 3] [--dpi 60]
                                                          contact sheet: many slides in one image
  python -P tools.py pptx   <pptx> [<outdir>]             slide-by-slide text (+ images exported to outdir)
  python -P tools.py docx   <docx>                         dump a .docx as plain text (headings marked)
"""
import os
import sys

import pymupdf


def _range(doc, a, b):
    a = int(a) if a else 1
    b = int(b) if b else doc.page_count
    return range(a, min(b, doc.page_count) + 1)


def cmd_text(pdf, a=None, b=None):
    d = pymupdf.open(pdf)
    for i in _range(d, a, b):
        print(f"\n===== page {i} =====")
        print(d[i - 1].get_text().strip())


def cmd_render(pdf, outdir, a=None, b=None, dpi=110):
    d = pymupdf.open(pdf)
    os.makedirs(outdir, exist_ok=True)
    for i in _range(d, a, b):
        p = os.path.join(outdir, f"p{i:03d}.png")
        d[i - 1].get_pixmap(dpi=dpi).save(p)
        print(p)


def cmd_sheet(pdf, out, a, b, cols=3, dpi=60):
    d = pymupdf.open(pdf)
    pages = list(_range(d, a, b))
    pix = [d[i - 1].get_pixmap(dpi=dpi) for i in pages]
    w = max(p.width for p in pix)
    h = max(p.height for p in pix)
    rows = (len(pix) + cols - 1) // cols
    sheet = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, cols * w, rows * (h + 18)), 0)
    sheet.clear_with(255)
    out_doc = pymupdf.open()
    page = out_doc.new_page(width=cols * w, height=rows * (h + 18))
    for k, (pg, px) in enumerate(zip(pages, pix)):
        x, y = (k % cols) * w, (k // cols) * (h + 18)
        page.insert_image(pymupdf.Rect(x, y + 16, x + px.width, y + 16 + px.height), pixmap=px)
        page.insert_text((x + 4, y + 12), f"p{pg}", fontsize=12, color=(0.8, 0, 0))
        page.draw_rect(pymupdf.Rect(x, y + 16, x + px.width, y + 16 + px.height), color=(0.6, 0.6, 0.6), width=0.5)
    page.get_pixmap(dpi=72).save(out)
    print(out)


def cmd_pptx(path, outdir=None):
    from pptx import Presentation
    prs = Presentation(path)
    if outdir:
        os.makedirs(outdir, exist_ok=True)
    for i, slide in enumerate(prs.slides, 1):
        print(f"\n===== slide {i} =====")
        for sh in slide.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip():
                print(sh.text_frame.text.strip())
            if getattr(sh, "has_table", False) and sh.has_table:
                for row in sh.table.rows:
                    print(" | ".join(c.text for c in row.cells))
            if outdir and sh.shape_type == 13:  # picture
                ext = sh.image.ext
                fn = os.path.join(outdir, f"s{i:03d}_{sh.shape_id}.{ext}")
                with open(fn, "wb") as f:
                    f.write(sh.image.blob)
                print(f"[image → {fn}]")
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame.text.strip():
            print("[notes] " + slide.notes_slide.notes_text_frame.text.strip())


def cmd_docx(path):
    from docx import Document
    d = Document(path)
    body = d.element.body
    for el in body.iterchildren():
        tag = el.tag.split("}")[1]
        if tag == "p":
            from docx.text.paragraph import Paragraph
            p = Paragraph(el, d)
            t = p.text.strip()
            if not t:
                if el.xpath(".//pic:pic"):
                    print("[FIGURE]")
                continue
            st = p.style.name if p.style is not None else ""
            pre = {"Heading 1": "# ", "Heading 2": "## ", "Heading 3": "### "}.get(st, "")
            print(pre + t)
        elif tag == "tbl":
            from docx.table import Table
            for row in Table(el, d).rows:
                cells = []
                for c in row.cells:
                    if not cells or c.text != cells[-1]:
                        cells.append(c.text.replace("\n", " / "))
                print("| " + " | ".join(cells) + " |")
            print()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:]]
    opts = {}
    for flag in ("--dpi", "--cols"):
        if flag in args:
            k = args.index(flag)
            opts[flag[2:]] = int(args[k + 1])
            del args[k:k + 2]
    cmd, rest = args[0], args[1:]
    {"text": cmd_text, "render": cmd_render, "sheet": cmd_sheet, "pptx": cmd_pptx, "docx": cmd_docx}[cmd](*rest, **opts)
