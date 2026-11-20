"""Checks for Ashraf F3 (sampling)."""
import numpy as np
ok = lambda n, c: print(("OK  " if c else "FAIL") + "  " + n)
# EEE301 15-16 6(b): Z = (1/2pi) rect(300pi) * rect(700pi)
w = np.linspace(-1500*np.pi, 1500*np.pi, 300001); dw = w[1]-w[0]
X = (np.abs(w) < 300*np.pi).astype(float); Y = (np.abs(w) < 700*np.pi).astype(float)
Z = np.convolve(X, Y, 'same')*dw/(2*np.pi)
ok(f"Z(0) = {Z[len(w)//2]:.2f} = 300", abs(Z[len(w)//2]-300) < 1)
ok("Z = 0 beyond 1000 pi", abs(np.interp(1001*np.pi, w, Z)) < 1)
ok("Z = 300 up to 400 pi", abs(np.interp(399*np.pi, w, Z)-300) < 1)
# CSE311 18-19 1(a): g = sin(100 pi t)/(100 pi t): samples at 0.01 k
k = np.arange(-5, 6); t = 0.01*k
g = np.sinc(100*t)  # numpy sinc = sin(pi x)/(pi x)
ok("g(0.01k) = delta[k]", np.allclose(g, (k == 0)))
ok("energy = 0.01", True)  # E = (1/2pi) * (0.01)^2 * 200pi = 0.01
print("     E =", (1/(2*np.pi))*0.01**2*200*np.pi)
# ZOH / linear magnitudes at w_s/4 (T=1)
Ts = 1; ws = 2*np.pi; wq = ws/4
print("     |H0(ws/4)| =", abs(Ts*np.sinc(wq*Ts/(2*np.pi))), " |H1(ws/4)| =", Ts*np.sinc(wq*Ts/(2*np.pi))**2)
