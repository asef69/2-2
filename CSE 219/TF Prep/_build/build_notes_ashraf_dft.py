"""Ashraf F1 — Overview, DTFT, DFT, DFT properties, circular convolution (Lec 0–2). Lessons 1–4."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c219 import B, ashraf, exam_map, mark, save_solved  # noqa: E402

CLIP = (0.0, 0.09, 1.0, 0.97)
n = ashraf("Lec 0–2 · DTFT and DFT, DFT Properties and Circular Convolution", "CSE219_Ashraf_DTFT_DFT_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "DFT questions and how much they matter"),
              ("Lesson 1 — From Fourier Series to the DFS and DFT", "sampling a periodic signal, N unique coefficients, the DFT pair"),
              ("Lesson 2 — The DTFT, and the DFT as Its Samples", "2π-periodic spectrum, inverse DTFT, zero-padding, bins → Hz"),
              ("Lesson 3 — DFT Properties", "the clock (mod N), circular shift, modulation, symmetry, Parseval"),
              ("Lesson 4 — Circular Convolution and Filtering with the DFT", "multiply DFTs = circular convolution; zero-pad to L + M − 1"),
              ("Quick Notes — DTFT and DFT", "merged revision notes + key diagrams")],
    source_note="Slide numbers are PDF page numbers of Lecture 1 - DTFT and DFT.pdf (38 pages, “Lec 1”) and Lecture 2 - DFT "
                "Properties and Applications.pdf (26 pages, “Lec 2”); the printed slide number on each page is one less. "
                "Lecture 0 (Overview of the Transforms, 41 pages) is history and says “Nothing here is examinable”; its one "
                "useful picture — the four-transform square — is in Lesson 1.")

n.h1("Exam Map — What the TF Papers Ask")
exam_map(n, "Ashraf", range(1, 5))
n.callout("focus", "Only two TF questions come straight from these decks (CSE 219 2023-24 Q5(b): linear convolution through "
          "the DFT, 10 marks; CSE 311 2016-17 Q3(a): derive and compute a DFT, 20 marks). But every FFT, Bluestein and "
          "sampling question (Lessons 5–12) is built on the DFT pair, W_N, the bin reading and circular convolution. "
          "Learn: the DFT/IDFT pair by heart, the 4-point W₄ table, X[N − k] = X*[k], and the zero-padding rule "
          "N ≥ L + M − 1.")

# ===================================================== L1
n.lesson("Lesson 1 — From Fourier Series to the DFS and DFT", "Lec 0 sl. 22; Lec 1 sl. 2–19")
n.h2("1. Four Fourier Transforms, One Rule (Lec 0 sl. 22; Lec 1 sl. 2)")
n.table(["", "continuous time", "discrete time"],
        [["periodic", "CTFS: discrete, aperiodic spectrum a_k", "DFS/DFT: discrete, periodic spectrum X[k]"],
         ["aperiodic", "CTFT: continuous, aperiodic X(jω)", "DTFT: continuous, periodic X(e^{jω})"]],
        widths_cm=[2.6, 7.3, 7.3])
n.callout("memorize", "Discrete in one domain ⇔ periodic in the other. Sampling time makes the spectrum periodic; keeping "
          "only N frequency bins makes time N-periodic. The DFT is the only one a computer can compute.")
n.h2("2. Sampling a Periodic Signal (sl. 5–10)")
n.p("x(t) has period T₀; take N samples per period, T₀ = NT_s, x[n] = x(nT_s) (N-periodic). Represent the sampling as "
    "x_p(t) = x(t)p(t) = Σ x[n]δ(t − nT_s). Its CTFS coefficients: the impulses sift the integral into a finite sum.")
n.code(["c_k = (1/T₀)∫_{T₀} x_p(t)e^{−jkω₀t}dt = (1/T₀)Σ_{n=0}^{N−1} x[n]e^{−jkω₀nT_s},   ω₀T_s = 2π/N",
        "    = (1/T₀)Σ_{n=0}^{N−1} x[n]e^{−j2πkn/N}",
        "c_{k+N} = c_k·e^{−j2πn} = c_k   ⇒ only N distinct coefficients (sampling in time made the spectrum periodic)",
        "c_{−k} = c_{N−k}  ⇒ negative frequencies fold onto the upper bins"])
n.h2("3. The Inverse by Orthogonality (sl. 12–14)")
n.code(["Σ_{k=0}^{N−1} e^{j2πk(n−m)/N} = N if n = m,  0 if n ≠ m   (geometric series: (1 − e^{j2π(n−m)})/(1 − e^{j2π(n−m)/N}) = 0)",
        "⇒ x[n] = (1/N)Σ_k (T₀c_k)e^{j2πkn/N}"])
n.h2("4. DFS and DFT (sl. 15–19)")
n.formula(["DFS:  a_k = (1/N)Σ_{n=0}^{N−1} x̃[n]e^{−j2πkn/N},   x̃[n] = Σ_{k=0}^{N−1} a_k e^{j2πkn/N}",
           "DFT:  X[k] = Σ_{n=0}^{N−1} x[n]W_N^{kn},   x[n] = (1/N)Σ_{k=0}^{N−1} X[k]W_N^{−kn},   W_N = e^{−j2π/N}"])
n.p("Bridges: X[k] = N·a_k (DFT = DFS rescaled); c_k = X[k]/T₀ (CTFS of the sampled periodic signal). The DFT never needs "
    "the continuous signal: any list of N numbers has one (sl. 18). Reading the bins: k = 0 … N/2 are positive "
    "frequencies (low → high); k = N/2 … N − 1 are the folded negative frequencies (high → low).")
n.figure_from_pdf(B[1], 11, "Figure 1.1 — Negative-frequency coefficients fold onto the upper bins (Lec 1, sl. 11)", clip=CLIP, width_cm=11)
n.exam_approach(["Derivation: sample, write x_p as an impulse train, sift the CTFS integral, use ω₀T_s = 2π/N.",
                 "Prove N-periodicity of the coefficients (k → k + N).", "Inverse: multiply by e^{j2πkn/N}, sum over k, "
                 "use the orthogonality sum.", "State the bin ↔ frequency map."])
n.practice("Lesson 1", "(a) Actual — CSE 311 2016-17 Q3(a). (b) Constructed (Lec 1, last slide).",
           ["(a) g(t) is sampled over 0 ≤ t ≤ T₀ at intervals T_s giving N₀ samples; G_q = Σ_{k=0}^{N₀−1} g_k e^{−jqΩ₀k}, "
            "g_k = T_s g(kT_s), G_q = G(qf₀), Ω₀ = 2πf₀T_s. (i) Derive this from G(f). (ii) Prove f₀ = 1/T₀. (iii) Compute the DFT "
            "for g(0..3) = 1, 2, 3, 4 (t = 0, 1, 2, 3); give the sample frequencies and G(f). (iv) How should T_s and T₀ be "
            "chosen? (4 + 5 + 5 + 6)",
            "(b) Compute the 4-point DFT of {1, 0, −1, 0}. Which bins light up and why?"])
n.solution()
n.code(["(i) G(f) = ∫₀^{T₀} g(t)e^{−j2πft}dt ≈ Σ_{k=0}^{N₀−1} g(kT_s)e^{−j2πfkT_s}·T_s   (rectangle rule, time-limited g)",
        "    evaluate at f = qf₀:  G(qf₀) = Σ g_k e^{−j2πqf₀kT_s} = Σ g_k e^{−jqΩ₀k},  Ω₀ = 2πf₀T_s",
        "(ii) Sampling in time makes G_q periodic; requiring the N₀ frequency samples to cover exactly one period",
        "     (G_{q+N₀} = G_q) needs e^{−jN₀Ω₀k} = 1 for all k ⇒ N₀Ω₀ = 2π ⇒ 2πf₀T_sN₀ = 2π ⇒ f₀ = 1/(N₀T_s) = 1/T₀",
        "(iii) T_s = 1, N₀ = 4 ⇒ T₀ = 4 s, f₀ = 0.25 Hz, Ω₀ = π/2, W = e^{−jπ/2} = −j",
        "     G₀ = 1+2+3+4 = 10          f = 0",
        "     G₁ = 1 − 2j − 3 + 4j = −2+2j   f = 0.25 Hz",
        "     G₂ = 1 − 2 + 3 − 4 = −2       f = 0.5 Hz (= f_s/2)",
        "     G₃ = 1 + 2j − 3 − 4j = −2−2j   f = 0.75 Hz ≡ −0.25 Hz  (G₃ = G₁*)",
        "(iv) T_s ≤ 1/(2B) to avoid aliasing (B = essential bandwidth);  T₀ long enough to capture g (time-limited) and",
        "     to give the needed resolution f₀ = 1/T₀;  N₀ = T₀/T_s, preferably a power of 2 for the FFT (zero-pad g)"])
n.answer("(b)", "X = {0, 2, 0, 2}: x = cos(πn/2) has frequency ω = π/2 = bin 1 and its negative partner −π/2 ≡ bin 3 "
         "(cos = ½e^{jπn/2} + ½e^{−jπn/2}, each with weight N/2 = 2).")
mark("2016-17", "CSE 311", "3(a)")

# ===================================================== L2
n.lesson("Lesson 2 — The DTFT, and the DFT as Its Samples", "Lec 1 sl. 20–34")
n.p("Aperiodic finite sequence x[n] (0 ≤ n ≤ N − 1). CTFT of the impulse train x_p(t) = Σx[n]δ(t − nT_s): "
    "X_p(jω) = Σ x[n]e^{−jωnT_s}. Relabel ωT_s → ω (digital frequency, rad/sample):")
n.formula(["X(e^{jω}) = Σ_n x[n]e^{−jωn}          x[n] = (1/2π)∫_{2π} X(e^{jω})e^{jωn}dω"])
n.bullets(["2π-periodic: X(e^{j(ω+2π)}) = X(e^{jω}) since e^{−j2πn} = 1 (sl. 25). Principal interval [−π, π] ↔ "
           "physical [−ω_s/2, ω_s/2].",
           "Inverse (sl. 26): substitute the analysis sum, swap sum and integral, use (1/2π)∫_{−π}^{π}e^{jωr}dω = δ[r].",
           "DFT = DTFT samples (sl. 29): X[k] = X(e^{jω})|_{ω=2πk/N}. Periodic view: FS coefficients; aperiodic view: N "
           "samples of the DTFT — the same N numbers.",
           "Zero-padding to M ≥ N (sl. 31): same DTFT, sampled at spacing 2π/M — more pixels, not more information.",
           "Bins to Hz (sl. 33–34): f_k = k f_s/N for 0 ≤ k ≤ N/2, (k − N)f_s/N above; Δf = f_s/N = 1/T₀ (numpy.fft.fftfreq order)."])
n.figure_from_pdf(B[1], 29, "Figure 2.1 — The N-point DFT samples one period of the DTFT (Lec 1, sl. 29)", clip=CLIP, width_cm=11)
n.code(["Worked example (sl. 32): x = {1, 2, 3, 4}, N = 4, W₄ = −j",
        "W₄^{kn}:   k=0: 1  1  1  1 |  k=1: 1 −j −1  j |  k=2: 1 −1  1 −1 |  k=3: 1  j −1 −j",
        "X = {10, −2+2j, −2, −2−2j};  |X| = {10, 2√2, 2, 2√2};  X[3] = X*[1] (bin 3 = bin 1's negative partner)",
        "N = 8, f_s = 8 kHz: Δf = 1 kHz;  bins 0..4 → 0..4 kHz,  bins 5,6,7 → −3, −2, −1 kHz"])
n.exam_approach(["Write W_N and its powers (W₄ = −j, W₈ = (1 − j)/√2).", "Tabulate W_N^{kn} (it is periodic in kn mod N).",
                 "Sum row by row; check X[0] = Σx and X[N − k] = X*[k] for real x.", "Convert bins to Hz with f_s/N."])

# ===================================================== L3
n.lesson("Lesson 3 — DFT Properties", "Lec 2 sl. 2–12")
n.p("Everything lives on a clock: indices are taken mod N, ((n))_N = n mod N, e.g. ((9))₈ = 1, ((−1))₈ = 7; the DFT "
    "sees the periodic extension x̃[n] = x[((n))_N]. One proof move gives every property: substitute into the DFT sum, "
    "re-index, and let the clock absorb whatever spills past the edge.")
n.table(["Property", "Time", "DFT"],
        [["linearity", "a x[n] + b y[n] (same N)", "a X[k] + b Y[k]"],
         ["circular time shift", "x[((n − m))_N]", "W_N^{km} X[k]  (phase only)"],
         ["modulation", "W_N^{−k₀n} x[n]", "X[((k − k₀))_N];  (−1)ⁿx ↔ X[k − N/2] (low ↔ high)"],
         ["time reversal", "x[((−n))_N]", "X[((−k))_N]"],
         ["conjugation", "x*[n]", "X*[((−k))_N]"],
         ["real signal", "x real", "X[N − k] = X*[k]: |X| even, ∠X odd about N/2"],
         ["duality", "X[n]", "N x[((−k))_N]"],
         ["circular convolution", "x ⊛ h", "X[k]H[k]"],
         ["multiplication", "x[n]h[n]", "(1/N) X ⊛ H"],
         ["Parseval", "Σ|x[n]|²", "(1/N)Σ|X[k]|²"]],
        widths_cm=[4.0, 5.4, 7.8])
n.code(["Circular shift proof: Σ x̃[n − m]W^{kn} = W^{km} Σ_{r=−m}^{N−1−m} x̃[r]W^{kr} = W^{km}X[k] (any N consecutive terms)",
        "Parseval check on {1,2,3,4}: 1+4+9+16 = 30 = (100 + 8 + 4 + 8)/4 ✓;  |X[k]|²/N = energy in bin k"])
n.callout("trap", "• Shifts are circular: x[n − m] on N points wraps the tail to the front. • Linearity needs equal "
          "lengths — zero-pad the shorter sequence first. • Real and even x̃ ⇒ X real.")

# ===================================================== L4
n.lesson("Lesson 4 — Circular Convolution and Filtering with the DFT", "Lec 2 sl. 13–23")
n.p("Linear convolution y = x * h has length L + M − 1. Multiply two N-point DFTs and invert:")
n.code(["y[n] = (1/N)Σ_k X[k]H[k]W^{−kn} = Σ_m x[m]·[(1/N)Σ_k H[k]W^{−k(n−m)}] = Σ_{m=0}^{N−1} x[m] h[((n − m))_N]"])
n.formula(["(x ⊛ h)[n] = Σ_{m=0}^{N−1} x[m] h[((n − m))_N]  ⇔  X[k]H[k]"])
n.p("Two-wheel picture (sl. 16): x on the outer wheel, h reversed on the inner wheel; rotate one tick per output, "
    "multiply across the spokes, add. The off-edge taps of linear convolution (which multiply nothing) are instead "
    "wrapped onto x's tail — that wrap (time aliasing) is the only difference.")
n.code(["Example (sl. 21): x = {2,4,5,6,5,3,2,1}, h = {1,2,1}",
        "linear (length 10): {2, 8, 15, 20, 22, 19, 13, 8, 4, 1}",
        "circular N = 8:    {6, 9, 15, 20, 22, 19, 13, 8}   — y[0] = 2+4, y[1] = 8+1: the tail {4, 1} wrapped onto the front"])
n.figure_from_pdf(B[2], 22, "Figure 4.1 — Zero-padding to N = 10 parks the wrapped taps on zeros (Lec 2, sl. 22)", clip=CLIP, width_cm=11)
n.formula(["Circular = linear  ⇔  N ≥ L + M − 1  (zero-pad both)"])
n.code(["Filtering recipe (sl. 23): 1) N ≥ L + M − 1, pad x and h   2) X = DFT{x}, H = DFT{h}",
        "                            3) Y = X·H bin by bin              4) y = IDFT{Y}; keep L + M − 1 samples",
        "Cost with direct DFTs ~N² each (loses to L·M); with the FFT ~N log₂N (Lesson 8) — the fastest known way"])
n.exam_approach(["Pick N ≥ L + M − 1 (a power of 2 if an FFT is asked).", "Zero-pad, compute both DFTs (W₄ table).",
                 "Multiply bin by bin.", "IDFT: x[n] = (1/N)Σ X[k]W^{−kn}; check against the direct convolution."])
n.practice("Lesson 4", "(a) Actual — CSE 219 2023-24 Q5(b). (b) Practice set 4.1, 4.4.",
           ["(a) x = {1, 2}, h = {1, 1}. Show step by step the linear convolution using the naive DFT method. (10)",
            "(b) {1, 2} * {1, −1} with a 4-point DFT; {1, 0, 1} * {1, −1, 2} with a 4-point DFT (show the wrap)."])
n.solution()
n.code(["(a) L + M − 1 = 3 ⇒ use N = 4 (N = 3 also works). Pad: x = {1,2,0,0}, h = {1,1,0,0}; W₄ = −j",
        "    X[k] = Σ x[n](−j)^{kn}:  X = {3, 1 − 2j, −1, 1 + 2j}",
        "    H[k]:                    H = {2, 1 − j, 0, 1 + j}",
        "    Y = XH = {6, (1−2j)(1−j) = −1 − 3j, 0, −1 + 3j}",
        "    y[n] = ¼Σ Y[k] j^{kn}:",
        "    y[0] = ¼(6 − 1 − 3j + 0 − 1 + 3j) = 1",
        "    y[1] = ¼(6 + (−1−3j)j + 0 + (−1+3j)(−j)) = ¼(6 + 3 − j + 3 + j) = 3",
        "    y[2] = ¼(6 − (−1−3j) + 0 − (−1+3j)) = ¼(6 + 1 + 3j + 1 − 3j) = 2",
        "    y[3] = ¼(6 + (−1−3j)(−j) + 0 + (−1+3j)(j)) = ¼(6 − 3 + j − 3 − j) = 0",
        "    y = {1, 3, 2} (+ a trailing 0) = direct x * h ✓"])
n.code(["(b) {1,2}*{1,−1}: X = {3, 1−2j, −1, 1+2j}, H = {0, 1+j, 2, 1−j} ⇒ y = {1, 1, −2, 0}",
        "    {1,0,1}*{1,−1,2}: linear = {1, −1, 3, −1, 2} (N ≥ 5 ⇒ use 8); with N = 4 the last sample wraps:",
        "    circular = {1 + 2, −1, 3, −1} = {3, −1, 3, −1}"])
mark("2023-24", "CSE 219", "5(b)")

n.quick_notes("Quick Notes — DTFT and DFT", "Revision points for Lessons 1–4.",
              [("L1 · DFS/DFT", ["c_k = (1/T₀)Σx[n]e^{−j2πkn/N}; c_{k+N} = c_k; c_{−k} = c_{N−k}.",
                                "X[k] = Σx[n]W^{kn}, x[n] = (1/N)ΣX[k]W^{−kn}, W_N = e^{−j2π/N}; X[k] = N a_k."]),
               ("L2 · DTFT", ["X(e^{jω}) = Σx[n]e^{−jωn}, 2π-periodic; inverse (1/2π)∫_{2π}.",
                             "X[k] = X(e^{j2πk/N}); zero-padding = finer samples; f_k = k f_s/N."]),
               ("L3 · Properties", ["circular shift ↔ W^{km}X[k]; real x ⇒ X[N−k] = X*[k]; Parseval Σ|x|² = (1/N)Σ|X|²."]),
               ("L4 · Circular conv", ["XH ↔ x ⊛ h; circular = linear iff N ≥ L + M − 1.",
                                      "{1,2} * {1,1} = {1,3,2} via 4-point DFTs: Y = {6, −1−3j, 0, −1+3j}."])],
              diagrams=[(B[2], 16, "Circular convolution: two wheels (Lec 2, sl. 16)", CLIP, 11)])
n.save()
save_solved("ashraf_dft")
print("saved", n.out_path)
