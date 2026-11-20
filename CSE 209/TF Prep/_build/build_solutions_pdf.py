"""Build CSE209_ART_Last5_Topicwise_Solutions.pdf: every question of the ART tracker (2019-20 … 2023-24),
grouped by topic, each followed by a worked solution.   Run with the python that has reportlab + pymupdf."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")
import matplotlib
import pymupdf
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, PageBreak, PageTemplate, Paragraph,
                                Preformatted, Spacer, Table, TableStyle)
from reportlab.platypus.flowables import Flowable

import sol_data1, sol_data2, sol_data3
from common import QUESTIONS, REPO, CH2, CH3

FD = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
for nm, f in (("DV", "DejaVuSans.ttf"), ("DV-B", "DejaVuSans-Bold.ttf"), ("DV-I", "DejaVuSans-Oblique.ttf"),
              ("DV-BI", "DejaVuSans-BoldOblique.ttf"), ("DVM", "DejaVuSansMono.ttf")):
    pdfmetrics.registerFont(TTFont(nm, os.path.join(FD, f)))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-BI")

NAVY, BLUE = colors.HexColor("#1F3864"), colors.HexColor("#2E75B6")
CORAL, GOLD = colors.HexColor("#E0674F"), colors.HexColor("#E0A800")
GREEN, GREY = colors.HexColor("#2E7D32"), colors.HexColor("#F2F2F2")

base = ParagraphStyle("base", fontName="DV", fontSize=8.8, leading=12.2, spaceAfter=3)
qst = ParagraphStyle("q", parent=base, fontSize=9, leading=12.5)
tcell = ParagraphStyle("tc", parent=base, fontSize=7.8, leading=10, spaceAfter=0)
thead = ParagraphStyle("th", parent=tcell, fontName="DV-B", textColor=colors.white)
code_st = ParagraphStyle("code", fontName="DVM", fontSize=7.6, leading=9.6)
ans_st = ParagraphStyle("ans", parent=base, fontName="DV", backColor=colors.HexColor("#E8F3E8"), borderPadding=(4, 5, 4, 5),
                        spaceBefore=4, spaceAfter=7)
h_topic = ParagraphStyle("ht", fontName="DV-B", fontSize=20, leading=24, textColor=NAVY, spaceAfter=6)
card_title = ParagraphStyle("ct", fontName="DV-B", fontSize=9.4, leading=12, textColor=colors.white)
card_sub = ParagraphStyle("cs", parent=card_title, fontName="DV", fontSize=7.6, textColor=colors.HexColor("#DDE6F2"))


def esc(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"`([^`]+)`", r'<font name="DVM">\1</font>', t)
    t = re.sub(r"\^\{([^}]*)\}", r"<super>\1</super>", t)
    t = re.sub(r"_\{([^}]*)\}", r"<sub>\1</sub>", t)
    return t


_imgs = {}


def img(key, caption, width=13.5 * cm):
    if key not in _imgs:
        pdf, page, clip = {"ch2_64": (CH2, 64, (0.1, 0.16, 0.86, 0.91)), "ch2_55": (CH2, 55, (0.2, 0.16, 0.86, 0.94)),
                           "ch3_6": (CH3, 6, (0.0, 0.12, 1.0, 0.92)), "ch3_7": (CH3, 7, (0.0, 0.18, 1.0, 0.82))}[key]
        d = pymupdf.open(pdf)
        pg = d[page - 1]
        r = pg.rect
        pix = pg.get_pixmap(dpi=170, clip=pymupdf.Rect(r.x0 + clip[0] * r.width, r.y0 + clip[1] * r.height,
                                                      r.x0 + clip[2] * r.width, r.y0 + clip[3] * r.height))
        _imgs[key] = (pix.tobytes("png"), pix.width / pix.height)
    data, ar = _imgs[key]
    w = min(width, 14 * cm)
    im = Image(io.BytesIO(data), width=w, height=w / ar)
    return KeepTogether([Spacer(1, 3), im, Paragraph(f"<i>{esc(caption)}</i>", ParagraphStyle("cap", parent=base, fontSize=7.4, alignment=TA_CENTER, textColor=colors.grey))])


def table(hdr, rows, widths):
    W = 17.4 * cm
    data = [[Paragraph(esc(h), thead) for h in hdr]] + [[Paragraph(esc(str(c)), tcell) for c in r] for r in rows]
    t = Table(data, colWidths=[W * w / 100 for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F8FC")]),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return t


def render(items):
    out, codebuf = [], []

    def flush():
        if codebuf:
            t = Table([[Preformatted("\n".join(codebuf), code_st)]], colWidths=[17.0 * cm])
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GREY), ("LINEBEFORE", (0, 0), (0, -1), 2, colors.HexColor("#8C8C8C")),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
            out.append(t)
            out.append(Spacer(1, 4))
            codebuf.clear()

    def add(it):
        if callable(it):
            for x in it():
                add(x)
        elif isinstance(it, str) and it.startswith("| "):
            codebuf.append(it[2:])
        else:
            flush()
            if isinstance(it, tuple) and it[0] == "T":
                out.append(table(it[1], it[2], it[3]))
                out.append(Spacer(1, 4))
            elif isinstance(it, tuple) and it[0] == "IMG":
                out.append(img(it[1], it[2]))
            elif isinstance(it, tuple):  # a table given directly (ADDR_TABLE style)
                out.append(table(it[1], it[2], it[3]))
                out.append(Spacer(1, 4))
            elif it.startswith("A: "):
                out.append(Paragraph("<b>Answer.</b> " + esc(it[3:]), ans_st))
            else:
                out.append(Paragraph(esc(it), base))

    for it in items:
        add(it)
    flush()
    return out


class Bookmark(Flowable):
    def __init__(self, key, title, level=0):
        super().__init__()
        self.key, self.title, self.level = key, title, level

    def wrap(self, *a):
        return 0, 0

    def draw(self):
        self.canv.bookmarkPage(self.key)
        self.canv.addOutlineEntry(self.title, self.key, level=self.level, closed=False)


def card(q, sol):
    badge = "" if q["marks"] is None else (f"{q['marks']:g}" if isinstance(q["marks"], (int, float)) else str(q["marks"]))
    left = Paragraph(f"{q['year'].replace('-', '–')} • Q{q['qno']}", card_title)
    right = Paragraph(f"{q['course']} • TF page {q['page']}" + (f"  •  MARKS {badge}" if badge else ""), card_sub)
    hdr = Table([[left, right]], colWidths=[7.6 * cm, 9.8 * cm])
    hdr.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), BLUE), ("ALIGN", (1, 0), (1, 0), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                             ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    qbox = Table([[Paragraph(esc(sol["q"]), qst)]], colWidths=[17.4 * cm])
    qbox.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7F9FC")), ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9D6E8")),
                              ("LEFTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    solhdr = Paragraph('<font color="#2E7D32"><b>SOLUTION</b></font>', ParagraphStyle("sh", parent=base, fontSize=8, spaceBefore=5, spaceAfter=2))
    body = render(sol["s"])
    return [KeepTogether([hdr, qbox, solhdr] + body[:1]), *body[1:], Spacer(1, 12)]


TOPICS = [(1, "Computer Abstractions and Performance", "Chapter 1 · Lessons L1–L4"),
          (2, "Arithmetic Logic Unit (ALU) Design", "ALU Design · Lessons L6–L9"),
          (3, "Instructions: Language of the Computer", "Chapter 2 · Lessons L10–L18"),
          (4, "Arithmetic for Computers", "Chapter 3 · Lessons L19–L22"),
          ("OUT", "Outside the Short Slides (textbook)", "Division, FP code, SPEC, rounding, signed multiplication, subword parallelism — answered from the textbook")]


def footer(c, d):
    c.saveState()
    c.setFont("DV", 7.5)
    c.setFillColor(colors.grey)
    c.drawString(1.8 * cm, 1.1 * cm, "CSE 209 • Computer Architecture • Tushar Sir part (ART) • last five term finals")
    c.drawRightString(A4[0] - 1.8 * cm, 1.1 * cm, str(d.page))
    c.restoreState()


def main():
    SOL = {}
    for m in (sol_data1, sol_data2, sol_data3):
        SOL.update(m.S)
    qs = [q for q in QUESTIONS if int(q["year"][:4]) >= 2019]
    missing = [(q["year"], q["course"], q["qno"]) for q in qs if (q["year"], q["course"], q["qno"]) not in SOL]
    extra = [k for k in SOL if k not in {(q["year"], q["course"], q["qno"]) for q in qs}]
    print("questions", len(qs), "missing", missing, "extra", extra)
    assert not missing and not extra
    out = os.path.join(REPO, "CSE 209", "TF Prep", "CSE209_ART_Last5_Topicwise_Solutions.pdf")
    doc = BaseDocTemplate(out, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.6 * cm, bottomMargin=1.8 * cm,
                          title="CSE 209 — ART part: topic-wise solutions (last five term finals)", author="Claude")
    doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")], onPage=footer)])
    st = []
    st += [Spacer(1, 4 * cm), Paragraph("BUET • CSE 209", ParagraphStyle("c1", fontName="DV-B", fontSize=13, textColor=BLUE)),
           Paragraph("Computer Architecture", ParagraphStyle("c2", fontName="DV-B", fontSize=34, leading=40, textColor=NAVY)),
           Paragraph("Tushar Sir's part (ART)", ParagraphStyle("c3", fontName="DV-B", fontSize=16, textColor=NAVY, spaceAfter=14)),
           Paragraph("Topic-wise questions with complete worked solutions", ParagraphStyle("c4", fontName="DV", fontSize=13, textColor=colors.grey, spaceAfter=24)),
           Paragraph(f"<b>{len(qs)}</b> question cards from the last five term finals — 2019–20 to 2023–24 (CSE 305 and CSE 209) — exactly the questions of "
                     "CSE209_ART_TF_Practice_Tracker.xlsx. Each question is followed by its solution; numerical answers, ALU designs, assembly programs, "
                     "encodings and traces were checked by script (all 4-bit ALU inputs simulated, every MIPS program run on a simulator).", base),
           Spacer(1, 6),
           Paragraph("Topics follow the course slides (Chapter 1, ALU Design, Chapter 2, Chapter 3). Questions on material outside the short slides are kept in a "
                     "separate, flagged topic at the end. Inside each topic the most recent paper comes first. Page numbers (\"TF page\") refer to "
                     "CSE209 ALL TF QUES (TF209).pdf. Two questions are shared with the RS part (2022–23 Q11(b) and Q12(c)); only the ART halves are solved here.", base),
           Spacer(1, 8), Paragraph("Credit: Claude", ParagraphStyle("cr", parent=base, textColor=colors.grey)), PageBreak()]
    n = 0
    for key, title, sub in TOPICS:
        rows = [q for q in qs if q["file"] == key]
        rows.sort(key=lambda q: (-int(q["year"][:4]), q["course"] != "CSE 209", q["qno"]))
        st += [Bookmark(f"t{key}", title), Paragraph(title, h_topic), Paragraph(f"{sub} · {len(rows)} questions", ParagraphStyle("sb", parent=base, textColor=colors.grey, spaceAfter=10))]
        for q in rows:
            st += [Bookmark(f"q{n}", f"{q['year']} Q{q['qno']}", 1)] + card(q, SOL[(q["year"], q["course"], q["qno"])])
            n += 1
        st.append(PageBreak())
    st.pop()
    doc.build(st)
    print(out, n, "cards")


main()
