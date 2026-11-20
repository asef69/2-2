"""
tracker_lib.py — builds a TF Practice Tracker (.xlsx) identical in layout to
CSE 209/TF Prep/CSE209_RS_TF_Practice_Tracker.xlsx.

    from tracker_lib import build_tracker
    build_tracker(
        out_path=r"...\\CSE 211\\TF Prep\\CSE211_Hakim_TF_Practice_Tracker.xlsx",
        course="CSE 211", part_name="Hakim Sir", part_short="Hakim",
        qpdf="CSE 211 All Merged Questions.pdf",      # the file 'TF Page' refers to
        high_from="2019-20",                           # this session and later = ★★★ High
        old_codes="CSE 211 = current code; CSE 309 = old code for the same content.",
        tabs=[
          dict(sheet="1 Intro + Languages",            # ≤ 31 chars, no []:*?/\\
               title="Lec01–02 — Introduction & Languages",
               note_file="CSE211_Hakim_Intro_Languages_Notes.docx",
               rows=[dict(year="2022-23", course="CSE 211", qno="5(a)",
                          question="Short question text…",
                          topic="Alphabet, strings, languages — Lec02, sl. 4–18",
                          lesson="L2", marks=10, page=12, type="Theory",
                          in_notes="✔ Solved", same_type="2019-20 5(b); 2016-17 6(a)")]),
          ...],
        outside=[dict(year="2014-15", course="CSE 309", qno="7(c)", question="…",
                      area="Topic not in slides", marks=8, page=40)],
        notes_extra=["Optional extra lines for the Dashboard footnote"],
    )

Row fields: year, course, qno, question, topic, lesson ("L3"), marks (number), page (int or "40–41"),
type (Numerical | Trace | Design | Proof | Theory | Derivation …), in_notes (✔ Solved | ◐ Method | ○ Partly),
same_type ("" or "—" if none), optional priority override ("★★★ High" | "★★ Medium" | "★ Low").
Rows are sorted by lesson number, then newest year first; Q No. is assigned after sorting.
"""
import os
import re

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, DataBarRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

NAVY = "1F3864"
WHITE = "FFFFFF"
HDR_FILL = PatternFill("solid", fgColor=NAVY)
BAND = PatternFill("solid", fgColor="F2F2F2")
DONE_FILL = PatternFill("solid", fgColor="FFF2CC")
TOTAL_FILL = PatternFill("solid", fgColor="D9E1F2")
HIGH_YEAR_FILL = PatternFill("solid", fgColor="FBE5D6")
PRIO_FILL = {"★★★ High": "F8CBAD", "★★ Medium": "FFE699", "★ Low": "E2EFDA"}
NOTES_FILL = {"✔ Solved": "E2EFDA", "◐ Method": "DDEBF7", "○ Partly": "FCE4D6"}
THIN = Side(style="thin", color="D9D9D9")
GRID = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP_TOP = Alignment(wrap_text=True, vertical="top")
CENTER_TOP = Alignment(horizontal="center", vertical="top", wrap_text=True)

COLS = ["Q No.", "Year", "Course", "Ques No.", "Short Question", "Topic (slide PDF · slides)", "Lesson",
        "Marks", "TF Page", "Priority", "Type", "In Notes", "Same Type Also In", "Done", "Confidence",
        "Date", "My Notes"]
WIDTHS = [6, 9, 9, 10, 58, 40, 8, 7, 8, 12, 11, 11, 30, 7, 12, 11, 32]
CENTER_COLS = {1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 14, 15, 16}


def _year_key(y):
    m = re.match(r"(\d{4})", str(y))
    return int(m.group(1)) if m else 0


def _lesson_key(l):
    m = re.search(r"(\d+)", str(l))
    return int(m.group(1)) if m else 999


def _priority(row, high_from):
    if row.get("priority"):
        return row["priority"]
    if _year_key(row["year"]) >= _year_key(high_from):
        return "★★★ High"
    st = (row.get("same_type") or "").strip()
    return "★★ Medium" if st and st != "—" else "★ Low"


def _hdr(ws, r, labels, c0=1):
    for k, lab in enumerate(labels):
        c = ws.cell(r, c0 + k, lab)
        c.font = Font(bold=True, color=WHITE)
        c.fill = HDR_FILL
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = GRID


def _q(sheet):
    return "'" + sheet.replace("'", "''") + "'"


def build_tracker(out_path, course, part_name, part_short, qpdf, tabs, outside=None,
                  high_from="2019-20", old_codes=None, notes_extra=None):
    wb = Workbook()
    howto = wb.active
    howto.title = "How to Use"
    dash = wb.create_sheet("Dashboard")
    ranges = []  # (sheet, first_row, last_row)

    # ------------------------------------------------------------ topic tabs
    for t in tabs:
        ws = wb.create_sheet(t["sheet"][:31])
        rows = sorted(t["rows"], key=lambda r: (_lesson_key(r["lesson"]), -_year_key(r["year"]),
                                                 str(r["qno"])))
        ws["A1"] = t["title"]
        ws["A1"].font = Font(bold=True, size=14, color=NAVY)
        ws["A2"] = (f"Note file: {t['note_file']}   ·   Solve after finishing the matching lesson. "
                    f"Filter Priority → ★★★ High first.")
        ws["A2"].font = Font(italic=True, color="595959")
        _hdr(ws, 3, COLS)
        ws.row_dimensions[3].height = 30
        band_on, last_lesson = False, None
        for i, r in enumerate(rows):
            rr = 4 + i
            if r["lesson"] != last_lesson:
                band_on, last_lesson = (not band_on), r["lesson"]
            prio = _priority(r, high_from)
            vals = [i + 1, r["year"], r.get("course", course), r["qno"], r["question"], r["topic"], r["lesson"],
                    r.get("marks"), r.get("page"), prio, r.get("type", ""), r.get("in_notes", ""),
                    r.get("same_type") or "—", False, None, None, None]
            for ci, v in enumerate(vals, 1):
                c = ws.cell(rr, ci, v)
                c.border = GRID
                c.alignment = CENTER_TOP if ci in CENTER_COLS else WRAP_TOP
                if band_on:
                    c.fill = BAND
            ws.cell(rr, 10).fill = PatternFill("solid", fgColor=PRIO_FILL.get(prio, "FFFFFF"))
            nf = NOTES_FILL.get(r.get("in_notes", ""))
            if nf:
                ws.cell(rr, 12).fill = PatternFill("solid", fgColor=nf)
            ws.cell(rr, 14).fill = DONE_FILL
        last = 3 + max(len(rows), 1)
        for ci, w in enumerate(WIDTHS, 1):
            ws.column_dimensions[get_column_letter(ci)].width = w
        ws.freeze_panes = "F4"
        ws.auto_filter.ref = f"A3:Q{last}"
        dv1 = DataValidation(type="list", formula1='"TRUE,FALSE"', allow_blank=True)
        dv2 = DataValidation(type="list", formula1='"Weak,OK,Strong"', allow_blank=True)
        ws.add_data_validation(dv1)
        ws.add_data_validation(dv2)
        dv1.add(f"N4:N{last}")
        dv2.add(f"O4:O{last}")
        ws.conditional_formatting.add(f"A4:Q{last}", FormulaRule(
            formula=["$N4=TRUE"], fill=PatternFill("solid", fgColor="C6EFCE", bgColor="C6EFCE"),
            font=Font(color="006100")))
        ws.conditional_formatting.add(f"O4:O{last}", CellIsRule(
            operator="equal", formula=['"Weak"'], fill=PatternFill("solid", fgColor="FFC7CE", bgColor="FFC7CE"),
            font=Font(color="9C0006", bold=True)))
        ws.conditional_formatting.add(f"O4:O{last}", CellIsRule(
            operator="equal", formula=['"Strong"'], fill=PatternFill("solid", fgColor="C6EFCE", bgColor="C6EFCE"),
            font=Font(color="006100", bold=True)))
        ws.sheet_view.zoomScale = 90
        ranges.append((ws.title, 4, last, t))

    # ------------------------------------------------------------ outside notes
    if outside:
        ws = wb.create_sheet("Outside Notes")
        ws["A1"] = f"{part_short}-section questions on topics NOT in the current slides"
        ws["A1"].font = Font(bold=True, size=14, color=NAVY)
        ws["A2"] = "Mostly older papers. Ask sir/ma'am whether these topics are in this term's syllabus before practising them."
        ws["A2"].font = Font(italic=True, color="595959")
        oc = ["Q No.", "Year", "Course", "Ques No.", "Short Question", "Topic Area", "Marks", "TF Page", "Done",
              "My Notes"]
        _hdr(ws, 3, oc)
        out_rows = sorted(outside, key=lambda r: -_year_key(r["year"]))
        for i, r in enumerate(out_rows):
            vals = [i + 1, r["year"], r.get("course", course), r["qno"], r["question"], r.get("area", ""),
                    r.get("marks"), r.get("page"), False, None]
            for ci, v in enumerate(vals, 1):
                c = ws.cell(4 + i, ci, v)
                c.border = GRID
                c.alignment = WRAP_TOP if ci in (5, 6, 10) else CENTER_TOP
            ws.cell(4 + i, 9).fill = DONE_FILL
        lastO = 3 + max(len(out_rows), 1)
        for ci, w in enumerate([6, 9, 9, 10, 58, 34, 7, 8, 7, 32], 1):
            ws.column_dimensions[get_column_letter(ci)].width = w
        dv = DataValidation(type="list", formula1='"TRUE,FALSE"', allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"I4:I{lastO}")
        ws.conditional_formatting.add(f"A4:J{lastO}", FormulaRule(
            formula=["$I4=TRUE"], fill=PatternFill("solid", fgColor="C6EFCE", bgColor="C6EFCE")))
        ws.freeze_panes = "F4"
        ws.auto_filter.ref = f"A3:J{lastO}"

    # ------------------------------------------------------------ dashboard
    n = len(ranges)
    dash["A1"] = "Progress Dashboard"
    dash["A1"].font = Font(bold=True, size=16, color=NAVY)
    dash["A2"] = f"Updates automatically when you tick Done / set Confidence in tabs 1–{n}."
    dash["A2"].font = Font(italic=True, color="595959")
    _hdr(dash, 4, ["#", "Note file (tab)", "Questions", "Done", "% Done", "Marks (total)", "Marks done",
                   "High-priority left", "Weak", "Next unsolved (top of tab)"])
    for k, (sh, r0, r1, t) in enumerate(ranges):
        r = 5 + k
        q = _q(sh)
        E, N, H, J, O, A, B, D, I = (f"{q}!${c}${r0}:${c}${r1}" for c in "ENHJOABDI")
        m = f"MATCH(FALSE(),{N},0)"
        vals = [k + 1, sh, f"=COUNTA({E})", f"=COUNTIF({N},TRUE())", f"=IF(C{r}=0,0,D{r}/C{r})",
                f"=SUM({H})", f"=SUMIF({N},TRUE(),{H})", f'=COUNTIFS({J},"★★★ High",{N},FALSE())',
                f'=COUNTIF({O},"Weak")',
                f'=IFERROR("Q"&INDEX({A},{m})&" · "&INDEX({B},{m})&" "&INDEX({D},{m})&" · TF p."&INDEX({I},{m}),"All done ✔")']
        for ci, v in enumerate(vals, 1):
            c = dash.cell(r, ci, v)
            c.border = GRID
            c.alignment = Alignment(horizontal="left" if ci in (2, 10) else "center", vertical="center")
        dash.cell(r, 5).number_format = "0%"
    tr = 5 + n
    dash.cell(tr, 2, "TOTAL")
    for ci, col in zip(range(3, 10), "CDEFGHI"):
        f = f"=IF(C{tr}=0,0,D{tr}/C{tr})" if col == "E" else f"=SUM({col}5:{col}{tr - 1})"
        dash.cell(tr, ci, f)
    for ci in range(2, 10):
        c = dash.cell(tr, ci)
        c.fill, c.font, c.border = TOTAL_FILL, Font(bold=True), GRID
        c.alignment = Alignment(horizontal="center")
    dash.cell(tr, 5).number_format = "0%"
    dash.conditional_formatting.add(f"E5:E{tr}", DataBarRule(start_type="num", start_value=0, end_type="num",
                                                             end_value=1, color="63BE7B"))

    years = sorted({rw["year"] for *_, t in ranges for rw in t["rows"]}, key=_year_key, reverse=True)
    y0 = tr + 2
    dash.cell(y0, 1, f"Questions by year (tabs 1–{n})").font = Font(bold=True, size=12, color=NAVY)
    _hdr(dash, y0 + 1, ["#", "Year", "Questions", "Done", "% Done", "Marks (total)"])
    for k, y in enumerate(years):
        r = y0 + 2 + k
        cnt = "+".join(f"COUNTIF({_q(sh)}!$B${a}:$B${b},$B{r})" for sh, a, b, _ in ranges)
        done = "+".join(f"COUNTIFS({_q(sh)}!$B${a}:$B${b},$B{r},{_q(sh)}!$N${a}:$N${b},TRUE())"
                        for sh, a, b, _ in ranges)
        mk = "+".join(f"SUMIF({_q(sh)}!$B${a}:$B${b},$B{r},{_q(sh)}!$H${a}:$H${b})" for sh, a, b, _ in ranges)
        vals = [k + 1, y, "=" + cnt, "=" + done, f"=IF(C{r}=0,0,D{r}/C{r})", "=" + mk]
        hi = _year_key(y) >= _year_key(high_from)
        for ci, v in enumerate(vals, 1):
            c = dash.cell(r, ci, v)
            c.border = GRID
            c.alignment = Alignment(horizontal="center")
            if hi:
                c.fill = HIGH_YEAR_FILL
        dash.cell(r, 5).number_format = "0%"
    ylast = y0 + 1 + len(years)
    if years:
        dash.conditional_formatting.add(f"E{y0 + 2}:E{ylast}", DataBarRule(
            start_type="num", start_value=0, end_type="num", end_value=1, color="63BE7B"))
    foot = [f"Shaded years = ★★★ High priority ({high_from} onward)."] + list(notes_extra or [])
    for k, line in enumerate(foot):
        dash.cell(ylast + 1 + k, 2, line).font = Font(italic=True, color="595959")
    for col, w in zip("ABCDEFGHIJ", [4, 30, 11, 8, 9, 12, 11, 14, 7, 46]):
        dash.column_dimensions[col].width = w
    dash.freeze_panes = "A5"

    # ------------------------------------------------------------ how to use
    hw = howto
    hw.column_dimensions["A"].width = 3
    hw.column_dimensions["B"].width = 24
    hw.column_dimensions["C"].width = 95
    hw["B2"] = f"{course} ({part_name} part) — TF Practice Tracker"
    hw["B2"].font = Font(bold=True, size=16, color=NAVY)
    hw["B3"] = (f"Every {part_short}-part question in {qpdf}, mapped to the note file and lesson that teaches it.")
    hw["B3"].font = Font(italic=True, color="595959")

    def block(r, title, items):
        hw.cell(r, 2, title).font = Font(bold=True, color=WHITE)
        hw.cell(r, 2).fill = HDR_FILL
        hw.cell(r, 3).fill = HDR_FILL
        for k, (a, b) in enumerate(items, 1):
            ca, cb = hw.cell(r + k, 2, a), hw.cell(r + k, 3, b)
            ca.font = Font(bold=True)
            ca.alignment = cb.alignment = WRAP_TOP
            ca.border = cb.border = GRID
        return r + len(items) + 2

    r = block(5, "Workflow — after you finish a note file", [
        ("1. Open its tab", f"Tabs 1–{n} follow the order of your note files. Q No. runs lesson by lesson, newest year first inside each lesson."),
        ("2. Filter", f"Use the filter arrow on Priority → ★★★ High first ({high_from} onward). Then ★★ Medium, then ★ Low."),
        ("3. Solve", f"Open {qpdf} at the TF Page shown. Solve on paper under exam time (≈1.5 min per mark). Do not read the note solution first."),
        ("4. Check", "In Notes tells you what the note has: ✔ Solved = same question worked out; ◐ Method = method / model answer you can apply; ○ Partly = notes cover most of it, finish the rest yourself."),
        ("5. Record", "Tick Done, pick Confidence, add the Date. Write mistakes in My Notes. Re-solve every 'Weak' row before the exam."),
        ("6. Repeats", "'Same Type Also In' lists other papers with the same question type. Solve one, then try a repeat cold — that is the real test."),
    ])
    r = block(r, "Columns you edit (all others are fixed data)", [
        ("Done (col N)", "TRUE / FALSE. In Google Sheets: select N4 downward → Insert → Checkbox. The values stay; ticking turns the row green."),
        ("Confidence (col O)", "Dropdown: Weak / OK / Strong. Weak rows turn the cell red."),
        ("Date (col P)", "Date you solved it, e.g. 16-Oct-2026."),
        ("My Notes (col Q)", "Mistakes, missing steps, formula you forgot."),
    ])
    legend = [
        ("★★★ High", f"Asked in {high_from} or later (most important — current question style)."),
        ("★★ Medium", "Older paper, but the same question type appears at least twice in TF."),
        ("★ Low", "Older paper, asked once."),
        ("Type", "Numerical = calculation · Trace = tables / step-by-step simulation · Design = construct / draw · Proof = prove / disprove · Theory = explain."),
    ]
    if old_codes:
        legend.append(("Course", old_codes))
    legend.append(("Topic", "Note lesson title — slide PDF and slide numbers."))
    if outside:
        legend.append(("Outside Notes tab", f"{part_short}-section questions from older papers on topics not in the current slides. Check with your teacher before spending time on them."))
    block(r, "Legend", legend)
    hw.sheet_view.showGridLines = False

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wb.save(out_path)
    return out_path
