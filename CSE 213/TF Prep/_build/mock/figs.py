"""figs.py - tiny UML/diagram drawing engine (reportlab Flowable) for the CSE 213 mock paper solutions."""
import math

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Flowable

INK = colors.Color(0.13, 0.15, 0.18)
FILL = colors.Color(0.96, 0.97, 0.99)
CLS = colors.Color(0.93, 0.96, 1.0)
STATE = colors.Color(0.94, 0.98, 0.94)
UC = colors.Color(1.0, 0.97, 0.90)
GREY = colors.Color(0.45, 0.48, 0.52)
FONT, BOLD, ITAL = "Seg", "SegB", "SegI"


def sw(t, size, f=FONT):
    return pdfmetrics.stringWidth(t, f, size)


class Node:
    def __init__(self, name, kind, x, y, w, h, **kw):
        self.name, self.kind, self.x, self.y, self.w, self.h = name, kind, x, y, w, h
        self.kw = kw

    @property
    def c(self):
        return (self.x + self.w / 2, self.y + self.h / 2)

    def anchor(self, tx, ty):
        """border point of the node facing the target point (tx, ty)."""
        cx, cy = self.c
        dx, dy = tx - cx, ty - cy
        if dx == 0 and dy == 0:
            return cx, cy
        if self.kind in ("ellipse", "circle", "diamond", "bstart", "bend"):
            a, b = self.w / 2, self.h / 2
            if self.kind == "diamond":
                t = 1.0 / (abs(dx) / a + abs(dy) / b)
            else:
                t = 1.0 / math.sqrt((dx / a) ** 2 + (dy / b) ** 2)
            return cx + dx * t, cy + dy * t
        a, b = self.w / 2, self.h / 2
        t = min(a / abs(dx) if dx else 1e9, b / abs(dy) if dy else 1e9)
        return cx + dx * t, cy + dy * t


class Fig(Flowable):
    """Coordinates are in points, origin bottom-left. The figure is scaled down to the available width."""

    def __init__(self, w, h, caption=None):
        super().__init__()
        self.W, self.H = w, h
        self.caption = caption
        self.nodes = {}
        self.ops = []          # ("node", Node) / ("edge", ...) / ("text", ...) / ("raw", fn)
        self.scale = 1.0

    # ------------------------------------------------------------------ builders
    def cls(self, name, x, y, w, attrs=(), ops=(), stereo=None, abstract=False, size=7.5):
        lines = (1 if stereo else 0) + 1
        h = 6 + lines * (size + 3) + (len(attrs) * (size + 2) + 5) + (len(ops) * (size + 2) + 5 if ops else 0)
        if not attrs and not ops:
            h = 6 + lines * (size + 3) + 6
        n = Node(name, "class", x, y, w, h, attrs=list(attrs), ops=list(ops), stereo=stereo, abstract=abstract, size=size)
        self.nodes[name] = n
        self.ops.append(("node", n))
        return n

    def state(self, name, x, y, w, h, lines=(), size=8, fill=STATE):
        n = Node(name, "state", x, y, w, h, lines=list(lines), size=size, fill=fill)
        self.nodes[name] = n
        self.ops.append(("node", n))
        return n

    def ellipse(self, name, x, y, w, h, text=None, size=7.5, fill=UC):
        n = Node(name, "ellipse", x, y, w, h, text=text if text is not None else name, size=size, fill=fill)
        self.nodes[name] = n
        self.ops.append(("node", n))
        return n

    def circle(self, name, x, y, d, text=None, size=7.5, fill=FILL):
        n = Node(name, "circle", x, y, d, d, text=text if text is not None else name, size=size, fill=fill)
        self.nodes[name] = n
        self.ops.append(("node", n))
        return n

    def diamond(self, name, x, y, w, h, text="", size=7.5, fill=FILL):
        n = Node(name, "diamond", x, y, w, h, text=text, size=size, fill=fill)
        self.nodes[name] = n
        self.ops.append(("node", n))
        return n

    def actor(self, name, x, y, size=8, side=None):
        n = Node(name, "actor", x, y, 26, 52, size=size, side=side)
        self.nodes[name] = n
        self.ops.append(("node", n))
        return n

    # ---- BPMN shapes
    def task(self, name, x, y, w, h, text, size=6.4, fill=colors.white):
        n = Node(name, "task", x, y, w, h, text=text, size=size, fill=fill)
        self.nodes[name] = n
        self.ops.append(("node", n))
        return n

    def bstart(self, name, x, y, d=14):
        n = Node(name, "bstart", x, y, d, d)
        self.nodes[name] = n
        self.ops.append(("node", n))
        return n

    def bend(self, name, x, y, d=14):
        n = Node(name, "bend", x, y, d, d)
        self.nodes[name] = n
        self.ops.append(("node", n))
        return n

    def xor(self, name, x, y, d=26):
        return self.diamond(name, x, y, d, d, text="×", size=9, fill=colors.white)

    def start(self, name, x, y):
        n = Node(name, "start", x, y, 10, 10)
        self.nodes[name] = n
        self.ops.append(("node", n))
        return n

    def end(self, name, x, y):
        n = Node(name, "end", x, y, 14, 14)
        self.nodes[name] = n
        self.ops.append(("node", n))
        return n

    def frame(self, x, y, w, h, label=None, dashed=False):
        self.ops.append(("frame", x, y, w, h, label, dashed))

    def text(self, x, y, s, size=7.5, font=FONT, color=INK, align="left"):
        self.ops.append(("text", x, y, s, size, font, color, align))

    def edge(self, a, b, kind="assoc", label=None, via=(), ma=None, mb=None, lpos=None, arrow=False, dashed=None):
        self.ops.append(("edge", a, b, kind, label, list(via), ma, mb, lpos, arrow, dashed))

    def raw(self, fn):
        self.ops.append(("raw", fn))

    # ------------------------------------------------------------------ flowable
    def wrap(self, aw, ah):
        self.scale = min(1.0, aw / self.W)
        self._aw = aw
        extra = 12 if self.caption else 0
        return aw, self.H * self.scale + extra

    def draw(self):
        c = self.canv
        c.saveState()
        extra = 12 if self.caption else 0
        c.translate(max(0, (self._aw - self.W * self.scale) / 2), extra)
        c.scale(self.scale, self.scale)
        c.setStrokeColor(INK)
        c.setFillColor(INK)
        c.setLineWidth(0.8)
        for op in self.ops:
            getattr(self, "_d_" + op[0])(c, *op[1:])
        c.restoreState()
        if self.caption:
            c.setFont(ITAL, 7.5)
            c.setFillColor(GREY)
            c.drawCentredString(self._aw / 2, 1, self.caption)

    # ------------------------------------------------------------------ painters
    def _d_text(self, c, x, y, s, size, font, color, align):
        c.setFont(font, size)
        c.setFillColor(color)
        for i, ln in enumerate(s.split("\n")):
            yy = y - i * (size + 1.5)
            if align == "center":
                c.drawCentredString(x, yy, ln)
            elif align == "right":
                c.drawRightString(x, yy, ln)
            else:
                c.drawString(x, yy, ln)
        c.setFillColor(INK)

    def _d_raw(self, c, fn):
        fn(c)

    def _d_frame(self, c, x, y, w, h, label, dashed):
        c.saveState()
        c.setStrokeColor(GREY)
        if dashed:
            c.setDash(3, 2)
        c.rect(x, y, w, h)
        c.restoreState()
        if label:
            c.setFont(BOLD, 7)
            c.setFillColor(INK)
            tw = sw(label, 7, BOLD) + 8
            c.setFillColor(colors.white)
            c.rect(x, y + h - 11, tw, 11, stroke=1, fill=1)
            c.setFillColor(INK)
            c.drawString(x + 4, y + h - 8.5, label)

    def _d_node(self, c, n):
        k = n.kind
        if k == "class":
            self._cls(c, n)
        elif k == "state":
            c.setFillColor(n.kw["fill"])
            c.roundRect(n.x, n.y, n.w, n.h, 8, stroke=1, fill=1)
            c.setFillColor(INK)
            ls = [n.name] + n.kw["lines"]
            size = n.kw["size"]
            if n.kw["lines"]:
                top = n.y + n.h - size - 3
                c.setFont(BOLD, size)
                c.drawCentredString(n.x + n.w / 2, top, n.name)
                c.line(n.x, top - 3, n.x + n.w, top - 3)
                c.setFont(FONT, size - 1)
                for i, ln in enumerate(n.kw["lines"]):
                    c.drawString(n.x + 5, top - 12 - i * (size + 0.5), ln)
            else:
                c.setFont(BOLD, size)
                c.drawCentredString(n.x + n.w / 2, n.y + n.h / 2 - size / 3, n.name)
        elif k in ("ellipse", "circle", "diamond"):
            c.setFillColor(n.kw["fill"])
            if k == "diamond":
                p = c.beginPath()
                p.moveTo(n.x, n.y + n.h / 2)
                p.lineTo(n.x + n.w / 2, n.y + n.h)
                p.lineTo(n.x + n.w, n.y + n.h / 2)
                p.lineTo(n.x + n.w / 2, n.y)
                p.close()
                c.drawPath(p, stroke=1, fill=1)
            else:
                c.ellipse(n.x, n.y, n.x + n.w, n.y + n.h, stroke=1, fill=1)
            c.setFillColor(INK)
            size = n.kw["size"]
            c.setFont(FONT, size)
            lines = str(n.kw["text"]).split("\n")
            for i, ln in enumerate(lines):
                yy = n.y + n.h / 2 + (len(lines) - 1) * (size + 1) / 2 - i * (size + 1) - size / 3
                c.drawCentredString(n.x + n.w / 2, yy, ln)
        elif k == "actor":
            cx = n.x + n.w / 2
            top = n.y + n.h
            c.circle(cx, top - 6, 5, stroke=1, fill=0)
            c.line(cx, top - 11, cx, top - 30)
            c.line(cx - 10, top - 18, cx + 10, top - 18)
            c.line(cx, top - 30, cx - 8, top - 42)
            c.line(cx, top - 30, cx + 8, top - 42)
            c.setFont(BOLD, n.kw["size"])
            if n.kw.get("side") == "right":
                c.drawString(cx + 15, n.y + 2, n.name)
            elif n.kw.get("side") == "top":
                c.drawCentredString(cx, n.y + n.h + 3, n.name)
            else:
                c.drawCentredString(cx, n.y - 8 + 0, n.name)
        elif k == "task":
            c.setFillColor(n.kw["fill"])
            c.roundRect(n.x, n.y, n.w, n.h, 5, stroke=1, fill=1)
            c.setFillColor(INK)
            size = n.kw["size"]
            c.setFont(FONT, size)
            lines = str(n.kw["text"]).split(chr(10))
            for i, ln in enumerate(lines):
                yy = n.y + n.h / 2 + (len(lines) - 1) * (size + 1) / 2 - i * (size + 1) - size / 3
                c.drawCentredString(n.x + n.w / 2, yy, ln)
        elif k == "bstart":
            c.setFillColor(colors.white)
            c.circle(n.x + n.w / 2, n.y + n.h / 2, n.w / 2, stroke=1, fill=1)
            c.setFillColor(INK)
        elif k == "bend":
            c.setFillColor(colors.white)
            c.saveState()
            c.setLineWidth(2.4)
            c.circle(n.x + n.w / 2, n.y + n.h / 2, n.w / 2, stroke=1, fill=1)
            c.restoreState()
            c.setFillColor(INK)
        elif k == "start":
            c.setFillColor(INK)
            c.circle(n.x + 5, n.y + 5, 5, stroke=0, fill=1)
        elif k == "end":
            c.setFillColor(colors.white)
            c.circle(n.x + 7, n.y + 7, 7, stroke=1, fill=1)
            c.setFillColor(INK)
            c.circle(n.x + 7, n.y + 7, 4, stroke=0, fill=1)

    def _cls(self, c, n):
        size = n.kw["size"]
        c.setFillColor(CLS)
        c.rect(n.x, n.y, n.w, n.h, stroke=1, fill=1)
        c.setFillColor(INK)
        top = n.y + n.h
        y = top - 4
        if n.kw["stereo"]:
            c.setFont(FONT, size - 0.5)
            c.drawCentredString(n.x + n.w / 2, y - size + 1, "«%s»" % n.kw["stereo"])
            y -= size + 2
        c.setFont(ITAL if n.kw["abstract"] else BOLD, size)
        c.drawCentredString(n.x + n.w / 2, y - size + 1, n.name)
        y -= size + 3
        if n.kw["attrs"] or n.kw["ops"]:
            c.line(n.x, y, n.x + n.w, y)
            y -= 2
            c.setFont(FONT, size - 0.5)
            for a in n.kw["attrs"]:
                c.drawString(n.x + 4, y - size + 1, a)
                y -= size + 2
            y -= 3
            if n.kw["ops"]:
                c.line(n.x, y, n.x + n.w, y)
                y -= 2
                for o in n.kw["ops"]:
                    c.setFont(ITAL if o.startswith("*") else FONT, size - 0.5)
                    c.drawString(n.x + 4, y - size + 1, o.lstrip("*"))
                    y -= size + 2

    def _pt(self, p, toward):
        if isinstance(p, tuple):
            return p
        return self.nodes[p].anchor(*toward)

    def _d_edge(self, c, a, b, kind, label, via, ma, mb, lpos, arrow, dashed):
        na = a if isinstance(a, tuple) else self.nodes[a].c
        nb = b if isinstance(b, tuple) else self.nodes[b].c
        first_t = via[0] if via else nb
        last_t = via[-1] if via else na
        p0 = self._pt(a, first_t)
        p1 = self._pt(b, last_t)
        pts = [p0] + list(via) + [p1]
        dash = dashed if dashed is not None else kind in ("realize", "depend", "dashed", "note")
        c.saveState()
        c.setStrokeColor(GREY if kind == "note" else INK)
        if dash:
            c.setDash(3, 2)
        # shorten the line where a head is drawn so the line does not poke through the head
        end_head = kind in ("inherit", "realize", "depend", "arrow", "open", "dashed") or arrow
        start_head = kind in ("comp", "aggr")
        q = list(pts)
        hl = 9
        if end_head and kind in ("inherit", "realize"):
            q[-1] = self._back(q[-2], q[-1], hl)
        if start_head:
            q[0] = self._back(q[1], q[0], 11)
        p = c.beginPath()
        p.moveTo(*q[0])
        for t in q[1:]:
            p.lineTo(*t)
        c.drawPath(p, stroke=1, fill=0)
        c.restoreState()
        c.setLineWidth(0.8)
        if end_head:
            if kind in ("inherit", "realize"):
                self._tri(c, pts[-2], pts[-1])
            elif kind in ("arrow",):
                self._head(c, pts[-2], pts[-1], True)
            else:
                self._head(c, pts[-2], pts[-1], False)
        if start_head:
            self._diamond(c, pts[1], pts[0], kind == "comp")
        if label:
            if lpos:
                lx, ly = lpos
            else:
                mid = self._mid(pts)
                lx, ly = mid[0], mid[1] + 3
            c.setFont(FONT, 6.8)
            c.setFillColor(INK)
            for i, ln in enumerate(label.split(chr(10))):
                c.drawCentredString(lx, ly - i * 8, ln)
        if ma:
            self._mult(c, pts[0], pts[1], ma)
        if mb:
            self._mult(c, pts[-1], pts[-2], mb)

    def _back(self, frm, to, d):
        dx, dy = to[0] - frm[0], to[1] - frm[1]
        L = math.hypot(dx, dy) or 1
        return (to[0] - dx / L * d, to[1] - dy / L * d)

    def _mid(self, pts):
        segs = [(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]), i) for i in range(len(pts) - 1)]
        total = sum(s for s, _ in segs)
        half, acc = total / 2, 0
        for s, i in segs:
            if acc + s >= half:
                f = (half - acc) / (s or 1)
                return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)
            acc += s
        return pts[0]

    def _mult(self, c, end, other, text):
        dx, dy = other[0] - end[0], other[1] - end[1]
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        px, py = end[0] + ux * 9 - uy * 7, end[1] + uy * 9 + ux * 7
        c.setFont(FONT, 6.8)
        c.setFillColor(INK)
        c.drawCentredString(px, py - 2, text)

    def _head(self, c, frm, to, filled):
        dx, dy = to[0] - frm[0], to[1] - frm[1]
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        s = 6.5
        bx, by = to[0] - ux * s, to[1] - uy * s
        l = (bx - uy * 3.2, by + ux * 3.2)
        r = (bx + uy * 3.2, by - ux * 3.2)
        c.saveState()
        c.setDash()
        p = c.beginPath()
        p.moveTo(*l)
        p.lineTo(*to)
        p.lineTo(*r)
        if filled:
            p.close()
            c.setFillColor(INK)
            c.drawPath(p, stroke=1, fill=1)
        else:
            c.drawPath(p, stroke=1, fill=0)
        c.restoreState()

    def _tri(self, c, frm, to):
        dx, dy = to[0] - frm[0], to[1] - frm[1]
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        s = 9
        bx, by = to[0] - ux * s, to[1] - uy * s
        l = (bx - uy * 4.5, by + ux * 4.5)
        r = (bx + uy * 4.5, by - ux * 4.5)
        c.saveState()
        c.setDash()
        c.setFillColor(colors.white)
        p = c.beginPath()
        p.moveTo(*l)
        p.lineTo(*to)
        p.lineTo(*r)
        p.close()
        c.drawPath(p, stroke=1, fill=1)
        c.restoreState()

    def _diamond(self, c, nxt, at, filled):
        dx, dy = nxt[0] - at[0], nxt[1] - at[1]
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        s = 11
        mid = (at[0] + ux * s / 2, at[1] + uy * s / 2)
        far = (at[0] + ux * s, at[1] + uy * s)
        l = (mid[0] - uy * 3.6, mid[1] + ux * 3.6)
        r = (mid[0] + uy * 3.6, mid[1] - ux * 3.6)
        c.saveState()
        c.setDash()
        c.setFillColor(INK if filled else colors.white)
        p = c.beginPath()
        p.moveTo(*at)
        p.lineTo(*l)
        p.lineTo(*far)
        p.lineTo(*r)
        p.close()
        c.drawPath(p, stroke=1, fill=1)
        c.restoreState()


# ---------------------------------------------------------------------- sequence diagrams
def sequence(width, height, parts, msgs, frames=(), caption=None, acts=()):
    """parts: [(name, x, is_actor)], msgs: [(y, from_name, to_name, label, kind)] kind: call | ret | self | create
    frames: [(y_top, y_bottom, label, x0, x1, divider_y_or_None)], acts: [(part, y0, y1)] activation bars."""
    f = Fig(width, height, caption)
    xs = {p[0]: p[1] for p in parts}
    top = height - 4

    def paint(c):
        for name, x, actor in parts:
            bw = max(58, sw(name, 7.5, BOLD) + 12)
            if actor:
                c.setFillColor(colors.white)
                c.setFont(BOLD, 7.5)
                c.rect(x - bw / 2, top - 20, bw, 20, stroke=1, fill=0)
                c.setFillColor(INK)
                c.drawCentredString(x, top - 13, name)
            else:
                c.setFillColor(CLS)
                c.rect(x - bw / 2, top - 20, bw, 20, stroke=1, fill=1)
                c.setFillColor(INK)
                c.setFont(BOLD, 7.5)
                c.drawCentredString(x, top - 13, name)
            c.saveState()
            c.setDash(3, 3)
            c.setStrokeColor(GREY)
            c.line(x, top - 20, x, 6)
            c.restoreState()
        for p, y0, y1 in acts:
            c.setFillColor(colors.white)
            c.rect(xs[p] - 3, y1, 6, y0 - y1, stroke=1, fill=1)
        for (yt, yb, label, x0, x1, div) in frames:
            c.saveState()
            c.setStrokeColor(INK)
            c.rect(x0, yb, x1 - x0, yt - yb, stroke=1, fill=0)
            tw = sw(label, 7, BOLD) + 8
            c.setFillColor(colors.white)
            c.rect(x0, yt - 11, tw, 11, stroke=1, fill=1)
            c.setFillColor(INK)
            c.setFont(BOLD, 7)
            c.drawString(x0 + 4, yt - 8.5, label)
            if div is not None:
                c.setDash(4, 3)
                c.line(x0, div, x1, div)
            c.restoreState()
        for (y, a, b, label, kind) in msgs:
            xa, xb = xs[a], xs[b]
            c.saveState()
            c.setFillColor(INK)
            if kind == "self":
                c.line(xa + 3, y, xa + 26, y)
                c.line(xa + 26, y, xa + 26, y - 10)
                c.line(xa + 26, y - 10, xa + 3, y - 10)
                f._head(c, (xa + 14, y - 10), (xa + 3, y - 10), False)
                c.setFont(FONT, 6.8)
                c.drawString(xa + 30, y - 6, label)
            else:
                d = 1 if xb > xa else -1
                sa, sb = xa + 3 * d, xb - 3 * d
                if kind == "ret":
                    c.setDash(3, 2)
                c.line(sa, y, sb, y)
                c.setDash()
                f._head(c, (sa, y), (sb, y), kind == "call-sync")
                c.setFont(ITAL if kind == "ret" else FONT, 6.8)
                c.drawCentredString((sa + sb) / 2, y + 2.5, label)
            c.restoreState()

    f.raw(paint)
    return f
