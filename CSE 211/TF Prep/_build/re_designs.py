"""Regular-expression answers, Thompson NFAs, GNFA (state elimination) and product checks for the Regulars note.
RE syntax used here: | = union, * = star, + (postfix) = one or more, ε = empty string, ∅ = empty set.
Every RE is compared with its language definition on all strings up to a length bound."""
import os, sys, re, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from automata import NFA, DFA, strings


def py(r):
    """Convert our RE notation to a Python regex (fullmatch)."""
    return r.replace("ε", "").replace("∅", "(?!)").replace(" ", "")


def match(r, w):
    return re.fullmatch(py(r), w) is not None


REQ = []  # (label, RE, predicate, alphabet, maxlen)


def req(label, r, pred, sig="01", n=10):
    REQ.append((label, r, pred, sig, n))


def occ(w, p):
    return sum(1 for i in range(len(w)) if w.startswith(p, i))


S = "(0|1)"
req("alt", "(1|ε)(01)*(0|ε)", lambda w: all(w[i] != w[i + 1] for i in range(len(w) - 1)))
req("ac", "(a|b|c)*a(a|b|c)*c(a|b|c)*|(a|b|c)*c(a|b|c)*a(a|b|c)*", lambda w: "a" in w and "c" in w, "abc", 6)
req("no00or11", "(1|01)*(0|ε)|(0|10)*(1|ε)", lambda w: "00" not in w or "11" not in w)
req("even1", "0*(10*10*)*", lambda w: w.count("1") % 2 == 0)
req("div5dec", "0|5|[1-9][0-9]*(0|5)", lambda w: w != "" and (w == "0" or w[0] != "0") and int(w) % 5 == 0, "0123456789", 3)
req("odd0or1", "1*0(1*01*0)*1*|0*1(0*10*1)*0*", lambda w: w.count("0") % 2 == 1 or w.count("1") % 2 == 1)
req("no101", "0*(1+00+)*(ε|1+|1+0)", lambda w: "101" not in w)
req("ab_abc", "(a|b|c)*a(a|b|c)*b(a|b|c)*|(a|b|c)*b(a|b|c)*a(a|b|c)*", lambda w: "a" in w and "b" in w, "abc", 6)


def b4(w):
    i11 = [i for i in range(len(w) - 1) if w[i:i + 2] == "11"]
    i00 = [i for i in range(len(w) - 1) if w[i:i + 2] == "00"]
    return all(j < i for i in i11 for j in i00)


req("00before11", "(0|10)*(1|ε)(1|01)*(0|ε)", b4)
perm = "|".join(f"(a|b|c)*{x}(a|b|c)*{y}(a|b|c)*{z}(a|b|c)*" for x, y, z in itertools.permutations("abc"))
req("abc_all", perm, lambda w: set("abc") <= set(w), "abc", 6)
req("anbm_n3_modd", "aaaa*b(bb)*", lambda w: re.fullmatch(r"a{3,}b+", w) is not None and w.count("b") % 2 == 1, "ab")
req("anbm_odd", "(aa)*a(bb)*|(aa)*b(bb)*", lambda w: re.fullmatch(r"a*b*", w) is not None and len(w) % 2 == 1, "ab")
req("vwv", "aa(a|b)*aa|ab(a|b)*ab|ba(a|b)*ba|bb(a|b)*bb", lambda w: len(w) >= 4 and w[:2] == w[-2:], "ab")
req("a_mod3", "b*(ab*ab*ab*)*", lambda w: w.count("a") % 3 == 0, "ab")
req("le3a", "b*(a|ε)b*(a|ε)b*(a|ε)b*", lambda w: w.count("a") <= 3, "ab")
req("one_aaa", "(b|ab|aab)*aaa(b|ba|baa)*", lambda w: occ(w, "aaa") == 1, "ab")
req("not_last2eq", "ε|0|1|(0|1)*(01|10)", lambda w: not (len(w) >= 2 and w[-1] == w[-2]))
req("15_i", "1(0|1)*0", lambda w: w[:1] == "1" and w[-1:] == "0")
req("15_ii", "(0|1)(0|1)0(0|1)*", lambda w: len(w) >= 3 and w[2] == "0")
req("15_iii", "(1*01*0)*1*|0*10*10*", lambda w: w.count("0") % 2 == 0 or w.count("1") == 2)
req("15_iv", "ε|0|1|00|01|10|0(0|1)(0|1)|10(0|1)|110|(0|1)(0|1)(0|1)(0|1)(0|1)*", lambda w: w not in ("11", "111"))
req("15_v", "000*|1000*|0100*|000*10*", lambda w: w.count("0") >= 2 and w.count("1") <= 1)
req("no11", "(1|ε)(00*1)*0*", lambda w: "11" not in w)
req("L1L2", "1(1|0)*000(1(01)*0)*", None)
req("simp1", "(a|b)*", lambda w: True, "ab")
req("13_6c", "(aa*b)*", None, "ab")
req("22_4c_A", "0*1(1|00*1)*", lambda w: w.endswith("1"))
req("22_4c_C", "(0|1)*1", lambda w: w.endswith("1"))

# RE option questions: which options are correct
OPTS = {
    "21_3d": (lambda w: "00" in w and "11" in w, "01", {
        "A": "(0|1)*0011(0|1)*|(0|1)*1100(0|1)*",
        "B": "(0|1)*(00(0|1)*11|11(0|1)*00)(0|1)*",
        "C": "(0|1)*00(0|1)*|(0|1)*11(0|1)*",
        "D": "00(0|1)*11|11(0|1)*00"}),
    "22_4c": (lambda w: w.endswith("1"), "01", {
        "A": "0*1(1|00*1)*", "B": "0*1*1|11*0*1", "C": "(0|1)*1"}),
    "23_4b": (lambda w: occ(w, "aa") <= 1, "ab", {
        "A": "(b|ab)*(ε|a|aa)(b|ab)*", "B": "(b|ab)*(ε|a|aa)(b|ba)*",
        "C": "(b|ab)*(ε|a)(b|ba)*", "D": "(b|ba)*(ε|a|aa)(b|ba)*"}),
}


def option_report(key, n=9):
    pred, sig, opts = OPTS[key]
    out = {}
    for k, r in opts.items():
        fp = [w for w in strings(sig, n) if match(r, w) and not pred(w)]
        fn = [w for w in strings(sig, n) if not match(r, w) and pred(w)]
        out[k] = (not fp and not fn, fp[:2], fn[:2])
    return out


# ---- Thompson construction (slides Lec05 sl. 87–93)
class T:
    def __init__(self):
        self.n, self.e = 0, []

    def new(self):
        self.n += 1
        return f"s{self.n}"

    def build(self, r):
        self.s, self.i = r.replace(" ", ""), 0
        a, b = self.union()
        return a, b

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else None

    def union(self):
        a, b = self.concat()
        while self.peek() == "|":
            self.i += 1
            c, d = self.concat()
            s, f = self.new(), self.new()
            self.e += [(s, "", a), (s, "", c), (b, "", f), (d, "", f)]
            a, b = s, f
        return a, b

    def concat(self):
        a, b = self.star()
        while self.peek() not in (None, "|", ")"):
            c, d = self.star()
            self.e.append((b, "", c))
            b = d
        return a, b

    def star(self):
        a, b = self.atom()
        while self.peek() == "*":
            self.i += 1
            s, f = self.new(), self.new()   # Sipser: new accepting start; we use s (start) and f (accept)
            self.e += [(s, "", a), (b, "", a), (b, "", f), (s, "", f)]
            a, b = s, f
        return a, b

    def atom(self):
        c = self.peek()
        if c == "(":
            self.i += 1
            a, b = self.union()
            self.i += 1
            return a, b
        self.i += 1
        s, f = self.new(), self.new()
        self.e.append((s, "" if c == "ε" else c, f))
        return s, f


def thompson(r, sig):
    t = T()
    s, f = t.build(r)
    d = {}
    for (p, a, q) in t.e:
        d.setdefault((p, a), set()).add(q)
    st = sorted({x for e in t.e for x in (e[0], e[2])}, key=lambda x: int(x[1:]))
    return NFA(st, sig, d, s, [f]), t.e


# ---- GNFA state elimination (slides Lec05 sl. 94–109)
def gnfa(states, start, accept, edges, order):
    """edges: dict (p,q)->RE string. Returns list of steps (ripped, new labels) and final RE."""
    R = dict(edges)
    S, A = "qs", "qa"
    R[(S, start)] = "ε"
    for f in accept:
        R[(f, A)] = R.get((f, A), "") and R[(f, A)] + "|ε" or "ε"
    alive = [S] + list(states) + [A]
    steps = []

    def cat(*xs):
        xs = [x for x in xs if x != "ε"]
        return "".join(f"({x})" if "|" in x else x for x in xs) or "ε"

    for rip in order:
        alive.remove(rip)
        loop = R.get((rip, rip))
        lp = (f"({loop})*" if len(loop) > 1 else f"{loop}*") if loop else ""
        changes = []
        for p in alive:
            for q in alive:
                if (p, rip) in R and (rip, q) in R:
                    path = cat(R[(p, rip)], lp, R[(rip, q)]) if lp else cat(R[(p, rip)], R[(rip, q)])
                    old = R.get((p, q))
                    R[(p, q)] = f"{old}|{path}" if old else path
                    changes.append(f"R({p},{q}) = {R[(p, q)]}")
        for k in [k for k in R if rip in k]:
            del R[k]
        steps.append((rip, changes))
    return steps, R.get((S, A), "∅")


DFA_RE = {
    "12_7b": (["1", "2", "3"], "1", ["2", "3"],
              {("1", "2"): "a", ("1", "3"): "b", ("2", "1"): "a", ("2", "2"): "b", ("3", "1"): "b", ("3", "2"): "a"}, "ab"),
    "13_6c": (["q0", "q1", "q2"], "q0", ["q0"],
              {("q0", "q1"): "a", ("q1", "q0"): "b", ("q1", "q2"): "a", ("q2", "q2"): "a", ("q2", "q0"): "b"}, "ab"),
    "11_7c": (["1", "2", "3"], "1", ["1", "2", "3"],
              {("1", "2"): "a|b", ("2", "2"): "a", ("2", "3"): "b", ("3", "1"): "a", ("3", "2"): "b"}, "ab"),
    "div3": (["q0", "q1", "q2"], "q0", ["q0"],
             {("q0", "q0"): "0", ("q0", "q1"): "1", ("q1", "q0"): "1", ("q1", "q2"): "0", ("q2", "q1"): "0", ("q2", "q2"): "1"}, "01"),
}


def dfa_accepts(spec, w):
    st, s, acc, ed, sig = spec
    q = s
    for c in w:
        nxt = [b for (a, b), lab in ed.items() if a == q and c in lab.split("|")]
        if not nxt:
            return False
        q = nxt[0]
    return q in acc


def star_flaw_demo():
    """N1: q1 (start) loops a, q1 -b-> q2 (accept). A = a*b. Hasty: q1 accepting + ε q2->q1."""
    good = NFA(["q0", "q1", "q2"], "ab", {("q0", ""): {"q1"}, ("q1", "a"): {"q1"}, ("q1", "b"): {"q2"}, ("q2", ""): {"q1"}},
               "q0", ["q0", "q2"])
    bad = NFA(["q1", "q2"], "ab", {("q1", "a"): {"q1"}, ("q1", "b"): {"q2"}, ("q2", ""): {"q1"}}, "q1", ["q1", "q2"])
    pred = lambda w: re.fullmatch(r"(a*b)*", w) is not None
    return (all(good.accepts(w) == pred(w) for w in strings("ab", 8)),
            [w for w in strings("ab", 4) if bad.accepts(w) and not pred(w)][:3])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ok = True
    for label, r, pred, sig, nmax in REQ:
        if pred is None:
            continue
        bad = [w for w in strings(sig, nmax) if match(r, w) != bool(pred(w))]
        print(f"{label:14} {'OK' if not bad else 'FAIL ' + str(bad[:4])}")
        ok &= not bad
    for w in ["1000", "1000101010", "10000111000100000"]:
        print("L1L2", w, match("1(1|0)*000(1(01)*0)*", w))
    for k in OPTS:
        print(k, option_report(k))
    for k, spec in DFA_RE.items():
        st = spec[0]
        order = st[::-1] if k == "div3" else st[::-1]
        steps, res = gnfa(st, spec[1], spec[2], spec[3], order)
        bad = [w for w in strings(spec[4], 9) if match(res, w) != dfa_accepts(spec, w)]
        print(k, res, "OK" if not bad else f"FAIL {bad[:4]}")
        ok &= not bad
    hand = {"12_7b": None, "13_6c": "(aa*b)*", "11_7c": "(a|b)*"}
    for k, r in hand.items():
        if r:
            bad = [w for w in strings("ab", 10) if match(r, w) != dfa_accepts(DFA_RE[k], w)]
            print("hand", k, r, "OK" if not bad else bad[:3]); ok &= not bad
    for r in ["(0|1)*1(0|1)", "(a|b)*aba", "((a*)a)*", "((00)*(11)|01)*"]:
        sig = "ab" if "a" in r else "01"
        nf, e = thompson(r, sig)
        bad = [w for w in strings(sig, 8) if nf.accepts(w) != match(r, w)]
        print("thompson", r, len(nf.states), "states", "OK" if not bad else bad[:3]); ok &= not bad
    print("star flaw:", star_flaw_demo())
    print("ALL OK" if ok else "FAIL")
