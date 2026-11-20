"""build_site.py step 3 — joins notes.json + groups.json + questions.json into data.json and writes index.html (from shell.html)."""
import collections
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)
N = json.load(open(os.path.join(HERE, "data", "notes.json"), encoding="utf-8"))
G = json.load(open(os.path.join(HERE, "data", "groups.json"), encoding="utf-8"))
Q = json.load(open(os.path.join(BUILD, "questions.json"), encoding="utf-8"))
SHEET = open(os.path.join(HERE, "sheet.html"), encoding="utf-8").read()

UNITS = [  # (file key, unit id, short name, part)
    ("CSE213_Anindya_Design_Principles_Notes", "A1", "Design principles", "A"),
    ("CSE213_Anindya_Creational_Patterns_Notes", "A2", "Creational patterns", "A"),
    ("CSE213_Anindya_Class_Diagrams_Notes", "A3", "Class diagrams", "A"),
    ("CSE213_Anindya_State_Diagrams_Notes", "A4", "State diagrams", "A"),
    ("CSE213_Anindya_Interaction_Diagrams_Notes", "A5", "Sequence & collaboration", "A"),
    ("CSE213_Anindya_UseCase_BPMN_Notes", "A6", "Use case & BPMN", "A"),
    ("CSE213_Anindya_Software_Testing_Notes", "A7", "Software testing", "A"),
    ("CSE213_IJ_Structural_Patterns_Notes", "I1", "Structural patterns", "B"),
    ("CSE213_IJ_Behavioral_Patterns_Notes", "I2", "Behavioral patterns", "B"),
    ("CSE213_IJ_Process_Agile_Notes", "I3", "Process models & agile", "B"),
    ("CSE213_IJ_UnitTesting_CodeReview_Notes", "I4", "Unit testing & code review", "B"),
    ("CSE213_IJ_Refactoring_Notes", "I5", "Refactoring", "B"),
    ("CSE213_IJ_Ethics_Requirements_Notes", "I6", "Ethics & requirements", "B"),
]
CHAPTER_UNITS = {   # chapter title of the solution book -> unit ids searched for a topic
    "Design Principles & Basics of Design Pattern": ["A1"], "Creational Design Patterns": ["A2"],
    "Structural Design Patterns": ["I1"], "Behavioural Design Patterns": ["I2"],
    "Class Diagram & State Diagram": ["A3", "A4"], "Sequence & Collaboration Diagrams": ["A5"],
    "Process Models & Agile Development": ["I3"], "Software Testing": ["A7"],
    "Unit Testing & Code Review": ["I4"], "Code Refactoring": ["I5"],
    "Software Ethics & Requirement Analysis": ["I6"], "Equivalence Partitioning & Coverage": ["A7"],
    "Use Case Diagram": ["A6"], "BPMN Diagram": ["A6"],
}

units, topics = [], {}
for key, uid, short, part in UNITS:
    f = N["notes"][key]
    u = dict(id=uid, part=part, title=short, topic=f["topic"], lessons=[], map="", quick="", senior="", note=f["source_note"] or "")
    for s in f["sections"]:
        m = re.match(r"Lesson (\d+) — (.*)", s["title"])
        if m:
            tid = ("a" if part == "A" else "i") + m.group(1)
            topics[tid] = dict(id=tid, num=int(m.group(1)), unit=uid, part=part, title=m.group(2), source=s["source"], html=s["html"], q=[])
            u["lessons"].append(tid)
        elif s["kind"] == "map":
            u["map"] = s["html"]
        elif s["kind"] == "quick":
            u["quick"] = s["html"]
        elif s["kind"] == "senior":
            u["senior"] = s["html"]
    units.append(u)
unit_of = {u["id"]: u for u in units}

# ---- practice
prac = []
for p in N["practice"]:
    uid = next(x[1] for x in UNITS if x[0] == p["file"])
    m = re.search(r"Lesson (\d+)", p["label"])
    tid = (("a" if unit_of[uid]["part"] == "A" else "i") + m.group(1)) if m else None
    prac.append(dict(unit=uid, topic=tid, label=p["label"], prov=p["prov"], html=p["html"], section=p["section"]))

# ---- questions (join groups to questions.json)
idx = collections.defaultdict(list)
for r in Q:
    idx[(r["year"], r["course"], r["qno"])].append(r)
groups, papers = {}, collections.OrderedDict()
bpmn_practice = []
for g in G:
    gid = g["gid"]
    ch = g["chapter"]
    tops = set()
    ents = []
    for e in g["entries"]:
        if e["kind"] == "practice":
            bpmn_practice.append(dict(gid=gid, n=e["n"], title=e["title"], marks=e["marks"]))
            ents.append(dict(kind="practice", n=e["n"], title=e["title"], marks=e["marks"]))
            continue
        r = idx.get((e["year"], e["course"], e["qno"]))
        r = r[0] if r else None
        t = None
        if r and r["file"][0] in "AI" and len(r["file"]) == 2:
            t = ("a" if r["file"][0] == "A" else "i") + r["lesson"][1:]
            if t in topics:
                tops.add(t)
            else:
                t = None
        ents.append(dict(kind="paper", year=e["year"], course=e["course"], qno=e["qno"], marks=e["marks"], date=e["date"],
                         ident=e["ident"], topic=t, text=(r["question"] if r else ""), qtype=(r.get("type", "") if r else ""),
                         same=(r.get("same_type", "") if r else "")))
    if not tops:
        for uid in CHAPTER_UNITS.get(ch, []):
            tops.update(unit_of[uid]["lessons"])
        gtopics = sorted(tops)
        exact = False
    else:
        gtopics = sorted(tops)
        exact = True
    groups[gid] = dict(id=gid, img=g["img"], w=g["w"], h=g["h"], chapter=ch, entries=ents, topics=gtopics, exact=exact)
    for e in ents:
        if e["kind"] != "paper":
            continue
        e["gid"] = gid
        papers.setdefault(e["year"], []).append(e)
    for t in gtopics:
        topics[t]["q"].append(gid)

# ---- exam map: actual term-final questions of the last seven papers
YEARS = ["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
cnt = collections.defaultdict(lambda: collections.Counter())
marks = collections.Counter()
for r in Q:
    if r["year"] in YEARS and r["course"] in ("CSE 307", "CSE 213") and r["file"][0] in "AI" and len(r["file"]) == 2:
        t = ("a" if r["file"][0] == "A" else "i") + r["lesson"][1:]
        cnt[t][r["year"]] += 1
        marks[t] += float(r["marks"])
emap = []
for t in topics.values():
    c = cnt[t["id"]]
    emap.append(dict(id=t["id"], title=t["title"], unit=t["unit"], counts=[c[y] for y in YEARS], marks=round(marks[t["id"]], 1),
                     years=sum(1 for y in YEARS if c[y])))

for t in topics.values():           # reduce question lists to unique, ordered gids
    t["q"] = sorted(set(t["q"]))

def msum(m):
    return sum(float(x) for x in re.findall(r"\d+(?:\.\d+)?", str(m or "")))


# papers meta
pm = []
for y in sorted(papers, reverse=True):
    es = papers[y]
    courses = sorted({e["course"] for e in es})
    pm.append(dict(id=y, courses=courses, n=len(es), marks=sum(msum(e["marks"]) for e in es),
                   entries=sorted(es, key=lambda e: (e["course"], [int(x) if x.isdigit() else 0 for x in re.findall(r"\d+", e["qno"])]))))

PLAN = [
    dict(day=1, title="Principles and creational patterns", note="Learn the principles first, they are the reasons behind every pattern.",
         items=["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8"]),
    dict(day=2, title="Structural and behavioral patterns", note="Draw each pattern's class diagram from memory, then write the Java skeleton.",
         items=["i1", "i2", "i3", "i4", "i5", "i6", "i7", "i8", "i9", "i10"]),
    dict(day=3, title="UML: class, state, sequence, collaboration", note="Every paper has at least one diagram question. Practise drawing, not reading.",
         items=["a9", "a10", "a11", "a12", "a13", "a14", "a15", "a16", "a17", "a18"]),
    dict(day=4, title="Use case, BPMN and testing", note="Numbers questions (coverage, basis paths, BVA) are quick marks once you know the method.",
         items=["a19", "a20", "a21", "a22", "a23", "a24", "a25", "a26", "a27"]),
    dict(day=5, title="Process, unit testing, refactoring, ethics, then a mock paper", note="Light reading topics. Finish by solving one full past paper against the clock.",
         items=["i11", "i12", "i13", "i14", "i15", "i16", "i17", "i18", "i19", "i20", "i21"]),
]
DATA = dict(units=units, topics=list(topics.values()), papers=pm, groups=groups, practice=prac, bpmn=bpmn_practice,
            emap=dict(years=YEARS, rows=emap), plan=PLAN, sheet=SHEET)
js = json.dumps(DATA, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
shell = open(os.path.join(HERE, "shell.html"), encoding="utf-8").read()
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(shell.replace("/*DATA*/", js))
print("topics", len(topics), "papers", len(pm), "entries", sum(p["n"] for p in pm), "groups", len(groups), "practice", len(prac),
      "bytes", len(js))
print("topics without questions:", [t["id"] for t in topics.values() if not t["q"]])
print("exact-join groups:", sum(1 for g in groups.values() if g["exact"]), "of", len(groups))
