"""make_site.py step 1 — runs the 13 build_notes_*.py scripts with the HTML Notes twin; writes site/data/notes.json + site/img/*.webp"""
import glob
import json
import os
import runpy
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, BUILD)
import html_notes  # noqa: E402

html_notes.OUT = HERE
os.makedirs(os.path.join(HERE, "img"), exist_ok=True)
os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
shim = types.ModuleType("notes_lib")
shim.Notes = html_notes.Notes
sys.modules["notes_lib"] = shim

for f in sorted(glob.glob(os.path.join(BUILD, "build_notes_*.py"))):
    print("running", os.path.basename(f))
    runpy.run_path(f, run_name="__main__")

json.dump({"notes": html_notes.RESULT, "practice": html_notes.PRACTICE},
          open(os.path.join(HERE, "data", "notes.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("files:", len(html_notes.RESULT), "practice blocks:", len(html_notes.PRACTICE))
for k, v in html_notes.RESULT.items():
    print(k, [(s["kind"], s["title"][:40], len(s["html"])) for s in v["sections"]])
