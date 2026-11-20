"""Shared helpers for the MATH 243 notes: every number in a worked solution is
computed here (exact Python arithmetic), so the notes and the check agree.

Conventions follow the slides: grouped variance uses divisor N (Dispersion deck p. 9),
step deviation d = (x − A)/h, moments μr' = (Σ f d^r / N)·h^r (Moments deck p. 10).
"""
import math
import sys
from fractions import Fraction as Fr

sys.path.insert(0, r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2\_tfprep")

import numpy as np
from scipy import stats

NOTES_DIR = r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2\MATH 243\TF Prep\notes"
PROB = r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2\MATH 243\probability"
STAT = r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2\MATH 243\stats"


def g(x, d=4):
    """Format a number: up to d decimals, trailing zeros stripped, minus sign as −."""
    if isinstance(x, Fr):
        x = float(x)
    if isinstance(x, (int, np.integer)) or (isinstance(x, float) and float(x).is_integer() and abs(x) < 1e12):
        s = f"{int(round(x)):,}" if abs(x) >= 10000 else str(int(round(x)))
    else:
        s = f"{x:.{d}f}".rstrip("0").rstrip(".")
    return s.replace("-", "−")


def fr(x):
    x = Fr(x).limit_denominator(100000)
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def Phi(z):
    return float(stats.norm.cdf(z))


def table_phi(z):
    """Value read from a 4-decimal z table after rounding z to 2 decimals."""
    return round(Phi(round(z, 2)), 4)


def zinv(p):
    return float(stats.norm.ppf(p))


# ------------------------------------------------------------------ grouped data
class Grouped:
    """Grouped frequency distribution. classes = [(lo, hi), ...] (boundaries or limits), f = [...]."""

    def __init__(self, classes, f, A=None, h=None):
        self.classes, self.f = classes, list(f)
        self.x = [(a + b) / 2 for a, b in classes]
        self.N = sum(self.f)
        self.h = h or (classes[1][0] - classes[0][0])
        if A is None:  # assumed mean = mid value of the class nearest the middle (largest f if tie-free)
            A = self.x[len(self.x) // 2]
        self.A = A
        self.d = [round((x - A) / self.h, 10) for x in self.x]
        self.s = [sum(fi * di ** r for fi, di in zip(self.f, self.d)) for r in range(5)]

    @property
    def mean(self):
        return self.A + self.s[1] / self.N * self.h

    @property
    def var(self):
        return (self.s[2] / self.N - (self.s[1] / self.N) ** 2) * self.h ** 2

    @property
    def sd(self):
        return math.sqrt(self.var)

    @property
    def cv(self):
        return self.sd / self.mean * 100

    def raw(self, r):
        return self.s[r] / self.N * self.h ** r

    def central(self):
        m1, m2, m3, m4 = (self.raw(r) for r in (1, 2, 3, 4))
        mu2 = m2 - m1 ** 2
        mu3 = m3 - 3 * m2 * m1 + 2 * m1 ** 3
        mu4 = m4 - 4 * m3 * m1 + 6 * m2 * m1 ** 2 - 3 * m1 ** 4
        return (m1, m2, m3, m4), (0.0, mu2, mu3, mu4)

    def beta_gamma(self):
        _, (_, mu2, mu3, mu4) = self.central()
        b1 = mu3 ** 2 / mu2 ** 3
        b2 = mu4 / mu2 ** 2
        g1 = mu3 / mu2 ** 1.5
        return b1, b2, g1, b2 - 3

    def cum(self):
        out, c = [], 0
        for fi in self.f:
            c += fi
            out.append(c)
        return out

    def quantile(self, k, parts=4):
        """i-th quartile (parts=4), decile (10), percentile (100): L + (iN/parts − pcf)/f · h."""
        pos = k * self.N / parts
        cf = self.cum()
        for i, c in enumerate(cf):
            if c >= pos:
                pcf = cf[i - 1] if i else 0
                L = self.classes[i][0]
                return L + (pos - pcf) / self.f[i] * self.h, dict(pos=pos, i=i, L=L, pcf=pcf, f=self.f[i])
        raise ValueError

    def median(self):
        return self.quantile(2, 4)

    def mode(self):
        i = max(range(len(self.f)), key=lambda j: self.f[j])
        f0 = self.f[i - 1] if i else 0
        f2 = self.f[i + 1] if i + 1 < len(self.f) else 0
        d1, d2 = self.f[i] - f0, self.f[i] - f2
        L = self.classes[i][0]
        return L + d1 / (d1 + d2) * self.h, dict(i=i, L=L, d1=d1, d2=d2)

    # ------------- rows for n.table()
    def rows(self, powers=2, cum=False, labels=None):
        rws = []
        for k, ((a, b), x, fi, di) in enumerate(zip(self.classes, self.x, self.f, self.d)):
            lab = labels[k] if labels else f"{g(a)}–{g(b)}"
            r = [lab, g(x), g(fi), g(di)] + [g(fi * di ** p) for p in range(1, powers + 1)]
            if cum:
                r.append(g(self.cum()[k]))
            rws.append(r)
        tot = ["Total", "", f"N = {g(self.N)}", ""] + [f"Σ = {g(self.s[p])}" for p in range(1, powers + 1)]
        if cum:
            tot.append("")
        rws.append(tot)
        return rws

    def headers(self, powers=2, cum=False, name="Class"):
        h = [name, "Mid x", "f", "d = (x − A)/h"] + ["fd" if p == 1 else f"fd^{{{p}}}" for p in range(1, powers + 1)]
        if cum:
            h.append("c.f.")
        return h


# ------------------------------------------------------------------ ungrouped
def summary(xs):
    xs = np.array(xs, float)
    n = len(xs)
    m = xs.mean()
    var = ((xs - m) ** 2).sum() / n
    return dict(n=n, sum=xs.sum(), mean=m, ss=((xs - m) ** 2).sum(), var=var, sd=math.sqrt(var),
                cv=math.sqrt(var) / m * 100)


def regression(x, y):
    x, y = np.array(x, float), np.array(y, float)
    n = len(x)
    Sx, Sy, Sxx, Syy, Sxy = x.sum(), y.sum(), (x * x).sum(), (y * y).sum(), (x * y).sum()
    sxx = Sxx - Sx ** 2 / n
    syy = Syy - Sy ** 2 / n
    sxy = Sxy - Sx * Sy / n
    byx = sxy / sxx
    bxy = sxy / syy
    r = sxy / math.sqrt(sxx * syy)
    xb, yb = Sx / n, Sy / n
    return dict(n=n, Sx=Sx, Sy=Sy, Sxx=Sxx, Syy=Syy, Sxy=Sxy, sxx=sxx, syy=syy, sxy=sxy, byx=byx, bxy=bxy,
                r=r, xb=xb, yb=yb, ayx=yb - byx * xb, axy=xb - bxy * yb)


def spearman_ties(x, y):
    rx = stats.rankdata(x)
    ry = stats.rankdata(y)
    D2 = ((rx - ry) ** 2).sum()
    n = len(x)
    corr = 0.0
    for arr in (x, y):
        vals, cnt = np.unique(arr, return_counts=True)
        for m in cnt:
            if m > 1:
                corr += (m ** 3 - m) / 12
    rs = 1 - 6 * (D2 + corr) / (n * (n * n - 1))
    return dict(rx=rx, ry=ry, D2=D2, corr=corr, rs=rs, n=n)


def anova1(groups):
    allv = np.concatenate([np.array(g_, float) for g_ in groups])
    N, k = len(allv), len(groups)
    G = allv.sum()
    CT = G ** 2 / N
    ST = (allv ** 2).sum() - CT
    T = [float(np.sum(g_)) for g_ in groups]
    n = [len(g_) for g_ in groups]
    SB = sum(t * t / m for t, m in zip(T, n)) - CT
    SW = ST - SB
    MSB, MSW = SB / (k - 1), SW / (N - k)
    F = MSB / MSW
    return dict(N=N, k=k, G=G, CT=CT, ST=ST, SB=SB, SW=SW, MSB=MSB, MSW=MSW, F=F, T=T, n=n,
                sumsq=float((allv ** 2).sum()), df1=k - 1, df2=N - k,
                F05=float(stats.f.ppf(0.95, k - 1, N - k)), F01=float(stats.f.ppf(0.99, k - 1, N - k)),
                p=float(stats.f.sf(F, k - 1, N - k)))


def anova2(M):
    """Two-way ANOVA without replication, rows = blocks, columns = treatments."""
    M = np.array(M, float)
    r, c = M.shape
    N = r * c
    G = M.sum()
    CT = G ** 2 / N
    ST = (M ** 2).sum() - CT
    R = M.sum(axis=1)
    C = M.sum(axis=0)
    SR = (R ** 2).sum() / c - CT
    SC = (C ** 2).sum() / r - CT
    SE = ST - SR - SC
    dfr, dfc, dfe = r - 1, c - 1, (r - 1) * (c - 1)
    MSR, MSC, MSE = SR / dfr, SC / dfc, SE / dfe
    return dict(r=r, c=c, N=N, G=G, CT=CT, ST=ST, R=R, C=C, SR=SR, SC=SC, SE=SE, dfr=dfr, dfc=dfc, dfe=dfe,
                MSR=MSR, MSC=MSC, MSE=MSE, FR=MSR / MSE, FC=MSC / MSE, sumsq=float((M ** 2).sum()),
                FR05=float(stats.f.ppf(0.95, dfr, dfe)), FC05=float(stats.f.ppf(0.95, dfc, dfe)))
