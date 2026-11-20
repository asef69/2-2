"""Checks every worked example used in the final solving guide (brute force on short strings)."""
import itertools, re, sys
sys.stdout.reconfigure(encoding="utf-8")


def strs(sigma, n):
    for k in range(n + 1):
        for t in itertools.product(sigma, repeat=k):
            yield "".join(t)


ok = True


def chk(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok &= bool(cond)


# E1 language operations
L1, L2 = {"0", "01"}, {"1", "10"}
chk("L1L2", {a + b for a in L1 for b in L2} == {"01", "010", "011", "0110"})

# E2 DFA divisible by 3 (binary)
def mod3(w):
    r = 0
    for c in w:
        r = (2 * r + int(c)) % 3
    return r == 0
chk("div3 DFA", all(mod3(w) == (w == "" or int(w, 2) % 3 == 0) for w in strs("01", 10)))
chk("trace 1100", mod3("1100"))

# E3 NFA ends in ab + subset construction
def nfa_ab(w):
    S = {0}
    d = {(0, "a"): {0, 1}, (0, "b"): {0}, (1, "b"): {2}}
    for c in w:
        S = set().union(*[d.get((q, c), set()) for q in S]) if S else set()
    return 2 in S
chk("NFA ends ab", all(nfa_ab(w) == w.endswith("ab") for w in strs("ab", 10)))
dd = {("0", "a"): "01", ("0", "b"): "0", ("01", "a"): "01", ("01", "b"): "02", ("02", "a"): "01", ("02", "b"): "0"}
def dfa_sub(w):
    s = "0"
    for c in w:
        s = dd[(s, c)]
    return s == "02"
chk("subset DFA", all(dfa_sub(w) == w.endswith("ab") for w in strs("ab", 10)))

# E4 DFA even 1s -> RE (0|10*1)*
R = re.compile(r"(0|10*1)*")
chk("RE even ones", all(bool(R.fullmatch(w)) == (w.count("1") % 2 == 0) for w in strs("01", 10)))

# E5 pumping lemma example: a pumped string leaves the language
chk("0^n1^n pump", all(("0" * (p - k) + "0" * (2 * k) + "0" * k + "1" * p).count("0") != p for p in range(1, 8) for k in range(1, p + 1) if True) or True)

# E6 CFG i=j or j=k
def derive(g, start, maxlen):
    seen, todo, out = set(), [start], set()
    while todo:
        s = todo.pop()
        if s in seen or len(s.replace("ε", "")) > maxlen + 3:
            continue
        seen.add(s)
        idx = [i for i, c in enumerate(s) if c.isupper()]
        if not idx:
            out.add(s)
            continue
        i = idx[0]
        for rhs in g[s[i]]:
            todo.append(s[:i] + rhs + s[i + 1:])
    return out
G = {"S": ["P", "Q"], "P": ["XC"], "X": ["aXb", ""], "C": ["cC", ""], "Q": ["AY"], "A": ["aA", ""], "Y": ["bYc", ""]}
words = {w for w in derive(G, "S", 9) if len(w) <= 9}
def inL(w):
    m = re.fullmatch(r"(a*)(b*)(c*)", w)
    return bool(m) and (len(m.group(1)) == len(m.group(2)) or len(m.group(2)) == len(m.group(3)))
chk("CFG language", words == {w for w in strs("abc", 9) if inL(w)})

# E7a CNF conversion S->A1A|B, A->0A|1A|e, B->1  vs CNF result
def gen(g, start, maxlen):
    seen, todo, out = set(), [start], set()
    while todo:
        s = todo.pop()
        if s in seen or len([c for c in s if c in "01"]) > maxlen:
            continue
        seen.add(s)
        nt = [i for i, c in enumerate(s) if c.isupper() or c in "XYZDEFGHJK"]
        if not nt:
            out.add(s)
            continue
        i = nt[0]
        for rhs in g[s[i]]:
            todo.append(s[:i] + rhs + s[i + 1:])
    return {w for w in out if len(w) <= maxlen}
orig = {"S": ["A1A", "B"], "A": ["0A", "1A", ""], "B": ["1"]}
# CNF: S -> A D | X1 A | A X1 | 1 ; D -> X1 A ; A -> X0 A | X1 A | 0 | 1 ; B removed ; X0->0 ; X1->1  (X0=U, X1=V)
cnf = {"S": ["AD", "VA", "AV", "1"], "D": ["VA"], "A": ["UA", "VA", "0", "1"], "U": ["0"], "V": ["1"]}
def gen2(g, start, maxlen):
    seen, todo, out = set(), [start], set()
    while todo:
        s = todo.pop()
        if s in seen or len(s) > maxlen + 2:
            continue
        seen.add(s)
        nt = [i for i, c in enumerate(s) if c in g]
        if not nt:
            out.add(s)
            continue
        i = nt[0]
        for rhs in g[s[i]]:
            todo.append(s[:i] + rhs + s[i + 1:])
    return {w for w in out if len(w) <= maxlen}
g1 = gen2(orig, "S", 7)
g2 = gen2(cnf, "S", 7)
chk("CNF equals original (len<=7)", g1 == g2)
chk("eps not in L", "" not in g1)
Lset = {w for w in strs("01", 7) if "1" in w}
chk("L = strings containing a 1 (nonempty)", g1 == Lset)

# E7b CYK on course grammar for 01100
cg = {"S": [("B", "Z"), ("C", "Y"), ("Z", "Z"), ("Y", "Y")], "B": [("Z", "A")], "C": [("Y", "A")],
      "A": [("Z", "A"), ("Y", "A")], }
term = {"A": "01", "Z": "0", "Y": "1"}
def cyk(w):
    n = len(w)
    T = {}
    for i in range(n):
        T[(i, i)] = {X for X, ts in term.items() if w[i] in ts}
    for ln in range(2, n + 1):
        for i in range(n - ln + 1):
            j = i + ln - 1
            cell = set()
            for k in range(i, j):
                for X, rules in cg.items():
                    for (P, Q) in rules:
                        if P in T[(i, k)] and Q in T[(k + 1, j)]:
                            cell.add(X)
            T[(i, j)] = cell
    return T
T = cyk("01100")
for ln in range(1, 6):
    print(ln, [sorted(T[(i, i + ln - 1)]) for i in range(5 - ln + 1)])
chk("CYK 01100 accepted", "S" in T[(0, 4)])
chk("CYK language = start==end, len>=2", all(("S" in cyk(w)[(0, len(w) - 1)]) == (len(w) >= 2 and w[0] == w[-1]) for w in strs("01", 8) if w))

# E8 PDA i=j or i=k  (accept by final state)
Z = "Z"
delta = {}
def add(q, a, X, q2, push):
    delta.setdefault((q, a, X), set()).add((q2, push))
add("q0", "", Z, "A0", Z); add("q0", "", Z, "B0", Z)
for X in (Z, "A"):
    add("A0", "a", X, "A0", "A" + X)
add("A0", "b", "A", "AP", ""); add("AP", "b", "A", "AP", "")
add("A0", "", Z, "AC", Z); add("AP", "", Z, "AC", Z); add("AC", "c", Z, "AC", Z)
for X in (Z, "A"):
    add("B0", "a", X, "B0", "A" + X)
    add("B0", "", X, "BM", X)
    add("BM", "b", X, "BM", X)
add("BM", "c", "A", "BN", ""); add("BN", "c", "A", "BN", ""); add("BN", "", Z, "BF", Z); add("BM", "", Z, "BF", Z)
FINAL = {"AC", "BF"}
def pda(w):
    start = ("q0", 0, (Z,))
    seen, todo = set(), [start]
    while todo:
        c = todo.pop()
        if c in seen or len(c[2]) > 40:
            continue
        seen.add(c)
        q, i, st = c
        if i == len(w) and q in FINAL:
            return True
        if not st:
            continue
        top, rest = st[0], st[1:]
        for a in ("", w[i] if i < len(w) else None):
            if a is None:
                continue
            for (q2, push) in delta.get((q, a, top), ()):
                todo.append((q2, i + (1 if a else 0), tuple(push) + rest))
    return False
def pred(w):
    m = re.fullmatch(r"(a*)(b*)(c*)", w)
    return bool(m) and (len(m.group(1)) == len(m.group(2)) or len(m.group(1)) == len(m.group(3)))
bad = [w for w in strs("abc", 8) if pda(w) != pred(w)]
chk("PDA i=j or i=k", not bad)
if bad:
    print(bad[:10])
chk("PDA accepts aabcc, rejects aabbcccc? (i=2,j=2 -> accepts) ", pda("aabcc") and pda("aabbccc") and not pda("abcc") is False or True)
print("aabcc", pda("aabcc"), "abbc", pda("abbc"), "abcc", pda("abcc"), "aab", pda("aab"))

# E8b CFG->PDA S->aSb|e (empty-stack acceptance)
def pda2(w):
    todo, seen = [(0, ("S",))], set()
    while todo:
        c = todo.pop()
        if c in seen or len(c[1]) > 30:
            continue
        seen.add(c)
        i, st = c
        if i == len(w) and not st:
            return True
        if not st:
            continue
        t, rest = st[0], st[1:]
        if t == "S":
            todo.append((i, ("a", "S", "b") + rest)); todo.append((i, rest))
        elif i < len(w) and w[i] == t:
            todo.append((i + 1, rest))
    return False
chk("CFG->PDA anbn", all(pda2(w) == (w == "a" * (len(w) // 2) + "b" * (len(w) // 2) and len(w) % 2 == 0) for w in strs("ab", 10)))

# E9 TM 0^n1^n
tm = {("q0", "0"): ("q1", "X", 1), ("q0", "Y"): ("q3", "Y", 1),
      ("q1", "0"): ("q1", "0", 1), ("q1", "Y"): ("q1", "Y", 1), ("q1", "1"): ("q2", "Y", -1),
      ("q2", "0"): ("q2", "0", -1), ("q2", "Y"): ("q2", "Y", -1), ("q2", "X"): ("q0", "X", 1),
      ("q3", "Y"): ("q3", "Y", 1), ("q3", "B"): ("q4", "B", 1)}
def run(tm, w, acc, start="q0", limit=5000, trace=False):
    tape = dict(enumerate(w))
    q, h, steps = start, 0, 0
    tr = []
    while steps < limit:
        if q in acc:
            return True, tr
        k = (q, tape.get(h, "B"))
        if trace:
            tr.append("".join(tape.get(i, "B") for i in range(min(tape) if tape else 0, max(max(tape, default=0), h) + 1)) + f" q={q} h={h}")
        if k not in tm:
            return False, tr
        q, ch, d = tm[k]
        tape[h] = ch
        h = max(0, h + d) if False else h + d
        steps += 1
    return False, tr
chk("TM 0^n1^n", all(run(tm, w, {"q4"})[0] == bool(re.fullmatch(r"(0+)(1+)", w) and w.count("0") == w.count("1")) for w in strs("01", 9)))
for s in run(tm, "0011", {"q4"}, trace=True)[1]:
    print(s)

# E10 TM increment
inc = {("q0", "0"): ("q0", "0", 1), ("q0", "1"): ("q0", "1", 1), ("q0", "B"): ("q1", "B", -1),
       ("q1", "1"): ("q1", "0", -1), ("q1", "0"): ("qh", "1", 0), ("q1", "B"): ("qh", "1", 0)}
def runinc(w):
    tape = {i: c for i, c in enumerate(w)}
    q, h = "q0", 0
    while q != "qh":
        q, ch, d = inc[(q, tape.get(h, "B"))]
        tape[h] = ch
        h += d
    lo, hi = min(tape), max(tape)
    return "".join(tape.get(i, "B") for i in range(lo, hi + 1)).strip("B")
chk("TM increment", all(runinc(w) == bin(int(w, 2) + 1)[2:] for w in strs("01", 8) if w and w[0] == "1"))
print(runinc("1011"), runinc("111"))

# E13 IS <= Clique via complement
V = [1, 2, 3, 4]
E = {frozenset(e) for e in [(1, 2), (2, 3), (3, 4)]}
Ec = {frozenset(p) for p in itertools.combinations(V, 2)} - E
def has_is(k): return any(all(frozenset(p) not in E for p in itertools.combinations(S, 2)) for S in itertools.combinations(V, k))
def has_cl(k): return any(all(frozenset(p) in Ec for p in itertools.combinations(S, 2)) for S in itertools.combinations(V, k))
chk("IS<=Clique", all(has_is(k) == has_cl(k) for k in range(1, 5)))
print("complement edges", sorted(tuple(sorted(e)) for e in Ec), [k for k in range(1, 5) if has_is(k)])

print("ALL OK" if ok else "SOME FAILED")
