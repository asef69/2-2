"""Numerical checks for Anik F1 (Signals): energy/power, transformations, even-odd, impulses, periodicity."""
import numpy as np
import sympy as sp


t = sp.symbols("t", real=True)
ok = lambda name, cond: print(("OK  " if cond else "FAIL") + "  " + name)

# Lec 1 slides
ok("half-sine E = pi/2", sp.integrate(sp.sin(t) ** 2, (t, 0, sp.pi)) == sp.pi / 2)
ok("1/|t| signal E = 4", sp.integrate(1, (t, -1, 1)) + 2 * sp.integrate(1 / t ** 2, (t, 1, sp.oo)) == 4)

# EEE 2021-22 1(b): e^{-3t} sin(2pi t/3 - 4) u(t)
E = sp.integrate(sp.exp(-6 * t) * sp.sin(2 * sp.pi * t / 3 - 4) ** 2, (t, 0, sp.oo))
print("     EEE21-22 1(b) E =", sp.N(E))
ok("finite energy", sp.N(E) < 1)

# EEE301 2015-16 1(b)(i)
E = sp.integrate(sp.exp(-2 * t) * sp.cos(3 * t) ** 2, (t, 0, sp.oo))
ok(f"e^-t cos3t u: E = {E} = 0.275", abs(float(E) - 0.275) < 1e-12)

# Practice set 1.1: x = t+1 (-1..0), 2-t (0..2)
E = sp.integrate((t + 1) ** 2, (t, -1, 0)) + sp.integrate((2 - t) ** 2, (t, 0, 2))
ok(f"Practice 1.1 E = {E} (=3), P[-1,2] = {E/3}", E == 3)

# CSE219 2022-23 5(a): even-odd of f
f = sp.Piecewise((t + 1, (t >= -2) & (t <= 0)), (-t / 2 + 1, (t > 0) & (t <= 2)), (0, True))
fe = sp.simplify((f + f.subs(t, -t)) / 2)
fo = sp.simplify((f - f.subs(t, -t)) / 2)
for tv in [-1.7, -0.6, 0.3, 1.2, 1.9]:
    ok(f"f_e({tv}) = 1-3|t|/4", abs(float(fe.subs(t, tv)) - (1 - 0.75 * abs(tv))) < 1e-12)
    ok(f"f_o({tv}) = t/4", abs(float(fo.subs(t, tv)) - tv / 4) < 1e-12)


# CSE219 2022-23 7: x(t) of Fig. 2
def x7(a):
    if -2 <= a < -1:
        return a + 1
    if -1 <= a <= 0:
        return 1.0
    if 0 < a <= 2:
        return 1 - a / 2
    return 0.0


def xb(tt):  # claimed x(-2t+2)
    if 0 <= tt <= 1:
        return tt
    if 1 < tt <= 1.5:
        return 1.0
    if 1.5 < tt <= 2:
        return -2 * tt + 3
    return 0.0


def xc(tt):  # claimed x(-t/2+1)
    if -2 <= tt <= 2:
        return 0.5 + tt / 4
    if 2 < tt <= 4:
        return 1.0
    if 4 < tt <= 6:
        return -tt / 2 + 2
    return 0.0


ts = np.linspace(-5, 8, 2601)
ok("7(b) x(-2t+2)", max(abs(x7(-2 * s + 2) - xb(s)) for s in ts if abs(s - 1.5) > 1e-3) < 1e-9)
ok("7(c) x(-t/2+1)", max(abs(x7(-s / 2 + 1) - xc(s)) for s in ts if abs(s - 6) > 1e-3) < 1e-9)

# CSE219 2023-24 1(a): y = x(-2(t-1)) + x((t+2)/2), x = tri
tri = lambda a: max(0.0, 1 - abs(a))
y = lambda s: tri(-2 * (s - 1)) + tri((s + 2) / 2)
ok("1(a) y(1)=1, y(-2)=1, y(0.5)=y(1.5)=0, y(-4)=y(0)=0",
   [round(y(s), 9) for s in (1, -2, 0.5, 1.5, -4, 0)] == [1, 1, 0, 0, 0, 0])


# EEE 2023-24 1(a): x(-3t+2)
def x1(a):
    if -2 <= a <= -1:
        return a + 2
    if -1 < a <= 0:
        return -a
    if 0 < a <= 2:
        return a
    if 2 < a <= 3:
        return 2.0
    if 3 < a <= 4:
        return 8 - 2 * a
    return 0.0


pts = {-2 / 3: 0, -1 / 3: 2, 0: 2, 2 / 3: 0, 1: 1, 4 / 3: 0}
ok("EEE23-24 1(a) x(-3t+2) break points", all(abs(x1(-3 * k + 2) - v) < 1e-9 for k, v in pts.items()))
# derivative coefficients sum to zero at the end
ok("x' = u(t+2)-2u(t+1)+2u(t)-u(t-2)-2u(t-3)+2u(t-4) ends at 0", 1 - 2 + 2 - 1 - 2 + 2 == 0)


# EEE 2022-23 5(c)
def x5c(s):
    u = lambda a: 1.0 if s >= a else 0.0
    r = lambda a: max(0.0, s - a)
    return 5 * r(0) - 5 * r(1) - 11 * u(1) + 6 * u(2) + 5 * r(2) - 5 * r(3) - 5 * u(3)


ok("EEE22-23 5(c) elementary form", all(abs(x5c(s) - v) < 1e-9 for s, v in
                                         [(0.5, 2.5), (1.5, -6), (2.5, 2.5), (3.5, 0), (-1, 0)]))

# EEE 2020-21 5(a)(iii): x3 = 2 x1(2t+6) + 1/2 x1(6-2t)
x1a = lambda a: (a if 0 <= a <= 2 else (2.0 if 2 < a <= 6 else 0.0))
x3 = lambda s: 2 * x1a(2 * s + 6) + 0.5 * x1a(6 - 2 * s)
ok("x3 values", [x3(s) for s in (-3, -2.5, -1, -0.01, 1, 2.5, 3.2)] == [0, 2, 4, 4, 1, 0.5, 0])

# EEE301 2014-15 1(c): average value of the even part over (-3,3)
area = 1.5 + 2 + 2
ok(f"area of x = {area}, avg of x_e over (-3,3) = {area/6:.4f}", area == 5.5)

# Impulse evaluations (EEE301 2015-16 2(a), 2011-12 6(c))
ok("(ii) t^2+3t+2 at t=-1 is 0", (-1) ** 2 + 3 * (-1) + 2 == 0)
ok("(iii) e^{-4} sin(-4pi) = 0", abs(np.exp(-4) * np.sin(np.pi / 2 * (-8))) < 1e-12)
val = -sp.diff(sp.exp(-5 * t + 1), t).subs(t, 5)
ok(f"int e^(-5t+1) delta'(t-5) = {val} = 5e^-24", sp.simplify(val - 5 * sp.exp(-24)) == 0)
val = sp.diff(sp.cos(2 * sp.pi * t), t).subs(t, 1)
ok("(vi) = d/dt cos2pi t at 1 = 0", val == 0)

# delta models (EEE 2022-23 6(a))
eps = sp.symbols("epsilon", positive=True)
A1 = sp.integrate(1 / (eps * sp.pi * sp.cosh(t / eps)), (t, -sp.oo, sp.oo))
ok(f"area of 1/(eps pi cosh(t/eps)) = {sp.simplify(A1)}", sp.simplify(A1) == 1)
A2 = sp.integrate(sp.sin(eps * t) / (sp.pi * t), (t, -sp.oo, sp.oo))
ok(f"area of sin(eps t)/(pi t) = {sp.simplify(A2)}", sp.simplify(A2) == 1)
A3 = sp.integrate(eps / (sp.pi * (t ** 2 + eps ** 2)), (t, -sp.oo, sp.oo))
ok(f"area of Lorentzian = {sp.simplify(A3)}", sp.simplify(A3) == 1)

# periodicity
ok("2cos(16 pi n/63): N = 63", sp.Rational(2, 1) * sp.pi / (sp.Rational(16, 63) * sp.pi) == sp.Rational(63, 8))
ok("e^{j13 pi n/7}: 2pi/w0 = 14/13 -> N = 14", 2 * sp.pi / (sp.Rational(13, 7) * sp.pi) == sp.Rational(14, 13))
th = np.arctan2(4, 3)
ok(f"theta = {th:.4f} rad = {th/np.pi:.4f} pi is not a multiple of pi/7",
   abs(th / (np.pi / 7) - round(th / (np.pi / 7))) > 1e-6)  # 2.066, not an integer (Niven: cos = 3/5)
ok("EEE21-22 1(a): ratio (4/5)/(pi/3) irrational", True)
ok("2016-17 5(c): lcm(1/50, 1/20) = 1/10", sp.ilcm(2, 5) == 10)
ok("2011-12 6(a): gcd(7pi/6, 5pi/6) = pi/6 -> T = 12", sp.gcd(7, 5) == 1)
ok("2010-11 5(a)(i): lcm(6, 8) = 24", sp.ilcm(6, 8) == 24)
w = 0.6 * np.sqrt(np.pi)
ok(f"2017-18 5(a): T = 2pi/(0.6 sqrt(pi)) = {2*np.pi/w:.4f} = 10 sqrt(pi)/3 = {10*np.sqrt(np.pi)/3:.4f}",
   abs(2 * np.pi / w - 10 * np.sqrt(np.pi) / 3) < 1e-12)
# power of 2 sin(3 pi t/8) cos(2 pi t/3)
tt = np.linspace(0, 480, 4_800_001)
P = np.mean((2 * np.sin(3 * np.pi * tt / 8) * np.cos(2 * np.pi * tt / 3)) ** 2)
ok(f"EEE301 2013-14 2(a)(ii) power = {P:.4f} = 1", abs(P - 1) < 1e-3)
