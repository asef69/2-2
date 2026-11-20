"""Independent numeric check of every KKS-part answer (probability + ANOVA)."""
import math
import sys
from fractions import Fraction as F
from math import comb, exp, factorial

import sympy as sp
from scipy import stats

sys.path.insert(0, r"C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2\MATH 243\TF Prep\_build")
from m243 import anova1, anova2

sys.stdout.reconfigure(encoding="utf-8")
P = lambda *a: print(*a)
x, y = sp.symbols("x y", real=True)

P("== L2 combinatorics")
P("2013-14 7b(i) different suits:", F(52 * 39 * 26, 52 * 51 * 50), float(F(52 * 39 * 26, 52 * 51 * 50)))
t = comb(20, 3)
P("2014-15 8a:", F(comb(8, 3), t), F(comb(8, 2) * 3, t), 1 - F(comb(17, 3), t), [float(v) for v in (F(comb(8, 3), t), F(comb(8, 2) * 3, t), 1 - F(comb(17, 3), t))])
P("== L3 independence")
P("2011-12 7b(ii):", 1 - F(4, 7) * F(1, 3) * F(1, 5))
q_series = 1 - 0.99 * 0.99
P("2016-17 7a circuit: branch fail series", q_series, "P(not operate)=", 0.02 * q_series * q_series * 0.02)
P("== L5 conditional")
PW, PH, PHgW = 0.35, 0.25, 0.8
both = PW * PHgW
P("2015-16 8a: both", both, "P(H|W')", (PH - both) / (1 - PW))
P("2018-19 6b: both =", 5 + 8 - (20 - 10), "P(not bitten|sun)=", F(2, 5), "P(sun|bitten)=", F(3, 8))
P("== L6 total prob / Bayes")
P("2022-23 1a:", F(4, 7) * F(5, 9) + F(3, 7) * F(6, 9))
P("2023-24 1b:", F(5, 12) * F(8, 12) + F(7, 12) * F(9, 12))
pr = [0.3, 0.45, 0.25]; d = [0.02, 0.03, 0.02]
pd = sum(a * b for a, b in zip(pr, d))
P("2022-23 1b: P(D)=", pd, [a * b / pd for a, b in zip(pr, d)])
pr = [0.45, 0.40, 0.15]; nv = [0.35, 0.20, 0.50]
pn = sum(a * b for a, b in zip(pr, nv))
P("2023-24 1c: P(not vote)=", pn, [a * b / pn for a, b in zip(pr, nv)])
pg = 0.9 * 0.05 + 0.01 * 0.95
P("2019-20 7a: P(judged guilty)=", pg, "P(innocent|G)=", 0.01 * 0.95 / pg)
P("== L8 CDF/pdf, exponential")
f1 = sp.Rational(1, 8)
P("2018-19 7a: P(X>=1.5)=", 1 - sp.Rational(3, 2) / 8, " P(X>=1|X<=3)=", (sp.Rational(9, 16) - sp.Rational(1, 8)) / sp.Rational(9, 16))
k = 1 / sp.integrate((3 - x) ** 2, (x, -1, 1))
P("2020-21 6b: k=", k, " P(X<1/2)=", sp.integrate(k * (3 - x) ** 2, (x, -1, sp.Rational(1, 2))),
  " P(|X|>0.8)=", sp.nsimplify(1 - sp.integrate(k * (3 - x) ** 2, (x, -sp.Rational(4, 5), sp.Rational(4, 5)))),
  float(1 - sp.integrate(k * (3 - x) ** 2, (x, -sp.Rational(4, 5), sp.Rational(4, 5)))))
P("2022-23 1c: P(>1000)=", exp(-0.5), " P(<2000)=", 1 - exp(-1))
P("2023-24 2a: P(X<0.2 h)=", 1 - exp(-8 * 0.2))
lam = 1.8 / 24  # per hour
P("2019-20 8b: (i) 1-e^{-1.8/96}=", 1 - exp(-1.8 / 96), "(ii) same (memoryless)",
  "(iii) e^{-0.75}=", exp(-0.75), "(iv) e^{-3}=", exp(-3), "(v) x=", -math.log(0.9) / lam, "h")
P("== L9 expectation")
P("2018-19 7b: E=", sum(F(xx * comb(4, xx) * comb(3, 3 - xx), comb(7, 3)) for xx in range(4)))
P("2019-20 7b: E(e^{2X/3})=", sp.integrate(sp.exp(2 * x / 3) * sp.exp(-x), (x, 0, sp.oo)))
EX = sp.integrate(x * 32 / (x + 4) ** 3, (x, 0, sp.oo))
P("2020-21 8a: E(X)=", EX, " E(Y)=", EX + 4, " check ∫f=", sp.integrate(32 / (x + 4) ** 3, (x, 0, sp.oo)))
P("2022-23 2b: E(X)=4 Var=16 → E(Y)=", 3 * 4 - 2, "Var(Y)=", 9 * 16)
mu = sp.integrate(x * 6 * x * (1 - x), (x, 0, 1)); var = sp.integrate(x ** 2 * 6 * x * (1 - x), (x, 0, 1)) - mu ** 2
sd = sp.sqrt(var)
lo, hi = sp.Max(0, mu - 2 * sd), sp.Min(1, mu + 2 * sd)
pp = sp.integrate(6 * x * (1 - x), (x, mu - 2 * sd, mu + 2 * sd))
P("2022-23 2c: mu=", mu, "var=", var, "sd=", sp.N(sd), "limits", sp.N(mu - 2 * sd), sp.N(mu + 2 * sd), "P=", sp.nsimplify(pp), sp.N(pp))
P("2023-24 3a: k=(84-60)/6=4 → P(X<84)>=1-1/(2*16) =", 1 - F(1, 32), "upper tail <=", F(1, 32), "→ ≤ 31.25 of 1000 above 84 ... ", 1000 / 32)
P("== L10–L11 joint")
num = sp.integrate((6 - 2 - y), (y, 2, 3)); den = sp.integrate((6 - 2 - y), (y, 2, 4))
P("2012-13 8a: P(1<Y<3|x=2)=", num / den)
kk = 1 / sp.integrate(sp.integrate(x ** 2 + y ** 2, (x, 30, 50)), (y, 30, 50))
P("2020-21 5c: k=", kk, " P(30<X<40,40<Y<50)=", sp.integrate(sp.integrate(kk * (x ** 2 + y ** 2), (x, 30, 40)), (y, 40, 50)),
  float(sp.integrate(sp.integrate(kk * (x ** 2 + y ** 2), (x, 30, 40)), (y, 40, 50))),
  " both under 40:", sp.integrate(sp.integrate(kk * (x ** 2 + y ** 2), (x, 30, 40)), (y, 30, 40)),
  float(sp.integrate(sp.integrate(kk * (x ** 2 + y ** 2), (x, 30, 40)), (y, 30, 40))))
f = 10 * x * y ** 2
gx = sp.integrate(f, (y, x, 1)); hy = sp.integrate(f, (x, 0, y))
fyx = sp.simplify(f / gx)
P("2022-23 2a: g=", sp.factor(gx), " h=", hy, " f(y|x)=", fyx, " P(Y>1/2|x=1/4)=",
  sp.integrate(fyx.subs(x, sp.Rational(1, 4)), (y, sp.Rational(1, 2), 1)), float(sp.integrate(fyx.subs(x, sp.Rational(1, 4)), (y, sp.Rational(1, 2), 1))))
# pens 3 red, 2 blue, 3 black choose 2
J = {(a, b): F(comb(3, a) * comb(2, b) * comb(3, 2 - a - b), comb(8, 2)) for a in range(3) for b in range(3) if a + b <= 2}
P("2023-24 2b joint:", J)
P("  P(x+y<=1)=", sum(v for (a, b), v in J.items() if a + b <= 1))
gX = {a: sum(v for (aa, b), v in J.items() if aa == a) for a in range(3)}
hY = {b: sum(v for (a, bb), v in J.items() if bb == b) for b in range(3)}
EXd = sum(a * v for a, v in gX.items()); EX2 = sum(a * a * v for a, v in gX.items())
EYd = sum(b * v for b, v in hY.items()); EXY = sum(a * b * v for (a, b), v in J.items())
P("  g=", gX, " h=", hY, " E(X)=", EXd, " Var(X)=", EX2 - EXd ** 2, " E(Y)=", EYd, " E(XY)=", EXY, " Cov=", EXY - EXd * EYd)
P("== L13 binomial")
B = stats.binom
P("2013-14 7b(ii): P(X>=4)=", B.sf(3, 12, 0.1))
P("2014-15 8b:", 0.6 ** 5, 1 - 0.6 ** 5, 0.4 ** 5)
P("2020-21 7a: mean", 200 * 0.03, "var", 200 * 0.03 * 0.97, "P0=", 0.97 ** 200, "(Poisson e^-6=", exp(-6), ")")
P("2023-24 3c: P(>=10)=", B.sf(9, 15, 0.4), " P(3..8)=", B.cdf(8, 15, 0.4) - B.cdf(2, 15, 0.4), " P(5 die = 10 survive)=", B.pmf(10, 15, 0.4))
P("2012-13 6b binom: P(4..7)=", B.cdf(7, 18, 0.2) - B.cdf(3, 18, 0.2), " P(<3)=", B.cdf(2, 18, 0.2), " P(>5)=", B.sf(5, 18, 0.2))
Po = stats.poisson
P("            Poisson λ=3.6: P(4..7)=", Po.cdf(7, 3.6) - Po.cdf(3, 3.6), " P(<3)=", Po.cdf(2, 3.6), " P(>5)=", Po.sf(5, 3.6))
P("== L14 Poisson")
P("2011-12 7b(i): λ=0.5 P(X>=5)=", Po.sf(4, 0.5), " binom", B.sf(4, 1000, 0.0005))
P("2016-17 8a: λ=2 P1=", Po.pmf(1, 2), " P<=3=", Po.cdf(3, 2))
P("2019-20 8a: λ=8 P<7=", Po.cdf(6, 8))
P("2022-23 3b: λ=10 P(6,7,8)=", Po.pmf(6, 10) + Po.pmf(7, 10) + Po.pmf(8, 10), [Po.pmf(i, 10) for i in (6, 7, 8)])
P("2023-24 3b: λ=2.5 P2=", Po.pmf(2, 2.5))
P("== L15 other discrete")
P("2020-21 6c: geometric (1/3)^4(2/3)=", F(1, 3) ** 4 * F(2, 3), float(F(1, 3) ** 4 * F(2, 3)),
  " neg.bin C(4,2)(2/3)^3(1/3)^2=", comb(4, 2) * F(2, 3) ** 3 * F(1, 3) ** 2, float(comb(4, 2) * F(2, 3) ** 3 * F(1, 3) ** 2))
hyp = sum(F(comb(200, i) * comb(300, 5 - i), comb(500, 5)) for i in range(3, 6))
P("2021-22 6a hypergeom P(>=3)=", float(hyp), " binomial approx p=.4:", B.sf(2, 5, 0.4))
P("2021-22 6b multinomial:", factorial(9) / (factorial(3) * factorial(3) * factorial(1) * factorial(2)) * 0.4 ** 3 * 0.2 ** 3 * 0.3 * 0.1 ** 2)
P("2021-22 6c:", [F(comb(2, i) * comb(3, 3 - i), comb(5, 3)) for i in range(3)])
P("== L16–L17 normal")
N = stats.norm
P("2014-15 8c: z=1.2 P=", N.cdf(1.2), " count", 2000 * N.cdf(1.2))
# 2015-16 8b: (65-mu)/s = z(0.10)=-1.28 ; (75-mu)/s = z(0.75)=0.67
z1, z2 = -1.28, 0.67
s = (75 - 65) / (z2 - z1); m = 65 - z1 * s
P("2015-16 8b: sigma=", s, " mu=", m, " P(60<X<74)=", N.cdf((74 - m) / s) - N.cdf((60 - m) / s), " zs:", (60 - m) / s, (74 - m) / s)
zz1, zz2 = N.ppf(0.10), N.ppf(0.75)
s_ = 10 / (zz2 - zz1); m_ = 65 - zz1 * s_
P("     exact z: sigma", s_, "mu", m_, "P", N.cdf((74 - m_) / s_) - N.cdf((60 - m_) / s_))
P("2018-19 8a: P(<90)=", N.cdf(-1.5), " count", 1000 * N.cdf(-1.5), " 10% point:", 120 + 20 * N.ppf(0.1), "(table z -1.28 →", 120 - 1.28 * 20, ")")
P("2020-21 7b: P(>32)=", N.sf((32 - 40) / 6.3), " z", (32 - 40) / 6.3, " P(37..49)=", N.cdf((49 - 40) / 6.3) - N.cdf((37 - 40) / 6.3), (37 - 40) / 6.3, (49 - 40) / 6.3)
P("2021-22 7b: scrapped", 2 * N.cdf(-2))
P("2022-23 3c: P(>=30)=", N.sf(6 / 3.8), "z", 6 / 3.8, " late (>15)", N.sf((15 - 24) / 3.8), "z", (15 - 24) / 3.8,
  " slowest 15%:", 24 + 3.8 * N.ppf(0.85), " 2 of 3:", 3 * N.sf(6 / 3.8) ** 2 * (1 - N.sf(6 / 3.8)))
P("2023-24 4a: P(778<X<834)=", N.cdf(34 / 40) - N.cdf(-22 / 40), " z", -22 / 40, 34 / 40)
sdD = math.sqrt(0.1 ** 2 + 2 * 0.05 ** 2)
P("2016-17 7b: mean D=6 sd=", sdD, " P(D<5.9)=", N.cdf((5.9 - 6) / sdD), " z", (5.9 - 6) / sdD)
se = 0.048 / 6; fpc = math.sqrt((1500 - 36) / (1500 - 1)); se2 = se * fpc
P("2016-17 7c: se with repl", se, " without", se2)
for s_e in (se, se2):
    a = N.cdf(0.01 / s_e) - N.cdf(-0.01 / s_e); b = N.sf(0.02 / s_e); c = N.cdf(-0.02 / s_e) + N.sf(0.01 / s_e)
    P("    z(0.01)=", 0.01 / s_e, " (i)", a, 300 * a, " (ii)", b, 300 * b, " (iii)", c, 300 * c)
P("== L18–L19 ANOVA")
for name, gr in (("2021-22 8b", [[300, 400, 300, 500, 0], [600, 300, 300, 400], [700, 300, 400, 600, 500]]),
                 ("2022-23 8b", [[20, 19, 21], [25, 23, 21], [24, 20, 22], [23, 20, 20]]),
                 ("2023-24 8b", [[15, 18, 23, 24], [23, 19, 18, 24], [19, 16, 22, 31]]),
                 ("deck reactor", [[72, 75, 78, 74, 76], [65, 68, 70, 72, 69], [78, 82, 85, 88, 90]])):
    a = anova1(gr)
    P(name, {k_: (round(v, 4) if isinstance(v, float) else v) for k_, v in a.items()})
a2 = anova2([[12, 15, 10, 14], [15, 19, 12, 11], [14, 18, 15, 12], [11, 16, 12, 16], [16, 17, 11, 14]])
P("2022-23 8c", {k_: (v.tolist() if hasattr(v, "tolist") else (round(v, 4) if isinstance(v, float) else v)) for k_, v in a2.items()})
