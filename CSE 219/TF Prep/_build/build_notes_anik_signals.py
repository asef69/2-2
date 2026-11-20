"""Anik F1 — Signals: energy & power, transformations, even/odd, step & impulse, periodicity (Lec 1–2)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402

from c219 import A, anik, exam_map, mark, pw, save_solved, sketch  # noqa: E402

T = np.linspace
CLIP = (0.0, 0.12, 1.0, 0.98)

n = anik("Lec 1–2 · Signals: Energy, Transformations, Even–Odd, Step & Impulse, Periodicity",
         "CSE219_Anik_Signals_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "signal-basics questions and how much they matter"),
              ("Lesson 1 — Energy and Power", "E and P in CT and DT; energy vs power signals"),
              ("Lesson 2 — Time Shifting, Reversal and Scaling", "the x(αt+β) recipe, sketches step by step"),
              ("Lesson 3 — Even and Odd Decomposition", "x_e, x_o for piecewise CT and DT signals"),
              ("Lesson 4 — Unit Step, Unit Impulse, Ramp and Signals Built from Them", "δ = du/dt, sifting, jumps → impulses, δ models"),
              ("Lesson 5 — Exponentials, Sinusoids and Periodicity", "CT and DT periodicity, sums of sinusoids"),
              ("Quick Notes — Signals", "merged revision notes + key diagrams")],
    source_note="Slide numbers refer to Lecture-1-A-Little-Introduction-to-Signals.pdf (53 slides, “Lec 1”) and "
                "Lecture-2-Some-Useful-Signals.pdf (51 slides, “Lec 2”). Questions are labelled by session and course: "
                "CSE 219 = this course (pages in the merged TF PDF or “22 batch p.N”); EEE 211 / EEE 301 = the EEE "
                "department's Continuous Signals and Linear Systems papers, same content (pages “EEE p.N”). "
                "Ramp functions, impulse scaling and δ′(t) are textbook background (marked).")

# ====================================================================== exam map
n.h1("Exam Map — What the TF Papers Ask")
n.p("Signal basics open almost every paper. In CSE 219 they are the first Anik-section questions (2022-23 Q5(a), Q7; "
    "2023-24 Q1(a), Q3(a)); in the EEE papers they are Q1 or Q5 every year.")
exam_map(n, "Anik", range(1, 6))
n.callout("focus", "Most repeated, in order: (1) sketch x(αt+β) or a sum of such signals — CSE 219 2022-23 Q7 (23 marks), "
          "2023-24 Q1(a) (15), EEE every year · (2) write a piecewise signal with u(t), r(t) and sketch its derivative "
          "(impulses at jumps) · (3) periodicity of CT/DT sinusoids (2022-23 Q5(c), 2023-24 Q3(a)) · (4) even–odd parts "
          "(2022-23 Q5(a), 15 marks) · (5) energy or power signal. Learn the x(αt+β) recipe (Lesson 2) first: it is "
          "worth about 25 marks per CSE 219 paper.")

# ====================================================================== Lesson 1
n.lesson("Lesson 1 — Energy and Power", "Slides 2–16 (Lec 1)")
n.h2("1. Signals (sl. 2–5)")
n.p("A signal is a pattern of change that carries information, as a function of time (voice, voltage) or space (image "
    "brightness).")
n.bullets(["**Continuous-time (CT)** signal x(t): defined at every real t (microphone voltage, temperature).",
           "**Discrete-time (DT)** signal x[n]: defined only at integer n (audio samples, a daily log). x[0.5] and x[π] "
           "do not exist.",
           "Convention: round brackets ( ) for CT, square brackets [ ] for DT."])
n.h2("2. Energy and Power (sl. 6–7)")
n.p("Square the values and add them up. |·| makes the formulas work for complex signals too.")
n.table(["", "Continuous time", "Discrete time"],
        [["Energy in an interval", "E = ∫_{t1}^{t2} |x(t)|² dt", "E = Σ_{n=n1}^{n2} |x[n]|²"],
         ["Average power in the interval", "P = E / (t2 − t1)", "P = E / (n2 − n1 + 1)"],
         ["Total energy", "E∞ = ∫_{−∞}^{∞} |x(t)|² dt", "E∞ = Σ_{n=−∞}^{∞} |x[n]|²"],
         ["Total average power", "P∞ = lim_{T→∞} (1/2T) ∫_{−T}^{T} |x(t)|² dt", "P∞ = lim_{N→∞} (1/(2N+1)) Σ_{−N}^{N} |x[n]|²"]],
        widths_cm=[4.2, 6.5, 6.5])
n.callout("memorize", "**Energy signal**: 0 < E∞ < ∞ (then P∞ = 0). **Power signal**: 0 < P∞ < ∞ (then E∞ = ∞). "
          "**Neither**: E∞ = ∞ and P∞ = ∞ (e.g. a ramp, e^{2t}) or the integral does not exist. A signal can never be both.",
          ["• Periodic signal (period T0): E∞ = ∞, P∞ = (1/T0) ∫_{T0} |x|² dt — one period is enough.",
           "• Finite-duration, bounded signal: always an energy signal.",
           "• A sinusoid A cos(ω0t + φ): P = A²/2. A complex exponential A e^{jω0t}: P = |A|²."])
n.h2("3. Worked Examples from the Slides (sl. 8–16)")
n.p("**Half-sine** x(t) = sin t on 0 ≤ t ≤ π, 0 elsewhere (sl. 8–9):")
n.code(["E = ∫₀^π sin²t dt = ∫₀^π (1 − cos 2t)/2 dt = π/2",
        "P[0,π] = E/(π − 0) = 1/2"])
n.p("**Discrete** x[0..3] = {1, −2, 2, −1} (sl. 10–11): E = 1 + 4 + 4 + 1 = 10, P[0,3] = 10/4 = 2.5.")
n.p("**Periodic half-sine** (sl. 12–14): repeating the lobe with period π gives E∞ = π/2 + π/2 + … = ∞ but "
    "P = (1/π)(π/2) = 1/2. If the lobe rests for half the period (period 2π), P = (1/2π)(π/2) = 1/4.")
n.figure_from_pdf(A[1], 14, "Figure 1.1 — Half-sine repeating with period 2π: infinite energy, power 1/4 (Lec 1, sl. 14)",
                  clip=CLIP, width_cm=10)
n.p("**An infinite-range signal with finite energy** (sl. 15–16): x(t) = 1 for |t| ≤ 1, 1/|t| for |t| > 1.")
n.code(["E = ∫_{−1}^{1} 1 dt + 2 ∫₁^∞ t^{−2} dt = 2 + 2[−1/t]₁^∞ = 2 + 2 = 4",
        "P∞ = 0     (finite energy spread over infinite time)"])
n.callout("trap", "Infinite duration does not mean infinite energy: 1/|t| tails have finite energy because ∫ t^{−2} "
          "converges. But 1/√|t| tails would give ∫ t^{−1} = ∞. Always integrate |x|², not x.")
n.exam_approach(["Sketch |x|² and decide what happens as t → ±∞: decays fast enough → try energy; settles to a "
                 "nonzero level or is periodic → power; grows → neither.",
                 "Energy: integrate |x|² over the support (split piecewise signals).",
                 "Power: for periodic signals average one period; for signals that settle to constants c₋ (t → −∞) and "
                 "c₊ (t → +∞), P∞ = (c₋² + c₊²)/2.",
                 "State the class in words: “E finite ⇒ energy signal, P = 0”."])
n.practice("Lesson 1",
           "(a) Actual — EEE 211 2021-22 Q1(b). (b) Actual — EEE 211 2020-21 Q5(b). (c) Actual — EEE 211 2018-19 Q6(a)(i). "
           "(d) Practice set 1.1. (e) Older EEE papers, quick answers.",
           ["(a) Determine whether e^{−3t} sin(2πt/3 − 4) u(t) is a power or an energy signal. (10)",
            "(b) Power or energy: (i) u(t − 6) − u(−t + 8); (ii) 2r(t − 4)u(t). (10)",
            "(c) Is x₁(t) = exp[j(2πt + π/4)] + exp(−2|t|) a power or an energy signal? (part of 15)",
            "(d) x(t) = t + 1 (−1 ≤ t < 0), 2 − t (0 ≤ t ≤ 2), 0 otherwise. Find its energy and its average power over [−1, 2].",
            "(e) Classify: (i) e^{−t}cos 3t u(t); (ii) u(t) − 2u(t−2) + u(t−5); (iii) u(t) + 5u(t−1) − 2u(t−2); "
            "(iv) 2 sin(3πt/8) cos(2πt/3); (v) 1 for t < 0, e^{3t} for t ≥ 0; (vi) A e^{−t}u(t) and A e^{−a|t|} (a > 0)."])
n.solution()
n.answer("(a)", "|x|² ≤ e^{−6t} for t ≥ 0, so E ≤ ∫₀^∞ e^{−6t} dt = 1/6 < ∞ → energy signal (P∞ = 0). Exact value "
         "(write sin² = (1 − cos 2θ)/2 with ω = 2π/3):")
n.code(["E = ∫₀^∞ e^{−6t} sin²(ωt − 4) dt = 1/12 − (1/2) Re{ e^{−j8} / (6 − j2ω) }",
        "  = 1/12 − (6 cos 8 + 2ω sin 8) / (2(36 + 4ω²))",
        "  = 0.08333 − (−0.873 + 4.144)/107.09 = 0.0528"])
n.answer("(b)", "(i) u(t − 6) = 1 for t > 6; u(8 − t) = 1 for t < 8. So x = −1 (t < 6), 0 (6 < t < 8), +1 (t > 8). "
         "E∞ = ∞, P∞ = [(−1)² + 1²]/2 = 1 → **power signal**, P = 1. (ii) 2r(t − 4)u(t) = 2(t − 4) for t ≥ 4: it grows "
         "without bound, (1/2T)∫(2(t−4))²dt → ∞ → **neither**.")
n.answer("(c)", "|x₁|² = 1 + e^{−4|t|} + 2e^{−2|t|}cos(2πt + π/4). The last two terms have finite area, so their "
         "contribution to (1/2T)∫ vanishes: P∞ = 1, E∞ = ∞ → **power signal**, P = 1 (the power of the exponential).")
n.answer("(d)", "Integrate each piece:")
n.code(["E = ∫_{−1}^{0} (t+1)² dt + ∫₀² (2−t)² dt = 1/3 + 8/3 = 3",
        "P[−1,2] = E / 3 = 1"])
n.answer("(e)", "(i) E = ∫₀^∞ e^{−2t}(1 + cos 6t)/2 dt = ½(½ + 2/40) = 0.275 → energy. (ii) 1 on (0,2), −1 on (2,5): "
         "E = 2 + 3 = 5 → energy. (iii) value 6 on (1,2), 4 for t > 2: P∞ = 4²/2 = 8 → power. (iv) = sin(25πt/24) "
         "− sin(7πt/24): two sinusoids of amplitude 1 → P = ½ + ½ = 1 → power. (v) grows as e^{3t} → neither. "
         "(vi) E = A²/2 and E = 2·A²/(2a) = A²/a → both energy signals.")
mark("2021-22", "EEE 211", "1(b)"); mark("2020-21", "EEE 211", "5(b)")
mark("2018-19", "EEE 211", "6(a)", "◐ Method")
for y, c, q in [("2015-16", "EEE 301", "1(b)"), ("2013-14", "EEE 301", "2(a)"), ("2011-12", "EEE 301", "6(b)"),
                ("2010-11", "EEE 301", "6(a)")]:
    mark(y, c, q)
mark("2015-16", "EEE 301", "1(b)", "◐ Method")  # part (iii) with impulses: see Lesson 4 note
n.callout("note", "EEE 301 2015-16 Q1(b)(iii) and EEE 211 2018-19 Q6(a)(ii) contain impulses δ(t − 2k) inside the signal. "
          "|δ|² is not defined, so the energy integral does not exist: classify as “neither” and say why.")

# ====================================================================== Lesson 2
n.lesson("Lesson 2 — Time Shifting, Reversal and Scaling", "Slides 17–39 (Lec 1)")
n.h2("1. The Three Operations (sl. 18–25)")
n.table(["Operation", "Rule (t0 > 0, α > 1)", "Effect on a feature at t = a"],
        [["Delay", "x(t − t0)", "moves right: a → a + t0"],
         ["Advance", "x(t + t0)", "moves left: a → a − t0"],
         ["Reversal", "x(−t)", "mirror about t = 0: a → −a"],
         ["Compression", "x(αt)", "a → a/α (narrower)"],
         ["Stretching", "x(t/α)", "a → αa (wider)"],
         ["Amplitude scaling", "A·x(t)", "height × A, time unchanged"]],
        widths_cm=[3.4, 5.0, 8.8])
n.p("DT shifts work the same way: x[n − 4] moves every sample 4 places right (sl. 21). Time scaling changes only the "
    "horizontal axis, not the height (sl. 25).")
n.h2("2. Order Matters (sl. 26–27)")
n.code(["x(t) --shift left 3--> x(t+3) --compress by 2--> x(2t+3)      ✓",
        "x(t) --compress by 2--> x(2t) --shift left 3--> x(2(t+3)) = x(2t+6)   ✗ (different!)"])
n.p("Each operation replaces t by something in the **whole** current expression. After compressing, a later shift "
    "of 3 becomes a shift of the argument by 6.")
n.h2("3. The Recipe for x(αt + β) (sl. 28–31)")
n.formula(["x(t) → g₁(t) = x(t + β) → g₂(t) = g₁(−t) if α < 0 → g₃(t) = g₂(|α|t) = x(αt + β)"])
n.bullets(["Step 1 — shift by β (β > 0: left; β < 0: right).",
           "Step 2 — reverse only if α < 0.",
           "Step 3 — scale by |α| (|α| > 1 compress, |α| < 1 stretch).",
           "Write the intermediate signal after every step (sl. 30)."])
n.callout("memorize", "Fast check (no sketch needed): a feature of x at t = a appears in x(αt + β) at **t = (a − β)/α**. "
          "Use it to find the new break points and the new support, then join them with the same shapes.")
n.h2("4. Worked Example: x(−3t + 2) (sl. 31–35)")
n.p("x(t) = 1 on 0 ≤ t < 1, 2 − t on 1 ≤ t ≤ 2, 0 otherwise.")
n.code(["Step 1  x(t+2)   = 1 on [−2,−1),  −t on [−1,0]",
        "Step 2  x(−t+2)  = t on [0,1),    1 on [1,2]",
        "Step 3  x(−3t+2) = 3t on [0,1/3), 1 on [1/3,2/3]",
        "Check with t = (a − β)/α: a = 0 → t = 2/3; a = 1 → t = 1/3; a = 2 → t = 0  ✓"])
n.figure_from_pdf(A[1], 35, "Figure 2.1 — The final compressed, reversed signal x(−3t + 2) (Lec 1, sl. 35)",
                  clip=CLIP, width_cm=10)
n.h2("5. Two Practice Problems from the Slides (sl. 36–39)")
n.p("**Practice 1**: x(3(2 − t/2)) = x(6 − 3t/2): shift left by 6 → x(t + 6); reverse → x(−t + 6); compress by 3/2 → "
    "x(−3t/2 + 6).")
n.p("**Practice 2**: start with x(t) and stretch by 2, shift left by 3, compress by 4, reverse:")
n.code(["y1 = x(t/2);  y2 = y1(t+3) = x((t+3)/2);  y3 = y2(4t) = x(2t + 3/2);  y4 = y3(−t) = x(−2t + 3/2)"])
n.callout("trap", "• A shift applied after scaling acts on t, not on αt: from x(2t), “shift left by 3” gives x(2(t+3)). "
          "• Reversal and scaling commute, but neither commutes with a shift. • Keep jumps (vertical edges) as jumps — "
          "they only move, they never become slopes.")
n.exam_approach(["Write x(t) piecewise first (the papers give 3 marks just for this).",
                 "Rewrite the argument as αt + β (expand brackets: −2(t − 1) = −2t + 2).",
                 "Apply the recipe: shift, reverse if α < 0, scale; name each intermediate signal and the property used.",
                 "Map every break point with t = (a − β)/α; check one interior value by direct substitution.",
                 "For sums such as x(·) + x(·), sketch each term separately, then add point by point."])
# figures for the CSE 219 questions
x7 = lambda a: pw(a, [(-2, -1, lambda s: s + 1), (-1, 0, lambda s: 1 + 0 * s), (0, 2.0001, lambda s: 1 - s / 2)])
tt = T(-5, 7, 2401)
sk7 = sketch("anik1_q7", [
    dict(title="x(t)  (Fig. 2)", curves=[(tt, x7(tt))], xlim=(-3, 3), xticks=range(-3, 4)),
    dict(title="Step 1: x(t+2) (shift left 2)", curves=[(tt, x7(tt + 2))], xlim=(-5, 1), xticks=range(-5, 2)),
    dict(title="Step 2: x(−t+2) (reverse)", curves=[(tt, x7(-tt + 2))], xlim=(-1, 5), xticks=range(-1, 6)),
    dict(title="Step 3: x(−2t+2) (compress by 2)", curves=[(tt, x7(-2 * tt + 2))], xlim=(-1, 3),
         xticks=[-1, 0, 0.5, 1, 1.5, 2, 3]),
    dict(title="x(−t+1) (shift left 1, reverse)", curves=[(tt, x7(-tt + 1))], xlim=(-2, 4), xticks=range(-2, 5)),
    dict(title="x(−t/2+1) (stretch by 2)", curves=[(tt, x7(-tt / 2 + 1))], xlim=(-3, 7), xticks=range(-2, 7, 2))],
    ncols=3)
n.practice("Lesson 2",
           "(a) Actual — CSE 219 2022-23 Q7(a)–(c). (b) Actual — CSE 219 2023-24 Q1(a). (c) Actual — CSE 219 2022-23 Q7(d). "
           "(d) Actual — EEE 301 2010-11 Q5(b)(ii). (e) Adapted — EEE 211 2016-17 Q5(b).",
           ["(a) x(t) of Figure 2 is 0 for t < −2 and t > 2: it rises linearly from −1 at t = −2 to 0 at t = −1, jumps to 1 "
            "and stays at 1 up to t = 0, then falls linearly to 0 at t = 2. (i) Write x(t) piecewise. (ii) Determine and "
            "draw x(−2t + 2), naming the properties used. (iii) Determine and draw x(−t/2 + 1). (3 + 10 + 10)",
            "(b) x(t) = 1 − |t| for |t| ≤ 1, 0 otherwise. Sketch y(t) = x(−2(t − 1)) + x((t + 2)/2), showing the effect of each "
            "operation on the two components. (15)",
            "(c) An image is a discrete signal. Which signal property/operation is useful for: compression, blurring, "
            "sharpening, flipping, zooming, contrast, edge detection? (7)",
            "(d) x(t) = −t + 1 (−1 ≤ t < 0), t (0 ≤ t < 2), 2 (2 ≤ t < 3), 0 otherwise. Find x(t − 2), x(t + 3), x(−3t − 2) "
            "and x(2t/3 + 1/2) analytically.",
            "(e) If y(t) = x(−2t + 6) is known, how do you recover x(t)?"])
n.solution()
n.answer("(a)", "(i) x(t) = t + 1 for −2 ≤ t < −1;  1 for −1 ≤ t ≤ 0;  1 − t/2 for 0 < t ≤ 2;  0 otherwise.")
n.code(["(ii) x(−2t+2):  α = −2, β = 2",
        "Step 1 (time shift, left by 2):  g1 = x(t+2) = t+3 on [−4,−3),  1 on [−3,−2],  −t/2 on (−2,0]",
        "Step 2 (time reversal):          g2 = x(−t+2) = t/2 on [0,2),  1 on [2,3],  3−t on (3,4]",
        "Step 3 (time compression by 2):  x(−2t+2) = t on [0,1),  1 on [1,1.5],  3−2t on (1.5,2]",
        "Check: t = 2 → x(−2) = −1 and 3 − 4 = −1 ✓;  t = 1 → x(0) = 1 ✓",
        "",
        "(iii) x(−t/2+1):  α = −1/2, β = 1",
        "Step 1 (shift left 1):     x(t+1) = t+2 on [−3,−2),  1 on [−2,−1],  (1−t)/2 on (−1,1]",
        "Step 2 (reversal):         x(−t+1) = (1+t)/2 on [−1,1),  1 on [1,2],  2−t on (2,3]",
        "Step 3 (stretch by 2):     x(−t/2+1) = 1/2 + t/4 on [−2,2),  1 on [2,4],  2 − t/2 on (4,6]",
        "Check: t = 6 → x(−2) = −1 and 2 − 3 = −1 ✓;  t = −2 → x(2) = 0 ✓"])
n.figure_image(sk7, "Figure 2.2 — CSE 219 2022-23 Q7: x(t), the three steps to x(−2t+2), and x(−t/2+1)", width_cm=16.5)
tri = lambda a: np.clip(1 - np.abs(a), 0, None)
sk1a = sketch("anik1_23q1a", [
    dict(title="x(−2(t−1)): centre t=1, half-width ½", curves=[(tt, tri(-2 * (tt - 1)))], xlim=(-5, 2),
         xticks=[-4, -2, 0, 1]),
    dict(title="x((t+2)/2): centre t=−2, half-width 2", curves=[(tt, tri((tt + 2) / 2))], xlim=(-5, 2),
         xticks=[-4, -2, 0, 1]),
    dict(title="y(t) = sum", curves=[(tt, tri(-2 * (tt - 1)) + tri((tt + 2) / 2))], xlim=(-5, 2),
         xticks=[-4, -2, 0, 1])], ncols=3)
n.answer("(b)", "First component x(−2(t − 1)) = x(−2t + 2): shift left 2 → triangle centred at −2; reverse → centred at "
         "+2; compress by 2 → centred at t = 1, half-width 1/2 (feature at a = 0 → t = (0 − 2)/(−2) = 1; a = ±1 → t = ½, "
         "3/2). Reversal changes nothing visible because the triangle is even. Second component x((t + 2)/2) = x(t/2 + 1): "
         "shift left 1 → centred at −1; stretch by 2 → centred at t = −2, half-width 2 (a = ±1 → t = 0, −4). The two "
         "triangles do not overlap, so:")
n.code(["y(t) = (t+4)/2      −4 ≤ t ≤ −2",
        "       −t/2         −2 < t ≤ 0",
        "       2t − 1        1/2 ≤ t ≤ 1",
        "       3 − 2t        1 < t ≤ 3/2",
        "       0             otherwise        (peaks y(−2) = y(1) = 1)"])
n.figure_image(sk1a, "Figure 2.3 — CSE 219 2023-24 Q1(a): the two transformed triangles and their sum", width_cm=16.5)
n.answer("(c)", "Compression — frequency content (Fourier/DCT): keep large low-frequency coefficients, drop small "
         "high-frequency ones. Blurring — convolution with an averaging (low-pass) kernel. Sharpening — high-pass "
         "filtering / adding back a differentiated (difference) image. Flipping — time (index) reversal x[−n] (x[−m, n] "
         "for a horizontal flip). Zooming — time (index) scaling: up-/down-sampling with interpolation. Contrast — "
         "amplitude scaling (and shifting) of pixel values; the spread (power/variance) of the values measures it. "
         "Edge detection — first difference x[n] − x[n−1] (derivative), i.e. high frequencies.")
n.answer("(d)", "Map each interval endpoint with t = (a − β)/α and keep the formula of each piece:")
n.code(["x(t−2)   : shift right 2:  −t+3 on [1,2),  t−2 on [2,4),  2 on [4,5)",
        "x(t+3)   : shift left 3 :  −t−2 on [−4,−3), t+3 on [−3,−1), 2 on [−1,0)",
        "x(−3t−2) : a = −3t−2, t = −(a+2)/3:",
        "           a ∈ [−1,0) → t ∈ (−2/3,−1/3]: x = −a+1 = 3t+3",
        "           a ∈ [0,2)  → t ∈ (−4/3,−2/3]: x = a = −3t−2",
        "           a ∈ [2,3)  → t ∈ (−5/3,−4/3]: x = 2",
        "x(2t/3+1/2): a = 2t/3+1/2, t = 3(a − 1/2)/2:",
        "           a ∈ [−1,0) → t ∈ [−9/4,−3/4): x = −a+1 = 1/2 − 2t/3",
        "           a ∈ [0,2)  → t ∈ [−3/4, 9/4): x = 2t/3 + 1/2",
        "           a ∈ [2,3)  → t ∈ [9/4, 15/4): x = 2"])

n.answer("(e)", "Undo the operations in reverse order: y(t) = x(−2t + 6) ⇒ x(t) = y((6 − t)/2) = y(−t/2 + 3). Recipe on y: "
         "shift left by 3, reverse, stretch by 2. Every feature of y at t = b goes to t = 6 − 2b.")
for k in [("2022-23", "CSE 219", "7(a)–(c)"), ("2023-24", "CSE 219", "1(a)"), ("2022-23", "CSE 219", "7(d)"),
          ("2010-11", "EEE 301", "5(b)(ii)")]:
    mark(*k)
mark("2016-17", "EEE 211", "5(b)", "◐ Method"); mark("2011-12", "EEE 301", "6(d)", "◐ Method")

# ====================================================================== Lesson 3
n.lesson("Lesson 3 — Even and Odd Decomposition", "Slides 40–52 (Lec 1)")
n.h2("1. Definitions (sl. 41–44)")
n.bullets(["Even: x(−t) = x(t) (mirror about the vertical axis), e.g. cos t.",
           "Odd: x(−t) = −x(t) (point symmetry about the origin), e.g. sin t. An odd signal has x(0) = 0."])
n.formula(["x_e(t) = ½[x(t) + x(−t)]          x_o(t) = ½[x(t) − x(−t)]", "x(t) = x_e(t) + x_o(t)"])
n.p("Checks (sl. 44): x_e(−t) = ½[x(−t) + x(t)] = x_e(t); x_o(−t) = ½[x(−t) − x(t)] = −x_o(t); adding them gives x(t). "
    "The same formulas hold in DT with n in place of t.")
n.h2("2. Worked Examples (sl. 45–52)")
n.p("x(t) = t + 1 on −1 ≤ t ≤ 1: x(−t) = 1 − t, so x_e = ½[(t+1) + (1−t)] = 1 and x_o = ½[(t+1) − (1−t)] = t, both on "
    "|t| ≤ 1.")
n.p("DT step x[n] = u[n]: x_e[n] = ½ for n ≠ 0 and 1 at n = 0; x_o[n] = −½ (n < 0), 0 (n = 0), ½ (n > 0).")
n.figure_from_pdf(A[1], 48, "Figure 3.1 — Odd part of x(t) = t + 1 on [−1, 1] is x_o(t) = t (Lec 1, sl. 48)",
                  clip=CLIP, width_cm=10)
n.callout("memorize", "Useful facts: even × even = even, odd × odd = even, even × odd = odd. ∫_{−a}^{a} odd = 0. "
          "The area of x_e equals the area of x (the odd part adds zero area). x_e(0) = x(0), x_o(0) = 0.")
n.callout("trap", "Work interval by interval: x(−t) has its pieces on the mirrored intervals, so on each sub-interval "
          "you must combine the correct piece of x(t) with the correct piece of x(−t) (one of them may be 0). "
          "Do not just replace t by −t inside one formula.")
n.exam_approach(["Write x(t) piecewise and list all break points ±a.",
                 "Write x(−t) piecewise (mirror the intervals, replace t by −t in each formula).",
                 "Cut the axis at all break points of both and compute ½(x ± x(−t)) on each piece.",
                 "Sketch: x_e must be mirror-symmetric, x_o must be point-symmetric — use this as a check."])
fx = lambda s: pw(s, [(-2, 0, lambda u: u + 1), (0, 2.0001, lambda u: -u / 2 + 1)])
sk5a = sketch("anik1_q5a", [
    dict(title="f(t) and f(−t)", curves=[(tt, fx(tt), "f(t)"), (tt, fx(-tt), "f(−t)")], xlim=(-3, 3), legend=True,
         xticks=range(-3, 4)),
    dict(title="f_e(t) = 1 − 3|t|/4", curves=[(tt, (fx(tt) + fx(-tt)) / 2)], xlim=(-3, 3), xticks=range(-3, 4)),
    dict(title="f_o(t) = t/4", curves=[(tt, (fx(tt) - fx(-tt)) / 2)], xlim=(-3, 3), xticks=range(-3, 4))], ncols=3)
n.practice("Lesson 3",
           "(a) Actual — CSE 219 2022-23 Q5(a). (b) Actual — EEE 301 2014-15 Q1(c). (c) Actual — EEE 301 2010-11 Q5(a)(ii).",
           ["(a) f(t) = t + 1 (−2 ≤ t ≤ 0), −t/2 + 1 (0 < t ≤ 2), 0 elsewhere. (i) Draw f(t). (ii) Find its even–odd "
            "decomposition using the definitions. (iii) Draw both parts. (3 + 6 + 6)",
            "(b) x(t) = −t + 1 (−1 ≤ t < 0), t (0 ≤ t < 2), 2 (2 ≤ t < 3), 0 otherwise. Find the odd and even parts "
            "and their average values. (20)",
            "(c) Find and sketch the odd and even parts of x(t) = A e^{−αt}, t > 0, and 0 otherwise."])
n.solution()
n.answer("(a)", "f(−t) = −t + 1 for 0 ≤ t ≤ 2 and t/2 + 1 for −2 ≤ t < 0.")
n.code(["For 0 < t ≤ 2:  f_e = ½[(−t/2 + 1) + (−t + 1)] = 1 − 3t/4     f_o = ½[(−t/2 + 1) − (−t + 1)] = t/4",
        "For −2 ≤ t < 0: f_e = ½[(t + 1) + (t/2 + 1)] = 1 + 3t/4     f_o = ½[(t + 1) − (t/2 + 1)] = t/4",
        "",
        "f_e(t) = 1 − 3|t|/4,  |t| ≤ 2  (0 elsewhere)        f_o(t) = t/4,  |t| ≤ 2  (0 elsewhere)",
        "Check: f_e + f_o at t = 1 → 1/4 + 1/4 = 1/2 = −1/2 + 1 ✓;  at t = −1 → 1/4 − 1/4 = 0 = −1 + 1 ✓"])
n.figure_image(sk5a, "Figure 3.2 — CSE 219 2022-23 Q5(a): f(t), its even part (a ‘tent’) and its odd part (a line)",
               width_cm=16.5)
n.answer("(b)", "x(−t) = t + 1 on (0, 1], −t on (−2, 0], 2 on (−3, −2]. Combining interval by interval:")
n.code(["interval     x(t)    x(−t)    x_e = ½(x + x(−t))    x_o = ½(x − x(−t))",
        "(−3,−2)       0       2         1                    −1",
        "(−2,−1)       0      −t        −t/2                   t/2",
        "(−1, 0)     −t+1     −t        −t + 1/2               1/2",
        "( 0, 1)       t      t+1        t + 1/2              −1/2",
        "( 1, 2)       t       0         t/2                   t/2",
        "( 2, 3)       2       0         1                     1"])
n.p("Average values over the support (−3, 3): the odd part averages to **0** (odd function on a symmetric interval). "
    "The even part has the same area as x: ∫x = 1.5 + 2 + 2 = 5.5, so its average is 5.5/6 ≈ **0.917**. (Over all time "
    "both averages are 0, because the signal has finite duration.)")
n.answer("(c)", "x_e(t) = (A/2) e^{−α|t|} (all t); x_o(t) = (A/2) e^{−αt} for t > 0 and −(A/2) e^{αt} for t < 0, i.e. "
         "(A/2) sgn(t) e^{−α|t|}. At t = 0: x_e = A/2 (taking x(0) = A/2), x_o = 0.")
mark("2022-23", "CSE 219", "5(a)"); mark("2014-15", "EEE 301", "1(c)"); mark("2010-11", "EEE 301", "5(a)(ii)")

# ====================================================================== Lesson 4
n.lesson("Lesson 4 — Unit Step, Unit Impulse, Ramp and Signals Built from Them",
         "Slides 2–29 (Lec 2) · ramp, impulse scaling and δ′(t) are textbook background")
n.h2("1. Discrete-Time Step and Impulse (sl. 3–15)")
n.formula(["u[n] = 1 (n ≥ 0), 0 (n < 0)        δ[n] = 1 (n = 0), 0 (n ≠ 0)"])
n.bullets(["R1 — first difference: δ[n] = u[n] − u[n − 1] (sl. 11).",
           "R2 — running sum: u[n] = Σ_{m=−∞}^{n} δ[m] — the spike at m = 0 is included only when n ≥ 0 (sl. 12–13).",
           "R3 — sum of delayed impulses: u[n] = Σ_{k=0}^{∞} δ[n − k] (sl. 14–15).",
           "Values: u[1] = 1, u[−3] = 0, u[0] = 1; δ[0] = 1, δ[4] = δ[−2] = 0 (sl. 7–8). u[n − 2] starts at n = 2, u[n + 3] "
           "at n = −3 (sl. 9–10)."])
n.h2("2. Continuous-Time Step and Impulse (sl. 16–27)")
n.p("u(t) = 0 for t < 0, 1 for t > 0 (the value at t = 0 does not matter). The impulse should be the derivative of the "
    "step, but u(t) has no ordinary derivative at the jump. Fix (sl. 20–25): replace the jump by a short ramp u_Δ(t) "
    "rising from 0 to 1 over [0, Δ]. Its derivative δ_Δ(t) is a pulse of height 1/Δ and width Δ — area 1 for every Δ. "
    "As Δ → 0 the pulse becomes the ideal impulse:")
n.formula(["δ(t) = du(t)/dt          u(t) = ∫_{−∞}^{t} δ(τ) dτ          ∫ δ(t) dt = 1"])
n.figure_from_pdf(A[2], 25, "Figure 4.1 — δ(t) is the limit of unit-area pulses δ_Δ(t) as Δ → 0 (Lec 2, sl. 25)",
                  clip=CLIP, width_cm=10)
n.p("Arrow notation (sl. 26): the number beside the arrow is the **area (strength)**, not the height; 2δ(t − 1) is an "
    "arrow of strength 2 at t = 1, −3δ(t − 3) points down. d/dt[2u(t)] = 2δ(t) (sl. 27).")
n.h2("3. Signals Made of Steps; Derivatives at Jumps (sl. 28–29)")
n.p("Read the jumps from left to right: x(t) jumps +2 at t = 1, −3 at t = 2 and +2 at t = 4, so")
n.code(["x(t) = 2u(t−1) − 3u(t−2) + 2u(t−4)",
        "dx/dt = 2δ(t−1) − 3δ(t−2) + 2δ(t−4)     (each jump → an impulse equal to the jump height)"])
n.figure_from_pdf(A[2], 29, "Figure 4.2 — Derivative of a jump signal: upward jumps give positive impulses (Lec 2, sl. 29)",
                  clip=CLIP, width_cm=10)
n.h2("4. Ramp and More Impulse Rules (textbook)")
n.table(["Rule", "Statement"],
        [["Ramp", "r(t) = t u(t) = ∫_{−∞}^{t} u(τ)dτ;  dr/dt = u(t)"],
         ["Sampling (product)", "x(t) δ(t − a) = x(a) δ(t − a)"],
         ["Sifting", "∫_{L}^{R} x(t) δ(t − a) dt = x(a) if L < a < R, 0 if a is outside (Lec 6, sl. 45–51)"],
         ["Scaling", "δ(at + b) = (1/|a|) δ(t + b/a);  δ(−t) = δ(t) (even)"],
         ["Composite", "δ(f(t)) = Σ δ(t − tᵢ)/|f′(tᵢ)| over the simple zeros tᵢ of f"],
         ["Doublet", "∫ x(t) δ′(t − a) dt = −x′(a);  δ′ is odd: δ′(−t) = −δ′(t)"],
         ["Building blocks", "slope change of m at t = a → m·r(t − a); jump of J at t = a → J·u(t − a)"]],
        widths_cm=[3.6, 13.6])
n.p("**Model of δ(t)** (needed in EEE 2022-23 Q6(a), 2013-14 Q1(b)): a family p_ε(t) represents δ(t) as ε → 0 if (1) its "
    "area is 1 for every ε, (2) p_ε(t) → 0 for every t ≠ 0, and (3) it becomes infinitely tall at t = 0 (all the area "
    "concentrates at the origin).")
n.callout("memorize", "Piecewise linear signal → elementary signals: scan left to right; at each break point add "
          "(new slope − old slope)·r(t − a) and (jump)·u(t − a). Derivative: replace r by u and u by δ.")
n.callout("trap", "• u(3t) = u(t) and u(−2t) = u(−t): scaling a step by a positive number changes nothing. "
          "• δ(3t − k) = (1/3)δ(t − k/3), not δ(t − k/3). • Impulses at a jump are part of the derivative — the "
          "answer “slope only” loses most of the marks.")
n.exam_approach(["Tabulate break points, slopes and jumps from the figure.",
                 "Write x(t) = Σ (slope changes)·r(t − a) + Σ (jumps)·u(t − a); check two values.",
                 "Derivative: piecewise slopes (rectangles) + impulses of strength = jump; second derivative: impulses at "
                 "slope changes.",
                 "Impulse integrals: find where the argument of δ is zero, scale by 1/|a|, check the point is inside the "
                 "limits, then sift."])
# EEE 2023-24 1(a)
xe1 = lambda a: pw(a, [(-2, -1, lambda s: s + 2), (-1, 0, lambda s: -s), (0, 2, lambda s: s),
                       (2, 3, lambda s: 2 + 0 * s), (3, 4.0001, lambda s: 8 - 2 * s)])
dxe1 = lambda a: pw(a, [(-2, -1, lambda s: 1 + 0 * s), (-1, 0, lambda s: -1 + 0 * s), (0, 2, lambda s: 1 + 0 * s),
                        (3, 4, lambda s: -2 + 0 * s)])
tt2 = T(-3, 5, 3201)
skE1 = sketch("anik1_eee2324_1a", [
    dict(title="x(t)", curves=[(tt2, xe1(tt2))], xlim=(-3, 5), xticks=range(-2, 5)),
    dict(title="x(−3t+2)", curves=[(tt2, xe1(-3 * tt2 + 2))], xlim=(-1, 1.5),
         xticks=[-2 / 3, -1 / 3, 0, 2 / 3, 1, 4 / 3]),
    dict(title="x′(t)  (no jumps → no impulses)", curves=[(tt2, dxe1(tt2))], xlim=(-3, 5), xticks=range(-2, 5)),
    dict(title="x″(t)", impulses=[(-2, 1), (-1, -2), (0, 2), (2, -1), (3, -2), (4, 2)], xlim=(-3, 5), ylim=(-2.8, 2.8),
         xticks=range(-2, 5))], ncols=2)
n.practice("Lesson 4",
           "(a) Actual — EEE 211 2023-24 Q1(a). (b) Actual — EEE 211 2022-23 Q5(c). (c) Actual — EEE 211 2020-21 Q5(a). "
           "(d) Actual — EEE 211 2019-20 Q5(a).",
           ["(a) x(t) is a triangle from (−2, 0) up to (−1, 1) and down to (0, 0), then a ramp from (0, 0) to (2, 2), flat at 2 "
            "until t = 3, and a line down to 0 at t = 4. (i) Draw x(−3t + 2), x′(t), x″(t). (ii) Express x′(t) using "
            "δ(t), u(t), r(t). (11)",
            "(b) x(t) = 5t on (0, 1), −6 on (1, 2), 5(t − 2) on (2, 3), 0 elsewhere. Write x(t) as a combination of "
            "elementary signals and sketch dx/dt. (10)",
            "(c) x₁(t): ramp from 0 to 2 on [0, 2], then 2 until t = 6. x₂(t): ramp from 0 at t = −4 to 2 at t = −2, 2 until "
            "t = 2, 3 on (2, 4). x₃(t): rises from 0 at t = −3 to 4 at t = −2, stays 4 until t = 0, then 1 until t = 2, then "
            "falls to 0 at t = 3. (i) Express x₁, x₂ with r and u. (ii) Draw x₁(t + 2)r(t − 2) and x₂(t − 2)u(−2t). "
            "(iii) Express x₃ in terms of x₁. (10 + 10 + 5)",
            "(d) x(t) = 2 on (−1.5, 0), 2e^{−t/2} on (0, 3), 0 elsewhere. Describe x(t) by a single expression valid for "
            "all t and sketch x(3t). (15)"])
n.solution()
n.code(["(a) x(t) = t+2 [−2,−1];  −t [−1,0];  t [0,2];  2 [2,3];  8−2t [3,4];  0 otherwise",
        "(i) x(−3t+2): a feature at a goes to t = (2 − a)/3:",
        "    a = 4,3,2,0,−1,−2  →  t = −2/3, −1/3, 0, 2/3, 1, 4/3   with values 0, 2, 2, 0, 1, 0",
        "    x(−3t+2) = 6t+4 [−2/3,−1/3];  2 [−1/3,0];  2−3t [0,2/3];  3t−2 [2/3,1];  4−3t [1,4/3]",
        "    x′(t) = 1 (−2,−1);  −1 (−1,0);  1 (0,2);  0 (2,3);  −2 (3,4)       (continuous x ⇒ no impulses)",
        "    x″(t) = δ(t+2) − 2δ(t+1) + 2δ(t) − δ(t−2) − 2δ(t−3) + 2δ(t−4)",
        "(ii) x′(t) = u(t+2) − 2u(t+1) + 2u(t) − u(t−2) − 2u(t−3) + 2u(t−4)",
        "     [equivalently x(t) = r(t+2) − 2r(t+1) + 2r(t) − r(t−2) − 2r(t−3) + 2r(t−4)]"])
n.figure_image(skE1, "Figure 4.3 — EEE 211 2023-24 Q1(a): x(t), x(−3t+2), x′(t) and x″(t)", width_cm=14)
xb5 = lambda s: pw(s, [(0, 1, lambda u: 5 * u), (1, 2, lambda u: -6 + 0 * u), (2, 3, lambda u: 5 * (u - 2))])
skb5 = sketch("anik1_eee2223_5c", [
    dict(title="x(t)", curves=[(tt2, xb5(tt2))], xlim=(-1, 4), xticks=range(-1, 5)),
    dict(title="dx/dt", curves=[(tt2, pw(tt2, [(0, 1, lambda u: 5 + 0 * u), (2, 3, lambda u: 5 + 0 * u)]))],
         impulses=[(1, -11), (2, 6), (3, -5)], xlim=(-1, 4), ylim=(-13, 9), xticks=range(-1, 5))], ncols=2)
n.code(["(b) Scan left to right: slope 5 starts at 0; at t = 1 slope 5 → 0 and jump 5 → −6 (−11);",
        "    at t = 2 jump −6 → 0 (+6) and slope 0 → 5; at t = 3 slope 5 → 0 and jump 5 → 0 (−5).",
        "    x(t) = 5r(t) − 5r(t−1) − 11u(t−1) + 6u(t−2) + 5r(t−2) − 5r(t−3) − 5u(t−3)",
        "    dx/dt = 5[u(t) − u(t−1)] + 5[u(t−2) − u(t−3)] − 11δ(t−1) + 6δ(t−2) − 5δ(t−3)"])
n.figure_image(skb5, "Figure 4.4 — EEE 211 2022-23 Q5(c): x(t) and dx/dt (rectangles of height 5 plus three impulses)",
               width_cm=12)
x1c = lambda s: pw(s, [(0, 2, lambda u: u), (2, 6, lambda u: 2 + 0 * u)])
x2c = lambda s: pw(s, [(-4, -2, lambda u: u + 4), (-2, 2, lambda u: 2 + 0 * u), (2, 4, lambda u: 3 + 0 * u)])
tt3 = T(-6, 8, 2801)
skc = sketch("anik1_eee2021_5a", [
    dict(title="x₁(t+2)·r(t−2)", curves=[(tt3, x1c(tt3 + 2) * np.maximum(tt3 - 2, 0))], xlim=(-1, 6),
         xticks=range(-1, 7)),
    dict(title="x₂(t−2)·u(−2t)", curves=[(tt3, x2c(tt3 - 2) * (tt3 < 0))], xlim=(-4, 3), xticks=range(-4, 4))],
    ncols=2)
n.code(["(c)(i)  x₁(t) = r(t) − r(t−2) − 2u(t−6)",
        "        x₂(t) = r(t+4) − r(t+2) + u(t−2) − 3u(t−4)",
        "(ii) x₁(t+2) = ramp on [−2,0], 2 on [0,4];  r(t−2) = t−2 for t ≥ 2  ⇒ product = 2(t−2) on [2,4], 0 elsewhere",
        "     x₂(t−2) = ramp 0→2 on [−2,0], 2 on [0,4], 3 on [4,6];  u(−2t) = u(−t) keeps t < 0  ⇒ product = t+2 on [−2,0]",
        "(iii) Left part (ramp over 1 unit to 4, flat 2 units) = 2·x₁(2(t+3)) = 2x₁(2t+6)",
        "      Right part (1 on [0,2], ramp down to 0 at 3) = ½·x₁(−2(t−3)) = ½x₁(6−2t)",
        "      x₃(t) = 2x₁(2t+6) + ½x₁(6−2t)     check: t = −1 → 2·2 + 0 = 4;  t = 2.5 → 0 + ½·1 = 0.5 ✓"])
n.figure_image(skc, "Figure 4.5 — EEE 211 2020-21 Q5(a)(ii): the two products", width_cm=12)
xd = lambda s: pw(s, [(-1.5, 0, lambda u: 2 + 0 * u), (0, 3, lambda u: 2 * np.exp(-u / 2))])
skd = sketch("anik1_eee1920_5a", [
    dict(title="x(t)", curves=[(tt3, xd(tt3))], xlim=(-2, 4), xticks=[-1.5, 0, 1, 2, 3]),
    dict(title="x(3t): compressed by 3", curves=[(tt3, xd(3 * tt3))], xlim=(-2, 4), xticks=[-0.5, 0, 1, 2, 3])],
    ncols=2)
n.code(["(d) x(t) = 2[u(t+1.5) − u(t)] + 2e^{−t/2}[u(t) − u(t−3)]",
        "    x(3t) = 2[u(t+0.5) − u(t)] + 2e^{−3t/2}[u(t) − u(t−1)]     (break points −1.5, 0, 3 → −0.5, 0, 1)"])
n.figure_image(skd, "Figure 4.6 — EEE 211 2019-20 Q5(a): x(t) and x(3t)", width_cm=12)
for k in [("2023-24", "EEE 211", "1(a)"), ("2022-23", "EEE 211", "5(c)"), ("2020-21", "EEE 211", "5(a)"),
          ("2019-20", "EEE 211", "5(a)")]:
    mark(*k)

n.practice("Lesson 4 (continued)",
           "(e) Actual — EEE 211 2022-23 Q6(a) and EEE 301 2013-14 Q1(b). (f) Actual — CSE 311 2019-20 Q2(b) and 2012-13 "
           "Q5(a). (g) Actual — EEE 211 2021-22 Q1(c). (h) Actual — EEE 301 2015-16 Q2(a), 2011-12 Q6(c), 2012-13 Q1(b).",
           ["(e) Check whether p₁(t) = lim_{ε→0} 1/(επ cosh(t/ε)) and p₂(t) = lim_{ε→0} (1/π) sin(εt)/t can be used as models "
            "of δ(t). Same for (1/π) ε/(t² + ε²). (20)",
            "(f) Prove that a unit step can be derived from a unit impulse and vice versa. Define the unit impulse and "
            "derive its sampling property. (11; 8)",
            "(g) x(t) = δ(t − 1) + u(t)u(t − 3) + u(cos t). Compute y(t) = ∫ x(τ)dτ and sketch y(t/2). (15)",
            "(h) Evaluate: ∫(t² + 3t + 2)δ(−1 − t)dt; ∫e^{t−1} sin{π(t−5)/2} δ(t + 3)dt; ((jω+2)/(ω²+9))δ(ω); "
            "δ(ω−3)/(jω+2); ∫_{−5}^{5} u₂(1 − τ)cos 2πτ dτ with u₂ = d²u/dt²; ∫e^{−5t+1}δ′(t − 5)dt. Also: is "
            "Σ_{k=−4}^{4} δ(3t − k) sin²(πt/3) a power or an energy signal?"])
n.solution()
n.answer("(e)", "Test the three conditions. p₁: substitute u = t/ε: ∫ dt/(επ cosh(t/ε)) = (1/π)∫ du/cosh u = (1/π)·π = 1 for "
         "every ε. For t ≠ 0, cosh(t/ε) ≈ ½e^{|t|/ε} → ∞ much faster than 1/ε grows, so p₁ → 0; p₁(0) = 1/(επ) → ∞. "
         "**p₁ is a valid model of δ(t).** p₂: area ∫ sin(εt)/(πt) dt = 1 for every ε > 0, but as ε → 0, sin(εt)/(πt) → 0 "
         "for every t (even the peak ε/π → 0) — the unit area spreads over a main lobe of width 2π/ε → ∞. **p₂ is not a "
         "model as ε → 0** (it does become δ(t) as ε → ∞). Lorentzian (1/π)ε/(t² + ε²): area (1/π)[tan⁻¹(t/ε)]_{−∞}^{∞} = 1; "
         "→ 0 for t ≠ 0; peak 1/(πε) → ∞ ⇒ **valid model**.")
n.answer("(f)", "Define δ(t) as the limit of the unit-area pulse δ_Δ(t) (height 1/Δ on [0, Δ]) as Δ → 0: δ(t) = 0 for t ≠ 0 "
         "and ∫δ = 1. (i) Step from impulse: u(t) = ∫_{−∞}^{t} δ(τ)dτ — for t < 0 the integration window does not "
         "contain the impulse (0), for t > 0 it does (1). (ii) Impulse from step: the smoothed step u_Δ rises from 0 to 1 "
         "over [0, Δ]; its derivative is δ_Δ, so δ(t) = lim du_Δ/dt = du/dt (in the generalized sense). Sampling "
         "property: since δ(t − a) = 0 except at t = a, x(t)δ(t − a) = x(a)δ(t − a); integrating, ∫x(t)δ(t − a)dt = "
         "x(a)∫δ(t − a)dt = x(a). (Rigorous version: ∫x(t)δ_Δ(t − a)dt = (1/Δ)∫_a^{a+Δ}x dt → x(a) for continuous x.)")
n.answer("(g)", "u(t)u(t − 3) = u(t − 3). u(cos t) = 1 whenever cos t > 0, i.e. a square wave of period 2π that is 1 on "
         "(−π/2 + 2kπ, π/2 + 2kπ). Its integral from −∞ diverges, so take the integral from 0 (the printed lower limit is "
         "not legible; state this assumption):")
n.code(["y(t) = ∫₀^t x dτ = u(t−1) + r(t−3) + w(t),   t ≥ 0",
        "w(t) = ∫₀^t u(cos τ)dτ:  t on [0, π/2];  π/2 on [π/2, 3π/2];  π/2 + (t − 3π/2) on [3π/2, 5π/2]; …",
        "       (a staircase-ramp rising with slope 1 for half of each period, average slope 1/2)",
        "y(t/2): replace t by t/2 — every break point doubles (1 → 2, 3 → 6, π/2 → π, 3π/2 → 3π, …)"])
n.answer("(h)", "Results:")
n.code(["∫(t²+3t+2)δ(−1−t)dt = (t²+3t+2)|_{t=−1} = 1 − 3 + 2 = 0          [δ(−1−t) = δ(t+1)]",
        "∫e^{t−1} sin{π(t−5)/2} δ(t+3)dt = e^{−4} sin(−4π) = 0",
        "((jω+2)/(ω²+9)) δ(ω) = (2/9) δ(ω);       δ(ω−3)/(jω+2) = δ(ω−3)/(2 + j3)",
        "∫_{−5}^{5} δ′(1−τ) cos2πτ dτ = −∫δ′(τ−1)cos2πτ dτ = +d/dτ[cos2πτ]_{τ=1} = −2π sin 2π = 0",
        "∫e^{−5t+1} δ′(t−5) dt = −d/dt[e^{−5t+1}]_{t=5} = 5e^{−24}",
        "Σ_{k=−4}^{4} δ(3t−k) sin²(πt/3) = Σ (1/3) sin²(πk/9) δ(t − k/3): 8 nonzero impulses (k = 0 vanishes).",
        "  Each impulse has finite area but |δ|² is not integrable → E = ∞; with a finite number of impulses the",
        "  time-average P = lim E/2T is not finite either → neither (state the reason)."])
for k in [("2022-23", "EEE 211", "6(a)"), ("2013-14", "EEE 301", "1(b)"), ("2019-20", "CSE 311", "2(b)"),
          ("2012-13", "CSE 311", "5(a)"), ("2021-22", "EEE 211", "1(c)"), ("2015-16", "EEE 301", "2(a)"),
          ("2011-12", "EEE 301", "6(c)")]:
    mark(*k)
for k in [("2012-13", "EEE 301", "1(b)"), ("2014-15", "EEE 301", "1(b)"), ("2017-18", "EEE 211", "5(b)"),
          ("2018-19", "EEE 211", "6(b)"), ("2016-17", "EEE 211", "5(a)"), ("2010-11", "EEE 301", "5(b)(i)")]:
    mark(*k, "◐ Method")

# ====================================================================== Lesson 5
n.lesson("Lesson 5 — Exponentials, Sinusoids and Periodicity", "Slides 30–50 (Lec 2)")
n.h2("1. Real Exponentials and the Step as a Switch (sl. 31–35)")
n.p("x(t) = Ce^{at}: grows (a > 0), constant (a = 0), decays (a < 0). Multiplying by u(t) keeps only the part t > 0; "
    "u(t − 2) switches on at t = 2; u(3 − t) keeps t < 3; u(−t) keeps t < 0.")
n.code(["e^{t}u(−t): rising exponential, ends at 1 at t = 0     e^{−t}u(t−2): starts at e^{−2} at t = 2",
        "e^{t}u(3−t): grows until t = 3, then 0                   e^{−t}u(3t) = e^{−t}u(t)"])
n.h2("2. Sinusoids and Complex Exponentials (sl. 36–42)")
n.formula(["x(t) = A cos(ω0t + φ),   T0 = 2π/|ω0|          e^{jθ} = cos θ + j sin θ",
           "cos θ = (e^{jθ} + e^{−jθ})/2          sin θ = (e^{jθ} − e^{−jθ})/2j"])
n.p("e^{jω0t} is a point rotating around the unit circle; cos and sin are its horizontal and vertical coordinates. "
    "A real cosine is two opposite rotations whose imaginary parts cancel (sl. 41). Period: e^{jω0T} = 1 ⇒ ω0T = 2π.")
n.h2("3. Discrete-Time Periodicity (sl. 43–50)")
n.p("x[n] = cos(ω0n + φ) is periodic only if some integer N satisfies ω0N = 2πm. So **2π/ω0 must be rational**: "
    "write 2π/ω0 = N/m in lowest terms; the fundamental period is N (after m cycles of the underlying cosine).")
n.table(["Signal", "2π/ω0", "Result"],
        [["cos(2t) (CT)", "—", "periodic, T0 = π"],
         ["cos(2n)", "π (irrational)", "not periodic"],
         ["cos(2πn/5)", "5", "N = 5"],
         ["3 sin(5n/7)", "14π/5 (irrational)", "not periodic"],
         ["2 cos(16πn/63 + π/3)", "63/8", "N = 63 (8 cycles of the cosine)"]],
        widths_cm=[5.5, 4.5, 7.2])
n.figure_from_pdf(A[2], 45, "Figure 5.1 — cos(2t) repeats every π, but cos(2n) never repeats: π is not an integer "
                  "shift (Lec 2, sl. 45)", clip=CLIP, width_cm=10)
n.h2("4. Sums of Periodic Signals (textbook)")
n.p("x₁ + x₂ (periods T₁, T₂) is periodic iff T₁/T₂ is rational; then T = LCM(T₁, T₂). Equivalently ω₁/ω₂ rational and "
    "ω0 = GCD(ω₁, ω₂). For DT sums: N = LCM(N₁, N₂) always exists if each part is periodic. Phase shifts never change a "
    "period. Powers and products: expand into sums of sinusoids first (sin²θ = (1 − cos 2θ)/2).")
n.callout("trap", "• The phase of a DT sinusoid does not affect periodicity (sl. 49). • In DT, ω0 = 2π·(m/N) gives "
          "period N, not 2π/ω0 (63/8 is not a period). • √(e^{j5πt}) = e^{j5πt/2}: halve the frequency. • An impulse "
          "train δ(t − kπ) has period π, u(cos t) has period 2π.")
n.exam_approach(["Rewrite everything as a sum of sinusoids / complex exponentials (expand squares and products).",
                 "CT: list the periods Tᵢ = 2π/ωᵢ; check every ratio is rational; T = LCM.",
                 "DT: for each term check 2π/ωᵢ = N/m rational; Nᵢ = numerator; N = LCM(Nᵢ).",
                 "Write the conclusion with the reason (“ratio is irrational ⇒ not periodic”)."])
n.practice("Lesson 5",
           "(a) Actual — CSE 219 2022-23 Q5(c). (b) Actual — CSE 219 2023-24 Q3(a). (c) Actual — EEE 211 2021-22 Q1(a). "
           "(d) Older papers, quick answers (EEE 211 2017-18 Q5(a), 2016-17 Q5(c); EEE 301 2015-16 Q1(a), 2014-15 Q1(a), "
           "2013-14 Q1(a), 2012-13 Q1(a), 2011-12 Q6(a), 2010-11 Q5(a)(i)).",
           ["(a) Is x[n] = 2cos(16πn/63 + π/3) periodic? Explain. (5)",
            "(b) x[n] = (3 − 4j)e^{j13πn/7}. (i) Are the real and imaginary parts periodic? Fundamental period? (ii) Can "
            "the phase shift in each part be interpreted as an integer time shift of a cosine sequence? (15)",
            "(c) Is x(t) = √(e^{j5πt}) + sin²(3t − π/4) periodic? If so, find the period. (10)",
            "(d) Periodic? Period? (i) [2cos(0.6√π t + π/6) + sin(1.2√π t − π/3)]²; (ii) cos(100πt + π/3) + sin(40πt + 2π/3); "
            "(iii) 3cos(4t + π/3), [cos(2t − π/3)]², Σ_{n=−7}^{7} e^{−(2t−n)}, e^{j(πt−1)}; (iv) u(cos t) − δ(t − kπ); "
            "(v) 4cos πt − sin(3πt + π/2) and 4cos 2t + 4cos 2πt; (vi) αδ(sin t) + (1 − α)δ(t − kπ), k odd, 0 < α < 1; "
            "(vii) e^{j7πt/6} + e^{j5πt/6}; (viii) cos(πt/3) + sin(πt/4)."])
n.solution()
n.answer("(a)", "ω0 = 16π/63, 2π/ω0 = 63/8 = N/m with N = 63, m = 8 (rational). **Periodic, N₀ = 63**: after 63 samples "
         "the angle advances by 16π = 8 full turns. The phase π/3 does not matter.")
n.answer("(b)", "3 − 4j = 5e^{−jθ}, θ = tan⁻¹(4/3) = 0.9273 rad. x[n] = 5e^{j(13πn/7 − θ)}, so Re x = 5cos(13πn/7 − θ), "
         "Im x = 5sin(13πn/7 − θ). (i) 2π/ω0 = 2π/(13π/7) = 14/13 → rational, N = 14 (13 cycles). Both parts are "
         "periodic with **N₀ = 14**. (ii) A time shift n₀ turns cos(13πn/7) into cos(13π(n − n₀)/7), a phase of −13πn₀/7, "
         "which is always a multiple of π/7 (mod 2π). θ = 0.9273 rad = 2.066·(π/7) is not a multiple of π/7 (in fact "
         "θ/π is irrational, since cos θ = 3/5 is rational but not 0, ±½, ±1). So **no**: the phase cannot be produced "
         "by an integer shift — it can only be read as a shift of the underlying CT cosine.")
n.answer("(c)", "√(e^{j5πt}) = e^{j5πt/2} (principal root): period 2π/(5π/2) = 4/5. sin²(3t − π/4) = ½ − ½cos(6t − π/2): "
         "period π/3. Ratio (4/5)/(π/3) = 12/(5π) is irrational ⇒ **not periodic**.")
n.code(["(d)(i)   periods 10√π/3 and 5√π/3 (ratio 2); the square contains 0.6√π·{1,2,3,4} ⇒ T = 10√π/3 ≈ 5.91",
        "(ii)    T₁ = 1/50, T₂ = 1/20 ⇒ T = LCM = 0.1 s",
        "(iii)   π/2;  π/2 (cos² = ½ + ½cos(4t − 2π/3));  e^{−2t}·const → not periodic;  T = 2",
        "(iv)    u(cos t): 2π;  impulse train: π  ⇒ T = 2π",
        "(v)     T = 2 and 2/3 ⇒ T = 2;    π and 1 (ratio π irrational) ⇒ not periodic",
        "(vi)    δ(sin t) = Σ_k δ(t − kπ) (|cos kπ| = 1) ⇒ weight α at even multiples of π, α + (1−α) = 1 at odd",
        "        multiples ⇒ periodic, T = 2π (α ≠ 1). For α = 0.5: ½ at 0, ±2π…; 1 at ±π, ±3π…",
        "(vii)   ω₀ = GCD(7π/6, 5π/6) = π/6 ⇒ T = 12",
        "(viii)  T₁ = 6, T₂ = 8 ⇒ T = 24"])
for k in [("2022-23", "CSE 219", "5(c)"), ("2023-24", "CSE 219", "3(a)"), ("2021-22", "EEE 211", "1(a)"),
          ("2017-18", "EEE 211", "5(a)"), ("2016-17", "EEE 211", "5(c)"), ("2015-16", "EEE 301", "1(a)"),
          ("2014-15", "EEE 301", "1(a)"), ("2013-14", "EEE 301", "1(a)"), ("2012-13", "EEE 301", "1(a)"),
          ("2011-12", "EEE 301", "6(a)"), ("2010-11", "EEE 301", "5(a)(i)")]:
    mark(*k)

# ====================================================================== quick notes
n.quick_notes(
    "Quick Notes — Signals", "Revision points for Lessons 1–5.",
    [("L1 · Energy and Power", [
        "E = ∫|x|²dt (Σ|x[n]|²); P = E / interval length; P∞ = lim (1/2T)∫_{−T}^{T}|x|².",
        "Energy signal: E finite, P = 0. Power signal: P finite, E = ∞. Neither: both infinite.",
        "Periodic → power, average one period. A cos(ω0t + φ): P = A²/2; Ae^{jω0t}: P = |A|².",
        "Half-sine E = π/2; 1 (|t| ≤ 1), 1/|t| beyond: E = 4."]),
     ("L2 · Transformations", [
         "x(t − t0) delay (right); x(t + t0) advance (left); x(−t) mirror; x(αt) compress (α > 1).",
         "Recipe for x(αt + β): shift by β → reverse if α < 0 → scale by |α|. Name each intermediate signal.",
         "Feature at a moves to t = (a − β)/α. x(2t + 3) ≠ x(2(t + 3)).",
         "2022-23 Q7: x(−2t+2) = t [0,1], 1 [1,1.5], 3 − 2t (1.5,2]; x(−t/2+1) = ½ + t/4 [−2,2], 1 [2,4], 2 − t/2 (4,6]."]),
     ("L3 · Even and Odd", [
         "x_e = ½[x(t) + x(−t)], x_o = ½[x(t) − x(−t)]; work interval by interval.",
         "x = t+1 on [−1,1] → x_e = 1, x_o = t. u[n] → x_e = ½ (1 at 0), x_o = ±½.",
         "2022-23 Q5(a): f_e = 1 − 3|t|/4, f_o = t/4 on |t| ≤ 2."]),
     ("L4 · Step, Impulse, Ramp", [
         "δ[n] = u[n] − u[n−1]; u[n] = Σ_{m≤n} δ[m] = Σ_{k≥0} δ[n−k]. δ(t) = du/dt; u(t) = ∫_{−∞}^{t} δ.",
         "Jump of J at a → Jδ(t − a) in the derivative; slope change m → m·r(t − a) in the signal.",
         "Sifting ∫x δ(t − a) = x(a) only if a is inside the limits; δ(at) = δ(t)/|a|; ∫x δ′(t − a) = −x′(a).",
         "δ model: unit area for all ε, → 0 for t ≠ 0, peak → ∞. sin(εt)/(πt) fails as ε → 0."]),
     ("L5 · Periodicity", [
         "CT: T0 = 2π/|ω0|; sum periodic iff period ratio rational, T = LCM.",
         "DT: periodic iff 2π/ω0 = N/m rational; N = numerator. cos 2n not periodic; 2cos(16πn/63 + π/3): N = 63.",
         "Phase never changes a period. Expand squares/products before deciding."])],
    diagrams=[(A[1], 30, "The x(αt + β) recipe (Lec 1, sl. 30)", CLIP, 10),
              (A[2], 11, "δ[n] = u[n] − u[n − 1] (Lec 2, sl. 11)", CLIP, 10)])
n.save()
save_solved("anik_signals")
print("saved", n.out_path)
