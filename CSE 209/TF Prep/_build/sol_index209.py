"""Index the cards of CSE209_Topicwise_Solutions.pdf (Mahdi Hasan's solved set): headers, stacked groups, clip spans."""
import os, re
import pymupdf
SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "CSE209_Topicwise_Solutions.pdf")
TOP_CONT, BOT_MAX = 52, 797
HDR = re.compile(r"^(\d{4})\s*[–-]\s*(\d{4})\s*•\s*(Q\S+(?:\s\S+)*?)\s*(?:CSE\s*(\d+).*)?$")


def is_topic_page(page):
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                if s["size"] >= 18 and s["text"].strip():
                    return True
    return False


def index(doc):
    H, S, R, T = [], [], [], set()
    for pno in range(len(doc)):
        if is_topic_page(doc[pno]):
            T.add(pno)
        lines = []
        for b in doc[pno].get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for l in b["lines"]:
                lines.append(("".join(s["text"] for s in l["spans"]).strip(), l["bbox"][1], l["bbox"][0]))
        for t, y, x in lines:
            m = HDR.match(t)
            if m:
                course = m.group(4)
                if not course:  # course sits in a neighbouring line on the same baseline
                    for t2, y2, x2 in lines:
                        mm = re.search(r"CSE\s*(\d+)", t2)
                        if mm and abs(y2 - y) < 4 and x2 > x:
                            course = mm.group(1)
                H.append(dict(pno=pno, y=y, year=f"{m.group(1)}-{m.group(2)[2:]}", q=m.group(3)[1:], course=course))
            elif t == "SOLUTION":
                S.append((pno, y))
            elif t.startswith("REPEATED"):
                R.append((pno, y))
    H = [h for h in H if h["year"] != "2099-00" and not h["q"].startswith("0")]
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
    return H, groups, T


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


def spans(doc, groups, T, k):
    s_p, s_y = groups[k]["start"]
    if k + 1 < len(groups):
        e_p, e_y = groups[k + 1]["start"]
    else:
        e_p, e_y = len(doc) - 1, None
    out = []
    W = doc[0].rect.width
    for p in range(s_p, e_p + 1):
        if p != s_p and p in T:      # a new topic starts here: nothing of this group lives on it
            continue
        y0 = s_y if p == s_p else TOP_CONT
        y1 = (e_y - 4) if (p == e_p and e_y is not None) else content_bottom(doc[p])
        if p == e_p and e_y is not None and e_y < 75 and p != s_p:
            continue
        if p == e_p - 1 and e_y is not None and e_y < 75:   # a REPEATED tag at the foot of this page belongs to the next group
            for b in doc[p].get_text("dict")["blocks"]:
                for l in (b.get("lines") or []):
                    if "".join(sp["text"] for sp in l["spans"]).strip().startswith("REPEATED") and l["bbox"][1] > 600:
                        y1 = min(y1, l["bbox"][1] - 6)
        if y1 - y0 > 10:
            out.append((p, pymupdf.Rect(0, y0, W, y1)))
    return out
