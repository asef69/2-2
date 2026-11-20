# Question log (raw transcription)
## CSE 219 2022-23 (merged p1-5). Sec A = Ashraf, Sec B = Anik
A1(a) ZT+ROC of a^n u[n] (10) p1
A1(b) is s=(-a,0) in ROC of LT of x(t)=e^{-at},0<t<T (10) p1
A1(c) bandlimited x(t), wM; analyze how x(t) uniquely determined by samples x(nT) if ws>2wM (15) p1
A2(a) state & prove time- and s-domain differentiation props of LT (10) p1
A2(b) inverse LT X(s)=(s+2)/(s^2+7s+12), -4<Re s<-3 (10) p1
A2(c) LT+ROC of e^{-b|t-2|} (15) p1
A3(a) x[n]=a^n 0<=n<=N-1: show ROC of ZT excludes origin (10) p2
A3(b) derive contour integral inverse ZT (10) p2
A3(c) inverse ZT X(z)=log(1+az^-1), |z|>|a| (15) p2
A4(a) relation LT and FT (10) p2
A4(b) x[n] with X(jw)=0 for 2pi/9<=|w|<=pi: lowest rate to sample x[n] (10) p2  [discrete-time sampling/decimation]
A4(c) compare complexity DFT vs radix-2 FFT (15) p2
B5(a) f(t)= t+1 (-2..0), -t/2+1 (0..2): i draw (3) ii even-odd decomposition (6) iii draw even/odd (6) p2
B5(b) X(jw)=1 |w|<3pi; |X1| triangle-ish M shape magnitude 9pi at ±3pi? angle +pi/2 for w>0? Fig1: i define X1 (2) ii inverse FT of X (8) iii X1 in terms of X (2) iv x1 in terms of x (3) v x1(t) (5) p2-3
B5(c) x[n]=2cos(16pi n/63 + pi/3) periodic? (5) p3
B5(d) x(t)=sum_{k=0}^{100} (1/2)^k e^{jk2pi t/50}: real-valued & even? (5) p3
B6 f(t)=e^{-at}u(t), sign(t): (a) define f(-t) (3) (b) FT of f, f(-t) (12) (c) sign in terms of f (5) (d) FT of sign via properties (10) p3
B7 x(t) figure 2: (a) piecewise def (3) (b) x(-2t+2) with properties+graph (10) (c) x(-t/2+1) (10) (d) image tasks -> signal properties (7) p4
B8(a) conv x[n]=3^n u[-n-1]+(1/3)^n u[n], h=(1/4)^n u[n+3] (20) p5
B8(b) causal/stable h1=e^{2t}u(-2-t), h2=t e^{-t}u(t) (10) p5

## CSE 219 2023-24 (22 batch pdf p1-5). Sec A = Anik, Sec B = Ashraf
A1(a) x(t)=1-|t| tri; sketch y=x(-2(t-1))+x((t+2)/2) (15) p1
A1(b) h1=d[n]-d[n-2], h2=u[n-1], h3=d[n]-d[n-1]; (h1+h2)*h3; i heq ii y for x=u[n] (15) p1
A1(c) FT rect(t); FT of rect((t-tau)/T)cos 2pi f0 t (15) p2
A2 x1=e^{-at}u(t), x2=e^{-a|t|}: (a) FT x1 then x2 (10) (b) I(a)=∫f^2/(a^2+(2pi f)^2)^2 df via Parseval (20) p2
A3(a) x[n]=(3-4j)e^{j13pi n/7}: i real/imag periodic? N0 ii phase shift as integer time shift? (15) p2
A3(b) causal/stable: e^{-4t}u(3-t), e^{-6|t|}, t e^{-t}u(t) (15) p2
A4 odd square wave A, y=x(t-T0/6): (a) half-wave sym (5) (b) Yk (10) (c) mag/phase spectra to k=5 (10) (d) compare trig FS (5) p2
B5(a) 8-pt DFT x={1,2,3,4,3,2} radix-2 DIT FFT, butterflies (15) p3
B5(b) lin conv {1,2}*{1,1} via DFT (10) p3
B5(c) reconstruction: sinc, ZOH, linear interp impulse responses compare; choose for real-time DAC (5+5) p3
B6(a) y''+7y'+12y=x'+2x, x=u, zero IC, solve by LT (12) p3
B6(b) LT+ROC |t|e^{-2|t|} - e^{-t}cos3t u(t) + t^2 e^{-4t}u(t), sketch ROC (13) p3
B6(c) causal but unstable? stable but non-causal? ROC reasoning (5+5) p3
B7(a) 2x4 Cooley-Tukey matrix DFT of {1,2,3,4,9,0,7,8} steps i-iii (15) p4
B7(b) chirp-z / Bluestein derivation, padding M>=2N-1 (10) p4
B7(c) Nyquist-Shannon theorem, Xp(jw) satisfy/violate, why aliasing irrecoverable (10) p4
B8(a) all ROCs of X(z)=(1+2z^-1-z^-2)/(1-11/6 z^-1+z^-2-1/6 z^-3) (12) p4
B8(b) pole-zero plot Y(z) poles 1/3,2/3,2: ROC for right-sided, FT converges, FT doesn't converge, left-sided (8) p5
B8(c) ZT of |n|(1/2)^|n| + pole-zero (10) p5
B8(d) LT vs ZT; why ZT for DT (5) p5

## CSE 311 papers in merged PDF (Data Communication; only signal-related parts logged; rest = comms, out of syllabus)
2022-23 (p6-7; paper pp.2-3 missing): 1(a) FS coeffs even->real odd->imag; cos2πf0t (17) p6 | 1(b) spectrum of Π(t/2B); practical spectra; how sampling changes band (18) p6 | 2(a) G(f)H(f) <-> g*h time-domain proof, LTI output = conv (20) p6 | 2(b) distortionless vs all-pass; how determine distortionless (15) p6
  comms: 3(a) bit stuffing DM1/2 (15) p6; 6(b) multitone AM (10) p7; 6(c) AM power (10) p7; 7(a) PM/FM (15) p7; 7(b) Carson (15) p7; 8(a) ASK/PSK (5); 8(b) Manchester (10); 8(c) music line code (15) p7
2021-22 (p8-11): 1(a) FT gate width B + exp FS periodic gate period 2B, four reps, correlate (20) p8 | 2(a) all-pass vs distortionless; freq resp; unrealizable (20) p8 | 3(a) time compression vs freq expansion; log quantization doesn't change BW (20) p8 | 3(b) Nyquist-rate samples zero except t=0 (A): g(t) (15) p8 | 6(a) PSD, power from PSD (5) p10
  comms: 1(b) T1 (15); 2(b) NRZ-I/2B1Q (15); 4(a) TDM video (18); 4(b) DM vs DPCM (17); 5(a)(b)(c) AM circuit (20,5,10); 6(b)(c)(d) QAM/QPSK (13,9,8); 7(a)(b)(c) PM/FM (16,13,6); 8(a)-(d) (13,8,7,7)
2020-21 (p12-14): 1(b) foretell future from past samples? (10) p12 | 2(b) exp FS coeffs sin2πt, cos2πt; need full cycle? (17) p12 | 3(a) practical signal not fully recoverable; aliasing; minimise (24) p12 | 3(b) Dirichlet; necessary? example (11) p12 | 4(a) distortionless characteristics, physical interpretation (20) p12
  comms: 1(a) DC line coding (25); 2(a) DPCM (18); 4(b) telemetry TDM (15) p13; 5(a)(b)(c) FSK/PM (15,10,10) p13; 6(a)(b)(c) (18,5,12) p14; 7(a)(b)(c) (15,12,8); 8(a)-(d) (12,10,7,6)
2019-20 (p15-17): 1(a) FS for cos/sin 2πf0t; coeffs real/imag (17) p15 | 1(b) FT of that signal; Dirichlet; necessity (18) p15 | 2(a) time delay -> linear phase; voice signal (24) p15 | 2(b) step from impulse and vice versa (11) p15 | 3 FT of 2B sinc(2πBt) or B sinc^2(πBt); sampled at 1.5x Nyquist spectrum; generic sampled spectrum (35) p15
  comms: 4(a) quantization SNR (27); 4(b) NRZ-I/2B1Q (8); 5(a) DSB-SC (35) p16; 6(a)(b)(c) FSK/MSK (15,10,10); 7(a)(b)(c) VSB/SSB/PLL (20,10,5) p16-17; 8(a)(b) PM/FM QAM (20,15) p17
2018-19 (p18-20): 1(a) g(t) BL 50Hz sampled 0.01s, g(0)=1 others 0: g(t), FT, characteristics; FT of delta (21) p18 | 1(b) distortionless; is all-pass distortionless (14) p18 | 2(b) FS coeffs even real / odd imag; half-cycle integration (15) p18 | 3(b) aliasing cause/problems/compensation (20) p18 | 4(a) frequency-shifting equation; FDM; dual technique (18) p18 | 4(b) prove y=x*h for LTI, time domain only (17) p18
  comms: 2(a) DM (20); 3(a) 4B5B (15); 5(a)(b)(c) AM (10,15,10) p19; 6(a)-(d) FM (12,8,7,8) p19-20; 7(a)-(d) PSK (10,10,10,5) p20; 8(a)-(d) (6,10,10,9) p20
2017-18 (p21-23): 1(a) freq-domain rep; spectrum of periodic vs aperiodic (rect pulse vs pulse train); bandwidth (18) p21 | 1(b) triangle h(t) from rect g(t) via FT properties (10) p21 | 1(c) ideal LPF transfer fn -> impulse response (7) p21 | 3(b) DIF FFT formulation, 8-pt signal flow graph, bit-reversed order (24) p22
  comms: 2(a) power-bandwidth tradeoff (10); 2(b) quantizer SNR (10); 2(c) mu-law (15) p22; 3(a) DPCM/DM (11); 4(a)(b) TDM/line code (15,20); 5(a)(b) (23,12) p23; 6(a)(b)(c) (3,15,17); 7(a)(b) (8,27); 8(a)(b) (15,20)
2016-17 (p24-27): 1(a) define bandwidth, sketch two signals (9) p24 | 1(b) real signal: amplitude spectrum even, phase odd (6) p24 | 1(c) duality: FT of sinc^2(t) from triangle pair (6) p24 | 1(d) ideal LPF unrealizable proof (8) p24 | 1(e) differentiator transfer function (6) p24 | 2(b) state & prove Nyquist sampling theorem; anti-alias filter; rate > Nyquist (16) p24 | 3(a) DFT: derive formula from G(f), prove f0=1/T0, compute DFT of samples, choosing Ts,T0 (20) p25
  comms: 2(a) adv digital (5); 2(c) companding (14) p25; 3(b) DPCM predictor (6); 3(c) DM step (9); 4(a) TDM stuffing (17); 4(b) ISI (18); 5(a)(b)(c) (15,10,10) p26; 6(a)(b) (15,20); 7(a)(b) (15,20); 8(a)(b)(c) (15,10,10) p27
2014-15 L-4/T-2 (p28-32, date 29/01/2017; paper p.4 missing): 5(b) dilation (time-scaling) property state & prove (10) p29 | 5(c) FT of sin^2(2πf0t) g(t) (10) p29 | 5(d) FT of Dirac delta (5) p29 | 6(a) bandwidth of two spectra (triangle at 0, triangles at ±) + if time domain (10) p30 | 6(b) FT of periodic signals derivation questions i-v (20) p30-31 | 7(a) short notes linear system, time-invariant system (10) p31 | 7(b) ideal LPF response to rect pulse; ideal vs real (10) p31 | 7(c) recurrence relationship for FFT (15) p31 | 8(a) FT of impulse-sampled signal, G_delta(f), sampling theorem (15) p32
  comms: 1(a)-(d) (13,10,6,12) p28; 2(a)(b)(c) (15,8,12) p28; 3(a)(b)(c) (13,12,10) p29; 4(a)(b)(c) (15,8,12) p29; 5(a) switching (10) p29; 6(c) nonuniform quant (5) p31; 8(b)(c) (10,10) p32
2014-15 L-3/T-1 (p33-36): 1(a) bandwidth def; bandwidth of δ(t) (12) p33 | 1(b) linearity & time invariance of LTI (10) p33 | 1(c) LPF H(f)=(1+k cos2πfT)e^{-j2πftd}: echo output (13) p33 | 2(c) aliasing effect, elimination (10) p33
  comms: 2(a) (5); 2(b) PCM rate (8); 2(d) mu-law (12) p33; 3(a)(b)(c) (13,8,14) p34; 4(a)(b) (15,20) p34; 5(a)(b)(d) (15,14,7?) p34; 6(a)(b)(c) p35; 7(a)-(d) p35; 8(a)(b)(c) p36
2013-14 (p37-40): 1(b) (i) bandwidth calc (ii) g(t) vs g(at) bandwidth a>1 (12) p37 | 1(c)(i) empirically find transfer function of LTI (8) p37 | 1(c)(ii) RC circuit as distortionless (10) p37 | 2(a) state & prove Nyquist sampling theorem (13) p37 | 2(b) practical sampling/reconstruction issues (10) p37
  comms: 1(a) (5); 2(c) (12); 3(a)-(d); 4(a)(b); 5(a)(b)(c); 6(a)(b)(c); 7(a)(b)(c); 8(a)-(d) p38-40
2012-13 (p41-44): 5(a) define unit impulse; derive sampling property (8) p43 | 5(b) prove convolution theorem both ways (14) p43 | 5(c) FT of Π(t/τ) (13) p43 | 6(b) state & prove time-shifting and frequency-shifting (10) p44 | 7(a) distortionless: |H| const, phase linear (8) p44 | 7(c) LPF (1+k cos2πfT) echo output (13) p44 | 8(a) prove min sampling freq 2B (15) p44
  comms: 1(a)(b) (20,15); 2(a)(b)(c); 3(a)(b)(c); 4(a)(b); 6(a)(c); 7(b); 8(b)
2011-12 (p45-48): 5(a) FT of rect f(t) (8) p47 | 5(b) FT of g (doublet) from f, then h (triangle) from g via properties (14) p47 | 5(c) bandwidth; which of f,g,h lowest bandwidth (13) p47 | 6(a) linearity, TI; G=HF proof (18) p47 | 6(b) distortionless H(w); RC approx (17) p47
  comms: 1-4, 7, 8
2010-11 (p49-51): 5(a) bandwidth; f vs f' bandwidth (14) p50 | 5(b) FT of g(t) (triangle) from f(t) via time-shift/scaling; inverse time-bandwidth (21) p50-51 | 6(a) ideal LPF impulse response, unrealizable (15) p51 | 6(b) g(t) through H=jw, output (8) p51 | 6(c) sampled at 2B through ideal LPF gives f(t) (12) p51
  comms: 1-4, 7, 8

## EEE 211 (Continuous Signals & Linear Systems) — page = "EEE p.N"
### 2023-24 (EEE p1-6)
1(a) piecewise x(t) fig (tri -2..0 peak 1 at -1; ramp 0..2 to 2; flat 2..3; down to 0 at 4): (i) draw x(-3t+2), x'(t), x''(t) (ii) x' via δ,u,r (11) p1
1(b) dy/dt + t^2 y = (2t+3)x: linear? time-invariant? (7) p1
1(c) h1=e^{-2t}u, h2=e^{-3t}u, h3=e^{-t}u, h4=δ, h5=e^{-3t}u interconnection: BIBO stable? y for x=e^{-t}u (17) p1  [structure: h1 || (h2*h3) || h4 -> sum -> h5 ; sign at adder?]
2(a) graphical convolution x=rect 1..2 height1, h=triangle -1..1 peak1 (18) p2
2(b) impulse response LC circuit time domain (17) p2
3(a) first canonical state-space of y'''-2y''+y'+4y = x''+5x; stability (18) p2  OUT
3(b) state eqn impulse response via Cayley-Hamilton (17) p2 OUT
4(a) RLC circuit vC(0-)=1, iL(0-)=2, x=u: find y (Laplace) (18) p2
4(b) force-voltage analog of mechanical system (17) p3 OUT
5(a) quadrature multiplexing: design H(jw), spectra at points (20) p3-4
5(b) feedback: plant 1/(s+2), controller (s+1)/s, final value = input?; controller 1/(s-2) (15) p4
6(a) FT of impulse-train-like signal fig (impulses ±1 at ...); amplitude/phase spectrum (15) p4
6(b) FT of sin(at)/(πt); Parseval energy (10) p4
6(c) FT of u(t); prove integration property (10) p4
7(a) three functions pairwise orthogonal on (-1,2); A for orthonormal (10) p4-5
7(b) half-wave rectified sine x(t) T=0.5ms into differentiator & LPF fc=1kHz |H|=5 linear phase: FS coeffs of y1; y2(t); compare (25) p5
8(a) block diagram transfer function, poles, stability (17) p6
8(b) y''+5y'+6y=x'+x, y(0-)=2, y'(0-)=1, x=e^{-4t}u: Laplace; ZIR, ZSR (18) p6
### 2022-23 (EEE p7-11)
1(a) thermostat: choose H1=s^2/(s^2+9) or H2=1+(1/20)s(s+10)/((s+10)^2+1); % incremental change at 1.5 s (18) p7
1(b) f-i electrical equivalent of pulley/mechanical system (17) p7 OUT
2(a) closed-form FT of x(t): ramp 0..1 to 1, flat 1..2, (fig) (10) p8
2(b) AM with downsampled m(t), filter Hf: spectra of x,y,z; energy of z (25) p8
3(a) circuit with v(t)=2 (t<0), 4e^{-2t} (t>=0): iR(t) by Laplace (18) p8
3(b) state space A,b,c,d -> H(s), h(t) via Laplace; ROC of step response Y(s) (17) p9 [state-space part OUT-ish; Laplace]
4(a) AM receiver with phase error θ, LPF gain 2: output expression (15) p9
4(b) H(s)=(s^2+s+1)/(s^3+4s^2+3s+2): second canonical simulation diagram; state equation (20) p9 OUT
5(a) x(t)=2+3cos2t+4sin2t+2sin(3t+30°)-cos(7t+150°): compact trig FS, amplitude spectrum (10) p9
5(b) LTI: given x(t) (V shape -1..1) -> y(t)=rect(-1..1); outputs for x(t-1/2)-x(t+1/2) and dx/dt (15) p9-10
5(c) x(t) fig (ramp 0..1 to 5, -6 for 1..2, ramp 2..3 to 5): elementary signals; sketch dx/dt (10) p10
6(a) are p1=lim 1/(επ cosh(t/ε)), p2=lim sin(εt)/(πt) models of delta? (20) p10
6(b) state-variable change z=Pv: A1,b1,c1,d1 (15) p11 OUT
7(a) exponential FS of periodic x(t) fig (scalloped exponential arcs period 2?) (20) p11
7(b) x(t)=h(t)=t[u(t)-u(t-1)]: y(t) for all t (15) p11
8(a) trig FS of impulse train δT0; amplitude spectrum (20) p11
8(b) dy/dt + t^2 y = (2t+3)x: linear? TI? (15) p11
### 2021-22 (EEE p12-16)
1(a) x(t)=sqrt(e^{j5πt}) + sin^2(3t-π/4) periodic? period (10) p12
1(b) e^{-3t} sin(2πt/3 - 4) u(t): power or energy? (10) p12
1(c) x=δ(t-1)+u(t)u(t-3)+u(cos t): y=∫x, sketch y(t/2)? [y(½)?] (15) p12
2(a) graphical conv: x triangle 0..2 peak1 at1; h = 2 on 0..1?, + δ? (fig: rect 0..2 height 2?, impulse at 3 of 1?) ; analytical y (17) p12
2(b) y1=x1*h, y2=x2*h, x1 triangle, x2 trapezoid (-2..2): [rest of wording cut off — illegible] (18) p12
3(a) periodic T=4 x=δ(t-1)+2[u(t-2)-u(t-4)] into RLC circuit: magnitude/phase spectra in/out (20) p13
3(b) three functions orthogonal on (-2,2); orthonormal; expand x=1 on 0..2; Parseval (15) p13
4 y''+7y'-12y=x''+3x'+4x state space/STM etc (35) p13 OUT (state-space)
5(a) FS -> FT limit T->∞ derivation (18) p14
5(b) inverse FT of piecewise-constant X(w) fig (17) p14
6(a) bandpass xa through c=cos10t, h1=sin2t/πt, p=impulse train 2πn/5, h2=2sin2t/πt cos10t: sketch spectra x1..x4 (20) p14-15
6(b) h=e^{2t}u(-t): 3-dB bandwidth, duration 1/e, duration-bandwidth product (15) p15
7(a) LT + ROC sketch: e^{-at}u a>0, a<0, -e^{-at}u(-t) a<0 (12) p15
7(b) convolution property: inverse LT 1/(s-a)^3 (12) p15
7(c) y'+2y=e^{-3t}u, y(0-)=1 by LT (11) p15
8(a) control system with disturbance: Hd(s)=Y/W; step disturbance zero steady state if Hc zero at 0 (18) p15-16
8(b) force-voltage analog (17) p16 OUT
### 2020-21 (EEE p17-21)
1(a) X(w)=jw/(w^2-3jw-2): FT of x'(t)cos t (15) p17
1(b) m(t) through h1,h2 (H1=½[H0(w-w0)+H0(w+w0)], H2=j/2[...−...]) × cos/sin, sum: spectrum of y, energy via Parseval (20) p17
2(a) PSD of impulse train Σδ(t-nT) (8) p17
2(b) 3-dB bandwidth of e^{-3t}u(t) (7) p17
2(c) causal y''+6y'+8y=2x: frequency response; response to t e^{-2t}u(t) (20) p17
3(a) feedback H1=1/(s^2+bs+(b-3)), H2=-2: overall TF, b for stability (15) p18
3(b) circuit switch at t=0, 10V, 4Ω,0.2F,3Ω,6Ω,0.5H: i(t) by Laplace (20) p18
4(a) block diagram H1=1/(s+2), H2=s/(s+3), K=2: TF and unit-step response (20) p18
4(b) torque-current analog rotational system (15) p19 OUT
5(a) x1 (ramp 0..2 to 2, flat to 6), x2, x3 figs: (i) x1,x2 via r,u (10) (ii) draw x1(t+2)r(t-2) and x2(t-2)u(-2t) (10) (iii) x3 in terms of x1 (5) p19
5(b) power or energy: u(t-6)-u(-t+8); 2r(t-4)u(t) (10) p20
6(a) y(t)=t x(t+2): linear, causal, TV, memoryless, stable (15) p20
6(b) graphical conv x=rect(t/2), h=r(t)u(-t+1); analytical y, draw (10) p20
6(c) RC series, output vR: impulse response by time domain (10) p20
7(a) triangle wave x(t) period 4 exp FS; y(t) rect train via FS properties; amplitude spectra (20) p20
7(b) y''+3y'+2y=x'+x, x=2cos t+6cos3t: amplitude/phase spectrum of y; average power Parseval (15) p20
8(a) y''+6y'+8y=x'+x: state variable impulse response, Cayley-Hamilton (20) p21 OUT
8(b) s-domain STM, step response (15) p21 OUT
### 2019-20 (EEE p22-26)
Q1 y=(1/3)∫x(τ)[δ(t-τ)+δ(t-τ+t0)+δ(t-τ-t0)]dτ: what it does; BIBO; linear; memoryless; causal; TI (35) p22
Q2 x(t), h(t+1) fig: causal? graphical conv; compare; output for z=x(t)-x(t-4) (35) p22-23
Q3 multipath y=x+a x(t-T): H(s); inverse system feedback; impulse response of inverse; causal & stable condition (35) p23
Q4 mechanical analog + state variable (35) p23-24 OUT
Q5(a) single expression x(t) fig, time-compress by 3 (15) p24
Q5(b) full-wave rectified sin t into RC LPF: H(w), y(t) (20) p24
Q6(a) 1/e duration of A e^{-t/T}u, x1(3t), x1(t/2) (15) p25
Q6(b) state & prove duality property of FT (20) p25
Q7(a) exponential FS of two impulse trains (15) p25
Q7(b) x=sin(ωB t/2)/(πt), p=Σδ(t-nπ/ωB), h=sin(3ωB t/2)/(πt): y(t) (20) p25
Q8(a) FT of impulse train is impulse train (15) p25-26
Q8(b) trig FS a0,an,bn of triangular signal fig (20) p26
### 2018-19 (EEE p27-31)
1(a) orthogonality condition; e^{j2t}, e^{j4t} orthogonal on [0,π]? (10) p27
1(b) x=2+½cos(t+45°)+2cos3t−sin(4t+30°): exponential FS; magnitude/phase spectra (10) p27
1(c) triangular wave T=4 A=4 into series R=100, L=0.1: power in R (15) p27
2(a) prove Parseval energy; energy of sinc(t/2) (10) p27
2(b) x=e^{-αt}u through h=sin2t/(πt): Y(w); α for half energy (10) p27-28
2(c) SSB generation filter: spectrum of y for wf=wm; hf(t); realizable? (15) p28
3(a) FT of impulse train is impulse train; sketch (10) p28
3(b) FT of sin1000πt+cos1200πt; sampling period for no aliasing (10) p28
3(c) periodic T=2, Cn=1 odd n, 0 even; through H (|H|=1 on 2π<|w|<4π, phase ±π/2): h(t), output (15) p28
4(a) causal y''+6y'+8y=2x by FT: h(t); y for x=t e^{-2t}u (17) p29
4(b) mechanical f-i / f-v analog (18) p29 OUT
5(a) X(s) two poles, no zeros, pole -1+j, e^{2t}x not abs integrable, X(0)=5: X(s), ROC (15) p29
5(b) circuit is(t)=2A t<=0, 4e^{-2t} t>=0, R=2,L=2: iL(t) by Laplace (20) p29-30
6(a) power/energy/neither: x1=exp[j(2πt+π/4)]+exp(-2|t|); x2=[u(cos t)-δ(t-kπ)]^0.5 (15) p30
6(b) v(t) fig: (i) steps & ramps (ii) derivative sketch (iii) even/odd of derivative (20) p30
7(a) system from x(rect 1..2)->y fig: causal, TI, memoryless? output for u(t)+u(t-1)-2u(t-2) (20) p30
7(b) h=u(t)-u(t-1), x=t^2[u(t)-u(t-3)]: graphical conv, analytical y (15) p31
8(a) y''+3y'+ky=x'': K for BIBO; ZIR y(0+)=0,y'(0+)=1,K=2 (15) p31
8(b) RLC state space, STM (20) p31 OUT
### 2017-18 (EEE p32-36)
1(a) orthogonal signals; φ1..φ3 fig set orthogonal; T for orthonormal (12) p32
1(b) distortionless LTI; FS coeff relation in/out (8) p32
1(c) H=1 |w|<=3π; x=1+2cos2πt+cos4πt+½cos6πt: exp FS, y, spectra (15) p32
2(a) derive Parseval for aperiodic (7) p32
2(b) h=(1/RC)e^{-t/RC}u, x=Vu: y by frequency domain; plot (13) p32-33
2(c) natural sampling with rectangular pulse train: spectrum xs; recoverable? (15) p33
3(a) s-domain equivalent circuit, x=cos t u(t), vC(0-)=1, iL(0-)=2 (17) p33
3(b) feedback H1=1/(s^2+bs+(b-2)), H2=-1: H(s), b for stability (18) p33
4(a) trig FS coeffs x=3+cos(4t+π/4)+sin(10t+π/3) (12) p34
4(b) y''+3y'+2y=2x'+x: TF, h(t) (13) p34
4(c) LT of periodic square wave ±1 period 2T, ROC (10) p34
5(a) x1=2cos(0.6√π t+π/6), x2=sin(1.2√π t−π/3): [x1+x2]^2 periodic? period (15) p34
5(b) power/energy: x(4−t/2)[δ(t+½)−δ(t−3/2)]; Σ_{k=-1}^{1} u(2x(t)−k) with x fig (20) p34
6(a) LTI response y1 to u(t)-u(t-1) given; response to x2 fig (20) p35
6(b) y=k1 cos[k2 t + ∫0^t k3 x dτ]: TI, memoryless, causal, invertible, stable (15) p35
7(a) graphical conv x (fig 0..3), h (fig -1..1) analytical (20) p35
7(b) cascade h1=te^{-t}u, h2=e^{-2t}u, x=u(t)-u(t-2)+δ(t+1): h, parallel equivalent, y (15) p35
8(a) simulation diagram -> diff eq; state-variable h(t) (20) p36 OUT
8(b) circuit f-i analog (15) p36 OUT
### 2016-17 (EEE p37-41) full marks 280
1(a) memoryless/causal/stable: δ(t)-δ(t-2); 2rect(t/2); 2e^{-4t}u; [1-e^{-4t}]u (15) p37
1(b) interconnection h1=e^{-2t}u,h2=e^{-2t}u,h3=e^{-t}u,h4=δ,h5=e^{-3t}u: h, y for x=u, stability (20) p37
2(a) Dirichlet conditions for FS (10) p37
2(b) square pulse train x (1 on 0..T/2): exp FS; avg power Parseval; FS of dx/dt; output with H=1/(1+jw); spectra (25) p37-38
3(a) φ1..φ3 orthogonal, T orthonormal, express x=A on 0..T (15) p38
3(b) distortionless LTI, FS coeff relation (10) p38
3(c) RL circuit impulse & step response (10) p38
4(a) state-space of circuit (15) p39 OUT
4(b) STM properties, h(t)=cφb+dδ (10) p39 OUT
4(c) simulation diagram canonical forms H=(s^2-3s+2)/(s^3+6s^2+11s+6) (10) p39 OUT
5(a) sketch x=(t+1)[u(t+2)-u(t)] (10) p39
5(b) y=x(-2t+6) given (fig triangle 1..3 peak1 at 2 + 1 at 0?) sketch x (15) p39
5(c) cos(100πt+π/3)+sin(40πt+2π/3) periodic? period (10) p39
6(a) FT rect(t/τ); triangle Δ(t/τ) via convolution property (12) p40
6(b) energy of sin(2π10(t-1/40))/(π(t-1/40)) cos(2π15t) (11) p40
6(c) x·p (impulse train nπ/ωB) then h=sin(3ωB t/2)/(πt): spectra of p,z,h,y (12) p40
7(a) bilateral & unilateral LT of e^{at}u(-t), a>0 (11) p40
7(b) X(s)=(s^3+2s^2+3s+2)/(s^4+2s^3+2s^2+2s+2): LT of t x + dx/dt + ∫0^t x (12) p40
7(c) u(t)->δ(t-1)-> [δ(t) || e^{-2t}u] -> sum: Y(s), y(t) (12) p40
8(a) impulse response ideal band-stop filter (stop 10<|w|<20) (12) p41
8(b) RLC circuit H(s), h(t) (12) p41
8(c) f-i analog (11) p41 OUT
### EEE 301 2015-16 (EEE p42-46)  course "EEE 301"
1(a) periodic? period: 3cos(4t+π/3); [cos(2t-π/3)]^2; Σ_{n=-7}^{7} e^{-(2t-n)}; e^{j(πt-1)} (20) p42
1(b) power/energy: e^{-t}cos3t u; u-2u(t-2)+u(t-5); te^{-t}u - δ(t-2k) (15) p42
2(a) evaluate impulse integrals (i)-(vi) (20) p42
2(b) y=sin{x(t)+x(t-2)}, t>=0: linear, TI, causal, memoryless, stable (15) p42
3(a) y''+6y'+9y=2x'+8x: simulation diagram/state eq/STM (20) p43 OUT
3(b) h=(e^{-3t}-e^{-2t})u: zero-state response to u(t), e^{-t}u (15) p43
4(a) FS x=3+√3cos2t+sin2t+sin3t−½cos(5t+π/3) through RLC circuit: y; distortionless? (20) p43
4(b) x=cos4πt, y=sin4πt T=1/2: FS coeffs of z=xy via multiplication property (15) p43
5(a) X(w)=(2+j4w+w^2)/(3+j4w−w^2): FT of x*x(t−1); x(−2t+1)e^{−j2t} (10) p43
5(b) h1,h2 Hilbert-like filters, cos/sin: magnitude spectra x1,x2,y1,y2,y (15) p44
5(c) |X| for x=sin t sin(t/2)/(πt^2) (10) p44
6(a) impulse train: FS, FT, PSD (10) p44
6(b) z=x·y bandwidths 150, 350 Hz: max Ts; x=sin300πt/πt, y=sin700πt/πt: spectrum for Ts=0.5ms, 2ms (12) p44
6(c) y''+6y'+8y=2x: H(w); response to te^{-2t}u (13) p44
7(a) state space -> H(s), h(t) (17) p45 OUT
7(b) y''+5y'+6y=2e^{-t}u, y'(0-)=-2, y(0-)=3 by LT (13) p45
7(c) D'Alembert principle (5) p45 OUT
8(a) circuit with initial conditions, Laplace (15) p45
8(b) block diagram G1,G2,G3: Y(s), final value (10) p45
8(c) f-v analog (10) p46 OUT
### EEE 301 2014-15 (EEE p47-50)
1(a) x=u(cos t)-δ(t-kπ): periodic? period; sketch (9) p47
1(b) Σ_{k=-4}^{4} δ(3t-k) sin(πt/3) sgn(t): power/energy/neither (6) p47
1(c) x= -t+1 (-1..0), t (0..2), 2 (2..3): odd & even parts, their average values (20) p47
2(a) (i) y=sin(2t)log10[x(t)] (ii) y=e^{-jwt}∫x e^{-jwτ}dτ: linear/TI/causal/memoryless/invertible/stable (18) p47
2(b) y'+10y=2x: h(t); output for x=(-1)^k δ(t-5k), k=0,±1,±2; lim_{t→5}h=0 (17) p47
3 y''+6y'+8y=x'-x state space (35) p48 OUT
4(a) Cn=½[1-(-1)^n], T=20 ms: real? time-domain signal, sketch (18) p48
4(b) Cn=1/(n^2+1) e^{jnπ/3} into LC-R circuit: first four harmonic amplitudes, avg output (17) p48
5(a) SSB filter: spectrum of y for wf=wm; hf(t) (15) p48-49
5(b) FT of α rect(αt/τ); α→∞, α→0 (7) p49
5(c) x=e^{-αt}u, h=sin(2t)/(πt): FT of output (13) p49
6(a) x·cos w0t -> h1 bandpass -> ×cos w0t -> h2=sin wB t/πt: Y(w) (16) p49
6(b) natural sampling rectangular pulses: spectrum; recoverable? (15) p49
6(c) D'Alembert (4) p49 OUT
7(a) y''+4y'+3y=e^{-3t}u, y(0-)=0, y'(0-)=1 LT (15) p49
7(b) bilateral LT + ROC of e^{bt}u(-t) (7) p50
7(c) block diagram 1/(s+2), s/(s+3), gain 2: Y(s) (13) p50
8(a) RLC circuit initial energy LT model: Y(s), y(t) (13) p50
8(b) state space H(s), stability, step response (18) p50 OUT
8(c) analog circuit (4) p50 OUT
### EEE 301 2013-14 (EEE p51-?)
1(a) x1+x2 periodic? (i) 4cos πt, -sin(3πt+π/2) (ii) 4cos2t, 4cos2πt; periods (18) p51
1(b) delta models: lim (1/π) ε/(t^2+ε^2); lim (1/π) sin(εt)/t (17) p51
2(a) power/energy: u(t)+5u(t-1)-2u(t-2); 2sin(3πt/8)·cos(2πt/3)?? [x2=2 sin(3π/8)t cos(2π/3)t] (18) p51
2(b) y=∫0^t e^{-(t-τ)}x(τ)dτ: LTI? impulse response w/o computation; BIBO (17) p51
3(a) tan(2πt), sin(2π/t): convergent FS? (Dirichlet) (18) p51
3(b) exp FS of triangle wave fig (peak 2, period π?) (17) p51
4(a) state equations of circuit, stability (18) p52 OUT
4(b) x=B+A cos(w0t+θ) into LC-R circuit: y(t) (17) p52
5(a) circuit LT with initial conditions vc=1/2, iL=-1, x=u (18) p52
5(b) state space H(s), step response (17) p53 OUT
6(a) y''+4y'+3y=u, y(0-)=2, y'(0-)=1 LT (13) p53
6(b) bilateral LT + ROC of cos(at)u(-t) (7) p53
6(c) block diagram with disturbance G1,G2,G3,H2: Y(s), lim y (15) p53
7(a) AM system with channel filters: sketch X,Y,Z,V (15) p53
7(b) show F{sinc(ωB t/2π)} = (2π/ωB) rect(ω/ωB) (7) p54
7(c) x=[(1/12)e^{-t/4}+(1/6)e^{-t/2}]u through h=e^{-t/3}u: Y(w), y(t) (13) p54
8(a) impulse sampling period 1/8 ms, X triangle ωc=2π·5e3, filter ωf=2π·5e3: P(w), Xs(w), sketch, recoverable? (17) p54
8(b) f-i analog mechanical (10) p54 OUT
8(c) analog circuit (8) p54 OUT
### EEE 301 2012-13 (EEE p55-58)
1(a) x=α δ(sin t)+(1-α)δ(t-kπ), k odd: periodic? period; sketch α=0.5 (12) p55
1(b) Σ_{k=-4}^{4} δ(3t-k) sin^2(πt/3): power/energy/neither (12) p55
1(c) y=xe - xo: invertible? inverse (11) p55
2(a) (i) y=∫_{∞}^{2t-3} x dτ [sic, -∞] (ii) y=½|x(t)|-πt: properties (18) p55
2(b) h1=δ(t+1),h2=δ(t-1),h3=δ(t),h4=rect(t/2) (paths h1→h2 and h3→h4, summed): y for x=(-1)^k δ(t-10k) (17) p55
3 y'''+3y''-y'-2y=3x''-x: simulation/state eq/STM Cayley-Hamilton (35) p56 OUT
4(a) express x(t) fig in orthogonal basis φ1,φ2,φ3 on 0..3 (17) p56
4(b) half-wave rectified cos t into LC-R circuit: 2nd and 4th harmonic amplitudes (18) p56
5(a) FT of δ(t), 1, e^{jw0t}, cos w0t, sin w0t (12) p57
5(b) three related signals fig 5(b): X(w), Y1,Y2 via properties [figure not shown in PDF — illegible] (15) p57
5(c) convolution in time = multiplication in freq (8) p57
6(a) ideal LPF frequency response, impulse response, causality (8) p57
6(b) x=sin(ωB t/2)/πt, p=Σδ(t-nπ/ωB), h=sin(3ωB t/2)/πt: X,P,Z,H,Y,S and draw (15) p57
6(c) H1,H2 Hilbert-pair filters: draw H1,H2,X1,X2,Y (12) p57
7(a) LT of |x(t)| for fig 7(a) [figure missing — illegible] (10) p57
7(b) state & prove final value theorem (5) p57
7(c) impulse response from input e^{-2t}u and output (e^{-t}-3e^{-2t})u (5) p57
7(d) f-v, f-i analog; force (15) p57 OUT
8(a) state space H(s) (20) p58 OUT
8(b) circuit LT vc(0-)=1, iL(0-)=2, x=u: model, Y(s), y(t) (15) p58
(2012-13 fix: 5(b) fig on p59 = x rect(t/τ), y1 doublet ±1 on (-τ,0),(0,τ), y2 triangle ±τ; 7(a) fig on p60 = z(t) pulse train +1 (0..τ), -1 (T..T+τ), period 2T)
### EEE 301 2011-12 (EEE p61-65)
1(a) real odd, T=2, ck=0 |k|>1, ½∫0^2|x|^2=1: two signals (18) p61
1(b) H=sin4w/w; x=2+x1*Σδ(t-8k), x1=1 (0..4), -1 (4..8): output via FS (17) p61
2(a) g=x cos^2 t * sin t/(πt), X=0 |w|>=1: h mapping x→g (17) p61
2(b) alternating-sign impulse train sampling, T<π/(2ωm): recovery system; Xp, Y (18) p61
3(a) causal, two poles -2 and 4, x=1→y=0, h(0+)=4: H(s) (18) p62
3(b) direct form II diagram: diff eq; steady-state & transient to 2cos4t u(t) (17) p62
4(a) noncausal LTI one causal pole y''+y'-6y=x'-x, x=e^{-t}u(t)+e^{t}u(-t-2): ROC of Y, bilateral LT, y(t) (18) p62
4(b) ideal -90° phase shifter: h(t), output for cos w0 t (17) p62
5 state-space (7+10+10+8) p62-63 OUT
6(a) e^{j7πt/6}+e^{j5πt/6} periodic? period (7) p63
6(b) x=1 t<0, e^{3t} t>=0: energy/power/neither (7) p63
6(c) delta properties; ∫e^{-5t+1}δ'(t-5)dt (8) p63
6(d) x(t) fig (t+2 on -2..-1?, t-2 on 1..2): sketch x(-2t-2), analytical (13) p63
7(a) y=2x cos wc t: linear/TI/causal/stable (8) p64
7(b) canonical form I simulation diagram (10) p64 OUT
7(c) importance of y=x*h in real life (4) p64
7(d) h1=δ(t+4), h2=δ(t-4) summed → g, h3 triangle; x rect(-1..1): sketch g, y graphical (13) p64
8(a) y''+5y'+6y=x''+5x'+5x: h(t) (17) p64
8(b)(c) analogs (8,10) p65 OUT
### EEE 301 2010-11 (EEE p66-70)
1(a) square wave K, width τ, period T: Cn; spectra τ=1, T=5,10,15; effect of T (18) p66
1(b) x=A exp(j10^3 t) into RC (R=10 kΩ, C fig): system function, magnitude/phase, y(t) (17) p66
2(a) (i) FT of impulse train (ii) energy in Fourier domain (iii) convolution theorem (iv) FT of x cos w0 t (20) p66
2(b) x=sin(ωB t/2)/(πt) × impulse train p: X, P, period; Xs; h,H; Y (15) p67
3(a) y''+3y'+2y=0, y(0-)=3, y'(0-)=1: Y(s); with x=e^{-3t}u H(s); final value (12) p67
3(b) inverse LT impulse response of H=(s^2-3s+2)/(s^3+6s^2+11s+6); two canonical forms (23) p67 [canonical part OUT]
4(a) feedback with disturbance r=Au, w=Bu: Y(s); Hc design so y tracks r; final value (20) p67-68
4(b) D'Alembert, f-v analog (15) p68 OUT
5(a)(i) cos(πt/3)+sin(πt/4) periodic? (6) (ii) A e^{-αt}u(t) odd/even parts (6) p68
5(b)(i) x=u(t+2)-2u(t+1)+2u(t)-u(t-2)-2u(t-3)+2u(t-4): sketch, y=∫x (8) (ii) piecewise x: sketch x(t-2), x(t+3), x(-3t-2), x(2t/3+1/2) analytical (15) p68
6(a) power/energy: A e^{-t}u, A e^{-a|t|} (10) p69
6(b)(i) graphical conv x=1 (0..2), h triangle (-1..1) (10) (ii) impulse response h1..h5 interconnection; causal, stable (15) p69
7(a) y=At x(t): linear/TI/causal/stable (10) p69
7(b) state variable (25) p69 OUT
8(a)(b) state space (18,17) p70 OUT
