"""
notes_lib.py — builds TF-prep lesson notes (.docx) in the exact style of the
CSE 209 RS-part reference notes (CSE 209/TF Prep/notes/*.docx).

Inline markup accepted by every text argument:
    **bold**   *italic*   `mono`   ^{sup}   _{sub}
Example:
    from notes_lib import Notes
    n = Notes(course="CSE 211", course_title="Theory of Computation",
              topic="Deterministic Finite Automata",
              part_label="Hakim Sir's portion", part_tag="Hakim Sir part",
              out_path=r"...\\CSE 211\\TF Prep\\notes\\CSE211_Hakim_DFA_Notes.docx")
    n.front_matter(contents=[("Exam Map — What the TF Papers Ask", "DFA questions and how much they matter"),
                             ("Lesson 1 — ...", "...")],
                   source_note="Slide numbers refer to Lec03 - DFA.pdf (42 slides).")
    n.h1("Exam Map — What the TF Papers Ask"); n.table([...], [...]); n.callout("focus", "...")
    n.lesson("Lesson 1 — Formal Definition of a DFA", "Slides 2–9")
    ...
    n.save()
"""
import io
import os
import re

import pymupdf
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Twips

NAVY = "1F3864"
BLUE = "1F4E79"
SKY = "2E75B6"
GREY = "595959"
LIGHT = "8C8C8C"
PURPLE = "5B2C83"
GREEN = "2E7D32"

CALLOUTS = {
    # kind: (label, border colour, fill, label colour)
    "focus": ("EXAM FOCUS", "E08A00", "FFF4E0", "B26B00"),
    "memorize": ("MEMORIZE", "2E7D32", "EAF5EA", "2E7D32"),
    "trap": ("TRAP", "C62828", "FDECEA", "C62828"),
    "answer": ("EXAM-READY ANSWER", "1F4E79", "EAF1FB", "1F4E79"),
    "note": ("NOTE", "7F7F7F", "F2F2F2", "595959"),
}

TEXT_W_TW = 9752  # usable width in twips (A4, 1077-twip margins)
TEXT_W_CM = 17.2

_TOKEN = re.compile(r"(\*\*.+?\*\*|\*[^*\s][^*]*?\*|`[^`]+`|\^\{[^}]*\}|_\{[^}]*\})")


# ---------------------------------------------------------------- xml helpers
def _set(el, tag, **attrs):
    child = el.find(qn(tag))
    if child is None:
        child = OxmlElement(tag)
        el.append(child)
    for k, v in attrs.items():
        child.set(qn(k), str(v))
    return child


def _ppr_border(p, sides, sz=4, color="BFBFBF", space=4):
    pPr = p._p.get_or_add_pPr()
    bdr = pPr.find(qn("w:pBdr"))
    if bdr is None:
        bdr = OxmlElement("w:pBdr")
        pPr.append(bdr)
    for s in sides:
        e = OxmlElement(f"w:{s}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), str(space))
        e.set(qn("w:color"), color)
        bdr.append(e)


def _ppr_shade(p, fill):
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    pPr.append(shd)


def _spacing(p, before=None, after=None, line=None):
    pf = p.paragraph_format
    if before is not None:
        pf.space_before = Twips(before)
    if after is not None:
        pf.space_after = Twips(after)
    if line is not None:
        pf.line_spacing = line


def _cell_props(cell, fill=None, borders=None, margins=None, width_tw=None):
    tcPr = cell._tc.get_or_add_tcPr()
    if width_tw:
        _set(tcPr, "w:tcW", **{"w:type": "dxa", "w:w": width_tw})
    if borders:
        tb = OxmlElement("w:tcBorders")
        for side, (sz, color) in borders.items():
            e = OxmlElement(f"w:{side}")
            e.set(qn("w:val"), "single" if sz else "nil")
            e.set(qn("w:sz"), str(sz or 0))
            e.set(qn("w:space"), "0")
            e.set(qn("w:color"), color)
            tb.append(e)
        tcPr.append(tb)
    if fill:
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), fill)
        tcPr.append(shd)
    if margins:
        mar = OxmlElement("w:tcMar")
        for side, w in zip(("top", "left", "bottom", "right"), margins):
            e = OxmlElement(f"w:{side}")
            e.set(qn("w:w"), str(w))
            e.set(qn("w:type"), "dxa")
            mar.append(e)
        tcPr.append(mar)


def _fixed_table(doc, rows, cols, widths_tw):
    t = doc.add_table(rows=rows, cols=cols)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    tblPr = t._tbl.tblPr
    _set(tblPr, "w:tblW", **{"w:type": "dxa", "w:w": sum(widths_tw)})
    _set(tblPr, "w:tblLayout", **{"w:type": "fixed"})
    grid = t._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths_tw):
        gc.set(qn("w:w"), str(w))
    for r in t.rows:
        for c, w in zip(r.cells, widths_tw):
            _cell_props(c, width_tw=w)
    return t


def _no_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:cantSplit"))


def _repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:tblHeader"))


def add_runs(p, text, size=None, color=None, bold=None, italic=None, font=None):
    """Append inline-marked-up text to paragraph p."""
    for part in _TOKEN.split(text):
        if not part:
            continue
        b, i, mono, sup, sub = bold, italic, False, False, False
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            part, b = part[2:-2], True
        elif part.startswith("`") and part.endswith("`"):
            part, mono = part[1:-1], True
        elif part.startswith("^{"):
            part, sup = part[2:-1], True
        elif part.startswith("_{"):
            part, sub = part[2:-1], True
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            part, i = part[1:-1], True
        # nested bold inside italic etc. is not supported — keep markup flat
        r = p.add_run(part)
        if b:
            r.bold = True
        if i:
            r.italic = True
        if mono:
            r.font.name = "Consolas"
            r._element.rPr.rFonts.set(qn("w:hAnsi"), "Consolas")
        if sup:
            r.font.superscript = True
        if sub:
            r.font.subscript = True
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        if font:
            r.font.name = font
    return p


# ---------------------------------------------------------------- the builder
class Notes:
    def __init__(self, course, course_title, topic, part_label, part_tag, out_path,
                 tagline="Lesson notes · Exam approach · TF practice with solutions · Quick notes"):
        """
        course      "CSE 211"
        course_title "Theory of Computation"
        topic       "Deterministic Finite Automata"  (subtitle; one slide deck / chapter)
        part_label  "Hakim Sir's portion"   (goes in the tagline brackets)
        part_tag    "Hakim Sir part"        (goes in the running header)
        """
        self.course, self.course_title, self.topic = course, course_title, topic
        self.part_label, self.part_tag, self.out_path = part_label, part_tag, out_path
        self.tagline = tagline
        self._fig_dpi = 200
        self.doc = Document()
        self._setup_styles()
        self._setup_page()

    # ---------------------------------------------------------- setup
    def _setup_styles(self):
        st = self.doc.styles
        normal = st["Normal"]
        normal.font.name = "Arial"
        normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
        normal.element.rPr.rFonts.set(qn("w:cs"), "Arial")
        normal.font.size = Pt(10.5)
        pf = normal.paragraph_format
        pf.space_before, pf.space_after, pf.line_spacing = Twips(0), Twips(100), 1.15
        for name, size, color, before, after in (
            ("Heading 1", 18, NAVY, 0, 160),
            ("Heading 2", 13.5, BLUE, 320, 100),
            ("Heading 3", 11.5, SKY, 220, 60),
        ):
            s = st[name]
            s.font.name = "Arial"
            rf = s.element.rPr.rFonts
            for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
                rf.set(qn(a), "Arial")
            for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
                if rf.get(qn(a)) is not None:
                    del rf.attrib[qn(a)]
            s.font.size = Pt(size)
            s.font.bold = True
            s.font.italic = False
            s.font.color.rgb = RGBColor.from_string(color)
            s.paragraph_format.space_before = Twips(before)
            s.paragraph_format.space_after = Twips(after)
            s.paragraph_format.keep_with_next = True
        for name in ("List Bullet", "List Number"):
            st[name].paragraph_format.space_after = Twips(40)

    def _setup_page(self):
        sec = self.doc.sections[0]
        sec.page_width, sec.page_height = Twips(11906), Twips(16838)
        sec.top_margin, sec.bottom_margin = Twips(964), Twips(907)
        sec.left_margin = sec.right_margin = Twips(1077)
        sec.header_distance = sec.footer_distance = Twips(454)
        hp = sec.header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        _ppr_border(hp, ["bottom"], sz=4, color="BFBFBF", space=2)
        r = hp.add_run(f"{self.course}  ·  {self.topic}  ·  {self.part_tag}")
        r.font.size, r.font.color.rgb = Pt(8), RGBColor.from_string(LIGHT)
        fp = sec.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = fp.add_run()
        r.font.size, r.font.color.rgb = Pt(8.5), RGBColor.from_string(LIGHT)
        for t, txt in (("begin", None), (None, "PAGE"), ("end", None)):
            if t:
                fc = OxmlElement("w:fldChar")
                fc.set(qn("w:fldCharType"), t)
                r._r.append(fc)
            else:
                it = OxmlElement("w:instrText")
                it.set(qn("xml:space"), "preserve")
                it.text = txt
                r._r.append(it)

    # ---------------------------------------------------------- front matter
    def front_matter(self, contents, source_note=None):
        """Title block + 'How to Read These Notes' legend + Contents (+ optional NOTE)."""
        d = self.doc
        p = d.add_paragraph()
        _spacing(p, before=200, after=40)
        add_runs(p, f"{self.course} — {self.course_title}", size=24, color=NAVY, bold=True)
        p = d.add_paragraph()
        _spacing(p, after=40)
        add_runs(p, self.topic, size=13, color=BLUE, bold=True)
        p = d.add_paragraph()
        _spacing(p, after=80)
        _ppr_border(p, ["bottom"], sz=12, color=NAVY, space=6)
        add_runs(p, f"{self.tagline} ({self.part_label})", size=10.5, color=GREY, italic=True)

        d.add_paragraph("How to Read These Notes", style="Heading 2")
        legend = [
            ("EXAM FOCUS", *CALLOUTS["focus"][1:], "Exam importance, where it appears in the TF collection"),
            ("MEMORIZE", *CALLOUTS["memorize"][1:], "Rules, tables and formulas to memorize"),
            ("TRAP", *CALLOUTS["trap"][1:], "Common mistakes and exam traps"),
            ("EXAM-READY ANSWER", *CALLOUTS["answer"][1:], "Model wording you can write in the exam"),
            ("NOTE", *CALLOUTS["note"][1:], "Extra explanation / clarification"),
            ("Grey box, monospace", "8C8C8C", "F2F2F2", "404040", "Code, worked tables, derivations and hand-drawn sketches"),
            ("Centered grey box", "BFBFBF", "F7F7F7", "404040", "Formula to remember / final numerical result"),
            ("Purple heading / ✔ green", PURPLE, "F3EEF8", PURPLE, "Practice questions / their solutions"),
        ]
        t = _fixed_table(d, len(legend), 2, [2600, 7152])
        for row, (lab, border, fill, lcol, desc) in zip(t.rows, legend):
            c0, c1 = row.cells
            _cell_props(c0, fill=fill, borders={"top": (0, "FFFFFF"), "left": (30, border),
                                                 "bottom": (0, "FFFFFF"), "right": (0, "FFFFFF")},
                        margins=(30, 110, 30, 80))
            _cell_props(c1, borders={s: (0, "FFFFFF") for s in ("top", "left", "bottom", "right")},
                        margins=(30, 110, 30, 80))
            p0 = c0.paragraphs[0]
            _spacing(p0, after=0)
            add_runs(p0, lab, size=8.5, color=lcol, bold=True)
            p1 = c1.paragraphs[0]
            _spacing(p1, after=0)
            add_runs(p1, desc, size=10)

        d.add_paragraph("Contents", style="Heading 2")
        for title, desc in contents:
            p = d.add_paragraph()
            _spacing(p, after=20)
            p.paragraph_format.left_indent = Twips(113)
            add_runs(p, title, size=10.5, color=NAVY, bold=True)
            if desc:
                add_runs(p, f"  —  {desc}", size=9.5, color=GREY)
        if source_note:
            self.callout("note", source_note)

    # ---------------------------------------------------------- headings
    def page_break(self):
        self.doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    def h1(self, text, new_page=True):
        if new_page:
            p = self.doc.add_paragraph("", style="Heading 1")
            p.paragraph_format.page_break_before = True
            add_runs(p, text)
        else:
            p = self.doc.add_paragraph("", style="Heading 1")
            add_runs(p, text)
        _ppr_border(p, ["bottom"], sz=12, color=NAVY, space=4)
        return p

    def lesson(self, title, source=None):
        """New page, 'Lesson N — Title', then grey italic source line (e.g. 'Slides 2–9 (§1.2)')."""
        self.h1(title)
        if source:
            self.source(source)

    def source(self, text):
        p = self.doc.add_paragraph()
        _spacing(p, after=120)
        add_runs(p, text, size=9, color=LIGHT, italic=True)

    def h2(self, text, color=None):
        p = self.doc.add_paragraph("", style="Heading 2")
        add_runs(p, text, color=color)
        return p

    def h3(self, text, color=None):
        p = self.doc.add_paragraph("", style="Heading 3")
        add_runs(p, text, color=color)
        return p

    # ---------------------------------------------------------- body text
    def p(self, text, size=None, color=None, align=None, after=None):
        para = self.doc.add_paragraph()
        add_runs(para, text, size=size, color=color)
        if align == "center":
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if after is not None:
            _spacing(para, after=after)
        return para

    def bullets(self, items, level=0):
        for it in items:
            if isinstance(it, (list, tuple)):
                self.bullets(it, level + 1)
                continue
            para = self.doc.add_paragraph(style="List Bullet" if level == 0 else "List Bullet 2")
            add_runs(para, it)

    def numbered(self, items):
        """Manual numbering (1. 2. 3.) with hanging indent — survives Google Docs import."""
        for k, it in enumerate(items, 1):
            para = self.doc.add_paragraph()
            para.paragraph_format.left_indent = Twips(482)
            para.paragraph_format.first_line_indent = Twips(-369)
            _spacing(para, after=50)
            add_runs(para, f"{k}.\t{it}")
            pPr = para._p.get_or_add_pPr()
            tabs = OxmlElement("w:tabs")
            tab = OxmlElement("w:tab")
            tab.set(qn("w:val"), "left")
            tab.set(qn("w:pos"), "482")
            tabs.append(tab)
            pPr.append(tabs)

    # ---------------------------------------------------------- boxes
    def callout(self, kind, text, extra=None):
        """kind ∈ focus | memorize | trap | answer | note.
        text: first paragraph (inline markup). extra: list of further paragraphs/bullets ('• ...')."""
        label, border, fill, lcol = CALLOUTS[kind]
        t = _fixed_table(self.doc, 1, 1, [TEXT_W_TW])
        _no_split(t.rows[0])
        cell = t.rows[0].cells[0]
        _cell_props(cell, fill=fill,
                    borders={"top": (4, fill), "left": (30, border), "bottom": (4, fill), "right": (4, fill)},
                    margins=(70, 170, 70, 140))
        p0 = cell.paragraphs[0]
        _spacing(p0, after=0)
        add_runs(p0, label + "   ", size=8.5, color=lcol, bold=True)
        add_runs(p0, text)
        for ex in extra or []:
            pe = cell.add_paragraph()
            _spacing(pe, before=40, after=0)
            add_runs(pe, ex)
        self._gap()

    def _gap(self, after=60):
        p = self.doc.add_paragraph()
        _spacing(p, before=0, after=after)
        p.paragraph_format.line_spacing = Pt(6)

    def code(self, lines, size=9):
        """Grey monospace box: code, bit layouts, worked tables in text, ASCII sketches."""
        if isinstance(lines, str):
            lines = lines.split("\n")
        t = _fixed_table(self.doc, 1, 1, [TEXT_W_TW])
        _no_split(t.rows[0])
        cell = t.rows[0].cells[0]
        _cell_props(cell, fill="F2F2F2",
                    borders={"top": (4, "D9D9D9"), "left": (18, "8C8C8C"), "bottom": (4, "D9D9D9"),
                             "right": (4, "D9D9D9")},
                    margins=(80, 170, 80, 140))
        first = True
        for ln in lines:
            para = cell.paragraphs[0] if first else cell.add_paragraph()
            first = False
            _spacing(para, after=0, line=1.0)
            r = para.add_run(ln if ln else " ")
            r.font.name = "Consolas"
            r._element.rPr.rFonts.set(qn("w:hAnsi"), "Consolas")
            r._element.rPr.rFonts.set(qn("w:cs"), "Consolas")
            r.font.size = Pt(size)
        self._gap()

    def formula(self, lines, size=11):
        """Centered grey box with bold lines: key formula / final numerical answer."""
        if isinstance(lines, str):
            lines = [lines]
        n = len(lines)
        for k, ln in enumerate(lines):
            para = self.doc.add_paragraph()
            sides = ["left", "right"] + (["top"] if k == 0 else []) + (["bottom"] if k == n - 1 else [])
            _ppr_border(para, sides, sz=4, color="BFBFBF", space=4)
            _ppr_shade(para, "F7F7F7")
            _spacing(para, before=80 if k == 0 else 0, after=80 if k == n - 1 else 20)
            para.paragraph_format.left_indent = Twips(1417)
            para.paragraph_format.right_indent = Twips(1417)
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_runs(para, ln, size=size, bold=True)

    # ---------------------------------------------------------- tables
    def table(self, headers, rows, widths_cm=None, font_size=9.5, first_col_bold=False, zebra=True):
        """Blue header row, thin grey grid. widths_cm must sum to ≤ 17.2."""
        ncol = len(headers)
        if widths_cm is None:
            widths_cm = [TEXT_W_CM / ncol] * ncol
        widths_tw = [int(w * 567) for w in widths_cm]
        t = _fixed_table(self.doc, len(rows) + 1, ncol, widths_tw)
        grid = {s: (4, "BFBFBF") for s in ("top", "left", "bottom", "right")}
        _repeat_header(t.rows[0])
        for c, h in zip(t.rows[0].cells, headers):
            _cell_props(c, fill="DCE6F2", borders=grid, margins=(40, 100, 40, 100))
            para = c.paragraphs[0]
            _spacing(para, after=0)
            add_runs(para, h, size=font_size, bold=True, color=NAVY)
        for ri, row in enumerate(rows, 1):
            _no_split(t.rows[ri])
            for ci, (c, val) in enumerate(zip(t.rows[ri].cells, row)):
                fill = "F7F9FC" if zebra and ri % 2 == 0 else None
                _cell_props(c, fill=fill, borders=grid, margins=(40, 100, 40, 100))
                parts = str(val).split("\n")
                for k, part in enumerate(parts):
                    para = c.paragraphs[0] if k == 0 else c.add_paragraph()
                    _spacing(para, after=0)
                    add_runs(para, part, size=font_size, bold=True if (first_col_bold and ci == 0) else None)
        self._gap(80)
        return t

    # ---------------------------------------------------------- figures
    def figure_from_pdf(self, pdf_path, page, caption, clip=None, width_cm=12.0, dpi=None):
        """Render one slide/page (1-based) of a PDF, optionally cropped.
        clip = (x0, y0, x1, y1) as FRACTIONS of the page (0–1), e.g. (0, 0.15, 1, 0.9)."""
        doc = pymupdf.open(pdf_path)
        pg = doc[page - 1]
        rect = pg.rect
        kw = {"dpi": dpi or self._fig_dpi}
        if clip:
            x0, y0, x1, y1 = clip
            kw["clip"] = pymupdf.Rect(rect.x0 + x0 * rect.width, rect.y0 + y0 * rect.height,
                                      rect.x0 + x1 * rect.width, rect.y0 + y1 * rect.height)
        pix = pg.get_pixmap(**kw)
        self.figure_bytes(pix.tobytes("png"), caption, width_cm)

    def figure_image(self, image_path, caption, width_cm=12.0):
        with open(image_path, "rb") as f:
            self.figure_bytes(f.read(), caption, width_cm)

    def figure_bytes(self, png_bytes, caption, width_cm=12.0):
        para = self.doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.keep_with_next = True
        _spacing(para, before=120, after=40)
        para.add_run().add_picture(io.BytesIO(png_bytes), width=Cm(min(width_cm, TEXT_W_CM)))
        cap = self.doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _spacing(cap, after=200)
        add_runs(cap, caption, size=9, color=GREY, italic=True)

    # ---------------------------------------------------------- practice
    def exam_approach(self, steps):
        self.h2("Exam Approach")
        self.numbered(steps)

    def practice(self, lesson_label, provenance, questions):
        """Purple 'Practice — Lesson N' heading, grey provenance line
        (e.g. '(a) Actual — 2019-20 Q5(b). (b) Adapted — 2016-17 Q6(a). (c) Constructed.'),
        then the questions ('(a) ...')."""
        self.h2(f"Practice — {lesson_label}", color=PURPLE)
        para = self.doc.add_paragraph()
        _spacing(para, after=120)
        add_runs(para, provenance, size=9, color=LIGHT, italic=True)
        for q in questions:
            para = self.doc.add_paragraph()
            _spacing(para, after=80)
            m = re.match(r"^(\([a-z0-9ivx]+\))\s*(.*)$", q, re.S)
            if m:
                add_runs(para, m.group(1) + " ", bold=True)
                add_runs(para, m.group(2))
            else:
                add_runs(para, q)

    def solution(self):
        """Green '✔ Solution' heading — follow with self.answer(...), self.formula, self.code, self.table ..."""
        self.h3("✔ Solution", color=GREEN)

    def answer(self, label, text):
        """'(a)' in bold followed by the answer text."""
        para = self.doc.add_paragraph()
        add_runs(para, f"**{label}** {text}")
        return para

    # ---------------------------------------------------------- quick notes
    def quick_notes(self, title, intro, groups, diagrams=None):
        """Quick Notes section on a new page.
        groups: [("L1 · Formal Definition", ["point", "point", ...]), ...]
        diagrams: optional [(pdf_path, page, caption, clip, width_cm), ...] → 'Key Diagrams to Reproduce'."""
        self.h1(title)
        para = self.doc.add_paragraph()
        _spacing(para, after=120)
        add_runs(para, intro, size=9.5, color=GREY, italic=True)
        for head, pts in groups:
            self.h2(head)
            self.bullets(pts)
        if diagrams:
            self.h2("Key Diagrams to Reproduce")
            for d in diagrams:
                pdf, page, cap = d[0], d[1], d[2]
                clip = d[3] if len(d) > 3 else None
                w = d[4] if len(d) > 4 else 11.0
                self.figure_from_pdf(pdf, page, cap, clip=clip, width_cm=w)

    # ---------------------------------------------------------- output
    def save(self):
        os.makedirs(os.path.dirname(self.out_path), exist_ok=True)
        self.doc.save(self.out_path)
        return self.out_path
