"""Anik F3 — Fourier Series (Lec 5–6). Lessons 11–15."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402

from c219 import A, anik, exam_map, mark, save_solved, sketch  # noqa: E402

CLIP = (0.0, 0.12, 1.0, 0.98)
n = anik("Lec 5–6 · Fourier Series and Its Properties", "CSE219_Anik_Fourier_Series_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "Fourier-series questions and their weight"),
              ("Lesson 11 — The Idea of Fourier Series; Orthogonality and Convergence", "harmonics, the coefficient formula, orthogonal sets, Dirichlet"),
              ("Lesson 12 — Computing Coefficients", "by inspection, by integration; square wave, ramp; trigonometric form"),
              ("Lesson 13 — Linearity, Shift, Reversal, Scaling and Symmetry", "coefficient rules; real/even/odd/half-wave"),
              ("Lesson 14 — Differentiation, Impulses, Impulse Trains, Integration", "jkω₀ rule, impulse train a_k = 1/T, sawtooth"),
              ("Lesson 15 — Multiplication, Parseval, and Periodic Inputs to LTI Systems", "coefficient convolution; y_k = H(jkω₀)a_k"),
              ("Quick Notes — Fourier Series", "merged revision notes + key diagrams")],
    source_note="Slide numbers refer to Lecture-5-Fourier-Series-Let's-Look-Inside.pdf (53 slides, “Lec 5”) and "
                "Lecture-6-Properties-of-Fourier-Series.pdf (82 slides, “Lec 6”). Orthogonal function sets, Dirichlet "
                "conditions, half-wave symmetry, Parseval's relation and the response of an LTI system to a periodic input "
                "are textbook background (marked); the EEE and CSE 311 papers ask them often.")

n.h1("Exam Map — What the TF Papers Ask")
n.p("Fourier series appear in every paper: a full 30-mark question in CSE 219 2023-24 (Q4) and two to three parts in "
    "every EEE paper.")
exam_map(n, "Anik", range(11, 16))
n.callout("focus", "Most asked: (1) coefficients by inspection from a sum of sinusoids (EEE every year, 10–17 marks) · "
          "(2) coefficients of a standard periodic waveform (square, triangle, rectified sine, impulse train) · "
          "(3) use properties instead of integrating — shift, derivative (CSE 219 2023-24 Q4, EEE 2020-21 Q7(a)) · "
          "(4) periodic input through an LTI filter: y_k = H(jkω₀)a_k (EEE 2023-24 Q7(b), 2019-20 Q5(b)) · "
          "(5) even → real, odd → imaginary coefficients (CSE 311 three times).")

# =============================================================== L11
n.lesson("Lesson 11 — The Idea of Fourier Series; Orthogonality and Convergence",
         "Slides 2–23, 44–52 (Lec 5) · orthogonal sets and Dirichlet conditions: textbook")
n.h2("1. Periodic Signals as Sums of Harmonics (sl. 2–17)")
n.p("Any periodic signal can be split into simple waves; each simple wave is easy to handle (a vibrating string, heat "
    "diffusion), and the answers are added back. A signal of period T contains only frequencies kω₀, ω₀ = 2π/T "
    "(bells ringing every 2, 3, 5 min repeat every lcm = 30 min, sl. 10–11).")
n.formula(["x(t) = Σ_{k=−∞}^{∞} a_k e^{jkω₀t}          ω₀ = 2π/T"])
n.h2("2. Finding a_k: Stop the Rotation and Average (sl. 18–22)")
n.p("The average of e^{jkω₀t} over one period is 1 for k = 0 and 0 otherwise. Multiply x(t) by e^{−jkω₀t}: the k-th term "
    "stops rotating, every other term still rotates and averages to zero.")
n.formula(["a_k = (1/T) ∫_T x(t) e^{−jkω₀t} dt          a₀ = average value of x"])
n.h2("3. Coordinates and Projections (sl. 44–52)")
n.p("Functions have coordinates just like vectors: 3 + 2t ↔ (3, 2) in the basis {1, t}; eᵗ ↔ (1, 1, 1/2!, …) in "
    "{1, t, t², …}. Fourier series uses the basis {e^{jkω₀t}}, and the coordinate is a projection with the inner product "
    "⟨x, z⟩ = (1/T)∫_T x z* dt. With z = e^{jkω₀t} this is exactly a_k.")
n.h2("4. Orthogonal and Orthonormal Sets (textbook)")
n.bullets(["φᵢ, φⱼ are orthogonal on (t₁, t₂) if ∫ φᵢ φⱼ* dt = 0 (i ≠ j); orthonormal if also ∫|φᵢ|² dt = 1.",
           "Normalize: divide φᵢ by √Eᵢ, Eᵢ = ∫|φᵢ|².",
           "Expansion: x ≈ Σ cᵢ φᵢ with cᵢ = ∫ x φᵢ* dt / Eᵢ (best least-squares coefficients).",
           "Parseval for the set: ∫|x|² dt = Σ |cᵢ|² Eᵢ when the set is complete for x."])
n.h2("5. Dirichlet Conditions (textbook)")
n.p("A periodic x(t) has a Fourier series that converges to x(t) at every point of continuity (and to the midpoint of "
    "each jump) if, over one period: (1) it is absolutely integrable, ∫_T|x|dt < ∞; (2) it has a finite number of "
    "maxima and minima; (3) it has a finite number of finite discontinuities. They are **sufficient, not necessary**: "
    "signals that violate them may still have useful series/transforms (e.g. impulse trains, u(t), sinusoids for the FT). "
    "Near a jump the partial sums overshoot by about 9% (Gibbs).")
n.callout("trap", "• tan(2πt) violates condition 1 (infinite jumps, not integrable); sin(2π/t) has infinitely many "
          "oscillations near t = 0 (and is not even periodic). • Orthogonality must be checked on the stated interval "
          "only.")
n.exam_approach(["Orthogonality: compute every pairwise integral over the interval (disjoint supports give 0 at once).",
                 "Normalize with A = 1/√(energy).", "Expansion: cᵢ = ⟨x, φᵢ⟩/Eᵢ, then check a value or Parseval.",
                 "Dirichlet: test each of the three conditions for one period and state which fails."])
n.practice("Lesson 11", "(a) Actual — EEE 211 2023-24 Q7(a). (b) Actual — EEE 211 2018-19 Q1(a). (c) Actual — EEE 301 2012-13 "
           "Q4(a). (d) Actual — EEE 301 2013-14 Q3(a), CSE 311 2020-21 Q3(b).",
           ["(a) φ₁ = −A on (−1, 0), A on (0, 1); φ₂ = A on (−1, 1); φ₃ = 1 on (1, 2). Show they are pairwise orthogonal on "
            "(−1, 2) and find A for orthonormality. (10)",
            "(b) State the condition for orthogonality. Are e^{j2t} and e^{j4t} orthogonal on [0, π]? (10)",
            "(c) φ₁ = 1 (0 ≤ t ≤ 2), φ₂ = 1 (0..1), −1 (1..2), φ₃ = 1 (2..3). Express x(t) = 2 (0..1), −1 (1..2), 1 (2..3).",
            "(d) Do tan(2πt) and sin(2π/t) have convergent Fourier series? State the Dirichlet conditions; are they "
            "necessary?"])
n.solution()
n.answer("(a)", "∫φ₁φ₂ = A²[∫_{−1}^{0}(−1)dt + ∫_0^1 1 dt] = 0; φ₃ is zero wherever φ₁, φ₂ are nonzero ⇒ ∫φ₁φ₃ = ∫φ₂φ₃ = 0. "
         "Energies: ∫φ₁² = ∫φ₂² = 2A², ∫φ₃² = 1. Orthonormal ⇒ 2A² = 1 ⇒ **A = 1/√2** (φ₃ already has unit energy).")
n.answer("(b)", "∫₀^π e^{j2t}(e^{j4t})* dt = ∫₀^π e^{−j2t}dt = (1 − e^{−j2π})/(2j) = 0 ⇒ **orthogonal**. (Each has energy π, "
         "so √(1/π)e^{j2t}, √(1/π)e^{j4t} are orthonormal.)")
n.answer("(c)", "E₁ = 2, E₂ = 2, E₃ = 1. c₁ = (2 − 1)/2 = ½; c₂ = (2·1 + (−1)(−1))/2 = 3/2; c₃ = 1. x = ½φ₁ + (3/2)φ₂ + φ₃ "
         "(check (1,2): ½ − 3/2 = −1 ✓).")
n.answer("(d)", "tan(2πt): period ½ but |x| → ∞ at t = ¼ + k/2 — not absolutely integrable ⇒ no convergent FS. sin(2π/t): "
         "not periodic, and has infinitely many maxima/minima near t = 0 ⇒ fails condition 2. Dirichlet conditions as "
         "in §5; sufficient but not necessary (cos ω₀t, impulse trains have series/transforms in the generalized sense).")
mark("2023-24", "EEE 211", "7(a)"); mark("2018-19", "EEE 211", "1(a)"); mark("2012-13", "EEE 301", "4(a)")
mark("2013-14", "EEE 301", "3(a)"); mark("2020-21", "CSE 311", "3(b)"); mark("2016-17", "EEE 211", "2(a)")
for k in [("2021-22", "EEE 211", "3(b)"), ("2017-18", "EEE 211", "1(a)"), ("2016-17", "EEE 211", "3(a)")]:
    mark(*k, "◐ Method")

# =============================================================== L12
n.lesson("Lesson 12 — Computing Coefficients", "Slides 24–43 (Lec 5) · trigonometric form: textbook")
n.h2("1. By Inspection (sl. 25–29)")
n.p("If x is already a sum of sinusoids, use Euler: cos θ = (e^{jθ} + e^{−jθ})/2, sin θ = (e^{jθ} − e^{−jθ})/2j.")
n.code(["x = 1 + sin ω₀t + 2cos ω₀t + cos(2ω₀t + π/4)",
        "a₀ = 1;  a₁ = 1 + 1/(2j) = 1 − j/2;  a₋₁ = 1 + j/2;  a₂ = ½e^{jπ/4} = (√2/4)(1 + j);  a₋₂ = (√2/4)(1 − j)",
        "|a₁| = √5/2, ∠a₁ = −tan⁻¹(½);  |a₂| = ½, ∠a₂ = π/4"])
n.h2("2. Square Wave (sl. 30–34)")
n.p("x = 1 for |t| < T₁, 0 for T₁ < |t| < T/2:")
n.formula(["a₀ = 2T₁/T          a_k = sin(kω₀T₁)/(kπ)   (k ≠ 0)"])
n.p("T₁ = T/4: a₀ = ½, a_k = sin(kπ/2)/(kπ): a_{±1} = 1/π, a_{±3} = −1/(3π), even k = 0.")
n.figure_from_pdf(A[5], 34, "Figure 12.1 — Coefficients of the square wave with T₁ = T/4 (Lec 5, sl. 34)", clip=CLIP, width_cm=10)
n.h2("3. Triangular Ramp, T = 3 (sl. 35–41)")
n.p("x = t (0 ≤ t < 1), (3 − t)/2 (1 ≤ t < 3). a₀ = area/period = (½·3·1)/3 = ½ (geometry, sl. 37). For k ≠ 0 the "
    "integrals give (e^{−jkω₀} − 1)/(2k²ω₀²).")
n.callout("trap", "Slide 39 has a sign slip in the second integral, so slides 40–41 print a_k = (e^{−jkω₀} − 1)/(6k²ω₀²). "
          "The correct value is (e^{−jkω₀} − 1)/(**2**k²ω₀²), ω₀ = 2π/3 (checked numerically; quickest derivation: x″ has "
          "impulses +3/2 at t = 0 and −3/2 at t = 1 per period, so (jkω₀)²a_k = (1/3)(3/2)(1 − e^{−jkω₀})).")
n.h2("4. Trigonometric Forms (textbook)")
n.code(["x(t) = a₀ + Σ_{n≥1} [aₙ cos nω₀t + bₙ sin nω₀t]       aₙ = (2/T)∫x cos nω₀t dt,  bₙ = (2/T)∫x sin nω₀t dt",
        "     = C₀ + Σ Cₙ cos(nω₀t + θₙ)   (compact)          Cₙ = √(aₙ² + bₙ²),  θₙ = −tan⁻¹(bₙ/aₙ)",
        "Exponential ↔ trig:  c₀ = a₀;  cₙ = (aₙ − jbₙ)/2;  c₋ₙ = cₙ*;  Cₙ = 2|cₙ|"])
n.exam_approach(["Sum of sinusoids → inspection; rewrite sines as cosines with phase, collect same frequencies.",
                 "Standard waveform → integrate over the most convenient period; k = 0 separately.",
                 "Piecewise-linear waveform → differentiate twice to get impulses (Lesson 14), then divide by (jkω₀)².",
                 "Spectra: plot |a_k| (even) and ∠a_k (odd) against k or kω₀."])
n.practice("Lesson 12", "(a) Actual — EEE 211 2022-23 Q5(a). (b) Actual — EEE 211 2018-19 Q1(b). (c) Actual — CSE 311 2019-20 "
           "Q1(a), 2020-21 Q2(b). (d) Actual — EEE 211 2019-20 Q8(b). (e) Older: EEE 211 2017-18 Q4(a), EEE 301 2013-14 Q3(b), "
           "2010-11 Q1(a).",
           ["(a) Compact trigonometric FS and amplitude spectrum of x = 2 + 3cos2t + 4sin2t + 2sin(3t + 30°) − cos(7t + 150°). (10)",
            "(b) Exponential FS and magnitude/phase spectra of x = 2 + ½cos(t + 45°) + 2cos3t − sin(4t + 30°). (10)",
            "(c) Exponential FS coefficients of cos 2πf₀t and sin 2πf₀t: real or imaginary? Must we integrate over a full "
            "cycle? (17)",
            "(d) Triangular wave, period 2: x(0) = −A, x(±1) = A, linear in between (zero crossings at ±½). a₀, aₙ, bₙ. (20)",
            "(e) (i) 3 + cos(4t + π/4) + sin(10t + π/3) (trig coefficients); (ii) triangle wave rising from 0 at t = 0 to 2 "
            "at t = π/2 and back to 0 at t = π, period π; (iii) square wave K of width τ, period T: Cₙ and the effect of T."])
n.solution()
n.code(["(a) ω₀ = 1.  3cos2t + 4sin2t = 5cos(2t − 53.13°);  2sin(3t + 30°) = 2cos(3t − 60°);",
        "    −cos(7t + 150°) = cos(7t − 30°)",
        "    x = 2 + 5cos(2t − 53.13°) + 2cos(3t − 60°) + cos(7t − 30°)",
        "    amplitude spectrum: C₀ = 2, C₂ = 5, C₃ = 2, C₇ = 1 (all others 0)",
        "(b) ω₀ = 1.  c₀ = 2;  c±₁ = ¼e^{±j45°};  c±₃ = 1;  −sin(4t + 30°) = cos(4t + 120°) ⇒ c±₄ = ½e^{±j120°}",
        "    |c|: 2 (k=0), ¼ (±1), 1 (±3), ½ (±4);   ∠c: ±45° (k = ±1), 0 (±3), ±120° (±4)"])
n.answer("(c)", "cos 2πf₀t = ½e^{j2πf₀t} + ½e^{−j2πf₀t} ⇒ a±₁ = ½ (**real**). sin 2πf₀t = (1/2j)e^{j2πf₀t} − (1/2j)e^{−j2πf₀t} ⇒ "
         "a±₁ = ∓j/2 (**purely imaginary**). Both satisfy Dirichlet (bounded, smooth, one max/min per period). In general "
         "a_k needs a full period; for even signals a_k = (2/T)∫₀^{T/2}x cos kω₀t dt and for odd signals a_k = "
         "(−2j/T)∫₀^{T/2}x sin kω₀t dt — half a cycle suffices (Lesson 13).")
n.answer("(d)", "x(t) = A(2|t| − 1), |t| ≤ 1, period 2 (ω₀ = π). Even ⇒ bₙ = 0. a₀ = average = 0 (equal areas above and below).")
n.code(["aₙ = (2/2)∫_{−1}^{1} A(2|t| − 1)cos nπt dt = 2A∫₀¹(2t − 1)cos nπt dt = 4A[(−1)ⁿ − 1]/(n²π²)",
        "   = −8A/(n²π²) for odd n,  0 for even n",
        "x(t) = −(8A/π²)[cos πt + (1/9)cos 3πt + (1/25)cos 5πt + …]"])
n.code(["(e)(i)  ω₀ = 2: a₀ = 3;  a₂ = cos π/4 = 0.707, b₂ = −sin π/4 = −0.707;",
        "        sin(10t + π/3) = (√3/2)cos10t + ½ sin10t ⇒ a₅ = 0.866, b₅ = 0.5",
        "(ii)    ω₀ = 2, even about π/2: c₀ = 1;  c_k = −4/(π²k²) for odd k, 0 for even k ≠ 0",
        "        x = 1 − (8/π²)Σ_{odd} cos(2kt)/k²",
        "(iii)   Cₙ = (Kτ/T)·sin(nπτ/T)/(nπτ/T); τ = 1: T = 5, 10, 15 ⇒ line spacing 2π/T shrinks and every line",
        "        shrinks (∝ 1/T) while the sinc envelope (zeros at multiples of 2π/τ) stays fixed"])
for k in [("2022-23", "EEE 211", "5(a)"), ("2018-19", "EEE 211", "1(b)"), ("2019-20", "CSE 311", "1(a)"),
          ("2020-21", "CSE 311", "2(b)"), ("2019-20", "EEE 211", "8(b)"), ("2017-18", "EEE 211", "4(a)"),
          ("2013-14", "EEE 301", "3(b)"), ("2010-11", "EEE 301", "1(a)")]:
    mark(*k)
mark("2022-23", "EEE 211", "7(a)", "◐ Method")

# =============================================================== L13
n.lesson("Lesson 13 — Linearity, Shift, Reversal, Scaling and Symmetry",
         "Slides 2–35 (Lec 6) · symmetry rules: textbook")
n.table(["Property", "Signal (same T)", "Coefficients"],
        [["Linearity (sl. 5–8)", "αx + βy", "αa_k + βb_k"],
         ["Time shift (sl. 9–17)", "x(t − t₀)", "a_k e^{−jkω₀t₀}  (magnitude unchanged)"],
         ["Reversal (sl. 18–23)", "x(−t)", "a₋ₖ"],
         ["Scaling (sl. 27–33)", "x(αt), α > 0", "a_k, but ω₀ → αω₀ (period T/α)"],
         ["Conjugation", "x*(t)", "a*₋ₖ"]],
        widths_cm=[4.2, 4.2, 8.8])
n.p("Worked (sl. 24–26, 34–35): x(4 − t) + y(t − 3) ↔ a₋ₖe^{−j4kω₀} + b_k e^{−j3kω₀}; x(4 − 3t) ↔ a₋ₖe^{−j4kω₀} with "
    "ω₀′ = 3ω₀ (shift, then reverse, then scale — the coefficient does not change in the last step).")
n.callout("trap", "Slide 26 writes y(t − 3) ↔ a_k e^{−j3kω₀}; it must be **b_k** e^{−j3kω₀} (y has coefficients b_k), as "
          "the boxed final answer shows.")
n.h2("Symmetry Rules (textbook)")
n.table(["Signal", "Coefficients"],
        [["real", "a₋ₖ = a_k*  (|a_k| even, ∠a_k odd)"],
         ["real and even", "a_k real and even (cosine terms only)"],
         ["real and odd", "a_k purely imaginary and odd, a₀ = 0 (sine terms only)"],
         ["half-wave symmetric: x(t + T/2) = −x(t)", "a_k = 0 for every even k (odd harmonics only)"]],
        widths_cm=[7.0, 10.2])
n.p("Proof of even → real: a_k = (1/T)∫_{−T/2}^{T/2} x(t)[cos kω₀t − j sin kω₀t]dt; x·sin is odd, so its integral vanishes "
    "and a_k = (2/T)∫₀^{T/2} x cos kω₀t dt is real. For odd x the cosine part vanishes: a_k = −(2j/T)∫₀^{T/2} x sin kω₀t dt, "
    "imaginary. Both need only half a cycle.")
n.exam_approach(["Write the new signal as a chain of operations on the known one.", "Apply the rules in the same order "
                 "(shift → reverse → scale), updating ω₀ after scaling.", "Use symmetry to predict which coefficients "
                 "vanish and whether they are real/imaginary — a free check."])
yt = np.arange(-5, 6)
mag = np.where(yt % 2 != 0, 2 / (np.pi * np.abs(np.where(yt == 0, 1, yt))), 0)
ph = np.where(yt % 2 != 0, np.angle(2 / (1j * np.pi * np.where(yt == 0, 1, yt)) * np.exp(-1j * yt * np.pi / 3)), 0)
sk4 = sketch("anik3_q4", [dict(title="|Y_k| (A = 1)", stems=[(yt, mag)], xlabel="k", xticks=range(-5, 6)),
                          dict(title="∠Y_k (rad)", stems=[(yt, ph)], xlabel="k", xticks=range(-5, 6))], ncols=2)
n.practice("Lesson 13", "(a) Actual — CSE 219 2023-24 Q4. (b) Actual — CSE 219 2022-23 Q5(d). (c) Actual — CSE 311 2022-23 "
           "Q1(a), 2018-19 Q2(b). (d) Actual — EEE 301 2011-12 Q1(a).",
           ["(a) x(t) = A (0 < t < T₀/2), −A (−T₀/2 < t < 0), periodic; y(t) = x(t − T₀/6). (a) Show y has half-wave symmetry. "
            "(b) Find Y_k from X_k. (c) Magnitude/phase spectra up to k = 5. (d) Compare the trigonometric series of x and y. "
            "(5 + 10 + 10 + 5)",
            "(b) Is x(t) = Σ_{k=0}^{100}(½)^k e^{jk2πt/50} real-valued? even? (5)",
            "(c) Show that the exponential FS coefficients of an even (odd) periodic signal are real (imaginary) and can be "
            "computed over half a cycle. (15–17)",
            "(d) x is real and odd, T = 2, c_k = 0 for |k| > 1, ½∫₀²|x|²dt = 1. Give two signals that satisfy this. (18)"])
n.solution()
n.code(["(a) X_k = (1/T₀)[∫₀^{T₀/2} A e^{−jkω₀t}dt − ∫_{−T₀/2}^{0} A e^{−jkω₀t}dt] = (A/(jkπ))[1 − (−1)^k]",
        "    X_k = 2A/(jπk) for odd k, 0 for even k (half-wave symmetric, real-odd ⇒ imaginary)",
        "    (a) y(t + T₀/2) = x(t + T₀/2 − T₀/6) = −x(t − T₀/6) = −y(t)  ✓ (a shift keeps half-wave symmetry)",
        "    (b) Y_k = X_k e^{−jkω₀T₀/6} = X_k e^{−jkπ/3} = (2A/(jπk)) e^{−jkπ/3}, odd k; 0 for even k",
        "    (c) |Y_k| = 2A/(π|k|): k = ±1: 0.637A, ±3: 0.212A, ±5: 0.127A",
        "        ∠Y_k = −π/2 − kπ/3 (k > 0): k=1: −5π/6;  k=3: −3π/2 ≡ +π/2;  k=5: −13π/6 ≡ −π/6  (odd in k)",
        "    (d) x(t) = Σ_{odd k} (4A/(πk)) sin kω₀t;   y(t) = Σ_{odd k} (4A/(πk)) sin(kω₀t − kπ/3)",
        "        same amplitudes (only odd harmonics); each harmonic phase-shifted by −kπ/3 (∝ k: pure delay)"])
n.figure_image(sk4, "Figure 13.1 — Spectra of y(t) = x(t − T₀/6) for CSE 219 2023-24 Q4 (A = 1)", width_cm=14)
n.answer("(b)", "Real requires a₋ₖ = a_k*. Here a_k = (½)^k for 0 ≤ k ≤ 100 but a₋ₖ = 0 ≠ a_k* ⇒ **not real**. Even requires "
         "a₋ₖ = a_k ⇒ **not even** either (x is a sum of positive-frequency exponentials only).")
n.answer("(c)", "Proof in the box above (split e^{−jkω₀t} into cos − j sin and use odd × even = odd).")
n.answer("(d)", "Real odd with only k = ±1 ⇒ x = B sin πt (ω₀ = π). Power ½∫₀²B²sin²πt dt = B²/2 = 1 ⇒ B = ±√2: "
         "x₁ = √2 sin πt and x₂ = −√2 sin πt.")
for k in [("2023-24", "CSE 219", "4(a)"), ("2023-24", "CSE 219", "4(b)–(d)"), ("2022-23", "CSE 219", "5(d)"),
          ("2022-23", "CSE 311", "1(a)"), ("2018-19", "CSE 311", "2(b)"), ("2011-12", "EEE 301", "1(a)")]:
    mark(*k)

# =============================================================== L14
n.lesson("Lesson 14 — Differentiation, Impulses, Impulse Trains, Integration", "Slides 36–72 (Lec 6)")
n.formula(["dx/dt ↔ jkω₀ a_k          ∫x dt ↔ a_k/(jkω₀) (k ≠ 0; find a₀ separately)"])
n.p("Every harmonic is a rotating arrow; differentiating gives its velocity: speed |kω₀||a_k|, direction tangent — "
    "multiplication by j (sl. 37–39). Example: d/dt x(4 − 3t) ↔ j3kω₀ a₋ₖ e^{−j4kω₀} (use the current ω₀′ = 3ω₀).")
n.p("**Derivative sketch** (sl. 42–44): slopes between jumps + impulses equal to each jump. **Sifting** (sl. 45–51): "
    "∫eᵗδ(t)dt = 1; ∫₁^∞ eᵗδ(t)dt = 0 (outside); ∫_{−5}^{5}eᵗ[δ(t+1) + 2δ(t−2)]dt = e^{−1} + 2e².")
n.h2("Impulse Train (sl. 52–56)")
n.formula(["Σₘ δ(t − mT) ↔ a_k = 1/T for every k          trig form: 1/T + (2/T)Σ cos(2πnt/T)"])
n.figure_from_pdf(A[6], 55, "Figure 14.1 — An impulse train has a flat line spectrum (Lec 6, sl. 55)", clip=CLIP, width_cm=10)
n.h2("Two Worked Uses (sl. 57–72)")
n.code(["Rectangular pulse train: dx/dt = δ(t + T₁) − δ(t − T₁) per period ⇒ b_k = (1/T)(e^{jkω₀T₁} − e^{−jkω₀T₁})",
        "   = (2j/T) sin kω₀T₁ = jkω₀ · sin(kω₀T₁)/(kπ) ✓",
        "Sawtooth x = t (0 ≤ t < 1), T = 1: dx/dt = 1 − Σδ(t − m) ⇒ b₀ = 0, b_k = −1",
        "   a_k = b_k/(jkω₀) = −1/(j2πk) = j/(2πk),  a₀ = ∫₀¹ t dt = ½"])
n.exam_approach(["Piecewise-constant or piecewise-linear x: differentiate until only impulses remain.",
                 "Impulse coefficients by sifting: δ(t − t₀) in one period ↔ (1/T)e^{−jkω₀t₀}.",
                 "Divide by (jkω₀)^m; get a₀ from the average.", "Trains with alternating signs = sum of shifted trains."])
n.practice("Lesson 14", "(a) Actual — EEE 211 2022-23 Q8(a). (b) Actual — EEE 211 2019-20 Q7(a). (c) Actual — EEE 211 2020-21 "
           "Q7(a). (d) Actual — EEE 301 2014-15 Q4(a), 2015-16 Q6(a).",
           ["(a) Trigonometric FS (A₀ + ΣAₙcos(2πnt/T₀ + φ)) of δ_{T₀}(t); amplitude spectrum. (20)",
            "(b) Exponential FS of (i) unit impulses at every integer; (ii) impulses −1 at even integers and +1 at odd "
            "integers. (15)",
            "(c) x(t) = 1 − |t| on [−2, 2], period 4 (triangle between ±1); y(t) = 4 on (0, 2), 0 on (2, 4), period 4. Find "
            "the exponential FS of x, then y by properties; amplitude spectra. (20)",
            "(d) C_n = ½[1 − (−1)ⁿ], T = 20 ms: real signal? find x(t). Impulse train: FS, FT, PSD."])
n.solution()
n.answer("(a)", "a_k = 1/T₀ for all k ⇒ δ_{T₀}(t) = 1/T₀ + (2/T₀)Σ_{n≥1} cos(2πnt/T₀): A₀ = 1/T₀, Aₙ = 2/T₀, φ = 0. Amplitude "
         "spectrum: a line of height 1/T₀ at n = 0 and 2/T₀ at every harmonic n·(1/T₀) Hz.")
n.answer("(b)", "(i) T = 1: a_k = 1 for all k ⇒ x = Σ e^{j2πkt}. (ii) T = 2, one period has −δ(t) and +δ(t − 1): "
         "a_k = ½[−1 + e^{−jkπ}] = ½[(−1)^k − 1] = −1 for odd k, 0 for even k ⇒ x = −Σ_{odd k} e^{jkπt} = −2Σ_{odd}cos kπt.")
n.code(["(c) x′ = −1 on (0,2), +1 on (−2,0); x″ = 2δ(t + 2) − 2δ(t) per period (T = 4, ω₀ = π/2)",
        "    (jkω₀)² a_k = (1/4)[2e^{jkπ} − 2] ⇒ a_k = (1 − (−1)^k)/(2·k²π²/4) = 4/(k²π²) for odd k, 0 even; a₀ = 0",
        "    y = 2 − 2x′(t)  (x′ = −1 on (0,2) gives 4, +1 on (2,4) gives 0)",
        "    b₀ = 2;  b_k = −2·jkω₀ a_k = −2j(kπ/2)(4/(k²π²)) = −4j/(πk) for odd k, 0 for even k ≠ 0",
        "    |a_k| = 4/(π²k²): 0.405, 0.045, 0.016 (k = 1, 3, 5);   |b_k| = 4/(π|k|): 1.273, 0.424, 0.255; |b₀| = 2"])
n.answer("(d)", "C_n = 1 for odd n, 0 for even n (C₀ = 0). C₋ₙ = Cₙ* and real ⇒ x is real and even. "
         "x = Σ_{odd n} e^{jnω₀t}, ω₀ = 2π/0.02 = 100π rad/s. Since Σ_{all}e^{jnω₀t} = T₀Σδ(t − kT₀) and the even-n part is "
         "(T₀/2)Σδ(t − kT₀/2), x(t) = (T₀/2)Σ_k(−1)^kδ(t − kT₀/2) = 0.01Σ(−1)^kδ(t − 0.01k): alternating impulses every "
         "10 ms. Impulse train δ_T: FS a_k = 1/T; FT (2π/T)Σδ(ω − 2πk/T); PSD S(ω) = (2π/T²)Σδ(ω − 2πk/T).")
for k in [("2022-23", "EEE 211", "8(a)"), ("2019-20", "EEE 211", "7(a)"), ("2020-21", "EEE 211", "7(a)"),
          ("2014-15", "EEE 301", "4(a)"), ("2015-16", "EEE 301", "6(a)")]:
    mark(*k)

# =============================================================== L15
n.lesson("Lesson 15 — Multiplication, Parseval, and Periodic Inputs to LTI Systems",
         "Slides 73–81 (Lec 6) · Parseval and LTI response: textbook")
n.formula(["x(t)y(t) ↔ c_k = Σₚ aₚ b_{k−p}   (convolution of coefficients)"])
n.p("Proof (sl. 75–78): put z = e^{jω₀t}; each series is a polynomial in z, and the product's z^k coefficient collects "
    "pairs with p + q = k. Example: x = 1 + cos ω₀t (a₀ = 1, a±₁ = ½) ⇒ x² ↔ {¼, 1, 3/2, 1, ¼} for k = −2…2; check: "
    "(1 + cos)² = 3/2 + 2cos ω₀t + ½cos 2ω₀t ✓.")
n.h2("Parseval and Power (textbook)")
n.formula(["P = (1/T)∫_T |x|² dt = Σ |a_k|²  (= C₀² + Σ Cₙ²/2 in compact trig form)"])
n.h2("Periodic Input to an LTI System (textbook)")
n.p("e^{jkω₀t} is an eigenfunction: it comes out as H(jkω₀)e^{jkω₀t}. So a periodic input with coefficients a_k gives a "
    "periodic output (same T) with")
n.formula(["y_k = H(jkω₀) a_k          A cos(ω t + θ) → A|H(jω)| cos(ωt + θ + ∠H(jω))"])
n.callout("memorize", "Distortionless system (EEE 2017-18 Q1(b)): H = K e^{−jωt_d} ⇒ y_k = K e^{−jkω₀t_d} a_k (same "
          "magnitudes ×K, phase linear in k). Ideal LPF with cutoff ω_c: keep only harmonics with |kω₀| < ω_c.")
n.exam_approach(["Find a_k of the input (inspection / standard waveform).", "Find H(jω) of the system (circuit: voltage "
                 "divider with jωL, 1/(jωC); ODE: replace d/dt by jω).", "Multiply harmonic by harmonic; list magnitudes "
                 "and phases.", "Power: Parseval on the output coefficients."])
n.practice("Lesson 15", "(a) Actual — EEE 211 2023-24 Q7(b). (b) Actual — EEE 211 2020-21 Q7(b). (c) Actual — EEE 211 2019-20 "
           "Q5(b). (d) Actual — EEE 211 2021-22 Q3(a). (e) Older: EEE 211 2017-18 Q1(c), EEE 301 2015-16 Q4(b), 2011-12 Q1(b), "
           "2012-13 Q4(b), EEE 211 2018-19 Q3(c).",
           ["(a) Half-wave rectified sine x(t) = sin(2πt/T) on the first half period, T = 0.5 ms, feeds (1) a differentiator, "
            "(2) a LPF with |H₂| = 5, linear phase (±π/2 at ±f_c), f_c = 1 kHz. (i) FS coefficients of y₁ from those of x. "
            "(ii) y₂(t); which harmonics survive? (iii) Compare the two systems. (25)",
            "(b) y″ + 3y′ + 2y = x′ + x, x = 2cos t + 6cos 3t: amplitude and phase spectra of y; average power by Parseval. (15)",
            "(c) Full-wave rectified sin t feeds an RC low-pass (R = 15 Ω, C = 1/5 F, output across C). H(ω) and y(t). (20)",
            "(d) Period 4: x = δ(t − 1) + 2[u(t − 2) − u(t − 4)] in one period, applied to a 0.1 H series inductor, 100 µF shunt "
            "capacitor and 1 kΩ load. Magnitude and phase spectra of x and y. (20)",
            "(e) Older (see solutions)."])
n.solution()
n.code(["(a) f₀ = 2 kHz, ω₀ = 4000π. Half-wave rectified sine (amplitude 1):",
        "    a₀ = 1/π,  a±₁ = ∓j/4,  a_k = −1/(π(k² − 1)) for even k,  0 for odd |k| ≥ 3",
        "(i) Differentiator H₁ = jω:  b_k = jkω₀ a_k  ⇒ b₀ = 0, b±₁ = (jω₀)(∓j/4)·(±1) = ω₀/4 = 1000π,",
        "    b_k = −jkω₀/(π(k² − 1)) = −j4000k/(k² − 1) for even k",
        "(ii) LPF passes |f| < 1 kHz only: the lowest harmonic is 2 kHz ⇒ only DC survives:",
        "    y₂(t) = H₂(0)a₀ = 5/π ≈ 1.59  (constant; harmonic k = 0 only)",
        "(iii) the differentiator scales harmonic k by |k|ω₀ — it boosts high frequencies and removes DC;",
        "     the LPF removes everything except DC — it keeps the average and rejects all harmonics"])
n.code(["(b) H(jω) = (jω + 1)/((jω)² + 3jω + 2) = 1/(jω + 2)",
        "    ω = 1: |H| = 1/√5, ∠H = −26.57°;   ω = 3: |H| = 1/√13, ∠H = −56.31°",
        "    y = (2/√5)cos(t − 26.57°) + (6/√13)cos(3t − 56.31°) = 0.894cos(t − 26.57°) + 1.664cos(3t − 56.31°)",
        "    P = ½(0.894² + 1.664²) = ½(4/5 + 36/13) = 1.785 W (1-Ω basis)",
        "(c) |sin t| = 2/π − (4/π)Σ_{k≥1} cos 2kt/(4k² − 1)   (T = π, ω₀ = 2)",
        "    RC = 3: H(ω) = 1/(1 + j3ω)",
        "    y(t) = 2/π − (4/π)Σ |H(j2k)| cos(2kt − tan⁻¹6k)/(4k² − 1)",
        "         = 0.637 − 0.0698cos(2t − 80.54°) − 0.0070cos(4t − 85.24°) − …   (nearly pure DC)",
        "(d) a₀ = (1 + 4)/4 = 5/4;  a_k = ¼e^{−jkπ/2} + j(1 − (−1)^k)/(kπ)   (ω₀ = π/2)",
        "    a±₁ = ±j(1/π·2 − ¼) = ±j0.387;  a±₂ = −¼;  a±₃ = ±j(2/(3π) + ¼) = ±j0.462;  a₄ = ¼ …",
        "    H(jω) = 1/(1 − ω²LC + jωL/R),  LC = 10⁻⁵, L/R = 10⁻⁴ ⇒ |H(jkπ/2)| = 1.000, ∠H ≈ −0.01° for low k",
        "    ⇒ output spectrum ≈ input spectrum (the filter's corner, 1/√(LC) = 316 rad/s, is far above kω₀ for small k)"])
n.code(["(e) EEE 211 2017-18 Q1(c): H passes |ω| ≤ 3π ⇒ y = 1 + 2cos2πt (cos4πt, cos6πt removed)",
        "    EEE 301 2015-16 Q4(b): a±₁ = ½, b±₁ = ±1/(2j) ⇒ c₀ = 0, c₂ = 1/(4j), c₋₂ = −1/(4j)  ⇒ z = ½ sin 8πt",
        "    EEE 301 2011-12 Q1(b): x = 2 + square wave (±1, T = 8, ω₀ = π/4); H(0) = 4; odd harmonics at kπ/4 meet",
        "      H = sin(kπ)/(kπ/4) = 0 ⇒ y(t) = 4·2 = 8 (constant)",
        "    EEE 301 2012-13 Q4(b): half-wave cos t: 2nd and 4th harmonic amplitudes 2/(3π) = 0.212, 2/(15π) = 0.042;",
        "      the LC–R network has |H| ≈ 1 at ω = 2, 4 (LC = 10⁻⁵) ⇒ output amplitudes ≈ 0.212 and 0.042",
        "    EEE 211 2018-19 Q3(c): T = 2, ω₀ = π, C_n = 1 (odd n); the band 2π < |ω| < 4π passes only n = ±3 ⇒",
        "      y = 2cos(3πt − π/2) = 2 sin 3πt (with −π/2 for ω > 0); h(t) = band-pass with −j sgn ω (method)"])
for k in [("2023-24", "EEE 211", "7(b)"), ("2020-21", "EEE 211", "7(b)"), ("2019-20", "EEE 211", "5(b)"),
          ("2021-22", "EEE 211", "3(a)"), ("2017-18", "EEE 211", "1(c)"), ("2015-16", "EEE 301", "4(b)"),
          ("2011-12", "EEE 301", "1(b)"), ("2012-13", "EEE 301", "4(b)")]:
    mark(*k)
for k in [("2018-19", "EEE 211", "3(c)"), ("2018-19", "EEE 211", "1(c)"), ("2016-17", "EEE 211", "2(b)"),
          ("2015-16", "EEE 301", "4(a)"), ("2014-15", "EEE 301", "4(b)"), ("2013-14", "EEE 301", "4(b)"),
          ("2010-11", "EEE 301", "1(b)")]:
    mark(*k, "◐ Method")

n.quick_notes("Quick Notes — Fourier Series", "Revision points for Lessons 11–15.",
              [("L11 · Idea, Orthogonality", ["x = Σ a_k e^{jkω₀t}, a_k = (1/T)∫_T x e^{−jkω₀t}dt, a₀ = average.",
                                             "Orthogonal: ∫φᵢφⱼ* = 0; normalize by 1/√E; cᵢ = ⟨x, φᵢ⟩/Eᵢ.",
                                             "Dirichlet: absolutely integrable, finite extrema, finite jumps — sufficient, not necessary."]),
               ("L12 · Coefficients", ["Square wave: a₀ = 2T₁/T, a_k = sin(kω₀T₁)/(kπ).",
                                      "Ramp (T = 3): a₀ = ½, a_k = (e^{−jkω₀} − 1)/(2k²ω₀²) (slide prints 6).",
                                      "cₙ = (aₙ − jbₙ)/2, Cₙ = 2|cₙ|."]),
               ("L13 · Properties", ["Shift: a_k e^{−jkω₀t₀}; reverse: a₋ₖ; x(αt): same a_k, ω₀ → αω₀.",
                                    "Real: a₋ₖ = a_k*; even → real; odd → imaginary; half-wave → odd harmonics only."]),
               ("L14 · Derivative, Trains", ["dx/dt ↔ jkω₀a_k; ∫ ↔ a_k/(jkω₀) (a₀ separately).",
                                            "Σδ(t − mT) ↔ 1/T. Sawtooth t (T = 1): a₀ = ½, a_k = j/(2πk)."]),
               ("L15 · Products, LTI", ["xy ↔ Σ aₚb_{k−p}. P = Σ|a_k|².", "LTI: y_k = H(jkω₀)a_k."])],
              diagrams=[(A[5], 30, "The periodic square wave (Lec 5, sl. 30)", CLIP, 10),
                        (A[6], 59, "Derivative of the rectangular pulse train (Lec 6, sl. 59)", CLIP, 10)])
n.save()
save_solved("anik_fourier_series")
print("saved", n.out_path)
