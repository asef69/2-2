"""common.py — shared helpers for the CSE 213 note builders."""
import json
import os
import sys

ROOT = r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2"
sys.path.insert(0, os.path.join(ROOT, "_tfprep"))
from notes_lib import Notes  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES_DIR = os.path.join(ROOT, "CSE 213", "TF Prep", "notes")
AN = os.path.join(ROOT, "CSE 213", "Anindya Sir")
IJ = os.path.join(ROOT, "CSE 213", "IJ Mam")
SCR = os.path.join(HERE, "pptx_pdf")  # PDF copies of the pptx decks (made by PowerPoint)

with open(os.path.join(HERE, "questions.json"), encoding="utf-8") as fh:
    Q = json.load(fh)


def new(teacher, topic, fname):
    if teacher == "Anindya":
        lab, tag = "Anindya Sir's portion", "Anindya Sir part"
    else:
        lab, tag = "IJ Mam's portion", "IJ Mam part"
    return Notes(course="CSE 213", course_title="Software Engineering", topic=topic,
                 part_label=lab, part_tag=tag, out_path=os.path.join(NOTES_DIR, fname))


def rows(file_key):
    def yk(r):
        return -int(r["year"][:4])
    return sorted([r for r in Q if r["file"] == file_key], key=lambda r: (yk(r), r["qno"]))


def fmt_marks(m):
    if isinstance(m, float):
        whole = int(m)
        frac = m - whole
        return f"{whole}⅔" if abs(frac - 0.67) < 0.02 else f"{m:g}"
    return str(m)


def exam_map(n, file_key, focus, intro=None):
    n.h1("Exam Map — What the TF Papers Ask")
    if intro:
        n.p(intro)
    rs = rows(file_key)
    by = {}
    for r in rs:
        by.setdefault(r["year"], []).append(r)
    tab = []
    for y, lst in by.items():
        tab.append([f"{y} ({lst[0]['course']})",
                    " · ".join(f"Q{r['qno']} {r['question']} ({fmt_marks(r['marks'])}) [{r['lesson']}]" for r in lst)])
    n.table(["Session (paper)", "Questions in this note file"], tab, widths_cm=[3.2, 14.0], font_size=8.5)
    n.callout("focus", focus)


def src_note(extra=""):
    return ("Slide numbers refer to the PDF page numbers of the deck named under each lesson title. "
            "TF page numbers refer to 'CSE 213 All Past Papers.pdf' (70 pages); the newest paper "
            "(22 batch, labelled 2024-25 here) is a separate file, cited as '22 batch p.N'. "
            "Old course code: CSE 307. " + extra)


def java(n, bundle, fname, size=8.5):
    """Put a compiled Java file (java/<bundle>/<fname>) into a grey code box."""
    with open(os.path.join(HERE, "java", bundle, fname), encoding="utf-8") as fh:
        code(n, fh.read().rstrip("\n"), size=size)


def code(n, text, size=8.5, maxlines=48):
    """Code box split into page-sized chunks (a box row cannot break across pages)."""
    lines = text.split("\n") if isinstance(text, str) else list(text)
    while len(lines) > maxlines:
        cut = maxlines
        for k in range(maxlines, maxlines // 2, -1):  # prefer a blank line or a class start
            if not lines[k].strip() or lines[k].startswith(("class ", "interface ", "abstract ", "public class", "//")):
                cut = k
                break
        n.code(lines[:cut], size=size)
        lines = lines[cut:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    n.code(lines, size=size)
