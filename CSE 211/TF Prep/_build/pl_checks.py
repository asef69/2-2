"""Checks for the pumping-lemma note: minimum pumping length of 2022-23 Q2(b) and the n! inequality."""
import sys, math
sys.stdout.reconfigure(encoding="utf-8")
def inL(w):
    return (set(w) <= {"a"} and len(w) >= 2 and (len(w) - 2) % 3 == 0) or (set(w) <= {"b"} and len(w) >= 10 and (len(w) - 10) % 12 == 0)
def pumpable(w, p):
    for xl in range(0, p):
        for yl in range(1, p - xl + 1):
            if xl + yl > len(w): continue
            x, y, z = w[:xl], w[xl:xl + yl], w[xl + yl:]
            if all(inL(x + y * i + z) for i in range(0, 6)): return True
    return False
def valid(p, N=80):
    ws = ["a" * m for m in range(N) if inL("a" * m)] + ["b" * m for m in range(N) if inL("b" * m)]
    return all(pumpable(w, p) for w in ws if len(w) >= p)
print({p: valid(p) for p in [3, 5, 9, 11, 12, 24]})
print("min pumping length:", min(p for p in range(1, 30) if valid(p)))
print("n! gap ok:", all(math.factorial(n) < math.factorial(n) + k < math.factorial(n + 1) for n in range(2, 12) for k in range(1, n + 1)))
