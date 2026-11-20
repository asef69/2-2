"""Checks for Anik F3 (Fourier series)."""
import numpy as np

ok = lambda name, cond: print(("OK  " if cond else "FAIL") + "  " + name)


def fs(x, T, k, N=200000):
    t = (np.arange(N) + 0.5) * T / N
    return np.mean(x(t) * np.exp(-1j * k * 2 * np.pi / T * t))


# Lec5 square wave T1 = T/4
T = 4.0
sq = lambda t: (np.mod(t + 1, 4) < 2).astype(float)
ok("square a1 = 1/pi", abs(fs(sq, T, 1) - 1 / np.pi) < 1e-4)
ok("square a3 = -1/(3pi)", abs(fs(sq, T, 3) + 1 / (3 * np.pi)) < 1e-4)
# ramp T = 3
ramp = lambda t: np.where(t < 1, t, (3 - t) / 2)
w0 = 2 * np.pi / 3
for k in (1, 2):
    ok(f"ramp a{k} = (e^-jkw0 - 1)/(2k^2w0^2)", abs(fs(ramp, 3, k) - (np.exp(-1j * k * w0) - 1) / (2 * k * k * w0 * w0)) < 1e-5)  # slide 40 prints 6: sign slip in sl. 39
# sawtooth a_k = j/(2 pi k)
ok("sawtooth a1 = j/2pi", abs(fs(lambda t: t, 1, 1) - 1j / (2 * np.pi)) < 1e-4)
# CSE219 23-24 Q4: odd square wave, y = x(t - T0/6)
A = 1.0
x4 = lambda t: np.where(np.mod(t, 1) < 0.5, A, -A)
y4 = lambda t: x4(t - 1 / 6)
for k in (1, 3, 5):
    Yk = fs(y4, 1, k)
    claim = 2 * A / (1j * np.pi * k) * np.exp(-1j * k * np.pi / 3)
    ok(f"Y_{k} |{abs(Yk):.4f}| angle {np.degrees(np.angle(Yk)):.1f}", abs(Yk - claim) < 1e-4)
ok("Y_2 = 0", abs(fs(y4, 1, 2)) < 1e-4)
# EEE 20-21 7(a): x = 1 - |t| on [-2,2] periodic 4; y = 2 - 2x'
xt = lambda t: 1 - np.abs(np.mod(t + 2, 4) - 2)
ok("tri a1 = 4/pi^2", abs(fs(xt, 4, 1) - 4 / np.pi ** 2) < 1e-5)
ok("tri a2 = 0", abs(fs(xt, 4, 2)) < 1e-5)
yt = lambda t: 4.0 * (np.mod(t, 4) < 2)
ok("y b1 = -4j/pi", abs(fs(yt, 4, 1) + 4j / np.pi) < 1e-4)
ok("y b0 = 2", abs(fs(yt, 4, 0) - 2) < 1e-4)
# EEE 19-20 8(b): x = A(2|t|-1), period 2; a_n = -8A/(n^2 pi^2) odd (trig)
x8 = lambda t: 2 * np.abs(np.mod(t + 1, 2) - 1) - 1
ok("trig a1 = -8/pi^2", abs(2 * fs(x8, 2, 1).real + 8 / np.pi ** 2) < 1e-5)
ok("trig a3 = -8/(9pi^2)", abs(2 * fs(x8, 2, 3).real + 8 / (9 * np.pi ** 2)) < 1e-5)
# EEE 21-22 3(a): a_k = e^{-jk pi/2}/4 + j(1-(-1)^k)/(k pi); impulse handled analytically
for k in (1, 2, 3):
    rect_part = fs(lambda t: 2.0 * (t >= 2), 4, k)
    ak = np.exp(-1j * k * np.pi / 2) / 4 + rect_part
    claim = np.exp(-1j * k * np.pi / 2) / 4 + 1j * (1 - (-1) ** k) / (k * np.pi)
    ok(f"3(a) a_{k} = {ak:.4f}", abs(ak - claim) < 1e-4)
L, C, R = 0.1, 100e-6, 1e3
H = lambda w: 1 / (1 - w * w * L * C + 1j * w * L / R)
print("     |H(k pi/2)| k=1..3:", [round(abs(H(k * np.pi / 2)), 5) for k in (1, 2, 3)])
# EEE 20-21 7(b)
H2 = lambda w: 1 / (2 + 1j * w)
P = 0.5 * (4 * abs(H2(1)) ** 2 + 36 * abs(H2(3)) ** 2)
ok(f"7(b) P = {P:.4f}", abs(P - 0.5 * (4 / 5 + 36 / 13)) < 1e-12)
print("     phases", np.degrees(np.angle(H2(1))), np.degrees(np.angle(H2(3))))
# EEE 19-20 5(b): |sin t| into 1/(1+3jw)
for k in (1, 2):
    c = 4 / (np.pi * (4 * k * k - 1)) * abs(1 / (1 + 3j * 2 * k))
    print(f"     5(b) k={k}: amplitude {c:.5f}, phase {-np.degrees(np.arctan(6*k)):.2f}")
full = lambda t: np.abs(np.sin(t))
ok("|sin| a1(trig) = -4/(3pi)", abs(2 * fs(full, np.pi, 1).real + 4 / (3 * np.pi)) < 1e-5)
# EEE 23-24 7(b): half-wave rectified sine
hw = lambda t: np.where(np.mod(t, 1) < 0.5, np.sin(2 * np.pi * t), 0)
ok("hw a0 = 1/pi", abs(fs(hw, 1, 0) - 1 / np.pi) < 1e-5)
ok("hw a1 = -j/4", abs(fs(hw, 1, 1) + 0.25j) < 1e-5)
ok("hw a2 = -1/(3pi)", abs(fs(hw, 1, 2) + 1 / (3 * np.pi)) < 1e-5)
ok("hw a3 = 0", abs(fs(hw, 1, 3)) < 1e-5)
# EEE 22-23 5(a)
ok("3cos+4sin = 5cos(2t - 53.13)", abs(np.degrees(np.arctan2(4, 3)) - 53.13) < 0.01)
# 13-14 3(b): triangle 0..pi, peak 2
trig = lambda t: np.where(np.mod(t, np.pi) < np.pi / 2, 4 / np.pi * np.mod(t, np.pi), 4 - 4 / np.pi * np.mod(t, np.pi))
c1 = fs(trig, np.pi, 1)
ok(f"13-14 3(b) c0 = 1, c1 = {c1:.5f} = -4/pi^2", abs(fs(trig, np.pi, 0) - 1) < 1e-5 and abs(c1 + 4 / np.pi ** 2) < 1e-5)
ok("c2 = 0", abs(fs(trig, np.pi, 2)) < 1e-5)
# 12-13 4(b): half-wave cos amplitudes of 2nd, 4th harmonics
hc = lambda t: np.maximum(np.cos(t), 0)
for k, v in ((2, 2 / (3 * np.pi)), (4, 2 / (15 * np.pi))):
    ok(f"half-wave cos harmonic {k} amplitude {2*abs(fs(hc, 2*np.pi, k)):.5f}", abs(2 * abs(fs(hc, 2 * np.pi, k)) - v) < 1e-5)
# 15-16 4(b)
z = lambda t: np.cos(4 * np.pi * t) * np.sin(4 * np.pi * t)
ok("z c2 = 1/(4j)", abs(fs(z, 0.5, 2) - 1 / 4j) < 1e-6)
