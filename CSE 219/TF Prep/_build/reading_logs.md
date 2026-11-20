# Reading logs — CSE 219 slide decks
(slide numbers = PDF page numbers; Ashraf's printed slide numbers are PDF page − 1)

## Anik Sir
### Lec 1 — A Little Introduction to Signals (53 sl.)
- sl 2–5 signal, CT vs DT, x(t) vs x[n] conventions.
- sl 6–16 energy / power: E = ∫|x|², P = E/(t2−t1); half-sine E = π/2, P = 1/2; DT example {1,−2,2,−1} E = 10, P = 2.5; periodic half-sine (E = ∞, P = 1/2), period 2π (P = 1/4); x = 1 (|t|≤1), 1/|t| beyond: E = 4, P = 0.
- sl 17–39 transformations: shift (delay right / advance left), reversal, scaling; order matters (x(2t+3) vs x(2(t+3))); recipe x(αt+β): shift by β, reverse if α<0, scale by |α|; worked example x(−3t+2) of a trapezoid (sl 31–35); Practice 1 x(3(2−t/2)) = x(6−3t/2); Practice 2 operation chain → x(−2t+3/2).
- sl 40–52 even/odd: xe = ½[x(t)+x(−t)], xo = ½[x(t)−x(−t)]; example x = t+1 on [−1,1] → xe = 1, xo = t; DT u[n] → xe = ½ (n≠0), 1 (n=0); xo = ±½.
- Figures: sl 8 half-sine, 12/14 periodic half-sine, 15 1/|t| signal, 32–35 transformation chain, 45–48 even/odd example, 49–52 DT even/odd.

### Lec 2 — Some Useful Signals (51 sl.)
- sl 3–15 u[n], δ[n], δ[n] = u[n]−u[n−1], u[n] = Σδ[m], u[n] = Σδ[n−k].
- sl 16–29 u(t), δ(t) = du/dt via smoothed step u_Δ (*), area 1, arrow notation, d/dt 2u(t) = 2δ(t); x = 2u(t−1)−3u(t−2)+2u(t−4) and its derivative.
- sl 30–35 real exponentials, ×u(t) as switch, e^{−t}u(t−2), e^t u(−t), e^t u(3−t), u(3t) = u(t).
- sl 36–42 sinusoids, T0 = 2π/|ω0|, Euler, cos = (e^{jθ}+e^{−jθ})/2.
- sl 43–50 DT periodicity: N = m·2π/ω0 must be integer; cos 2n not periodic; cos(2πn/5) N = 5; 3 sin(5n/7) not periodic; 2cos(16πn/63+π/3) N = 63 (= 2022-23 B5(c)).
- Figures: sl 11 δ = u − u[n−1], 26 impulse arrows, 28–29 jump signal & derivative, 35 exponential-step panels, 45 cos 2t vs cos 2n.

### Lec 3 — LTI Systems and Convolution (59 sl.)
- sl 2–11 systems, linearity (scaling + additivity), time invariance, LTI.
- sl 12–31 convolution as polynomial multiplication: c[n] = Σ a[k]b[n−k]; z^4 coefficient = 17; reflect–shift–multiply–add; example x = {1,2,1,1}, h = {1,1,−1,2} → y = {1,3,2,2,4,1,2}; commutativity.
- sl 32–57 why convolution: impulse response, echo system h = u[n], α^n u[n], delay h = δ[n−3]; x = δ+2δ[n−1]−δ[n−2]+δ[n−3] → y = u+2u[n−1]−u[n−2]+u[n−3]; x[n] = Σx[k]δ[n−k] ⇒ y = Σx[k]h[n−k].
- Figures: sl 15 criss-cross pairing, 17–19 sliding, 28 final output, 50–51 echo outputs, 54 shifted copy.

### Lec 4 — Convolution, Causality and Stability (70 sl.)
- sl 2–9 DT and CT convolution recipe (sl 7 overlap picture).
- sl 11–19 Ex 2.2 x = {0.5, 2}, h = {1,1,1} → {0.5, 2.5, 2.5, 2}.
- sl 20–27 Ex 2.3 α^n u[n] * u[n] = (1−α^{n+1})/(1−α) u[n].
- sl 28–34 Ex 2.5 2^n u[−n] * u[n] = 2^{n+1} (n<0), 2 (n≥0).
- sl 35–40 Ex 2.6 e^{−at}u(t) * u(t) = (1−e^{−at})/a u(t).
- sl 41–47 distributivity; Ex 2.10 [(½)^n u[n] + 2^n u[−n]] * u[n] → 2^{n+1} (n<0), 4 − 2^{−n} (n≥0).
- sl 48–52 e^t u(−t) * e^{−t}u(t) = ½e^{−|t|}.
- sl 53–69 causality h(t) = 0 for t<0; BIBO ⇔ ∫|h| < ∞; periodic h cannot be causal or stable; h1 = e^{2t}u(−2−t) non-causal, stable (½e^{−4}); h2 = te^{−t}u(t) causal, stable; minimum delay making e^{−2t}u(t+2) causal: a ≥ 2.
- Figures: sl 7 CT overlap, 13–19 sliding Ex 2.2, 23 overlap Ex 2.3, 47 Ex 2.10 sketch, 50–52 two-sided result, 55 causal/non-causal h, 64 h1 support.

### Lec 5 — Fourier Series: Let's Look Inside (53 sl.)
- sl 2–17 why FS (strings, heat), harmonics kω0, x = Σ a_k e^{jkω0t}, cos as two lines.
- sl 18–22 averaging trick → a_k = (1/T)∫_T x e^{−jkω0t} dt.
- sl 25–29 by inspection: x = 1 + sin ω0t + 2cos ω0t + cos(2ω0t+π/4) → a0 = 1, a±1 = 1 ∓ j/2 … , magnitude/phase spectra.
- sl 30–34 square wave: a0 = 2T1/T, a_k = sin(kω0T1)/(kπ); T1 = T/4 spectrum.
- sl 35–41 triangular ramp (T = 3): a0 = ½, a_k = (e^{−jkω0} − 1)/(6k²ω0²).
- sl 44–52 (*) coordinate/projection view: inner product ⟨x,z⟩ = (1/T)∫ x z*.
- Figures: sl 29 spectra, 30 square wave, 34 square-wave spectrum, 35 ramp.

### Lec 6 — Properties of Fourier Series (82 sl.)
- sl 5–8 linearity; sl 9–17 time shift a_k e^{−jkω0t0}; sl 18–23 reversal a_{−k}; sl 24–26 combined x(4−t)+y(t−3) (slide 26 typo: should be b_k e^{−j3kω0}); sl 27–35 time scaling (same a_k, ω0' = αω0); x(4−3t) ↔ a_{−k}e^{−j4kω0}.
- sl 36–41 differentiation jkω0 a_k; d/dt x(4−3t) ↔ j3kω0 a_{−k}e^{−j4kω0}.
- sl 42–44 derivative sketch with impulses; sl 45–51 sifting; ∫ e^t δ… examples.
- sl 52–56 impulse train a_k = 1/T.
- sl 57–63 derivative of rectangular pulse train: b_k = (2j/T) sin(kω0T1) = jkω0 a_k.
- sl 64–72 integration a_k/(jkω0), a0 separately; sawtooth x = t (period 1): a0 = ½, a_k = j/(2πk).
- sl 73–81 multiplication ↔ convolution of coefficients; (1+cos ω0t)² → c0 = 3/2, c±1 = 1, c±2 = 1/4.
- Figures: sl 43–44 derivative sketch, 55 impulse-train spectrum, 59 derivative of pulse train, 67–68 sawtooth & derivative.

### Lec 7 — Fourier Transform (61 sl.)
- sl 2–18 FS → FT: periodic extension, T a_k = X(jkω0), T → ∞, analysis/synthesis pair.
- sl 19–28 frequency shift x e^{jω0t} ↔ X(j(ω−ω0)); x cos ω0t ↔ ½[X(j(ω−ω0)) + X(j(ω+ω0))].
- sl 29–38 rect width T ↔ 2 sin(ωT/2)/ω; widths 2 and 6; shifted rect 4<t<10 ↔ e^{−j7ω} 2sin3ω/ω; Lego block ↔ e^{−j2.5ω}[2 sin1.5ω/ω + sin0.5ω/ω].
- sl 39–40 windowed cosine; sl 41–44 δ(t) ↔ 1, δ(t−t0) ↔ e^{−jωt0}.
- sl 45–59 applications (denoising, JPEG, MRI, music ID, vibration, ECG).
- Figures: sl 12 stems on envelope, 27 two copies, 30–31 rect & sinc, 37 Lego decomposition, 40 windowed cosine spectrum, 43 δ ↔ 1.

## Ashraf Sir
### Lec 0 — Overview of the Transforms (41 sl.) — "Nothing here is examinable"
- History: Bernoulli/Lagrange string, Fourier & heat equation, Gibbs, CTFT naming, FFT (Gauss 1805, Cooley–Tukey 1965), Heaviside & Laplace, z-transform (Hurewicz, Ragazzini–Zadeh, z = e^{sT}). sl 22 four-transform square; sl 24 N² vs N log N table; sl 32 Laplace = Fourier of x e^{−σt}; sl 40 family tree.

### Lec 1 — DTFT and DFT (38 sl.)
- sl 5–19 CTFS → sample periodic signal → c_k = (1/T0)Σ x[n]e^{−j2πkn/N}; N-periodic coefficients; c_{−k} = c_{N−k}; orthogonality → inverse; DFS pair; DFT/IDFT with W_N; X[k] = N a_k, c_k = X[k]/T0.
- sl 20–27 DTFT X(e^{jω}) = Σ x[n]e^{−jωn}; 2π-periodic; inverse DTFT.
- sl 28–34 DFT = samples of DTFT at 2πk/N; zero-padding; N = 4 example {1,2,3,4} → {10, −2+2j, −2, −2−2j}; bins to Hz f_k = k f_s/N.
- Figures: sl 10 periodic coefficients, 29 DFT samples DTFT, 32 worked example table, 36 square.

### Lec 2 — DFT Properties and Applications (26 sl.)
- sl 5–12 clock ((n))_N, linearity, circular shift W^{km}X[k], modulation, reversal, conjugation, X[N−k] = X*[k] for real x, Parseval (check 30 = 120/4), property table.
- sl 13–23 circular convolution theorem; two-wheel picture; x = {2,4,5,6,5,3,2,1}, h = {1,2,1}: linear {2,8,15,20,22,19,13,8,4,1}, circular {6,9,15,20,22,19,13,8}; pad N ≥ L+M−1; filtering recipe.
- Figures: sl 16 two wheels, 21 circular vs linear, 22 zero-padding.

### Lec 3 — Fast Fourier Transform (19 sl.)
- sl 4 O(N²); sl 7–9 DIT: X[k] = G[k] + W^k H[k], X[k+N/2] = G[k] − W^k H[k]; sl 10–13 butterflies N = 2, 4, 8 (flow graphs); sl 14 bit reversal table; sl 15 pseudocode & O(N log N); sl 16–18 DIF: a(n) = x[n]+x[n+N/2], b(n) = (x[n]−x[n+N/2])W^n, outputs bit-reversed; sl 19 zero-padding.
- Figures: sl 11 4-pt DIT, 12 8-pt first stage, 13 full 8-pt DIT, 14 bit-reverse table, 17 DIF butterfly, 18 full 8-pt DIF.

### Lec 4 — Advanced FFT (24 sl.)
- sl 5–8 radix-2 as 2 × N/2 matrix: column-major input, row DFTs, twiddle W^{n1 k2}, column DFTs, row-major output; sl 9–10 radix-3; sl 11–13 general N = N1N2 derivation; sl 14 Bailey four-step.
- sl 16–17 fast convolution, complexity (≈300× for 1 s audio).
- sl 19–22 Bluestein: kn = [k² + n² − (k−n)²]/2, X[k] = W_{2N}^{k²}(a*b)[k], a = x W_{2N}^{n²}, b = W_{2N}^{−n²}; M ≥ 2N−1, wrapped chirp.
- Figures: sl 6–7 matrix steps, 10 radix-3 table, 21 Bluestein padding.

### Lec 5 — Sampling (47 sl.)
- sl 5 ambiguity; sl 6 impulse-train sampling; sl 8–17 two roads; duality; multiplication ↔ (1/2π) convolution; P(jω) = (2π/T)Σδ(ω−kω_s); Xp = (1/T)Σ X(j(ω−kω_s)).
- sl 19–22 theorem ω_s > 2ω_M, Nyquist rate, oversampling / aliasing pictures.
- sl 24–36 reconstruction: ideal LPF gain T cutoff ω_s/2, h = sinc(t/T), sinc interpolation; ZOH h0 = rect[0,T], H0 = T e^{−jωT/2} sinc(ωT/2π); linear interpolation h1 triangle, H1 = T sinc²(ωT/2π); comparison.
- sl 38–47 time-limited ⇒ not band-limited; DTFT from Xp; inverse DTFT from LPF; DFT as samples of one ω_s period; periodic signals: X[k] = N a_k.
- Figures: sl 17 map, 20 theorem picture, 21–22 over/undersampling, 25 ideal LPF, 31 ZOH, 35 linear, 36 comparison.

### Lec 6 — Laplace (36 sl.)
- sl 4–7 eigenfunction e^{st}, definition, LT = FT of x e^{−σt}.
- sl 9–15 Ex 9.1–9.5 (e^{−at}u, −e^{−at}u(−t), 3e^{−2t}u − 2e^{−t}u, e^{−2t}u + e^{−t}cos3t u, δ − (4/3)e^{−t}u + (1/3)e^{2t}u).
- sl 17–25 ROC properties 1–8; Ex 9.6 finite e^{−at} on (0,T) — no true pole; Ex 9.7 e^{−b|t|} ↔ −2b/(s²−b²), −b<σ<b; Ex 9.8 three ROCs.
- sl 27–36 inverse: Bromwich integral, numerical approximation, partial fractions; Ex 9.9–9.11.
- Figures: sl 9–10 ROC pictures, 13 pole-zero, 23 two-sided, 25 three ROCs, 29 Bromwich contour, 32 ROC → side.

### Lec 7 — More Laplace (28 sl.)
- sl 4–18 properties with proofs: linearity (Ex 9.13 cancellation), time shift, s-shift, scaling, reversal, conjugation, convolution, d/dt ↔ sX (u → δ), −t x ↔ dX/ds (Ex 9.14, 9.15), integration X/s; summary table.
- sl 20–23 system function; causality (ROC right of rightmost pole), stability (ROC ∋ jω-axis), Ex 9.20 three ROCs of (s−1)/((s+1)(s−2)); causal rational stable ⇔ poles in LHP.
- sl 25–28 DE → H(s): dy/dt + 3y = x, x = e^{−2t}u → y = (e^{−2t} − e^{−3t})u; LCCDE → H(s).
- Figures: sl 18 table, 22 three ROCs.

### Lec 8 — z-Transform (47 sl.)
- sl 4–10 motivation, z = e^{sT}, mapping (strip → annulus), H(z), X(re^{jω}) = F{x r^{−n}}.
- sl 12–16 Ex 10.1 a^n u[n] ↔ 1/(1−az^{−1}) |z|>|a|; Ex 10.2 left-sided; Ex 10.3 7(1/3)^n u − 6(1/2)^n u; Ex 10.4 (1/3)^n sin(πn/4) u.
- sl 17–26 ROC properties 1–9; Ex 10.5 impulses; Ex 10.6 finite a^n (N−1 zeros on circle radius a, poles at 0); Ex 10.7 b^{|n|}; Ex 10.8 three ROCs.
- sl 28–32 inverse: contour formula; partial fractions Ex 10.9–10.11; power series Ex 10.12–10.14 (log(1+az^{−1})).
- sl 34–41 properties table (shift, scaling, reversal, conjugation, time expansion, convolution, first difference, accumulation, n x[n], initial value, LCCDE).
- sl 43–47 causality (ROC exterior incl. ∞), stability (ROC ∋ unit circle), Ex 10.20–10.25, step response y = (8/3)u − (5/3)(½)^n u.
- Figures: sl 12–13 ROC exterior/interior, 15 pole-zero, 23 finite-length zeros, 24 b^{|n|}, 26 three ROCs, 44–45 causality/stability.
