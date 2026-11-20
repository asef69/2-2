"""Brute-force checks for the exam-style worked examples in CSE211_Final_Solving_Guide.tex (version 2)."""
import itertools, re

ok = True
def check(name, cond):
    global ok
    print(("OK  " if cond else "FAIL"), name)
    ok &= bool(cond)

def words(alpha, n):
    for k in range(n + 1):
        for t in itertools.product(alpha, repeat=k):
            yield "".join(t)

# 2021-22 Q1(b): DFA, begins with a, no substring aab, <= 5 states
D = {("q0", "a"): "A", ("q0", "b"): "d", ("A", "a"): "AA", ("A", "b"): "B", ("AA", "a"): "AA", ("AA", "b"): "d",
     ("B", "a"): "A", ("B", "b"): "B", ("d", "a"): "d", ("d", "b"): "d"}
def runD(w):
    s = "q0"
    for c in w: s = D[(s, c)]
    return s in {"A", "AA", "B"}
check("DFA begins-with-a, no aab", all(runD(w) == (w.startswith("a") and "aab" not in w) for w in words("ab", 11)))

# 2021-22 Q3(b): NFA at least two 0s OR exactly two 1s (union of two counters)
def nfa_q3b(w):
    return w.count("0") >= 2 or w.count("1") == 2
def nfa_sim(w):
    # branch 1: a0 -0-> a1 -0-> a2 (a2 loops 0,1), 1 loops on a0,a1 ; branch 2: b0 -1-> b1 -1-> b2, 0 loops, no 1 from b2
    A = {"a0"}
    Bset = {"b0"}
    for c in w:
        A = {({"a0": "a1", "a1": "a2", "a2": "a2"}[s] if c == "0" else s) for s in A}
        Bset = {({"b0": "b1", "b1": "b2"}[s] if c == "1" else s) for s in Bset if not (c == "1" and s == "b2")}
    return "a2" in A or "b2" in Bset
check("NFA >=2 zeros or exactly two 1s", all(nfa_sim(w) == nfa_q3b(w) for w in words("01", 11)))

# 2021-22 Q3(c): eps-NFA q1 -a-> q3, q1 -eps-> q2, q2 -a-> q1, q3 -a-> q2, q3 -b-> {q2,q3}; start q1, accept q2
d = {("q1", "a"): {"q3"}, ("q2", "a"): {"q1"}, ("q3", "a"): {"q2"}, ("q3", "b"): {"q2", "q3"}}
eps = {"q1": {"q2"}}
def E(S):
    S = set(S); st = list(S)
    while st:
        q = st.pop()
        for r in eps.get(q, ()):
            if r not in S: S.add(r); st.append(r)
    return frozenset(S)
def nfa(w):
    S = E({"q1"})
    for c in w:
        S = E(set().union(*[d.get((q, c), set()) for q in S]))
    return "q2" in S
DFA = {("12", "a"): "123", ("12", "b"): "-", ("123", "a"): "123", ("123", "b"): "23", ("23", "a"): "12", ("23", "b"): "23",
       ("-", "a"): "-", ("-", "b"): "-"}
def dfa(w):
    s = "12"
    for c in w: s = DFA[(s, c)]
    return s != "-"
check("eps-NFA 2021-22 Q3(c) -> 4-state DFA", all(nfa(w) == dfa(w) for w in words("ab", 11)))
# check the subset table entries themselves
name = {frozenset({"q1", "q2"}): "12", frozenset({"q1", "q2", "q3"}): "123", frozenset({"q2", "q3"}): "23", frozenset(): "-"}
good = True
for S, nm in name.items():
    for c in "ab":
        T = E(set().union(*[d.get((q, c), set()) for q in S])) if S else frozenset()
        good &= name.get(T) == DFA[(nm, c)]
check("subset table entries", good)

# 2019-20 Q4(b): regular expressions
R1 = r"b*(ab*ab*ab*)*"
R2 = r"b*(a|)b*(a|)b*(a|)b*"
N = r"(b|ab|aab)*"
R3 = N + r"aaa(b" + N + r"(|a|aa))?"
cnt = lambda w: sum(1 for i in range(len(w) - 2) if w[i:i + 3] == "aaa")
check("RE #a divisible by 3", all(bool(re.fullmatch(R1, w)) == (w.count("a") % 3 == 0) for w in words("ab", 11)))
check("RE at most three a's", all(bool(re.fullmatch(R2, w)) == (w.count("a") <= 3) for w in words("ab", 11)))
check("RE exactly one aaa", all(bool(re.fullmatch(R3, w)) == (cnt(w) == 1) for w in words("ab", 12)))

# 2020 Q4(a): (1+e)(00*1)*0* = no two consecutive 1s
check("(1+e)(00*1)*0* = no 11", all(bool(re.fullmatch(r"1?(00*1)*0*", w)) == ("11" not in w) for w in words("01", 12)))
# 2019-20 Q2(b) simplifications
check("(a*b)*U(b*a)* = (a+b)*", all(re.fullmatch(r"(a*b)*", w) or re.fullmatch(r"(b*a)*", w) for w in words("ab", 10)))

# 2021-22 Q2(d): CFG for a^i b^j c^k, i != j+k
def gen(rules, start, maxlen):
    out, frontier, seen = set(), {start}, set()
    while frontier:
        nxt = set()
        for f in frontier:
            i = next((k for k, ch in enumerate(f) if ch.isupper()), -1)
            if i < 0: out.add(f); continue
            for r in rules[f[i]]:
                g = f[:i] + r + f[i + 1:]
                if sum(ch.islower() for ch in g) <= maxlen and g not in seen:
                    seen.add(g); nxt.add(g)
        frontier = nxt
    return out
rules = {"S": ["X", "Y", "W"],
         "X": ["aXc", "P"], "P": ["aPb", "A"], "A": ["aA", "a"],
         "Y": ["aYc", "Q"], "Q": ["aQb", "B"], "B": ["bB", "b"],
         "W": ["aWc", "U"], "U": ["bU", "C"], "C": ["cC", "c"]}
G = gen(rules, "S", 9)
T = {w for w in words("abc", 9) if re.fullmatch(r"a*b*c*", w) and w.count("a") != w.count("b") + w.count("c")}
check("CFG a^i b^j c^k, i != j+k (len<=9)", G == T)

# 2022-23 Q7 CYK on 0100
g = {"S": ["AB", "AY", "YA", "1"], "A": ["ZA", "YA", "0", "1"], "B": ["YA"], "Z": ["0"], "Y": ["1"]}
def cyk(w):
    n = len(w); X = {}
    for i in range(n): X[(i, i)] = {A for A, rs in g.items() if w[i] in rs}
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1; X[(i, j)] = set()
            for k in range(i, j):
                for A, rs in g.items():
                    for r in rs:
                        if len(r) == 2 and r[0] in X[(i, k)] and r[1] in X[(k + 1, j)]: X[(i, j)].add(A)
    return X
X = cyk("0100")
exp = {(0, 0): {"A", "Z"}, (1, 1): {"A", "S", "Y"}, (2, 2): {"A", "Z"}, (3, 3): {"A", "Z"},
       (0, 1): {"A", "S"}, (1, 2): {"A", "B", "S"}, (2, 3): {"A"},
       (0, 2): {"A", "S"}, (1, 3): {"A", "B", "S"}, (0, 3): {"A", "S"}}
check("CYK table 0100 (2022-23 Q7)", all(X[k] == v for k, v in exp.items()))
check("L(G) = strings with at least one 1 (len 1..7)", all(("S" in cyk(w)[(0, len(w) - 1)]) == ("1" in w) for w in words("01", 7) if w))

# 2023-24 Q8 PDA a^n b^m c^m d^n, n,m >= 1 (final state)
P = {("q0", "a", "Z"): ("q1", "AZ"), ("q1", "a", "A"): ("q1", "AA"), ("q1", "b", "A"): ("q2", "BA"), ("q2", "b", "B"): ("q2", "BB"),
     ("q2", "c", "B"): ("q3", ""), ("q3", "c", "B"): ("q3", ""), ("q3", "d", "A"): ("q4", ""), ("q4", "d", "A"): ("q4", "")}
def pda(w):
    st, stack = "q0", "Z"
    for ch in w:
        key = (st, ch, stack[0] if stack else None)
        if key not in P: return False
        st, push = P[key]; stack = push + stack[1:]
    return st == "q4" and stack == "Z"   # eps, Z/Z -> q5
def inL(w):
    m = re.fullmatch(r"(a+)(b+)(c+)(d+)", w)
    return bool(m) and len(m.group(1)) == len(m.group(4)) and len(m.group(2)) == len(m.group(3))
check("PDA a^n b^m c^m d^n", all(pda(w) == inL(w) for w in words("abcd", 9)))

# 2019-20 Q9: TM computing AND of w1 c w2 c (generic bitwise op)
def tm(w1, w2, op):
    tape = dict(enumerate(w1 + "c" + w2 + "c")); pos, st = 0, "q0"
    steps = 0
    while st != "h":
        steps += 1
        if steps > 10000: return None
        s = tape.get(pos, "B")
        if st == "q0":
            if s in "XY": pos += 1
            elif s in "01": tape[pos] = "X" if s == "0" else "Y"; st = "p" + s; pos += 1
            elif s == "c": st = "l"; pos -= 1
            else: return None
        elif st[0] == "p":                       # carry bit of w1, go to w2
            if s in "01": pos += 1
            elif s == "c": st = "s" + st[1]; pos += 1
            else: return None
        elif st[0] == "s":                       # find first unmarked bit of w2
            if s in "XY": pos += 1
            elif s in "01": tape[pos] = "X" if s == "0" else "Y"; st = "t" + str(op(int(st[1]), int(s))); pos += 1
            else: return None
        elif st[0] == "t":                       # go past second c
            if s in "01": pos += 1
            elif s == "c": st = "u" + st[1]; pos += 1
            else: return None
        elif st[0] == "u":                       # past result bits, write
            if s in "01": pos += 1
            elif s == "B": tape[pos] = st[1]; st = "b"; pos -= 1
        elif st == "b":                          # back to left end
            if s == "B": st = "q0"; pos += 1
            else: pos -= 1
        elif st == "l":                          # done: go to left end, then restore
            if s == "B": st = "r"; pos += 1
            else: pos -= 1
        elif st == "r":
            if s == "X": tape[pos] = "0"; pos += 1
            elif s == "Y": tape[pos] = "1"; pos += 1
            elif s in "01c": pos += 1
            elif s == "B": st = "h"
    return "".join(tape[i] for i in sorted(tape) if tape[i] != "B")
good = True
for n in range(1, 6):
    for a in words("01", n):
        if len(a) != n: continue
        for b in itertools.product("01", repeat=n):
            b = "".join(b)
            exp_ = a + "c" + b + "c" + "".join(str(int(x) & int(y)) for x, y in zip(a, b))
            good &= tm(a, b, lambda x, y: x & y) == exp_
check("TM AND of w1cw2c (all equal-length pairs, length 1..5)", good)
check("TM trace example 101c110c -> 100", tm("101", "110", lambda x, y: x & y) == "101c110c100")

# quick CFG answers (2022-23 Q5, 2020 Q5, 2019-20 Q5, 2017-18 Q5); lower-case letters only as terminals -> map 0/1 to x/y, (/) to l/r
def bal(w):
    d = 0
    for ch in w:
        d += 1 if ch == "l" else -1
        if d < 0: return False
    return d == 0
g1 = gen({"S": ["AyAyA"], "A": ["xA", "yA", ""]}, "S", 8)
check("S->A1A1A: at least two 1s", g1 == {w for w in words("xy", 8) if w.count("y") >= 2})
g2 = gen({"S": ["AxAyA", "AyAxA"], "A": ["xA", "yA", ""]}, "S", 8)
check("S->A0A1A|A1A0A: at least one 0 and one 1", g2 == {w for w in words("xy", 8) if "x" in w and "y" in w})
g3 = gen({"S": ["lSrS", ""]}, "S", 10)
check("S->(S)S|e: balanced parentheses", g3 == {w for w in words("lr", 10) if bal(w)})

print("ALL OK" if ok else "SOME FAILED")
