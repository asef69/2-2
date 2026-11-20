"""CFG→PDA (empty stack), PDA→CFG (triple construction with pruning), FS→ES and ES→FS, all verified.
PDA transition format (Hopcroft): (q, a, X, r, gamma): a '' = ε, gamma = string of stack symbols, FIRST char = new top."""
import os, sys, itertools, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
from cfg_tools import CFG


def run_es(trans, start, z0, w, maxstack=None, accept_states=None, mode="ES"):
    """accept by empty stack (mode ES) or final state (mode FS). Returns bool."""
    maxstack = maxstack or 3 * len(w) + 6
    seen, todo = set(), [(start, 0, z0)]
    while todo:
        c = todo.pop()
        if c in seen or len(c[2]) > maxstack:
            continue
        seen.add(c)
        q, i, st = c
        if i == len(w) and ((mode == "ES" and st == "") or (mode == "FS" and q in accept_states)):
            return True
        if not st:
            continue
        for (p, a, X, r, g) in trans:
            if p == q and st[0] == X and (not a or (i < len(w) and w[i] == a)):
                todo.append((r, i + (1 if a else 0), g + st[1:]))
    return False


def cfg_to_pda(rules, start):
    """rules {A: [bodies]} single-char symbols. PDA: one state q, δ(q,ε,A)={(q,β)}, δ(q,a,a)={(q,ε)}."""
    T = []
    terms = set()
    for A, bs in rules.items():
        for b in bs:
            T.append(("q", "", A, "q", b))
            terms |= {c for c in b if c not in rules}
    for a in sorted(terms):
        T.append(("q", a, a, "q", ""))
    return T, terms


def pda_to_cfg(trans, states, start, z0):
    """Triple construction for empty-stack PDA; returns pruned rules (names '[pXq]') and start 'S'."""
    R = {"S": [f"[{start}{z0}{p}]" for p in states]}
    for (q, a, X, r, g) in trans:
        k = len(g)
        for rs in itertools.product(states, repeat=k):
            for rk in (rs[-1:] if k else [r]):
                if k == 0:
                    head = f"[{q}{X}{r}]"
                    R.setdefault(head, []).append(a)
                    continue
            if k:
                head_last = rs[-1]
                chain, prev = [], r
                for Y, nxt in zip(g, rs):
                    chain.append(f"[{prev}{Y}{nxt}]"); prev = nxt
                R.setdefault(f"[{q}{X}{head_last}]", []).append(a + "".join(chain))
    # prune: generating then reachable
    def toks(b):
        return re.findall(r"\[[^\]]+\]|.", b)
    gen = set()
    ch = True
    while ch:
        ch = False
        for A, bs in R.items():
            if A in gen:
                continue
            if any(all((t in gen) or not t.startswith("[") for t in toks(b)) for b in bs):
                gen.add(A); ch = True
    R2 = {A: [b for b in bs if all((t in gen) or not t.startswith("[") for t in toks(b))] for A, bs in R.items() if A in gen}
    reach, todo = {"S"}, ["S"]
    while todo:
        A = todo.pop()
        for b in R2.get(A, []):
            for t in toks(b):
                if t.startswith("[") and t not in reach:
                    reach.add(t); todo.append(t)
    return {A: bs for A, bs in R2.items() if A in reach}


def cfg_from_named(R):
    names = {A: chr(ord("A") + i) if A != "S" else "S" for i, A in enumerate(sorted(R, key=lambda x: (x != "S", x)))}
    out = {}
    for A, bs in R.items():
        nb = []
        for b in bs:
            toks = re.findall(r"\[[^\]]+\]|.", b)
            nb.append("".join(names.get(t, t) for t in toks))
        out[names[A]] = nb
    return out, names


def lang_cfg(R, sig, n):
    c = CFG({k: v for k, v in R.items()}, "S")
    return {w for L in range(n + 1) for w in map("".join, itertools.product(sig, repeat=L)) if c.count(w)}


if __name__ == "__main__":
    ok = True
    # --- CFG → PDA
    cases = {
        "2009-10 11(a)": ({"S": ["AS", "A"], "A": ["0A", "1B", "1"], "B": ["0B", "0"]}, "01"),
        "2012-13 1(a)": ({"S": ["BS", "A"], "A": ["0A", ""], "B": ["BB1", "2"]}, "012"),
        "2011-12 4(b)": ({"S": ["aTXb"], "T": ["XTS", ""], "X": ["a", "b"]}, "ab"),
        "2010-11 12(d)": ({"S": ["TX"], "T": ["0T0", "1T1", "#X"], "X": ["0X", "1X", ""]}, "01#"),
        "2013-14 1(a)": ({"E": ["E+T", "T"], "T": ["T×F", "T/F", "F"], "F": ["(E)", "a"]}, "a+×/()"),
    }
    for name, (rules, sig) in cases.items():
        T, terms = cfg_to_pda(rules, next(iter(rules)))
        st = "S" if "S" in rules else "E"
        g = CFG(rules, st)
        bad = [w for L in range(7 if len(sig) <= 3 else 5) for w in map("".join, itertools.product(sig, repeat=L))
               if run_es(T, "q", st, w) != (g.count(w) > 0)]
        print(name, len(T), "transitions", "OK" if not bad else f"FAIL {bad[:3]}")
        ok &= not bad
    # --- PDA → CFG
    # slides: balanced parentheses (Atif Lec 3 sl. 119–121) with last move emptying the stack
    par = [("q0", "(", "Z", "q0", "(Z"), ("q0", "(", "(", "q0", "(("), ("q0", ")", "(", "q0", ""), ("q0", "", "Z", "q1", "")]
    R = pda_to_cfg(par, ["q0", "q1"], "q0", "Z")
    print("parentheses grammar (pruned):")
    for A, bs in R.items():
        print("  ", A, "→", " | ".join(bs))
    named, names = cfg_from_named(R)
    g = lang_cfg(named, "()", 8)
    bal = {w for L in range(9) for w in map("".join, itertools.product("()", repeat=L))
           if CFG({"S": ["(S)S", ""]}, "S").count(w)}
    ok &= g == bal
    print("par OK" if g == bal else "par FAIL")
    # 2009-10 11(b): L = ∅
    P2 = [("q", "1", "Z", "q", "XZ"), ("q", "0", "X", "p", "X"), ("p", "1", "X", "p", "")]
    R2 = pda_to_cfg(P2, ["q", "p"], "q", "Z")
    print("2009-10 11(b) pruned grammar:", R2)
    # palindromes (empty-stack form)
    pal = [("p", "0", "Z", "p", "0Z"), ("p", "1", "Z", "p", "1Z"), ("p", "0", "0", "p", "00"), ("p", "0", "1", "p", "01"),
           ("p", "1", "0", "p", "10"), ("p", "1", "1", "p", "11"), ("p", "", "Z", "m", ""), ("p", "", "0", "m", "0"), ("p", "", "1", "m", "1"),
           ("m", "0", "0", "m", ""), ("m", "1", "1", "m", ""), ("m", "", "Z", "m", "")]
    # check the ES-PDA for ww^R accepts even palindromes
    okp = all(run_es(pal, "p", "Z", w) == (len(w) % 2 == 0 and w == w[::-1]) for L in range(9) for w in map("".join, itertools.product("01", repeat=L)))
    print("palindrome ES-PDA OK" if okp else "FAIL"); ok &= okp
    Rp = pda_to_cfg(pal, ["p", "m"], "p", "Z")
    named, names = cfg_from_named(Rp)
    gp = lang_cfg(named, "01", 8)
    exp = {w for L in range(9) for w in map("".join, itertools.product("01", repeat=L)) if len(w) % 2 == 0 and w == w[::-1]}
    print("palindrome CFG size", sum(len(v) for v in named.values()), "OK" if gp == exp else "FAIL")
    ok &= gp == exp
    for A, bs in Rp.items():
        print("  ", A, "→", " | ".join(bs))
    # --- FS ↔ ES
    # PF: 0^n1^n by final state (Z0 start, q2 final) ; construct PN and check ES language equals
    PF = [("q0", "0", "Z", "q0", "XZ"), ("q0", "0", "X", "q0", "XX"), ("q0", "1", "X", "q1", ""), ("q1", "1", "X", "q1", ""), ("q1", "", "Z", "q2", "Z")]
    acc = {"q2"}
    chk = all(run_es(PF, "q0", "Z", w, accept_states=acc, mode="FS") == (re.fullmatch(r"0+1+", w) is not None and w.count("0") == w.count("1"))
              for L in range(9) for w in map("".join, itertools.product("01", repeat=L)))
    print("PF OK" if chk else "FAIL"); ok &= chk
    PN = [("p0", "", "W", "q0", "ZW")] + PF + [(f, "", X, "pe", "") for f in acc for X in "ZXW"] + [("pe", "", X, "pe", "") for X in "ZXW"]
    chk = all(run_es(PN, "p0", "W", w) == run_es(PF, "q0", "Z", w, accept_states=acc, mode="FS")
              for L in range(9) for w in map("".join, itertools.product("01", repeat=L)))
    print("FS→ES OK" if chk else "FAIL"); ok &= chk
    # ES → FS: PN' = PN of the parentheses grammar-style; use ES PDA for balanced parentheses
    ES = [("q", "(", "Z", "q", "(Z"), ("q", "(", "(", "q", "(("), ("q", ")", "(", "q", ""), ("q", "", "Z", "q", "")]
    PF2 = [("p0", "", "W", "q", "ZW")] + ES + [("q", "", "W", "pf", "")]
    chk = all(run_es(PF2, "p0", "W", w, accept_states={"pf"}, mode="FS") == run_es(ES, "q", "Z", w)
              for L in range(9) for w in map("".join, itertools.product("()", repeat=L)))
    print("ES→FS OK" if chk else "FAIL"); ok &= chk
    print("ALL OK" if ok else "FAIL")
