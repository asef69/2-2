"""Anik F4 — Fourier Transform (Lec 7). Lessons 16–19."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402

from c219 import A, anik, exam_map, mark, save_solved, sketch  # noqa: E402

CLIP = (0.0, 0.12, 1.0, 0.98)
n = anik("Lec 7 · Fourier Transform: Pairs, Properties, Filters", "CSE219_Anik_Fourier_Transform_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "Fourier-transform questions and their weight"),
              ("Lesson 16 — From Fourier Series to Fourier Transform", "T → ∞, the transform pair, existence, FT of periodic signals"),
              ("Lesson 17 — Rectangles, Shifts and Modulation", "rect ↔ sinc, time shift, frequency shift, cos-modulation, δ"),
              ("Lesson 18 — Transform Pairs and Properties Toolbox", "e^{−at}u, sign, u, scaling, duality, d/dt, ∫, convolution, Parseval"),
              ("Lesson 19 — LTI Systems in Frequency: Filters, Distortionless, Bandwidth", "H(ω), ideal filters, echo filter, PSD, 3-dB width"),
              ("Quick Notes — Fourier Transform", "merged revision notes + key diagrams")],
    source_note="Slide numbers refer to Lecture-7-Fourier-Transform.pdf (61 slides, “Lec 7”). The deck covers the FS → FT "
                "derivation, the rectangle, time/frequency shifting, modulation and δ(t). Lessons 18–19 add the standard "
                "textbook pairs and properties that the TF papers ask (marked “textbook”). Note: CSE 311 papers use f (Hz) "
                "and Lathi's sinc(x) = sin x / x; EEE and CSE 219 papers use ω.")

n.h1("Exam Map — What the TF Papers Ask")
n.p("The Fourier transform is the heaviest Anik-part topic in CSE 219 (2022-23: Q5(b) 20 + Q6 30 marks; 2023-24: Q1(c) 15 + "
    "Q2 30 marks) and appears in every EEE and CSE 311 paper.")
exam_map(n, "Anik", range(16, 20))
n.callout("focus", "Learn first: (1) the pair table and the properties in Lesson 18 — CSE 219 asks “use the properties, name "
          "them” (sign(t) from e^{−at}u, e^{−a|t|} from e^{−at}u, Parseval integrals) · (2) modulation/frequency shift "
          "(2023-24 Q1(c), EEE spectra-sketch questions every year) · (3) inverse FT of a given spectrum (2022-23 Q5(b)) · "
          "(4) distortionless systems, ideal LPF unrealizable, bandwidth (CSE 311 every year).")

# ========================================================= L16
n.lesson("Lesson 16 — From Fourier Series to Fourier Transform", "Slides 2–18 (Lec 7) · existence and periodic signals: textbook")
n.p("Fourier series need x(t + T) = x(t); real signals are often one-time events (sl. 5). Trick (sl. 6–17): repeat one "
    "pulse with period T, take the FS, let T → ∞.")
n.code(["a_k = (1/T)∫_{−T/2}^{T/2} x(t)e^{−jkω₀t}dt = (1/T)X(jkω₀),   X(jω) ≜ ∫ x(t)e^{−jωt}dt",
        "⇒ T·a_k are samples of a smooth envelope X(jω) at ω = kω₀ (sl. 12)",
        "x̃_T(t) = Σ a_k e^{jkω₀t} = (1/2π) Σ X(jkω₀) e^{jkω₀t} Δω,   Δω = ω₀ = 2π/T",
        "T → ∞: Δω → dω, kω₀ → ω, Σ → ∫  ⇒  x(t) = (1/2π)∫ X(jω)e^{jωt} dω"])
n.formula(["X(jω) = ∫_{−∞}^{∞} x(t)e^{−jωt}dt          x(t) = (1/2π)∫_{−∞}^{∞} X(jω)e^{jωt}dω"])
n.figure_from_pdf(A[7], 12, "Figure 16.1 — Fourier-series stems are samples of the smooth envelope X(jω) (Lec 7, sl. 12)", clip=CLIP, width_cm=10)
n.p("Why raw coefficients shrink (sl. 13–14): a_k = (Δω/2π)X(jkω₀) — each stem is the area of a bin of width Δω, so "
    "X(jω) is a **spectral density**. As T grows the lines crowd together and shorten.")
n.h2("Existence and Periodic Signals (textbook)")
n.bullets(["Dirichlet conditions for the FT: ∫|x|dt < ∞, finitely many extrema and finite jumps in any finite interval. "
           "Sufficient only: cos ω₀t, u(t), δ-trains have transforms containing δ(ω).",
           "Periodic x with FS a_k: X(jω) = 2π Σ a_k δ(ω − kω₀) (each harmonic e^{jkω₀t} ↔ 2πδ(ω − kω₀)).",
           "Impulse train Σδ(t − nT) ↔ (2π/T)Σδ(ω − 2πk/T): a train stays a train."])
n.exam_approach(["Derivation question: write a_k for the periodic extension, identify T·a_k = X(jkω₀), substitute "
                 "1/T = Δω/2π into the synthesis sum, take the limit.", "Periodic signal: find a_k first, then put 2πa_k "
                 "impulses at kω₀.", "State Dirichlet conditions and whether they are necessary."])
nn = np.arange(-5, 6)
ak = 0.25 * (np.exp(-1j * nn * np.pi / 2) + np.exp(-1j * nn * np.pi) - np.exp(-1.5j * nn * np.pi) - 1)
sk6a = sketch("anik4_eee2324_6a", [dict(title="|X(jω)|: impulses of area 2π|a_k| at kπ/2", stems=[(nn * np.pi / 2, 2 * np.pi * np.abs(ak))],
                                        xlabel="ω (rad/s)"),
                                   dict(title="∠X (rad)", stems=[(nn * np.pi / 2, np.where(np.abs(ak) > 1e-9, np.angle(ak), 0))],
                                        xlabel="ω (rad/s)")], ncols=2)
n.practice("Lesson 16", "(a) Actual — EEE 211 2021-22 Q5(a). (b) Actual — EEE 211 2023-24 Q6(a). (c) Actual — CSE 311 2021-22 "
           "Q1(a), 2017-18 Q1(a). (d) Actual — CSE 311 2020-21 Q3(b), 2019-20 Q1(b), 2014-15 Q6(b).",
           ["(a) What happens to x̃(t) = ΣC_n e^{jnω₀t} if the waveform stays the same but T grows? Show that as T → ∞ one "
            "period becomes x(t) = (1/2π)∫X(ω)e^{jωt}dω. (18)",
            "(b) x(t) is periodic with impulses +1 at t = 1, 2 and −1 at t = 3, 4 (period 4). Find its FT; plot amplitude and "
            "phase spectra. (15)",
            "(c) FT of a gate of width B and the exponential FS of the gate repeated with period 2B; relate them. Spectrum of "
            "a pulse vs a pulse train. (20)",
            "(d) Dirichlet conditions — necessary? Represent cos 2πf₀t by an FT. FT of a periodic signal."])
n.solution()
n.answer("(a)", "As T increases the lines kω₀ = 2πk/T crowd together and each C_n = (1/T)X(jnω₀) shrinks, but T·C_n stays on "
         "the envelope X(jω). Derivation in the grey box above: substitute C_n = (Δω/2π)X(jnω₀) and let Δω → 0.")
n.code(["(b) T = 4, ω₀ = π/2. One period: δ(t−1) + δ(t−2) − δ(t−3) − δ(t−4)",
        "    a_k = ¼[e^{−jkπ/2} + e^{−jkπ} − e^{−j3kπ/2} − 1]",
        "    even k: a_k = 0;   odd k: a_k = ½(−j)^k − ½",
        "    a±1 = −½ ∓ j½ (|a| = 0.707, ∠ = ∓135°);   a±3 = −½ ± j½ (∠ = ±135°);  pattern repeats every 4",
        "    X(jω) = 2π Σ_{odd k} a_k δ(ω − kπ/2): impulses of area 2π/√2 = 4.44 at ω = ±π/2, ±3π/2, …"])
n.figure_image(sk6a, "Figure 16.2 — EEE 211 2023-24 Q6(a): amplitude and phase spectra", width_cm=14)
n.answer("(c)", "Gate of width B: X(f) = B·sin(πfB)/(πfB) (continuous). Repeated with period T₀ = 2B: D_n = (1/T₀)X(n/T₀) = "
         "½·sin(nπ/2)/(nπ/2) — lines at n/(2B) Hz whose heights are samples of X(f)/T₀. A single pulse has a continuous "
         "spectrum; the train has a line spectrum under the same sinc envelope. Bandwidth (first null) = 1/B Hz in both.")
n.answer("(d)", "Dirichlet conditions as above — sufficient, not necessary. cos 2πf₀t is not absolutely integrable, yet "
         "cos 2πf₀t ↔ ½[δ(f − f₀) + δ(f + f₀)] (sin ↔ (1/2j)[δ(f − f₀) − δ(f + f₀)]). Periodic signals: X = 2πΣa_kδ(ω − kω₀).")
for k in [("2021-22", "EEE 211", "5(a)"), ("2023-24", "EEE 211", "6(a)"), ("2021-22", "CSE 311", "1(a)"),
          ("2017-18", "CSE 311", "1(a)"), ("2020-21", "CSE 311", "3(b)"), ("2019-20", "CSE 311", "1(b)"),
          ("2014-15", "CSE 311", "6(b)")]:
    mark(*k)

# ========================================================= L17
n.lesson("Lesson 17 — Rectangles, Shifts and Modulation", "Slides 19–44 (Lec 7)")
n.h2("1. Frequency Shift and Modulation (sl. 19–28)")
n.formula(["x(t)e^{jω₀t} ↔ X(j(ω − ω₀))", "x(t)cos ω₀t ↔ ½X(j(ω − ω₀)) + ½X(j(ω + ω₀))"])
n.p("Each component e^{jωt} times e^{jω₀t} becomes e^{j(ω+ω₀)t}: the whole spectrum slides right by ω₀. A cosine is two "
    "rotating exponentials, so it creates two half-height copies at ±ω₀ (damped pendulum, ringing circuits, AM radio).")
n.figure_from_pdf(A[7], 27, "Figure 17.1 — Cosine modulation creates two spectral copies (Lec 7, sl. 27)", clip=CLIP, width_cm=10)
n.h2("2. The Rectangle (sl. 29–38)")
n.formula(["x(t) = 1 for |t| < T/2  ↔  X(jω) = 2 sin(ωT/2)/ω  (= T at ω = 0)"])
n.p("Wider rectangle → narrower main lobe (first zero at 2π/T). Widths 2 and 6: 2sin ω/ω and 2sin 3ω/ω. Shifted rectangle "
    "4 < t < 10 = width-6 rectangle shifted by 7: X = e^{−j7ω}·2 sin 3ω/ω, X(0) = 6.")
n.formula(["Time shift: x(t − t₀) ↔ e^{−jωt₀}X(jω)   (|X| unchanged, phase −ωt₀: linear in ω)"])
n.code(["Lego block (sl. 36–38): height-1 block on (1,4) + height-0.5 block on (2,3), both centred at 2.5",
        "X(jω) = e^{−j2.5ω}[2 sin(1.5ω)/ω + sin(0.5ω)/ω]",
        "Windowed cosine r(t)cos ω₀t (sl. 39–40): ½[R(j(ω − ω₀)) + R(j(ω + ω₀))] — two sincs centred at ±ω₀",
        "Impulse (sl. 41–44): δ(t) ↔ 1 (flat — a spike needs all frequencies);  δ(t − t₀) ↔ e^{−jωt₀}"])
n.figure_from_pdf(A[7], 31, "Figure 17.2 — Wider rectangle, narrower spectrum (Lec 7, sl. 31)", clip=CLIP, width_cm=10)
n.callout("memorize", "Proof of time shift: ∫x(t − t₀)e^{−jωt}dt, put τ = t − t₀ ⇒ e^{−jωt₀}∫x(τ)e^{−jωτ}dτ. Proof of "
          "frequency shift: ∫x e^{jω₀t}e^{−jωt}dt = ∫x e^{−j(ω−ω₀)t}dt = X(j(ω − ω₀)). In Hz: Π(t/τ) ↔ τ sinc(fτ) with "
          "sinc(x) = sin(πx)/(πx); g(t − t₀) ↔ G(f)e^{−j2πft₀}.")
n.exam_approach(["Decompose the signal into rectangles/triangles/known pulses.", "Transform each centred piece, then "
                 "multiply by e^{−jωt_c} for its centre.", "Modulation: write ½ copies at ±ω₀; sketch both copies with "
                 "half height.", "Name every property used."])
n.practice("Lesson 17", "(a) Actual — CSE 219 2023-24 Q1(c). (b) Actual — CSE 311 2019-20 Q2(a), 2012-13 Q6(b). (c) Actual — "
           "EEE 211 2023-24 Q5(a). (d) Actual — EEE 211 2022-23 Q2(b), Q4(a). (e) Actual — EEE 211 2021-22 Q6(a). (f) Practice "
           "set 7.1–7.4; CSE 311 2014-15 Q5(c), 2012-13 Q5(c), 2018-19 Q4(a), 2011-12 Q5(a), 2022-23 Q1(b).",
           ["(a) FT of x₁ = rect(t); then x₂ = rect((t − τ)/T)·cos 2πf₀t by properties. (15)",
            "(b) Show that a time delay causes a linear phase shift. What would happen to a voice signal if this did not hold? (24)",
            "(c) Quadrature multiplexing: u₁ = x₁cos ω_ct, u₂ = x₂ sin ω_ct, r = u₁ + u₂; receiver multiplies by cos ω_ct and "
            "sin ω_ct and filters with H(jω). X₁ = rect of height 1 on |ω| < ω_m, X₂ = triangle peak 1, ω_c = 4ω_m. (i) Design "
            "H so that y₁ = x₁, y₂ = x₂. (ii) Spectra of u₁, u₂, v₁, v₂, y₂. (20)",
            "(d) (i) m(t) (triangle spectrum, height A, edge ω_m) is down-sampled by 2 (x(t) = m(2t)), multiplied by cos ω₀t and "
            "filtered by H_f = B on ω₀ < |ω| < ω₀ + ω_f, with ω_m = ω_f = ω₀/2. Spectra of x, y, z; energy of z. (25) "
            "(ii) AM: x cos ω_ct, receiver oscillator cos(ω_ct − θ), LPF gain 2: output? (15)",
            "(e) x_a: triangles of height 1 centred at ±10 (width ±2). x₁ = x_a cos 10t → h₁ = sin 2t/(πt) → x₂ → × p(t) = "
            "Σδ(t − 2πn/5) → x₃ → h₂ = 2 sin(2t)cos(10t)/(πt) → x₄. Sketch the spectra. (20)",
            "(f) Shifted rect, Lego block, r(t)cos 3t, impulses; sin²(2πf₀t)g(t); Π(t/τ)."])
n.solution()
n.code(["(a) rect(t) ↔ sin(πf)/(πf) = sinc f   (2 sin(ω/2)/ω in ω)",
        "    time scaling: rect(t/T) ↔ T sinc(fT);  time shift by τ: ↔ T sinc(fT)e^{−j2πfτ}",
        "    modulation by cos 2πf₀t:",
        "    X₂(f) = (T/2)[sinc((f − f₀)T)e^{−j2π(f−f₀)τ} + sinc((f + f₀)T)e^{−j2π(f+f₀)τ}]"])
n.answer("(b)", "Proof: as in the MEMORIZE box, x(t − t₀) ↔ X(ω)e^{−jωt₀}: magnitude unchanged, phase −ωt₀ — a straight line "
         "through the origin with slope −t₀. Meaning: every component is delayed by the same t₀ (group delay "
         "−dφ/dω = t₀), so the waveform keeps its shape. A voice signal is a sum of many frequencies; if the phase were not "
         "linear, different frequencies would arrive with different delays (dispersion): syllables smear, transients "
         "spread, speech sounds distorted even though every amplitude is intact.")
n.code(["(c) v₁ = r cos ω_ct = x₁cos²ω_ct + x₂ sin ω_ct cos ω_ct = ½x₁ + ½x₁cos 2ω_ct + ½x₂ sin 2ω_ct",
        "    v₂ = r sin ω_ct = ½x₂ − ½x₂cos 2ω_ct + ½x₁ sin 2ω_ct",
        "(i) H(jω) = 2 for |ω| < ω_f, 0 otherwise, with ω_m ≤ ω_f ≤ 2ω_c − ω_m = 7ω_m (ideal LPF, gain 2)",
        "(ii) |U₁| = ½ rect around ±4ω_m (width ±ω_m); |U₂| = ½ triangles at ±4ω_m;",
        "     |V₁|: ½X₁ at baseband + copies of height ¼ (x₁ and x₂ parts) around ±8ω_m; same for V₂ with x₂ at baseband;",
        "     |Y₂| = triangle of height 1 on |ω| < ω_m  (= X₂)"])
n.code(["(d)(i) X(ω) = ½M(ω/2): triangle of height A/2 reaching ±2ω_m = ±ω₀",
        "       Y(ω) = ½X(ω − ω₀) + ½X(ω + ω₀): triangles of height A/4 centred at ±ω₀ spanning 0…2ω₀",
        "       Z(ω) = B·Y on ω₀ < |ω| < 1.5ω₀: the upper half-triangle from A/4 (at ω₀) down to A/8 (at 1.5ω₀) — an SSB-like signal",
        "       E_z = (1/2π)·2∫_{ω₀}^{1.5ω₀} (AB/4)²(1 − (ω − ω₀)/ω₀)² dω = (A²B²ω₀/16π)(7/24) = 7A²B²ω₀/(384π)",
        "   (ii) x cos ω_ct · cos(ω_ct − θ) = ½x[cos θ + cos(2ω_ct − θ)]; LPF (gain 2) removes the 2ω_c term:",
        "        y(t) = x(t) cos θ   (θ = 90° gives zero output — the quadrature null)"])
n.code(["(e) X₁ = ½X_a(ω − 10) + ½X_a(ω + 10): a triangle of height 1 at 0 (two halves add) + height-½ triangles at ±20",
        "    h₁ = sin 2t/(πt) ↔ ideal LPF, gain 1, |ω| < 2 ⇒ X₂ = triangle of height 1 on |ω| < 2",
        "    p(t): period 2π/5 ⇒ P = 5Σδ(ω − 5k);  X₃ = (1/2π)X₂ * P = (5/2π)Σ X₂(ω − 5k)  (copies every 5, height 0.796,",
        "    no overlap since 5 > 4)",
        "    h₂ = 2 sin 2t cos 10t/(πt) ↔ gain 1 on 8 < |ω| < 12 ⇒ keeps the copies at ±10:",
        "    X₄ = (5/2π)[triangles at ±10] ⇒ x₄(t) = (5/2π)x_a(t) ≈ 0.796 x_a(t)  (the band-pass signal is recovered)"])
n.code(["(f) Practice set: x = 1 on (4,10): e^{−j7ω}2 sin3ω/ω, X(0) = 6;  Lego with heights 3, 4.5:",
        "    e^{−j2.5ω}[6 sin1.5ω/ω + 3 sin0.5ω/ω];  r(t)cos 3t: sin(ω − 3)/(ω − 3) + sin(ω + 3)/(ω + 3);",
        "    3δ(t+2) − 2δ(t−1) ↔ 3e^{j2ω} − 2e^{−jω}, X(0) = 1",
        "    sin²(2πf₀t)g(t) = ½g − ½g cos 4πf₀t ↔ ½G(f) − ¼[G(f − 2f₀) + G(f + 2f₀)]",
        "    Π(t/τ) ↔ τ sinc(πfτ) (Lathi) = τ sin(πfτ)/(πfτ);  Π(t/2B) ↔ 2B sin(2πBf)/(2πBf)"])
for k in [("2023-24", "CSE 219", "1(c)"), ("2019-20", "CSE 311", "2(a)"), ("2012-13", "CSE 311", "6(b)"),
          ("2023-24", "EEE 211", "5(a)"), ("2022-23", "EEE 211", "2(b)"), ("2022-23", "EEE 211", "4(a)"),
          ("2021-22", "EEE 211", "6(a)"), ("2014-15", "CSE 311", "5(c)"), ("2012-13", "CSE 311", "5(c)"),
          ("2018-19", "CSE 311", "4(a)"), ("2011-12", "CSE 311", "5(a)"), ("2022-23", "CSE 311", "1(b)")]:
    mark(*k)
for k in [("2020-21", "EEE 211", "1(b)"), ("2018-19", "EEE 211", "2(c)"), ("2015-16", "EEE 301", "5(b)"),
          ("2014-15", "EEE 301", "5(a)"), ("2014-15", "EEE 301", "6(a)"), ("2013-14", "EEE 301", "7(a)"),
          ("2012-13", "EEE 301", "6(c)")]:
    mark(*k, "◐ Method")

# ========================================================= L18
n.lesson("Lesson 18 — Transform Pairs and Properties Toolbox", "Textbook (Oppenheim & Willsky Tables 4.1–4.2), built on Lec 7")
n.table(["x(t)", "X(jω)", "x(t)", "X(jω)"],
        [["δ(t)", "1", "1", "2πδ(ω)"],
         ["e^{−at}u(t), a > 0", "1/(a + jω)", "e^{at}u(−t)", "1/(a − jω)"],
         ["e^{−a|t|}", "2a/(a² + ω²)", "te^{−at}u(t)", "1/(a + jω)²"],
         ["sgn(t)", "2/(jω)", "u(t)", "πδ(ω) + 1/(jω)"],
         ["rect: 1 for |t| < T/2", "2 sin(ωT/2)/ω", "sin(Wt)/(πt)", "1 for |ω| < W"],
         ["triangle 1 − |t|/τ, |t| < τ", "τ·[sin(ωτ/2)/(ωτ/2)]²", "e^{jω₀t}", "2πδ(ω − ω₀)"],
         ["cos ω₀t", "π[δ(ω − ω₀) + δ(ω + ω₀)]", "sin ω₀t", "(π/j)[δ(ω − ω₀) − δ(ω + ω₀)]"],
         ["Σδ(t − nT)", "(2π/T)Σδ(ω − 2πk/T)", "e^{−at²}", "√(π/a) e^{−ω²/4a}"]],
        widths_cm=[4.3, 4.3, 4.3, 4.3], font_size=8.5)
n.table(["Property", "x(t)", "X(jω)"],
        [["Linearity", "ax + by", "aX + bY"],
         ["Time shift / frequency shift", "x(t − t₀) / x e^{jω₀t}", "e^{−jωt₀}X / X(j(ω − ω₀))"],
         ["Scaling", "x(at)", "(1/|a|)X(jω/a)  (compress in time ⇔ stretch in frequency)"],
         ["Reversal", "x(−t)", "X(−jω)  (= X* for real x)"],
         ["Duality", "X(jt)", "2πx(−ω)"],
         ["Differentiation", "dx/dt", "jωX"],
         ["Frequency differentiation", "−jt x(t)", "dX/dω"],
         ["Integration", "∫_{−∞}^{t}x dτ", "X/(jω) + πX(0)δ(ω)"],
         ["Convolution", "x * h", "XH"],
         ["Multiplication", "x·y", "(1/2π)X * Y"],
         ["Parseval", "∫|x|²dt", "(1/2π)∫|X|²dω  (= ∫|X(f)|²df)"],
         ["Real signal", "x real", "|X| even, ∠X odd; x even ⇒ X real"]],
        widths_cm=[4.2, 4.0, 9.0], font_size=8.5)
n.callout("memorize", "Proofs to know: (i) duality — from x(t) = (1/2π)∫X(jω)e^{jωt}dω, 2πx(−t) = ∫X(jω)e^{−jωt}dω; rename "
          "t ↔ ω: 2πx(−ω) = ∫X(jt)e^{−jωt}dt = F{X(jt)}. (ii) convolution — swap the order of integration and use the "
          "time shift. (iii) Parseval — ∫x x* dt with x* written as the conjugate inverse transform. (iv) scaling — "
          "substitute τ = at (|a| because a < 0 flips the limits). (v) real x: X(−jω) = ∫x e^{jωt} = X*(jω).")
n.exam_approach(["Recognise the signal as a known pair ± shift/scale/modulate/differentiate.",
                 "Write each step with its property name (CSE 219 gives marks for naming).",
                 "For a ratio X(ω) = N/D: partial fractions in jω, invert term by term.",
                 "Parseval integrals: identify ∫|X|² as the energy of a known x(t) and integrate in time instead."])
n.practice("Lesson 18", "(a) Actual — CSE 219 2022-23 Q6. (b) Actual — CSE 219 2023-24 Q2. (c) Actual — CSE 219 2022-23 Q5(b). "
           "(d) Actual — EEE 211 2023-24 Q6(b)–(c), 2022-23 Q2(a), 2021-22 Q5(b), 2020-21 Q1(a), 2019-20 Q6(b).",
           ["(a) f(t) = e^{−at}u(t), a > 0; sign(t) = −1 (t < 0), 1 (t > 0). (a) Define f(−t). (b) FT of f and f(−t). (c) sign(t) in "
            "terms of f(t), f(−t). (d) FT of sign(t) by properties (name them). (30)",
            "(b) x₁ = e^{−at}u(t), x₂ = e^{−a|t|}. (a) FT of x₁, then of x₂ (name the properties). (b) Evaluate "
            "I(a) = ∫ f²/(a² + (2πf)²)² df using Parseval. (30)",
            "(c) X(jω) = 1 for |ω| < 3π; |X₁(jω)| rises linearly from 0 at ω = 0 to 9π at |ω| = 3π (zero outside), ∠X₁ = π/2 "
            "(ω > 0), −π/2 (ω < 0). (i) Define X₁. (ii) x(t). (iii) X₁ via X. (iv) x₁ via x. (v) x₁(t). (20)",
            "(d) FT of sin(at)/(πt) and its energy; FT of u(t) and the integration property; closed-form FT of a ramp-and-hold "
            "pulse (0 → 1 on [0,1], 1 on [1,2]); inverse FT of X = 1 on 3 < |ω| < 7 plus 1 more on 4 < |ω| < 6; X = jω/(ω² − "
            "3jω − 2): FT of x′(t)cos t; duality."])
n.solution()
n.code(["(a)(a) f(−t) = e^{at} for t < 0, 0 for t > 0  (= e^{at}u(−t))",
        "   (b) F{f} = ∫₀^∞ e^{−at}e^{−jωt}dt = 1/(a + jω);   time reversal: F{f(−t)} = F(−jω) = 1/(a − jω)",
        "   (c) sign(t) = lim_{a→0} [f(t) − f(−t)]",
        "   (d) linearity + time reversal: F{f(t) − f(−t)} = 1/(a + jω) − 1/(a − jω) = −2jω/(a² + ω²)",
        "       a → 0: F{sign(t)} = −2jω/ω² = 2/(jω)   (X(0) = 0: sign has zero average)",
        "(b)(a) X₁ = 1/(a + jω); x₂ = x₁(t) + x₁(−t) (linearity + reversal) ⇒ X₂ = 1/(a+jω) + 1/(a−jω) = 2a/(a² + ω²)",
        "   (b) Differentiation: dx₂/dt ↔ jω·2a/(a² + ω²) = j2πf·2a/(a² + (2πf)²)",
        "       |F{dx₂/dt}|² = 16π²a² f²/(a² + (2πf)²)²",
        "       Parseval (in f): ∫|dx₂/dt|²dt = ∫|F|²df.  dx₂/dt = −a sgn(t)e^{−a|t|} ⇒ ∫a²e^{−2a|t|}dt = a",
        "       ⇒ 16π²a²·I(a) = a  ⇒  I(a) = 1/(16π²a)"])
n.code(["(c)(i)  X₁(jω) = 3|ω|e^{jπ sgn ω/2} = 3jω for |ω| < 3π, 0 otherwise",
        "   (ii) x(t) = (1/2π)∫_{−3π}^{3π} e^{jωt}dω = sin(3πt)/(πt)",
        "   (iii) X₁(jω) = 3jω X(jω)",
        "   (iv) differentiation property: x₁(t) = 3 dx/dt",
        "   (v)  x₁(t) = 3 d/dt[sin 3πt/(πt)] = 3(3πt cos 3πt − sin 3πt)/(πt²)"])
n.code(["(d) sin(at)/(πt) ↔ 1 for |ω| < a  (duality of the rectangle);  E = (1/2π)·2a = a/π",
        "    u(t) = ½ + ½sgn(t) ↔ πδ(ω) + 1/(jω);  ∫_{−∞}^{t}x = x * u ↔ X(jω)[πδ(ω) + 1/(jω)] = X/(jω) + πX(0)δ(ω)",
        "    ramp-and-hold: x′ = u(t) − u(t−1) − δ(t−2) ⇒ jωX = (1 − e^{−jω})/(jω) − e^{−j2ω}",
        "        X(ω) = (e^{−jω} − 1)/ω² + j e^{−j2ω}/ω",
        "    band rects: a rect on a < |ω| < b ↔ [sin bt − sin at]/(πt) ⇒ x(t) = [sin 7t − sin 3t + sin 6t − sin 4t]/(πt)",
        "    x′(t)cos t: x′ ↔ G = jωX = −ω²/(ω² − 3jω − 2) ⇒ F{x′cos t} = ½G(ω − 1) + ½G(ω + 1)",
        "    duality: proof in the MEMORIZE box (EEE 2019-20 Q6(b), 20 marks — add the example rect ↔ sinc ⇒ sinc ↔ 2π rect)"])
for k in [("2022-23", "CSE 219", "6(a)–(b)"), ("2022-23", "CSE 219", "6(c)–(d)"), ("2023-24", "CSE 219", "2(a)"),
          ("2023-24", "CSE 219", "2(b)"), ("2022-23", "CSE 219", "5(b)"), ("2023-24", "EEE 211", "6(b)"),
          ("2023-24", "EEE 211", "6(c)"), ("2022-23", "EEE 211", "2(a)"), ("2021-22", "EEE 211", "5(b)"),
          ("2020-21", "EEE 211", "1(a)"), ("2019-20", "EEE 211", "6(b)"), ("2022-23", "CSE 311", "2(a)"),
          ("2012-13", "CSE 311", "5(b)"), ("2011-12", "CSE 311", "6(a)"), ("2016-17", "CSE 311", "1(b)"),
          ("2016-17", "CSE 311", "1(e)"), ("2014-15", "CSE 311", "5(b)"), ("2014-15", "CSE 311", "5(d)"),
          ("2016-17", "EEE 211", "6(b)"), ("2016-17", "EEE 211", "6(a)"), ("2018-19", "EEE 211", "2(a)"),
          ("2017-18", "EEE 211", "2(a)"), ("2015-16", "EEE 301", "5(a)"), ("2012-13", "EEE 301", "5(a)"),
          ("2013-14", "EEE 301", "7(b)"), ("2011-12", "EEE 301", "4(b)"), ("2010-11", "EEE 301", "2(a)"),
          ("2012-13", "EEE 301", "5(c)"), ("2014-15", "EEE 301", "5(b)")]:
    mark(*k)
for k in [("2017-18", "CSE 311", "1(b)"), ("2016-17", "CSE 311", "1(c)"), ("2011-12", "CSE 311", "5(b)"),
          ("2010-11", "CSE 311", "5(b)"), ("2010-11", "CSE 311", "6(b)"), ("2015-16", "EEE 301", "5(c)"),
          ("2012-13", "EEE 301", "5(b)")]:
    mark(*k, "◐ Method")
n.code(["Older quick answers: −90° phase shifter H = −j sgn ω ⇒ h = 1/(πt), cos ω₀t → sin ω₀t;",
        "  sin t·sin(t/2)/(πt²) = π·[sin t/(πt)]·[sin(t/2)/(πt)] ↔ ½·(rect|ω|<1 * rect|ω|<½): |X| = ½ for |ω| < ½,",
        "  falling linearly to 0 at |ω| = 3/2;  α rect(αt/τ) ↔ τ·sin(ωτ/2α)/(ωτ/2α): α → ∞ gives τ (flat; τδ(t)),",
        "  α → 0 shrinks the spectrum onto ω = 0;  energy of sin(20π(t − 1/40))/(π(t − 1/40))·cos 30πt = 10",
        "  (rect of height 1 on |ω| < 20π, shifted to ±30π with height ½: (1/2π)·2·¼·40π)"])

# ========================================================= L19
n.lesson("Lesson 19 — LTI Systems in Frequency: Filters, Distortionless, Bandwidth",
         "Slides 45–59 (Lec 7: applications) · frequency response, filters, distortionless, PSD: textbook")
n.p("Applications on the slides: audio and image denoising (remove noise frequencies), JPEG (drop small high-frequency "
    "coefficients), MRI (data measured in k-space = frequency domain), music fingerprinting (peak patterns in a "
    "spectrogram), vibration diagnosis (faults change the spectrum), ECG (notch out 50 Hz mains hum).")
n.formula(["y = x * h  ⇔  Y(jω) = H(jω)X(jω)          e^{jωt} → H(jω)e^{jωt}"])
n.h2("Distortionless Transmission (textbook)")
n.p("Distortionless: y(t) = K x(t − t_d) ⇒ H(jω) = K e^{−jωt_d}: |H| = K constant and phase −ωt_d linear through the "
    "origin (constant group delay t_d). An **all-pass** system has |H| constant but its phase need not be linear, so it "
    "is distortionless only if its phase is linear — otherwise it causes phase (delay) distortion.")
n.p("RC low-pass H = 1/(1 + jωRC): for ωRC ≪ 1, |H| ≈ 1 and ∠H ≈ −ωRC — approximately distortionless (delay RC) for "
    "signals whose bandwidth B ≪ 1/(2πRC).")
n.h2("Ideal Filters (textbook)")
n.code(["Ideal LPF H = 1 (|ω| < ω_c), linear phase e^{−jωt_d}:  h(t) = sin(ω_c(t − t_d))/(π(t − t_d))",
        "  h ≠ 0 for t < 0 for every finite t_d ⇒ non-causal ⇒ physically unrealizable (Paley–Wiener: |H| cannot be",
        "  zero over a band). Practical filters approximate it with a large delay and a truncated sinc.",
        "Ideal band-stop (stop 10 < |ω| < 20): h = δ(t) − [sin 20t − sin 10t]/(πt)",
        "Echo filter H = (1 + k cos 2πfT)e^{−j2πft_d} = e^{−j2πft_d}[1 + (k/2)(e^{j2πfT} + e^{−j2πfT})]",
        "  ⇒ y = g(t − t_d) + (k/2)[g(t − t_d + T) + g(t − t_d − T)]  (a band-limited input inside |f| < B)"])
n.h2("Bandwidth, Duration, PSD (textbook)")
n.bullets(["Bandwidth = range of frequencies holding (most of) the energy: first-null, 3-dB (|X|² falls to half) or "
           "essential bandwidth. δ(t) has infinite bandwidth (flat spectrum).",
           "Scaling: x(at), a > 1, is shorter ⇒ wider spectrum (time–bandwidth product constant). A derivative boosts high "
           "frequencies (|jωX|) ⇒ larger bandwidth. Smoother signals (rect → triangle) have narrower bandwidth.",
           "PSD of a power signal: S(ω) = lim |X_T(ω)|²/T; P = (1/2π)∫S dω. Periodic x: S = 2πΣ|a_k|²δ(ω − kω₀).",
           "Empirical H: drive with sinusoids e^{jωt} (or an impulse/white noise), measure output amplitude ratio and phase "
           "shift at each ω."])
n.practice("Lesson 19", "(a) Actual — CSE 311 2022-23 Q2(b), 2021-22 Q2(a), 2020-21 Q4(a), 2018-19 Q1(b), 2012-13 Q7(a). "
           "(b) Actual — CSE 311 2016-17 Q1(d), 2017-18 Q1(c), 2010-11 Q6(a). (c) Actual — EEE 211 2020-21 Q2(c). (d) Actual — "
           "EEE 211 2021-22 Q6(b), 2020-21 Q2(a)–(b), 2019-20 Q6(a); CSE 311 2021-22 Q3(a), 6(a). (e) Older: echo filter, "
           "bandwidth questions, RC, band-stop, e^{−αt}u through sin2t/(πt).",
           ["(a) Characterize a distortionless system; is an all-pass system distortionless? Physical interpretation.",
            "(b) Ideal LPF: transfer function → impulse response; prove it is unrealizable.",
            "(c) Causal y″ + 6y′ + 8y = 2x: H(ω); response to x = te^{−2t}u(t). (20)",
            "(d) h = e^{2t}u(−t): 3-dB bandwidth, 1/e duration, product; PSD of Σδ(t − nT); 3-dB bandwidth of e^{−3t}u(t); "
            "1/e durations of Ae^{−t/T}u(t), x₁(3t), x₁(t/2); time compression ↔ frequency expansion.",
            "(e) Older (see solutions)."])
n.solution()
n.answer("(a)", "y = Kx(t − t_d) for every input ⇒ Y = Ke^{−jωt_d}X ⇒ H = Ke^{−jωt_d}: constant gain (no amplitude "
         "distortion) and phase linear in ω through the origin (every component delayed by the same t_d, no phase "
         "distortion). An all-pass filter only guarantees constant |H|; e.g. H = (a − jω)/(a + jω) has phase "
         "−2tan⁻¹(ω/a), not linear ⇒ frequencies are delayed differently ⇒ **not distortionless** (unless the phase is "
         "linear over the signal band, where it then behaves as a pure delay).")
n.answer("(b)", "H = e^{−jωt_d} for |ω| < ω_c ⇒ h(t) = (1/2π)∫_{−ω_c}^{ω_c}e^{jω(t−t_d)}dω = sin ω_c(t − t_d)/(π(t − t_d)). The sinc "
         "extends to t → −∞, so h(t) ≠ 0 for t < 0: the filter responds before the impulse arrives ⇒ non-causal ⇒ not "
         "realizable. A pulse input gives an output with ripples (Gibbs) and a non-zero response before the pulse.")
n.code(["(c) H(ω) = 2/((jω)² + 6jω + 8) = 2/((jω + 2)(jω + 4));  X = 1/(jω + 2)²",
        "    Y = 2/((jω + 2)³(jω + 4)) = −¼/(jω+4) + ¼/(jω+2) − ½/(jω+2)² + 1/(jω+2)³",
        "    y(t) = [−¼e^{−4t} + ¼e^{−2t} − ½te^{−2t} + ½t²e^{−2t}] u(t)",
        "(d) H = 1/(2 − jω): |H|² = 1/(4 + ω²) halves at ω = 2 ⇒ 3-dB bandwidth 2 rad/s; h(0) = 1 falls to 1/e at",
        "    t = −½ ⇒ duration ½; product = 1 (fixed for this shape: the time–bandwidth relation)",
        "    PSD of Σδ(t − nT): S(ω) = (2π/T²)Σδ(ω − 2πk/T)  (power 1/T² in each line)",
        "    e^{−3t}u: |X|² = 1/(9 + ω²) ⇒ 3 rad/s (0.477 Hz);  durations: T, T/3, 2T (compress ×3 ⇒ duration ÷3,",
        "    bandwidth ×3);  g(at) ↔ (1/|a|)G(f/a): compression in time = expansion in frequency"])
n.code(["(e) x = e^{−αt}u through sin 2t/(πt) (ideal LPF |ω| < 2): Y = 1/(α + jω), |ω| < 2;",
        "    E_y = (1/π)(1/α)tan⁻¹(2/α); half of E_x = 1/(2α) ⇒ tan⁻¹(2/α) = π/4 ⇒ α = 2",
        "    x = [(1/12)e^{−t/4} + (1/6)e^{−t/2}]u, h = e^{−t/3}u ⇒ y = (e^{−t/4} − e^{−t/2})u(t)",
        "    RC, x = Vu: y = V(1 − e^{−t/RC})u(t);  band-stop: h = δ(t) − [sin20t − sin10t]/(πt)",
        "    bandwidth of δ: ∞;  f vs f′: f′ has larger bandwidth (|ωF| grows);  g vs g(at), a > 1: g(at) wider"])
for k in [("2022-23", "CSE 311", "2(b)"), ("2021-22", "CSE 311", "2(a)"), ("2020-21", "CSE 311", "4(a)"),
          ("2018-19", "CSE 311", "1(b)"), ("2012-13", "CSE 311", "7(a)"), ("2016-17", "CSE 311", "1(d)"),
          ("2017-18", "CSE 311", "1(c)"), ("2010-11", "CSE 311", "6(a)"), ("2020-21", "EEE 211", "2(c)"),
          ("2018-19", "EEE 211", "4(a)"), ("2015-16", "EEE 301", "6(c)"), ("2021-22", "EEE 211", "6(b)"),
          ("2020-21", "EEE 211", "2(a)"), ("2020-21", "EEE 211", "2(b)"), ("2019-20", "EEE 211", "6(a)"),
          ("2021-22", "CSE 311", "3(a)"), ("2021-22", "CSE 311", "6(a)"), ("2018-19", "EEE 211", "2(b)"),
          ("2014-15", "EEE 301", "5(c)"), ("2013-14", "EEE 301", "7(c)"), ("2017-18", "EEE 211", "2(b)"),
          ("2016-17", "EEE 211", "8(a)"), ("2014-15", "CSE 311", "1(c) [L-3]"), ("2012-13", "CSE 311", "7(c)"),
          ("2014-15", "CSE 311", "1(a) [L-3]"), ("2016-17", "CSE 311", "1(a)"), ("2013-14", "CSE 311", "1(b)"),
          ("2011-12", "CSE 311", "5(c)"), ("2010-11", "CSE 311", "5(a)"), ("2014-15", "CSE 311", "6(a)"),
          ("2013-14", "CSE 311", "1(c)(i)"), ("2017-18", "EEE 211", "1(b)"), ("2016-17", "EEE 211", "3(b)"),
          ("2012-13", "EEE 301", "6(a)"), ("2011-12", "EEE 301", "2(a)")]:
    mark(*k)
for k in [("2013-14", "CSE 311", "1(c)(ii)"), ("2011-12", "CSE 311", "6(b)"), ("2014-15", "CSE 311", "7(b)")]:
    mark(*k, "◐ Method")

n.quick_notes("Quick Notes — Fourier Transform", "Revision points for Lessons 16–19.",
              [("L16 · FS → FT", ["T·a_k = X(jkω₀); X = ∫x e^{−jωt}; x = (1/2π)∫X e^{jωt}.",
                                 "Periodic: X = 2πΣa_kδ(ω − kω₀). Dirichlet sufficient, not necessary."]),
               ("L17 · Shifts", ["x(t − t₀) ↔ e^{−jωt₀}X; x e^{jω₀t} ↔ X(ω − ω₀); x cos ω₀t ↔ ½[X(ω − ω₀) + X(ω + ω₀)].",
                                "rect width T ↔ 2sin(ωT/2)/ω; δ ↔ 1; (4,10) rect ↔ e^{−j7ω}2 sin3ω/ω."]),
               ("L18 · Toolbox", ["e^{−at}u ↔ 1/(a + jω); e^{−a|t|} ↔ 2a/(a² + ω²); sgn ↔ 2/(jω); u ↔ πδ + 1/(jω).",
                                 "Duality X(jt) ↔ 2πx(−ω); d/dt ↔ jω; ∫ ↔ X/(jω) + πX(0)δ; Parseval E = (1/2π)∫|X|².",
                                 "CSE 219 2023-24 Q2(b): I(a) = 1/(16π²a)."]),
               ("L19 · Filters", ["Distortionless H = Ke^{−jωt_d}; all-pass ≠ distortionless unless phase linear.",
                                 "Ideal LPF h = sin ω_c(t − t_d)/(π(t − t_d)) — non-causal.",
                                 "3-dB bandwidth of e^{−at}u: a rad/s. Compress in time ⇔ expand in frequency."])],
              diagrams=[(A[7], 30, "Fourier transform of the rectangle (Lec 7, sl. 30)", CLIP, 10),
                        (A[7], 43, "δ(t) ↔ 1 (Lec 7, sl. 43)", CLIP, 10)])
n.save()
save_solved("anik_fourier_transform")
print("saved", n.out_path)
