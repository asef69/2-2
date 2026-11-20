"""Checks for the 2024-25 CSE 211 term-final solutions (CSE211_2024-25_Final_Solutions.tex)."""
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

def run_pda(delta, start, z0, finals, w, accept="final"):
    """delta: dict (state, input-or-'', top) -> list of (state, push string, leftmost = new top)."""
    seen, todo = set(), [(start, 0, z0)]
    while todo:
        cfg = todo.pop()
        if cfg in seen: continue
        seen.add(cfg)
        q, i, st = cfg
        if i == len(w) and ((accept == "final" and q in finals) or (accept == "empty" and st == "")): return True
        if len(st) > 2 * len(w) + 6: continue
        if not st: continue
        top, rest = st[0], st[1:]
        for (p, push) in delta.get((q, "", top), []): todo.append((p, i, push + rest))
        if i < len(w):
            for (p, push) in delta.get((q, w[i], top), []): todo.append((p, i + 1, push + rest))
    return False

# Q1: PDA (final state) for a^i b^j c^k, j = i + k
D1 = {("q0", "a", "Z"): [("q0", "XZ")], ("q0", "a", "X"): [("q0", "XX")],
      ("q0", "b", "X"): [("q1", "")], ("q0", "b", "Z"): [("q1", "YZ")], ("q0", "", "Z"): [("qf", "Z")],
      ("q1", "b", "X"): [("q1", "")], ("q1", "b", "Z"): [("q1", "YZ")], ("q1", "b", "Y"): [("q1", "YY")],
      ("q1", "c", "Y"): [("q2", "")], ("q1", "", "Z"): [("qf", "Z")],
      ("q2", "c", "Y"): [("q2", "")], ("q2", "", "Z"): [("qf", "Z")]}
inL1 = lambda w: bool(re.fullmatch(r"a*b*c*", w)) and w.count("b") == w.count("a") + w.count("c")
check("Q1 PDA a^i b^j c^k, j=i+k (len<=10)", all(run_pda(D1, "q0", "Z", {"qf"}, w) == inL1(w) for w in words("abc", 10)))

# Q2: CFG -> PDA (empty stack) and -> final state; compare with grammar generation
G = {"E": ["E+T", "T"], "T": ["T*F", "F"], "F": ["(E)", "I"], "I": ["a", "b"]}
def gen(rules, start, maxlen):
    out, frontier, seen = set(), {start}, set()
    while frontier:
        nxt = set()
        for f in frontier:
            i = next((k for k, ch in enumerate(f) if ch in rules), -1)
            if i < 0: out.add(f); continue
            for r in rules[f[i]]:
                g = f[:i] + r + f[i + 1:]
                if sum(ch not in rules for ch in g) <= maxlen and len(g) <= 2 * maxlen + 2 and g not in seen:
                    seen.add(g); nxt.add(g)
        frontier = nxt
    return out
LG = gen(G, "E", 5)
D2 = {("q", "", A): [("q", r) for r in rs] for A, rs in G.items()}
for t in "ab+*()": D2[("q", t, t)] = [("q", "")]
D2f = dict(D2)
D2f[("p0", "", "X")] = [("q", "EX")]
D2f[("q", "", "X")] = [("pf", "")]
cand = [w for w in words("ab+*()", 5)]
check("Q2(a) PDA by empty stack = L(G) (len<=5)", all(run_pda(D2, "q", "E", set(), w, "empty") == (w in LG) for w in cand))
check("Q2(b) PDA by final state = L(G) (len<=5)", all(run_pda(D2f, "p0", "X", {"pf"}, w) == (w in LG) for w in cand))

# Q4: TM 2's complement of w (LSB leftmost), tape wc -> wc<result>
def tm2c(w):
    tape = dict(enumerate(w + "c")); pos, st = 0, "s0"
    for _ in range(100000):
        s = tape.get(pos, "B")
        if st in ("s0", "s1"):
            f = st[1]
            if s in "XY": pos += 1
            elif s in "01":
                tape[pos] = "X" if s == "0" else "Y"
                if f == "0": o, nf = s, ("1" if s == "1" else "0")
                else: o, nf = ("1" if s == "0" else "0"), "1"
                st = "w" + nf + o; pos += 1
            elif s == "c": st = "l"; pos -= 1
        elif st[0] == "w":
            if s in "01": pos += 1
            elif s == "c": st = "u" + st[1:]; pos += 1
        elif st[0] == "u":
            if s in "01": pos += 1
            elif s == "B": tape[pos] = st[2]; st = "k" + st[1]; pos -= 1
        elif st[0] == "k":
            if s == "B": st = "s" + st[1]; pos += 1
            else: pos -= 1
        elif st == "l":
            if s == "B": st = "r"; pos += 1
            else: pos -= 1
        elif st == "r":
            if s == "X": tape[pos] = "0"; pos += 1
            elif s == "Y": tape[pos] = "1"; pos += 1
            elif s in "01c": pos += 1
            elif s == "B": return "".join(tape[i] for i in sorted(tape) if tape[i] != "B")
    return None
good = True
for n in range(1, 8):
    for t in itertools.product("01", repeat=n):
        w = "".join(t); v = sum(int(b) << i for i, b in enumerate(w))
        c = (-v) % (1 << n); exp = "".join(str((c >> i) & 1) for i in range(n))
        good &= tm2c(w) == w + "c" + exp
check("Q4 TM 2's complement, all w of length 1..7", good)
check("Q4 trace 0110c -> 0110c0101", tm2c("0110") == "0110c0101")

# Q10(b): DFA, 3rd symbol from right is 0, |w|>=3; states = last three bits, start 111
def dfa3(w):
    s = "111"
    for ch in w: s = s[1:] + ch
    return s[0] == "0"
check("Q10(b) 8-state DFA (len<=12)", all(dfa3(w) == (len(w) >= 3 and w[-3] == "0") for w in words("01", 12)))
# minimality: the 8 states are pairwise distinguishable
sts = ["".join(t) for t in itertools.product("01", repeat=3)]
def acc_from(s, w):
    for ch in w: s = s[1:] + ch
    return s[0] == "0"
check("Q10(b) all 8 states distinguishable", all(any(acc_from(x, w) != acc_from(y, w) for w in words("01", 3)) for x, y in itertools.combinations(sts, 2)))

# Q10(c): S -> aSc | aBc, B -> bB | b
L10 = gen({"S": ["aSc", "aBc"], "B": ["bB", "b"]}, "S", 11)
check("Q10(c) CFG a^n b^m c^n, n,m>=1 (len<=11)",
      L10 == {w for w in words("abc", 11) if re.fullmatch(r"(a+)(b+)(c+)", w) and w.count("a") == w.count("c")})

# Q11(b): NFA even number of 0s OR exactly two 1s
def nfa11(w):
    A = {"e"}; B = {"c0"}
    for ch in w:
        A = {({"e": "o", "o": "e"}[s] if ch == "0" else s) for s in A}
        B = {({"c0": "c1", "c1": "c2"}[s] if ch == "1" else s) for s in B if not (ch == "1" and s == "c2")}
    return "e" in A or "c2" in B
check("Q11(b) NFA (len<=12)", all(nfa11(w) == (w.count("0") % 2 == 0 or w.count("1") == 2) for w in words("01", 12)))
check("Q11(b) 00101 accepted", nfa11("00101"))

# Q12(c): S -> aScS | bScS | cSaS | cSbS | eps generates n_a + n_b = n_c
L12 = gen({"S": ["aScS", "bScS", "cSaS", "cSbS", ""]}, "S", 8)
check("Q12(c) CFG n_a+n_b=n_c (len<=8)", L12 == {w for w in words("abc", 8) if w.count("a") + w.count("b") == w.count("c")})

# Q13(c): Thompson-style eps-NFA for (ab*c U ac)*
T = {("n1", "a"): {"n2"}, ("n4", "b"): {"n5"}, ("n6", "c"): {"n7"}, ("n8", "a"): {"n9"}, ("n10", "c"): {"n11"}}
E = {"S": {"n0"}, "n0": {"n1", "n8"}, "n2": {"n3"}, "n3": {"n4", "n6"}, "n5": {"n4", "n6"}, "n9": {"n10"},
     "n7": {"n0"}, "n11": {"n0"}}
F = {"S", "n7", "n11"}
def clo(S):
    S = set(S); st = list(S)
    while st:
        q = st.pop()
        for r in E.get(q, ()):
            if r not in S: S.add(r); st.append(r)
    return S
def nfa13(w):
    S = clo({"S"})
    for ch in w: S = clo(set().union(*[T.get((q, ch), set()) for q in S]))
    return bool(S & F)
check("Q13(c) Thompson NFA = (ab*c|ac)* (len<=10)", all(nfa13(w) == bool(re.fullmatch(r"(ab*c|ac)*", w)) for w in words("abc", 10)))

print("ALL OK" if ok else "SOME FAILED")
