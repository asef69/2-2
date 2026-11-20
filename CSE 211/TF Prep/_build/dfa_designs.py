"""Every DFA designed in the DFA note (Lessons 3–5), with a brute-force check against the language definition.
Run: python -P dfa_designs.py"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from automata import DFA, check, strings

D = {}

# 2006-07 1(a): start with 0 and odd length, or start with 1 and even length
D["06_1a"] = DFA(["s", "0odd", "0even", "1odd", "1even"], "01",
                 {("s", "0"): "0odd", ("s", "1"): "1odd",
                  **{(q, c): r for q, r in [("0odd", "0even"), ("0even", "0odd"), ("1odd", "1even"), ("1even", "1odd")] for c in "01"}},
                 "s", ["0odd", "1even"])
P = {"06_1a": lambda w: (w[:1] == "0" and len(w) % 2 == 1) or (w[:1] == "1" and len(w) % 2 == 0 and w != "")}

# 2006-07 2(b): even #0 and odd #1
par = {}
for z in "EO":
    for o in "EO":
        par[(z + o, "0")] = ("O" if z == "E" else "E") + o
        par[(z + o, "1")] = z + ("O" if o == "E" else "E")
D["06_2b"] = DFA(["EE", "EO", "OE", "OO"], "01", par, "EE", ["EO"])
P["06_2b"] = lambda w: w.count("0") % 2 == 0 and w.count("1") % 2 == 1

# 2007-08 1(b): every a immediately followed by b  = (b ∪ ab)*
D["07_1b"] = DFA(["q0", "q1"], "ab", {("q0", "b"): "q0", ("q0", "a"): "q1", ("q1", "b"): "q0"}, "q0", ["q0"], dead="d")
P["07_1b"] = lambda w: re.fullmatch(r"(b|ab)*", w) is not None

# remainder DFAs


def mod_dfa(base, m, accept_rems, first=None, digits=None):
    digits = digits or [str(d) for d in range(base)]
    st = ["s"] + [f"r{r}" for r in range(m)]
    dl = {}
    for d in digits:
        if first is None or d in first:
            dl[("s", d)] = f"r{int(d) % m}"
    for r in range(m):
        for d in digits:
            dl[(f"r{r}", d)] = f"r{(base * r + int(d)) % m}"
    dead = None if first is None else "dead"
    return DFA(st, digits, dl, "s", [f"r{r}" for r in accept_rems], dead=dead)


D["mod3"] = mod_dfa(2, 3, [0]); P["mod3"] = lambda w: w != "" and int(w, 2) % 3 == 0
D["not3"] = mod_dfa(2, 3, [1, 2]); P["not3"] = lambda w: w != "" and int(w, 2) % 3 != 0
D["mod5"] = mod_dfa(2, 5, [0]); P["mod5"] = lambda w: w != "" and int(w, 2) % 5 == 0
D["mod4"] = mod_dfa(2, 4, [0]); P["mod4"] = lambda w: w != "" and int(w, 2) % 4 == 0
D["mod5_lead1"] = mod_dfa(2, 5, [0], first=["1"]); P["mod5_lead1"] = lambda w: w[:1] == "1" and int(w, 2) % 5 == 0
D["b3_not4"] = mod_dfa(3, 4, [1, 2, 3]); P["b3_not4"] = lambda w: w != "" and int(w, 3) % 4 != 0
# power of 2 beginning with 1 = 10*
D["pow2"] = DFA(["s", "A"], "01", {("s", "1"): "A", ("A", "0"): "A"}, "s", ["A"], dead="dead")
P["pow2"] = lambda w: w[:1] == "1" and int(w, 2) & (int(w, 2) - 1) == 0

# 2009-10 Q2: first symbol never appears three times in a row
dl = {("s", "a"): "A1", ("s", "b"): "B1"}
for X, Y in (("A", "b"), ("B", "a")):
    x = X.lower()
    dl[(X + "0", x)] = X + "1"; dl[(X + "0", Y)] = X + "0"
    dl[(X + "1", x)] = X + "2"; dl[(X + "1", Y)] = X + "0"
    dl[(X + "2", Y)] = X + "0"
D["09_2"] = DFA(["s", "A0", "A1", "A2", "B0", "B1", "B2"], "ab", dl, "s",
                ["s", "A0", "A1", "A2", "B0", "B1", "B2"], dead="D")
P["09_2"] = lambda w: w == "" or (w[0] * 3) not in w

# 2010-11 Q2: (#a) mod 3 = 1
D["10_2"] = DFA(["r0", "r1", "r2"], "ab", {("r0", "a"): "r1", ("r1", "a"): "r2", ("r2", "a"): "r0",
                                         ("r0", "b"): "r0", ("r1", "b"): "r1", ("r2", "b"): "r2"}, "r0", ["r1"])
P["10_2"] = lambda w: w.count("a") % 3 == 1

# 2010-11 Q4: no 110
D["10_4"] = DFA(["q", "q1", "q11"], "01", {("q", "0"): "q", ("q", "1"): "q1", ("q1", "0"): "q", ("q1", "1"): "q11",
                                         ("q11", "1"): "q11"}, "q", ["q", "q1", "q11"], dead="D")
P["10_4"] = lambda w: "110" not in w
RE_10_4 = r"(0|10)*1*"

# 2011-12 5(c): |w| <= 5
D["11_5c"] = DFA([f"q{i}" for i in range(6)], "01",
                 {(f"q{i}", c): f"q{i + 1}" for i in range(5) for c in "01"}, "q0", [f"q{i}" for i in range(6)], dead="q6")
P["11_5c"] = lambda w: len(w) <= 5

# 2013-14 5(c): a^p b^q, p+q even
D["13_5c"] = DFA(["Ea", "Oa", "Eb", "Ob"], "ab", {("Ea", "a"): "Oa", ("Oa", "a"): "Ea", ("Ea", "b"): "Ob", ("Oa", "b"): "Eb",
                                                ("Eb", "b"): "Ob", ("Ob", "b"): "Eb"}, "Ea", ["Ea", "Eb"], dead="D")
P["13_5c"] = lambda w: re.fullmatch(r"a*b*", w) is not None and len(w) % 2 == 0


# sum-with-reset DFAs


def reset_dfa(digits, m, acc):
    dl = {}
    for r in range(m):
        for d in digits:
            dl[(f"r{r}", d)] = f"r{(r + int(d)) % m}"
        dl[(f"r{r}", "R")] = "r0"
    return DFA([f"r{r}" for r in range(m)], digits + ["R"], dl, "r0", [f"r{r}" for r in acc])


def reset_pred(m, acc):
    def p(w):
        s = 0
        for c in w:
            s = 0 if c == "R" else s + int(c)
        return s % m in acc
    return p


D["14_1a"] = reset_dfa(["0", "1", "2", "3"], 3, [0]); P["14_1a"] = reset_pred(3, [0])
D["19_1c"] = reset_dfa(["0", "1", "2"], 5, [1, 2]); P["19_1c"] = reset_pred(5, [1, 2])
D["22_1b"] = reset_dfa(["0", "1", "2"], 3, [0]); P["22_1b"] = reset_pred(3, [0])

# 2016-17 2(a): #a ≡ 0 mod 3 and even digit sum, over {a,b,1,2}
dl = {}
for k in range(3):
    for p_ in "EO":
        q = f"{k}{p_}"
        dl[(q, "a")] = f"{(k + 1) % 3}{p_}"
        dl[(q, "b")] = q
        dl[(q, "1")] = f"{k}{'O' if p_ == 'E' else 'E'}"
        dl[(q, "2")] = q
D["16_2a"] = DFA([f"{k}{p_}" for k in range(3) for p_ in "EO"], "ab12", dl, "0E", ["0E"])
P["16_2a"] = lambda w: w.count("a") % 3 == 0 and sum(int(c) for c in w if c in "12") % 2 == 0

# 2021-22 1(b): begins with a, no aab (≤ 5 states)
D["21_1b"] = DFA(["S", "A", "AA", "B"], "ab", {("S", "a"): "A", ("A", "a"): "AA", ("A", "b"): "B", ("AA", "a"): "AA",
                                             ("B", "a"): "A", ("B", "b"): "B"}, "S", ["A", "AA", "B"], dead="D")
P["21_1b"] = lambda w: w[:1] == "a" and "aab" not in w

# 2022-23 1(c): neither aa nor bb
D["22_1c"] = DFA(["S", "A", "B"], "ab", {("S", "a"): "A", ("S", "b"): "B", ("A", "b"): "B", ("B", "a"): "A"},
                 "S", ["S", "A", "B"], dead="D")
P["22_1c"] = lambda w: "aa" not in w and "bb" not in w

# 2023-24 2(b): awa
D["23_2b"] = DFA(["S", "P", "Q"], "ab", {("S", "a"): "P", ("P", "a"): "Q", ("P", "b"): "P", ("Q", "a"): "Q",
                                       ("Q", "b"): "P"}, "S", ["Q"], dead="D")
P["23_2b"] = lambda w: len(w) >= 2 and w[0] == "a" and w[-1] == "a"

# 2022-23 3(a): no run of 0s of even length >= 2
D["22_3a"] = DFA(["N", "O", "E"], "01", {("N", "0"): "O", ("N", "1"): "N", ("O", "0"): "E", ("O", "1"): "N",
                                       ("E", "0"): "O"}, "N", ["N", "O"], dead="D")
P["22_3a"] = lambda w: all(len(r) % 2 == 1 for r in re.findall(r"0+", w))


# 2023-24 1(b): at most two runs of a's of length exactly three
def build_runs():
    st, dl, acc = [], {}, []
    for k in range(3):
        for c in range(5):  # c = current a-run length, 4 means ≥4
            q = f"{k},{c}"
            st.append(q)
            dl[(q, "a")] = f"{k},{min(c + 1, 4)}"
            k2 = k + (1 if c == 3 else 0)
            dl[(q, "b")] = f"{k2},0" if k2 <= 2 else "D"
            if k + (1 if c == 3 else 0) <= 2:
                acc.append(q)
    return DFA(st, "ab", dl, "0,0", acc, dead="D")


D["23_1b"] = build_runs()
P["23_1b"] = lambda w: sum(1 for r in re.findall(r"a+", w) if len(r) == 3) <= 2

# 2022-23 2(a) given automata (reading)
D["22_2a_i"] = DFA(["S", "T", "R"], "ab", {("S", "a"): "T", ("T", "b"): "S", ("T", "a"): "R"}, "S", ["T"], dead="D")
P["22_2a_i"] = lambda w: re.fullmatch(r"(ab)*a", w) is not None
D["22_2a_ii"] = DFA(["S", "A", "F1", "F2"], "ab", {("S", "a"): "A", ("A", "a"): "A", ("A", "b"): "F1", ("S", "b"): "F2"},
                    "S", ["F1", "F2"], dead="D")
P["22_2a_ii"] = lambda w: re.fullmatch(r"a*b", w) is not None
D["22_2a_iii"] = DFA(["S", "M", "R"], "ab", {("S", "a"): "M", ("M", "b"): "S", ("M", "a"): "R", ("R", "b"): "M"},
                     "S", ["S"], dead="D")


def depth2(w):
    d = 0
    for c in w:
        d += 1 if c == "a" else -1
        if d < 0 or d > 2:
            return False
    return d == 0


P["22_2a_iii"] = depth2
D["22_2a_iv"] = DFA(["C", "L", "R"], "ab", {("C", "b"): "L", ("L", "a"): "C", ("C", "a"): "R", ("R", "b"): "C"},
                    "C", ["C"], dead="D")
P["22_2a_iv"] = lambda w: re.fullmatch(r"(ab|ba)*", w) is not None
D["22_2a_v"] = DFA(["TL", "TM", "ML", "TR", "BL", "BR"], "ab",
                   {("TL", "b"): "TM", ("TL", "a"): "ML", ("TM", "a"): "ML", ("ML", "b"): "TM", ("TM", "b"): "TR",
                    ("TR", "b"): "TR", ("TR", "a"): "BR", ("ML", "a"): "BL", ("BL", "a"): "BL", ("BL", "b"): "BR",
                    ("BR", "a"): "BR", ("BR", "b"): "BR"}, "TL", ["BR"])
P["22_2a_v"] = lambda w: "aab" in w or "bba" in w

# Jan-2020 2(a)
D["20_2a"] = DFA(["q0", "q1", "q2", "q3", "q4"], "01",
                 {("q0", "0"): "q1", ("q0", "1"): "q2", ("q1", "0"): "q3", ("q1", "1"): "q2", ("q2", "0"): "q1",
                  ("q2", "1"): "q4", ("q3", "0"): "q3", ("q3", "1"): "q2", ("q4", "1"): "q4", ("q4", "0"): "q1"},
                 "q0", ["q3", "q4"])
P["20_2a"] = lambda w: len(w) >= 2 and w[-1] == w[-2]

# 2015-16 Q1: F1, F2 (partial, missing → reject)
D["F1"] = DFA(list("abcde"), "01", {("a", "0"): "b", ("b", "0"): "b", ("b", "1"): "c", ("a", "1"): "d", ("d", "0"): "e"},
              "a", ["c", "e"], dead="X")
P["F1"] = lambda w: re.fullmatch(r"0+1|10", w) is not None
D["F2"] = DFA(list("abcde"), "01", {("a", "0"): "b", ("b", "0"): "b", ("b", "1"): "c", ("a", "1"): "d", ("d", "0"): "e",
                                    ("d", "1"): "d"}, "a", ["c", "e"], dead="X")
P["F2"] = lambda w: re.fullmatch(r"0+1|1+0", w) is not None


def xustaeter(N):
    """States (r,g,b), r+g+b=N. Returns dict state -> class (must / cant / might / failed)."""
    S = [(r, g, N - r - g) for r in range(N + 1) for g in range(N + 1 - r)]

    def succ(s):
        r, g, b = s
        out = []
        if g and b: out.append((r + 2, g - 1, b - 1))
        if r and b: out.append((r - 1, g + 2, b - 1))
        if r and g: out.append((r - 1, g - 1, b + 2))
        return out
    fail = {s for s in S if sorted(s) == [0, 0, N]}
    can = set(fail)  # can reach failure
    ch = True
    while ch:
        ch = False
        for s in S:
            if s not in can and any(t in can for t in succ(s)):
                can.add(s); ch = True
    must = set(fail)
    ch = True
    while ch:
        ch = False
        for s in S:
            if s not in must and succ(s) and all(t in must for t in succ(s)):
                must.add(s); ch = True
    cls = {}
    for s in S:
        cls[s] = "failed" if s in fail else "must-fail" if s in must else "might-fail" if s in can else "can't-fail"
    return S, succ, cls


if __name__ == "__main__":
    ok = True
    for k in D:
        if k in P:
            ok &= check(D[k], P[k], maxlen=9 if len(D[k].sigma) <= 2 else 6, label=k)
    ok &= all(bool(re.fullmatch(RE_10_4, w)) == ("110" not in w) for w in strings("01", 12))
    print("RE (0|10)*1* for 'no 110':", ok)
    print("min states 23_1b:", D["23_1b"].minimize_count(), "of", len(D["23_1b"].states))
    print("min states mod4:", D["mod4"].minimize_count())
    for N in (3, 4, 6):
        S, succ, cls = xustaeter(N)
        print("N=", N)
        for s in S:
            print("   ", s, cls[s], "->", succ(s))
    print("ALL OK" if ok else "SOMETHING FAILED")
