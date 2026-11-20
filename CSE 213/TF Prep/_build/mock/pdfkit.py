"""pdfkit.py - fonts, styles and small flowable helpers shared by the mock paper and its solutions."""
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageTemplate, Paragraph, Preformatted,
                                Spacer, Table, TableStyle)

W = r"C:\Windows\Fonts"
for n, f in (("Seg", "segoeui.ttf"), ("SegB", "segoeuib.ttf"), ("SegI", "segoeuii.ttf"), ("SegBI", "segoeuiz.ttf"),
             ("Mono", "consola.ttf"), ("MonoB", "consolab.ttf")):
    pdfmetrics.registerFont(TTFont(n, W + "\\" + f))
pdfmetrics.registerFontFamily("Seg", normal="Seg", bold="SegB", italic="SegI", boldItalic="SegBI")
pdfmetrics.registerFontFamily("Mono", normal="Mono", bold="MonoB", italic="Mono", boldItalic="MonoB")

INK = colors.Color(0.13, 0.15, 0.18)
ACC = colors.Color(0.10, 0.32, 0.62)
GREEN = colors.Color(0.09, 0.46, 0.27)
GREY = colors.Color(0.42, 0.45, 0.50)
RULE = colors.Color(0.80, 0.83, 0.87)
SHADE = colors.Color(0.955, 0.965, 0.975)
AMBER = colors.Color(0.98, 0.94, 0.82)

S = dict(
    body=ParagraphStyle("body", fontName="Seg", fontSize=9.3, leading=12.8, textColor=INK, spaceAfter=3.5, alignment=TA_LEFT),
    small=ParagraphStyle("small", fontName="Seg", fontSize=8.2, leading=11, textColor=GREY, spaceAfter=2),
    title=ParagraphStyle("title", fontName="SegB", fontSize=17, leading=21, textColor=INK, alignment=1, spaceAfter=2),
    sub=ParagraphStyle("sub", fontName="Seg", fontSize=10, leading=13, textColor=GREY, alignment=1, spaceAfter=2),
    sec=ParagraphStyle("sec", fontName="SegB", fontSize=12, leading=15, textColor=colors.white),
    q=ParagraphStyle("q", fontName="SegB", fontSize=11, leading=14, textColor=ACC, spaceBefore=9, spaceAfter=3, keepWithNext=1),
    h2=ParagraphStyle("h2", fontName="SegB", fontSize=10.5, leading=13.5, textColor=ACC, spaceBefore=6, spaceAfter=3, keepWithNext=1),
    lab=ParagraphStyle("lab", fontName="Seg", fontSize=9.3, leading=12.8, textColor=INK, spaceAfter=3.5, keepWithNext=1),
    sol=ParagraphStyle("sol", fontName="SegB", fontSize=9.3, leading=12, textColor=GREEN, spaceBefore=3, spaceAfter=2, keepWithNext=1),
    cell=ParagraphStyle("cell", fontName="Seg", fontSize=8.4, leading=10.6, textColor=INK),
    cellb=ParagraphStyle("cellb", fontName="SegB", fontSize=8.4, leading=10.6, textColor=INK),
    mk=ParagraphStyle("mk", fontName="SegB", fontSize=9, leading=12, textColor=ACC, alignment=2),
    bul=ParagraphStyle("bul", fontName="Seg", fontSize=9.3, leading=12.5, textColor=INK, leftIndent=13, bulletIndent=2, spaceAfter=1.5),
)
CODE = ParagraphStyle("code", fontName="Mono", fontSize=7.7, leading=9.4, textColor=INK)


def P(t, st="body"):
    return Paragraph(t, S[st] if isinstance(st, str) else st)


def bullets(items):
    return [Paragraph(t, S["bul"], bulletText="\u2022") for t in items]


def code(text, shade=SHADE):
    pre = Preformatted(text.strip("\n"), CODE)
    t = Table([[pre]], colWidths=[None])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), shade), ("BOX", (0, 0), (-1, -1), 0.5, RULE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def table(rows, widths, header=True, zebra=True, size=None):
    data = []
    for i, r in enumerate(rows):
        st = "cellb" if (header and i == 0) else "cell"
        data.append([c if not isinstance(c, str) else Paragraph(c, S[st]) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    sty = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
           ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    if header:
        sty.append(("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.89, 0.93, 0.98)))
    if zebra:
        for i in range(1 if header else 0, len(rows)):
            if i % 2 == 0:
                sty.append(("BACKGROUND", (0, i), (-1, i), SHADE))
    t.setStyle(TableStyle(sty))
    return t


def banner(text, color=ACC):
    t = Table([[Paragraph(text, S["sec"])]], colWidths=[None])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), color), ("LEFTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


def part(label, marks, flows, width):
    """one lettered question part: label + body on the left, [marks] on the right."""
    left = [Paragraph("<b>%s</b>&nbsp;" % label, S["body"])] if False else []
    body = flows if isinstance(flows, list) else [flows]
    first = body[0]
    if isinstance(first, Paragraph):
        first = Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (label, first.text), first.style)
        body = [first] + body[1:]
    else:
        body = [Paragraph("<b>%s</b>" % label, S["body"])] + body
    t = Table([[body, Paragraph("[%s]" % marks, S["mk"])]], colWidths=[width - 1.6 * cm, 1.6 * cm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 1),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    return t


def make_doc(path, title, footer, left_head):
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.9 * cm,
                          bottomMargin=1.7 * cm, title=title, author="CSE 213 TF prep")
    fw = A4[0] - 3.6 * cm
    frame = Frame(doc.leftMargin, doc.bottomMargin, fw, A4[1] - doc.topMargin - doc.bottomMargin, id="f",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    def deco(c, d):
        c.saveState()
        c.setFont("Seg", 7.8)
        c.setFillColor(GREY)
        c.drawString(doc.leftMargin, A4[1] - 1.2 * cm, left_head)
        c.drawRightString(A4[0] - doc.rightMargin, A4[1] - 1.2 * cm, footer)
        c.setStrokeColor(RULE)
        c.line(doc.leftMargin, A4[1] - 1.35 * cm, A4[0] - doc.rightMargin, A4[1] - 1.35 * cm)
        c.drawCentredString(A4[0] / 2, 0.9 * cm, "Page %d" % d.page)
        c.restoreState()
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=deco)])
    return doc, fw


__all__ = ["P", "bullets", "code", "table", "banner", "part", "make_doc", "S", "CODE", "KeepTogether", "Spacer", "cm",
           "ACC", "GREEN", "GREY", "AMBER", "SHADE", "RULE", "INK", "Table", "TableStyle", "colors", "Paragraph"]
