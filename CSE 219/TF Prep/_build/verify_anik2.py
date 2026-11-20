"""Checks for Anik F2 (LTI systems, convolution, causality, stability)."""
import numpy as np
import sympy as sp

t, tau = sp.symbols("t tau", real=True)
ok = lambda name, cond: print(("OK  " if cond else "FAIL") + "  " + name)


def dconv(x, h, n0x=0, n0h=0):
    y = np.convolve(x, h)
    return y, n0x + n0h


# slides
y, _ = dconv([1, 2, 1, 1], [1, 1, -1, 2])
ok(f"Lec3 sl28 y = {list(y)}", list(y) == [1, 3, 2, 2, 4, 1, 2])
ok("Lec3 z^4 coefficient = 17", np.convolve([1, 3, 2, 5, 4], [2, -1, 4, 1, 3])[4] == 17)
y, _ = dconv([0.5, 2], [1, 1, 1])
ok(f"Lec4 Ex2.2 y = {list(y)}", list(y) == [0.5, 2.5, 2.5, 2])
ok("Practice set 3.1 {1,2}*{1,-1,2}", list(np.convolve([1, 2], [1, -1, 2])) == [1, 1, 0, 4])


# CSE219 2022-23 8(a): x = 3^n u[-n-1] + (1/3)^n u[n], h = (1/4)^n u[n+3]
def x(n):
    return 3.0 ** n if n <= -1 else (1 / 3) ** n


def h(n):
    return 0.25 ** n if n >= -3 else 0.0


def ynum(n):
    return sum(x(k) * h(n - k) for k in range(-200, 200))


def yclaim(n):
    return 256 * 3.0 ** (n + 4) / 11 if n <= -4 else 256 / 3.0 ** (n + 3) - (32 / 11) * 0.25 ** n


ok("CSE219 22-23 8(a) closed form",
   all(abs(ynum(n) - yclaim(n)) < 1e-9 * max(1, abs(yclaim(n))) for n in range(-15, 15)))
print("     y[-4..3] =", [round(yclaim(n), 4) for n in range(-4, 4)])

# CSE219 2023-24 1(b)
d = lambda n: 1 if n == 0 else 0
u = lambda n: 1 if n >= 0 else 0
h1 = lambda n: d(n) - d(n - 2)
h2 = lambda n: u(n - 1)
h3 = lambda n: d(n) - d(n - 1)
N = range(-5, 30)
hs = lambda n: h1(n) + h2(n)
heq = lambda n: sum(hs(k) * h3(n - k) for k in range(-5, 40))
ok("1(b) heq = d[n] - d[n-2] + d[n-3]", all(heq(n) == d(n) - d(n - 2) + d(n - 3) for n in N))
yy = [sum(heq(k) * u(n - k) for k in range(-5, 40)) for n in range(0, 8)]
ok(f"1(b) y[0..7] = {yy}", yy == [1, 1, 0, 1, 1, 1, 1, 1])

# EEE 2023-24 1(c)
U = sp.Heaviside


def cconv(f, g, lo=0):
    return sp.simplify(sp.integrate(sp.expand(sp.powsimp(sp.expand(f.subs(t, tau) * g.subs(t, t - tau)))), (tau, lo, t), conds='none'))


h23 = cconv(sp.exp(-2 * t), sp.exp(-t))
g = sp.exp(-2 * t) + h23
ok(f"h1 + h2*h3 = {sp.simplify(g)}", sp.simplify(g - sp.exp(-t)) == 0)
heq_c = sp.exp(-3 * t) + cconv(sp.exp(-t), sp.exp(-3 * t))
ok(f"heq = {sp.simplify(heq_c)}", sp.simplify(heq_c - (sp.exp(-t) + sp.exp(-3 * t)) / 2) == 0)
ok("int |heq| = 2/3", sp.integrate((sp.exp(-t) + sp.exp(-3 * t)) / 2, (t, 0, sp.oo)) == sp.Rational(2, 3))
yc = cconv(sp.exp(-t), (sp.exp(-t) + sp.exp(-3 * t)) / 2)
ok(f"y = {sp.expand(yc)}", sp.simplify(yc - (t * sp.exp(-t) / 2 + sp.exp(-t) / 4 - sp.exp(-3 * t) / 4)) == 0)


# graphical convolutions (numeric)
def num_conv(xf, hf, a, b, dt=1e-3):
    tt = np.arange(a, b, dt)
    y = np.convolve(xf(tt), hf(tt)) * dt
    ty = 2 * a + np.arange(len(y)) * dt
    return ty, y


tri = lambda s: np.clip(1 - np.abs(s), 0, None)
rect = lambda s, lo, hi: ((s >= lo) & (s < hi)).astype(float)


def check(name, xf, hf, claim, a=-6, b=8, pts=None, tol=5e-3):
    ty, y = num_conv(xf, hf, a, b)
    pts = pts or np.linspace(a + 0.5, b - 0.5, 41)
    err = max(abs(np.interp(p, ty, y) - claim(p)) for p in pts)
    ok(f"{name} (max err {err:.1e})", err < tol)


def pwc(pieces):
    def f(s):
        for lo, hi, fn in pieces:
            if lo <= s < hi:
                return fn(s)
        return 0.0
    return f


check("EEE23-24 2(a) rect[1,2]*tri", lambda s: rect(s, 1, 2), tri,
      pwc([(0, 1, lambda s: s * s / 2), (1, 2, lambda s: -s * s + 3 * s - 1.5), (2, 3, lambda s: (3 - s) ** 2 / 2)]))
check("EEE19-20 Q2 rect[0,2]*tri(t-1)", lambda s: rect(s, 0, 2), lambda s: tri(s - 1),
      pwc([(0, 1, lambda s: s * s / 2), (1, 2, lambda s: 1 - (2 - s) ** 2 / 2), (2, 3, lambda s: 1 - (s - 2) ** 2 / 2),
           (3, 4, lambda s: (4 - s) ** 2 / 2)]))
check("EEE10-11 6(b)(i) rect[0,2]*tri", lambda s: rect(s, 0, 2), tri,
      pwc([(-1, 0, lambda s: (s + 1) ** 2 / 2), (0, 1, lambda s: 1 - (1 - s) ** 2 / 2), (1, 2, lambda s: 1 - (s - 1) ** 2 / 2),
           (2, 3, lambda s: (3 - s) ** 2 / 2)]))
check("EEE20-21 6(b) rect(t/2)*r(t)u(1-t)", lambda s: rect(s, -1, 1), lambda s: np.where((s >= 0) & (s < 1), s, 0.0),
      pwc([(-1, 0, lambda s: (s + 1) ** 2 / 2), (0, 1, lambda s: 0.5), (1, 2, lambda s: 0.5 - (s - 1) ** 2 / 2)]))
check("EEE21-22 2(a) tri(t-1)*[2rect(0,1)]", lambda s: tri(s - 1), lambda s: 2 * rect(s, 0, 1),
      pwc([(0, 1, lambda s: s * s), (1, 2, lambda s: -2 * s * s + 6 * s - 3), (2, 3, lambda s: (3 - s) ** 2)]))
check("EEE18-19 7(b) t^2[0,3]*rect(0,1)", lambda s: np.where((s >= 0) & (s < 3), s * s, 0.0), lambda s: rect(s, 0, 1),
      pwc([(0, 1, lambda s: s ** 3 / 3), (1, 3, lambda s: (s ** 3 - (s - 1) ** 3) / 3), (3, 4, lambda s: (27 - (s - 1) ** 3) / 3)]), tol=2e-2)
check("EEE301 11-12 7(d) P(t) = rect(-1,1)*tri", lambda s: rect(s, -1, 1), tri,
      pwc([(-2, -1, lambda s: (s + 2) ** 2 / 2), (-1, 1, lambda s: 1 - s * s / 2), (1, 2, lambda s: (2 - s) ** 2 / 2)]))

# EEE 2022-23 7(b): x = h = t on [0,1]
y1 = sp.integrate(tau * (t - tau), (tau, 0, t))
y2 = sp.integrate(tau * (t - tau), (tau, t - 1, 1))
print("     7(b): y =", sp.factor(y1), "on [0,1];", sp.expand(y2), "on [1,2]")
ok("7(b) continuity at t=1", y1.subs(t, 1) == y2.subs(t, 1) and y2.subs(t, 2) == 0)

# EEE 2023-24 2(b): LC: h = w0 sin(w0 t) satisfies LC h'' + h = 0, h(0+) = 0, h'(0+) = 1/LC
L, C = sp.symbols("L C", positive=True)
w0 = 1 / sp.sqrt(L * C)
hh = w0 * sp.sin(w0 * t)
ok("LC h'' + h = 0", sp.simplify(L * C * sp.diff(hh, t, 2) + hh) == 0)
ok("h'(0+) = 1/LC", sp.simplify(sp.diff(hh, t).subs(t, 0) - 1 / (L * C)) == 0)

# EEE301 2015-16 3(b)
hb = sp.exp(-3 * t) - sp.exp(-2 * t)
s1 = sp.integrate(hb.subs(t, tau), (tau, 0, t))
ok(f"step response = {sp.expand(s1)}", sp.simplify(s1 - (-sp.Rational(1, 6) - sp.exp(-3 * t) / 3 + sp.exp(-2 * t) / 2)) == 0)
ye = cconv(sp.exp(-t), hb)
ok(f"response to e^-t u = {sp.expand(ye)}",
   sp.simplify(ye - (-sp.exp(-t) / 2 + sp.exp(-2 * t) - sp.exp(-3 * t) / 2)) == 0)

# EEE 2017-18 7(b): te^-t * e^-2t
hc = cconv(t * sp.exp(-t), sp.exp(-2 * t))
ok(f"te^-t * e^-2t = {sp.expand(hc)}", sp.simplify(hc - ((t - 1) * sp.exp(-t) + sp.exp(-2 * t))) == 0)

# stability integrals
ok("int e^{2t}, t<=-2 = e^-4/2", sp.integrate(sp.exp(2 * t), (t, -sp.oo, -2)) == sp.exp(-4) / 2)
ok("int t e^-t = 1", sp.integrate(t * sp.exp(-t), (t, 0, sp.oo)) == 1)
ok("int e^-6|t| = 1/3", 2 * sp.integrate(sp.exp(-6 * t), (t, 0, sp.oo)) == sp.Rational(1, 3))
ok("int_{-oo}^3 e^-4t diverges", sp.integrate(sp.exp(-4 * t), (t, -sp.oo, 3)) == sp.oo)
# Lec 4 examples
a = sp.symbols("a", positive=True)
ok("e^-at u * u = (1-e^-at)/a", sp.simplify(cconv(sp.exp(-a * t), sp.Integer(1)) - (1 - sp.exp(-a * t)) / a) == 0)
yl = sp.integrate(sp.exp(tau) * sp.exp(-(t - tau)), (tau, -sp.oo, t))
ok("e^t u(-t) * e^-t u(t), t<0 = e^t/2", sp.simplify(yl - sp.exp(t) / 2) == 0)
n_ = sp.symbols("n", integer=True)
ok("Ex2.10 n>=0: 4 - 2^-n", all(abs(sum((0.5 ** k if k >= 0 else 0) + (2.0 ** k if k <= 0 else 0) for k in range(-80, nn + 1))
                                  - (4 - 2.0 ** -nn)) < 1e-9 for nn in range(0, 6)))
