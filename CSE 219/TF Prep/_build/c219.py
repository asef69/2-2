"""Shared helpers for the CSE 219 note builders (paths, Notes factory, matplotlib sketches)."""
import json
import os
import sys

REPO = r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2"
sys.path.insert(0, os.path.join(REPO, "_tfprep"))
from notes_lib import Notes  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

BUILD = os.path.dirname(os.path.abspath(__file__))
PREP = os.path.dirname(BUILD)
NOTES = os.path.join(PREP, "notes")
FIG = os.path.join(BUILD, "fig")
os.makedirs(FIG, exist_ok=True)
COURSE = os.path.join(REPO, "CSE 219")
ANIK = os.path.join(COURSE, "Anik Sir")
ASHRAF = os.path.join(COURSE, "Ashraf Sir")
A = {1: os.path.join(ANIK, "Lecture-1-A-Little-Introduction-to-Signals.pdf"),
     2: os.path.join(ANIK, "Lecture-2-Some-Useful-Signals.pdf"),
     3: os.path.join(ANIK, "Lecture-3-Linear-Time-Invariant-Systems-and-Convolution.pdf"),
     4: os.path.join(ANIK, "Lecture-4-Convolution-Causality-and-Stability.pdf"),
     5: os.path.join(ANIK, "Lecture-5-Fourier-Series-Let's-Look-Inside.pdf"),
     6: os.path.join(ANIK, "Lecture-6-Properties-of-Fourier-Series.pdf"),
     7: os.path.join(ANIK, "Lecture-7-Fourier-Transform.pdf")}
B = {0: os.path.join(ASHRAF, "Lecture 0 - Overview of the Transforms.pdf"),
     1: os.path.join(ASHRAF, "Lecture 1 - DTFT and DFT.pdf"),
     2: os.path.join(ASHRAF, "Lecture 2 - DFT Properties and Applications.pdf"),
     3: os.path.join(ASHRAF, "Lecture 3 - Fast Fourier Transform.pdf"),
     4: os.path.join(ASHRAF, "Lecture 4 - Advanced FFT.pdf"),
     5: os.path.join(ASHRAF, "Lecture 5 - Sampling.pdf"),
     6: os.path.join(ASHRAF, "6 - Laplace.pdf"),
     7: os.path.join(ASHRAF, "7 - More Laplace.pdf"),
     8: os.path.join(ASHRAF, "8 - Z-Transform.pdf")}

TITLE = "Signals and Linear Systems"


def anik(topic, fname):
    return Notes(course="CSE 219", course_title=TITLE, topic=topic,
                 part_label="Anik Sir's portion", part_tag="Anik Sir part",
                 out_path=os.path.join(NOTES, fname))


def ashraf(topic, fname):
    return Notes(course="CSE 219", course_title=TITLE, topic=topic,
                 part_label="Ashraf Sir's portion", part_tag="Ashraf Sir part",
                 out_path=os.path.join(NOTES, fname))


def questions(teacher=None):
    with open(os.path.join(BUILD, "questions.json"), encoding="utf-8") as f:
        q = json.load(f)
    return [r for r in q if teacher is None or r["teacher"] == teacher]


def page_ref(r):
    p = str(r["page"])
    if p.startswith("EEE") or p.startswith("22 batch"):
        return p
    return "TF p." + p


# ------------------------------------------------------------------ sketches
def _style(ax, xlabel="t", ylabel=None):
    ax.axhline(0, color="black", lw=0.8)
    ax.axvline(0, color="black", lw=0.8)
    ax.grid(True, ls=":", lw=0.5, color="#BBBBBB")
    ax.set_xlabel(xlabel, fontsize=9)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=9)
    ax.tick_params(labelsize=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def sketch(name, panels, ncols=None, size=(3.2, 2.2), xlabel="t"):
    """panels: list of dict(title, curves=[(t, y, label)], impulses=[(t0, area)], xlim, ylim, xticks, yticks,
    stems=[(n, x)], xlabel). Saves FIG/name.png and returns its path."""
    n = len(panels)
    ncols = ncols or min(n, 3)
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(size[0] * ncols, size[1] * nrows), squeeze=False)
    colors = ["#1F4E79", "#C55A11", "#2E7D32", "#7030A0"]
    for k, p in enumerate(panels):
        ax = axes[k // ncols][k % ncols]
        _style(ax, p.get("xlabel", xlabel))
        for i, c in enumerate(p.get("curves", [])):
            t, y = c[0], c[1]
            lab = c[2] if len(c) > 2 else None
            ax.plot(t, y, color=colors[i % 4], lw=1.8, label=lab)
        for t0, a in p.get("impulses", []):
            ax.annotate("", xy=(t0, a), xytext=(t0, 0),
                        arrowprops=dict(arrowstyle="-|>", color="#C00000", lw=1.6))
            ax.text(t0, a + (0.08 if a >= 0 else -0.25) * max(1, abs(a)), f"({a:g})", ha="center",
                    fontsize=7.5, color="#C00000")
        for i, st in enumerate(p.get("stems", [])):
            nn, xx = st[0], st[1]
            ml, sl, bl = ax.stem(nn, xx, basefmt=" ")
            plt.setp(ml, color=colors[i % 4], markersize=4)
            plt.setp(sl, color=colors[i % 4], lw=1.2)
            if p.get("label_stems"):
                for a, b in zip(nn, xx):
                    if b != 0:
                        ax.text(a, b + 0.06 * max(abs(np.asarray(xx))), f"{b:g}", ha="center", fontsize=7)
        if p.get("xlim"):
            ax.set_xlim(*p["xlim"])
        if p.get("ylim"):
            ax.set_ylim(*p["ylim"])
        if p.get("xticks") is not None:
            ax.set_xticks(p["xticks"])
        if p.get("yticks") is not None:
            ax.set_yticks(p["yticks"])
        if p.get("legend"):
            ax.legend(fontsize=7, loc=p.get("legend_loc", "best"))
        ax.set_title(p.get("title", ""), fontsize=9.5)
    for k in range(n, nrows * ncols):
        axes[k // ncols][k % ncols].axis("off")
    fig.tight_layout()
    path = os.path.join(FIG, name + ".png")
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


def pw(t, pieces):
    """Piecewise function: pieces = [(a, b, f)] with f callable on numpy arrays; 0 elsewhere."""
    t = np.asarray(t, dtype=float)
    y = np.zeros_like(t)
    for a, b, f in pieces:
        m = (t >= a) & (t < b)
        y[m] = f(t[m])
    return y


# ------------------------------------------------------------------ exam map + solved registry
def _yk(y):
    return int(str(y)[:4])


def exam_map(n, teacher, lessons, extra_rows=None, width=(3.2, 14.0)):
    """Table of every TF question of `teacher` whose lesson is in `lessons` (ints), newest first."""
    rows = [r for r in questions(teacher) if r["lesson"] and int(r["lesson"][1:]) in lessons]
    groups = {}
    for r in rows:
        groups.setdefault((r["year"], r["course"]), []).append(r)
    order = sorted(groups, key=lambda k: (-_yk(k[0]), {"CSE 219": 0, "EEE 211": 1, "EEE 301": 1, "CSE 311": 2}[k[1]]))
    table = []
    for key in order:
        items = " · ".join(f"Q{r['qno']} {r['question']} ({r['marks']})" for r in groups[key])
        table.append([f"{key[0]} ({key[1]})", items])
    table += extra_rows or []
    n.table(["Session (paper)", "Questions answered by this note"], table, widths_cm=list(width), font_size=8.5)
    return rows


SOLVED = {}


def mark(year, course, qno, status="✔ Solved"):
    SOLVED[f"{year}|{course}|{qno}"] = status


def save_solved(fname):
    with open(os.path.join(BUILD, f"solved_{fname}.json"), "w", encoding="utf-8") as f:
        json.dump(SOLVED, f, ensure_ascii=False, indent=1)
