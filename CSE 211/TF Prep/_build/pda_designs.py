"""PDA simulator (Sipser style: input, pop → push, ε = '') and every PDA designed in the two PDA notes.
Transitions: list of (q, a, pop, r, push). push string is pushed so that its FIRST char ends on top.
Acceptance by final state (input consumed)."""
import os, sys, re, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
from cfg_tools import CFG


class PDA:
    def __init__(self, start, accept, trans, sigma):
        self.start, self.accept, self.T, self.sigma = start, set(accept), trans, sigma

    def step(self, conf):
        q, i, st, w = conf
        out = []
        for (p, a, pop, r, push) in self.T:
            if p != q:
                continue
            if a and (i >= len(w) or w[i] != a):
                continue
            if pop and not st.startswith(pop):
                continue
            ns = push + (st[len(pop):] if pop else st)
            out.append((r, i + (1 if a else 0), ns, w))
        return out

    def accepts(self, w, maxstack=None):
        maxstack = maxstack or 2 * len(w) + 4
        seen, todo = set(), [(self.start, 0, "", w)]
        while todo:
            c = todo.pop()
            if c in seen or len(c[2]) > maxstack:
                continue
            seen.add(c)
            if c[1] == len(w) and c[0] in self.accept:
                return True
            todo.extend(self.step(c))
        return False

    def trace(self, w, maxstack=None):
        """one accepting sequence of configurations (q, unread, stack)"""
        maxstack = maxstack or 2 * len(w) + 4
        from collections import deque
        s0 = (self.start, 0, "", w)
        par, dq = {s0: None}, deque([s0])
        while dq:
            c = dq.popleft()
            if c[1] == len(w) and c[0] in self.accept:
                path = []
                while c:
                    path.append((c[0], w[c[1]:] or "ε", c[2] or "ε"))
                    c = par[c]
                return path[::-1]
            for d in self.step(c):
                if d not in par and len(d[2]) <= maxstack:
                    par[d] = c; dq.append(d)
        return None

    def lines(self):
        out = []
        for (p, a, pop, r, push) in self.T:
            out.append(f"{p:>6} ──{a or 'ε'}, {pop or 'ε'} → {push or 'ε'}──▶ {r}")
        return out


def check(name, pda, pred, n=8):
    bad = [w for L in range(n + 1) for w in map("".join, itertools.product(pda.sigma, repeat=L)) if pda.accepts(w) != bool(pred(w))]
    print(f"{name:12} {'OK' if not bad else 'FAIL ' + str(bad[:5])}")
    return not bad


def m3(w):
    return re.fullmatch(r"(a*)(b*)(c*)", w)


P, PR = {}, {}
Z = "Z"
P["0n1n"] = PDA("s", ["acc"], [("s", "", "", "p", Z), ("p", "0", "", "p", "X"), ("p", "", "", "m", ""), ("m", "1", "X", "m", ""),
                                ("m", "", Z, "acc", "")], "01")
PR["0n1n"] = lambda w: re.fullmatch(r"(0*)(1*)", w) is not None and w.count("0") == w.count("1")
P["anb2n"] = PDA("qs", ["qacc"], [("qs", "", "", "qa", Z), ("qa", "a", "", "qa", "X"), ("qa", "b", "", "qb1", ""), ("qb1", "b", "X", "qb0", ""),
                                  ("qb0", "b", "", "qb1", ""), ("qa", "", Z, "qacc", ""), ("qb0", "", Z, "qacc", "")], "ab")
PR["anb2n"] = lambda w: (m := re.fullmatch(r"(a*)(b*)", w)) is not None and 2 * len(m.group(1)) == len(m.group(2))
P["wwr"] = PDA("s", ["acc"], [("s", "", "", "p", Z), ("p", "0", "", "p", "0"), ("p", "1", "", "p", "1"), ("p", "", "", "m", ""),
                              ("m", "0", "0", "m", ""), ("m", "1", "1", "m", ""), ("m", "", Z, "acc", "")], "01")
PR["wwr"] = lambda w: len(w) % 2 == 0 and w == w[::-1]
P["pal"] = PDA("s", ["acc"], [("s", "", "", "p", Z), ("p", "0", "", "p", "0"), ("p", "1", "", "p", "1"), ("p", "", "", "m", ""),
                              ("p", "0", "", "m", ""), ("p", "1", "", "m", ""), ("m", "0", "0", "m", ""), ("m", "1", "1", "m", ""),
                              ("m", "", Z, "acc", "")], "01")
PR["pal"] = lambda w: w == w[::-1]
P["wcwr"] = PDA("s", ["acc"], [("s", "", "", "p", Z), ("p", "a", "", "p", "a"), ("p", "b", "", "p", "b"), ("p", "c", "", "m", ""),
                               ("m", "a", "a", "m", ""), ("m", "b", "b", "m", ""), ("m", "", Z, "acc", "")], "abc")
PR["wcwr"] = lambda w: w.count("c") == 1 and w.split("c")[0] == w.split("c")[1][::-1] and "c" not in w.split("c")[0]
# i = j or i = k (TF ★★★ ×3)
P["ij_or_ik"] = PDA("s", ["f1", "f2"], [
    ("s", "", "", "q", Z), ("q", "", "", "p1", ""), ("q", "", "", "r1", ""),
    ("p1", "a", "", "p1", "X"), ("p1", "", "", "p2", ""), ("p2", "b", "X", "p2", ""), ("p2", "", Z, "p3", Z),
    ("p3", "c", "", "p3", ""), ("p3", "", "", "f1", ""),
    ("r1", "a", "", "r1", "X"), ("r1", "", "", "r2", ""), ("r2", "b", "", "r2", ""), ("r2", "", "", "r3", ""),
    ("r3", "c", "X", "r3", ""), ("r3", "", Z, "f2", "")], "abc")
PR["ij_or_ik"] = lambda w: (m := m3(w)) is not None and (len(m.group(1)) == len(m.group(2)) or len(m.group(1)) == len(m.group(3)))
# i = j or j = k (2013-14 1(b), Hakim ex 8)
P["ij_or_jk"] = PDA("s", ["f1", "f2"], [
    ("s", "", "", "q", Z), ("q", "", "", "p1", ""), ("q", "", "", "r1", ""),
    ("p1", "a", "", "p1", "X"), ("p1", "", "", "p2", ""), ("p2", "b", "X", "p2", ""), ("p2", "", Z, "p3", Z),
    ("p3", "c", "", "p3", ""), ("p3", "", "", "f1", ""),
    ("r1", "a", "", "r1", ""), ("r1", "", "", "r2", ""), ("r2", "b", "", "r2", "Y"), ("r2", "", "", "r3", ""),
    ("r3", "c", "Y", "r3", ""), ("r3", "", Z, "f2", "")], "abc")
PR["ij_or_jk"] = lambda w: (m := m3(w)) is not None and (len(m.group(1)) == len(m.group(2)) or len(m.group(2)) == len(m.group(3)))
# a^n b^n c^m d^m, n,m ≥ 1 (2017-18 8)
P["anbncmdm"] = PDA("s", ["acc"], [
    ("s", "", "", "qa", Z), ("qa", "a", "", "qa", "X"), ("qa", "b", "X", "qb", ""), ("qb", "b", "X", "qb", ""),
    ("qb", "c", Z, "qc", "Z" + ""), ("qc", "", "", "qc", ""), ], "abcd")
P["anbncmdm"] = PDA("s", ["acc"], [
    ("s", "", "", "qa", Z), ("qa", "a", "", "qa", "X"), ("qa", "b", "X", "qb", ""), ("qb", "b", "X", "qb", ""),
    ("qb", "c", Z, "qc", "YZ"), ("qc", "c", "", "qc", "Y"), ("qc", "d", "Y", "qd", ""), ("qd", "d", "Y", "qd", ""),
    ("qd", "", Z, "acc", "")], "abcd")
PR["anbncmdm"] = lambda w: (m := re.fullmatch(r"(a+)(b+)(c+)(d+)", w)) is not None and len(m.group(1)) == len(m.group(2)) and len(m.group(3)) == len(m.group(4))
# a^n b^m c^m d^n, n,m ≥ 1 (2023-24 8)
P["anbmcmdn"] = PDA("s", ["acc"], [
    ("s", "", "", "qa", Z), ("qa", "a", "", "qa", "A"), ("qa", "b", "A", "qb", "BA"), ("qb", "b", "", "qb", "B"),
    ("qb", "c", "B", "qc", ""), ("qc", "c", "B", "qc", ""), ("qc", "d", "A", "qd", ""), ("qd", "d", "A", "qd", ""),
    ("qd", "", Z, "acc", "")], "abcd")
PR["anbmcmdn"] = lambda w: (m := re.fullmatch(r"(a+)(b+)(c+)(d+)", w)) is not None and len(m.group(1)) == len(m.group(4)) and len(m.group(2)) == len(m.group(3))
# ARITH
P["arith"] = PDA("s", ["acc"], [
    ("s", "", "", "E", Z), ("E", "a", "", "O", ""), ("E", "(", "", "E", "X"),
    ("O", "+", "", "E", ""), ("O", "*", "", "E", ""), ("O", ")", "X", "O", ""), ("O", "", Z, "acc", "")], "a+*()")
ARITH = CFG({"E": ["E+E", "E*E", "(E)", "a"]}, "E")
PR["arith"] = lambda w: ARITH.count(w) > 0
# 0^n 1^m, n ≤ m ≤ 2n (2016-17 6a)
P["n_m_2n"] = PDA("s", ["acc"], [
    ("s", "", "", "p", Z), ("p", "0", "", "p", "X"), ("p", "0", "", "p", "XX"), ("p", "", "", "q", ""),
    ("q", "1", "X", "q", ""), ("q", "", Z, "acc", "")], "01")
PR["n_m_2n"] = lambda w: (m := re.fullmatch(r"(0*)(1*)", w)) is not None and len(m.group(1)) <= len(m.group(2)) <= 2 * len(m.group(1))
# odd length, middle a (2011-12 3(c), 2012-13 4(c))
P["mid_a"] = PDA("s", ["acc"], [
    ("s", "", "", "p", Z), ("p", "a", "", "p", "X"), ("p", "b", "", "p", "X"), ("p", "a", "", "m", ""),
    ("m", "a", "X", "m", ""), ("m", "b", "X", "m", ""), ("m", "", Z, "acc", "")], "ab")
PR["mid_a"] = lambda w: len(w) % 2 == 1 and w[len(w) // 2] == "a"
# a^i b^j c^k, i + j = k
P["ijk_sum"] = PDA("s", ["acc"], [
    ("s", "", "", "qa", Z), ("qa", "a", "", "qa", "X"), ("qa", "", "", "qb", ""), ("qb", "b", "", "qb", "X"), ("qb", "", "", "qc", ""),
    ("qc", "c", "X", "qc", ""), ("qc", "", Z, "acc", "")], "abc")
PR["ijk_sum"] = lambda w: (m := m3(w)) is not None and len(m.group(1)) + len(m.group(2)) == len(m.group(3))
# equal a's and b's
P["eq_ab"] = PDA("s", ["acc"], [
    ("s", "", "", "q", Z), ("q", "a", Z, "q", "AZ"), ("q", "a", "A", "q", "AA"), ("q", "a", "B", "q", ""),
    ("q", "b", Z, "q", "BZ"), ("q", "b", "B", "q", "BB"), ("q", "b", "A", "q", ""), ("q", "", Z, "acc", "")], "ab")
PR["eq_ab"] = lambda w: w.count("a") == w.count("b")
# a^i c^k (bc)^i (2007-08 5)
P["aic_k_bci"] = PDA("s", ["acc"], [
    ("s", "", "", "qa", Z), ("qa", "a", "", "qa", "X"), ("qa", "", "", "qc", ""), ("qc", "c", "", "qc", ""), ("qc", "", "", "qb", ""),
    ("qb", "b", "X", "qx", ""), ("qx", "c", "", "qb", ""), ("qb", "", Z, "acc", "")], "abc")
PR["aic_k_bci"] = lambda w: any(w == "a" * i + "c" * k + "bc" * i for i in range(len(w) + 1) for k in range(len(w) + 1))
# balanced parentheses
P["paren"] = PDA("s", ["acc"], [("s", "", "", "q", Z), ("q", "(", "", "q", "X"), ("q", ")", "X", "q", ""), ("q", "", Z, "acc", "")], "()")
PR["paren"] = lambda w: CFG({"S": ["(S)S", ""]}, "S").count(w) > 0

# 2015-16 Q5 given PDA (Hopcroft style; acceptance by final state p). Atif notation (q, a, X) -> (p, γ)
GIVEN_1516 = [("q", "0", "Z0", "q", "XZ0"), ("q", "0", "X", "q", "XX"), ("q", "1", "X", "q", "X"), ("q", "", "X", "p", ""),
              ("p", "", "X", "p", ""), ("p", "1", "X", "p", "XX"), ("p", "1", "Z0", "p", "")]


def reachable_ids(trans, w, start="q", z0="Z0"):
    """all IDs (state, remaining, stack) reachable from (start, w, Z0); stack symbols as tokens."""
    def toks(s):
        return re.findall(r"Z0|X|[A-Z]", s)
    init = (start, w, (z0,))
    seen, order, todo = {init}, [init], [init]
    edges = []
    while todo:
        c = todo.pop(0)
        q, rest, st = c
        if not st:
            continue
        for (p, a, X, r, push) in trans:
            if p != q or st[0] != X:
                continue
            if a and not rest.startswith(a):
                continue
            n2 = (r, rest[len(a):], tuple(toks(push)) + st[1:])
            edges.append((c, n2))
            if n2 not in seen:
                seen.add(n2); order.append(n2); todo.append(n2)
    return order, edges


if __name__ == "__main__":
    ok = True
    for k in P:
        if k in PR:
            ok &= check(k, P[k], PR[k], 7 if len(P[k].sigma) <= 2 else 5 if len(P[k].sigma) <= 3 else 4)
    for w in ["00111", "0011111"]:
        print("n_m_2n", w, P["n_m_2n"].accepts(w))
    print("trace bbcbb:", P["wcwr"].trace("bbcbb"))
    print("trace aabbccdd (anbmcmdn):", P["anbmcmdn"].trace("aabbccdd"))
    for w in ["0011", "0101", "1010"]:
        ids, edges = reachable_ids(GIVEN_1516, w)
        fin = [i for i in ids if i[1] == "" and i[0] == "p"]
        print(w, len(ids), "IDs; accepted:", bool(fin))
        for i in ids:
            print("   ", i)
    print("ALL OK" if ok else "FAIL")
