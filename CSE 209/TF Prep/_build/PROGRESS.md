# CSE 209 — ART (Tushar Sir) TF kit — progress

## Done
- Read FORMAT_SPEC, notes_lib, tracker_lib, tools; dumped RS Control Unit + Single-Cycle notes and RS tracker.
- Read all 4 decks (text + rendered every slide). Reading log: `reading_log.md`.
- Read every TF209 page (rendered scans). Findings:
  - `CSE 209 (22 batch).pdf` (7 p) == TF209 pp. 1–7 (2023-24 CSE 209) — identical images. No "22 batch p.N" rows needed.
  - `CSE 209 All Merged Questions.pdf` (80 p) == TF209 pp. 8–87. Nothing new.
  - ART part = every question not in the RS tracker + RS-outside rows tagged "ISA (ART part)" (CISC vs RISC).
- Question master list: `questions_data.py` → `questions.json`.

## Plan (lessons numbered L1–L23 across files)
1. `CSE209_ART_Ch1_Performance_Notes.docx` — L1–L4
2. `CSE209_ART_ALU_Design_Notes.docx` — L5–L9
3. `CSE209_ART_Ch2_MIPS_ISA_Notes.docx` — L10–L18
4. `CSE209_ART_Ch3_Arithmetic_Notes.docx` — L19–L23 (L23 = textbook insurance: division, signed mult, FP instructions, guard/round/sticky)
Tracker: `CSE209_ART_TF_Practice_Tracker.xlsx` via `build_tracker.py`.

## Next
- verify.py (numerics + mini MIPS interpreter to test assembly answers)
- build_notes_ch1.py → ALU → ch2 → ch3 (save each when done)
- build_tracker.py, Word→PDF visual check, final report

## Status per file
- [x] verify.py (ALL PASS — output in verify_out.txt; MIPS answers in answers_asm.py, traces in traces.py)
- [x] Ch1 notes built (L1–L4), checked in Word PDF (19 p), crops fixed
- [x] ALU notes built (L5–L9), checked in Word PDF (21 p)
- [x] Ch2 notes built (L10–L18), checked in Word PDF (35 p), crops fixed
- [x] Ch3 notes built (L19–L23)
- [x] tracker built
- [x] visual check (all four PDFs viewed; crops fixed). DONE.
- 2016-17 6(a), 2014-15 6(a)/(c) tables zoomed
