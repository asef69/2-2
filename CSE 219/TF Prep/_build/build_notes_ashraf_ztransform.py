"""Ashraf F5 — z-transform (Lec 8). Lessons 17–19."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from c219 import B, FIG, ashraf, exam_map, mark, save_solved  # noqa: E402

CLIP = (0.0, 0.09, 1.0, 0.97)
n = ashraf("Lec 8 · z-Transform: ROC, Inverse, Properties, LTI Systems", "CSE219_Ashraf_ZTransform_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "z-transform questions and their weight"),
              ("Lesson 17 — Definition, ROC and Standard Transforms", "z = e^{sT}, aⁿu[n], left-sided, finite sequences, ROC properties 1–9"),
              ("Lesson 18 — The Inverse z-Transform", "contour formula, partial fractions, power series (log)"),
              ("Lesson 19 — Properties and LTI Systems", "ROC and causality/stability, pole-zero plots, difference equations"),
              ("Quick Notes — z-Transform", "merged revision notes + key diagrams")],
    source_note="Slide numbers are PDF page numbers of 8 - Z-Transform.pdf (47 pages, “Lec 8”); the printed slide number is one "
                "less. The deck mirrors the Laplace transform: right-sided ⇒ outside a circle, left-sided ⇒ inside, "
                "two-sided ⇒ an annulus; the unit circle plays the role of the jω-axis.")

n.h1("Exam Map — What the TF Papers Ask")
exam_map(n, "Ashraf", range(17, 20))
n.callout("focus", "The z-transform appears only in the two newest CSE 219 papers, always in Ashraf's part: 2022-23 Q1(a), Q3 "
          "(35 marks) and 2023-24 Q8 (35 marks). Learn: aⁿu[n] with its ROC, the three ROCs of a rational X(z), partial "
          "fractions in z⁻¹, the unit-circle test for the DTFT, and the power-series method (log(1 + az⁻¹)).")

# ===================================================== L17
n.lesson("Lesson 17 — Definition, ROC and Standard Transforms", "Lec 8 sl. 4–26")
n.p("zⁿ is the eigenfunction of discrete LTI systems: y[n] = H(z)zⁿ with H(z) = Σh[k]z^{−k}. Sampling e^{st} at t = nT gives "
    "(e^{sT})ⁿ, so z = e^{sT} = e^{σT}e^{jωT} = re^{jθ} (sl. 6): the jω-axis maps to the unit circle |z| = 1, the left "
    "half-plane to the interior, a vertical strip to an annulus; s and s + j2π/T give the same z, which is why z is "
    "used for sequences (sl. 7–8).")
n.formula(["X(z) = Σ_{n=−∞}^{∞} x[n]z^{−n}          X(re^{jω}) = F{x[n]r^{−n}}   (r = 1: DTFT)",
           "The DTFT exists iff the ROC contains the unit circle |z| = 1"])
n.table(["Sequence", "X(z)", "ROC"],
        [["aⁿu[n]", "1/(1 − az⁻¹) = z/(z − a)", "|z| > |a|  (pole a, zero 0; exterior of a circle)"],
         ["−aⁿu[−n−1]", "1/(1 − az⁻¹)", "|z| < |a|  (same expression, interior)"],
         ["7(1/3)ⁿu − 6(1/2)ⁿu", "z(z − 2/3)/((z − 1/3)(z − 1/2))", "|z| > 1/2"],
         ["(1/3)ⁿ sin(πn/4)u[n]", "(√2/6)z⁻¹/(1 − (√2/3)z⁻¹ + z⁻²/9)", "|z| > 1/3"],
         ["δ[n]; δ[n−1]; δ[n+1]", "1; z⁻¹; z", "all z; all z ≠ 0; all finite z"],
         ["aⁿ, 0 ≤ n ≤ N−1", "(1 − aᴺz⁻ᴺ)/(1 − az⁻¹) = z(1 − aᴺz⁻ᴺ)/(z − a)", "all z ≠ 0; N−1 zeros on |z| = a at ae^{j2πk/N}"],
         ["b^{|n|}, 0 < b < 1", "(1−b²)/((1−bz⁻¹)(1−bz))", "b < |z| < 1/b (no ROC if b > 1)"]],
        widths_cm=[4.4, 7.0, 5.8], font_size=8.5)
n.callout("memorize", "A z-transform = expression + ROC. Geometric series: Σ(az⁻¹)ⁿ = 1/(1 − az⁻¹) for |az⁻¹| < 1. "
          "Left-sided: −Σ_{m≥1}(a⁻¹z)^m = 1/(1 − az⁻¹) for |z| < |a|.")
n.h2("ROC Properties (sl. 17–26)")
n.table(["#", "Property"],
        [["1", "ROC is a ring centred at the origin (depends on r = |z| only)"],
         ["2", "ROC contains no poles (poles bound it)"],
         ["3", "Finite-duration x ⇒ ROC = all z except possibly z = 0 (samples at n > 0 give z^{−n}) and/or ∞ (samples at n < 0). "
               "N₁ ≥ 0 ⇒ ∞ included; N₂ ≤ 0 ⇒ 0 included"],
         ["4", "Right-sided ⇒ exterior of a circle |z| > r₀ (includes ∞ iff causal)"],
         ["5", "Left-sided ⇒ interior 0 < |z| < r₀ (includes 0 iff anti-causal)"],
         ["6", "Two-sided ⇒ annulus r₁ < |z| < r₂ (or empty)"],
         ["7–9", "Rational: bounded by poles or reaching 0/∞; right-sided ⇒ outside the outermost pole; left-sided ⇒ inside "
                 "the innermost non-zero pole"]],
        widths_cm=[1.2, 16.0])
n.figure_from_pdf(B[8], 26, "Figure 17.1 — Three ROCs of one X(z): exterior (right-sided), annulus (two-sided, has a DTFT), interior (left-sided) (Lec 8, sl. 26)",
                  clip=CLIP, width_cm=12)
n.exam_approach(["Write the geometric series that defines X(z) and state the convergence condition — that is the ROC.",
                 "For a finite sequence: list the powers of z; positive powers (n < 0) exclude ∞, negative powers (n > 0) exclude 0.",
                 "For X(z) = N/D: poles = roots of D (in z, not in z⁻¹!); possible ROCs = regions separated by the pole circles.",
                 "State which ROC contains |z| = 1 (⇒ DTFT exists)."])
n.practice("Lesson 17", "(a) Actual — CSE 219 2022-23 Q1(a), Q3(a). (b) Actual — CSE 219 2023-24 Q8(a), Q8(d).",
           ["(a) (i) z-transform and ROC of x[n] = aⁿu[n]. (ii) x[n] = aⁿ for 0 ≤ n ≤ N − 1: show that the ROC of X(z) cannot "
            "include the origin. (10 + 10)",
            "(b) Find all possible two-sided... sequences with X(z) = (1 + 2z⁻¹ − z⁻²)/(1 − (11/6)z⁻¹ + z⁻² − (1/6)z⁻³): for each, "
            "the ROC and x[n]. Differentiate the Laplace and z-transforms and say why z is preferred for discrete time. (12 + 5)"])
n.solution()
n.code(["(a)(i) X(z) = Σ_{n=0}^{∞} aⁿz^{−n} = Σ(az⁻¹)ⁿ = 1/(1 − az⁻¹) = z/(z − a),   |az⁻¹| < 1 ⇔ |z| > |a|",
        "      pole z = a, zero z = 0; ROC outside the circle through the pole; contains |z| = 1 iff |a| < 1.",
        "(ii) X(z) = Σ_{n=0}^{N−1} aⁿz^{−n} = 1 + az⁻¹ + a²z⁻² + … + a^{N−1}z^{−(N−1)}.  For N ≥ 2 the term a z⁻¹ → ∞ as z → 0",
        "     (|z|⁻¹ → ∞), so X(0) is not finite ⇒ z = 0 cannot belong to the ROC. The sum is finite for every z ≠ 0,",
        "     so ROC = |z| > 0. (Closed form: X = z(1 − aᴺz⁻ᴺ)/(z − a): N−1 poles at the origin; the pole at z = a is",
        "     cancelled by a zero.)"])
n.code(["(b) Denominator: z³ − (11/6)z² + z − 1/6 = (z − 1)(z − 1/2)(z − 1/3) ⇒ poles 1, 1/2, 1/3",
        "    X = 6/(1 − z⁻¹) − 3/(1 − ½z⁻¹) − 2/(1 − ⅓z⁻¹)   [x[0] = lim X = 1 = 6 − 3 − 2 ✓]",
        "    Four ROCs (rings between the pole circles); poles inside the ROC's inner side give right-sided terms:",
        "    (1) |z| > 1       : x[n] = [6 − 3(1/2)ⁿ − 2(1/3)ⁿ] u[n]                                   right-sided, causal",
        "    (2) 1/2 < |z| < 1 : x[n] = −6u[−n−1] − 3(1/2)ⁿu[n] − 2(1/3)ⁿu[n]                           two-sided",
        "    (3) 1/3 < |z| < 1/2: x[n] = −6u[−n−1] + 3(1/2)ⁿu[−n−1] − 2(1/3)ⁿu[n]                      two-sided",
        "    (4) |z| < 1/3     : x[n] = −6u[−n−1] + 3(1/2)ⁿu[−n−1] + 2(1/3)ⁿu[−n−1]                     left-sided",
        "    Rule: a pole on the inner side of the ROC (|p| < |z|) → right-sided term Apⁿu[n];",
        "          a pole on the outer side (|p| > |z|) → left-sided term −Apⁿu[−n−1].",
        "    The pole at z = 1 lies on the unit circle, so |z| = 1 belongs to no valid ROC: the DTFT of none of the four exists."])
n.answer("(d)", "Laplace: continuous-time, X(s) = ∫x e^{−st}dt, s = σ + jω, ROC = vertical strips/half-planes, stability ↔ ROC ∋ "
         "jω-axis, rational in s. z-transform: discrete-time, X(z) = Σx[n]z^{−n}, z = re^{jω}, ROC = rings/exteriors/"
         "interiors, stability ↔ ROC ∋ unit circle, rational in z (or z⁻¹), related by z = e^{sT}. Why z for DT: the map "
         "s → e^{sT} is many-to-one (s and s + j2π/T give the same sequence e^{snT}), so the s-plane would count the "
         "same discrete signal infinitely often; z removes that redundancy, turns difference equations into algebraic "
         "ones, uses the finite sum Σx[n]z^{−n} (no integrals) and makes the unit circle the frequency axis.")
for k in [("2022-23", "CSE 219", "1(a)"), ("2022-23", "CSE 219", "3(a)"), ("2023-24", "CSE 219", "8(a)"),
          ("2023-24", "CSE 219", "8(d)")]:
    mark(*k)

# ===================================================== L18
n.lesson("Lesson 18 — The Inverse z-Transform", "Lec 8 sl. 28–32")
n.h2("1. Contour Formula (sl. 28)")
n.code(["z = re^{jω} in the ROC: x[n]r^{−n} = (1/2π)∫_{2π} X(re^{jω})e^{jωn}dω  (inverse DTFT)",
        "multiply by rⁿ:  x[n] = (1/2π)∫_{2π} X(re^{jω})(re^{jω})ⁿ dω",
        "z = re^{jω} ⇒ dz = jz dω ⇒ dω = dz/(jz):",
        "x[n] = (1/2πj) ∮_C X(z) z^{n−1} dz     (C: counter-clockwise circle inside the ROC; evaluate by residues)"])
n.h2("2. Partial Fractions (sl. 29–31)")
n.p("X(z) = (3 − (5/2)z⁻¹)/((1 − ¼z⁻¹)(1 − ⅓z⁻¹)) = 1/(1 − ¼z⁻¹) + 2/(1 − ⅓z⁻¹). ROC |z| > 1/3 ⇒ both right-sided: "
    "x = (¼)ⁿu[n] + 2(⅓)ⁿu[n]. ROC ¼ < |z| < ⅓: x = (¼)ⁿu[n] − 2(⅓)ⁿu[−n−1]. ROC |z| < ¼: both left-sided: "
    "−(¼)ⁿu[−n−1] − 2(⅓)ⁿu[−n−1]. The expansion never changes; the ROC decides each term.")
n.h2("3. Power Series (sl. 31–32)")
n.p("The coefficient of z^{−n} is x[n] (positive powers of z are negative times). 4z² + 2 + 3z⁻¹ ⇒ 4δ[n+2] + 2δ[n] + 3δ[n−1]. "
    "1/(1 − az⁻¹) = 1 + az⁻¹ + a²z⁻² + … (|z| > |a|) ⇒ aⁿu[n]; for |z| < |a| expand in z/a ⇒ −aⁿu[−n−1].")
n.code(["X(z) = log(1 + az⁻¹), |z| > |a|:   log(1 + v) = Σ_{n≥1} (−1)^{n+1}vⁿ/n  (|v| < 1), v = az⁻¹ (|v| < 1 ⇔ |z| > |a|)",
        "X(z) = Σ_{n≥1} (−1)^{n+1} (aⁿ/n) z^{−n}   ⇒   x[n] = (−1)^{n+1} aⁿ/n for n ≥ 1,  0 for n ≤ 0",
        "i.e. x[n] = (−1)^{n+1}(aⁿ/n) u[n − 1]   (checked numerically: Σ ... = log(1 + a/|z|))"])
n.exam_approach(["Rational X: partial fractions in z⁻¹ (write with unit constant terms), then use the ROC for each term.",
                 "Log/irrational X: expand in a power series of z⁻¹ valid in the ROC (|…| < 1) and read off the coefficients.",
                 "Check x[0] = lim_{z→∞}X(z) for causal sequences."])
n.practice("Lesson 18", "(a) Actual — CSE 219 2022-23 Q3(b), Q3(c). (b) Practice set 11.1–11.5 (first two).",
           ["(a) Derive the contour-integral formula for the inverse z-transform; find the sequence for X(z) = log(1 + az⁻¹), |z| > |a|. (10 + 15)",
            "(b) Invert (2 − z⁻¹)/((1 − ¼z⁻¹)(1 − ¾z⁻¹)), |z| > ¾; and 1/((1 − 2z⁻¹)(1 − ⅓z⁻¹)), 1/3 < |z| < 2."])
n.solution()
n.answer("(a)", "Derivation and the logarithm series in the boxes above (the log series needs |az⁻¹| < 1, which is exactly the ROC |z| > |a|).")
n.code(["(b) (2 − z⁻¹)/((1 − ¼z⁻¹)(1 − ¾z⁻¹)) = 1/(1 − ¼z⁻¹) + 1/(1 − ¾z⁻¹)   [A = (2−4)/(1−3)=1, B = (2−4/3)/(1−1/3)=1]",
        "    |z| > 3/4: x[n] = [(¼)ⁿ + (¾)ⁿ] u[n]",
        "    1/((1−2z⁻¹)(1−⅓z⁻¹)) = (6/5)/(1 − 2z⁻¹) − (1/5)/(1 − ⅓z⁻¹)   [A = 1/(1−1/6) = 6/5, B = 1/(1−6) = −1/5]",
        "    1/3 < |z| < 2: the pole 2 is outside ⇒ left-sided; pole 1/3 inside ⇒ right-sided:",
        "    x[n] = −(6/5)2ⁿu[−n−1] − (1/5)(⅓)ⁿu[n]"])
for k in [("2022-23", "CSE 219", "3(b)"), ("2022-23", "CSE 219", "3(c)")]:
    mark(*k)

# ===================================================== L19
n.lesson("Lesson 19 — Properties and LTI Systems", "Lec 8 sl. 34–47")
n.table(["Property", "Sequence", "Transform", "ROC"],
        [["Linearity", "ax₁ + bx₂", "aX₁ + bX₂", "⊇ R₁ ∩ R₂"],
         ["Time shift", "x[n − n₀]", "z^{−n₀}X(z)", "R (except 0, ∞)"],
         ["z-scaling", "a₀ⁿx[n]", "X(z/a₀)", "|a₀|R"],
         ["Reversal", "x[−n]", "X(z⁻¹)", "R⁻¹"],
         ["Conjugation", "x*[n]", "X*(z*)", "R"],
         ["Time expansion", "x[n/k] (zeros between)", "X(zᵏ)", "R^{1/k}"],
         ["Convolution", "x₁ * x₂", "X₁X₂", "⊇ R₁ ∩ R₂"],
         ["First difference", "x[n] − x[n−1]", "(1 − z⁻¹)X", "R (+ 0 deleted, z = 1 may be added)"],
         ["Accumulation", "Σ_{k≤n}x[k]", "X/(1 − z⁻¹)", "⊇ R ∩ {|z| > 1}"],
         ["z-differentiation", "n x[n]", "−z dX/dz", "R"],
         ["Initial value", "x[n] = 0 for n < 0", "x[0] = lim_{z→∞}X(z)", ""]],
        widths_cm=[3.5, 4.2, 4.0, 5.5], font_size=8.5)
n.p("Example 10.18: aⁿu[n] ↔ 1/(1 − az⁻¹) ⇒ n aⁿ u[n] ↔ −z d/dz[1/(1 − az⁻¹)] = az⁻¹/(1 − az⁻¹)².")
n.h2("LTI Systems (sl. 43–47)")
n.bullets(["Y(z) = H(z)X(z); if the ROC contains |z| = 1, H(e^{jω}) is the frequency response.",
           "**Causal** ⇔ ROC is the exterior of a circle including ∞ (for rational H: outside the outermost pole, "
           "numerator degree ≤ denominator degree in z).",
           "**Stable** ⇔ ROC contains the unit circle. Causal + rational: stable ⇔ all poles inside |z| = 1.",
           "H = 1/(1 − 2r cos θ z⁻¹ + r²z⁻²): poles re^{±jθ}; causal ⇒ stable iff r < 1.",
           "Difference equation Σaₖy[n−k] = Σbₖx[n−k] ⇒ H(z) = Σbₖz^{−k}/Σaₖz^{−k}; the equation gives the expression, "
           "**not the ROC** (causality chooses it).",
           "Ex 10.25: y[n] − ½y[n−1] = x[n] + ⅓x[n−1] ⇒ H = (1 + ⅓z⁻¹)/(1 − ½z⁻¹); step response (|z| > ½): "
           "Y = H/(1 − z⁻¹) = (8/3)/(1 − z⁻¹) − (5/3)/(1 − ½z⁻¹) ⇒ y[n] = (8/3)u[n] − (5/3)(½)ⁿu[n]."])
n.figure_from_pdf(B[8], 44, "Figure 19.1 — Causality and stability from the ROC of H(z) (Lec 8, sl. 44)", clip=CLIP, width_cm=12)
# pole-zero plots for 8(b), 8(c)
fig, ax = plt.subplots(1, 3, figsize=(10.5, 3.4))
th = np.linspace(0, 2 * np.pi, 300)
def pz(a, poles, zeros, title, ring=None, double=()):
    a.plot(np.cos(th), np.sin(th), color="#888", lw=0.8)
    a.axhline(0, color="k", lw=0.5); a.axvline(0, color="k", lw=0.5)
    if ring:
        r1, r2 = ring
        a.add_patch(plt.Circle((0, 0), r2, color="#1F4E79", alpha=0.15))
        if r1 > 0:
            a.add_patch(plt.Circle((0, 0), r1, color="white"))
            a.plot(r1 * np.cos(th), r1 * np.sin(th), "--", color="#1F4E79", lw=0.8)
        a.plot(r2 * np.cos(th), r2 * np.sin(th), "--", color="#1F4E79", lw=0.8)
    a.plot([p.real for p in poles], [p.imag for p in poles], "x", color="#C00000", ms=9, mew=2)
    a.plot([p.real for p in zeros], [p.imag for p in zeros], "o", mfc="none", color="#1F4E79", ms=7)
    a.set_aspect("equal"); a.set_xlim(-2.6, 2.6); a.set_ylim(-1.6, 1.6); a.set_title(title, fontsize=9)
    a.tick_params(labelsize=7)
pz(ax[0], [1 / 3, 2 / 3, 2], [], "8(b): FT converges: 2/3 < |z| < 2", ring=(2 / 3, 2))
pz(ax[1], [1 / 3, 2 / 3, 2], [], "right-sided: |z| > 2 (FT diverges)", ring=(2, 2.55))
pz(ax[2], [0.5, 0.5, 2, 2], [0, 0.8 + 0.6j, 0.8 - 0.6j], "8(c): |n|(1/2)^{|n|}, 1/2 < |z| < 2", ring=(0.5, 2))
fig.tight_layout()
pzp = os.path.join(FIG, "ashraf5_pz.png"); fig.savefig(pzp, dpi=170); plt.close(fig)
n.callout("trap", "• Poles are roots in z: 1 − (11/6)z⁻¹ + z⁻² − (1/6)z⁻³ = 0 ⇔ z³ − (11/6)z² + z − 1/6 = 0. • The ring that contains the "
          "unit circle is the only one with a DTFT. • ROC of a sum can exceed the intersection if poles cancel. • "
          "Left-sided/anti-causal sequences use u[−n − 1] with a minus sign.")
n.exam_approach(["Identify the pole radii; list the rings.", "Right-sided → outside the largest pole; left-sided → inside the "
                 "smallest; DTFT exists ⇔ unit circle in the ROC.", "For |n|bⁿ-type sequences split n ≥ 0 and n < 0, "
                 "transform each, intersect the ROCs (a ring)."])
n.practice("Lesson 19", "(a) Actual — CSE 219 2023-24 Q8(b), Q8(c). (b) Practice set 12.1, 12.4.",
           ["(a) (i) Fig. 2 shows the pole-zero plot of Y(z) (poles at 1/3, 2/3 and 2). What can be said about the ROC if: (i) y[n] is "
            "right-sided; (ii) the FT of y[n] converges; (iii) the FT does not converge; (iv) y[n] is left-sided? (8) (ii) z-transform "
            "and pole-zero plot of x[n] = |n|(1/2)^{|n|}. (10)",
            "(b) H(z) = (1 − 2z⁻¹)/((1 − ½z⁻¹)(1 − 2z⁻¹)): valid ROCs, causality, stability and DTFT; h[n] = (2/3)ⁿu[n] − "
            "(4/3)ⁿu[−n−1]: H(z), ROC, causal? stable? DTFT?"])
n.solution()
n.code(["(a)(i) right-sided ⇒ ROC is the exterior of the outermost pole: |z| > 2",
        "    (ii) FT converges ⇔ ROC contains |z| = 1 and no pole: 2/3 < |z| < 2",
        "    (iii) FT does not converge ⇔ the ROC excludes |z| = 1: |z| > 2, or |z| < 1/3, or 1/3 < |z| < 2/3",
        "    (iv) left-sided ⇒ interior of the innermost pole: |z| < 1/3"])
n.figure_image(pzp, "Figure 19.2 — Pole-zero plots with the ROC shaded: 8(b)(ii), 8(b)(i), and 8(c)", width_cm=16.5)
n.code(["(ii) x[n] = |n|aⁿ-type, a = 1/2:  for n ≥ 0: n(½)ⁿu[n] ↔ ½z⁻¹/(1 − ½z⁻¹)², |z| > ½",
        "     for n < 0: x[n] = (−n)(½)^{−n} = (−n)2ⁿ = m(½)^m with m = −n ≥ 1:  Σ_{m≥1} m(½)^m z^{m} = ½z/(1 − ½z)², |z| < 2",
        "     X(z) = ½z⁻¹/(1 − ½z⁻¹)² + ½z/(1 − ½z)² = 2z(5z² − 8z + 5)/((z − 2)²(2z − 1)²),   ½ < |z| < 2",
        "     poles: z = ½ (double), z = 2 (double);  zeros: z = 0 and z = 0.8 ± 0.6j (on the unit circle, 5z² − 8z + 5 = 0)",
        "     the ROC is an annulus containing |z| = 1 ⇒ the DTFT exists. Check: X(1) = 4 = Σ|n|(½)^{|n|} ✓"])
n.code(["(b) H = (1 − 2z⁻¹)/((1 − ½z⁻¹)(1 − 2z⁻¹)): the zero at z = 2 cancels the pole at z = 2 ⇒ H = 1/(1 − ½z⁻¹)",
        "    cancelling: H = 1/(1 − ½z⁻¹) with ROC |z| > ½ (causal; contains the unit circle ⇒ stable, DTFT exists) or |z| < ½",
        "    (anti-causal, unstable). Without cancelling, the rings are |z| > 2, ½ < |z| < 2, |z| < ½ (the 2-pole counts as a boundary).",
        "    h[n] = (2/3)ⁿu[n] − (4/3)ⁿu[−n−1]: H = 1/(1 − (2/3)z⁻¹) + 1/(1 − (4/3)z⁻¹), ROC 2/3 < |z| < 4/3 (the two ROCs",
        "    overlap in a ring) ⇒ two-sided ⇒ non-causal; the ring contains |z| = 1 ⇒ stable and the DTFT exists."])
for k in [("2023-24", "CSE 219", "8(b)"), ("2023-24", "CSE 219", "8(c)")]:
    mark(*k)

n.quick_notes("Quick Notes — z-Transform", "Revision points for Lessons 17–19.",
              [("L17 · ROC", ["X = Σx[n]z^{−n}; z = e^{sT}; DTFT ⇔ ROC ∋ |z| = 1.",
                             "aⁿu ↔ 1/(1−az⁻¹), |z| > |a|; −aⁿu[−n−1], |z| < |a|; right → exterior, left → interior, two-sided → ring.",
                             "Finite sequence: all z except 0 (n > 0 terms) / ∞ (n < 0 terms)."]),
               ("L18 · Inverse", ["x[n] = (1/2πj)∮X z^{n−1}dz; partial fractions in z⁻¹; pole inside the ROC's inner edge → right-sided term.",
                                 "log(1 + az⁻¹), |z| > |a| ⇒ (−1)^{n+1}aⁿ/n, n ≥ 1."]),
               ("L19 · Systems", ["Causal ⇔ exterior ROC incl. ∞; stable ⇔ ROC ∋ unit circle; causal + stable ⇔ poles inside |z| = 1.",
                                 "8(a) 2023-24: poles 1, ½, ⅓: four ROCs; X = 6/(1−z⁻¹) − 3/(1−½z⁻¹) − 2/(1−⅓z⁻¹).",
                                 "8(c): X = 2z(5z²−8z+5)/((z−2)²(2z−1)²), ½ < |z| < 2."])],
              diagrams=[(B[8], 12, "z-transform of aⁿu[n]: pole-zero plot and ROC (Lec 8, sl. 12)", CLIP, 12)])
n.save()
save_solved("ashraf_ztransform")
print("saved", n.out_path)
