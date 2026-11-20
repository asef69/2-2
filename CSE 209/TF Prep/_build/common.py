"""Shared paths and helpers for the ART note builders."""
import json
import os
import sys

REPO = r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2"
sys.path.insert(0, os.path.join(REPO, "_tfprep"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
from notes_lib import Notes  # noqa: E402

SLIDES = os.path.join(REPO, "CSE 209", "Tushar Sir")
CH1 = os.path.join(SLIDES, "Chapter_01.pdf")
ALU = os.path.join(SLIDES, "ALU Design.pdf")
CH2 = os.path.join(SLIDES, "Chapter_02.pdf")
CH3 = os.path.join(SLIDES, "Chapter_03_Arithmetic-shortslide.pdf")
TF = os.path.join(REPO, "CSE 209", "TF questions", "CSE209 ALL TF QUES (TF209).pdf")
OUT = os.path.join(REPO, "CSE 209", "TF Prep", "notes")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "questions.json"), encoding="utf-8") as f:
    QUESTIONS = json.load(f)


def new(topic, fname):
    return Notes(course="CSE 209", course_title="Computer Architecture", topic=topic,
                 part_label="Tushar Sir's portion", part_tag="Tushar Sir part",
                 out_path=os.path.join(OUT, fname))


def _yk(y):
    return int(y[:4])


def exam_map(n, file_no, extra_rows=()):
    """Table of every TF question mapped to this note file (newest first)."""
    rows = [q for q in QUESTIONS if q["file"] == file_no]
    rows.sort(key=lambda q: (-_yk(q["year"]), q["course"] != "CSE 209", q["qno"]))
    data = []
    for q in rows:
        paper = f"{q['year']} ({q['course']})"
        mk = "" if q["marks"] is None else (str(q["marks"]).rstrip("0").rstrip(".") if isinstance(q["marks"], float) else str(q["marks"]))
        star = " ★" if _yk(q["year"]) >= 2019 else ""
        data.append([paper + star, q["qno"], q["question"], mk, q["lesson"]])
    data += [list(r) for r in extra_rows]
    n.table(["Session (paper)", "Q", "What is asked", "Marks", "Lesson"], data,
            widths_cm=[3.5, 1.7, 8.7, 1.3, 1.7], font_size=8.5)
    return rows


def marks_since(file_no, y0=2019):
    return sum(q["marks"] or 0 for q in QUESTIONS if q["file"] == file_no and _yk(q["year"]) >= y0)
