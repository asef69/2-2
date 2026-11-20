"""NFAs and subset constructions for the NFA note (Lessons 6–9), each checked by simulation.
'' = ε. Run: python -P nfa_designs.py"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from automata import NFA, DFA, strings, check

N, P = {}, {}


def nfa(start, accept, edges, sigma):
    d = {}
    st = set([start]) | set(accept)
    for (q, a, r) in edges:
        d.setdefault((q, a), set()).add(r)
        st |= {q, r}
    order = [start] + sorted(st - {start})
    return NFA(order, sigma, d, start, accept)


# ---------------- designs
# 2014-15 3(a): nonzero length, nonzero even number of a's at the end (block preceded by b or start)
N["14_3a"] = nfa("s", ["A2"], [("s", "a", "A1"), ("s", "b", "B"), ("s", "a", "L"), ("s", "b", "L"), ("L", "a", "L"),
                               ("L", "b", "L"), ("L", "b", "B"), ("B", "a", "A1"), ("A1", "a", "A2"), ("A2", "a", "A1")], "ab")
P["14_3a"] = lambda w: (m := re.search(r"a*$", w)) is not None and len(m.group()) > 0 and len(m.group()) % 2 == 0

# 2016-17 3(a)(i)/(ii) — digits; checked on alphabet {0,1,2} (same construction for 10 digits)
DIG = "012"
e = []
for d in DIG:
    e += [("s", x, "s") for x in DIG]
    e += [("s", d, f"p{d}")] + [(f"p{d}", x, f"p{d}") for x in DIG] + [(f"p{d}", d, "f")]
N["16_3a_i"] = nfa("s", ["f"], e, DIG)
P["16_3a_i"] = lambda w: len(w) >= 1 and w[-1] in w[:-1]
e = []
for d in DIG:
    e += [("s", "", f"r{d}")] + [(f"r{d}", x, f"r{d}") for x in DIG if x != d] + [(f"r{d}", d, "f")]
N["16_3a_ii"] = nfa("s", ["f"], e, DIG)
P["16_3a_ii"] = lambda w: len(w) >= 1 and w[-1] not in w[:-1]

# 2016-17 3(a)(iii): two 0s with k characters between, k ≡ 0 (mod 4), k = 0 allowed
e = [("s", x, "s") for x in "01"] + [("s", "0", "c0"), ("c0", "0", "F")]
for i in range(4):
    e += [(f"c{i}", x, f"c{(i + 1) % 4}") for x in "01"]
e += [("F", x, "F") for x in "01"]
N["16_3a_iii"] = nfa("s", ["F"], e, "01")


def zeros_gap(w, nonzero):
    z = [i for i, c in enumerate(w) if c == "0"]
    return any((j - i - 1) % 4 == 0 and (j - i - 1 > 0 or not nonzero) for i in z for j in z if j > i)


P["16_3a_iii"] = lambda w: zeros_gap(w, False)
# 2017-18 3(a): same but the gap must be nonzero
e = [("s", x, "s") for x in "01"] + [("s", "0", "d0")]
e += [("d0", x, "e1") for x in "01"] + [("e1", x, "e2") for x in "01"] + [("e2", x, "e3") for x in "01"]
e += [("e3", x, "e4") for x in "01"] + [("e4", x, "e1") for x in "01"] + [("e4", "0", "F")] + [("F", x, "F") for x in "01"]
N["17_3a"] = nfa("s", ["F"], e, "01")
P["17_3a"] = lambda w: zeros_gap(w, True)

# Jan-2020 2(b): last two symbols equal
N["20_2b"] = nfa("s", ["F"], [("s", "0", "s"), ("s", "1", "s"), ("s", "0", "a"), ("a", "0", "F"), ("s", "1", "b"),
                              ("b", "1", "F")], "01")
P["20_2b"] = lambda w: len(w) >= 2 and w[-1] == w[-2]

# 2019-20 3(b): {a^n b^n | n ≤ 3} = {ε, ab, aabb, aaabbb}
N["19_3b"] = nfa("q0", ["q0", "f"], [("q0", "a", "q1"), ("q1", "a", "q2"), ("q2", "a", "q3"), ("q1", "b", "f"),
                                     ("q2", "b", "p1"), ("q3", "b", "p2"), ("p2", "b", "p1"), ("p1", "b", "f")], "ab")
P["19_3b"] = lambda w: w in ("", "ab", "aabb", "aaabbb")

# 2021-22 3(b): at least two 0s, or exactly two 1s
N["21_3b"] = nfa("s", ["u1", "u2"], [("s", "", "s1"), ("s", "", "s2"), ("s1", "0", "s1"), ("s1", "1", "s1"),
                                     ("s1", "0", "t1"), ("t1", "0", "t1"), ("t1", "1", "t1"), ("t1", "0", "u1"),
                                     ("u1", "0", "u1"), ("u1", "1", "u1"), ("s2", "0", "s2"), ("s2", "1", "t2"),
                                     ("t2", "0", "t2"), ("t2", "1", "u2"), ("u2", "0", "u2")], "01")
P["21_3b"] = lambda w: w.count("0") >= 2 or w.count("1") == 2

# 2022-23 4(b): begin and end with different symbols, odd length
N["22_4b"] = nfa("s", ["F"], [("s", "0", "x0"), ("x0", "0", "y0"), ("x0", "1", "y0"), ("y0", "0", "x0"), ("y0", "1", "x0"),
                              ("y0", "1", "F"), ("s", "1", "x1"), ("x1", "0", "y1"), ("x1", "1", "y1"), ("y1", "0", "x1"),
                              ("y1", "1", "x1"), ("y1", "0", "F")], "01")
P["22_4b"] = lambda w: len(w) % 2 == 1 and len(w) >= 3 and w[0] != w[-1]

# 2023-24 3(a): {a^n | n≥1} ∪ {b^m a^k} = b*a*
N["23_3a_3"] = nfa("s", ["s", "A", "B"], [("s", "a", "A"), ("A", "a", "A"), ("s", "b", "B"), ("B", "b", "B"), ("B", "a", "A")], "ab")
N["23_3a_2"] = nfa("q0", ["q0", "q1"], [("q0", "b", "q0"), ("q0", "a", "q1"), ("q1", "a", "q1")], "ab")
P["23_3a_3"] = P["23_3a_2"] = lambda w: re.fullmatch(r"b*a*", w) is not None

# 2023-24 4(a): {a}* ; removing edge S -ε-> M leaves {a}
N["23_4a"] = nfa("S", ["M", "F"], [("S", "", "M"), ("M", "a", "M"), ("S", "a", "F")], "a")
N["23_4a_cut"] = nfa("S", ["M", "F"], [("M", "a", "M"), ("S", "a", "F")], "a")
P["23_4a"] = lambda w: True
P["23_4a_cut"] = lambda w: w == "a"

# 2008-09 6(b): n-th symbol from the end is 1 (n = 3)
N["nth3"] = nfa("q0", ["q3"], [("q0", "0", "q0"), ("q0", "1", "q0"), ("q0", "1", "q1"), ("q1", "0", "q2"), ("q1", "1", "q2"),
                               ("q2", "0", "q3"), ("q2", "1", "q3")], "01")
P["nth3"] = lambda w: len(w) >= 3 and w[-3] == "1"

# 2011-12 7(a): (01 ∪ 001 ∪ 010)*
N["11_7a"] = nfa("s", ["s"], [("s", "0", "p"), ("p", "1", "s"), ("p", "1", "r"), ("r", "0", "s"), ("p", "0", "u"),
                              ("u", "1", "s")], "01")
P["11_7a"] = lambda w: re.fullmatch(r"(01|001|010)*", w) is not None

# 2014-15 4(a): even number of occurrences of 01  — NFA from 1*(0+1+0+1+)*0*
N["14_4a"] = nfa("s", ["e"], [("s", "1", "s"), ("s", "", "m"), ("m", "0", "a"), ("a", "0", "a"), ("a", "1", "b"),
                              ("b", "1", "b"), ("b", "0", "c"), ("c", "0", "c"), ("c", "1", "d"), ("d", "1", "d"),
                              ("d", "", "m"), ("m", "", "e"), ("e", "0", "e")], "01")
P["14_4a"] = lambda w: w.count("01") % 2 == 0

# ---------------- given NFAs (conversion questions)
TBL = nfa("p", ["r"], [("p", "a", "p"), ("p", "b", "q"), ("p", "c", "r"), ("q", "a", "q"), ("q", "b", "r"), ("q", "", "p"),
                       ("r", "a", "r"), ("r", "c", "p"), ("r", "", "q")], "abc")
N["pqr"] = TBL  # 2008-09 6(c), 2017-18 4(a), Jan-2020 1(c)
N["10_3"] = nfa("p", ["s", "t"], [("p", "0", "p"), ("p", "0", "q"), ("p", "1", "p"), ("q", "0", "r"), ("q", "0", "s"),
                                  ("q", "1", "t"), ("r", "0", "p"), ("r", "0", "r"), ("r", "1", "t")], "01")
N["09_3"] = nfa("q1", ["q5"], [("q1", "", "q2"), ("q2", "a", "q3"), ("q3", "a", "q2"), ("q3", "b", "q3"), ("q3", "", "q5"),
                               ("q2", "b", "q4"), ("q4", "b", "q2"), ("q4", "a", "q3"), ("q4", "", "q5")], "ab")
N["16_2b"] = nfa("p", ["q"], [("p", "0", "q"), ("p", "", "r"), ("q", "0", "q"), ("q", "", "r"), ("r", "1", "q"),
                              ("r", "", "s"), ("s", "0", "p"), ("s", "0", "r")], "01")
N["20_4b"] = nfa("q0", ["q10"], [("q0", "", "q1"), ("q0", "", "q7"), ("q1", "", "q2"), ("q1", "", "q4"), ("q2", "0", "q3"),
                                 ("q3", "", "q6"), ("q4", "1", "q5"), ("q5", "", "q6"), ("q6", "", "q1"), ("q6", "", "q7"),
                                 ("q7", "0", "q8"), ("q8", "1", "q9"), ("q9", "1", "q10")], "01")
P["20_4b"] = lambda w: w.endswith("011")
N["21_3c"] = nfa("q1", ["q3"], [("q1", "a", "q3"), ("q1", "", "q2"), ("q2", "a", "q1"), ("q3", "a", "q2"), ("q3", "b", "q2"),
                                ("q3", "b", "q3")], "ab")  # accept state not printed: q3 assumed
P["16_2b"] = lambda w: len(w) >= 1
# 2016-17 3(a)(iii) distance reading: zeros at i < j with j − i a positive multiple of 4
e = [("s", x, "s") for x in "01"] + [("s", "0", "t0")]
for i in range(4):
    e += [(f"t{i}", x, f"t{(i + 1) % 4}") for x in "01"]
e += [("t3", "0", "F")] + [("F", x, "F") for x in "01"]
N["16_dist"] = nfa("s", ["F"], e, "01")
P["16_dist"] = lambda w: any(w[i] == w[j] == "0" and (j - i) % 4 == 0 for i in range(len(w)) for j in range(i + 1, len(w)))
N["13_7a"] = nfa("q0", ["q2"], [("q0", "a", "q1"), ("q0", "", "q4"), ("q1", "", "q2"), ("q2", "a", "q1"), ("q4", "b", "q1"),
                                ("q4", "a", "q3"), ("q3", "b", "q1"), ("q3", "", "q2")], "ab")
N["slides_aba"] = nfa("q0", ["q3"], [("q0", "a", "q0"), ("q0", "b", "q0"), ("q0", "a", "q1"), ("q1", "b", "q2"),
                                     ("q2", "a", "q3"), ("q3", "a", "q3"), ("q3", "b", "q3")], "ab")
P["slides_aba"] = lambda w: "aba" in w
N["slides_eps"] = nfa("q0", ["q4"], [("q0", "", "q1"), ("q1", "0", "q2"), ("q1", "1", "q3"), ("q2", "", "q4"),
                                     ("q3", "", "q1"), ("q3", "1", "q4")], "01")


def subset_lines(nf, names=None):
    order, delta, acc = nf.subset()
    names = names or {S: chr(ord("A") + i) for i, S in enumerate(order)}
    w = max(9, max(len(setname(S)) for S in order) + 2)
    lines = [f"{'':3}{'DFA state':<10}{'NFA set':<{w}}" + "".join(f"{a:<8}" for a in nf.sigma)]
    for S in order:
        tag = ("→" if S == order[0] else " ") + ("*" if S in acc else " ")
        lines.append(f"{tag} {names[S]:<10}{setname(S):<{w}}" + "".join(f"{names[delta[(S, a)]]:<8}" for a in nf.sigma))
    return lines, order, delta, acc, names


def setname(S):
    if not S:
        return "∅"
    def k(x):
        m = re.match(r"([a-zA-Z]+)(\d*)", x)
        return (m.group(1), int(m.group(2)) if m.group(2) else -1)
    return "{" + ",".join(sorted(S, key=k)) + "}"


def eps_closure_lines(nf):
    return [f"E({q}) = {setname(nf.close({q}))}" for q in nf.states]


def remove_eps(nf):
    """Slides' method (Lec04 sl. 80–82): δ'(q,a) = E(∪_{r∈E(q)} δ(r,a)), F' = {q : E(q) ∩ F ≠ ∅}."""
    d, F = {}, set()
    for q in nf.states:
        Eq = nf.close({q})
        if Eq & nf.accept:
            F.add(q)
        for a in nf.sigma:
            t = set()
            for r in Eq:
                t |= nf.delta.get((r, a), set())
            d[(q, a)] = nf.close(t) if t else frozenset()
    return d, F


def nfa_table(nf):
    cols = nf.sigma + ([""] if any(k[1] == "" for k in nf.delta) else [])
    w = 4 + max(len(setname(nf.delta.get((q, a), set()))) for q in nf.states for a in cols)
    lines = ["      " + "".join(f"{(a or 'ε'):<{w}}" for a in cols)]
    for q in nf.states:
        tag = ("→" if q == nf.start else " ") + ("*" if q in nf.accept else " ")
        lines.append(f"{tag} {q:<4}" + "".join(f"{setname(nf.delta.get((q, a), set())):<{w}}" for a in cols))
    return lines


if __name__ == "__main__":
    ok = True
    for k in N:
        if k in P:
            nf = N[k]
            bad = [w for w in strings(nf.sigma, 8 if len(nf.sigma) <= 2 else 5) if nf.accepts(w) != bool(P[k](w))]
            print(k, "OK" if not bad else f"FAIL {bad[:6]}")
            ok &= not bad
            # its subset DFA must agree too
            D = nf.to_dfa()
            bad2 = [w for w in strings(nf.sigma, 7 if len(nf.sigma) <= 2 else 4) if D.accepts(w) != bool(P[k](w))]
            ok &= not bad2
    for k in ["pqr", "10_3", "09_3", "16_2b", "20_4b", "21_3c", "13_7a", "11_7a", "14_4a", "slides_aba", "slides_eps"]:
        lines, order, delta, acc, names = subset_lines(N[k])
        print("\n#", k, f"{len(order)} DFA states")
        print("\n".join(lines))
    print("\nε-closures pqr:", eps_closure_lines(N["pqr"]))
    acc3 = [w for w in strings("abc", 3) if N["pqr"].accepts(w)]
    print("pqr accepted, |w|<=3:", len(acc3), acc3)
    d, F = remove_eps(N["13_7a"])
    print("13_7a ε-removed F' =", F)
    for q in N["13_7a"].states:
        print("  ", q, {a: setname(d[(q, a)]) for a in "ab"})
    # check ε-removal preserves language
    nn = NFA(N["13_7a"].states, "ab", {k: set(v) for k, v in d.items()}, "q0", F)
    ok &= all(nn.accepts(w) == N["13_7a"].accepts(w) for w in strings("ab", 8))
    d2, F2 = remove_eps(N["slides_eps"])
    print("slides eps F'", F2, {(q, a): setname(d2[(q, a)]) for q in N['slides_eps'].states for a in '01'})
    print("23_4a min-state check: 1-state NFAs cannot give b*a* (by inspection)")
    print("ALL OK" if ok else "FAIL")
