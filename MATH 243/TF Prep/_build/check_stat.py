"""Numeric check of every Statistics-part answer (independent of the note scripts where possible)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

from m243 import Grouped, regression, spearman_ties, summary

sys.stdout.reconfigure(encoding="utf-8")


def show(name, G):
    (m1, m2, m3, m4), (_, u2, u3, u4) = G.central()
    b1, b2, g1, g2 = G.beta_gamma()
    mo = G.mode()[0]; me = G.median()[0]
    q1 = G.quantile(1)[0]; q3 = G.quantile(3)[0]
    print(f"{name}: N={G.N} A={G.A} sums={G.s[1:]} mean={G.mean:.4f} median={me:.4f} mode={mo:.4f} sd={G.sd:.4f} "
          f"cv={G.cv:.2f} Q1={q1:.4f} Q3={q3:.4f} raw={[round(v,4) for v in (m1,m2,m3,m4)]} mu={[round(v,4) for v in (u2,u3,u4)]} "
          f"b1={b1:.4f} b2={b2:.4f} g1={g1:.4f} g2={g2:.4f} SKp={(G.mean-mo)/G.sd:.4f} SKp2={3*(G.mean-me)/G.sd:.4f} "
          f"bowley={(q3+q1-2*me)/(q3-q1):.4f}")


cl = lambda a, h, k: [(a + i * h, a + (i + 1) * h) for i in range(k)]
show("profits 18,20,30,22,10", Grouped(cl(10, 10, 5), [18, 20, 30, 22, 10]))
show("174,86,32,181,27", Grouped(cl(10, 10, 5), [174, 86, 32, 181, 27]))
show("age 83..54 (boundaries 20.5)", Grouped(cl(20.5, 6, 6), [83, 75, 176, 130, 92, 54]))
show("earnings", Grouped(cl(50, 20, 7), [4, 8, 12, 20, 6, 7, 3], A=120))
show("marks 0-70 2023-24", Grouped(cl(0, 10, 7), [8, 12, 20, 30, 15, 10, 5]))
show("weights bowley 2020-21", Grouped(cl(30, 10, 6), [18, 37, 45, 27, 15, 8]))
Gw = Grouped(cl(30, 10, 6), [18, 37, 45, 27, 15, 8])
d1, d9 = Gw.quantile(1, 10)[0], Gw.quantile(9, 10)[0]; d5 = Gw.quantile(5, 10)[0]
print("  Kelly D1 D5 D9", d1, d5, d9, (d9 + d1 - 2 * d5) / (d9 - d1))
show("CV profits 2019-20", Grouped(cl(20, 10, 8), [4, 8, 18, 30, 15, 10, 8, 7]))
for nm, f in (("fridge A", [5, 16, 13, 7, 5, 4]), ("fridge B", [2, 7, 12, 19, 9, 1])):
    show(nm, Grouped(cl(0, 2, 6), f))
for nm, f in (("wages A", [15, 30, 44, 60, 30, 14, 7]), ("wages B", [25, 40, 60, 35, 20, 15, 5])):
    show(nm, Grouped(cl(20, 10, 7), f))
for nm, f in (("bulb A", [10, 16, 20, 8, 6]), ("bulb B", [3, 40, 12, 3, 2])):
    show(nm, Grouped(cl(1700, 200, 5), f))
# missing frequencies
for med in (413.11, 415):
    # classes 300..500 width 25; f1=x (375-400), f2=y (425-450); x+y = 1000-525 = 475
    # median class 400-425: med = 400 + (500 - (102 + x))/326*25
    x = 500 - 102 - (med - 400) * 326 / 25
    y = 475 - x
    fs = [5, 17, 80, x, 326, y, 88, 9]
    G = Grouped(cl(300, 25, 8), fs)
    print("missing med", med, "x=", x, "y=", y, "mode", G.mode()[0], "mean", G.mean, "sd", G.sd)
# ungrouped CV
for nm, d in (("A time", [130, 124, 119, 134, 142, 130, 141]), ("B time", [132, 144, 136, 143, 132, 133, 140]),
              ("X marks", [58, 59, 60, 54, 65, 66, 52, 75, 69, 52]), ("Y marks", [87, 89, 78, 71, 73, 84, 65, 66, 56, 46]),
              ("runs A", [55, 80, 78, 49, 52, 76, 78, 76, 62, 76]), ("runs B", [54, 78, 55, 66, 63, 69, 74, 64, 59, 85])):
    s = summary(d); print(nm, {k: round(float(v), 4) for k, v in s.items()})
b = np.sort([54, 78, 55, 66, 63, 69, 74, 64, 59, 85]); print("runs B sorted", b)
xb = b.mean(); dev = b - xb
m2, m3, m4 = (dev ** 2).mean(), (dev ** 3).mean(), (dev ** 4).mean()
print("runs B m2 m3 m4", m2, m3, m4, "b1", m3 ** 2 / m2 ** 3, "b2", m4 / m2 ** 2)
print("shares CV", [5.4 / 18 * 100, 4.5 / 22.5 * 100, 6 / 24 * 100])
# corrected mean/sd
n_, m_, s_ = 200, 60, 20
S1 = n_ * m_ - (3 + 67) + (13 + 17); S2 = n_ * (s_ ** 2 + m_ ** 2) - (9 + 4489) + (169 + 289)
cm = S1 / n_; cs = math.sqrt(S2 / n_ - cm ** 2); print("corrected", S1, S2, cm, cs, cs / cm * 100)
# regression
for nm, x, y in (("2011-12", [105, 112, 104, 114, 117, 108, 106, 117, 111], [58, 56, 47, 46, 51, 64, 66, 50, 55]),
                 ("2012-13 econ(x) bus(y)", [47, 38, 34, 44, 32, 41, 35, 32, 42, 30], [38, 34, 42, 39, 34, 33, 30, 41, 38, 28]),
                 ("2013-14 husb wife", [22, 25, 28, 31, 35, 32, 37, 39], [19, 18, 22, 29, 31, 23, 30, 33]),
                 ("2014-15", [42, 44, 58, 55, 89, 98, 66], [56, 49, 53, 58, 65, 76, 51]),
                 ("2015-16 service income", [10, 8, 9, 5, 7, 6, 12, 11, 13], [17, 12, 14, 8, 10, 9, 20, 18, 22]),
                 ("exp rating", [16, 12, 18, 4, 3], [87, 88, 89, 68, 58]),
                 ("transmitter paper", [13, 12, 17, 19, 14, 15, 15, 8, 13, 3], [34.4, 38.4, 30.4, 29.7, 30.1, 33.9, 32.8, 35.2, 34.9, 36.8]),
                 ("transmitter deck", [13, 1, 17, 19, 14, 15, 15, 8, 13, 3], [34.4, 38.4, 30.4, 29.7, 30.1, 33.9, 32.8, 35.2, 34.9, 36.8]),
                 ("pines", [0.414, 0.383, 0.399, 0.402, 0.442, 0.422, 0.466, 0.500, 0.514, 0.530, 0.569, 0.558, 0.577, 0.572, 0.548],
                  [29186, 29266, 26215, 30162, 38867, 37831, 44576, 46097, 59698, 67705, 66088, 78486, 89869, 77369, 67095]),
                 ("2022-23 husb wife", [22, 23, 23, 24, 26, 27, 27, 28, 30, 30], [18, 20, 21, 20, 21, 22, 23, 24, 25, 26]),
                 ("sales exp", [50, 50, 55, 60, 65, 65, 65, 60, 60, 50], [11, 13, 14, 16, 16, 15, 15, 14, 13, 13]),
                 ("restaurants", [22, 29, 15, 18, 23], [3.5, 4.0, 3.0, 4.0, 3.5]),
                 ("hardness", [146, 152, 158, 164, 170], [75, 78, 77, 89, 82])):
    r = regression(x, y)
    yh = r["ayx"] + r["byx"] * np.array(x, float)
    ssr = ((yh - r["yb"]) ** 2).sum()
    print(nm, {k: round(float(v), 4) for k, v in r.items()}, "SSR", round(ssr, 4), "SST", round(r["syy"], 4), "R2", round(ssr / r["syy"], 4))
r = 0.62; print("capacity on prod: b=", r * 8.5 / 10.5, " prod on cap b=", r * 10.5 / 8.5, " prod at 70:", 35.6 + r * 10.5 / 8.5 * (70 - 84.8))
for nm, x, y in (("bangla eng", [15, 20, 28, 12, 40, 60, 20, 80], [40, 30, 50, 30, 20, 10, 30, 60]),
                 ("sales exp", [50, 50, 55, 60, 65, 65, 65, 60, 60, 50], [11, 13, 14, 16, 16, 15, 15, 14, 13, 13]),
                 ("managers", [10, 2, 1, 4, 3, 6, 5, 8, 7, 9], [9, 4, 2, 3, 1, 5, 6, 8, 7, 10])):
    s = spearman_ties(x, y); print(nm, s)
X = np.array([0, 1, 2, 3, 4, 5.]); Y = np.array([15, 25, 40, 55, 52, 43.])
c = np.polyfit(X, Y, 2); yh = np.polyval(c, X)
print("poly", c[::-1], "R2", 1 - ((Y - yh) ** 2).sum() / ((Y - Y.mean()) ** 2).sum(), "sums", X.sum(), (X**2).sum(), (X**3).sum(), (X**4).sum(), Y.sum(), (X*Y).sum(), (X*X*Y).sum())
# pencils
p = sorted([17.2, 16.4, 18.6, 17.4, 17.5, 19.0, 17.4, 16.8, 19.0, 17.8, 18.8, 18.7]); print("pencils", p, np.median(p))
# thickness Sturges
t = [18, 21, 22, 29, 25, 31, 37, 38, 41, 39, 44, 48, 54, 56, 56, 57, 47, 38, 35, 36, 29, 37, 32, 42, 43, 40, 48, 36, 37, 37,
     36, 38, 40, 41, 44, 39, 38, 34, 24, 32, 39, 44, 42, 30, 37, 30, 42, 37, 34, 37, 32, 24, 42, 36, 49, 39, 23, 34, 36, 40]
print("thick n", len(t), min(t), max(t), "K", 1 + 3.322 * math.log10(len(t)))
edges = [17.5 + 6 * i for i in range(8)]
print("freq w=6 from 17.5", np.histogram(t, bins=edges)[0], edges)
# wages ogive 2021-22
Gm = Grouped([(1900, 1950), (1950, 2000), (2000, 2050), (2050, 2100), (2100, 2150), (2150, 2200), (2200, 2400)],
             [6, 10, 22, 30, 16, 12, 15], h=50)
cf = Gm.cum(); print("wages cum", cf, "N", Gm.N)
pos = Gm.N / 2; print("median pos", pos)
# 2000-2170: 22+30+16 + 12*(20/50)
print("between 2000 and 2170", 22 + 30 + 16 + 12 * 20 / 50)
