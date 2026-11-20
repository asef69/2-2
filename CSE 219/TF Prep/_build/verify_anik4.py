"""Checks for Anik F4 (Fourier transform)."""
import numpy as np
import sympy as sp

ok = lambda name, cond: print(("OK  " if cond else "FAIL") + "  " + name)
t, w = sp.symbols("t omega", real=True)
a = sp.symbols("a", positive=True)


def ft_num(x, wv, lo=-60, hi=60, N=1_200_001):
    tt = np.linspace(lo, hi, N)
    dt = tt[1] - tt[0]
    return np.sum(x(tt) * np.exp(-1j * wv * tt)) * dt


# rect, shifted rect, Lego (Lec 7)
X = ft_num(lambda s: ((s > 4) & (s < 10)).astype(float), 1.3)
ok("rect(4,10) = e^{-j7w} 2 sin3w / w", abs(X - np.exp(-7j * 1.3) * 2 * np.sin(3.9) / 1.3) < 1e-3)
lego = lambda s: ((s > 1) & (s < 4)) + 0.5 * ((s > 2) & (s < 3))
X = ft_num(lambda s: lego(s).astype(float), 0.7)
ok("Lego", abs(X - np.exp(-2.5j * 0.7) * (2 * np.sin(1.05) / 0.7 + np.sin(0.35) / 0.7)) < 1e-3)
# e^{-at}u, e^{-a|t|}, sign
ok("F{e^-at u} = 1/(a+jw)", sp.simplify(sp.integrate(sp.exp(-a * t) * sp.exp(-sp.I * w * t), (t, 0, sp.oo), conds="none")
                                        - 1 / (a + sp.I * w)) == 0)
ok("1/(a+jw) - 1/(a-jw) -> 2/(jw) as a->0", sp.limit(1 / (a + sp.I * w) - 1 / (a - sp.I * w), a, 0) == 2 / (sp.I * w))
# Parseval I(a) = 1/(16 pi^2 a)
f = sp.symbols("f", real=True)
I = sp.integrate(f ** 2 / (a ** 2 + (2 * sp.pi * f) ** 2) ** 2, (f, -sp.oo, sp.oo))
ok(f"I(a) = {sp.simplify(I)}", sp.simplify(I - 1 / (16 * sp.pi ** 2 * a)) == 0)
# CSE219 22-23 5(b): x1 = 3 dx/dt, x = sin 3pi t/(pi t)
xs = sp.sin(3 * sp.pi * t) / (sp.pi * t)
x1 = sp.simplify(3 * sp.diff(xs, t))
claim = 3 * (3 * sp.pi * t * sp.cos(3 * sp.pi * t) - sp.sin(3 * sp.pi * t)) / (sp.pi * t ** 2)
ok("x1(t)", sp.simplify(x1 - claim) == 0)
wv = 2.0
X1 = 1 / (2 * np.pi) * 0  # check inverse numerically: x1(t0) = (1/2pi) int_{-3pi}^{3pi} 3jw e^{jwt0} dw
t0 = 0.37
ww = np.linspace(-3 * np.pi, 3 * np.pi, 400001)
val = np.trapezoid(3j * ww * np.exp(1j * ww * t0), ww) / (2 * np.pi)
ok("x1 numeric inverse FT", abs(val - float(claim.subs(t, t0))) < 1e-6)
# EEE 22-23 2(a): ramp 0..1, flat 1..2
xr = lambda s: np.clip(s, 0, 1) * (s < 2) * (s > 0)
for wv in (0.9, 2.3):
    Xc = (np.exp(-1j * wv) - 1) / wv ** 2 + 1j * np.exp(-2j * wv) / wv
    ok(f"EEE22-23 2(a) X({wv})", abs(ft_num(lambda s: xr(s).astype(float) if hasattr(xr(s), 'astype') else xr(s), wv) - Xc) < 1e-3)
# EEE 22-23 2(b) energy fraction
u = sp.symbols("u")
ok("int_0^.5 (1-u)^2 = 7/24", sp.integrate((1 - u) ** 2, (u, 0, sp.Rational(1, 2))) == sp.Rational(7, 24))
# EEE 20-21 2(c): y = PF of 2/((s+2)^3 (s+4))
s = sp.symbols("s")
pf = sp.apart(2 / ((s + 2) ** 3 * (s + 4)), s)
print("     2(c) PF:", pf)
yt = sp.inverse_laplace_transform(2 / ((s + 2) ** 3 * (s + 4)), s, t)
ok(f"2(c) y = {sp.simplify(yt)}", sp.simplify(yt - (-sp.exp(-4 * t) / 4 + sp.exp(-2 * t) / 4 - t * sp.exp(-2 * t) / 2
                                                    + t ** 2 * sp.exp(-2 * t) / 2) * sp.Heaviside(t)) == 0)
# EEE 18-19 2(b): alpha for half energy
al = sp.symbols("alpha", positive=True)
Ey = sp.integrate(1 / (al ** 2 + w ** 2), (w, -2, 2)) / (2 * sp.pi)
ok("alpha = 2 gives half energy", sp.simplify(Ey.subs(al, 2) - sp.Rational(1, 2) / (2 * 2)) == 0)
# EEE 16-17 6(b) energy = 10
ok("energy = 10", abs((1 / (2 * np.pi)) * 2 * 0.25 * 40 * np.pi - 10) < 1e-12)
# EEE 23-24 6(a): impulse pattern +1 at 1,2; -1 at 3,4 (period 4)
for k in range(-3, 6):
    ak = 0.25 * (np.exp(-1j * k * np.pi / 2) + np.exp(-1j * k * np.pi) - np.exp(-1.5j * k * np.pi) - 1)
    print(f"     a_{k} = {ak:.4f}  |a|={abs(ak):.4f}  angle={np.degrees(np.angle(ak)) if abs(ak)>1e-9 else 0:.1f}")
# EEE301 2013-14 7(c)
tau = sp.symbols("tau")
yc = sp.integrate((sp.exp(-tau / 4) / 12 + sp.exp(-tau / 2) / 6) * sp.exp(-(t - tau) / 3), (tau, 0, t))
ok(f"y = {sp.simplify(yc)}", sp.simplify(yc - (sp.exp(-t / 4) - sp.exp(-t / 2))) == 0)
