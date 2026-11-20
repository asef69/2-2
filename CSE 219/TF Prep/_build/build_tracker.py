"""Builds both CSE 219 TF Practice Trackers from questions.json + solved_*.json."""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c219 import PREP, REPO  # noqa
sys.path.insert(0, os.path.join(REPO, "_tfprep"))
from tracker_lib import build_tracker  # noqa

BUILD = os.path.dirname(os.path.abspath(__file__))
Q = [r for r in json.load(open(os.path.join(BUILD, "questions.json"), encoding="utf-8")) if int(r["year"][:4]) >= 2018]  # 2018-19 and newer only
SOLVED = {}
for f in glob.glob(os.path.join(BUILD, "solved_*.json")):
    SOLVED.update(json.load(open(f, encoding="utf-8")))

ANIK_LESSONS = {
 1: ("Energy and power — Lec 1, sl. 2–16", 1), 2: ("Shift, reversal, scaling x(αt+β) — Lec 1, sl. 17–39", 1),
 3: ("Even and odd parts — Lec 1, sl. 40–52", 1), 4: ("Step, impulse, ramp, jump signals — Lec 2, sl. 2–29", 1),
 5: ("Exponentials, sinusoids, periodicity — Lec 2, sl. 30–50", 1),
 6: ("Systems: linearity, time invariance — Lec 3, sl. 2–11", 2), 7: ("Discrete convolution as polynomial product — Lec 3, sl. 12–31", 2),
 8: ("Impulse response, y = x*h derivation — Lec 3, sl. 32–57", 2), 9: ("Convolution practice, interconnections — Lec 4, sl. 2–52", 2),
 10: ("Causality and stability — Lec 4, sl. 53–69", 2),
 11: ("Fourier series idea, orthogonality — Lec 5, sl. 2–23, 44–52", 3), 12: ("Computing FS coefficients — Lec 5, sl. 24–43", 3),
 13: ("FS properties and symmetry — Lec 6, sl. 2–35", 3), 14: ("FS differentiation, impulse trains — Lec 6, sl. 36–72", 3),
 15: ("FS multiplication, Parseval, LTI input — Lec 6, sl. 73–81", 3),
 16: ("From FS to FT — Lec 7, sl. 2–18", 4), 17: ("Rectangles, shifts, modulation — Lec 7, sl. 19–44", 4),
 18: ("FT pairs and properties — Lec 7 + textbook", 4), 19: ("LTI in frequency, filters, bandwidth — Lec 7, sl. 45–59 + textbook", 4)}
ASH_LESSONS = {
 1: ("From Fourier series to DFS/DFT — Lec 1, sl. 2–19", 1), 2: ("DTFT and DFT as samples — Lec 1, sl. 20–34", 1),
 3: ("DFT properties — Lec 2, sl. 2–12", 1), 4: ("Circular convolution, DFT filtering — Lec 2, sl. 13–23", 1),
 5: ("Radix-2 DIT FFT — Lec 3, sl. 4–15", 2), 6: ("Radix-2 DIF FFT — Lec 3, sl. 16–18", 2),
 7: ("Matrix (Cooley–Tukey/Bailey) FFT — Lec 4, sl. 5–14", 2), 8: ("Fast convolution, Bluestein — Lec 4, sl. 16–22", 2),
 9: ("Impulse-train sampling spectrum — Lec 5, sl. 4–17", 3), 10: ("Sampling theorem, aliasing — Lec 5, sl. 19–22", 3),
 11: ("Reconstruction: sinc, ZOH, linear — Lec 5, sl. 24–36", 3), 12: ("Practical issues, DFT link — Lec 5, sl. 38–47", 3),
 13: ("Laplace definition and ROC — Lec 6, sl. 4–25", 4), 14: ("Inverse Laplace — Lec 6, sl. 27–36", 4),
 15: ("Laplace properties — Lec 7, sl. 4–18", 4), 16: ("LTI systems, ODEs, circuits, feedback — Lec 7, sl. 20–28 + textbook", 4),
 17: ("z-transform definition and ROC — Lec 8, sl. 4–26", 5), 18: ("Inverse z-transform — Lec 8, sl. 28–32", 5),
 19: ("z properties and LTI systems — Lec 8, sl. 34–47", 5)}
A_TABS = [("1 Signals", "Lec 1–2 — Signals", "CSE219_Anik_Signals_Notes.docx"),
          ("2 LTI + Convolution", "Lec 3–4 — LTI Systems and Convolution", "CSE219_Anik_LTI_Convolution_Notes.docx"),
          ("3 Fourier Series", "Lec 5–6 — Fourier Series", "CSE219_Anik_Fourier_Series_Notes.docx"),
          ("4 Fourier Transform", "Lec 7 — Fourier Transform", "CSE219_Anik_Fourier_Transform_Notes.docx")]
B_TABS = [("1 DTFT + DFT", "Lec 0–2 — DTFT, DFT, circular convolution", "CSE219_Ashraf_DTFT_DFT_Notes.docx"),
          ("2 FFT", "Lec 3–4 — Fast Fourier Transform", "CSE219_Ashraf_FFT_Notes.docx"),
          ("3 Sampling", "Lec 5 — Sampling and reconstruction", "CSE219_Ashraf_Sampling_Notes.docx"),
          ("4 Laplace", "Lec 6–7 — Laplace transform", "CSE219_Ashraf_Laplace_Notes.docx"),
          ("5 z-Transform", "Lec 8 — z-transform", "CSE219_Ashraf_ZTransform_Notes.docx")]
AREA = {"state_space": "State-space models (not in slides)", "analogue": "Mechanical–electrical analogues / D'Alembert (not in slides)"}
TAG = {"CSE 219": "", "EEE 211": " (EEE)", "EEE 301": " (EEE)", "CSE 311": " (CSE 311)"}


def build(teacher, short, name, lessons, tabs, outside_ok):
    rows = [r for r in Q if r["teacher"] == teacher]
    groups = {}
    for r in rows:
        groups.setdefault(r["group"], []).append(r)
    tab_rows = {i: [] for i in range(1, len(tabs) + 1)}
    for r in rows:
        ln = int(r["lesson"][1:])
        title, tab = lessons[ln]
        key = f"{r['year']}|{r['course']}|{r['qno']}"
        same = "; ".join(f"{o['year']} {o['qno']}{TAG[o['course']]}" for o in groups[r["group"]] if o is not r)
        tab_rows[tab].append(dict(year=r["year"], course=r["course"], qno=r["qno"], question=r["question"], topic=title,
                                  lesson=r["lesson"], marks=r["marks"], page=r["page"], type=r["type"],
                                  in_notes=SOLVED.get(key) or r["in_notes"] or "◐ Method", same_type=same or "—"))
    outside = [dict(year=r["year"], course=r["course"], qno=r["qno"], question=r["question"], area=AREA[r["group"]],
                    marks=r["marks"], page=r["page"]) for r in Q if r["teacher"] == "OUT"] if outside_ok else None
    t = [dict(sheet=sh, title=ti, note_file=nf, rows=tab_rows[i + 1]) for i, (sh, ti, nf) in enumerate(tabs)]
    out = os.path.join(PREP, f"CSE219_{short}_TF_Practice_Tracker.xlsx")
    build_tracker(out, "CSE 219", f"{name} Sir", short, "CSE 219 All Merged Questions.pdf (22-batch and EEE pages as written in TF Page)",
                  t, outside=outside, high_from="2019-20",
                  old_codes="CSE 219 = current course; EEE 211 / EEE 301 = predecessor course (same content, TF Page = 'EEE p.N' in "
                            "EEE 211 - TF Questions 2023-24 to 2010-11.pdf); CSE 311 = Data Communication papers in the merged PDF "
                            "(only their signals/Fourier/sampling parts are listed).",
                  notes_extra=["2023-24 CSE 219 pages are in 'CSE 219 (22 batch).pdf' (TF Page '22 batch p.N').",
                               "Section split: Anik Sir = signals, LTI, Fourier series/transform; Ashraf Sir = DFT/FFT, sampling, Laplace, z."])
    return len(rows), sum(len(v) for v in tab_rows.values()), (len(outside) if outside else 0), out


for teacher, short, name, lessons, tabs, o in [("Anik", "Anik", "Anik", ANIK_LESSONS, A_TABS, False),
                                               ("Ashraf", "Ashraf", "Ashraf", ASH_LESSONS, B_TABS, True)]:
    print(teacher, build(teacher, short, name, lessons, tabs, o))
from collections import Counter
print("Per paper:")
for tch in ("Anik", "Ashraf", "OUT"):
    c = Counter((r["course"], r["year"]) for r in Q if r["teacher"] == tch)
    print(tch, dict(sorted(c.items())))
missing = [k for k in [f"{r['year']}|{r['course']}|{r['qno']}" for r in Q if r["teacher"] != "OUT"] if k not in SOLVED]
print("not marked (default from json/Method):", len(missing)); print(missing)
