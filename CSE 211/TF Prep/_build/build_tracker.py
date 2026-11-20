"""Builds CSE211_Hakim_TF_Practice_Tracker.xlsx and CSE211_Atif_TF_Practice_Tracker.xlsx from questions.json."""
import os, sys, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPO, PREP, load, _ykey  # noqa
from tracker_lib import build_tracker  # noqa

D = load()
Q = [q for q in D["questions"] if _ykey(q["year"]) >= 2017]  # only papers 2017-18 … 2023-24

LESSON_TITLE = {
    "H": {1: ("Why Theory of Computation?", "Lec01 Introduction, sl. 2–53"), 2: ("Alphabets, strings, languages, problems", "Lec02 Languages, sl. 2–52"),
          3: ("The DFA as a mathematical object", "Lec03 DFA, sl. 2–20"), 4: ("Designing DFAs", "Lec03 DFA, sl. 21–29"),
          5: ("Advanced DFAs and reading DFAs", "Lec03 DFA, sl. 30–42"), 6: ("Nondeterminism and the NFA", "Lec04 NFA, sl. 2–49"),
          7: ("Designing NFAs", "Lec04 NFA, sl. 50–70"), 8: ("ε-transitions and removing them", "Lec04 NFA, sl. 71–90"),
          9: ("NFA → DFA: subset construction", "Lec04 NFA, sl. 91–109"), 10: ("Regular operations, closure under ∪ ∘ ∗", "Lec05 Regulars, sl. 1–37"),
          11: ("Complement, intersection, difference, reverse", "Lec05 Regulars, sl. 38–60"), 12: ("Regular expressions", "Lec05 Regulars, sl. 61–84"),
          13: ("RE → NFA (Thompson)", "Lec05 Regulars, sl. 85–93"), 14: ("DFA → RE (GNFA), Kleene", "Lec05 Regulars, sl. 94–111"),
          15: ("Pumping lemma: statement, proof, logic", "Lec06 Non Regulars, sl. 1–11"), 16: ("Pumping-lemma proofs", "Lec06 Non Regulars, sl. 12–28"),
          17: ("Closure arguments, faulty proofs, pumping lengths", "Lec06 Non Regulars, sl. 24–50"),
          18: ("Grammars, derivations, parse trees", "Lec07 CFG, sl. 1–29"), 19: ("Designing CFGs", "Lec07 CFG, sl. 30–52"),
          20: ("Ambiguity, inherent ambiguity", "Lec07 CFG, sl. 53–63"), 21: ("Pumping lemma for CFLs", "Lec07 CFG, sl. 64–97")},
    "A": {1: ("The three areas", "Lecture 1, sl. 2–14"), 2: ("Simplifying grammars", "Lecture 2 CNF, sl. 19–30"),
          3: ("Converting to CNF", "Lecture 2 CNF, sl. 2–3, 19–35"), 4: ("CYK algorithm", "Lecture 2 CNF, sl. 4–18"),
          5: ("PDA: definition and idea", "Lecture 3 PDA, sl. 2–55"), 6: ("IDs and traces", "Lecture 3 PDA, sl. 56–86"),
          7: ("Designing PDAs", "Lecture 3 PDA, sl. 20–55, 87–101"), 8: ("Final state vs empty stack", "Lecture 3 PDA, sl. 102–109"),
          9: ("CFG ↔ PDA", "Lecture 3 PDA, sl. 104, 110–122"), 10: ("CFL pumping lemma, DPDA, hierarchy", "Lecture 3 PDA, sl. 123–136"),
          11: ("TM definition, IDs, language", "Lecture 4 TM1, sl. 1–41, 116–123"), 12: ("Designing language-deciding TMs", "Lecture 4 TM1, sl. 42–70"),
          13: ("TMs computing functions", "Lecture 4 TM1, sl. 71–115"), 14: ("Storage in the state, tracks, subroutines", "Lecture 5 TM2, sl. 1–83, 132–133"),
          15: ("Bit-manipulation TMs", "Lecture 5 TM2, sl. 84–131"), 16: ("Multitape TMs and simulation", "Lecture 6 TM3, sl. 1–22"),
          17: ("NTMs and restricted TMs", "Lecture 6 TM3, sl. 23–39"), 18: ("TMs and computers", "Lecture 6 TM3, sl. 40–68"),
          19: ("Recursive, RE, decidable languages", "Lecture 7 Undecidability, sl. 2–13"), 20: ("Counting, TM codes, L_d", "Lecture 7 Undecidability, sl. 14–51"),
          21: ("Complements, L_u, halting, A_TM", "Lecture 7 Undecidability, sl. 52–70"), 22: ("Reductions, Rice, PCP", "Lecture 7 Undecidability, sl. 71–77"),
          23: ("P, NP, certificates", "Lecture 8 Complexity, sl. 2–8"), 24: ("NP-completeness, SAT, Cook", "Lecture 8 Complexity, sl. 9–28"),
          25: ("NP-completeness proofs", "Lecture 8 Complexity, sl. 29–51 + textbook"), 26: ("PSPACE, Savitch, class relationships", "Lecture 9 Space complexity, sl. 2–20")}}

TABS = {
    "H": [("1 Intro + Languages", "Lec01–02 — Introduction & Languages", "CSE211_Hakim_Intro_Languages_Notes.docx", (1, 2)),
          ("2 DFA", "Lec03 — Deterministic Finite Automata", "CSE211_Hakim_DFA_Notes.docx", (3, 4, 5)),
          ("3 NFA", "Lec04 — Nondeterminism and NFAs", "CSE211_Hakim_NFA_Notes.docx", (6, 7, 8, 9)),
          ("4 Regular Languages", "Lec05 — Closure Properties and Regular Expressions", "CSE211_Hakim_Regular_Languages_Notes.docx", (10, 11, 12, 13, 14)),
          ("5 Pumping Lemma", "Lec06 — Non-Regular Languages", "CSE211_Hakim_NonRegular_Notes.docx", (15, 16, 17)),
          ("6 CFG", "Lec07 — Context-Free Grammars", "CSE211_Hakim_CFG_Notes.docx", (18, 19, 20, 21)),
          ("7 PDA (see Atif tracker)", "lec_08 — Pushdown Automata (design workshop; all PDA questions are tracked in the Atif tracker)", "CSE211_Hakim_PDA_Notes.docx", (22, 23, 24))],
    "A": [("1 Intro + CNF", "Lectures 1–2 — Introduction, CFG simplification, CNF, CYK", "CSE211_Atif_Intro_CNF_Notes.docx", (1, 2, 3, 4)),
          ("2 PDA", "Lecture 3 — Pushdown Automata, CFG–PDA equivalence, CFL pumping lemma", "CSE211_Atif_PDA_Notes.docx", (5, 6, 7, 8, 9, 10)),
          ("3 TM Basics", "Lecture 4 — Turing Machines: definition and design", "CSE211_Atif_TM_Basics_Notes.docx", (11, 12, 13)),
          ("4 TM Techniques", "Lecture 5 — Programming techniques and bit-manipulation TMs", "CSE211_Atif_TM_Techniques_Notes.docx", (14, 15)),
          ("5 TM Variants", "Lecture 6 — Variants of Turing machines, TMs vs computers", "CSE211_Atif_TM_Variants_Notes.docx", (16, 17, 18)),
          ("6 Undecidability", "Lecture 7 — Decidability and undecidability", "CSE211_Atif_Undecidability_Notes.docx", (19, 20, 21, 22)),
          ("7 Complexity", "Lectures 8–9 — P, NP, NP-completeness, PSPACE", "CSE211_Atif_Complexity_Notes.docx", (23, 24, 25, 26))]}

METHOD_KEYS = {"toc_theory", "dfa_re_pairs", "tm_multitape", "utm", "rice", "cfg_pda_equiv", "tm_computer", "tm_variants", "recinf",
               "parse_tree", "tracks_vs_tapes", "pda_given_x", "tm_describe_x"}
PARTLY = {("2009-10", "12(c)")}


def in_notes(q):
    if (q["year"], q["qno"]) in PARTLY:
        return "○ Partly"
    if q["key"] == "inherent_amb" and _ykey(q["year"]) < 2019:
        return "◐ Method"
    if q["key"] in METHOD_KEYS:
        return "◐ Method"
    return "✔ Solved"


def same_type(q, pool):
    others = [o for o in pool if o["key"] == q["key"] and not (o["year"] == q["year"] and o["qno"] == q["qno"])]
    others.sort(key=lambda o: -_ykey(o["year"]))
    return "; ".join(f"{o['year']} {o['qno']}" for o in others[:6])


out = os.path.join(PREP)
for t, (name, short) in (("H", ("Hakim Sir", "Hakim")), ("A", ("Atif Sir", "Atif"))):
    pool = [q for q in Q if q["teacher"] == t]
    tabs = []
    for sheet, title, nf, lessons in TABS[t]:
        rows = []
        for q in pool:
            if q["lesson"] in lessons:
                lt, deck = LESSON_TITLE[t][q["lesson"]]
                rows.append(dict(year=q["year"], course="CSE 211", qno=q["qno"], question=q["question"],
                                 topic=f"{lt} — {deck}", lesson=f"L{q['lesson']}", marks=q["marks"], page=q["page"],
                                 type=q["type"], in_notes=in_notes(q), same_type=same_type(q, pool)))
        tabs.append(dict(sheet=sheet, title=title, note_file=nf, rows=rows))
    outside = []
    if t == "A":
        outside = [dict(year=o["year"], course=o["course"], qno=o["qno"], question=o["question"], area=o["area"], marks=o["marks"], page=o["page"])
                   for o in D["outside"]]
    extra = ["Papers 2017-18 … 2023-24 only (7 papers), as requested; older papers (2006-07 … 2016-17) are not listed. The 2023-24 paper is "
             "not inside the merged PDF; its rows say '22 batch p.N' (CSE 211 (22 batch).pdf).",
             "The paper printed 'January 2020 Term' (held 16/01/2021) is listed as '2020 (Jan term)'. 2017-18 is ★★ Medium / ★ Low; "
             "2019-20 onward are ★★★ High.",
             "Questions were assigned to a teacher by topic, not by section letter."]
    if t == "H":
        extra.append("PDA questions are taught by both teachers; every PDA question sat in the Turing-machine section of its paper, so "
                     "they are tracked in the Atif tracker (tab 2). Tab 7 of this workbook is intentionally empty — its note is the PDA "
                     "design workshop. CFL pumping-lemma questions follow the same rule (2013-14 Q7(c) is here; later ones are Atif's).")
        extra.append("2013-14 Q5(b): the mark is not printed on the paper (5 by the section total) — left blank.")
    else:
        extra.append("The Outside Notes tab holds 2010-11 Q12(b) (machine-schema notation of Lewis–Papadimitriou, not in the slides).")
    path = os.path.join(out, f"CSE211_{short}_TF_Practice_Tracker.xlsx")
    build_tracker(out_path=path, course="CSE 211", part_name=name, part_short=short,
                  qpdf="CSE 211 All Merged Questions.pdf (2023-24 rows: CSE 211 (22 batch).pdf)", tabs=tabs, outside=outside,
                  high_from="2019-20", old_codes="Every paper in the collection carries the code CSE 211.", notes_extra=extra)
    print(path, {tb["sheet"]: len(tb["rows"]) for tb in tabs}, "outside", len(outside))
