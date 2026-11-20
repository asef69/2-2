# TF Prep — format spec (shared by all course sessions)

Goal: for each course, turn the teacher's **slides** and the **previous years' term-final (TF) questions**
into the same study kit that exists for CSE 209 (Rifat Sir part):

1. **Lesson notes** — one `.docx` per slide deck (or per small group of related decks), and
2. **TF Practice Tracker** — one `.xlsx` per teacher's part. It maps every past TF question of that
   teacher's section to the note file + lesson that teaches it.

## 0. The gold reference: read it before you write anything

`CSE 209/TF Prep/` holds the finished kit for Rifat Sir's part of CSE 209:

- `notes/CSE209_Control_Unit_Notes.docx` (short), `notes/CSE209_Ch4_SingleCycle_Notes.docx`,
  `notes/CSE209_Ch4_Part2_Pipelining_Notes.docx` (long)
- `CSE209_RS_TF_Practice_Tracker.xlsx`

Dump them as text and read **at least two notes files in full**, plus the tracker. Match their
**depth, tone and structure**, not just their look:

```bash
python -P _tfprep/tools.py docx "CSE 209/TF Prep/notes/CSE209_Control_Unit_Notes.docx"
```

## 1. Folder layout (write only inside your own course folder)

```
<COURSE>/TF Prep/
    notes/<CODE>_<Teacher>_<Topic>_Notes.docx      e.g. CSE211_Hakim_DFA_Notes.docx
    <CODE>_<Teacher>_TF_Practice_Tracker.xlsx      e.g. CSE211_Hakim_TF_Practice_Tracker.xlsx
    _build/                                         your build scripts (build_notes_*.py, build_tracker.py, questions.json)
```

`<CODE>` has no space (CSE211). `<Teacher>` is a short name taken from the slide folder name
(Hakim, Atif, Anindya, IJ, Anik, Ashraf, ART …). Keep the build scripts in `_build/`, so a note can be
fixed and rebuilt later.

## 2. Tooling (shared, do NOT edit — extend in your own script if you need more)

- `_tfprep/notes_lib.py` — `Notes` class: front matter, h1/lesson/h2/h3, p, bullets, numbered, table,
  callout(focus|memorize|trap|answer|note), code (grey mono box), formula (centred grey box),
  figure_from_pdf (renders and crops a slide), practice / solution / answer, quick_notes, save.
  Inline markup: `**bold**`, `*italic*`, `` `mono` ``, `^{sup}`, `_{sub}`. Read the docstrings.
- `_tfprep/tracker_lib.py` — `build_tracker(...)`. Read the docstring for the row fields.
- `_tfprep/tools.py` — `text`, `render` (PNG per page, then look at it with the Read tool), `sheet`
  (contact sheet of many slides), `pptx`, `docx`.
- Run Python as `python -P script.py` (libraries are in the user site-packages; `-I` hides them).
  Add `sys.path.insert(0, r"<repo>/_tfprep")` in your scripts.
- To check a note visually, convert it to PDF with Word, then render 2–4 pages and look at them:
  ```powershell
  $w=New-Object -ComObject Word.Application; $w.Visible=$false; $d=$w.Documents.Open("<abs>.docx",$false,$true); $d.SaveAs2("<abs-in-your-scratchpad>.pdf",17); $d.Close($false); $w.Quit()
  ```
  Other sessions use Word too. If the COM call fails, wait 20 s and retry. Always `Quit()`.
  Write those PDFs to your scratchpad, never into the course folder.

## 3. Process

### 3.1 Read every slide — no skimming
- Get the text of each deck with `tools.py text`. Many slides are diagram-heavy (low characters per
  page) or scanned (0 characters). For those, **render them and look at them** (`render`, or a
  `sheet` contact sheet for a quick pass, then full-size pages for anything with content).
- Note for each deck: its topics, slide ranges, worked examples, definitions, algorithms, figures
  worth reproducing, and anything the teacher stressed.

### 3.2 Read every question paper
- The merged question PDF (`TF questions/*All Merged*.pdf` or similar) is the **TF page** reference.
  Every `page` in the tracker is a 1-based page number in **that** file. Also read the separate
  newest-batch paper (`(22 batch).pdf`, scanned) and any other files in `TF questions/`.
  If the newest paper is not inside the merged PDF, give its rows `page` = `"22 batch p.N"`.
- Scanned pages must be **rendered and read visually**. Do not guess at text you cannot see.
- For every paper, record: session/year (e.g. `2022-23`), course code (old codes count — note
  them in `old_codes`), section (A/B), question numbers, sub-parts, marks, and a short paraphrase.
- Assign each question to a **teacher's part**. BUET papers usually give one section per teacher.
  Confirm this from the topics, not from the section letter alone. Parts that match neither teacher's
  slides go in that teacher's **Outside Notes** tab (or are left out if they belong to the other
  section). Say which in your final report.
- Save the master list as `_build/questions.json`.
- `Analysis/<COURSE>_*.pdf` (an earlier analysis made for this user) may be used as a **cross-check
  only**. Your own reading of the papers wins.

### 3.3 Map and plan
- Map each question → note file → lesson (`L<n>`, numbered **continuously across all of that
  teacher's note files**, as RS does L1…L32) → slide numbers.
- Group repeats: "Same Type Also In" lists the other papers with the same *type* of question.
- Plan the note files: normally one per slide deck. Merge decks only when they are tiny and on the same
  topic (e.g. 4-page lectures). Lessons are ~5–15 slides of one sub-topic each.

### 3.4 Write the notes (one build script per note file)
Every note file has, in order:
1. `front_matter(contents, source_note)` — title, legend, contents, plus a NOTE saying which PDF the
   slide numbers refer to.
2. **Exam Map — What the TF Papers Ask**: a table of every TF question that this deck answers
   (session, Q no., short wording, marks), then an EXAM FOCUS callout that says how often the topic
   is asked, which years, and what to learn first. If no question comes from the deck, say so plainly
   ("insurance topic").
3. **Lessons** (`n.lesson("Lesson N — Title", "Slides a–b (Deck name)")`). Inside each lesson:
   - Teach **everything on the slides**, in order, in clear exam-ready English: definitions, theorems
     (with proof ideas when the course asks for proofs), algorithms step by step, every worked example
     (redo it in full, do not just cite it), tables. Cite slide numbers in the headings: `(sl. 12–15)`.
   - Add the standard textbook background the slides assume when a question needs it, and mark it
     ("textbook").
   - Figures: crop the important diagrams from the slides with `figure_from_pdf` (clip as page
     fractions), with the caption `Figure N.k — … (sl. x)`. Use them where a diagram really carries
     the content. Don't paste whole text slides.
   - Callouts: MEMORIZE for formulas and rules, TRAP for the usual mistakes, EXAM-READY ANSWER for
     model wording to theory questions that appeared in TF, NOTE for clarifications.
   - **Exam Approach**: a numbered recipe for the lesson's question types.
   - **Practice — Lesson N**: 2–4 questions. Use the **actual TF questions** wherever they exist
     (label each one: `Actual — 2022-23 Q5(b)`, `Adapted — …`, `Constructed`). Then `✔ Solution` with
     **complete, correct, step-by-step solutions**, written the way a top student would write them
     in the exam.
   - Every ★★★ question (2019-20 onward), and every question type that repeats, must be **solved in
     full** somewhere in the notes. For anything else, at least give the method.
4. **Quick Notes — <Topic>** (new page): revision bullets grouped per lesson (`L3 · Title`), then
   **Key Diagrams to Reproduce**.

Language: plain, precise English. Short sentences. No filler. Unicode maths (Σ, δ, ∈, ≤, →, ⊆, ∫, ω,
²…) and `^{}` / `_{}` for super/subscripts. Put long derivations and tables in `code` or `table`.

### 3.5 Build the tracker
- One tab per note file, in the same order as the notes: `"1 <short name>"`, `"2 …"` (≤ 31 chars).
- `in_notes`: `✔ Solved` (that exact question is solved in the notes), `◐ Method` (the method or a
  model answer is there), `○ Partly`.
- `type`: Numerical / Trace / Design / Proof / Derivation / Theory (pick what fits the course).
- `high_from="2019-20"` unless the papers make a different cut obviously better. If they do,
  say why in `notes_extra`.
- Out-of-syllabus questions go in `outside=[...]`.

### 3.6 Verify before reporting
- **Coverage**: every question of the teacher's section in every paper appears exactly once in the
  tracker (topic tab or Outside Notes). Print a count per paper and compare it with the papers.
- **Correctness**: re-check every numerical answer with a quick Python computation. Re-derive
  constructions (DFA/PDA/TM traces, convolution sums, transforms, pattern code, probabilities…)
  instead of trusting memory.
- **Look**: convert each docx to PDF, then render and view at least the first page, one lesson page with
  a figure, and one solution page. Fix overflowing tables, unreadable crops and broken markup.
- The tracker opens with openpyxl, and each tab's row count matches your list.

## 4. Rules
- Write only inside your own course folder (`<COURSE>/TF Prep/…`). Don't edit `_tfprep/`, the slides,
  the question PDFs, `Analysis/`, or another course's folder. Don't commit to git.
- Never invent a past question, a year or a mark. If something is illegible, write `[illegible]` and
  list it in your final report.
- Final report (your last message): the files you produced (paths); questions per paper and per teacher;
  which questions went to Outside Notes; anything illegible or uncertain; the time and effort the kit
  points at (the top 5 topics by marks since 2019-20).
