"""Ashraf F4 — Laplace transform (Lec 6–7). Lessons 13–16."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c219 import B, ashraf, exam_map, mark, save_solved  # noqa: E402

CLIP = (0.0, 0.09, 1.0, 0.97)
n = ashraf("Lec 6–7 · Laplace Transform: ROC, Properties, Inverse, LTI Systems", "CSE219_Ashraf_Laplace_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "Laplace questions and their weight"),
              ("Lesson 13 — Definition, ROC and Transforms of Standard Signals", "eigenfunction e^{st}, ROC properties 1–8, two-sided and finite signals"),
              ("Lesson 14 — Inverse Laplace Transform", "Bromwich integral, partial fractions, the ROC picks the signal"),
              ("Lesson 15 — Properties of the Laplace Transform", "shift, scaling, reversal, convolution, derivative, integration, final value"),
              ("Lesson 16 — LTI Systems, Differential Equations, Circuits and Feedback", "H(s), causality/stability from the ROC, ICs, block diagrams"),
              ("Quick Notes — Laplace Transform", "merged revision notes + key diagrams")],
    source_note="Slide numbers are PDF page numbers of 6 - Laplace.pdf (36 pages, “Lec 6”) and 7 - More Laplace.pdf "
                "(28 pages, “Lec 7”); the printed slide number is one less. The slides use the bilateral transform; "
                "the unilateral transform (initial conditions at 0⁻), final-value theorem, circuits and feedback loops are "
                "textbook background (marked) that the EEE papers ask almost every year. Mechanical analogues and "
                "state-space questions are not in these slides and are listed in the Outside Notes tab.")

n.h1("Exam Map — What the TF Papers Ask")
exam_map(n, "Ashraf", range(13, 17))
n.callout("focus", "Laplace is the largest topic of Ashraf Sir's part: 32 marks in CSE 219 2022-23 Q1–Q2 and 35 in 2023-24 Q6, "
          "and 2–3 questions in every EEE paper. Learn: (1) the ROC rules (right-sided: to the right of the rightmost pole …) "
          "and the 'same expression, different ROC, different signal' idea; (2) partial fractions + ROC for the inverse; "
          "(3) solving a differential equation with initial conditions at 0⁻ (ZIR + ZSR); (4) H(s) from block diagrams / "
          "circuits, causal-stable tests from the ROC.")

# ===================================================== L13
n.lesson("Lesson 13 — Definition, ROC and Transforms of Standard Signals", "Lec 6 sl. 4–25")
n.p("For an LTI system with impulse response h, the input e^{st} (any complex s = σ + jω) gives y = H(s)e^{st}, "
    "H(s) = ∫h(t)e^{−st}dt (sl. 5). Generalising to any signal:")
n.formula(["X(s) = ∫_{−∞}^{∞} x(t)e^{−st}dt = F{x(t)e^{−σt}}   (sl. 6–7: Laplace = Fourier of the weighted signal)",
           "s = jω (σ = 0) ⇒ X(jω) = Fourier transform — valid only if the ROC contains the jω-axis"])
n.p("Relation to the Fourier transform (CSE 219 2022-23 Q4(a)): x(t)e^{−σt} has Fourier transform X(σ + jω); a growing "
    "signal such as e^{2t}u(t) has no Fourier transform but has a Laplace transform for σ > 2.")
n.h2("Basic Pairs and Why the ROC Matters (sl. 9–15)")
n.table(["Signal", "X(s)", "ROC"],
        [["e^{−at}u(t)", "1/(s + a)", "Re{s} > −a"],
         ["−e^{−at}u(−t)", "1/(s + a)", "Re{s} < −a"],
         ["3e^{−2t}u − 2e^{−t}u", "(s − 1)/((s+1)(s+2))", "Re{s} > −1"],
         ["e^{−2t}u + e^{−t}cos3t u", "(2s² + 5s + 12)/((s+2)(s²+2s+10))", "Re{s} > −1"],
         ["δ(t) − (4/3)e^{−t}u + (1/3)e^{2t}u", "(s − 1)²/((s+1)(s−2))", "Re{s} > 2"],
         ["e^{−b|t|}, b > 0", "−2b/(s² − b²)", "−b < Re{s} < b"],
         ["δ(t)", "1", "all s"],
         ["u(t)", "1/s", "Re{s} > 0"]],
        widths_cm=[6.2, 6.5, 4.5])
n.callout("memorize", "The algebraic expression alone does not specify the signal: 1/(s + a) is e^{−at}u(t) for Re{s} > −a and "
          "−e^{−at}u(−t) for Re{s} < −a. A transform = expression + ROC. The ROC is the set of σ for which "
          "∫|x|e^{−σt}dt < ∞.")
n.h2("ROC Properties (sl. 17–25)")
n.table(["#", "Property"],
        [["1", "ROC = vertical strips (depends on σ only)"],
         ["2", "ROC of a rational X(s) contains no poles"],
         ["3", "Finite-duration, absolutely integrable x ⇒ ROC = entire s-plane (Ex 9.6: x = e^{−at} on (0, T) has X = (1 − e^{−(s+a)T})/(s + a); the 'pole' at s = −a is cancelled — limit = T)"],
         ["4", "Right-sided ⇒ ROC is a right half-plane Re{s} > σ₀"],
         ["5", "Left-sided ⇒ ROC is a left half-plane Re{s} < σ₀"],
         ["6", "Two-sided ⇒ a strip σ_R < Re{s} < σ_L (or empty ⇒ no transform)"],
         ["7", "Rational X: ROC bounded by poles or extends to ∞"],
         ["8", "Rational and right-sided ⇒ right of the rightmost pole; left-sided ⇒ left of the leftmost pole"]],
        widths_cm=[1.0, 16.2])
n.p("Example 9.8: X = 1/((s+1)(s+2)) has three possible ROCs — Re > −1 (right-sided), Re < −2 (left-sided), −2 < Re < −1 "
    "(two-sided). Only the strip contains... none contains the jω-axis except Re > −1 (which is causal and stable).")
n.figure_from_pdf(B[6], 25, "Figure 13.1 — One X(s), three ROCs, three signals (Lec 6, sl. 25)", clip=CLIP, width_cm=12)
n.exam_approach(["Split x(t) into right-sided, left-sided and finite parts; transform each with its own ROC.",
                 "ROC of the sum = intersection of the individual ROCs (empty ⇒ the transform does not exist).",
                 "Time shift does not change the ROC (e^{−st₀} has no poles); a finite-duration piece has ROC = all s.",
                 "Sketch the ROC as a shaded strip with the poles (×) marked on its boundaries."])
n.practice("Lesson 13", "(a) Actual — CSE 219 2022-23 Q1(b), Q2(c), Q4(a). (b) Actual — EEE 211 2021-22 Q7(a). (c) Actual — EEE 211 "
           "2016-17 Q7(a), EEE 301 2014-15 Q7(b), 2013-14 Q6(b).",
           ["(a) (i) x(t) = e^{−at} for 0 < t < T, 0 elsewhere: is s = −a in the ROC of its Laplace transform? (ii) LT and ROC of "
            "e^{−b|t−2|} (b > 0). (iii) Relation between the Laplace and Fourier transforms. (10 + 15 + 10)",
            "(b) LT and ROC of (i) e^{−at}u(t), a > 0; (ii) e^{−at}u(t), a < 0; (iii) −e^{−at}u(−t), a < 0. (12)",
            "(c) Bilateral and unilateral LT of e^{at}u(−t) (a > 0); of e^{bt}u(−t); of cos(at)u(−t). (11; 7; 7)"])
n.solution()
n.answer("(a)", "(i) X(s) = ∫₀^T e^{−(s+a)t}dt = [1 − e^{−(s+a)T}]/(s + a). Finite duration and absolutely integrable ⇒ ROC = "
         "all s (property 3). At s = −a numerator and denominator both vanish; L'Hôpital: X(−a) = T e^{0} = T, finite. "
         "So **yes**, s = −a is in the ROC — there is no pole there. (ii) e^{−b|t−2|} = e^{−b|τ|}|_{τ=t−2}: e^{−b|t|} = "
         "e^{−bt}u(t) + e^{bt}u(−t) ↔ 1/(s + b) − 1/(s − b) = −2b/(s² − b²), −b < Re{s} < b. Time shift by 2 multiplies by "
         "e^{−2s}: **X(s) = −2b e^{−2s}/(s² − b²) = 2b e^{−2s}/(b² − s²), −b < Re{s} < b** (shift leaves the ROC unchanged). "
         "(iii) X(σ + jω) = ∫[x(t)e^{−σt}]e^{−jωt}dt = F{x(t)e^{−σt}}; setting σ = 0 gives the Fourier transform, valid "
         "when the ROC contains the jω-axis; the Laplace transform also exists for signals (growing exponentials) whose "
         "Fourier transform does not.")
n.code(["(b) (i)  1/(s + a), Re{s} > −a (a > 0: ROC contains jω axis ⇒ FT exists)",
        "    (ii) a < 0: e^{−at} = e^{|a|t} grows: 1/(s + a), Re{s} > −a = |a| > 0 (jω-axis not in ROC ⇒ no FT)",
        "    (iii) −e^{−at}u(−t): 1/(s + a), Re{s} < −a = |a| (a < 0 ⇒ ROC Re{s} < |a|, contains the jω-axis)",
        "(c) bilateral: e^{at}u(−t) ↔ −1/(s − a), Re{s} < a;   unilateral (integral from 0⁻): u(−t) = 0 for t > 0 ⇒ 0",
        "    e^{bt}u(−t) ↔ −1/(s − b), Re{s} < b;   cos(at)u(−t) ↔ −s/(s² + a²), Re{s} < 0"])
for k in [("2022-23", "CSE 219", "1(b)"), ("2022-23", "CSE 219", "2(c)"), ("2022-23", "CSE 219", "4(a)"),
          ("2021-22", "EEE 211", "7(a)"), ("2016-17", "EEE 211", "7(a)"), ("2014-15", "EEE 301", "7(b)"),
          ("2013-14", "EEE 301", "6(b)")]:
    mark(*k)

# ===================================================== L14
n.lesson("Lesson 14 — Inverse Laplace Transform", "Lec 6 sl. 27–36")
n.p("Inverse by the Bromwich integral (sl. 27–29): x(t)e^{−σt} = (1/2π)∫X(σ + jω)e^{jωt}dω, hence")
n.formula(["x(t) = (1/2πj)∫_{σ−j∞}^{σ+j∞} X(s)e^{st}ds,   σ anywhere in the ROC"])
n.p("Evaluated by closing the contour (Cauchy residues) — rarely by hand — or numerically (Riemann sum, sl. 30). In practice: "
    "**partial fractions + the ROC to choose each term's signal** (sl. 31–36):")
n.code(["A/(s + a):  ROC to the right of −a → A e^{−at}u(t);   ROC to the left of −a → −A e^{−at}u(−t)",
        "Ex: X = 1/((s+1)(s+2)) = 1/(s+1) − 1/(s+2)",
        "  Re{s} > −1:        x = (e^{−t} − e^{−2t})u(t)",
        "  Re{s} < −2:        x = (−e^{−t} + e^{−2t})u(−t)",
        "  −2 < Re{s} < −1:   x = −e^{−t}u(−t) − e^{−2t}u(t)"])
n.callout("memorize", "Repeated pole: 1/(s + a)^m ↔ t^{m−1}e^{−at}u(t)/(m − 1)! (right-sided) — for the left-sided case multiply "
          "by −u(−t) instead. If the degree of the numerator ≥ the denominator, divide first (polynomial part ⇒ δ(t), δ′(t)). "
          "Complex poles −α ± jβ: complete the square → e^{−αt}cos βt, e^{−αt}sin βt.")
n.exam_approach(["Factor the denominator, expand in partial fractions (cover-up for simple poles).",
                 "For each pole decide right- or left-sided from the given ROC (poles to the left of the ROC → right-sided, "
                 "poles to the right → left-sided).", "Invert term by term; write the final signal with u(t) and u(−t).",
                 "Check with the initial value or one numeric value."])
n.practice("Lesson 14", "(a) Actual — CSE 219 2022-23 Q2(b). (b) Actual — EEE 301 2010-11 Q3(b). (c) Practice set 8.1–8.7.",
           ["(a) Inverse LT of X(s) = (s + 2)/(s² + 7s + 12), −4 < Re{s} < −3. (10)",
            "(b) Impulse response of H(s) = (s² − 3s + 2)/(s³ + 6s² + 11s + 6) (causal). (6)",
            "(c) Invert (3s + 7)/((s+1)(s+2)), Re > −1; (2s+3)/(s²+2s+5), Re > −1; −5/((s+1)(s−4)), −1 < Re < 4; "
            "e^{−s}/(s(s+2)), Re > 0; s/(s+2), Re > −2."])
n.solution()
n.code(["(a) X = (s+2)/((s+3)(s+4)) = −1/(s+3) + 2/(s+4)      [A = (−3+2)/(−3+4) = −1, B = (−4+2)/(−4+3) = 2]",
        "    ROC −4 < Re{s} < −3: pole −3 is to the right of the ROC ⇒ left-sided; pole −4 is to the left ⇒ right-sided:",
        "    −1/(s+3) (Re < −3) ↔ +e^{−3t}u(−t);    2/(s+4) (Re > −4) ↔ 2e^{−4t}u(t)",
        "    x(t) = 2e^{−4t}u(t) + e^{−3t}u(−t)"])
n.code(["(b) H = 3/(s+1) − 12/(s+2) + 10/(s+3)   ⇒  h(t) = (3e^{−t} − 12e^{−2t} + 10e^{−3t})u(t)   [h(0⁺) = 1 ✓: leading coefficient]",
        "(c) (3s+7)/((s+1)(s+2)) = 4/(s+1) − 1/(s+2) ⇒ (4e^{−t} − e^{−2t})u(t)",
        "    (2s+3)/((s+1)²+4) = 2(s+1)/((s+1)²+4) + (1/2)·2/((s+1)²+4) ⇒ e^{−t}[2cos2t + ½sin2t]u(t)",
        "    −5/((s+1)(s−4)) = 1/(s+1) − 1/(s−4); −1 < Re < 4 ⇒ e^{−t}u(t) + e^{4t}u(−t)",
        "    e^{−s}/(s(s+2)) = e^{−s}·½[1/s − 1/(s+2)] ⇒ ½[1 − e^{−2(t−1)}]u(t−1)",
        "    s/(s+2) = 1 − 2/(s+2) ⇒ δ(t) − 2e^{−2t}u(t)"])
mark("2022-23", "CSE 219", "2(b)"); mark("2010-11", "EEE 301", "3(b)", "◐ Method")

# ===================================================== L15
n.lesson("Lesson 15 — Properties of the Laplace Transform", "Lec 7 sl. 4–18")
n.table(["Property", "Signal", "Transform", "ROC"],
        [["Linearity", "ax₁ + bx₂", "aX₁ + bX₂", "⊇ R₁ ∩ R₂ (pole cancellation can enlarge it: Ex 9.13)"],
         ["Time shift", "x(t − t₀)", "e^{−st₀}X(s)", "R"],
         ["s-shift", "e^{s₀t}x(t)", "X(s − s₀)", "R + Re{s₀}"],
         ["Scaling", "x(at)", "(1/|a|)X(s/a)", "aR"],
         ["Reversal", "x(−t)", "X(−s)", "−R"],
         ["Conjugation", "x*(t)", "X*(s*)", "R"],
         ["Convolution", "x₁ * x₂", "X₁X₂", "⊇ R₁ ∩ R₂"],
         ["Time differentiation", "dx/dt", "sX(s)", "⊇ R"],
         ["s-differentiation", "−t x(t)", "dX/ds", "R"],
         ["Integration", "∫_{−∞}^{t}x", "X(s)/s", "⊇ R ∩ {Re{s} > 0}"]],
        widths_cm=[3.4, 3.2, 3.8, 6.8], font_size=8.5)
n.callout("memorize", "Real x(t): poles and zeros are real or occur in conjugate pairs. te^{−at}u ↔ 1/(s + a)², "
          "t^{n−1}e^{−at}u/(n − 1)! ↔ 1/(s + a)ⁿ. Example 9.15: (2s² + 5s + 5)/((s+1)²(s+2)) = 2/(s+1)² − 1/(s+1) + 3/(s+2) "
          "⇒ x = (2te^{−t} − e^{−t} + 3e^{−2t})u(t).")
n.h2("Proofs You May Be Asked For")
n.code(["Differentiation in time: x = (1/2πj)∫X(s)e^{st}ds ⇒ dx/dt = (1/2πj)∫sX(s)e^{st}ds ⇒ dx/dt ↔ sX(s); ROC ⊇ R",
        "   (u ↔ 1/s, Re > 0;  du/dt = δ ↔ s·(1/s) = 1, all s — the pole cancels and the ROC grows)",
        "Differentiation in s: dX/ds = ∫x(t)(−t)e^{−st}dt ⇒ −t x(t) ↔ dX/ds (ROC unchanged)",
        "Unilateral (initial conditions): L{y′} = sY − y(0⁻);  L{y″} = s²Y − sy(0⁻) − y′(0⁻)",
        "Final-value theorem: if sY(s) has all poles in the open left half-plane, y(∞) = lim_{s→0} sY(s)",
        "   proof: ∫₀^∞ y′e^{−st}dt = sY − y(0⁻) → y(∞) − y(0⁻) as s → 0 ⇒ y(∞) = lim sY(s)",
        "   (does not apply if sY has a pole on the jω-axis other than a simple pole at 0 or in the RHP)"])
n.exam_approach(["Identify which properties connect the given signal to a known pair; name each used.",
                 "Track the ROC through every step (shift moves it, scaling scales it, reversal flips it).",
                 "Unilateral problems: use the derivative formulas with initial values at 0⁻."])
n.practice("Lesson 15", "(a) Actual — CSE 219 2022-23 Q2(a). (b) Actual — CSE 219 2023-24 Q6(b). (c) Actual — EEE 211 2021-22 "
           "Q7(b), 2017-18 Q4(c), 2016-17 Q7(b). (d) Actual — EEE 301 2012-13 Q7(a)–(b).",
           ["(a) State and prove the time-domain and s-domain differentiation properties of the Laplace transform. (10)",
            "(b) LT and ROC of x(t) = |t|e^{−2|t|} − e^{−t}cos(3t)u(t) + t²e^{−4t}u(t); sketch the ROC marking the poles. (13)",
            "(c) Inverse LT of 1/(s − a)³ by the convolution property; LT of a periodic ±1 square wave of period 2T; given "
            "X(s) of a right-sided signal, find the LT of y = t x + dx/dt + ∫₀ᵗ x.",
            "(d) LT of |z(t)| for the alternating pulse train of height 1, width τ, period 2T (+1 on (0,τ), −1 on (T, T+τ), …); "
            "state and prove the final-value theorem."])
n.solution()
n.answer("(a)", "Proofs in the box above (time: differentiate the inverse integral under the sign; s: differentiate the "
         "defining integral). The ROC of sX(s) contains R; that of dX/ds is exactly R.")
n.code(["(b) |t|e^{−2|t|} = te^{−2t}u(t) + (−t)e^{2t}u(−t)",
        "    te^{−2t}u(t) ↔ 1/(s+2)²,  Re{s} > −2",
        "    e^{2t}u(−t) ↔ −1/(s−2), Re < 2;  multiply by −t ↔ d/ds: (−t)e^{2t}u(−t) ↔ d/ds[−1/(s−2)] = 1/(s−2)², Re{s} < 2",
        "    ⇒ first term: 1/(s+2)² + 1/(s−2)²,  −2 < Re{s} < 2",
        "    e^{−t}cos3t u(t) ↔ (s+1)/((s+1)²+9), Re{s} > −1   (poles −1 ± 3j)",
        "    t²e^{−4t}u(t) ↔ 2/(s+4)³,  Re{s} > −4",
        "    X(s) = 1/(s+2)² + 1/(s−2)² − (s+1)/((s+1)²+9) + 2/(s+4)³",
        "    ROC: (−2, 2) ∩ (−1, ∞) ∩ (−4, ∞) = −1 < Re{s} < 2",
        "    poles to mark: s = −2 (double, outside the ROC), s = 2 (double), s = −1 ± 3j (on the left boundary), s = −4 (triple)",
        "    The ROC is the vertical strip between Re = −1 and Re = 2; it contains the jω-axis ⇒ Fourier transform exists."])
n.code(["(c) 1/(s−a)³: 1/(s−a)² ↔ te^{at}u(t) (right-sided, Re > a); convolution: 1/(s−a)·1/(s−a)²",
        "    e^{at}u * te^{at}u = e^{at}∫₀ᵗ τ dτ·u(t) = (t²/2)e^{at}u(t)   ⇒  x(t) = (t²/2)e^{at}u(t)",
        "    square wave ±1, half-period T: LT of one period = (1 − e^{−sT})²/s ⇒ X = (1 − e^{−sT})²/(s(1 − e^{−2sT})) = (1 − e^{−sT})/(s(1 + e^{−sT})) = (1/s)tanh(sT/2), Re > 0",
        "    y = t x + dx/dt + ∫₀ᵗx ↔ −X′(s) + sX(s) + X(s)/s  (x causal: x(0⁻) = 0 so L{x′} = sX)",
        "(d) final value: see the box; |z(t)| for the alternating train = rectangular pulses height 1 width τ every T,",
        "    L = (1 − e^{−sτ})/(s(1 − e^{−sT})), Re > 0"])
for k in [("2022-23", "CSE 219", "2(a)"), ("2023-24", "CSE 219", "6(b)"), ("2021-22", "EEE 211", "7(b)"),
          ("2017-18", "EEE 211", "4(c)"), ("2012-13", "EEE 301", "7(b)")]:
    mark(*k)
mark("2016-17", "EEE 211", "7(b)", "◐ Method"); mark("2012-13", "EEE 301", "7(a)")

# ===================================================== L16
n.lesson("Lesson 16 — LTI Systems, Differential Equations, Circuits and Feedback", "Lec 7 sl. 20–28 · circuits, feedback: textbook")
n.p("Y(s) = H(s)X(s) with H = L{h} the system function (sl. 20). From the differential equation Σaₖy^{(k)} = Σbₖx^{(k)} "
    "(zero initial conditions): H(s) = Y/X = Σbₖsᵏ/Σaₖsᵏ — zeros from the numerator, poles from the denominator; "
    "the equation fixes H(s) but **not the ROC**; causality chooses it (sl. 25–28).")
n.bullets(["**Causal** ⇔ ROC is a right half-plane (right of the rightmost pole for rational H).",
           "**Stable** ⇔ ROC contains the jω-axis. Causal + rational: stable ⇔ all poles in the open left half-plane.",
           "Ex 9.20: H = (s − 1)/((s + 1)(s − 2)): Re > 2 causal-unstable; −1 < Re < 2 stable, non-causal; Re < −1 "
           "anti-causal, unstable.",
           "**Causal but unstable**: H = 1/(s − 2), Re{s} > 2 (pole in the RHP). **Stable but non-causal**: "
           "H = −2/(s² − 1), −1 < Re < 1, h = e^{−|t|} (two-sided).",
           "Solving: dy/dt + 3y = x, x = e^{−2t}u: Y = 1/((s+2)(s+3)) ⇒ y = (e^{−2t} − e^{−3t})u (sl. 27)."])
n.h2("Initial Conditions, ZIR and ZSR (unilateral, textbook)")
n.code(["Y(s)·D(s) = N(s)X(s) + I(s)  where I(s) collects the initial-condition terms:",
        "  y″ + a₁y′ + a₀y = ... ⇒ I(s) = (s + a₁)y(0⁻) + y′(0⁻) ;   y′ + ay = ... ⇒ I(s) = y(0⁻)",
        "ZIR = I(s)/D(s) (x = 0);   ZSR = N(s)X(s)/D(s) (zero initial state);   y = ZIR + ZSR",
        "Final value of y: lim sY(s) (poles of sY in the open LHP only)"])
n.h2("Circuits (textbook)")
n.p("Replace elements by s-domain models: R → R; L → sL in series with the voltage source L·i(0⁻) (or sL in parallel with "
    "the current source i(0⁻)/s); C → 1/(sC) in series with v(0⁻)/s (or sC in parallel with the current source Cv(0⁻)). "
    "Then solve by KVL/KCL or voltage/current division. Inputs that are 'on for t < 0' (e.g. 2 V then 4e^{−2t} V) set "
    "the initial states from the dc steady state at 0⁻.")
n.h2("Block Diagrams and Feedback (textbook)")
n.code(["cascade: H₁H₂;  parallel: H₁ + H₂;  negative feedback: Y/X = G/(1 + GH)  (H = 1 for unity feedback)",
        "disturbance W entering after the controller: Y = [G_c G/(1 + G_c G)]R + [G/(1 + G_c G)]W",
        "Stability: poles of the closed loop = roots of 1 + GH = 0.",
        "Steady state: apply the final-value theorem to sY(s) after confirming that the closed-loop poles are in the LHP."])
n.exam_approach(["From the DE or diagram get H(s) as a ratio of polynomials; mark poles and zeros.",
                 "State the ROC from causality (right of rightmost pole) and compare with the jω-axis for stability.",
                 "Solve with initial conditions: collect terms in Y(s), partial fractions, invert.",
                 "Circuits: s-domain model with initial-energy sources; use division/KVL; invert.",
                 "Feedback: reduce with G/(1 + GH); check stability before using the final-value theorem."])
n.practice("Lesson 16 (A)", "(a) Actual — CSE 219 2023-24 Q6(a), Q6(c). (b) Actual — EEE 211 2023-24 Q8(b), Q5(b). (c) Actual — EEE 211 "
           "2021-22 Q7(c), 2017-18 Q4(b). (d) Actual — EEE 301 2015-16 Q7(b), 2014-15 Q7(a), 2013-14 Q6(a), 2010-11 Q3(a), "
           "2011-12 Q3–Q4, Q8(a).",
           ["(a) y″ + 7y′ + 12y = x′ + 2x, x = u(t), zero initial conditions: solve with the LT. (12) Can a system be (i) causal but "
            "unstable? (ii) stable but non-causal? Explain with the ROC and an example. (5 + 5)",
            "(b) y″ + 5y′ + 6y = x′ + x, y(0⁻) = 2, y′(0⁻) = 1, x = e^{−4t}u(t): Laplace solution, ZIR and ZSR. (18) Unity-feedback "
            "loop, plant 1/(s+2), controller (s+1)/s, x = Au: can the output settle to A? Repeat with controller 1/(s−2). (15)",
            "(c) y′ + 2y = e^{−3t}u, y(0⁻) = 1; y″ + 3y′ + 2y = 2x′ + x: H(s) and h(t).",
            "(d) y″ + 5y′ + 6y = 2e^{−t}u, y′(0⁻) = −2, y(0⁻) = 3; y″ + 4y′ + 3y = e^{−3t}u, y(0⁻) = 0, y′(0⁻) = 1; "
            "y″ + 4y′ + 3y = u, y(0⁻) = 2, y′(0⁻) = 1; y″ + 3y′ + 2y = 0, y(0⁻) = 3, y′(0⁻) = 1 (then H for x = e^{−3t}u and the final "
            "value); y″ + 5y′ + 6y = x″ + 5x′ + 5x: h(t)."])
n.solution()
n.code(["(a) Y = (s+2)/(s(s+3)(s+4)) = (1/6)/s + (1/3)/(s+3) − (1/2)/(s+4)",
        "    y(t) = [1/6 + (1/3)e^{−3t} − (1/2)e^{−4t}] u(t)      (y(0⁺) = 0 ✓, y(∞) = 1/6 = H(0))",
        "    (i)  causal but unstable: H = 1/(s−2), ROC Re > 2 (right half-plane ⇒ causal; the pole at +2 ⇒ ROC excludes the jω axis ⇒ unstable): h = e^{2t}u(t)",
        "    (ii) stable but non-causal: H = −2/(s²−1), ROC −1 < Re < 1 (strip contains jω; not a right half-plane): h = e^{−|t|}"])
n.code(["(b) Y(s²+5s+6) = (s+1)X + (s+5)y(0⁻) + y′(0⁻) = (s+1)/(s+4) + 2(s+5) + 1",
        "    ZIR: (2s+11)/((s+2)(s+3)) = 7/(s+2) − 5/(s+3)        ⇒ (7e^{−2t} − 5e^{−3t})u(t)",
        "    ZSR: (s+1)/((s+2)(s+3)(s+4)) = −½/(s+2) + 2/(s+3) − 3/2/(s+4) ⇒ (−½e^{−2t} + 2e^{−3t} − 1.5e^{−4t})u(t)",
        "    y(t) = (6.5e^{−2t} − 3e^{−3t} − 1.5e^{−4t})u(t)       (y(0⁺) = 2 ✓)",
        "    Feedback: G = (s+1)/(s(s+2)), T = G/(1+G) = (s+1)/(s²+3s+1): poles (−3 ± √5)/2 ⇒ stable;",
        "    y(∞) = lim s·T·A/s = T(0)A = A ⇒ the goal is met (integral action: the controller has a pole at 0).",
        "    Controller 1/(s−2): T = 1/(s²−3): poles ±√3, one in the RHP ⇒ unstable: the output grows like e^{√3t};",
        "    the final-value theorem does not apply (the formal limit −A/3 is meaningless)."])
n.code(["(c) y′+2y = e^{−3t}u, y(0⁻) = 1: Y = (1 + 1/(s+3))/(s+2) = 2/(s+2) − 1/(s+3) ⇒ y = (2e^{−2t} − e^{−3t})u",
        "    H = (2s+1)/((s+1)(s+2)) = −1/(s+1) + 3/(s+2) ⇒ h = (3e^{−2t} − e^{−t})u(t)  (causal, stable)"])
n.code(["(d) 2e^{−t}: Y = (2/(s+1) + 3s + 13)/((s+2)(s+3)) = 1/(s+1) + 5/(s+2) − 3/(s+3) ⇒ y = (e^{−t} + 5e^{−2t} − 3e^{−3t})u",
        "    e^{−3t}: Y = (1/(s+3) + 1)/((s+1)(s+3)) = (3/4)/(s+1) − (3/4)/(s+3) − (1/2)/(s+3)² ⇒ y = (¾e^{−t} − ¾e^{−3t} − ½te^{−3t})u",
        "    u: Y = (2s² + 9s + 1)/(s(s+1)(s+3)) = (1/3)/s + 3/(s+1) − (4/3)/(s+3) ⇒ y = (1/3 + 3e^{−t} − (4/3)e^{−3t})u",
        "    free: Y = (3s+10)/((s+1)(s+2)) = 7/(s+1) − 4/(s+2) ⇒ y = (7e^{−t} − 4e^{−2t})u, y(∞) = 0;",
        "          H = 1/((s+1)(s+2)); x = e^{−3t}u: Y_zs = 1/((s+1)(s+2)(s+3)), lim sY_total = 0",
        "    H = (s²+5s+5)/(s²+5s+6) = 1 − 1/((s+2)(s+3)) = 1 − 1/(s+2) + 1/(s+3) ⇒ h = δ(t) + (e^{−3t} − e^{−2t})u(t)"])
for k in [("2023-24", "CSE 219", "6(a)"), ("2023-24", "CSE 219", "6(c)"), ("2023-24", "EEE 211", "8(b)"),
          ("2023-24", "EEE 211", "5(b)"), ("2021-22", "EEE 211", "7(c)"), ("2017-18", "EEE 211", "4(b)"),
          ("2015-16", "EEE 301", "7(b)"), ("2014-15", "EEE 301", "7(a)"), ("2013-14", "EEE 301", "6(a)"),
          ("2010-11", "EEE 301", "3(a)"), ("2011-12", "EEE 301", "8(a)")]:
    mark(*k)

n.practice("Lesson 16 (B) — Circuits, Feedback, System Identification",
           "(e) Actual — EEE 211 2023-24 Q4(a), 2022-23 Q3(a), Q1(a), 2020-21 Q3(b), 2018-19 Q5(b), 2017-18 Q3(a); EEE 301 2016-17 "
           "Q8(b), 2015-16 Q8(a), 2014-15 Q8(a), 2013-14 Q5(a), 2012-13 Q8(b). (f) Actual — EEE 211 2023-24 Q8(a), 2020-21 Q3(a), "
           "Q4(a), 2017-18 Q3(b), 2019-20 Q3, 2018-19 Q5(a); EEE 301 2014-15 Q7(c), 2013-14 Q6(c), 2015-16 Q8(b), 2016-17 EEE 211 "
           "Q7(c), 2021-22 Q8(a), 2010-11 Q4(a), 2011-12 Q3(a)–(b), Q4(a), 2012-13 Q7(c).",
           ["(e) Series inductor L = 2 H feeding the parallel R = 1 Ω, C = 2 F (output y = v_C), v_C(0⁻) = 1 V, i_L(0⁻) = 2 A, "
            "x = u(t): y(t) by LT; H(s) and h(t) of the same circuit.",
            "(f) H₁ = 1/(s² + bs + (b − 3)) with feedback H₂ = −2 (or H₁ = 1/(s² + bs + (b − 2)), H₂ = −1): overall H and the values "
            "of b for stability. u(t) → δ(t − 1) → [δ(t) ∥ e^{−2t}u(t)] → y: Y(s), y(t). Multipath y = x + a x(t − T): H(s), inverse "
            "system, h_inv, condition for causal and stable."])
n.solution()
n.code(["(e) Elements: L → 2s with series source 2·i(0⁻) = 4 V (opposing), C → 1/(2s) with v_C(0⁻) = 1 V.",
        "    KVL/KCL: X/s = 2(sI − 2) + V,   I = V/R + C(sV − 1) = (2s+1)V − 2",
        "    ⇒ V(4s² + 2s + 1) = 1/s + 4s + 4   ⇒   Y(s) = (4s² + 4s + 1)/(s(4s² + 2s + 1)) = 1/s + 2/(4s² + 2s + 1)",
        "    4s² + 2s + 1 = 4[(s + ¼)² + 3/16]:  y(t) = [1 + (2/√3)e^{−t/4} sin(√3t/4)] u(t)",
        "    check: y(0⁺) = 1 = v_C(0⁻) ✓, y(∞) = 1 = x",
        "    H(s) = 1/(4s² + 2s + 1) ⇒ h(t) = (1/√3) e^{−t/4} sin(√3t/4) u(t)",
        "    (other circuits of this type: same steps — s-domain model, KVL/KCL with initial sources, partial fractions)"])
n.code(["(f) H₁/(1 + H₁H₂) with H₂ = −2: H = 1/(s² + bs + b − 5);  with H₂ = −1 and (b − 2): H = 1/(s² + bs + b − 3)",
        "    stability (causal, 2nd order): all coefficients > 0 ⇒ b > 5 (first), b > 3 (second)  [b > 0 also needed]",
        "    u → δ(t−1) → parallel: Y = (1/s)e^{−s}(1 + 1/(s+2)) = e^{−s}(s+3)/(s(s+2))",
        "        = e^{−s}[(3/2)/s − (1/2)/(s+2)] ⇒ y = u(t−1)[3/2 − ½e^{−2(t−1)}]",
        "    multipath: H = 1 + a e^{−sT}; inverse H_inv = 1/(1 + a e^{−sT}) = feedback system with forward gain 1 and",
        "    feedback path a e^{−sT} (delay T, gain a); expanding for |a| < 1: h_inv = Σ_{k≥0}(−a)^k δ(t − kT);",
        "    causal and stable (ROC Re{s} > σ₀ ∋ jω) iff |a| < 1 (poles of H_inv at e^{−sT} = −1/a lie in the left half-plane).",
        "    Block diagrams with H₁, H₂, K or disturbances: reduce with G/(1+GH); disturbance transfer H_d = G/(1 + G_cG),",
        "    steady-state error zero for a step disturbance if G_c has a zero at s = 0 ... (H_d(0) = 0 ⇒ G_c(s) ~ s numerator zero)"])
for k in [("2023-24", "EEE 211", "4(a)"), ("2022-23", "EEE 211", "3(a)"), ("2020-21", "EEE 211", "3(b)"),
          ("2018-19", "EEE 211", "5(b)"), ("2017-18", "EEE 211", "3(a)"), ("2016-17", "EEE 211", "8(b)"),
          ("2015-16", "EEE 301", "8(a)"), ("2014-15", "EEE 301", "8(a)"), ("2013-14", "EEE 301", "5(a)"),
          ("2012-13", "EEE 301", "8(b)"), ("2020-21", "EEE 211", "3(a)"), ("2017-18", "EEE 211", "3(b)"),
          ("2016-17", "EEE 211", "7(c)"), ("2019-20", "EEE 211", "3"), ("2015-16", "EEE 301", "8(b)")]:
    mark(*k, "◐ Method")
for k in [("2023-24", "EEE 211", "8(a)"), ("2020-21", "EEE 211", "4(a)"), ("2018-19", "EEE 211", "5(a)"),
          ("2014-15", "EEE 301", "7(c)"), ("2013-14", "EEE 301", "6(c)"), ("2021-22", "EEE 211", "8(a)"),
          ("2010-11", "EEE 301", "4(a)"), ("2011-12", "EEE 301", "3(a)"), ("2011-12", "EEE 301", "3(b)"),
          ("2011-12", "EEE 301", "4(a)"), ("2012-13", "EEE 301", "7(c)"), ("2022-23", "EEE 211", "1(a)"),
          ("2018-19", "EEE 211", "8(a)")]:
    mark(*k, "○ Partly")
mark("2012-13", "EEE 301", "7(c)", "✔ Solved")
n.callout("note", "Several EEE questions in this tab depend on a figure (block diagram, circuit) that is only partly legible in the "
          "scanned papers — they are marked ‘Method’ or ‘Partly’ in the tracker. Method for each: write H(s) from the diagram, "
          "check ROC/stability, then partial fractions (and final value for steady-state questions). EEE 301 2012-13 Q7(c): "
          "H = Y/X = (s + 2)[1/(s+1) − 3/(s+2)] = (s+2)/(s+1) − 3 = 1/(s+1) − 2, "
          "so **h(t) = e^{−t}u(t) − 2δ(t)**.")

n.quick_notes("Quick Notes — Laplace Transform", "Revision points for Lessons 13–16.",
              [("L13 · ROC", ["X = ∫x e^{−st}; LT = FT of x e^{−σt}; ROC = vertical strip, no poles; finite signal ⇒ all s.",
                             "Right-sided → right of rightmost pole; left-sided → left of leftmost; two-sided → strip.",
                             "e^{−at}u ↔ 1/(s+a) Re > −a; −e^{−at}u(−t) ↔ same, Re < −a; e^{−b|t|} ↔ −2b/(s²−b²), |Re| < b."]),
               ("L14 · Inverse", ["Partial fractions; pole left of ROC → right-sided term; pole right of ROC → left-sided.",
                                 "(s+2)/((s+3)(s+4)), −4 < Re < −3 → 2e^{−4t}u(t) + e^{−3t}u(−t)."]),
               ("L15 · Properties", ["shift e^{−st₀}X; s-shift X(s−s₀); scale X(s/a)/|a|; d/dt ↔ s; −t x ↔ dX/ds; ∫ ↔ X/s; conv ↔ product.",
                                    "Unilateral: sY − y(0⁻); final value lim sY."]),
               ("L16 · Systems", ["H = N/D; causal ⇔ right half-plane ROC; stable ⇔ ROC ∋ jω.",
                                 "y = ZIR + ZSR; feedback G/(1+GH). 6(a) CSE 219: y = [1/6 + e^{−3t}/3 − e^{−4t}/2]u."])],
              diagrams=[(B[7], 22, "Stability from the ROC: three ROCs of (s−1)/((s+1)(s−2)) (Lec 7, sl. 22)", CLIP, 12)])
n.save()
save_solved("ashraf_laplace")
print("saved", n.out_path)
