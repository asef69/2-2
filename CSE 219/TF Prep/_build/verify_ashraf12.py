"""Checks + intermediate tables for Ashraf F1 (DTFT/DFT) and F2 (FFT)."""
import numpy as np

np.set_printoptions(precision=4, suppress=True)
ok = lambda name, cond: print(("OK  " if cond else "FAIL") + "  " + name)
c = lambda z: f"{z.real:+.4f}{z.imag:+.4f}j"

ok("DFT {1,2,3,4}", np.allclose(np.fft.fft([1, 2, 3, 4]), [10, -2 + 2j, -2, -2 - 2j]))
ok("Parseval 30", np.isclose(sum(np.abs(np.fft.fft([1, 2, 3, 4])) ** 2) / 4, 30))
x = np.array([2, 4, 5, 6, 5, 3, 2, 1]); h = np.array([1, 2, 1])
ok("linear conv", list(np.convolve(x, h)) == [2, 8, 15, 20, 22, 19, 13, 8, 4, 1])
cc = np.real(np.fft.ifft(np.fft.fft(x) * np.fft.fft(h, 8))).round(6)
ok(f"circular conv {cc}", np.allclose(cc, [6, 9, 15, 20, 22, 19, 13, 8]))
print("     DFT {1,0,-1,0}:", np.fft.fft([1, 0, -1, 0]))

# CSE219 23-24 5(b): {1,2}*{1,1} via 4-pt DFT
X = np.fft.fft([1, 2, 0, 0]); H = np.fft.fft([1, 1, 0, 0])
print("     5(b) X =", X, " H =", H, " XH =", X * H, " y =", np.real(np.fft.ifft(X * H)).round(6))
X3 = np.fft.fft([1, 2, 0]); H3 = np.fft.fft([1, 1, 0])
print("     N=3: X =", X3, " H =", H3, " y =", np.real(np.fft.ifft(X3 * H3)).round(6))


# radix-2 DIT with all stages
def dit_stages(x):
    N = len(x)
    b = int(np.log2(N))
    idx = [int(format(i, f"0{b}b")[::-1], 2) for i in range(N)]
    a = np.array([x[i] for i in idx], dtype=complex)
    print("     bit-reversed input:", idx, a.real)
    M = 2
    while M <= N:
        for l in range(0, N, M):
            for k in range(M // 2):
                W = np.exp(-2j * np.pi * k / M)
                g, hh = a[l + k], W * a[l + k + M // 2]
                a[l + k], a[l + k + M // 2] = g + hh, g - hh
        print(f"     after stage M={M}:", [c(z) for z in a])
        M *= 2
    return a


xa = [1, 2, 3, 4, 3, 2, 0, 0]
Xa = dit_stages(xa)
ok("23-24 5(a) FFT = numpy", np.allclose(Xa, np.fft.fft(xa)))
for i, z in enumerate(Xa):
    print(f"     X[{i}] = {c(z)}")
for xp in ([2, 1, -3, 4], [1, 2, 0, -1, 3, 0, 2, 1]):
    Xp = dit_stages(xp)
    ok(f"practice {xp}", np.allclose(Xp, np.fft.fft(xp)))
Xk = np.array([6, np.sqrt(2) - 1j * np.sqrt(2), 2 + 4j, -np.sqrt(2) - 1j * np.sqrt(2), -2, -np.sqrt(2) + 1j * np.sqrt(2),
               2 - 4j, np.sqrt(2) + 1j * np.sqrt(2)])
print("     practice 1.5 IFFT:", np.fft.ifft(Xk).round(6))

# CSE219 23-24 7(a): 2x4 matrix (N1 = 2 rows, N2 = 4 columns), n = 2 n2 + n1
xm = np.array([1, 2, 3, 4, 9, 0, 7, 8])
M = np.array([xm[0::2], xm[1::2]])
G = np.fft.fft(M, axis=1)
print("     row DFTs G:\n", G)
Wt = np.array([[np.exp(-2j * np.pi * n1 * k2 / 8) for k2 in range(4)] for n1 in range(2)])
print("     twiddles:\n", Wt)
Hm = G * Wt
print("     H = G .* W:\n", Hm)
Xm = np.fft.fft(Hm, axis=0)
print("     column DFTs (row k1, col k2):\n", Xm)
Xflat = Xm.reshape(-1)
ok("7(a) row-major read = fft", np.allclose(Xflat, np.fft.fft(xm)))
for i, z in enumerate(Xflat):
    print(f"     X[{i}] = {c(z)}")

# Bailey practice 2.2
xb = np.array([1, 3, -1, 2, 0, 4, 2, 1])
Mb = np.fft.fft(np.array([xb[0::2], xb[1::2]]), axis=1) * Wt
ok("practice 2.2", np.allclose(np.fft.fft(Mb, axis=0).reshape(-1), np.fft.fft(xb)))


# Bluestein 3-point {2,-1,3}
def bluestein(x):
    N = len(x)
    W2 = lambda m: np.exp(-2j * np.pi * m / (2 * N))
    a = np.array([x[n] * W2(n * n) for n in range(N)])
    Mlen = 1 << int(np.ceil(np.log2(2 * N - 1)))
    A_ = np.zeros(Mlen, complex); A_[:N] = a
    B_ = np.zeros(Mlen, complex)
    for n in range(-(N - 1), N):
        B_[n % Mlen] = W2(-n * n)
    y = np.fft.ifft(np.fft.fft(A_) * np.fft.fft(B_))
    return np.array([y[k] * W2(k * k) for k in range(N)]), a, Mlen


Xb, a3, Ml = bluestein([2, -1, 3])
print("     Bluestein a[n] =", a3, "M =", Ml)
ok("Bluestein 3-pt", np.allclose(Xb, np.fft.fft([2, -1, 3])))
print("     X =", Xb)
# complexity table
for N in (8, 1024, 2 ** 20):
    print(f"     N={N}: N^2 = {N*N:.3g}, (N/2)log2N = {N/2*np.log2(N):.3g}, ratio {N*N/(N/2*np.log2(N)):.1f}")
