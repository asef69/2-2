"""Turing-machine toolkit + every TM of the TM notes, each verified by simulation.
Blank = '_' internally (printed ⊔). Rule: (state, symbols) -> (state', write or '=', D) ; '=' = write the symbol read."""
import os, sys, itertools, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

BL = "_"


class TM:
    def __init__(self, name, start, accept, rules, sigma):
        self.name, self.start, self.accept, self.sigma = name, start, set(accept), sigma
        self.rules = rules  # list of (q, symbols-string, r, write, D)
        self.d = {}
        for q, syms, r, w, D in rules:
            for a in syms:
                assert (q, a) not in self.d, f"{name}: duplicate rule {(q, a)}"
                self.d[(q, a)] = (r, a if w == "=" else w, D)

    def run(self, w, maxsteps=20000):
        tape = dict(enumerate(w))
        q, h, steps = self.start, 0, 0
        while steps < maxsteps:
            a = tape.get(h, BL)
            if (q, a) not in self.d:
                break
            r, b, D = self.d[(q, a)]
            tape[h] = b
            h += 1 if D == "R" else -1
            q = r
            steps += 1
        if steps >= maxsteps:
            return None, None, steps
        if not tape:
            return q, "", steps
        lo, hi = min(tape), max(tape)
        s = "".join(tape.get(i, BL) for i in range(lo, hi + 1)).strip(BL)
        return q, s, steps

    def decides(self, w):
        q, s, st = self.run(w)
        return q in self.accept

    def trace(self, w, limit=60):
        """configurations X1..q..Xn in the slides' ID notation"""
        tape = dict(enumerate(w))
        q, h = self.start, 0
        out = []
        for _ in range(limit):
            lo = min(min(tape, default=0), h); hi = max(max(tape, default=0), h)
            cells = [tape.get(i, BL) for i in range(lo, hi + 1)]
            k = h - lo
            ids = "".join(cells[:k]) + f"[{q}]" + "".join(cells[k:])
            out.append(ids.replace(BL, "⊔").strip("⊔") if False else ids.replace(BL, "⊔"))
            a = tape.get(h, BL)
            if (q, a) not in self.d:
                break
            r, b, D = self.d[(q, a)]
            tape[h] = b
            h += 1 if D == "R" else -1
            q = r
        return out

    def lines(self):
        out = []
        for q, syms, r, w, D in self.rules:
            s = ",".join(syms).replace(BL, "⊔")
            wr = "same" if w == "=" else w.replace(BL, "⊔")
            out.append(f"δ({q}, {s}) = ({r}, {wr}, {D})")
        return out


def pairs(q, syms, r, w, D):
    return (q, syms, r, w, D)


M = {}
CHK = {}

# ---- 0^n 1^n, n ≥ 1 (Lec4 sl. 42–65)
M["0n1n"] = TM("0n1n", "q0", ["q4"], [
    ("q0", "0", "q1", "X", "R"), ("q0", "Y", "q3", "Y", "R"),
    ("q1", "0Y", "q1", "=", "R"), ("q1", "1", "q2", "Y", "L"),
    ("q2", "0Y", "q2", "=", "L"), ("q2", "X", "q0", "X", "R"),
    ("q3", "Y", "q3", "Y", "R"), ("q3", BL, "q4", BL, "R")], "01")
CHK["0n1n"] = (lambda w: re.fullmatch(r"0+1+", w) is not None and w.count("0") == w.count("1"), "01", 9)

# ---- a^n b^n c^n, n ≥ 1
M["anbncn"] = TM("anbncn", "q0", ["q6"], [
    ("q0", "a", "q1", "X", "R"), ("q0", "Y", "q4", "Y", "R"),
    ("q1", "aY", "q1", "=", "R"), ("q1", "b", "q2", "Y", "R"),
    ("q2", "bZ", "q2", "=", "R"), ("q2", "c", "q3", "Z", "L"),
    ("q3", "abYZ", "q3", "=", "L"), ("q3", "X", "q0", "X", "R"),
    ("q4", "Y", "q4", "Y", "R"), ("q4", "Z", "q5", "Z", "R"),
    ("q5", "Z", "q5", "Z", "R"), ("q5", BL, "q6", BL, "R")], "abc")
CHK["anbncn"] = (lambda w: re.fullmatch(r"a+b+c+", w) is not None and w.count("a") == w.count("b") == w.count("c"), "abc", 7)

# ---- 0^N 1^N 0^N, N ≥ 0 (2013-14 2(a))
M["0n1n0n"] = TM("0n1n0n", "q0", ["q6"], [
    ("q0", BL, "q6", BL, "R"), ("q0", "0", "q1", "X", "R"), ("q0", "Y", "q4", "Y", "R"),
    ("q1", "0Y", "q1", "=", "R"), ("q1", "1", "q2", "Y", "R"),
    ("q2", "1Z", "q2", "=", "R"), ("q2", "0", "q3", "Z", "L"),
    ("q3", "01YZ", "q3", "=", "L"), ("q3", "X", "q0", "X", "R"),
    ("q4", "Y", "q4", "Y", "R"), ("q4", "Z", "q5", "Z", "R"),
    ("q5", "Z", "q5", "Z", "R"), ("q5", BL, "q6", BL, "R")], "01")
CHK["0n1n0n"] = (lambda w: re.fullmatch(r"(0*)(1*)(0*)", w) is not None and (lambda m: len(m.group(1)) == len(m.group(2)) == len(m.group(3)))(re.fullmatch(r"(0*)(1*)(0*)", w)), "01", 9)

# ---- a^n c^n b^n d^n, n ≥ 0 (2009-10 12(b)); marks A, C, B', D
M["ancnbndn"] = TM("ancnbndn", "q0", ["q8"], [
    ("q0", BL, "q8", BL, "R"), ("q0", "a", "q1", "A", "R"), ("q0", "C", "q5", "C", "R"),
    ("q1", "aC", "q1", "=", "R"), ("q1", "c", "q2", "C", "R"),
    ("q2", "cB", "q2", "=", "R"), ("q2", "b", "q3", "B", "R"),
    ("q3", "bD", "q3", "=", "R"), ("q3", "d", "q4", "D", "L"),
    ("q4", "DbBcCa", "q4", "=", "L"), ("q4", "A", "q0", "A", "R"),
    ("q5", "C", "q5", "C", "R"), ("q5", "B", "q6", "B", "R"),
    ("q6", "B", "q6", "B", "R"), ("q6", "D", "q7", "D", "R"),
    ("q7", "D", "q7", "D", "R"), ("q7", BL, "q8", BL, "R")], "abcd")
CHK["ancnbndn"] = (lambda w: re.fullmatch(r"(a*)(c*)(b*)(d*)", w) is not None and (lambda m: len(m.group(1)) == len(m.group(2)) == len(m.group(3)) == len(m.group(4)))(re.fullmatch(r"(a*)(c*)(b*)(d*)", w)), "abcd", 8)

# ---- equal numbers of 0s and 1s (2016-17 6(c))
M["eq01"] = TM("eq01", "q0", ["q4"], [
    ("q0", "XY", "q0", "=", "R"), ("q0", "0", "q1", "X", "R"), ("q0", "1", "q2", "X", "R"), ("q0", BL, "q4", BL, "R"),
    ("q1", "0Y", "q1", "=", "R"), ("q1", "1", "q3", "Y", "L"),
    ("q2", "1Y", "q2", "=", "R"), ("q2", "0", "q3", "Y", "L"),
    ("q3", "01XY", "q3", "=", "L"), ("q3", BL, "q0", BL, "R")], "01")
CHK["eq01"] = (lambda w: w.count("0") == w.count("1"), "01", 9)

# ---- {w−w | w ∈ {a,b}*} (2014-15 8(b)); '-' separator
M["w-w"] = TM("w-w", "q0", ["qa"], [
    ("q0", "XY", "q0", "=", "R"), ("q0", "a", "sa", "X", "R"), ("q0", "b", "sb", "Y", "R"), ("q0", "-", "chk", "-", "R"),
    ("sa", "ab", "sa", "=", "R"), ("sa", "-", "ta", "-", "R"), ("sb", "ab", "sb", "=", "R"), ("sb", "-", "tb", "-", "R"),
    ("ta", "XY", "ta", "=", "R"), ("ta", "a", "back", "X", "L"), ("tb", "XY", "tb", "=", "R"), ("tb", "b", "back", "Y", "L"),
    ("back", "abXY-", "back", "=", "L"), ("back", BL, "q0", BL, "R"),
    ("chk", "XY", "chk", "=", "R"), ("chk", BL, "qa", BL, "R")], "ab-")
CHK["w-w"] = (lambda w: w.count("-") == 1 and w.split("-")[0] == w.split("-")[1], "ab-", 9)

# ---- {w−w−w} (2012-13 3(b))
M["w-w-w"] = TM("w-w-w", "q0", ["qa"], [
    ("q0", "XY", "q0", "=", "R"), ("q0", "a", "sa", "X", "R"), ("q0", "b", "sb", "Y", "R"), ("q0", "-", "chk1", "-", "R"),
    ("sa", "ab", "sa", "=", "R"), ("sa", "-", "ta", "-", "R"), ("sb", "ab", "sb", "=", "R"), ("sb", "-", "tb", "-", "R"),
    ("ta", "XY", "ta", "=", "R"), ("ta", "a", "ua", "X", "R"), ("tb", "XY", "tb", "=", "R"), ("tb", "b", "ub", "Y", "R"),
    ("ua", "ab", "ua", "=", "R"), ("ua", "-", "va", "-", "R"), ("ub", "ab", "ub", "=", "R"), ("ub", "-", "vb", "-", "R"),
    ("va", "XY", "va", "=", "R"), ("va", "a", "back", "X", "L"), ("vb", "XY", "vb", "=", "R"), ("vb", "b", "back", "Y", "L"),
    ("back", "abXY-", "back", "=", "L"), ("back", BL, "q0", BL, "R"),
    ("chk1", "XY", "chk1", "=", "R"), ("chk1", "-", "chk2", "-", "R"), ("chk2", "XY", "chk2", "=", "R"), ("chk2", BL, "qa", BL, "R")], "ab-")
CHK["w-w-w"] = (lambda w: w.count("-") == 2 and len(set(w.split("-"))) == 1, "ab-", 9)

# ---- monus m ∸ n on 0^m 1 0^n → 0^max(m-n,0) (Lec4 sl. 71–115, own rule set)
M["monus"] = TM("monus", "q0", ["q6"], [
    ("q0", "0", "q1", BL, "R"), ("q0", "1", "q5", BL, "R"),
    ("q1", "0", "q1", "0", "R"), ("q1", "1", "q2", "1", "R"),
    ("q2", "1", "q2", "1", "R"), ("q2", "0", "q3", "1", "L"), ("q2", BL, "q4", BL, "L"),
    ("q3", "01", "q3", "=", "L"), ("q3", BL, "q0", BL, "R"),
    ("q4", "1", "q4", BL, "L"), ("q4", "0", "q4b", "0", "L"), ("q4", BL, "q6", "0", "R"),
    ("q4b", "0", "q4b", "0", "L"), ("q4b", BL, "q6", "0", "R"),
    ("q5", "01", "q5", BL, "R"), ("q5", BL, "q6", BL, "R")], "01")

# ---- unary: 1^a 0 1^b → 1^max(b-a,0)  (2015-16 8(a))
M["monus1"] = TM("monus1", "q0", ["qh"], [
    ("q0", "X", "q0", "X", "R"), ("q0", "1", "q1", "X", "R"), ("q0", "0", "q9", "0", "L"),
    ("q1", "1", "q1", "1", "R"), ("q1", "0", "q2", "0", "R"),
    ("q2", "X", "q2", "X", "R"), ("q2", "1", "q3", "X", "L"), ("q2", BL, "q7", BL, "L"),
    ("q3", "X01", "q3", "=", "L"), ("q3", BL, "q0", BL, "R"),
    ("q9", "X", "q9", BL, "L"), ("q9", BL, "q10", BL, "R"),
    ("q10", BL, "q10", BL, "R"), ("q10", "0", "q11", BL, "R"),
    ("q11", "X", "q11", BL, "R"), ("q11", "1", "q6", "1", "R"), ("q11", BL, "qh", BL, "R"),
    ("q6", "1", "q6", "1", "R"), ("q6", BL, "qh", BL, "R"),
    ("q7", "X01", "q7", BL, "L"), ("q7", BL, "qh", BL, "R")], "01")

# ---- unary subtraction 1^(x+1) 0 1^(y+1) → 1^(x-y+1)  (2011-12 1(a))
M["unsub"] = TM("unsub", "q0", ["qh"], [
    ("q0", "X", "q0", "X", "R"), ("q0", "1", "q1", "X", "R"), ("q0", "0", "q8", "0", "R"),
    ("q1", "1", "q1", "1", "R"), ("q1", "0", "q2", "0", "R"),
    ("q2", "X", "q2", "X", "R"), ("q2", "1", "q3", "X", "L"), ("q2", BL, "q4", BL, "L"),
    ("q3", "X01", "q3", "=", "L"), ("q3", BL, "q0", BL, "R"),
    ("q8", "X", "q8", "X", "R"), ("q8", BL, "q9", BL, "L"),
    ("q9", "X", "q9", BL, "L"), ("q9", "0", "q9b", BL, "L"), ("q9b", "X", "q6", "1", "L"),
    ("q4", "X", "q4", BL, "L"), ("q4", "0", "q4b", BL, "L"),
    ("q4b", "1", "q5", "1", "L"), ("q4b", "X", "q6a", "1", "L"),
    ("q5", "1", "q5", "1", "L"), ("q5", "X", "q6a", "1", "L"),
    ("q6a", "X", "q6", "1", "L"),
    ("q6", "X", "q6", BL, "L"), ("q6", BL, "qh", BL, "R")], "01")

# ---- binary increment #N → #N+1 (2016-17 5(b)); # may become 1
M["inc"] = TM("inc", "q0", ["qh"], [
    ("q0", "#", "q1", "#", "R"), ("q1", "01", "q1", "=", "R"), ("q1", BL, "q2", BL, "L"),
    ("q2", "1", "q2", "0", "L"), ("q2", "0", "qh", "1", "R"), ("q2", "#", "qh", "1", "R")], "01#")

# ---- parity: #w → #0^n (n even) or #1^n (n odd), w ∈ {0,1}*   (2011-12 3(a), 2012-13 3(c))
M["parity"] = TM("parity", "q0", ["qh"], [
    ("q0", "#", "pe", "#", "R"),
    ("pe", "01", "po", "=", "R"), ("po", "01", "pe", "=", "R"),
    ("pe", BL, "we", BL, "L"), ("po", BL, "wo", BL, "L"),
    ("we", "01", "we", "0", "L"), ("we", "#", "qh", "#", "R"),
    ("wo", "01", "wo", "1", "L"), ("wo", "#", "qh", "#", "R")], "01#")

# ---- bitwise ops on w1 S w2 S → result after second S  (S = 'c' or '#')
def bitwise(name, op, S):
    f = {"xor": lambda a, b: str(int(a) ^ int(b)), "and": lambda a, b: str(int(a) & int(b)), "or": lambda a, b: str(int(a) | int(b))}[op]
    R = [("q0", "xy", "q0", "=", "R"), ("q0", "0", "s0", "x", "R"), ("q0", "1", "s1", "y", "R"),
         ("q0", S, "qh", S, "R")]
    for a in "01":
        R += [(f"s{a}", "01xy", f"s{a}", "=", "R"), (f"s{a}", S, f"t{a}", S, "R")]
        R += [(f"t{a}", "xy", f"t{a}", "=", "R")]
        for b in "01":
            R += [(f"t{a}", b, f"u{a}{b}", "y" if b == "1" else "x", "R")]
            R += [(f"u{a}{b}", "01xy" + S, f"u{a}{b}", "=", "R"), (f"u{a}{b}", BL, "v", f(a, b), "L")]
    R += [("v", "01xy" + S, "v", "=", "L"), ("v", BL, "q0", BL, "R")]
    return TM(name, "q0", ["qh"], R, "01" + S)


for op, S in (("xor", "c"), ("and", "c"), ("or", "#")):
    M[f"{op}_{S}"] = bitwise(f"{op}_{S}", op, S)


def bw_check(op, S):
    f = {"xor": lambda a, b: a ^ b, "and": lambda a, b: a & b, "or": lambda a, b: a | b}[op]
    ok = True
    for n in range(0, 5):
        for a in itertools.product("01", repeat=n):
            for b in itertools.product("01", repeat=n):
                w = "".join(a) + S + "".join(b) + S
                q, s, _ = M[f"{op}_{S}"].run(w)
                exp = ("".join(str(f(int(x), int(y))) for x, y in zip(a, b)))
                ok &= (q == "qh" and s.replace("x", "0").replace("y", "1") == ("".join(a) + S + "".join(b) + S + exp).strip(BL).replace("x", "0").replace("y", "1"))
    return ok


# ---- binary addition w1 c w2 c (LSB first, equal length) → sum after the second c (Lec5 sl. 84–131; 2007-08 Q8)
def addtm():
    S = "c"
    R = []
    for cr in "01":
        R += [(f"p{cr}", "xy", f"p{cr}", "=", "R"), (f"p{cr}", S, f"w{cr}", S, "R"), (f"w{cr}", "01xyc", f"w{cr}", "=", "R"), (f"w{cr}", BL, "qh", cr, "R")]
        for a in "01":
            R += [(f"p{cr}", a, f"s{cr}{a}", "x" if a == "0" else "y", "R")]
            R += [(f"s{cr}{a}", "01xy", f"s{cr}{a}", "=", "R"), (f"s{cr}{a}", S, f"t{cr}{a}", S, "R"), (f"t{cr}{a}", "xy", f"t{cr}{a}", "=", "R")]
            for b in "01":
                tot = int(cr) + int(a) + int(b)
                R += [(f"t{cr}{a}", b, f"u{cr}{a}{b}", "x" if b == "0" else "y", "R")]
                R += [(f"u{cr}{a}{b}", "01xy" + S, f"u{cr}{a}{b}", "=", "R"), (f"u{cr}{a}{b}", BL, f"v{tot // 2}", str(tot % 2), "L")]
    for cr in "01":
        R += [(f"v{cr}", "01xy" + S, f"v{cr}", "=", "L"), (f"v{cr}", BL, f"p{cr}", BL, "R")]
    return TM("add", "p0", ["qh"], R, "01c")


M["add"] = addtm()

# ---- slides' storage-in-state example: 01* + 10*   (Lec5 sl. 7–26)
R = [("q0B", "0", "q1_0", "0", "R"), ("q0B", "1", "q1_1", "1", "R"),
     ("q1_0", "1", "q1_0", "1", "R"), ("q1_1", "0", "q1_1", "0", "R"),
     ("q1_0", BL, "q1B", BL, "R"), ("q1_1", BL, "q1B", BL, "R")]
M["store"] = TM("store", "q0B", ["q1B"], R, "01")

# ---- slides' two-track example: {wcw | w ∈ (0+1)+}  (Lec5 sl. 27–83); checked 0/1 are x/y
R = []
for a in "01":
    ck = "x" if a == "0" else "y"
    R += [("q1", a, f"q2{a}", ck, "R"), (f"q2{a}", "01", f"q2{a}", "=", "R"), (f"q2{a}", "c", f"q3{a}", "c", "R"),
          (f"q3{a}", "xy", f"q3{a}", "=", "R"), (f"q3{a}", a, "q4", ck, "L")]
R += [("q4", "xy", "q4", "=", "L"), ("q4", "c", "q5", "c", "L"), ("q5", "01", "q6", "=", "L"), ("q5", "xy", "q7", "=", "R"),
      ("q6", "01", "q6", "=", "L"), ("q6", "xy", "q1", "=", "R"), ("q7", "c", "q8", "c", "R"), ("q8", "xy", "q8", "=", "R"), ("q8", BL, "q9", BL, "R")]
M["wcw"] = TM("wcw", "q1", ["q9"], R, "01c")
CHK["store"] = (lambda w: re.fullmatch(r"01*|10*", w) is not None, "01", 9)
CHK["wcw"] = (lambda w: (lambda m: m is not None and m.group(1) == m.group(2))(re.fullmatch(r"([01]+)c([01]+)", w)), "01c", 7)

# ---- XOR replacing w2, then erase w1 and ','  : 0010#1011 → 1001  (2006-07 Q11, 2008-09 Q3(b)-(c))
def xor_inplace():
    S = "#"
    R = [("q0", "xy", "q0", "=", "R"), ("q0", "0", "s0", "x", "R"), ("q0", "1", "s1", "y", "R"), ("q0", S, "c1", S, "R")]
    for a in "01":
        R += [(f"s{a}", "01xy", f"s{a}", "=", "R"), (f"s{a}", S, f"t{a}", S, "R"), (f"t{a}", "pq", f"t{a}", "=", "R")]
        for b in "01":
            r = str(int(a) ^ int(b))
            R += [(f"t{a}", b, "v", "p" if r == "0" else "q", "L")]
    R += [("v", "01xypq" + S, "v", "=", "L"), ("v", BL, "q0", BL, "R")]
    # cleanup: erase everything left of the result; convert p,q to 0,1
    R += [("c1", "pq", "c1", "=", "R"), ("c1", BL, "c2", BL, "L"),
          ("c2", "p", "c2", "0", "L"), ("c2", "q", "c2", "1", "L"), ("c2", S, "c3", BL, "L"),
          ("c3", "01xy", "c3", BL, "L"), ("c3", BL, "c4", BL, "R"), ("c4", BL, "c4", BL, "R"), ("c4", "01", "qh", "=", "R")]
    return TM("xor_inplace", "q0", ["qh"], R, "01#")


M["xor_inplace"] = xor_inplace()

# ---- signed magnitude → 2's complement (MSB 1 = negative) (2021-22 Q9)
M["twos"] = TM("twos", "q0", ["qh"], [
    ("q0", "0", "qh", "0", "R"), ("q0", "1", "q1", "S", "R"),
    ("q1", "0", "q1", "1", "R"), ("q1", "1", "q1", "0", "R"), ("q1", BL, "q2", BL, "L"),
    ("q2", "1", "q2", "0", "L"), ("q2", "0", "q3", "1", "L"), ("q2", "S", "qh", "1", "R"),
    ("q3", "01", "q3", "=", "L"), ("q3", "S", "qh", "1", "R")], "01")

# ---- NOT: w c → w c ¬w (2022-23 Q10)
M["notw"] = TM("notw", "q0", ["qh"], [
    ("q0", "xy", "q0", "=", "R"), ("q0", "0", "s0", "x", "R"), ("q0", "1", "s1", "y", "R"), ("q0", "c", "qr", "c", "L"),
    ("s0", "01xyc", "s0", "=", "R"), ("s0", BL, "v", "1", "L"), ("s1", "01xyc", "s1", "=", "R"), ("s1", BL, "v", "0", "L"),
    ("v", "01xyc", "v", "=", "L"), ("v", BL, "q0", BL, "R"),
    ("qr", "x", "qr", "0", "L"), ("qr", "y", "qr", "1", "L"), ("qr", BL, "qh", BL, "R")], "01c")

# ---- equality: w1 c w2 c → append 0 if w1 = w2 else 1 (2023-24 Q9)
def eqtm():
    R = [("q0", "xy", "q0", "=", "R"), ("q0", "0", "s0", "x", "R"), ("q0", "1", "s1", "y", "R"), ("q0", "c", "w0", "c", "R"),
         ("w0", "01xyc", "w0", "=", "R"), ("w0", BL, "qh", "0", "R")]
    for a in "01":
        R += [(f"s{a}", "01xy", f"s{a}", "=", "R"), (f"s{a}", "c", f"t{a}", "c", "R"), (f"t{a}", "xy", f"t{a}", "=", "R")]
        R += [(f"t{a}", a, "v", "x" if a == "0" else "y", "L"), (f"t{a}", "1" if a == "0" else "0", "m", "=", "R")]
    R += [("v", "01xyc", "v", "=", "L"), ("v", BL, "q0", BL, "R"), ("m", "01xyc", "m", "=", "R"), ("m", BL, "qh", "1", "R")]
    return TM("eq", "q0", ["qh"], R, "01c")


M["eq"] = eqtm()

# ---- two consecutive a's (2009-10 12(a)): scan right until aa then halt
M["aa"] = TM("aa", "q0", ["qa"], [("q0", "b", "q0", "b", "R"), ("q0", "a", "q1", "a", "R"), ("q1", "b", "q0", "b", "R"), ("q1", "a", "qa", "a", "R")], "ab")
CHK["aa"] = (lambda w: "aa" in w, "ab", 9)

# ---- a^(2^n) b? : TM deciding a^(2^n), n ≥ 0 (2010-11 11(b): the string aaaab has b at the end; we decide a^(2^n) b)
M["pow2"] = TM("pow2", "s0", ["qa"], [
    ("s0", "X", "s0", "X", "R"), ("s0", "a", "s1", "a", "R"),
    ("s1", "X", "s1", "X", "R"), ("s1", "a", "t0", "X", "R"), ("s1", "b", "qa", "b", "R"),
    ("t0", "X", "t0", "X", "R"), ("t0", "a", "t1", "a", "R"), ("t0", "b", "r", "b", "L"),
    ("t1", "X", "t1", "X", "R"), ("t1", "a", "t0", "X", "R"),
    ("r", "aX", "r", "=", "L"), ("r", BL, "s0", BL, "R")], "ab")


def pow2_ok():
    # decider for a^k b where k is a power of two (k ≥ 1)
    bad = []
    for k in range(0, 18):
        w = "a" * k + "b"
        exp = k > 0 and (k & (k - 1)) == 0
        q, s, _ = M["pow2"].run(w)
        if (q in M["pow2"].accept) != exp:
            bad.append(k)
    return bad


if __name__ == "__main__":
    ok = True
    for k, (pred, sig, n) in CHK.items():
        bad = [w for L in range(n + 1) for w in map("".join, itertools.product(sig, repeat=L))
               if M[k].decides(w) != bool(pred(w))]
        print(f"{k:10} {'OK' if not bad else 'FAIL ' + str(bad[:5])}")
        ok &= not bad
    b = pow2_ok(); print("pow2", "OK" if not b else f"FAIL {b}"); ok &= not b
    # monus
    bad = []
    for m in range(0, 8):
        for n_ in range(0, 8):
            q, s, _ = M["monus"].run("0" * m + "1" + "0" * n_)
            if s != "0" * max(m - n_, 0):
                bad.append((m, n_, s))
    print("monus", "OK" if not bad else bad[:5]); ok &= not bad
    bad = []
    for a in range(0, 8):
        for b_ in range(0, 8):
            q, s, _ = M["monus1"].run("1" * a + "0" + "1" * b_)
            if s != "1" * max(b_ - a, 0):
                bad.append((a, b_, s))
    print("monus1", "OK" if not bad else bad[:5]); ok &= not bad
    bad = []
    for x in range(0, 8):
        for y in range(0, x + 1):
            q, s, _ = M["unsub"].run("1" * (x + 1) + "0" + "1" * (y + 1))
            if s != "1" * (x - y + 1):
                bad.append((x, y, s))
    print("unsub", "OK" if not bad else bad[:5]); ok &= not bad
    bad = []
    for n_ in range(0, 7):
        for t in itertools.product("01", repeat=n_):
            N = "".join(t)
            q, s, _ = M["inc"].run("#" + N)
            v = (int(N, 2) + 1) if N else 1
            exp = bin(v)[2:].zfill(max(len(N), 0))
            got = s.lstrip("#")
            if (N and int(got, 2) != int(N, 2) + 1) or (not N and got not in ("1",)):
                bad.append((N, s))
    print("inc", "OK" if not bad else bad[:5]); ok &= not bad
    bad = []
    for n_ in range(0, 7):
        for t in itertools.product("01", repeat=n_):
            w = "".join(t)
            q, s, _ = M["parity"].run("#" + w)
            exp = "#" + ("0" if n_ % 2 == 0 else "1") * n_
            if s != exp:
                bad.append((w, s))
    print("parity", "OK" if not bad else bad[:5]); ok &= not bad
    for op, S in (("xor", "c"), ("and", "c"), ("or", "#")):
        r = bw_check(op, S); print(op, S, "OK" if r else "FAIL"); ok &= r
    bad = []
    for n_ in range(1, 5):
        for a in itertools.product("01", repeat=n_):
            for b_ in itertools.product("01", repeat=n_):
                q, s, _ = M["xor_inplace"].run("".join(a) + "#" + "".join(b_))
                exp = "".join(str(int(x) ^ int(y)) for x, y in zip(a, b_))
                if s != exp:
                    bad.append((a, b_, s))
    print("xor_inplace", "OK" if not bad else bad[:3]); ok &= not bad
    print(M["xor_inplace"].run("0010#1011"), M["xor_inplace"].run("1011#0010"))
    bad = []
    for n_ in range(1, 6):
        for t in itertools.product("01", repeat=n_):
            w = "".join(t)
            q, s, _ = M["twos"].run(w)
            if w[0] == "0":
                exp = w
            else:
                mag = int(w[1:], 2) if n_ > 1 else 0
                exp = "1" + (bin((1 << (n_ - 1)) - mag if mag else 0)[2:].zfill(n_ - 1) if n_ > 1 else "")
                if mag == 0: exp = "1" + "0" * (n_ - 1)
            if s.replace("S", "1") != exp:
                bad.append((w, s, exp))
    print("twos", "OK" if not bad else bad[:5]); ok &= not bad
    bad = []
    for n_ in range(0, 6):
        for t in itertools.product("01", repeat=n_):
            w = "".join(t)
            q, s, _ = M["notw"].run(w + "c")
            if s != w + "c" + "".join("1" if c == "0" else "0" for c in w):
                bad.append((w, s))
    print("notw", "OK" if not bad else bad[:5]); ok &= not bad
    bad = []
    for n_ in range(0, 5):
        for a in itertools.product("01", repeat=n_):
            for b_ in itertools.product("01", repeat=n_):
                q, s, _ = M["eq"].run("".join(a) + "c" + "".join(b_) + "c")
                last = s[-1]
                if last != ("0" if a == b_ else "1"):
                    bad.append((a, b_, s))
    print("eq", "OK" if not bad else bad[:5]); ok &= not bad
    bad = []
    for n_ in range(0, 5):
        for a in itertools.product("01", repeat=n_):
            for b_ in itertools.product("01", repeat=n_):
                q, s2, _ = M["add"].run("".join(a) + "c" + "".join(b_) + "c")
                A = int("".join(a)[::-1] or "0", 2); B = int("".join(b_)[::-1] or "0", 2)
                tot = A + B
                got = s2.split("c")[-1] if q == "qh" else None
                exp = "".join(str((tot >> i) & 1) for i in range(n_)) + str((tot >> n_) & 1)
                if got != exp:
                    bad.append((a, b_, got, exp))
    print("add", "OK" if not bad else bad[:3]); ok &= not bad
    print("trace 0011:", " ⊢ ".join(M["0n1n"].trace("0011")))
    print("ALL OK" if ok else "FAIL")
