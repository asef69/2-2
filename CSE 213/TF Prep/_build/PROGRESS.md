# CSE 213 TF kit — PROGRESS
See HANDOVER.md for findings. Logs: questions_log.md (papers), anindya_decknotes.md, ij_decknotes.md, raw_text/ (all deck + paper text).
## Done
- All question papers read; 2017-18 onward logged with marks in questions_log.md.
- Anindya Sir decks read + logged. IJ Mam decks read + logged (all 9).
## Plan (note files)
Anindya: 1 Design_Principles (Lec1-2) · 2 Creational_Patterns (Lec3) · 3 Class_Diagram (Lec4-6 + class diagram.pptx) · 4 State_Diagram (Lec7) · 5 Interaction_Diagrams (Lec8-10) · 6 UseCase_BPMN (Use case.pptx + 3-BPMN.pptx) · 7 Software_Testing (Lec11 + Coverage + EP pptx)
IJ: 1 Structural_Patterns · 2 Behavioral_Patterns (+Misc) · 3 Process_Agile · 4 UnitTesting_CodeReview · 5 Refactoring · 6 Ethics_Requirements
Outside topics (EVM, CPM/PERT, COCOMO/FP, risk, security, architecture, DevOps, IS-design/DFD/cost-benefit) -> Outside Notes tabs.
## Done since
- questions.json written (questions_data.py).
- notes A1 Design_Principles, A2 Creational_Patterns built + PDF-checked (java/A2 compiled).
- A3 Class_Diagrams, A4 State_Diagrams, A5 Interaction, A6 UseCase_BPMN, A7 Software_Testing built + checked. ALL ANINDYA NOTES DONE.
- Next: IJ notes I1..I6 (java bundles I1.txt, I2.txt ...)
## Next
- Log 2016-17..2010-11 papers (render to read marks) -> questions.json
- Build notes one file at a time (build_notes_<name>.py), then trackers, javac, PDF check, report.
- I1 Structural built + checked (java/I1).
- I2 Behavioral built + checked (java/I2).
- I3 Process_Agile, I4 UnitTesting_CodeReview built (java/I4 tests pass).
- I5 Refactoring built (java/I5).
- I6 Ethics_Requirements built. ALL NOTES DONE. Next: trackers.
- Trackers built (build_tracker.py): 349 questions, each exactly once; outside topics in Outside Notes tabs.
## STATUS: COMPLETE (notes A1–A7, I1–I6; two trackers). Remaining nice-to-have: more slide figures in I2 note.
## 2026-11-15 syllabus change
- Facade, Command, Chain of Responsibility, Interpreter removed from the syllabus.
- I1: Facade section/question removed; I2: Command lesson removed, CoR/Interpreter removed; IJ lessons renumbered
  (State L9, Identify L10, process L11–14, unit test/review L15–16, refactoring L17–19, ethics/req L20–21).
- Facade/CoR/Interpreter questions -> OI (Outside Notes); Smart Home 2024-25 Q5(b) kept under Mediator (part (i) only, ○ Partly).
- Solution book: rebuild_book.py moved the Smart Home group to chapter X1 (out of syllabus); original in _build/backup/.
- Questions PDF regenerated (make_question_pdf.py): 259 in-syllabus questions.
## 2026-11-15 slide PDF ('TF Prep.pdf', 852 pages from Downloads)
- clean_slides.py -> CSE 213/TF Prep/TF Prep.pdf (841 pages): deleted Behavioral slides 168-178 (Command intro; 179-202 were already absent),
  removed Facade / Interpreter / Chain of Responsibility / Command from the Lec 2 pattern lists (counts 7->6, 11->8) and covered the
  Facade sentence on Structural slide 82. Original untouched.
- run_check2.py <pdf>: every slide of every deck in CSE 213/Anindya Sir and IJ Mam is present, in order, 0 mismatches.
