"""Question-only PDFs (no solutions) for each teacher, read from the practice trackers."""
import os, re, sys
import openpyxl
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, KeepTogether, PageBreak, Table, TableStyle

F = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Seg", F + r"\segoeui.ttf"))
pdfmetrics.registerFont(TTFont("SegB", F + r"\segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("SegI", F + r"\segoeuii.ttf"))
pdfmetrics.registerFont(TTFont("Sym", F + r"\seguisym.ttf"))
pdfmetrics.registerFontFamily("Seg", normal="Seg", bold="SegB", italic="SegI", boldItalic="SegB")

PREP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACC = colors.HexColor("#1F3864")
st = lambda n, **k: ParagraphStyle(n, **{"fontName": "Seg", **k})
S_T = st("t", fontSize=22, leading=27, textColor=ACC, fontName="SegB", spaceAfter=4)
S_ST = st("st", fontSize=11, leading=15, textColor=colors.HexColor("#444444"), spaceAfter=10)
S_H1 = st("h1", fontSize=15, leading=19, textColor=colors.white, fontName="SegB")
S_H2 = st("h2", fontSize=11.5, leading=15, textColor=ACC, fontName="SegB", spaceBefore=8, spaceAfter=3)
S_Q = st("q", fontSize=10.5, leading=14.5)
S_M = st("m", fontSize=8.5, leading=11, textColor=colors.HexColor("#555555"))
S_N = st("n", fontSize=9.5, leading=13)


def fx(s):
    s = escape(str(s))
    return s.replace("★", '<font name="Sym">★</font>')


def load(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    tabs = []
    for name in wb.sheetnames:
        if name in ("How to Use", "Dashboard"):
            continue
        ws = wb[name]
        title = ws.cell(1, 1).value
        hdr = [c.value for c in ws[3]]
        rows = [dict(zip(hdr, r)) for r in ws.iter_rows(min_row=4, values_only=True) if r[0] is not None]
        tabs.append((name, title, rows))
    return tabs


def build(short, teacher, xlsx, out):
    tabs = load(os.path.join(PREP, xlsx))
    total = sum(len(r) for _, _, r in tabs)
    story = []

    def footer(c, d):
        c.saveState(); c.setFont("Seg", 8); c.setFillColor(colors.HexColor("#777777"))
        c.drawString(18 * mm, 10 * mm, f"CSE 211 · {teacher} · TF question bank (2017-18 to 2023-24)")
        c.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {d.page}")
        c.restoreState()
    doc = BaseDocTemplate(out, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm,
                          title=f"CSE 211 {teacher} TF Question Bank", author="")
    doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")], onPage=footer)])

    story += [Paragraph(f"CSE 211 — {teacher}", S_T),
              Paragraph(f"Term-Final question bank · {total} questions (papers 2017-18, 2019-20, Jan-2020, 2021-22, 2022-23, 2023-24{"; plus one older out-of-syllabus question" if short=="Atif" else ""})", S_ST),
              Paragraph("Questions only (no solutions), taken from the practice tracker and grouped by tab and lesson, in the tracker’s order. "
                        "<font name='Sym'>★★★</font> High = 2019-20 onward; <font name='Sym'>★★</font> Medium = the question type repeats in another paper; "
                        "<font name='Sym'>★</font> Low = appears once. Each entry shows the exam year, the question number as printed on the paper, and the marks. "
                        "Solve after reading the matching note, then tick the box.", S_N), Spacer(1, 6)]
    summary = [["Tab", "Questions"]] + [[n, str(len(r))] for n, _, r in tabs if r]
    t = Table(summary, colWidths=[110 * mm, 30 * mm])
    t.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "Seg"), ("FONTNAME", (0, 0), (-1, 0), "SegB"), ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F5")), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B0B8C8")),
                           ("ALIGN", (1, 0), (1, -1), "RIGHT")]))
    story += [t]
    n = 0
    for name, title, rows in tabs:
        if not rows:
            continue
        story.append(PageBreak())
        h = Table([[Paragraph(fx(f"{name} — {title}"), S_H1)]], colWidths=[doc.width])
        h.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ACC), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
        story += [h]
        if "Lesson" not in rows[0]:
            story.append(Paragraph("Not covered by the current slides — check with the teacher whether these are in this term’s syllabus.", S_H2))
            for r in rows:
                n += 1
                meta = f"{r['Year']} · Q{r['Ques No.']} · {r['Marks']} marks · {r['Topic Area']}"
                story.append(KeepTogether([Paragraph(f"<b>{n}.</b> " + fx(r["Short Question"]), S_Q), Paragraph(fx(meta), S_M), Spacer(1, 6)]))
            continue
        lessons = {}
        for r in rows:
            lessons.setdefault((r["Lesson"], r["Topic (slide PDF · slides)"].split(" — ")[0]), []).append(r)
        for (les, lt), rs in sorted(lessons.items(), key=lambda kv: int(re.sub(r"\D", "", kv[0][0]))):
            story.append(Paragraph(fx(f"{les} · {lt}"), S_H2))
            for r in rs:
                n += 1
                marks = f"{r['Marks']} marks" if r["Marks"] is not None else "marks not printed"
                meta = f"{r['Year']} · Q{r['Ques No.']} · {marks} · {r['Priority']} · {r['Type']}"
                box = Paragraph("☐", ParagraphStyle("b", fontName="Sym", fontSize=12, leading=14))
                body = [Paragraph(f"<b>{n}.</b> " + fx(r["Short Question"]), S_Q), Paragraph(fx(meta), S_M)]
                row = Table([[box, body]], colWidths=[8 * mm, doc.width - 8 * mm])
                row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#DDDDDD"))]))
                story.append(KeepTogether([row]))
    doc.build(story)
    print(out, total, "questions,", os.path.getsize(out) // 1024, "KB")


build("Hakim", "Hakim Sir", "CSE211_Hakim_TF_Practice_Tracker.xlsx", os.path.join(PREP, "CSE211_Hakim_TF_Questions.pdf"))
build("Atif", "Atif Sir", "CSE211_Atif_TF_Practice_Tracker.xlsx", os.path.join(PREP, "CSE211_Atif_TF_Questions.pdf"))
