"""Ashraf F3 — Sampling and reconstruction (Lec 5). Lessons 9–12."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c219 import B, ashraf, exam_map, mark, save_solved  # noqa: E402

CLIP = (0.0, 0.09, 1.0, 0.97)
n = ashraf("Lec 5 · Sampling, Aliasing and Reconstruction", "CSE219_Ashraf_Sampling_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "sampling questions and their weight"),
              ("Lesson 9 — Impulse-Train Sampling and the Spectrum of the Sampled Signal", "Xp = (1/T)ΣX(j(ω − kωs)), P(jω), duality, FT of impulse trains"),
              ("Lesson 10 — The Sampling Theorem and Aliasing", "ωs > 2ωM, proof, oversampling vs aliasing, natural sampling"),
              ("Lesson 11 — Ideal Reconstruction, ZOH and Linear Interpolation", "sinc interpolation, h0, h1, comparison, real-time DAC"),
              ("Lesson 12 — Practical Issues; Connection to the DFT", "time-limited ⇒ not band-limited, anti-alias filter, periodic signals"),
              ("Quick Notes — Sampling", "merged revision notes + key diagrams")],
    source_note="Slide numbers are PDF page numbers of Lecture 5 - Sampling.pdf (47 pages, “Lec 5”); the printed slide "
                "number is one less. Natural sampling and discrete-time down-sampling (CSE 219 2022-23 Q4(b)) are textbook "
                "background (marked).")

n.h1("Exam Map — What the TF Papers Ask")
exam_map(n, "Ashraf", range(9, 13))
n.callout("focus", "Sampling is asked in every paper: 'state and prove the sampling theorem' (CSE 311 2012-13, 2013-14, "
          "2016-17; CSE 219 2022-23 Q1(c) 15 marks, 2023-24 Q7(c) 10), spectrum sketches of an impulse-sampled signal "
          "(EEE every year) and aliasing explanations. Know the one-line derivation Xp = (1/T)ΣX(j(ω − kωs)) and the "
          "sketch of non-overlapping vs overlapping copies.")

# ===================================================== L9
n.lesson("Lesson 9 — Impulse-Train Sampling and the Spectrum of the Sampled Signal", "Lec 5 sl. 4–17")
n.p("Many signals give the same samples (sl. 5), so recovery needs a condition. Model sampling as multiplication by an "
    "impulse train (sl. 6):")
n.formula(["x_p(t) = x(t)p(t) = Σ x(nT)δ(t − nT),   p(t) = Σ δ(t − nT),   ω_s = 2π/T"])
n.h2("Two roads to X_p(jω) (sl. 8–17)")
n.bullets(["Road 1 — transform the product: X_p(jω) = Σ x(nT)e^{−jωnT}: correct (it is the DTFT after ωT → ω) but "
           "X(jω) does not appear — uninterpretable.",
           "Road 2 — multiplication in time = convolution in frequency: X_p = (1/2π)X(jω) * P(jω). Needs P(jω)."])
n.code(["Duality:  x(t) ↔ X(jω) ⇒ X(jt) ↔ 2πx(−ω)       (from x(t) = (1/2π)∫X e^{jωt}dω: 2πx(−t) = ∫X(jω)e^{−jωt}dω, rename)",
        "Multiplication ↔ convolution:  u(t)v(t) ↔ (1/2π)U * V   (duality of the convolution property)",
        "P(jω): p is T-periodic ⇒ Fourier series p = (1/T)Σ e^{jkω_s t} (c_k = (1/T)∫δ(t)e^{−jkω_s t}dt = 1/T);",
        "       e^{jkω_s t} ↔ 2πδ(ω − kω_s)  ⇒  P(jω) = (2π/T)Σ δ(ω − kω_s)   (an impulse train is an impulse train)",
        "Convolving with δ(ω − kω_s) just shifts: X * δ(ω − kω_s) = X(j(ω − kω_s))"])
n.formula(["X_p(jω) = (1/2π) X(jω) * (2π/T)Σδ(ω − kω_s) = (1/T) Σ_{k=−∞}^{∞} X(j(ω − kω_s))"])
n.figure_from_pdf(B[5], 17, "Figure 9.1 — Sampling replicates X(jω) at every kω_s, scaled by 1/T (Lec 5, sl. 17)", clip=CLIP, width_cm=12)
n.h2("FT of an Impulse Train (also asked directly)")
n.p("Σ δ(t − nT) has Fourier series coefficients 1/T for every k, so its FT is (2π/T)Σδ(ω − 2πk/T): impulses of area 2π/T "
    "at multiples of ω_s. Closer samples (small T) give sparser, higher spectral lines.")
n.callout("memorize", "Spectrum of the sampled signal = the original spectrum repeated every ω_s and divided by T. Copies "
          "are 2ω_M wide and ω_s apart.")
n.exam_approach(["Sketch X(jω) with its edge ω_M.", "Write P(jω) = (2π/T)Σδ(ω − kω_s) and the factor 1/(2π).",
                 "Draw copies at kω_s with height scaled by 1/T.", "Decide overlap: ω_s − ω_M vs ω_M."])
n.practice("Lesson 9", "(a) Actual — CSE 311 2019-20 Q3. (b) Actual — EEE 211 2018-19 Q3(a) and 2019-20 Q8(a). (c) Actual — EEE 211 "
           "2019-20 Q7(b), 2016-17 Q6(c). (d) Actual — EEE 301 2013-14 Q8(a), 2011-12 Q2(b), 2010-11 Q2(b), 2012-13 Q6(b). "
           "(e) Actual — CSE 311 2014-15 Q8(a).",
           ["(a) FT of g(t) = 2B sinc(2πBt) [sinc x = sin x/x]; spectrum after sampling at 1.5 × Nyquist; general expression "
            "for the sampled spectrum at rate f_s. (35)",
            "(b) Show that the FT of an impulse train is an impulse train; sketch both. (10–15)",
            "(c) x(t) = sin(ω_Bt/2)/(πt), p(t) = Σδ(t − nπ/ω_B), z = xp, y = z * h with h = sin(3ω_Bt/2)/(πt). Find y(t). (20; 12)",
            "(d) Impulse sampling of a band-limited signal followed by filters (alternating sign train, squarer, 1/8 ms period).",
            "(e) FT of the impulse-sampled signal G_δ(f); the sampling theorem. (15)"])
n.solution()
n.code(["(a) g(t) = 2B sinc(2πBt) = sin(2πBt)/(πt) ↔ G(f) = rect(f/2B) (height 1, |f| < B). Nyquist rate 2B, so f_s = 3B:",
        "    G_s(f) = f_s Σ_k G(f − k f_s) = 3B Σ rect((f − 3Bk)/2B): rectangles of height 3B, width 2B, every 3B (gaps of B).",
        "    (for Bsinc²(πBt): G = triangle of height 1 and half-width B ⇒ Nyquist 2B again; at 3B: triangles every 3B, height 3B, non-overlapping)",
        "    general: G_δ(f) = f_s Σ_{n=−∞}^{∞} G(f − n f_s)   (from g_δ(t) = g(t)Σδ(t − nT_s), Σδ(t − nT) = f_s Σ e^{j2πn f_s t})",
        "(b) Σδ(t − nT) = (1/T)Σ e^{jkω_s t} ⇒ FT (2π/T)Σδ(ω − kω_s): impulses of area 2π/T at 0, ±ω_s, ±2ω_s …",
        "(c) X = rect(|ω| < ω_B/2) (height 1); P = (2ω_B)Σδ(ω − 2ω_B k)  [T = π/ω_B ⇒ ω_s = 2ω_B]; Z = (1/2π)X * P = ω_B/π Σ X(ω − 2kω_B)/…",
        "    copies of height ω_B/π at multiples of 2ω_B, each of width ω_B (no overlap: ω_B < 2ω_B − ω_B/2... gaps exist);",
        "    h passes |ω| < 3ω_B/2 ⇒ only the k = 0 copy (the next starts at 2ω_B − ω_B/2 = 1.5ω_B)  ⇒",
        "    Y = (ω_B/π)·X ⇒ y(t) = (ω_B/π)x(t) = ω_B sin(ω_Bt/2)/(π²t)",
        "(d) same picture: X_s = (1/T)ΣX(ω − kω_s); with ω_s > 2ω_M copies are separated, an LPF of cutoff ω_s/2 and gain T recovers x.",
        "    Alternating-sign train p = Σ(−1)ⁿδ(t − nT): period 2T, P = (2π/2T)·Σ_{odd k} 2·δ(ω − kπ/T) (odd harmonics only) ⇒ copies",
        "    centred at ±ω_s/2, ±3ω_s/2…: recovery requires a band-pass filter at ω_s/2 followed by demodulation by cos(ω_s t/2).",
        "(e) g_δ(t) = Σ g(nT_s)δ(t − nT_s) = g(t)·Σδ(t − nT_s) ⇒ G_δ(f) = G(f) * f_s Σδ(f − n f_s) = f_s ΣG(f − n f_s)"])
mark("2019-20", "CSE 311", "3", "◐ Method")
for k in [("2018-19", "EEE 211", "3(a)"), ("2019-20", "EEE 211", "8(a)"), ("2019-20", "EEE 211", "7(b)"),
          ("2014-15", "CSE 311", "8(a)")]:
    mark(*k)
for k in [("2016-17", "EEE 211", "6(c)"), ("2013-14", "EEE 301", "8(a)"), ("2011-12", "EEE 301", "2(b)"),
          ("2010-11", "EEE 301", "2(b)"), ("2012-13", "EEE 301", "6(b)")]:
    mark(*k, "◐ Method")

# ===================================================== L10
n.lesson("Lesson 10 — The Sampling Theorem and Aliasing", "Lec 5 sl. 19–22; natural sampling: textbook")
n.formula(["Band-limited x: X(jω) = 0 for |ω| > ω_M.  Then x(t) is uniquely determined by x(nT) if ω_s > 2ω_M (ω_s = 2π/T)",
           "Nyquist rate = 2ω_M  (f_s > 2f_M); T < π/ω_M"])
n.h2("Proof (exam-ready)")
n.numbered(["X_p(jω) = (1/T)ΣX(j(ω − kω_s)) (Lesson 9): copies of X at kω_s, each [kω_s − ω_M, kω_s + ω_M].",
            "Neighbouring copies stay apart iff ω_M < ω_s − ω_M ⇔ ω_s > 2ω_M.",
            "Then the central copy is an untouched X(jω)/T; an ideal LPF H = T on |ω| < ω_c, ω_M < ω_c < ω_s − ω_M, recovers X "
            "exactly, hence x(t) (Lesson 11 gives x(t) = Σx(nT)sinc((t − nT)/T)).",
            "If ω_s < 2ω_M the copies overlap and add; the overlapped values cannot be separated, so no filter can "
            "recover X ⇒ x(t) is not uniquely determined (two different band-limited... signals give identical samples)."])
n.figure_from_pdf(B[5], 22, "Figure 10.1 — Undersampling: the copies overlap and high frequencies fold into the baseband (Lec 5, sl. 22)",
                  clip=CLIP, width_cm=12)
n.table(["Case", "Condition", "Result"],
        [["Oversampling", "ω_s > 2ω_M", "copies separated by a guard band; recoverable with an LPF"],
         ["Critical sampling", "ω_s = 2ω_M", "copies touch; works only in the limit (sinc kernel), impractical"],
         ["Undersampling", "ω_s < 2ω_M", "overlap = **aliasing**: frequency ω appears as ω − kω_s; irreversible"]],
        widths_cm=[3.6, 3.6, 10.0])
n.h2("Aliasing and Practical Cures")
n.bullets(["Cause: sampling too slowly (or a signal not band-limited): spectral copies overlap, high frequencies masquerade "
           "as low ones (e.g. wagon wheels, a 1.8 kHz tone sampled at 2.8 kHz appears at 1 kHz).",
           "Problems: distortion that cannot be undone; the original signal is lost.",
           "Cures: an analog **anti-aliasing low-pass filter** before sampling (cutoff ≤ f_s/2); sample above Nyquist "
           "(oversample, which also eases reconstruction filter design); a guard band.",
           "Why practical signals always alias a little: real signals are time-limited, so their spectra are not exactly "
           "band-limited (Lesson 12)."])
n.h2("Discrete-Time Sampling (textbook)")
n.p("For a sequence, X(e^{jω}) = 0 for 2π/9 ≤ |ω| ≤ π, i.e. bandlimited to W = 2π/9. Keeping every M-th sample "
    "(rate 1/M of the original) is alias-free iff MW ≤ π ⇒ M ≤ 4.5 ⇒ M = 4 (largest integer): the lowest rate is the "
    "original rate/4 (a sample every 4 steps): bandwidth 2π/9 → spread to 8π/9 < π.")
n.h2("Natural Sampling (textbook)")
n.p("Multiply by a train of rectangular pulses of width τ, period T: p(t) has Fourier coefficients c_k = (τ/T)sinc(kτ/T), so "
    "X_s(ω) = Σ c_k X(ω − kω_s): the copies have **different heights** (sinc-weighted) but the same shape — x is "
    "recoverable with an LPF if ω_s > 2ω_M, only scaled by c₀ = τ/T.")
n.exam_approach(["Sketch X(jω); mark ω_M; find ω_s and compare with 2ω_M.", "Draw copies at ±ω_s, ±2ω_s with height 1/T.",
                 "Aliasing: show the overlap region; cure: anti-aliasing filter / higher f_s.", "Multiple signals: use the "
                 "highest frequency present (bandwidth of a product = sum of the bandwidths)."])
n.practice("Lesson 10", "(a) Actual — CSE 219 2022-23 Q1(c). (b) Actual — CSE 219 2023-24 Q7(c). (c) Actual — CSE 311 2012-13 Q8(a), "
           "2013-14 Q2(a), 2016-17 Q2(b). (d) Actual — CSE 311 2018-19 Q3(b), 2014-15 Q2(c) [L-3]. (e) Actual — CSE 219 2022-23 "
           "Q4(b). (f) Actual — EEE 211 2018-19 Q3(b), EEE 301 2015-16 Q6(b). (g) Natural sampling: EEE 211 2017-18 Q2(c), "
           "EEE 301 2014-15 Q6(b).",
           ["(a) Band-limited x(t) with ω_s > 2ω_M; analyze how x(t) is uniquely determined by its samples x(nT). (15)",
            "(b) State the Nyquist–Shannon theorem; analyze X_p(jω) when ω_s satisfies/violates it; sketch; why is perfect "
            "reconstruction impossible after aliasing? (10)",
            "(c) State and prove the sampling theorem; why in practice is the signal band-limited first and why is the rate "
            "above Nyquist? Prove the minimum sampling frequency is 2B. (13–16)",
            "(d) Cause of aliasing, its problems and compensation. (20)",
            "(e) A sequence has X(e^{jω}) = 0 for 2π/9 ≤ |ω| ≤ π. Lowest rate to sample it for perfect reconstruction? (10)",
            "(f) x = sin 1000πt + cos 1200πt: sampling period for no aliasing. z = xy with x, y band-limited to 150 Hz and "
            "350 Hz: maximum T_s; spectra for T_s = 0.5 ms and 2 ms. (10; 12)",
            "(g) Natural sampling with a rectangular pulse train: spectrum; can x be recovered?"])
n.solution()
n.answer("(a)", "Proof steps 1–3 above; uniqueness: if two band-limited signals had equal samples, their sampled spectra "
         "(1/T)ΣX₁(j(ω − kω_s)) and (1/T)ΣX₂(…) would be equal, and with no overlap the central copies X₁ = X₂ ⇒ x₁ = x₂.")
n.answer("(b)", "Theorem (steps 1–4). Satisfied: copies spaced ω_s apart, guard band ω_s − 2ω_M, LPF recovers x. Violated: "
         "overlap, aliasing; the overlapped region is a sum of two or more frequency components, an information loss that "
         "no linear filter can invert (in the overlap X_p(jω) cannot tell which copy each part came from).")
n.answer("(c)", "Proof as above (CSE 311 papers: X_p(f) = f_sΣG(f − nf_s); LPF of bandwidth B recovers G if f_s ≥ 2B — the "
         "boundary f_s = 2B is the minimum). (i) A band-limiting filter before sampling removes energy above f_s/2 that "
         "would alias. (ii) A rate above Nyquist leaves a guard band so a realizable (non-ideal, finite-slope) "
         "reconstruction filter can separate the copies.")
n.answer("(d)", "Cause: copies of the spectrum overlap because f_s < 2f_M (or the signal has components above f_s/2). Effects: "
         "a component at f appears at |f − kf_s| in the baseband (e.g. 1.8 kHz at f_s = 2.8 kHz → 1 kHz), irreversibly "
         "distorting the signal. Compensation: anti-aliasing LPF before the sampler, higher sampling rate, "
         "guard band; after sampling nothing can be undone.")
n.answer("(e)", "W = 2π/9; down-sampling by M keeps no aliasing iff MW ≤ π ⇒ M ≤ 4.5 ⇒ **M = 4**: the sequence can be sampled "
         "(decimated) at ¼ of its rate; the lowest rate is 1 sample per 4 (new bandwidth 8π/9 < π).")
n.code(["(f) sin 1000πt: f = 500 Hz; cos 1200πt: 600 Hz ⇒ f_M = 600 Hz ⇒ f_s > 1200 Hz ⇒ T < 1/1200 s = 0.833 ms",
        "    z = xy: bandwidth 150 + 350 = 500 Hz ⇒ T_s,max = 1/(2·500) = 1 ms",
        "    T_s = 0.5 ms (f_s = 2 kHz): copies every 2 kHz, each ±500 Hz wide ⇒ no overlap (guard 1 kHz)",
        "    T_s = 2 ms (f_s = 500 Hz): copies every 500 Hz overlap (width 1000 Hz) ⇒ aliasing, flat sum between copies"])
n.answer("(g)", "Pulse train coefficients c_k = (τ/T)sinc(kτ/T); X_s(ω) = ΣX c_k X(ω − kω_s): copies of the same shape with heights "
         "c_k·X; recoverable by an LPF of gain T/τ if ω_s > 2ω_M.")
for k in [("2022-23", "CSE 219", "1(c)"), ("2023-24", "CSE 219", "7(c)"), ("2012-13", "CSE 311", "8(a)"),
          ("2013-14", "CSE 311", "2(a)"), ("2016-17", "CSE 311", "2(b)"), ("2018-19", "CSE 311", "3(b)"),
          ("2014-15", "CSE 311", "2(c) [L-3]"), ("2022-23", "CSE 219", "4(b)"), ("2018-19", "EEE 211", "3(b)"),
          ("2015-16", "EEE 301", "6(b)"), ("2017-18", "EEE 211", "2(c)"), ("2014-15", "EEE 301", "6(b)")]:
    mark(*k)

# ===================================================== L11
n.lesson("Lesson 11 — Ideal Reconstruction, ZOH and Linear Interpolation", "Lec 5 sl. 24–36")
n.h2("1. Ideal Reconstruction (sl. 24–27)")
n.code(["H(jω) = T for |ω| < ω_s/2 (= π/T), 0 otherwise  (ω_M < ω_c < ω_s − ω_M)",
        "h(t) = (1/2π)∫_{−π/T}^{π/T} T e^{jωt}dω = sin(πt/T)/(πt/T) = sinc(t/T)   (sinc x = sin πx/πx)",
        "x_r(t) = x_p * h = Σ x(nT) sinc((t − nT)/T)   (sum of shifted sincs)",
        "h is non-causal (non-zero for t < 0) and decays slowly ⇒ unrealizable ⇒ approximations"])
n.h2("2. Zero-Order Hold (sl. 28–31)")
n.p("Hold each sample for T: h₀(t) = 1 on [0, T] (a staircase; every real DAC). Each sample y(nT) contributes "
    "y(nT)h₀(t − nT), which must be 1 from nT to (n + 1)T and 0 elsewhere.")
n.formula(["H₀(jω) = ∫₀^T e^{−jωt}dt = (1 − e^{−jωT})/(jω) = T e^{−jωT/2} sinc(ωT/2π)"])
n.p("Magnitude T|sinc(ωT/2π)|: droops inside the passband |ω| < ω_s/2 (about −3.9 dB at ω_s/2) and does not cut out "
    "the aliasing copies (non-zero beyond ω_s/2). Phase −ωT/2: a pure delay of T/2 — causal.")
n.h2("3. Linear Interpolation / First-Order Hold (sl. 32–35)")
n.p("Join adjacent samples by straight lines: the weight of y(nT) must rise 0 → 1 over [(n − 1)T, nT] and fall 1 → 0 over "
    "[nT, (n + 1)T] ⇒ h₁ = triangle on [−T, T], peak 1. It equals (1/T)·[h₀(t + T/2) * h₀(t + T/2)].")
n.formula(["H₁(jω) = (1/T)[T sinc(ωT/2π)]² = T sinc²(ωT/2π)   (real, no delay — the triangle is non-causal; delaying it by T makes it causal)"])
n.table(["", "Ideal (sinc)", "ZOH (rect)", "Linear interp. (triangle)"],
        [["h(t)", "sinc(t/T), ∞ both sides", "1 on [0, T]", "triangle on [−T, T]"],
         ["H(jω)", "T rect(|ω| < ω_s/2)", "T e^{−jωT/2} sinc(ωT/2π)", "T sinc²(ωT/2π)"],
         ["causal?", "no", "yes", "no (needs one sample ahead; delay T makes it causal)"],
         ["|H| at ω_s/4 (T = 1)", "1", "0.90", "0.81"],
         ["out-of-band leakage", "none", "large (sinc sidelobes)", "small (sinc² falls faster)"],
         ["use", "theory, offline", "real-time DACs", "smoother offline/graphics"]],
        widths_cm=[3.4, 4.3, 4.8, 4.7], font_size=8.5)
n.figure_from_pdf(B[5], 36, "Figure 11.1 — Magnitude responses of ideal, ZOH and linear interpolation (Lec 5, sl. 36)", clip=CLIP, width_cm=12)
n.callout("answer", "Real-time DAC (CSE 219 2023-24 Q5(c)(ii)): choose the **zero-order hold**. It is causal, needs only the "
          "current sample (no delay buffer), is a simple hold circuit inside the DAC, and its droop/leakage can be "
          "corrected with an analog reconstruction filter. The ideal sinc is non-causal and infinitely long; linear "
          "interpolation needs the next sample (one-sample delay buffer), so it is not directly real-time.")
n.exam_approach(["Write h(t) for each method and the reason it has that shape (weight of one sample).",
                 "Derive H(jω) by Fourier integration (rect → sinc), triangle = rect * rect.", "Compare causality, "
                 "passband flatness and out-of-band leakage.", "State a one-line advantage and drawback of each."])
n.practice("Lesson 11", "(a) Actual — CSE 219 2023-24 Q5(c). (b) Actual — CSE 311 2018-19 Q1(a), 2021-22 Q3(b), 2010-11 Q6(c), "
           "2020-21 Q1(b).",
           ["(a) An engineer must convert stored samples to an analog signal using an ideal sinc low-pass filter, a ZOH, or "
            "linear interpolation; the hardware cannot do non-causal filtering and no delay buffer is allowed. (i) Compare "
            "the three impulse responses. (ii) Which should he choose? (5 + 5)",
            "(b) g(t) is band-limited to 50 Hz; samples at 0.01 s: g(0) = 1, all others 0. Find g(t) and G(f) and its "
            "characteristics. Same with Nyquist-rate samples zero except g(0) = A. Samples at 2B through an ideal LPF of "
            "bandwidth B give an output ∝ f(t). Can the past samples foretell the future?"])
n.solution()
n.answer("(a)", "(i) Ideal: h = sinc(t/T), two-sided and infinite ⇒ non-causal. ZOH: h₀ = rect on [0, T] ⇒ causal, "
         "finite. Linear: h₁ = triangle on [−T, T] ⇒ finite but non-causal. (ii) ZOH (see EXAM-READY ANSWER).")
n.code(["(b) samples g(0.01k) = δ[k]: f_s = 100 Hz = 2 × 50 Hz (Nyquist rate), so g = Σδ[k]sinc((t − 0.01k)/0.01) = sinc(100t)",
        "    = sin(100πt)/(100πt);  G(f) = 0.01·rect(f/100) (flat 0.01 on |f| < 50 Hz, T = 0.01).",
        "    Characteristics: band-limited (|f| ≤ 50 Hz), even, real, non-causal, infinite duration, zeros at t = ±0.01k, energy",
        "    E = ∫|G|²df = 0.01²·100 = 0.01;  G(f)/T flat = the spectrum of a 'band-limited δ': as B → ∞, g → δ(t), G → 1",
        "    — the Dirac delta's flat spectrum is the limiting case (justifies δ ↔ 1).",
        "    Samples zero except g(0) = A at Nyquist ⇒ g = A sinc(t/T)·…; same form scaled by A.",
        "    Samples at 2B through an LPF (gain T, cutoff B): Σf(nT)δ(t − nT) → f(t) ⇒ output ∝ f(t) (proportionality "
        "constant = filter gain × T... equals f when gain T).",
        "    'Foretell the future': every future sample of a band-limited signal is determined by the past (the sinc-sum "
        "      is a linear combination), but only in theory — infinite memory, exact band limit and no noise are needed."])
for k in [("2023-24", "CSE 219", "5(c)"), ("2018-19", "CSE 311", "1(a)"), ("2021-22", "CSE 311", "3(b)"),
          ("2010-11", "CSE 311", "6(c)")]:
    mark(*k)
mark("2020-21", "CSE 311", "1(b)", "◐ Method")

# ===================================================== L12
n.lesson("Lesson 12 — Practical Issues; Connection to the DFT", "Lec 5 sl. 38–47")
n.h2("Time-limited vs Band-limited (sl. 38)")
n.p("A signal cannot be both time-limited and strictly band-limited (uncertainty principle). Real signals are "
    "finite-duration, so their spectra have infinite tails; the tails always overlap in sampling ⇒ **some aliasing is "
    "unavoidable**. Practical measures: anti-aliasing filter, rate above Nyquist, realizable reconstruction filters "
    "(ZOH + analog LPF), quantization noise handled separately.")
n.h2("DTFT and DFT from the Sampled Signal (sl. 39–42)")
n.bullets(["X_p(jω) = Σx[n]e^{−jωnT} repeats every ω_s; with ωT → ω this is the DTFT.",
           "The ideal LPF keeps one ω_s-wide period: x(t) = (1/2π)∫_{−ω_s/2}^{ω_s/2}T X_p(jω)e^{jωt}dω ⇒ inverse DTFT at t = nT.",
           "The N-point DFT = N uniform samples of one ω_s-wide period: X[k] = X_p(jkω_s/N)."])
n.h2("Periodic Signals (sl. 43–47)")
n.code(["x(t) = Σ a_k e^{jkω₀t} ⇒ X(jω) = 2πΣa_kδ(ω − kω₀);  sample N times per period: T₀ = NT, ω_s = Nω₀",
        "X_p = (1/T)ΣX(j(ω − rω_s)) = (2π/T)ΣΣ a_k δ(ω − kω₀ − rω_s): every line is copied into every band",
        "Nyquist for periodic x: a_k = 0 for |k| ≥ N/2 (|kω₀| < ω_s/2) ⇒ one clean copy per band",
        "c_k = a_k/T, X[k] = T₀c_k = N a_k; inverse DFT x[n] = (1/N)Σ_{k=0}^{N−1}X[k]e^{j2πkn/N}"])
n.practice("Lesson 12", "(a) Actual — CSE 311 2013-14 Q2(b), 2020-21 Q3(a).",
           ["(a) What are the practical issues in sampling and reconstruction? Why can practical signals not be fully "
            "recovered? How are the problems handled/minimised? (10; 24)"])
n.solution()
n.answer("(a)", "Practical issues: (1) real signals are time-limited ⇒ not band-limited ⇒ aliasing from the spectral tails; "
         "(2) the ideal LPF/sinc interpolator is non-causal and infinite, so reconstruction is approximate (ZOH, "
         "linear interpolation, finite-length filters); (3) samplers are not ideal impulses (finite-width pulses, "
         "jitter); (4) quantization noise; (5) the signal must be known for all time for exact recovery. Handling: an "
         "anti-aliasing LPF before the sampler, sample above Nyquist (guard band), reconstruct with a ZOH followed by an "
         "analog low-pass (compensating the sinc droop), use practical band-limits (essential bandwidth), enough bits.")
for k in [("2013-14", "CSE 311", "2(b)"), ("2020-21", "CSE 311", "3(a)")]:
    mark(*k)

n.quick_notes("Quick Notes — Sampling", "Revision points for Lessons 9–12.",
              [("L9 · Sampled spectrum", ["x_p = xΣδ(t − nT); X_p = (1/T)ΣX(j(ω − kω_s)); P = (2π/T)Σδ(ω − kω_s).",
                                         "Duality: X(jt) ↔ 2πx(−ω); product ↔ (1/2π) convolution."]),
               ("L10 · Theorem, aliasing", ["ω_s > 2ω_M; T < π/ω_M. Overlap = aliasing: f → |f − kf_s|; irreversible.",
                                           "Cure: anti-alias LPF, higher rate. Product xy: bandwidths add. Natural sampling: sinc-weighted copies.",
                                           "DT: M ≤ π/W (W = 2π/9 ⇒ M = 4)."]),
               ("L11 · Reconstruction", ["Ideal: H = T on |ω| < ω_s/2, h = sinc(t/T), x = Σx(nT)sinc((t − nT)/T).",
                                        "ZOH: h₀ = rect[0,T], H₀ = Te^{−jωT/2}sinc(ωT/2π). Linear: h₁ = triangle, H₁ = T sinc²(ωT/2π).",
                                        "Real-time DAC → ZOH."]),
               ("L12 · Practice", ["Time-limited ⇒ not band-limited ⇒ some aliasing always; X[k] = N a_k."])],
              diagrams=[(B[5], 20, "The sampling theorem picture (Lec 5, sl. 20)", CLIP, 12)])
n.save()
save_solved("ashraf_sampling")
print("saved", n.out_path)
