"""CYK tables and CNF conversions for the Atif Intro+CNF note, verified with cfg_tools.CFG."""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg_tools import CFG
sys.stdout.reconfigure(encoding="utf-8")


def cyk(rules, w):
    """rules: {A: ["BC", "a", ...]} in CNF with single-letter variables. Returns table X[i][j] (1-based)."""
    n = len(w)
    X = {}
    for i in range(1, n + 1):
        X[(i, i)] = {A for A, bs in rules.items() if w[i - 1] in bs}
    for L in range(2, n + 1):
        for i in range(1, n - L + 2):
            j = i + L - 1
            s = set()
            for k in range(i, j):
                for A, bs in rules.items():
                    for b in bs:
                        if len(b) == 2 and b[0] in X[(i, k)] and b[1] in X[(k + 1, j)]:
                            s.add(A)
            X[(i, j)] = s
    return X


def cyk_lines(rules, w, start="S"):
    X = cyk(rules, w)
    n = len(w)
    cw = max(9, max(len("{" + ",".join(sorted(v)) + "}") for v in X.values()) + 2)
    lines = []
    for L in range(n, 0, -1):
        row = []
        for i in range(1, n - L + 2):
            v = X[(i, i + L - 1)]
            row.append(f"X{i}{i + L - 1}=" + ("{" + ",".join(sorted(v)) + "}" if v else "∅"))
        lines.append(f"len {L}: " + "  ".join(f"{c:<{cw + 4}}" for c in row))
    lines.append("        " + "  ".join(f"{c:<{cw + 4}}" for c in w))
    ok = start in X[(1, n)]
    lines.append(f"{start} {'∈' if ok else '∉'} X1{n}  ⇒  {w} {'∈' if ok else '∉'} L(G)")
    return lines, ok


G_SLIDE = {"S": ["AB", "BC"], "A": ["BA", "a"], "B": ["CC", "b"], "C": ["AB", "a"]}
G_SAME = {"S": ["BZ", "CY", "ZZ", "YY"], "B": ["ZA"], "C": ["YA"], "A": ["ZA", "YA", "0", "1"], "Z": ["0"], "Y": ["1"]}
G_2223 = {"S": ["AB", "AY", "YA", "1"], "A": ["ZA", "YA", "0", "1"], "B": ["YA"], "Z": ["0"], "Y": ["1"]}
# CNF of S→A1A|B, A→0A|1A|ε (2017-18; B has no rules → useless, D unreachable) — same for 2021-22 with B→1
CNF_1718 = {"S": ["AU", "UA", "VA", "1"], "V": ["AU"], "A": ["ZA", "UA", "0", "1"], "Z": ["0"], "U": ["1"]}
CNF_2122 = CNF_1718  # B→1 adds S→1, already present
CNF_BAB = {"S": ["BC", "BB", "AB", "BA", "ZZ"], "A": ["BC", "BB", "AB", "BA", "ZZ"], "C": ["AB"], "B": ["ZZ"], "Z": ["0"]}  # + S→ε

if __name__ == "__main__":
    ok = True
    for name, G, w in [("slide baaba", G_SLIDE, "baaba"), ("2007-08 abaab", G_SLIDE, "abaab"),
                       ("Jan-2020 10011", G_SAME, "10011"), ("2019-20 01100", G_SAME, "01100"),
                       ("2023-24 0010", G_SAME, "0010"), ("2022-23 0100", G_2223, "0100"),
                       ("2017-18 01101", CNF_1718, "01101")]:
        lines, r = cyk_lines(G, w)
        print("#", name); print("\n".join(lines))
        g = CFG({k: list(v) for k, v in G.items()}, "S")
        ok &= (g.count(w) > 0) == r
    same = CFG({k: list(v) for k, v in G_SAME.items()}, "S")
    ok &= all((same.count(w) > 0) == (len(w) >= 2 and w[0] == w[-1]) for L in range(7) for w in map("".join, itertools.product("01", repeat=L)))
    orig = CFG({"S": ["A1A"], "A": ["0A", "1A", ""]}, "S")
    cnf = CFG({k: list(v) for k, v in CNF_1718.items()}, "S")
    ok &= all((orig.count(w) > 0) == (cnf.count(w) > 0) for L in range(8) for w in map("".join, itertools.product("01", repeat=L)))
    o2 = CFG({"A": ["BAB", "B", ""], "B": ["00", ""]}, "A")
    c2 = CFG({k: list(v) for k, v in CNF_BAB.items()}, "S")
    ok &= all((o2.count(w) > 0) == (c2.count(w) > 0 or w == "") for L in range(9) for w in map("".join, itertools.product("0", repeat=L)))
    print("L(A→BAB|B|ε, B→00|ε) =", [w for w in map("".join, ("0" * L for L in range(9))) if o2.count(w)])
    # 2008-09 simplification check
    g0 = CFG({"S": ["ASB", ""], "A": ["aAS", "a"], "B": ["SbS", "A", "bb"]}, "S")
    g1 = CFG({"S": ["ASB", "AB"], "A": ["aAS", "aA", "a"], "B": ["SbS", "Sb", "bS", "b", "A", "bb"]}, "S")
    g2 = CFG({"S": ["ASB", "AB"], "A": ["aAS", "aA", "a"], "B": ["SbS", "Sb", "bS", "b", "bb", "aAS", "aA", "a"]}, "S")
    ok &= all((g0.count(w) > 0) == (g1.count(w) > 0 or w == "") == (g2.count(w) > 0 or w == "")
              for L in range(7) for w in map("".join, itertools.product("ab", repeat=L)))
    print("ALL OK" if ok else "FAIL")
