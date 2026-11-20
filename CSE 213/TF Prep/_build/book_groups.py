"""book_groups.py — splits the topic-wise solution book into question groups.

A group = an optional 'REPEATED' banner + one or more question cards + the SOLUTION that follows,
up to the start of the next group (or chapter). Each group is a list of (page, y0, y1) strips.
Used by rebuild_books.py (and to search group text)."""
import re

import pymupdf

CORAL = (0.906, 0.435, 0.318)
HEAD = re.compile(r"^(\d{4}\D\d{4}|[A-Z][a-z]{2} \d{4}) • Q")
TOP, FOOT = 27, 796          # page content area in the source (below the running header, above the page number)


def _close(c, ref, tol=0.02):
    return c is not None and all(abs(a - b) < tol for a, b in zip(c, ref))


def cards(pg):
    rs = []
    for dr in pg.get_drawings():
        r = dr["rect"]
        if _close(dr.get("fill"), CORAL) and r.width > 400 and r.height > 10:
            rs.append((r.y0, r.y1))
    return sorted(rs)


def starts(pg):
    """y positions where a new group starts on this page: a REPEATED banner, or a card whose header
    is not directly preceded by another card/banner (i.e. preceded by solution content)."""
    blocks = pg.get_text("blocks")
    banners = [b[1] for b in blocks if b[4].lstrip().startswith("REPEATED")]
    heads = sorted(b[1] for b in blocks if HEAD.match(b[4].strip()))
    cs = cards(pg)
    out = list(banners)
    for h in heads:
        card = next((c for c in cs if c[0] - 2 <= h <= c[1]), None)
        if card is None:
            continue
        top = card[0]
        # previous thing above this card: another card or banner within 22 pt -> same group
        prev_card = any(0 <= top - c1 <= 22 for c0, c1 in cs if c1 <= top)
        prev_banner = any(0 <= top - b <= 40 for b in banners)
        if not prev_card and not prev_banner:
            out.append(top)
    return sorted(set(round(y - 3, 1) for y in out))


def groups(doc, first, last, chapter_pages):
    """Groups between 0-based pages first..last (inclusive). chapter_pages: 1-based pages that start a chapter."""
    res, cur = [], None
    for pno in range(first, last + 1):
        pg = doc[pno]
        top = TOP
        if pno + 1 in chapter_pages:          # skip the chapter banner/title
            cs = cards(pg)
            ss = starts(pg)
            top = min(ss) if ss else (cs[0][0] - 3 if cs else FOOT)
            if cur:
                res.append(cur)
                cur = None
        cuts = [y for y in starts(pg) if y >= top - 1]
        y0 = top
        for c in cuts:
            if cur is not None and c > y0 + 2:
                cur["strips"].append((pno, y0, c))
            if cur is not None:
                res.append(cur)
            cur = {"strips": [], "page": pno}
            y0 = c
        if cur is not None:
            cur["strips"].append((pno, y0, FOOT))
    if cur:
        res.append(cur)
    for g in res:
        g["text"] = "\n".join(doc[p].get_textbox(pymupdf.Rect(0, a, 600, b)) for p, a, b in g["strips"])
        g["heads"] = [l for l in g["text"].split("\n") if HEAD.match(l.strip())]
    return res
