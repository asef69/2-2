"""Grammar checker: G = {Var: ["body", ...]}, bodies are lists of symbols written as space-free strings where
uppercase letters (and names in VARS) are variables. Membership + parse-tree counting by memoised splitting.
Used to verify every CFG, derivation and ambiguity claim in the CFG/CNF notes."""
import sys, re, itertools
from functools import lru_cache
sys.stdout.reconfigure(encoding="utf-8")


def parse_body(body, variables):
    if body in ("", "ε"):
        return ()
    toks, i = [], 0
    names = sorted(variables, key=len, reverse=True)
    while i < len(body):
        for v in names:
            if body.startswith(v, i):
                toks.append(v); i += len(v); break
        else:
            toks.append(body[i]); i += 1
    return tuple(toks)


class CFG:
    def __init__(self, rules, start):
        self.vars = set(rules)
        self.start = start
        self.R = {A: [parse_body(b, self.vars) for b in bs] for A, bs in rules.items()}
        self.nullable = set()
        ch = True
        while ch:
            ch = False
            for A, bs in self.R.items():
                if A not in self.nullable and any(all(s in self.nullable for s in b) for b in bs):
                    self.nullable.add(A); ch = True

    def count(self, w, sym=None):
        """number of parse trees of w from sym (cycles cut off)."""
        sym = sym or self.start
        stack = set()

        @lru_cache(maxsize=None)
        def c(X, s):
            if X not in self.vars:
                return 1 if s == X else 0
            if (X, s) in stack:
                return 0
            stack.add((X, s))
            tot = 0
            for b in self.R[X]:
                tot += seq(b, s)
            stack.discard((X, s))
            return tot

        def seq(b, s):
            if not b:
                return 1 if s == "" else 0
            X, rest = b[0], b[1:]
            tot = 0
            for k in range(len(s) + 1):
                if k == 0 and X not in self.nullable:
                    continue
                left = c(X, s[:k])
                if left:
                    tot += left * seq(rest, s[k:])
            return tot
        return c(sym, w)

    def gen(self, sigma, n):
        return [w for L in range(n + 1) for w in map("".join, itertools.product(sigma, repeat=L)) if self.count(w)]


def verify(name, g, pred, sigma, n=8):
    bad = []
    for L in range(n + 1):
        for t in itertools.product(sigma, repeat=L):
            w = "".join(t)
            if bool(g.count(w)) != bool(pred(w)):
                bad.append(w)
                if len(bad) > 3:
                    break
    print(f"{name:16} {'OK' if not bad else 'FAIL ' + str(bad[:4])}")
    return not bad


def ambiguous_witness(g, sigma, n=8):
    for L in range(n + 1):
        for t in itertools.product(sigma, repeat=L):
            w = "".join(t)
            if g.count(w) > 1:
                return w, g.count(w)
    return None
