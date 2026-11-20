"""Common pieces for the MATH 243 note build scripts."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2\_tfprep")
sys.path.insert(0, HERE)

from notes_lib import Notes  # noqa: E402

from m243 import NOTES_DIR  # noqa: E402

PARTS = {
    "KKS": dict(part_label="KKS Sir's portion — Probability & ANOVA", part_tag="KKS Sir part"),
    "Stat": dict(part_label="Statistics portion", part_tag="Statistics part"),
}


def new(part, topic, fname):
    return Notes(course="MATH 243", course_title="Probability and Statistics", topic=topic,
                 out_path=os.path.join(NOTES_DIR, fname), **PARTS[part])


def questions(note=None, part=None):
    with open(os.path.join(HERE, "questions.json"), encoding="utf-8") as f:
        qs = json.load(f)
    if note:
        qs = [q for q in qs if q["note"] == note]
    if part:
        qs = [q for q in qs if q["part"] == part]
    return qs


def yk(y):
    return int(y[:4])


def exam_map(n, note, intro=None):
    """Exam Map table: one row per paper with that note's questions, newest first."""
    qs = questions(note)
    by = {}
    for q in qs:
        by.setdefault((q["year"], q["course"]), []).append(q)
    rows = []
    for (y, c), lst in sorted(by.items(), key=lambda kv: -yk(kv[0][0])):
        lst.sort(key=lambda q: q["qno"])
        cell = " · ".join(f"Q{q['qno']} {q['question']} ({q['marks']}) [{q['lesson']}]" for q in lst)
        page = sorted({str(q["page"]) for q in lst})
        rows.append([f"{y} ({c})\nTF p. {', '.join(page)}", cell])
    if intro:
        n.p(intro)
    n.table(["Session (paper)", "Questions answered by this note  [lesson]"], rows, widths_cm=[3.4, 13.8],
            font_size=9)
    tot = sum(q["marks"] for q in qs)
    hi = [q for q in qs if yk(q["year"]) >= 2019]
    return dict(n=len(qs), marks=tot, n_hi=len(hi), marks_hi=sum(q["marks"] for q in hi),
                years=sorted({q["year"] for q in qs}, key=yk))


def ans_table(n, headers, rows, widths=None, fs=9):
    n.table(headers, rows, widths_cm=widths, font_size=fs)
