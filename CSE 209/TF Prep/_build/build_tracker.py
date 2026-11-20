"""Build CSE209_ART_TF_Practice_Tracker.xlsx from questions.json.   python -P build_tracker.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collections import Counter
from common import QUESTIONS as _ALL, REPO
QUESTIONS = [q for q in _ALL if int(q["year"][:4]) >= 2019]   # tracker keeps the last 5 papers: 2023-24 back to 2019-20
from tracker_lib import build_tracker

TOPIC = {
    "L1": "Abstraction, components, great ideas — Ch1, sl. 1–13", "L2": "Response time, throughput, CPU time — Ch1, sl. 14–20",
    "L3": "CPI, instruction mix, performance equation — Ch1, sl. 21–25", "L4": "Amdahl's law, MIPS/FLOPS pitfall — Ch1, sl. 26–28",
    "L6": "Arithmetic circuit, output carry — ALU, sl. 6–11", "L7": "X/Y/Z arithmetic-unit design — ALU, sl. 12–14",
    "L8": "Logic circuit, complete ALU — ALU, sl. 15–20", "L9": "Status register, overflow, comparators — ALU, sl. 21–22",
    "L10": "Operands, design principles — Ch2, sl. 2–13", "L11": "Signed numbers, encoding — Ch2, sl. 14–23",
    "L12": "Logical ops, decisions, loops — Ch2, sl. 24–35", "L13": "Procedures, stack, recursion — Ch2, sl. 36–45",
    "L14": "Bytes, strings, 32-bit constants — Ch2, sl. 46–50", "L15": "Branch/jump addressing, far branches — Ch2, sl. 51–54",
    "L16": "Addressing modes — Ch2, sl. 55", "L17": "Synchronization, pseudoinstructions — Ch2, sl. 56–59",
    "L18": "Linking, loading, JIT, RISC vs CISC — Ch2, sl. 58–69", "L19": "Integer add/sub overflow — Ch3, sl. 2–4",
    "L20": "Multiplication hardware — Ch3, sl. 5–8", "L21": "IEEE 754 representation — Ch3, sl. 9–16",
    "L22": "FP addition, FP adder — Ch3, sl. 17–20",
}
FILES = {1: ("1 Ch1 Performance", "Chapter 1 — Abstractions, Technology & Performance", "CSE209_ART_Ch1_Performance_Notes.docx"),
         2: ("2 ALU Design", "ALU Design (Mano ch. 9)", "CSE209_ART_ALU_Design_Notes.docx"),
         3: ("3 Ch2 MIPS ISA", "Chapter 2 — Instructions: Language of the Computer", "CSE209_ART_Ch2_MIPS_ISA_Notes.docx"),
         4: ("4 Ch3 Arithmetic", "Chapter 3 — Arithmetic for Computers", "CSE209_ART_Ch3_Arithmetic_Notes.docx")}


def row(q):
    return dict(year=q["year"], course=q["course"], qno=q["qno"], question=q["question"], topic=TOPIC[q["lesson"]],
                lesson=q["lesson"], marks=q["marks"], page=q["page"], type=q["type"], in_notes=q["in_notes"], same_type=q["same_type"])


tabs = [dict(sheet=s, title=t, note_file=f, rows=[row(q) for q in QUESTIONS if q["file"] == k]) for k, (s, t, f) in FILES.items()]
outside = [dict(year=q["year"], course=q["course"], qno=q["qno"], question=q["question"], area=q["area"], marks=q["marks"], page=q["page"])
           for q in QUESTIONS if q["file"] == "OUT"]
out = build_tracker(
    out_path=os.path.join(REPO, "CSE 209", "TF Prep", "CSE209_ART_TF_Practice_Tracker.xlsx"),
    course="CSE 209", part_name="Tushar Sir", part_short="ART", qpdf="TF209.pdf (CSE209 ALL TF QUES)",
    high_from="2019-20", tabs=tabs, outside=outside,
    old_codes="CSE 209 = current course code; CSE 305 = old code for the same content.",
    notes_extra=["'CSE 209 (22 batch).pdf' is identical to TF209 pp. 1–7 (2023-24); 'All Merged Questions.pdf' = TF209 pp. 8–87.",
                 "Outside Notes rows marked 'solved in Ch3 notes L23' / 'Ch1 notes L4' have full textbook solutions in the notes.",
                 "Tracker lists the last 5 papers (2019-20 to 2023-24) only; older papers are covered in the notes.",
                 "2022-23 11(b) and 12(c) are shared with the RS tracker (jal and j-reach parts are there)."])
print(out)
print({t["sheet"]: len(t["rows"]) for t in tabs}, "outside", len(outside))
print(sorted(Counter(q["year"] for q in QUESTIONS).items()))
