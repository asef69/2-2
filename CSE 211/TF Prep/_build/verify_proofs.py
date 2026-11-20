"""Brute-force checks for the claims in CSE211_Proofs_Exam_Ready.tex that a program can check."""
import itertools, random

ok = True
def check(name, cond):
    global ok
    print(("OK  " if cond else "FAIL"), name)
    ok &= bool(cond)

# 1. 2022-23 Q2(b): L = a^(2+3k) U b^(10+12k); which p are pumping lengths?
def inL(s):
    if s and set(s) == {"a"}: return len(s) >= 2 and (len(s) - 2) % 3 == 0
    if s and set(s) == {"b"}: return len(s) >= 10 and (len(s) - 10) % 12 == 0
    return False
def pumpable(s, p, imax=4):
    for xl in range(0, p):
        for yl in range(1, p - xl + 1):
            if xl + yl > len(s): break
            x, y, z = s[:xl], s[xl:xl + yl], s[xl + yl:]
            if all(inL(x + y * i + z) for i in range(imax + 1)):
                return True
    return False
strings = ["a" * n for n in range(1, 80) if inL("a" * n)] + ["b" * n for n in range(1, 160) if inL("b" * n)]
good = [p for p in range(1, 40) if all(pumpable(s, p) for s in strings if len(s) >= p)]
check("pumping lengths: 3,5,9 fail, 24 works, minimum 12", min(good) == 12 and 24 in good and not {3, 5, 9} & set(good))

# 2. S -> 0S1S | 1S0S | eps generates exactly the equal-count strings (length <= 10)
def gen(maxlen):
    out, frontier = set(), {"S"}
    while frontier:
        nxt = set()
        for f in frontier:
            i = f.find("S")
            if i < 0:
                out.add(f); continue
            for r in ("0S1S", "1S0S", ""):
                g = f[:i] + r + f[i + 1:]
                if len(g.replace("S", "")) <= maxlen:
                    nxt.add(g)
        frontier = nxt
    return out
G = gen(10)
E = {"".join(t) for n in range(0, 11, 2) for t in itertools.product("01", repeat=n) if t.count("0") == t.count("1")}
check("S->0S1S|1S0S|eps = equal 0s and 1s (len<=10)", G == E)

# 3. 3-SAT -> 3-COL gadget: G_phi 3-colourable iff phi satisfiable (all 3-literal formulas, 3 vars, 1-2 clauses)
def build(nv, clauses):
    V, Ed = ["T", "F", "B"], [("T", "F"), ("F", "B"), ("T", "B")]
    lit = lambda l: f"x{abs(l)}" if l > 0 else f"-x{abs(l)}"
    for i in range(1, nv + 1):
        V += [f"x{i}", f"-x{i}"]; Ed += [(f"x{i}", f"-x{i}"), (f"x{i}", "B"), (f"-x{i}", "B")]
    for c, (a, b, d) in enumerate(clauses):
        def OR(u, v, tag):
            p, q, o = f"p{tag}", f"q{tag}", f"o{tag}"
            V.extend([p, q, o]); Ed.extend([(u, p), (v, q), (p, q), (p, o), (q, o)])
            return o
        o1 = OR(lit(a), lit(b), f"{c}a")
        o2 = OR(o1, lit(d), f"{c}b")
        Ed += [(o2, "F"), (o2, "B")]
    return V, Ed
def colourable(V, Ed):
    adj = {v: set() for v in V}
    for u, v in Ed: adj[u].add(v); adj[v].add(u)
    col = {}
    def bt(i):
        if i == len(V): return True
        v = V[i]
        for c in range(3):
            if all(col.get(w) != c for w in adj[v]):
                col[v] = c
                if bt(i + 1): return True
                del col[v]
        return False
    return bt(0)
def sat(nv, clauses):
    return any(all(any((l > 0) == bits[abs(l) - 1] for l in cl) for cl in clauses)
               for bits in itertools.product([False, True], repeat=nv))
lits = [l for v in (1, 2, 3) for l in (v, -v)]
allcl = list(itertools.combinations(lits, 3))
random.seed(1)
cases = [[c] for c in allcl] + [random.sample(allcl, 2) for _ in range(60)] + [[(1, 2, 3), (-1, -2, -3), (1, -2, 3), (-1, 2, -3)]]
check("3-COL reduction correct on %d formulas" % len(cases), all(colourable(*build(3, cl)) == sat(3, cl) for cl in cases))
V, Ed = build(4, [(1, -2, -3), (1, 3, 4)])
check("2017-18 Q1(c) graph: %d vertices, %d edges, 3-colourable" % (len(V), len(Ed)),
      len(V) == 3 + 8 + 12 and len(Ed) == 3 + 12 + 24 and colourable(V, Ed))
unsat = [(a, b, c) for a in (1, -1) for b in (2, -2) for c in (3, -3)]
check("all 8 sign patterns on x1,x2,x3 -> not 3-colourable", not colourable(*build(3, unsat)))

# 4. Subset Sum -> Partition (both cases of the slides)
def subset_sum(a, t):
    return any(sum(c) == t for r in range(len(a) + 1) for c in itertools.combinations(a, r))
def partition(a):
    s = sum(a)
    return s % 2 == 0 and subset_sum(a, s // 2)
good = True
for _ in range(400):
    a = [random.randint(0, 9) for _ in range(random.randint(1, 6))]
    t = random.randint(0, sum(a) + 3)
    tot = sum(a)
    b = a + [2 * t - tot] if 2 * t >= tot else a + [tot - 2 * t]
    good &= subset_sum(a, t) == partition(b)
check("Subset Sum <=p Partition (400 random instances)", good)

# 5. Independent Set -> Clique by complementing (random graphs, 5 vertices)
def has_is(n, E, k, comp=False):
    for S in itertools.combinations(range(n), k):
        if all(((u, v) in E or (v, u) in E) == comp for u, v in itertools.combinations(S, 2)):
            return True
    return False
good = True
for _ in range(200):
    E = {(u, v) for u, v in itertools.combinations(range(5), 2) if random.random() < 0.5}
    Ec = {(u, v) for u, v in itertools.combinations(range(5), 2) if (u, v) not in E}
    k = random.randint(1, 5)
    good &= has_is(5, E, k) == has_is(5, Ec, k, comp=True)
check("Independent Set <=p Clique (200 random graphs)", good)

# 6. Star-construction counterexample: A = a*b, bad NFA accepts 'a' which is not in A*
import re
check("'a' not in (a*b)*, 'ab' in (a*b)*", not re.fullmatch(r"(a*b)*", "a") and re.fullmatch(r"(a*b)*", "ab"))

# 7. a^(n!) : m!+k strictly between m! and (m+1)! for 1<=k<=m, m>=2
from math import factorial
check("m! < m!+k < (m+1)! for 2<=m<=12, 1<=k<=m",
      all(factorial(m) < factorial(m) + k < factorial(m + 1) for m in range(2, 13) for k in range(1, m + 1)))

print("ALL OK" if ok else "SOME FAILED")
