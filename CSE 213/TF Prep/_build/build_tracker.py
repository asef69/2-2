"""Builds both CSE 213 TF Practice Trackers from questions.json."""
import json
import os
import sys
from collections import Counter

ROOT = r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2"
sys.path.insert(0, os.path.join(ROOT, "_tfprep"))
from tracker_lib import build_tracker  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "CSE 213", "TF Prep")
Q = [r for r in json.load(open(os.path.join(HERE, "questions.json"), encoding="utf-8")) if 2018 <= int(r["year"][:4]) <= 2024]

TOPIC = {
    "L1": "Encapsulation, interfaces, cohesion/coupling — Lec 1, sl. 2–9",
    "L2": "SRP, OCP — Lec 1, sl. 10–17",
    "L3": "LSP, ISP, DIP — Lec 1, sl. 18–31",
    "L4": "Pattern basics, GoF catalogue — Lec 2, sl. 1–10",
    "L5": "UML recap, Factory Method — Lec 3, sl. 2–16",
    "L6": "Abstract Factory — Lec 3, sl. 17–35",
    "L7": "Singleton — Lec 3, sl. 36–42",
    "L8": "Builder, choosing a creational pattern — Lec 3, sl. 43–53",
    "L9": "Class notation, kinds of classes — Lec 5, sl. 1–5",
    "L10": "Relationships, aggregation vs composition — Lec 5, sl. 6–14",
    "L11": "Scenario class diagrams — Lec 5, sl. 15–24",
    "L12": "ERD to class, CRC — Lec 6, sl. 1–10",
    "L13": "States, events, transitions — Lec 7, sl. 1–11",
    "L14": "Nested & concurrent states — Lec 7, sl. 12–24",
    "L15": "Worked statecharts — Lec 7, sl. 25–29",
    "L16": "Sequence diagram notation — Lec 8, sl. 1–10",
    "L17": "Use case → sequence diagram — Lec 9, sl. 1–5",
    "L18": "Collaboration diagrams — Lec 9 sl. 6–8, Lec 10",
    "L19": "UML overview, use case relationships — Use case.pptx, sl. 1–16",
    "L20": "Use case diagrams & narratives — Use case.pptx (TF scenarios)",
    "L21": "BPMN core — 3-BPMN.pptx, sl. 1–20",
    "L22": "BPMN pools, lanes — 3-BPMN.pptx, sl. 21–34",
    "L23": "Testing basics, black/white box — Lec 11, sl. 1–13",
    "L24": "Testing types, integration, performance — Lec 11, sl. 14–22",
    "L25": "Code coverage — 1-Coverage.pptx, sl. 1–8",
    "L26": "Basis paths, loop testing — textbook",
    "L27": "EP, BVA, positive/negative — 2-Equivalence partitioning.pptx",
}
TOPIC_IJ = {
    "L1": "Decorator — Structural pp. 1–50",
    "L2": "Composite — Structural pp. 51–60",
    "L3": "Adapter — Structural pp. 61–95",
    "L4": "Bridge — Structural pp. 96–111",
    "L5": "Strategy — Behavioral pp. 4–48",
    "L6": "Template Method — Behavioral pp. 49–81",
    "L7": "Observer — Behavioral pp. 82–128",
    "L8": "Mediator — Behavioral pp. 129–167",
    "L9": "State — Behavioral pp. 203–260",
    "L10": "Identifying the pattern — mixed",
    "L11": "Generic process model — Process pp. 2–16",
    "L12": "Prescriptive models — Process pp. 15–42",
    "L13": "Agile principles, XP — Process pp. 43–63",
    "L14": "Scrum, Kanban — Process pp. 64–84",
    "L15": "Unit testing, JUnit, TDD — Unit Testing pp. 1–24",
    "L16": "Code reviews — CodeReviews pp. 1–21",
    "L17": "Refactoring basics — Refactoring pp. 1–14",
    "L18": "Code smells — Refactoring pp. 15–29",
    "L19": "Refactoring catalogue, worked code — Refactoring pp. 30–47",
    "L20": "Software ethics — Ethics pp. 1–12",
    "L21": "Requirement analysis — Requirements pp. 1–12",
}
A_TABS = [
    ("A1", "1 Design Principles", "Lec 1–2 — Design Principles & Pattern Basics", "CSE213_Anindya_Design_Principles_Notes.docx"),
    ("A2", "2 Creational Patterns", "Lec 3 — Creational Design Patterns", "CSE213_Anindya_Creational_Patterns_Notes.docx"),
    ("A3", "3 Class Diagrams", "Lec 4–6 — Class Diagrams & ERD to Class", "CSE213_Anindya_Class_Diagrams_Notes.docx"),
    ("A4", "4 State Diagrams", "Lec 7 — State Diagrams", "CSE213_Anindya_State_Diagrams_Notes.docx"),
    ("A5", "5 Interaction Diagrams", "Lec 8–10 — Sequence & Collaboration", "CSE213_Anindya_Interaction_Diagrams_Notes.docx"),
    ("A6", "6 Use Case + BPMN", "Use case.pptx + BPMN.pptx", "CSE213_Anindya_UseCase_BPMN_Notes.docx"),
    ("A7", "7 Software Testing", "Lec 11 + Coverage + Equivalence Partitioning", "CSE213_Anindya_Software_Testing_Notes.docx"),
]
I_TABS = [
    ("I1", "1 Structural Patterns", "Structural Design Patterns", "CSE213_IJ_Structural_Patterns_Notes.docx"),
    ("I2", "2 Behavioral Patterns", "Behavioral Design Patterns (+ Misc)", "CSE213_IJ_Behavioral_Patterns_Notes.docx"),
    ("I3", "3 Process + Agile", "Process Models and Agile Development", "CSE213_IJ_Process_Agile_Notes.docx"),
    ("I4", "4 Unit Testing + Review", "Unit Testing and Code Reviews", "CSE213_IJ_UnitTesting_CodeReview_Notes.docx"),
    ("I5", "5 Refactoring", "Refactoring and Code Smells", "CSE213_IJ_Refactoring_Notes.docx"),
    ("I6", "6 Ethics + Requirements", "Software Ethics and Requirement Analysis", "CSE213_IJ_Ethics_Requirements_Notes.docx"),
]


def page(p):
    return p if isinstance(p, str) else int(p)


def tabs(spec, topics):
    out = []
    for key, sheet, title, nf in spec:
        rows = []
        for r in Q:
            if r["file"] != key:
                continue
            rows.append(dict(year=r["year"], course=r["course"], qno=r["qno"], question=r["question"],
                             topic=topics[r["lesson"]], lesson=r["lesson"], marks=r["marks"], page=page(r["page"]),
                             type=r["type"], in_notes=r["in_notes"], same_type=r["same_type"]))
        out.append(dict(sheet=sheet, title=title, note_file=nf, rows=rows))
    return out


def outside(key):
    return [dict(year=r["year"], course=r["course"], qno=r["qno"], question=r["question"], area=r["key"],
                 marks=r["marks"], page=page(r["page"])) for r in Q if r["file"] == key]


COMMON = dict(course="CSE 213", qpdf="CSE 213 All Past Papers.pdf", high_from="2019-20",
              old_codes="CSE 213 = current code (2023-24 onward); CSE 307 = old L-3/T-1 code for the same course. "
                        "'2024-25' = the 22-batch paper (exam 10/05/2026, header says 2023-2024), separate file "
                        "'CSE 213 (22 batch).pdf' → TF Page '22 batch p.N'.")
NOTE = ["Facade, Command, Chain of Responsibility and Interpreter are not in this term's syllabus; their questions are in Outside Notes.", "Rows with Course = CSE 325 are diagram questions from AI Sir's senior course (folder 'AI Sir Diagram question from seniors'); TF Page = 'AI Sir <session> p.N'. Their solutions are in the 'Senior Diagram Practice' section of note files 3–6.", "Only papers from 2018-19 to 2024-25 are listed (others left out on request).", "TF Page = page in 'CSE 213 All Past Papers.pdf' (70 p.). It contains everything in 'CSE 213 Question.pdf' "
        "(63 p.) plus the 2023-24 CSE 213 paper (21 batch) as pages 1–7, so Question.pdf page = All Past Papers page − 7.",
        "Papers do not split by teacher section; every question is assigned by topic. Topics in neither teacher's slides "
        "(EVM, CPM/PERT, COCOMO/FP, risk, security, architecture, DevOps, IS design) are in 'Outside Notes'."]

a = build_tracker(out_path=os.path.join(OUT, "CSE213_Anindya_TF_Practice_Tracker.xlsx"), part_name="Anindya Sir",
                  part_short="Anindya", tabs=tabs(A_TABS, TOPIC), outside=outside("OA"), notes_extra=NOTE, **COMMON)
i = build_tracker(out_path=os.path.join(OUT, "CSE213_IJ_TF_Practice_Tracker.xlsx"), part_name="IJ Mam",
                  part_short="IJ", tabs=tabs(I_TABS, TOPIC_IJ), outside=outside("OI"), notes_extra=NOTE, **COMMON)
print(a, i, sep="\n")

# ---- verification: every question exactly once, per paper and per teacher
from openpyxl import load_workbook  # noqa: E402
seen = Counter()
for path in (a, i):
    wb = load_workbook(path)
    for ws in wb.worksheets[2:]:
        for row in ws.iter_rows(min_row=4, values_only=True):
            if row[1]:
                seen[(row[1], row[2], row[3])] += 1
dups = [k for k, v in seen.items() if v > 1]
exp = Counter((r["year"], r["course"], r["qno"]) for r in Q)
print("rows in trackers:", sum(seen.values()), "questions:", len(Q), "duplicates:", dups,
      "missing:", [k for k in exp if k not in seen])
by = Counter()
for r in Q:
    by[(r["year"], r["teacher"], "outside" if r["file"] in ("OA", "OI") else "topic")] += 1
for y in sorted({r["year"] for r in Q}, reverse=True):
    print(y, {k[1] + "/" + k[2]: v for k, v in by.items() if k[0] == y})
