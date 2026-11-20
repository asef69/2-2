"""html_notes.py — HtmlNotes: same API as notes_lib.Notes, but emits HTML sections (for the CSE 213 Green Card site).
Used by make_site.py, which injects it as the module `notes_lib` so the existing build_notes_*.py scripts run unchanged."""
import hashlib
import html
import io
import json
import os
import re

import pymupdf
from PIL import Image

_TOKEN = re.compile(r"(\*\*.+?\*\*|\*[^*\s][^*]*?\*|`[^`]+`|\^\{[^}]*\}|_\{[^}]*\})")
OUT = None          # set by make_site: output dir (contains img/)
RESULT = {}         # note-file key -> dict
PRACTICE = []       # global list of practice blocks


def esc(t):
    return html.escape(str(t), quote=False)


def inline(text):
    out = []
    for part in _TOKEN.split(str(text)):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            out.append("<strong>%s</strong>" % esc(part[2:-2]))
        elif part.startswith("`") and part.endswith("`"):
            out.append("<code>%s</code>" % esc(part[1:-1]))
        elif part.startswith("^{"):
            out.append("<sup>%s</sup>" % esc(part[2:-1]))
        elif part.startswith("_{"):
            out.append("<sub>%s</sub>" % esc(part[2:-1]))
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            out.append("<em>%s</em>" % esc(part[1:-1]))
        else:
            out.append(esc(part))
    return "".join(out)


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:60]


CALL = {"focus": "Exam focus", "memorize": "Memorize", "trap": "Trap", "answer": "Exam-ready answer", "note": "Note"}


class Notes:
    def __init__(self, course, course_title, topic, part_label, part_tag, out_path, tagline=""):
        self.key = os.path.basename(out_path).replace(".docx", "")
        self.topic, self.part_label, self.part_tag = topic, part_label, part_tag
        self.sections = []      # {title, source, kind, html}
        self.cur = None
        self.source_note = None
        self.contents = []
        self._sol = False
        self._prac = None       # buffer for the current practice block
        self._prac_meta = None
        self._fig_dpi = 200
        self.doc = None

    # ---------------------------------------------------------------- plumbing
    def _e(self, h):
        if self.cur is None:
            self.h1("Introduction", new_page=False)
        self.cur["html"].append(h)
        if self._prac is not None:
            self._prac.append(h)

    def _close_sol(self):
        if self._sol:
            self._sol = False
            self._e("</div></details>")

    def _close_prac(self):
        self._close_sol()
        if self._prac is not None:
            PRACTICE.append(dict(file=self.key, section=self.cur["title"] if self.cur else "", **self._prac_meta,
                                 html="".join(self._prac)))
            self._prac = None

    def _finish(self):
        self._close_prac()

    # ---------------------------------------------------------------- front matter / headings
    def front_matter(self, contents, source_note=None):
        self.contents = contents
        self.source_note = source_note

    def page_break(self):
        pass

    def h1(self, text, new_page=True):
        self._close_prac()
        kind = "lesson" if text.startswith("Lesson") else "map" if text.startswith("Exam Map") else \
            "quick" if text.startswith("Quick Notes") else "senior" if text.startswith("Senior Diagram") else "other"
        self.cur = {"title": text, "source": "", "kind": kind, "html": []}
        self.sections.append(self.cur)

    def lesson(self, title, source=None):
        self.h1(title)
        if source:
            self.source(source)

    def source(self, text):
        self.cur["source"] = text

    def h2(self, text, color=None):
        self._close_prac()
        self._e("<h3 class='%s'>%s</h3>" % ("pr" if color else "", inline(text)))

    def h3(self, text, color=None):
        if color and "Solution" in text:
            self._e("<details class='sol'><summary>Show solution</summary><div class='solbody'>")
            self._sol = True
            return
        self._e("<h4>%s</h4>" % inline(text))

    # ---------------------------------------------------------------- body
    def p(self, text, size=None, color=None, align=None, after=None):
        self._e("<p%s>%s</p>" % (" class='c'" if align == "center" else "", inline(text)))

    def bullets(self, items, level=0):
        out = ["<ul>"]
        for it in items:
            if isinstance(it, (list, tuple)):
                out.append(self._sub(it))
            else:
                out.append("<li>%s</li>" % inline(it))
        out.append("</ul>")
        self._e("".join(out))

    def _sub(self, items):
        out = ["<ul>"]
        for it in items:
            out.append(self._sub(it) if isinstance(it, (list, tuple)) else "<li>%s</li>" % inline(it))
        out.append("</ul>")
        return "".join(out)

    def numbered(self, items):
        self._e("<ol>%s</ol>" % "".join("<li>%s</li>" % inline(i) for i in items))

    def callout(self, kind, text, extra=None):
        body = "<p>%s</p>" % inline(text)
        for ex in extra or []:
            body += "<p>%s</p>" % inline(ex)
        self._e("<div class='co co-%s'><div class='cl'>%s</div>%s</div>" % (kind, CALL[kind], body))

    def code(self, lines, size=9):
        if isinstance(lines, str):
            lines = lines.split("\n")
        self._e("<pre class='code'><code>%s</code></pre>" % esc("\n".join(lines)))

    def formula(self, lines, size=11):
        if isinstance(lines, str):
            lines = [lines]
        self._e("<div class='formula'>%s</div>" % "<br>".join(inline(l) for l in lines))

    def table(self, headers, rows, widths_cm=None, font_size=9.5, first_col_bold=False, zebra=True):
        h = "".join("<th>%s</th>" % inline(x) for x in headers)
        body = []
        for r in rows:
            cells = []
            for ci, v in enumerate(r):
                t = "<br>".join(inline(x) for x in str(v).split("\n"))
                cells.append("<td>%s</td>" % (("<strong>%s</strong>" % t) if first_col_bold and ci == 0 else t))
            body.append("<tr>%s</tr>" % "".join(cells))
        self._e("<div class='tbl'><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (h, "".join(body)))

    # ---------------------------------------------------------------- figures
    def figure_from_pdf(self, pdf_path, page, caption, clip=None, width_cm=12.0, dpi=None):
        doc = pymupdf.open(pdf_path)
        pg = doc[page - 1]
        r = pg.rect
        kw = {"dpi": 110}
        if clip:
            x0, y0, x1, y1 = clip
            kw["clip"] = pymupdf.Rect(r.x0 + x0 * r.width, r.y0 + y0 * r.height, r.x0 + x1 * r.width, r.y0 + y1 * r.height)
        pix = pg.get_pixmap(**kw)
        self.figure_bytes(pix.tobytes("png"), caption, width_cm)

    def figure_image(self, image_path, caption, width_cm=12.0):
        with open(image_path, "rb") as f:
            self.figure_bytes(f.read(), caption, width_cm)

    def figure_bytes(self, png_bytes, caption, width_cm=12.0):
        name = "f" + hashlib.md5(png_bytes).hexdigest()[:10] + ".webp"
        path = os.path.join(OUT, "img", name)
        if not os.path.exists(path):
            Image.open(io.BytesIO(png_bytes)).convert("RGB").save(path, "WEBP", quality=78, method=6)
        self._e("<figure class='fig'><img src='img/%s' alt='%s' loading='lazy' data-zoom='1'><figcaption>%s</figcaption></figure>"
                % (name, html.escape(caption, quote=True), inline(caption)))

    # ---------------------------------------------------------------- practice
    def exam_approach(self, steps):
        self.h2("Exam approach")
        self.numbered(steps)

    def practice(self, lesson_label, provenance, questions):
        self._close_prac()
        self._prac = []
        self._prac_meta = dict(label=lesson_label, prov=provenance)
        self._e("<h3 class='pr'>Practice — %s</h3><p class='prov'>%s</p>" % (esc(lesson_label), inline(provenance)))
        for q in questions:
            m = re.match(r"^(\([a-z0-9ivx]+\))\s*(.*)$", q, re.S)
            self._e("<p class='pq'>%s</p>" % (("<strong>%s</strong> %s" % (esc(m.group(1)), inline(m.group(2)))) if m else inline(q)))

    def solution(self):
        self._e("<details class='sol'><summary>Show solution</summary><div class='solbody'>")
        self._sol = True

    def answer(self, label, text):
        self._e("<p class='ans'><strong>%s</strong> %s</p>" % (esc(label), inline(text)))

    # ---------------------------------------------------------------- quick notes
    def quick_notes(self, title, intro, groups, diagrams=None):
        self.h1(title)
        self._e("<p class='prov'>%s</p>" % inline(intro))
        for head, pts in groups:
            self.h2(head)
            self.bullets(pts)
        if diagrams:
            self.h2("Key diagrams to reproduce")
            for d in diagrams:
                self.figure_from_pdf(d[0], d[1], d[2], clip=d[3] if len(d) > 3 else None)

    def save(self):
        self._finish()
        RESULT[self.key] = dict(key=self.key, topic=self.topic, part=self.part_tag, contents=self.contents,
                                source_note=self.source_note,
                                sections=[dict(title=s["title"], source=s["source"], kind=s["kind"], html="".join(s["html"]))
                                          for s in self.sections])
        return self.key
