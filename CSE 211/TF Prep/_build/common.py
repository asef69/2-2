"""Shared helpers for the CSE 211 TF-prep build scripts."""
import json
import os
import re
import sys

REPO = r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2"
sys.path.insert(0, os.path.join(REPO, "_tfprep"))
import notes_lib  # noqa: E402
from notes_lib import Notes  # noqa: E402

# Kleene stars (a*b, (ab)*, Σ*) must not open italics: an italic *…* must start after whitespace/punctuation
# and end before a non-word character. Patched here, in this course's build only (shared lib untouched).
notes_lib._TOKEN = re.compile(
    r"(\*\*.+?\*\*"
    r"|(?<![^\s(\[\"'—–:;,/])\*[^*\s](?:[^*]*?[^*\s])?\*(?![\w(\[{])"
    r"|`[^`]+`|\^\{[^}]*\}|_\{[^}]*\})")

COURSE_DIR = os.path.join(REPO, "CSE 211")
PREP = os.path.join(COURSE_DIR, "TF Prep")
NOTES_DIR = os.path.join(PREP, "notes")
BUILD = os.path.join(PREP, "_build")
H = os.path.join(COURSE_DIR, "Hakim Sir")
A = os.path.join(COURSE_DIR, "Atif Sir")
QPDF = os.path.join(COURSE_DIR, "TF questions", "CSE 211 All Merged Questions.pdf")

PDF = {
    "H1": os.path.join(H, "Lec01 - Introduction.pdf"),
    "H2": os.path.join(H, "Lec02 - Languages.pdf"),
    "H3": os.path.join(H, "Lec03 - DFA.pdf"),
    "H4": os.path.join(H, "Lec04 - NFA.pdf"),
    "H5": os.path.join(H, "Lec05 - The Regulars.pdf"),
    "H6": os.path.join(H, "Lec06 - Non Regulars.pdf"),
    "H7": os.path.join(H, "Lec07 - CFG.pdf"),
    "H8": os.path.join(H, "lec_08_pda.pdf"),
    "A1": os.path.join(A, "Lecture - 1 (intro_2).pdf"),
    "A2": os.path.join(A, "Lecture - 2 (cnf).pdf"),
    "A3": os.path.join(A, "Lecture - 3 (pda).pdf"),
    "A4": os.path.join(A, "Lecture - 4 (Turing Machine 1).pdf"),
    "A5": os.path.join(A, "Lecture - 5 (Turing Machine 2).pdf"),
    "A6": os.path.join(A, "Lecture - 6 (Turing Machine 3).pdf"),
    "A7": os.path.join(A, "Lecture - 7 (Undecidability).pdf"),
    "A8": os.path.join(A, "Lecture - 8 (complexity).pdf"),
    "A9": os.path.join(A, "Lecture - 9 (space_complexity).pdf"),
}

PRACT_NOTE = ("Practice provenance: Actual = taken from a TF paper; Adapted = TF question with changed "
              "details; Constructed = new question in TF style.")


def load():
    with open(os.path.join(BUILD, "questions.json"), encoding="utf-8") as f:
        return json.load(f)


def _ykey(y):
    m = re.match(r"(\d{4})", y)
    return int(m.group(1)) if m else 0


def fmt_marks(m):
    if m is None:
        return "–"
    if abs(m - round(m)) < 1e-9:
        return str(int(round(m)))
    if abs((m - int(m)) - 1 / 3) < 0.01:
        return f"{int(m)}⅓"
    return f"{m:g}"


def exam_map_rows(teacher, lessons):
    """Rows [session, 'Q.. text (marks) · ...'] newest first, for questions whose lesson is in `lessons`."""
    qs = [q for q in load()["questions"] if q["teacher"] == teacher and q["lesson"] in lessons]
    by = {}
    for q in qs:
        by.setdefault(q["year"], []).append(q)
    rows = []
    for y in sorted(by, key=_ykey, reverse=True):
        parts = [f"Q{q['qno']} {q['question']} ({fmt_marks(q['marks'])})" for q in by[y]]
        rows.append([y, " · ".join(parts)])
    return rows, len(qs)


def new_notes(teacher, topic, fname):
    if teacher == "H":
        part_label, part_tag = "Hakim Sir's portion", "Hakim Sir part"
    else:
        part_label, part_tag = "Atif Sir's portion", "Atif Sir part"
    return Notes(course="CSE 211", course_title="Theory of Computation", topic=topic,
                 part_label=part_label, part_tag=part_tag, out_path=os.path.join(NOTES_DIR, fname))


def fig(n, deck, page, caption, clip=None, width_cm=12.0):
    n.figure_from_pdf(PDF[deck], page, caption, clip=clip, width_cm=width_cm)
