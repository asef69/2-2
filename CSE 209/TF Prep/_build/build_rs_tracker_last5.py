"""Rebuild the RS tracker keeping only 2019-20 … 2023-24 (read from the existing file; backup kept outside the repo)."""
import os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl
from common import REPO
from tracker_lib import build_tracker
P = os.path.join(REPO, "CSE 209", "TF Prep", "CSE209_RS_TF_Practice_Tracker.xlsx")
SRC = sys.argv[1] if len(sys.argv) > 1 else P
ok = lambda y: int(str(y)[:4]) >= 2019
wb = openpyxl.load_workbook(SRC)
tabs, outside = [], []
for ws in wb.worksheets[2:]:
    if ws.title == "Outside Notes":
        for r in ws.iter_rows(min_row=4, values_only=True):
            if r[0] is not None and ok(r[1]):
                outside.append(dict(year=r[1], course=r[2], qno=r[3], question=r[4], area=r[5], marks=r[6], page=r[7]))
        continue
    note = ws["A2"].value.split("Note file:")[1].split("·")[0].strip()
    rows = []
    for r in ws.iter_rows(min_row=4, values_only=True):
        if r[0] is not None and ok(r[1]):
            rows.append(dict(year=r[1], course=r[2], qno=r[3], question=r[4], topic=r[5], lesson=r[6], marks=r[7], page=r[8],
                             type=r[10], in_notes=r[11], same_type=r[12]))
    print(ws.title, len(rows))
    if rows:
        tabs.append(dict(sheet=ws.title, title=ws["A1"].value, note_file=note.replace(".docx", ".pdf"), rows=rows))
print("outside", len(outside))
build_tracker(out_path=P, course="CSE 209", part_name="Rifat Sir", part_short="RS", qpdf="TF209.pdf", tabs=tabs, outside=outside,
              high_from="2019-20", old_codes="CSE 209 = current course code; CSE 305 = old code for the same Rifat Sir content.",
              notes_extra=["Tracker lists the last five papers (2019-20 to 2023-24) only; older papers are covered in the notes and the topic-wise solutions book.",
                           "Control Unit has no question in these papers (insurance topic), so it has no tab."])
