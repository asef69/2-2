"""Small automata toolkit used to VERIFY every construction printed in the notes.
import sys; sys.stdout.reconfigure(encoding="utf-8")
DFA: dict(states, sigma, delta{(q,a):r}, start, accept)
NFA: delta{(q,a or ''):set}, '' = ε
"""
from itertools import product


def strings(sigma, maxlen):
    yield ""
    for n in range(1, maxlen + 1):
        for t in product(sigma, repeat=n):
            yield "".join(t)


class DFA:
    def __init__(self, states, sigma, delta, start, accept, dead=None):
        self.states, self.sigma, self.delta = list(states), list(sigma), dict(delta)
        self.start, self.accept = start, set(accept)
        if dead is not None:  # complete with a dead state
            for q in list(self.states) + [dead]:
                for a in self.sigma:
                    self.delta.setdefault((q, a), dead)
            if dead not in self.states:
                self.states.append(dead)

    def run(self, w):
        q = self.start
        for c in w:
            if (q, c) not in self.delta:
                return None
            q = self.delta[(q, c)]
        return q

    def accepts(self, w):
        q = self.run(w)
        return q is not None and q in self.accept

    def table(self, names=None, star="*", arrow="→"):
        nm = names or {q: str(q) for q in self.states}
        nw = max(len(nm[q]) for q in self.states) + 2
        cw = max(4, max(len(nm[q]) for q in self.states) + 2)
        lines = [" " * (2 + nw) + "".join(f"{a:<{cw}}" for a in self.sigma).rstrip()]
        for q in self.states:
            tag = (arrow if q == self.start else " ") + (star if q in self.accept else " ")
            row = tag + f"{nm[q]:<{nw}}" + "".join(f"{nm[self.delta[(q, a)]]:<{cw}}" for a in self.sigma)
            lines.append(row.rstrip())
        return lines

    def minimize_count(self):
        reach, todo = {self.start}, [self.start]
        while todo:
            q = todo.pop()
            for a in self.sigma:
                r = self.delta[(q, a)]
                if r not in reach:
                    reach.add(r); todo.append(r)
        part = {q: (q in self.accept) for q in reach}
        while True:
            sig = {q: (part[q],) + tuple(part[self.delta[(q, a)]] for a in self.sigma) for q in reach}
            ids = {}
            new = {q: ids.setdefault(sig[q], len(ids)) for q in reach}
            if len(set(new.values())) == len(set(part.values())):
                return len(set(new.values()))
            part = new


def check(dfa, pred, maxlen=10, label=""):
    bad = [w for w in strings(dfa.sigma, maxlen) if dfa.accepts(w) != bool(pred(w))]
    status = "OK" if not bad else f"FAIL e.g. {bad[:5]}"
    print(f"[{label}] {status}  (all strings ≤ {maxlen})")
    return not bad


class NFA:
    def __init__(self, states, sigma, delta, start, accept):
        self.states, self.sigma, self.start, self.accept = list(states), list(sigma), start, set(accept)
        self.delta = {k: set(v) for k, v in delta.items()}

    def close(self, S):
        S, todo = set(S), list(S)
        while todo:
            q = todo.pop()
            for r in self.delta.get((q, ""), ()):
                if r not in S:
                    S.add(r); todo.append(r)
        return frozenset(S)

    def step(self, S, a):
        out = set()
        for q in S:
            out |= self.delta.get((q, a), set())
        return self.close(out)

    def accepts(self, w):
        S = self.close({self.start})
        for c in w:
            S = self.step(S, c)
        return bool(S & self.accept)

    def subset(self):
        """Reachable subset construction (Sipser: start = E({q0})). Returns (order, delta, accept)."""
        s0 = self.close({self.start})
        order, delta, todo = [s0], {}, [s0]
        while todo:
            S = todo.pop(0)
            for a in self.sigma:
                T = self.step(S, a)
                delta[(S, a)] = T
                if T not in order:
                    order.append(T); todo.append(T)
        acc = [S for S in order if S & self.accept]
        return order, delta, acc

    def to_dfa(self):
        order, delta, acc = self.subset()
        return DFA(order, self.sigma, delta, order[0], acc)


def setname(S, order=None):
    if not S:
        return "∅"
    return "{" + ",".join(sorted(S, key=str)) + "}"
