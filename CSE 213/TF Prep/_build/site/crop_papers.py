"""crop_papers.py — cuts CSE213_Topicwise_TF_Solutions.pdf into one image per question group (question card(s) + solution).
Writes site/img/q/gNNN.webp and site/data/groups.json."""
import io
import json
import os
import re
import sys

import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "CSE213_Topicwise_TF_Solutions.pdf")
OUTD = os.path.join(HERE, "img", "q")
os.makedirs(OUTD, exist_ok=True)
CORAL = (0.906, 0.435, 0.318)
HEAD = re.compile(r"^(.+?) • (Q.+?)\s+(CSE\s?\d+) •")
PRAC = re.compile(r"^Practice (\d+) • (.+)")
CARDHEAD = re.compile(r"^(\d{4}\D\d{4}|Jan 2021|Practice \d) • ")
DPI = 100
X0, X1 = 46, 550

d = pymupdf.open(SRC)
toc = d.get_toc()
chap_start = {p - 1: t for _, t, p in toc}          # 0-based page -> title
chap_of = {}
cur_ch = None
for pno in range(d.page_count):
    if pno in chap_start:
        cur_ch = chap_start[pno]
    chap_of[pno] = cur_ch


def close(c, ref, tol=0.02):
    return c is not None and all(abs(a - b) < tol for a, b in zip(c, ref))


groups = []     # {strips:[(pno,y0,y1)], entries:[...], chapter}
cur = None
state = None


def start(pno, y, ch):
    global cur, state
    cur = {"strips": [], "entries": [], "chapter": ch, "ptr": y, "pno": pno}
    groups.append(cur)
    state = "q"


def close_strip(pno, y1):
    if cur and cur["ptr"] is not None and y1 - cur["ptr"] > 3:
        cur["strips"].append((cur["ptr"] and pno, cur["ptr"], y1))


for pno in range(4, d.page_count):
    pg = d[pno]
    blocks = pg.get_text("blocks")
    ev = []
    for dr in pg.get_drawings():
        r = dr["rect"]
        if close(dr.get("fill"), CORAL) and r.width > 400 and r.height > 10:
            hdr = ""
            for b in blocks:
                if r.y0 - 1 <= b[1] <= r.y1 and CARDHEAD.match(b[4].strip()):
                    hdr = b[4].strip()
                    break
            ev.append(("card", r.y0 - 2, r.y1 + 2, hdr))
    for b in blocks:
        t = b[4].lstrip()
        if t.startswith("REPEATED"):
            ev.append(("banner", b[1] - 7, b[3], ""))
        elif t.startswith("SOLUTION") and len(t) < 14:
            ev.append(("sol", b[1], b[3], ""))
    ev.sort(key=lambda e: e[1])
    # a repeated group: collapse the header cards
    bottoms = [b[3] for b in blocks if b[3] < 795]
    bottom = min(max(bottoms) + 8, 790) if bottoms else 790
    is_chap = pno in chap_start
    ptr = 56
    if is_chap:
        cur = None
        state = None
    if cur is not None:
        cur["ptr"] = ptr
        cur["pno"] = pno
    for kind, y0, y1, hdr in ev:
        trigger = kind == "banner" or (kind == "card" and (cur is None or state == "s"))
        if trigger and not (kind == "card" and cur is not None and state == "q"):
            if cur is not None:
                cur["strips"].append((pno, cur["ptr"], max(y0, cur["ptr"] + 1)))
            start(pno, y0, chap_of[pno])
            cur["ptr"] = y0
            cur["pno"] = pno
        if kind == "card" and cur is not None and hdr:
            first = hdr.split("\n")[0]
            mk = (re.search(r"MARKS\s+([^\n]+)", hdr) or [0, ""])[1].strip()
            dt = re.search(r"(\d\d/\d\d/\d{4})", first)
            pm = PRAC.match(first)
            if pm:
                cur["entries"].append(dict(kind="practice", n=pm.group(1), title=pm.group(2), marks=mk))
            else:
                m = HEAD.match(first)
                sess = m.group(1)
                ym = re.match(r"(\d{4})\D(\d{4})", sess)
                year = "%s-%s" % (ym.group(1), ym.group(2)[2:]) if ym else "2020-21"
                if sess.startswith("2023") and dt and dt.group(1).endswith("2026"):
                    year = "2024-25"
                cur["entries"].append(dict(kind="paper", year=year, session=sess, course=m.group(3).replace("CSE", "CSE "), qno=m.group(2)[1:],
                                           date=dt.group(1) if dt else "", ident=first.split(" • ")[-1], marks=mk))
        if kind == "sol":
            state = "s"
    if cur is not None:
        cur["strips"].append((pno, cur["ptr"], bottom))
        cur["ptr"] = 56      # next page starts below the running header

print("groups", len(groups), "entries", sum(len(g["entries"]) for g in groups))
bad = [i for i, g in enumerate(groups) if not g["entries"]]
print("groups without entries:", bad[:20])

# ---- render
total = 0
meta = []
for gi, g in enumerate(groups, 1):
    if not g["entries"]:
        continue
    parts = []
    for pno, y0, y1 in g["strips"]:
        if y1 - y0 < 2:
            continue
        pix = d[pno].get_pixmap(dpi=DPI, clip=pymupdf.Rect(X0, y0, X1, y1))
        parts.append(Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB"))
    w = max(p.width for p in parts)
    h = sum(p.height for p in parts)
    im = Image.new("RGB", (w, h), "white")
    y = 0
    for p in parts:
        im.paste(p, (0, y))
        y += p.height
    name = "g%03d.webp" % gi
    im.save(os.path.join(OUTD, name), "WEBP", quality=62, method=6)
    total += os.path.getsize(os.path.join(OUTD, name))
    meta.append(dict(gid=gi, img="img/q/" + name, w=w, h=h, chapter=g["chapter"], entries=g["entries"]))
json.dump(meta, open(os.path.join(HERE, "data", "groups.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("images", len(meta), "MB", round(total / 1e6, 1))
