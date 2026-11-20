"""Index the cards of CSE211_Topicwise_TF_Solutions.pdf: card headers, stacked groups, page/y spans."""
import re, os
import pymupdf
SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "CSE211_Topicwise_TF_Solutions.pdf")
TOP_CONT, BOT_MAX = 52, 797


def year_key(label):
    label = label.strip()
    if label.startswith("January 2020"):
        return "2020 (Jan term)"
    m = re.match(r"(\d{4})\s*[–-]\s*(\d{4})", label)
    return f"{m.group(1)}-{m.group(2)[2:]}" if m else label


def index(doc):
    H, S, R = [], [], []
    for pno in range(len(doc)):
        for b in doc[pno].get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for l in b["lines"]:
                t = "".join(s["text"] for s in l["spans"]).strip()
                y = l["bbox"][1]
                if "Source" in t and "•" in t and re.match(r"^\S.*•\s*Q", t):
                    left, right = t.split("•", 1)
                    q = re.match(r"\s*(Q\S+(?:\s\S+)*?)\s+Source", right).group(1)
                    H.append(dict(pno=pno, y=y, year=year_key(left), q=q[1:], label=t))
                elif t == "SOLUTION":
                    S.append((pno, y))
                elif t.startswith("REPEATED"):
                    R.append((pno, y))
    H.sort(key=lambda h: (h["pno"], h["y"]))
    groups, cur = [], None
    for i, h in enumerate(H):
        new = cur is None
        if cur is not None:
            prev = H[i - 1]
            new = any((prev["pno"], prev["y"]) < s < (h["pno"], h["y"]) for s in S)
        if new:
            cur = dict(cards=[], start=None)
            groups.append(cur)
        cur["cards"].append(h)
    for g in groups:
        f = g["cards"][0]
        top = f["y"] - 14
        for rp, ry in R:
            if rp == f["pno"] and 0 < f["y"] - ry < 45:
                top = ry - 6
        g["start"] = (f["pno"], max(top, 40))
    return H, groups


def content_bottom(page):
    bot = 60
    for b in page.get_text("dict")["blocks"]:
        if b["bbox"][3] < 798 and b["bbox"][1] > 50:
            bot = max(bot, b["bbox"][3])
    for d in page.get_drawings():
        r = d["rect"]
        if r.y1 < 798 and r.y0 > 50 and r.width < 560:
            bot = max(bot, r.y1)
    return min(bot + 8, BOT_MAX)


def spans(doc, groups, k):
    """clip rectangles [(pno, rect)] for group k"""
    s_p, s_y = groups[k]["start"]
    if k + 1 < len(groups):
        e_p, e_y = groups[k + 1]["start"]
    else:
        e_p, e_y = len(doc) - 1, None
    out = []
    W = doc[0].rect.width
    for p in range(s_p, e_p + 1):
        y0 = s_y if p == s_p else TOP_CONT
        if p == e_p and e_y is not None:
            y1 = e_y - 4
        else:
            y1 = content_bottom(doc[p])
        if p == e_p and e_y is not None and e_y < 75 and p != s_p:
            continue
        if y1 - y0 > 10:
            out.append((p, pymupdf.Rect(0, y0, W, y1)))
    return out
