"""Verification for the undecidability + complexity notes: TM encoding, shortlex enumeration, countability,
3-SAT → 3-colouring, IS → Clique, Clique → subgraph isomorphism, Subset Sum → Partition, DFA decidability."""
import os, sys, itertools, random, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")


def enc_tm(rules):
    """rules: list of (i, j, k, l, m) meaning δ(q_i, X_j) = (q_k, X_l, D_m); returns code string."""
    parts = ["0" * i + "1" + "0" * j + "1" + "0" * k + "1" + "0" * l + "1" + "0" * m for (i, j, k, l, m) in rules]
    return "11".join(parts)


def nth_string(i):
    """i-th binary string: write i in binary, drop the leading 1 (ε is the 1st)."""
    return bin(i)[3:]


def index_of(w):
    return int("1" + w, 2)


# ---- 3-SAT → 3-COLOURING (palette T,F,B; variable nodes; OR gadget per clause)
def sat_to_3col(nvars, clauses):
    E, nodes = set(), set()

    def edge(a, b):
        E.add(frozenset((a, b))); nodes.update((a, b))
    edge("T", "F"); edge("F", "B"); edge("B", "T")
    for v in range(1, nvars + 1):
        edge(f"x{v}", f"~x{v}"); edge(f"x{v}", "B"); edge(f"~x{v}", "B")

    def lit(l):
        return f"x{l}" if l > 0 else f"~x{-l}"
    for ci, cl in enumerate(clauses, 1):
        a, b, c = (lit(l) for l in cl)
        # OR gadget of a,b then (ab) with c
        g1, g2, g3 = f"c{ci}a", f"c{ci}b", f"c{ci}o1"
        edge(a, g1); edge(b, g2); edge(g1, g2); edge(g1, g3); edge(g2, g3)
        h1, h2, h3 = f"c{ci}c", f"c{ci}d", f"c{ci}o2"
        edge(g3, h1); edge(c, h2); edge(h1, h2); edge(h1, h3); edge(h2, h3)
        edge(h3, "F"); edge(h3, "B")
    return sorted(nodes), E


def three_colorable(nodes, E):
    adj = {v: set() for v in nodes}
    for e in E:
        a, b = tuple(e)
        adj[a].add(b); adj[b].add(a)
    order = sorted(nodes, key=lambda v: -len(adj[v]))
    col = {}

    def go(i):
        if i == len(order):
            return True
        v = order[i]
        for c in range(3):
            if all(col.get(u) != c for u in adj[v]):
                col[v] = c
                if go(i + 1):
                    return True
                del col[v]
        return False
    return go(0)


def satisfiable(nvars, clauses):
    return any(all(any((a[abs(l) - 1] if l > 0 else not a[abs(l) - 1]) for l in cl) for cl in clauses)
               for a in itertools.product([False, True], repeat=nvars))


def check_sat_col(trials=60):
    random.seed(7)
    bad = 0
    for _ in range(trials):
        nv = random.randint(2, 3)
        cls = [tuple(random.choice([-1, 1]) * random.randint(1, nv) for _ in range(3)) for _ in range(random.randint(1, 4))]
        nodes, E = sat_to_3col(nv, cls)
        if three_colorable(nodes, E) != satisfiable(nv, cls):
            bad += 1
    # force an unsatisfiable formula over 2 variables: all 4 two-literal combos as 3-literal clauses (repeating literals)
    uns = [(1, 2, 2), (1, -2, -2), (-1, 2, 2), (-1, -2, -2)]
    nodes, E = sat_to_3col(2, uns)
    return bad, three_colorable(nodes, E), satisfiable(2, uns)


# ---- Clique / independent set / subgraph isomorphism
def has_clique(V, E, k):
    return any(all(frozenset((a, b)) in E for a, b in itertools.combinations(S, 2)) for S in itertools.combinations(V, k))


def has_is(V, E, k):
    return any(all(frozenset((a, b)) not in E for a, b in itertools.combinations(S, 2)) for S in itertools.combinations(V, k))


def complement(V, E):
    return {frozenset(p) for p in itertools.combinations(V, 2) if frozenset(p) not in E}


def has_subgraph(V1, E1, V2, E2):
    n2 = len(V2)
    for S in itertools.permutations(V1, n2):
        if all(frozenset((S[V2.index(a)], S[V2.index(b)])) in E1 for a, b in (tuple(e) for e in E2)):
            return True
    return False


def check_graphs():
    random.seed(3)
    bad = 0
    for _ in range(40):
        n = random.randint(3, 6)
        V = list(range(n))
        E = {frozenset(p) for p in itertools.combinations(V, 2) if random.random() < 0.5}
        for k in range(1, n + 1):
            if has_is(V, E, k) != has_clique(V, complement(V, E), k):
                bad += 1
            K = list(range(k))
            Ek = {frozenset(p) for p in itertools.combinations(K, 2)}
            if has_clique(V, E, k) != has_subgraph(V, E, K, Ek):
                bad += 1
    return bad


def subset_sum(a, t):
    return any(sum(S) == t for r in range(len(a) + 1) for S in itertools.combinations(a, r))


def partition(a):
    s = sum(a)
    return s % 2 == 0 and subset_sum(a, s // 2)


def check_partition():
    random.seed(5)
    bad = 0
    for _ in range(300):
        a = [random.randint(1, 9) for _ in range(random.randint(1, 6))]
        t = random.randint(0, sum(a) + 3)
        A = sum(a)
        extra = abs(2 * t - A)
        if (partition(a + [extra])) != subset_sum(a, t) and 2 * t <= 2 * A:
            bad += 1
    return bad


# ---- decidability constructions
def dfa_accepts(d, w):
    q = d["start"]
    for c in w:
        q = d["delta"][(q, c)]
    return q in d["acc"]


def dfa_empty(d, sigma):
    seen, todo = {d["start"]}, [d["start"]]
    while todo:
        q = todo.pop()
        for c in sigma:
            r = d["delta"][(q, c)]
            if r not in seen:
                seen.add(r); todo.append(r)
    return not (seen & d["acc"])


def connected(n, E):
    seen, todo = {0}, [0]
    adj = {v: set() for v in range(n)}
    for a, b in E:
        adj[a].add(b); adj[b].add(a)
    while todo:
        v = todo.pop()
        for u in adj[v]:
            if u not in seen:
                seen.add(u); todo.append(u)
    return len(seen) == n


if __name__ == "__main__":
    # slides' TM example: δ(q1,1)=(q3,0,R) δ(q3,0)=(q1,1,R) δ(q3,1)=(q2,0,R) δ(q3,B)=(q3,1,L); states q1,q2,q3; 0=X1 1=X2 B=X3; L=D1 R=D2
    code = enc_tm([(1, 2, 3, 1, 2), (3, 1, 1, 2, 2), (3, 2, 2, 1, 2), (3, 3, 3, 2, 1)])
    print("code of M:", code, len(code))
    print("slide code ok:", code == "01001000101001100010101001001100010010010100110001000100010010")
    print("13th string:", nth_string(13), "index of 101:", index_of("101"), [nth_string(i) or "ε" for i in range(1, 9)])
    print("sat→3col:", check_sat_col())
    print("graph reductions bad:", check_graphs())
    print("partition bad:", check_partition())
    nodes, E = sat_to_3col(4, [(1, -2, -3), (1, 3, 4)])
    print("2017-18 Q1(c) graph:", len(nodes), "nodes", len(E), "edges;",
          "3-colourable:", three_colorable(nodes, E), "satisfiable:", satisfiable(4, [(1, -2, -3), (1, 3, 4)]))
    print(sorted(nodes))
    print("ALL DONE")
