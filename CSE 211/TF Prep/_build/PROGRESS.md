# CSE 211 TF kit — hand-over (session stopped at usage limit)

Status: reading phase done; NOTHING written to `CSE 211/TF Prep/` yet.

## Done
- Read FORMAT_SPEC, notes_lib, tracker_lib, tools, gold RS notes (Control Unit, Memory Hierarchy) and gold tracker.
- Read all 17 papers visually/text: merged PDF pp.1-52 + `CSE 211 (22 batch).pdf` (= 2023-24, NOT in merged PDF → page "22 batch p.N").
- Read all text of all 17 decks (deduped overlay builds). Contact sheets of diagram slides built in the scratchpad but NOT yet viewed.

## Paper → merged-PDF pages
2006-07 p1-3 · 2007-08 p4-5 · 2008-09 p6-7 · 2009-10 p8-10 · 2010-11 p11-13 · 2011-12 p14-16 · 2012-13 p17-18 ·
2013-14 p19-21 · 2014-15 p22-23 · 2015-16 p24-27 · 2016-17 p28-31 · 2017-18 p32-35 · "January 2020 Term" p36-39 ·
2019-20 p40-43 · 2021-22 p44-48 · 2022-23 p49-52 · 2023-24 = 22 batch p1-4.

## Decisions taken
- "January 2020 Term" (held 16/01/2021): label year "2020 (Jan term)" so tracker _year_key=2020 → ★★★; explain in notes_extra.
- Section sides swap in old papers (2011-12, 2012-13, 2013-14: Sec A = PDA/TM side). Assign by topic:
  Hakim = intro/3 areas of ToC, languages, DFA, NFA, closure/regex, pumping (regular), CFG design/derivation/parse
  tree/ambiguity/"why context-free". Atif = CNF/CYK/simplification, PDA formal + FS↔ES + CFG↔PDA + DPDA, TM, variants,
  decidability/RE/Ld/Lu/halting/Rice, P/NP/NPC reductions/Cook, PSPACE/Savitch.
- Topics in BOTH decks → by side of origin: PDA (all PDA questions sat in the TM-side section → Atif tracker; Hakim's
  PDA note gets 0 rows, says so, solves design examples + cross-refs); CFL pumping lemma (Hakim Lec07 sl.64-97 and
  Atif Lec3 sl.123-129) → by side (e.g. 2013-14 Q7(c) → Hakim; 2023-24 Q7, 2022-23 Q9, 2021-22 Q8 → Atif).
- Complexity in Sec A (2017-18 Q1 3-colorability, Jan-2020 Q1(a) dominating set) → Atif.
- 2013-14 Q5(b): mark not printed (5 by section total) → marks None, report it.
- Slide numbers = PDF page numbers (Hakim decks are beamer overlays).

## Planned note files
Hakim (L numbered continuously): Intro+Languages (Lec01+02 merged), DFA, NFA, Regulars (closure, regex, GNFA), NonRegulars, CFG, PDA.
Atif: Intro+CNF (Lec1+2), PDA, TM1, TM2 (programming techniques; bitwise-op TMs: OR/XOR/AND/NOT/compare/2's complement
use the w1cw2c add-TM template sl.84-131), TM3 (variants), Undecidability, Complexity (+Space, or separate).

## Remaining
questions.json, build scripts, all notes, both trackers, Python simulation of DFA/NFA/PDA/TM answers, Word→PDF visual check, final report.

## Session 2 log
- [x] READING_LOG.md written (all 17 decks).
- [x] questions.py → questions.json: 371 rows (H/A per paper) + 1 outside (2010-11 12(b)).
- Lesson plan — Hakim: Intro_Languages L1–2 · DFA L3–5 · NFA L6–9 · Regulars L10–14 · NonRegulars L15–17 · CFG L18–21 · PDA L22–24.
  Atif: Intro_CNF L1–4 · PDA L5–10 · TM_Basics L11–13 · TM_Techniques L14–15 · TM_Variants L16–18 · Undecidability L19–22 · Complexity (Lec 8+9) L23–26.
- Next: notes one file at a time (build_notes_<x>.py + verify_<x>.py), then trackers.
- [x] Note 1 Hakim Intro_Languages (L1–2) built + checked (10 pp).
- [x] Note 2 Hakim DFA (L3–5) built + checked; designs verified in dfa_designs.py (32 DFAs).
- [x] Note 3 Hakim NFA (L6–9) built + checked; nfa_designs.py verifies 20 NFAs + 11 subset constructions.
- [ ] NEXT: Note 4 Hakim Regulars (L10–14). Figures read: 2011-12 7(c) states 1(start,acc)-a,b->2, 2 loop a, 2-b->3, 3-a->1, 3-b->2, all three accepting; 2012-13 7(b) 1 start, 1-a->2, 2-a->1, 2 loop b, 1-b->3, 3-b->1, 3-a->2, accept 2,3; 2013-14 6(c) q0 start/acc, q0-a->q1, q1-b->q0, q1-a->q2, q2 loop a, q2-b->q0; 2022-23 4(c) q0 loop0, q0-1->q1 (acc) loop1, q1-0->q0.
- Then: Hakim NonRegulars, CFG, PDA; all 7 Atif notes; trackers (build_tracker.py from questions.json); final PDF check + report.
- [x] Note 4 Hakim Regular_Languages (L10–14) built + checked (19 pp); re_designs.py verifies 26 REs, 3 option Qs, GNFA, Thompson.
- [x] Note 5 Hakim NonRegular (L15–17) built + checked; pl_checks.py (min pumping length 12).
- [x] Note 6 Hakim CFG (L18–21) + Note 7 Hakim PDA (L22–24) built + checked; cfg_designs.py (28 grammars), pda_designs.py (16 PDAs). HAKIM DONE.
- [x] Note 8 Atif Intro_CNF (L1–4) built + checked (cnf_cyk.py). NEXT: Atif PDA (L5–10), TM_Basics L11–13, TM_Techniques L14–15, TM_Variants L16–18, Undecidability L19–22, Complexity L23–26; then trackers + report.
- [x] Note 9 Atif PDA (L5–10) built + checked (pda_conv.py). NEXT: TM notes (A4 L11–13 basics, A5 L14–15 techniques, A6 L16–18 variants), Undecidability L19–22, Complexity L23–26, trackers, report.
- [x] Note 10 Atif TM_Basics (L11–13) built (tm_designs.py: 25 TMs verified). NEXT: A5 TM_Techniques (L14–15), A6 TM_Variants (L16–18), Undecidability L19–22, Complexity L23–26, trackers, report.
- [x] Note 11 Atif TM_Techniques (L14–15) built + checked. NEXT: A6 TM_Variants (L16–18), A7 Undecidability L19–22, A8 Complexity L23–26, trackers, report.
- [x] Note 12 Atif TM_Variants (L16–18) built.
- [x] Note 13 Atif Undecidability (L19–22) + Note 14 Atif Complexity (L23–26) built. ALL 14 NOTES DONE. NEXT: trackers + coverage check + final report.
- [x] Trackers built (Hakim 205 rows, Atif 166 + 1 outside); all 14 notes converted to PDF OK (9–19 pp). REMAINING: final report only.
