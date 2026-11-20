"""Anik F2 — LTI systems, convolution, causality, stability (Lec 3–4). Lessons 6–10."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402

from c219 import A, anik, exam_map, mark, pw, save_solved, sketch  # noqa: E402

CLIP = (0.0, 0.12, 1.0, 0.98)
T = np.linspace

n = anik("Lec 3–4 · LTI Systems, Convolution, Causality and Stability", "CSE219_Anik_LTI_Convolution_Notes.docx")
n.front_matter(
    contents=[("Exam Map — What the TF Papers Ask", "system-property and convolution questions"),
              ("Lesson 6 — Systems and Their Properties", "linearity, time invariance (+ memory, causality, stability, invertibility)"),
              ("Lesson 7 — Discrete Convolution as Polynomial Multiplication", "reflect, shift, multiply, add"),
              ("Lesson 8 — Impulse Response and the Convolution Sum / Integral", "why y = x * h for every LTI system"),
              ("Lesson 9 — Convolution Practice: DT, CT, Graphical, Interconnections", "interval tables, cascades, parallel paths"),
              ("Lesson 10 — Causality and Stability from h(t); h(t) of Simple Systems", "h = 0 for t < 0; ∫|h| < ∞"),
              ("Quick Notes — LTI and Convolution", "merged revision notes + key diagrams")],
    source_note="Slide numbers refer to Lecture-3-Linear-Time-Invariant-Systems-and-Convolution.pdf (59 slides, “Lec 3”) "
                "and Lecture-4-Convolution-Causality-and-Stability.pdf (70 slides, “Lec 4”). Memory, invertibility, "
                "interconnections and impulse responses of differential equations/circuits are textbook background "
                "(marked) — the EEE papers ask them every year.")

n.h1("Exam Map — What the TF Papers Ask")
n.p("Convolution is the single most-asked Anik-part topic outside the transforms: 20 marks in CSE 219 2022-23 (Q8(a)), "
    "15 in 2023-24 (Q1(b)), and a graphical convolution in nearly every EEE paper.")
exam_map(n, "Anik", range(6, 11))
n.callout("focus", "Learn in this order: (1) graphical CT convolution with an interval table (EEE every year) · (2) DT "
          "convolution of one-sided exponentials split into left/right parts (CSE 219 2022-23 Q8(a), 20 marks) · "
          "(3) causal? stable? from h(t) (2022-23 Q8(b), 2023-24 Q3(b)) · (4) interconnected systems: h_eq then y "
          "(2023-24 Q1(b), EEE 2023-24 Q1(c)) · (5) test linear / time-invariant / causal / memoryless / stable for a "
          "given equation.")

# ============================================================ L6
n.lesson("Lesson 6 — Systems and Their Properties", "Slides 2–11 (Lec 3) · memory, causality, stability, invertibility: textbook")
n.h2("1. What a System Is (sl. 3–5)")
n.p("A system takes a **whole input signal** and produces a whole output signal: x(t) → S → y(t) (or x[n] → y[n]). "
    "It is not a number-to-number function.")
n.h2("2. Linearity and Time Invariance (sl. 7–11)")
n.bullets(["**Homogeneity**: a x(t) → a y(t). **Additivity**: x₁ + x₂ → y₁ + y₂. Together: a x₁ + b x₂ → a y₁ + b y₂.",
           "**Time invariance**: x(t − t₀) → y(t − t₀): delaying the input only delays the output.",
           "**LTI** = both. Payoff: one special response (the impulse response) gives the output for every input."])
n.h2("3. Other Properties (textbook)")
n.table(["Property", "Definition", "Quick test"],
        [["Memoryless", "y(t) depends only on x(t) at the same t", "any x(t − a), integral or derivative ⇒ memory"],
         ["Causal", "y(t) depends only on x(τ), τ ≤ t", "look for x(t + a), x(−t), x(2t), upper limit > t"],
         ["Stable (BIBO)", "|x| ≤ B ⇒ |y| ≤ M", "try x = constant, x = u(t); look for t·x, ∫x, 1/x, log x"],
         ["Invertible", "distinct inputs → distinct outputs", "|x|, x², cos x, multiplying by something that can be 0 ⇒ not"],
         ["Time-invariant", "x(t − t₀) → y(t − t₀)", "t appearing outside x(·), or x(2t), x(−t) ⇒ variant"]],
        widths_cm=[3.0, 6.2, 8.0])
n.callout("memorize", "Linearity test: (1) zero input must give zero output (an added constant or −πt breaks it); "
          "(2) y must contain x only to the first power, inside no non-linear function. Time-invariance test: compute "
          "y₁ = S{x(t − t₀)} and y(t − t₀) separately and compare.")
n.callout("trap", "• y = x(2t), y = x(−t) are linear but time-variant and non-causal. • A system with a coefficient "
          "depending on t (t²y, t·x) is time-variant even though it is linear. • A differential equation is linear only "
          "with zero initial conditions.")
n.exam_approach(["Linearity: apply a x₁ + b x₂ and compare with a y₁ + b y₂.",
                 "TI: compare S{x(t − t₀)} with y(t − t₀).",
                 "Causality/memory: list every time instant of x used to compute y(t).",
                 "Stability: find a bounded input with unbounded output (counterexample), or bound |y|.",
                 "Answer each property with one line of justification."])
n.practice("Lesson 6",
           "(a) Actual — EEE 211 2019-20 Q1. (b) Actual — EEE 211 2023-24 Q1(b) / 2022-23 Q8(b). (c) Actual — EEE 211 "
           "2020-21 Q6(a). (d) Actual — EEE 211 2022-23 Q5(b). (e) Older papers, quick answers.",
           ["(a) y(t) = (1/3)∫x(τ)[δ(t − τ) + δ(t − τ + t₀) + δ(t − τ − t₀)]dτ. What does it do? Is it BIBO-stable, linear, "
            "memoryless, causal, time-invariant? (35)",
            "(b) dy/dt + t²y = (2t + 3)x(t): linear? time-invariant?",
            "(c) y(t) = t·x(t + 2): linear, causal, time-variant, memoryless, stable? (15)",
            "(d) An LTI system maps x(t) = |t| (|t| ≤ 1, 0 elsewhere) to y(t) = 1 (|t| ≤ 1). Sketch the outputs for "
            "(i) x(t − ½) − x(t + ½), (ii) dx/dt. (15)",
            "(e) (i) y = sin{x(t) + x(t − 2)}; (ii) y = sin(2t)log₁₀x(t); (iii) y = ∫_{−∞}^{2t−3}x dτ; (iv) y = ½|x(t)| − πt; "
            "(v) y = x_e − x_o; (vi) y = 2x cos ω_c t; (vii) y = At·x(t); (viii) y = ∫₀ᵗ e^{−(t−τ)}x(τ)dτ; "
            "(ix) y = k₁cos[k₂t + ∫₀ᵗ k₃x dτ]."])
n.solution()
n.answer("(a)", "Sifting each impulse: y(t) = (1/3)[x(t) + x(t + t₀) + x(t − t₀)] — a **three-point moving average** "
         "(smoothing / low-pass filter). Linear: yes (sum of shifted copies). Time-invariant: yes (x(t − a) gives "
         "y(t − a)); h(t) = (1/3)[δ(t) + δ(t + t₀) + δ(t − t₀)]. Memoryless: no (uses t ± t₀). Causal: no for t₀ ≠ 0 "
         "(uses x(t + t₀); h ≠ 0 at t = −t₀). BIBO-stable: yes, |y| ≤ (1/3)(B + B + B) = B (∫|h| = 1).")
n.answer("(b)", "Linear: if x₁ → y₁, x₂ → y₂ then a x₁ + b x₂ satisfies the equation with a y₁ + b y₂ (all terms are first "
         "power in x and y, zero initial state) ⇒ **linear**. Time-variant: with input x(t − t₀) the solution y₁ obeys "
         "y₁′ + t²y₁ = (2t + 3)x(t − t₀), while y(t − t₀) obeys y′ + (t − t₀)²y = (2t − 2t₀ + 3)x(t − t₀) — different "
         "coefficients ⇒ **time-variant**.")
n.answer("(c)", "Linear (a x₁ + b x₂ → t(a x₁ + b x₂)(t + 2)). Non-causal (uses x(t + 2), the future). Time-variant: "
         "S{x(t − t₀)} = t x(t − t₀ + 2) ≠ y(t − t₀) = (t − t₀)x(t − t₀ + 2). Has memory (uses t + 2). Unstable: x = 1 "
         "gives y = t → ∞.")
n.answer("(d)", "Use linearity and time invariance on the given pair: (i) output = y(t − ½) − y(t + ½) = −1 on (−3/2, −½), "
         "0 on (−½, ½), +1 on (½, 3/2). (ii) Differentiation commutes with an LTI system (derivative = limit of a "
         "difference of shifted inputs), so output = dy/dt = δ(t + 1) − δ(t − 1).")
n.code(["(e)          linear  TI   causal  memoryless  stable  invertible",
        "(i)           no     yes   yes       no         yes      no",
        "(ii)          no     no    yes       yes        no       no (sin 2t = 0 at some t)",
        "(iii)         yes    no    no        no         no       yes (y′(t) = 2x(2t − 3))",
        "(iv)          no     no    yes       yes        no       no (|x|)",
        "(v) = x(−t)   yes    no    no        no         yes      yes (inverse = itself)",
        "(vi)          yes    no    yes       yes        yes      no (cos ω_c t = 0)",
        "(vii)         yes    no    yes       yes        no       no (t = 0)",
        "(viii)        yes    for inputs starting at t ≥ 0 it is LTI with h = e^{−t}u(t); ∫|h| = 1 ⇒ stable",
        "(ix)          no     no    yes       no         yes (|y| ≤ |k₁|)"])
mark("2019-20", "EEE 211", "1"); mark("2023-24", "EEE 211", "1(b)"); mark("2022-23", "EEE 211", "8(b)")
mark("2020-21", "EEE 211", "6(a)"); mark("2022-23", "EEE 211", "5(b)")
for k in [("2015-16", "EEE 301", "2(b)"), ("2014-15", "EEE 301", "2(a)"), ("2012-13", "EEE 301", "2(a)"),
          ("2012-13", "EEE 301", "1(c)"), ("2011-12", "EEE 301", "7(a)"), ("2010-11", "EEE 301", "7(a)"),
          ("2013-14", "EEE 301", "2(b)"), ("2017-18", "EEE 211", "6(b)"), ("2014-15", "CSE 311", "7(a)"),
          ("2014-15", "CSE 311", "1(b) [L-3]")]:
    mark(*k)
for k in [("2021-22", "EEE 211", "2(b)"), ("2018-19", "EEE 211", "7(a)"), ("2017-18", "EEE 211", "6(a)")]:
    mark(*k, "◐ Method")

# ============================================================ L7
n.lesson("Lesson 7 — Discrete Convolution as Polynomial Multiplication", "Slides 12–31 (Lec 3)")
n.p("Multiply A(z) = 1 + 3z + 2z² + 5z³ + 4z⁴ by B(z) = 2 − z + 4z² + z³ + 3z⁴. The coefficient of z⁴ collects every "
    "product whose powers add to 4 (sl. 14–15):")
n.code(["c[4] = a0b4 + a1b3 + a2b2 + a3b1 + a4b0 = 1·3 + 3·1 + 2·4 + 5·(−1) + 4·2 = 17"])
n.formula(["c[n] = (a * b)[n] = Σₖ a[k] b[n − k]"])
n.p("b[n − k] means: **reflect** b (b[−k]), then **shift** it right by n, multiply the samples that line up, and add "
    "(sl. 17–22). Convolution is commutative: a * b = b * a (polynomial product order does not matter, sl. 29–30).")
n.figure_from_pdf(A[3], 15, "Figure 7.1 — The z⁴ coefficient comes from criss-crossed pairings (Lec 3, sl. 15)", clip=CLIP, width_cm=10)
n.h2("Worked Example (sl. 23–28)")
n.code(["x = {1, 2, 1, 1},  h = {1, 1, −1, 2}  (both start at n = 0)",
        "n:     0    1    2    3    4    5    6",
        "y:     1    3    2    2    4    1    2",
        "e.g. y[3] = 1·2 + 2·(−1) + 1·1 + 1·1 = 2;   length = 4 + 4 − 1 = 7"])
n.callout("memorize", "Finite sequences: start index = sum of start indices, length = L + M − 1, Σy = (Σx)(Σh) (quick check: "
          "5 × 3 = 15 = 1+3+2+2+4+1+2 ✓). Fast hand method: multiply as polynomials, or use a sliding-strip table.")
n.exam_approach(["Write both sequences with their index ranges.", "Reflect h, slide one step at a time, multiply-add "
                 "the overlap (or multiply polynomials).", "Check: start index, length, and Σy = Σx·Σh."])
n.practice("Lesson 7", "(a) Practice set 3.1. (b) Practice set 3.3. (c) Constructed.",
           ["(a) x = {1, 2} (n = 0, 1), h = {1, −1, 2} (n = 0, 1, 2). Find y = x * h.",
            "(b) x[n] is zero except x[−1] = 2, x[0] = −1, x[2] = 3. Write x as shifted impulses and y in terms of h.",
            "(c) Find the coefficient of z⁵ in A(z)B(z) of the slide example."])
n.solution()
n.answer("(a)", "(1 + 2z)(1 − z + 2z²) = 1 + z + 0z² + 4z³ → y = {1, 1, 0, 4}, n = 0…3. Check Σ: 3·2 = 6 ✓.")
n.answer("(b)", "x[n] = 2δ[n + 1] − δ[n] + 3δ[n − 2] ⇒ y[n] = 2h[n + 1] − h[n] + 3h[n − 2].")
n.answer("(c)", "c[5] = a1b4 + a2b3 + a3b2 + a4b1 = 3·3 + 2·1 + 5·4 + 4·(−1) = 27.")

# ============================================================ L8
n.lesson("Lesson 8 — Impulse Response and the Convolution Sum / Integral", "Slides 32–57 (Lec 3), 2–9 (Lec 4)")
n.p("Philosophy (sl. 34–37): solve for the simplest input, break any input into such pieces, combine the answers "
    "(like counting factors of 72 = 2³·3²: (3+1)(2+1) = 12).")
n.bullets(["Simplest input: δ[n]. Its output is the **impulse response** h[n] — the system's signature (sl. 38–40).",
           "Echo system: h[n] = u[n] (equal echoes forever); h = αⁿu[n], 0 < α < 1: fading echoes, larger α fades "
           "slower (sl. 42–44). Pure delay by 3: h[n] = δ[n − 3] (CT: δ(t − 3)) (sl. 45–46).",
           "Input x = δ[n] + 2δ[n−1] − δ[n−2] + δ[n−3] into h = u[n]: y = u[n] + 2u[n−1] − u[n−2] + u[n−3] = 1, 3, 2, 3, 3, … "
           "(sl. 47–51)."])
n.h2("Derivation (sl. 52–57) — exam-ready")
n.code(["1. Any input is a sum of shifted, scaled impulses:  x[n] = Σₖ x[k] δ[n − k]",
        "2. Time invariance:  δ[n − k] → h[n − k]",
        "3. Homogeneity:      x[k]δ[n − k] → x[k]h[n − k]",
        "4. Additivity:       y[n] = Σₖ x[k] h[n − k] = (x * h)[n]",
        "CT (textbook): x(t) = ∫ x(τ) δ(t − τ) dτ (sifting) → same steps with ∫ ⇒ y(t) = ∫ x(τ) h(t − τ) dτ"])
n.figure_from_pdf(A[3], 55, "Figure 8.1 — Input decomposition becomes output summation (Lec 3, sl. 55)", clip=CLIP, width_cm=10)
n.p("**CT convolution** (Lec 4, sl. 6–8): y(t) = ∫ x(τ)h(t − τ)dτ. Fix t, slide h(t − τ) along τ, integrate the product "
    "over the overlap. Same recipe: choose the output point, reflect and shift, multiply and add.")
n.callout("answer", "Why convolution matters in real life (EEE 301 2011-12 Q7(c)): once h(t) is measured (hit the "
          "system with an impulse — clap in a hall, tap a structure), the output for every input is x * h without "
          "re-solving the system: reverb/echo simulation, sensor smoothing (moving average), image blurring and "
          "sharpening, channel modelling in communications.")
n.practice("Lesson 8", "(a) Actual — CSE 311 2018-19 Q4(b). (b) Actual — EEE 301 2011-12 Q7(c). (c) Practice set 4.9–4.11.",
           ["(a) Prove that for an input x(t), the output of an LTI system with impulse response h(t) is y = x * h, using "
            "only time-domain arguments. (17)",
            "(b) Mention the importance of y = x * h in real-life applications. (4)",
            "(c) How can convolution simulate a large hall, smooth sensor readings, and add an echo?"])
n.solution()
n.answer("(a)", "By the sifting property x(t) = ∫x(τ)δ(t − τ)dτ: x is a continuum of impulses of strength x(τ)dτ at t = τ. "
         "Let δ(t) → h(t). Time invariance: δ(t − τ) → h(t − τ). Homogeneity: x(τ)dτ δ(t − τ) → x(τ)dτ h(t − τ). "
         "Additivity (the integral is a limit of sums): y(t) = ∫x(τ)h(t − τ)dτ = x(t) * h(t). Every step uses only L and TI.")
n.answer("(b)", "See the EXAM-READY ANSWER above.")
n.answer("(c)", "Hall: record the hall's impulse response (a clap or balloon pop) and convolve the dry voice with it. "
         "Smoothing: convolve readings with a short averaging kernel h = (1/M)Σδ[n − k], k = 0…M−1. Echo: h[n] = δ[n] + "
         "aδ[n − D]; D sets the delay, a (< 1) the strength; more taps (a, a², …) give repeated echoes.")
mark("2018-19", "CSE 311", "4(b)"); mark("2011-12", "EEE 301", "7(c)")

# ============================================================ L9
n.lesson("Lesson 9 — Convolution Practice: DT, CT, Graphical, Interconnections",
         "Slides 10–52 (Lec 4) · interconnections: textbook")
n.h2("1. Slide Examples")
n.table(["Example", "Signals", "Result"],
        [["Ex 2.2 (sl. 11–19)", "x = {0.5, 2}, h = {1, 1, 1}", "y = {0.5, 2.5, 2.5, 2}, n = 0…3"],
         ["Ex 2.3 (sl. 20–27)", "αⁿu[n] * u[n]", "(1 − α^{n+1})/(1 − α) u[n] → 1/(1 − α)"],
         ["Ex 2.5 (sl. 28–34)", "2ⁿu[−n] * u[n]", "2^{n+1} (n < 0); 2 (n ≥ 0)"],
         ["Ex 2.6 (sl. 35–40)", "e^{−at}u(t) * u(t)", "(1/a)(1 − e^{−at})u(t)"],
         ["Ex 2.10 (sl. 42–47)", "[(½)ⁿu[n] + 2ⁿu[−n]] * u[n]", "2^{n+1} (n < 0); 4 − 2^{−n} (n ≥ 0)"],
         ["sl. 48–52", "eᵗu(−t) * e^{−t}u(t)", "½e^{t} (t < 0); ½e^{−t} (t ≥ 0) = ½e^{−|t|}"]],
        widths_cm=[3.3, 6.0, 7.9])
n.p("Key step of every infinite-length example: find the overlap. For x[k] = αᵏu[k] and h[n − k] = u[n − k], x is "
    "nonzero for k ≥ 0 and h[n − k] for k ≤ n ⇒ overlap 0 ≤ k ≤ n (empty for n < 0). Then sum a geometric series:")
n.formula(["Σ_{k=0}^{n} αᵏ = (1 − α^{n+1})/(1 − α)          Σ_{k=−∞}^{m} βᵏ = β^{m}/(1 − 1/β)  (β > 1)"])
n.p("**Distributivity** (sl. 41): x * (h₁ + h₂) = x * h₁ + x * h₂ — split a two-sided input into its left and right "
    "parts, convolve separately, add.")
n.figure_from_pdf(A[4], 50, "Figure 9.1 — CT overlap for t < 0 ends at τ = t (Lec 4, sl. 50)", clip=CLIP, width_cm=10)
n.h2("2. Graphical CT Convolution — the Interval Table")
n.bullets(["Choose the simpler signal to flip (often the rectangle).",
           "Write the edges of h(t − τ) as functions of t; list the t-intervals where the overlap changes "
           "(edge of one passes edge of the other).",
           "On each interval write the integral limits and evaluate; check continuity at interval ends.",
           "Useful shortcut: x = rect on (a, b) ⇒ y(t) = ∫_{t−b}^{t−a} h(s)ds = H(t − a) − H(t − b), H = running integral of h."])
n.h2("3. Interconnections (textbook)")
n.formula(["Cascade: h = h₁ * h₂          Parallel: h = h₁ + h₂          δ(t − a) * h(t) = h(t − a)"])
n.code(["Useful pair:  e^{−at}u(t) * e^{−bt}u(t) = [e^{−bt} − e^{−at}]/(a − b) · u(t)     (a ≠ b)",
        "              e^{−at}u(t) * e^{−at}u(t) = t e^{−at}u(t)"])
n.callout("trap", "• Do not forget the n < 0 (t < 0) region: one-sided signals often give a nonzero left tail "
          "(Ex 2.5). • u[n + 3] starts at n = −3: shift the summation limits. • Interval ends are where the "
          "edges meet — write them as t-values before integrating.")
n.exam_approach(["Sketch both signals; decide which to flip.", "Find the overlap limits as functions of n (or t) and "
                 "split into cases.", "Evaluate each sum/integral; geometric series for exponentials.",
                 "Check continuity at case boundaries, the support (sum of supports) and the area (∫y = ∫x·∫h)."])

# --- CSE 219 practice
nn = np.arange(-8, 8)
yv = np.where(nn <= -4, 256 * 3.0 ** (nn + 4) / 11, 256 / 3.0 ** (nn + 3) - (32 / 11) * 0.25 ** nn)
sk8 = sketch("anik2_q8a", [dict(title="y[n] (CSE 219 2022-23 Q8(a))", stems=[(nn, yv)], xlabel="n", xticks=range(-8, 8))],
             size=(6.5, 2.4))
n.practice("Lesson 9", "(a) Actual — CSE 219 2022-23 Q8(a). (b) Actual — CSE 219 2023-24 Q1(b). (c) Actual — EEE 211 "
           "2023-24 Q1(c).",
           ["(a) Convolve x[n] = 3ⁿu[−n − 1] + (1/3)ⁿu[n] with h[n] = (1/4)ⁿu[n + 3]. (20)",
            "(b) h₁ = δ[n] − δ[n − 2] and h₂ = u[n − 1] in parallel, followed by h₃ = δ[n] − δ[n − 1]. (i) h_eq; (ii) y for "
            "x = u[n]. (15)",
            "(c) x feeds three paths — h₁; h₂ followed by h₃; h₄ — which are added and passed through h₅. h₁ = e^{−2t}u, "
            "h₂ = e^{−2t}u, h₃ = e^{−t}u, h₄ = δ(t), h₅ = e^{−3t}u. Using time-domain techniques: (i) is it BIBO stable? "
            "(ii) y for x = e^{−t}u(t). (17)"])
n.solution()
n.answer("(a)", "Split x = x₁ + x₂ (distributivity), x₁ = 3ⁿu[−n−1], x₂ = (1/3)ⁿu[n]. h[n − k] = (¼)^{n−k} is nonzero for "
         "k ≤ n + 3.")
n.code(["y1[n] = Σ_{k ≤ min(−1, n+3)} 3^k (1/4)^{n−k} = 4^{−n} Σ 12^k",
        "  n ≤ −4: upper limit n+3:  4^{−n}·12^{n+3}·(12/11) = 256·3^{n+4}/11",
        "  n ≥ −3: upper limit −1:   4^{−n}·(1/12)/(1 − 1/12) = 4^{−n}/11",
        "y2[n] = Σ_{k=0}^{n+3} (1/3)^k (1/4)^{n−k}  (n ≥ −3) = 4^{−n} Σ_{k=0}^{n+3} (4/3)^k",
        "      = 4^{−n}·[(4/3)^{n+4} − 1]/(1/3) = 256·3^{−(n+3)} − 3·4^{−n};   0 for n < −3",
        "",
        "y[n] = 256·3^{n+4}/11                       n ≤ −4",
        "       256·3^{−(n+3)} − (32/11)·4^{−n}       n ≥ −3",
        "Values: y[−4] = 23.27, y[−3] = 69.82, y[−2] = 38.79, y[−1] = 16.81, y[0] = 6.57, y[1] = 2.43"])
n.figure_image(sk8, "Figure 9.2 — Output of CSE 219 2022-23 Q8(a): rises as 3ⁿ on the left, peaks at n = −3, decays on the right", width_cm=13)
n.answer("(b)", "Parallel then cascade: h_eq = (h₁ + h₂) * h₃. u[n − 1] * (δ[n] − δ[n − 1]) = u[n − 1] − u[n − 2] = δ[n − 1]; "
         "(δ[n] − δ[n − 2]) * (δ[n] − δ[n − 1]) = δ[n] − δ[n−1] − δ[n−2] + δ[n−3]. Adding:")
n.code(["(i)  h_eq[n] = δ[n] − δ[n − 2] + δ[n − 3]",
        "(ii) y[n] = u[n] * h_eq = u[n] − u[n − 2] + u[n − 3]",
        "     n:   <0   0   1   2   3   4 …",
        "     y:    0   1   1   0   1   1 …"])
n.answer("(c)", "Middle path: h₂ * h₃ = e^{−2t}u * e^{−t}u = (e^{−t} − e^{−2t})u. Sum of the three paths: g = e^{−2t}u + "
         "(e^{−t} − e^{−2t})u + δ(t) = δ(t) + e^{−t}u(t). Then")
n.code(["h_eq = g * h5 = e^{−3t}u + e^{−t}u * e^{−3t}u = e^{−3t}u + ½(e^{−t} − e^{−3t})u = ½(e^{−t} + e^{−3t})u(t)",
        "(i)  ∫|h_eq| dt = ½(1 + 1/3) = 2/3 < ∞  ⇒ BIBO stable (also causal)",
        "(ii) y = e^{−t}u * ½(e^{−t} + e^{−3t})u = ½ t e^{−t}u + ¼(e^{−t} − e^{−3t})u",
        "     y(t) = [ ½ t e^{−t} + ¼ e^{−t} − ¼ e^{−3t} ] u(t)"])
mark("2022-23", "CSE 219", "8(a)"); mark("2023-24", "CSE 219", "1(b)"); mark("2023-24", "EEE 211", "1(c)")
for k in [("2016-17", "EEE 211", "1(b)"), ("2010-11", "EEE 301", "6(b)(ii)")]:
    mark(*k, "◐ Method")

# --- graphical practice
tri = lambda s: np.clip(1 - np.abs(s), 0, None)
tt = T(-2, 6, 3201)
yA = pw(tt, [(0, 1, lambda s: s * s / 2), (1, 2, lambda s: -s * s + 3 * s - 1.5), (2, 3, lambda s: (3 - s) ** 2 / 2)])
yB = pw(tt, [(0, 1, lambda s: s * s / 2), (1, 2, lambda s: 1 - (2 - s) ** 2 / 2), (2, 3, lambda s: 1 - (s - 2) ** 2 / 2),
             (3, 4, lambda s: (4 - s) ** 2 / 2)])
yC = pw(tt, [(0, 1, lambda s: s * s), (1, 2, lambda s: -2 * s * s + 6 * s - 3), (2, 3, lambda s: (3 - s) ** 2)]) + tri(tt - 4)
yD = pw(tt, [(-1, 0, lambda s: (s + 1) ** 2 / 2), (0, 1, lambda s: 0.5 + 0 * s), (1, 2, lambda s: 0.5 - (s - 1) ** 2 / 2)])
yE = pw(tt, [(0, 1, lambda s: s ** 3 / 6), (1, 2, lambda s: -s ** 3 / 6 + s - 2 / 3)])
skg = sketch("anik2_graph", [
    dict(title="EEE 23-24 Q2(a): rect(1,2) * tri", curves=[(tt, yA)], xlim=(-1, 4)),
    dict(title="EEE 19-20 Q2: rect(0,2) * h", curves=[(tt, yB)], xlim=(-1, 5)),
    dict(title="EEE 21-22 Q2(a)", curves=[(tt, yC)], xlim=(-1, 6)),
    dict(title="EEE 20-21 Q6(b)", curves=[(tt, yD)], xlim=(-2, 3)),
    dict(title="EEE 22-23 Q7(b): t·rect * t·rect", curves=[(tt, yE)], xlim=(-1, 3))], ncols=3)
n.practice("Lesson 9 (continued) — Graphical Convolution",
           "(d) Actual — EEE 211 2023-24 Q2(a). (e) Actual — EEE 211 2019-20 Q2. (f) Actual — EEE 211 2021-22 Q2(a). "
           "(g) Actual — EEE 211 2020-21 Q6(b). (h) Actual — EEE 211 2022-23 Q7(b). (i) Older: EEE 301 2010-11 Q6(b)(i), "
           "EEE 211 2018-19 Q7(b), EEE 301 2011-12 Q7(d), 2012-13 Q2(b), 2015-16 Q3(b).",
           ["(d) x = 1 on (1, 2); h = triangle on (−1, 1), peak 1 at 0. Find y = x * h graphically. (18)",
            "(e) x = 1 on (0, 2); h(t + 1) is the triangle on (−1, 1). (i) Causal? (ii) y = x * h. (iii) What does the system do? "
            "(iv) Output for z = x(t) − x(t − 4). (35)",
            "(f) x = triangle on (0, 2), peak 1 at t = 1; h = 2 on (0, 1) plus an impulse δ(t − 3). Find y graphically and "
            "analytically. (17)",
            "(g) x = rect(t/2), h = r(t)u(−t + 1). Find y. (10)",
            "(h) x(t) = h(t) = t[u(t) − u(t − 1)]: find y(t) for all t. (15)",
            "(i) Older papers (see solutions)."])
n.solution()
n.answer("(d)", "Flip the rectangle: y(t) = ∫_{t−2}^{t−1} tri(s)ds. Let F(s) = running integral of the triangle: 0 (s < −1), "
         "(s + 1)²/2 (−1..0), 1 − (1 − s)²/2 (0..1), 1 (s > 1). y = F(t − 1) − F(t − 2):")
n.code(["interval    overlap                    y(t)",
        "t < 0       none                       0",
        "0 ≤ t ≤ 1   left edge of tri          t²/2",
        "1 ≤ t ≤ 2   rect covers the peak      −t² + 3t − 3/2      (max 3/4 at t = 1.5)",
        "2 ≤ t ≤ 3   right edge                (3 − t)²/2",
        "t > 3       none                       0           check: area = 1·1 = 1 ✓"])
n.answer("(e)", "(i) h(t) = triangle on (0, 2) with peak 1 at t = 1 ⇒ h = 0 for t < 0 ⇒ **causal**. (ii) y = F(t − 1) − F(t − 3):")
n.code(["0 ≤ t ≤ 1: t²/2        1 ≤ t ≤ 2: 1 − (2 − t)²/2        2 ≤ t ≤ 3: 1 − (t − 2)²/2        3 ≤ t ≤ 4: (4 − t)²/2",
        "(iii) a smoothing (low-pass, triangular-weighted moving average) filter with a delay of 1: the sharp",
        "      edges of x become smooth S-curves, the duration grows from 2 to 4, peak y(2) = 1, area 2·1 = 2 ✓",
        "(iv) z → y(t) − y(t − 4): the pulse above on [0, 4] followed by its negative on [4, 8]"])
n.answer("(f)", "h = 2[u(t) − u(t − 1)] + δ(t − 3). The impulse part gives x(t − 3) (triangle on (3, 5)). The rectangle part: "
         "2∫_{t−1}^{t} x(s)ds:")
n.code(["0 ≤ t ≤ 1: t²      1 ≤ t ≤ 2: −2t² + 6t − 3      2 ≤ t ≤ 3: (3 − t)²",
        "plus 3 ≤ t ≤ 4: t − 3,  4 ≤ t ≤ 5: 5 − t   (the delayed triangle)",
        "y(t) = t²[u(t) − u(t−1)] + (−2t² + 6t − 3)[u(t−1) − u(t−2)] + (3−t)²[u(t−2) − u(t−3)] + x(t − 3)"])
n.answer("(g)", "x = 1 on (−1, 1); h = t on (0, 1). y = ∫_{t−1}^{t+1}h(s)ds = H(t + 1) − H(t − 1), H(s) = s²/2 on [0,1], ½ after:")
n.code(["−1 ≤ t ≤ 0: (t + 1)²/2      0 ≤ t ≤ 1: 1/2      1 ≤ t ≤ 2: 1/2 − (t − 1)²/2      else 0"])
n.answer("(h)", "Overlap 0 ≤ τ ≤ t for 0 ≤ t ≤ 1 and t − 1 ≤ τ ≤ 1 for 1 ≤ t ≤ 2:")
n.code(["0 ≤ t ≤ 1: ∫₀ᵗ τ(t − τ)dτ = t³/6",
        "1 ≤ t ≤ 2: ∫_{t−1}^{1} τ(t − τ)dτ = −t³/6 + t − 2/3      (continuous: 1/6 at t = 1, 0 at t = 2)",
        "otherwise 0"])
n.figure_image(skg, "Figure 9.3 — Outputs of the graphical-convolution questions (d)–(h)", width_cm=16.5)
n.answer("(i)", "EEE 301 2010-11 Q6(b)(i): x = 1 on (0, 2), h = tri: (t+1)²/2 [−1,0]; 1 − (1−t)²/2 [0,1]; 1 − (t−1)²/2 [1,2]; "
         "(3−t)²/2 [2,3]. EEE 211 2018-19 Q7(b): x = t² on (0, 3), h = 1 on (0, 1): y = t³/3 [0,1]; [t³ − (t−1)³]/3 [1,3]; "
         "[27 − (t−1)³]/3 [3,4]. EEE 301 2011-12 Q7(d): g = x(t + 4) + x(t − 4); y = P(t + 4) + P(t − 4) with P = rect(−1,1) "
         "* tri = (t+2)²/2 [−2,−1], 1 − t²/2 [−1,1], (2−t)²/2 [1,2]. EEE 301 2012-13 Q2(b): δ(t+1)*δ(t−1) = δ(t), so "
         "h = δ(t) + rect(t/2); y = Σ(−1)ᵏ[δ(t − 10k) + rect((t − 10k)/2)]. EEE 301 2015-16 Q3(b): step response "
         "−1/6 + ½e^{−2t} − ⅓e^{−3t}; response to e^{−t}u: −½e^{−t} + e^{−2t} − ½e^{−3t} (all × u(t)). EEE 211 "
         "2017-18 Q7(b): h₁ * h₂ = (t − 1)e^{−t} + e^{−2t} = t e^{−t} − e^{−t} + e^{−2t} (three parallel branches).")
for k in [("2023-24", "EEE 211", "2(a)"), ("2019-20", "EEE 211", "2"), ("2021-22", "EEE 211", "2(a)"),
          ("2020-21", "EEE 211", "6(b)"), ("2022-23", "EEE 211", "7(b)"), ("2010-11", "EEE 301", "6(b)(i)"),
          ("2018-19", "EEE 211", "7(b)"), ("2011-12", "EEE 301", "7(d)"), ("2012-13", "EEE 301", "2(b)"),
          ("2015-16", "EEE 301", "3(b)")]:
    mark(*k)
mark("2017-18", "EEE 211", "7(b)", "◐ Method"); mark("2017-18", "EEE 211", "7(a)", "◐ Method")

# ============================================================ L10
n.lesson("Lesson 10 — Causality and Stability from h(t); h(t) of Simple Systems",
         "Slides 53–69 (Lec 4) · impulse responses of differential equations and circuits: textbook")
n.formula(["causal ⇔ h(t) = 0 for t < 0  (h[n] = 0, n < 0)", "BIBO stable ⇔ ∫|h(t)|dt < ∞  (Σ|h[n]| < ∞)"])
n.p("Why (sl. 58): |y(t)| = |∫h(τ)x(t − τ)dτ| ≤ B∫|h(τ)|dτ. Periodic h (sl. 60–62): a nonzero periodic h cannot be "
    "causal (any nonzero value repeats at t₀ − kT < 0) and cannot be stable (area A per period, infinitely many periods).")
n.figure_from_pdf(A[4], 55, "Figure 10.1 — Causal vs non-causal impulse responses (Lec 4, sl. 55)", clip=CLIP, width_cm=10)
n.code(["Slide examples:  h1 = e^{2t}u(−2 − t): nonzero for t ≤ −2 ⇒ non-causal;  ∫_{−∞}^{−2} e^{2t} = e^{−4}/2 ⇒ stable",
        "                 h2 = t e^{−t}u(t): causal;  ∫₀^∞ t e^{−t} dt = 1 ⇒ stable",
        "Minimum delay to make e^{−2t}u(t + 2) causal (sl. 68–69): start −2 + a ≥ 0 ⇒ a ≥ 2"])
n.h2("Impulse Response of a First/Second-Order System (textbook)")
n.code(["y′ + a y = b x         ⇒ h(t) = b e^{−at}u(t)",
        "Series RC, output v_C: RC v′ + v = x  ⇒ h_C = (1/RC) e^{−t/RC} u(t)",
        "Series RC, output v_R = x − v_C       ⇒ h_R = δ(t) − (1/RC) e^{−t/RC} u(t)",
        "Series L, shunt C (output v_C): LC y″ + y = x ⇒ h = ω₀ sin(ω₀t) u(t), ω₀ = 1/√(LC)",
        "Method: for t > 0 solve the homogeneous equation; the impulse sets the initial conditions",
        "        (order n: h^{(n−1)}(0⁺) = 1/a_n, lower derivatives 0; a δ in h appears if numerator order = n)"])
n.callout("trap", "• u(3 − t) and u(−2 − t) extend to −∞: non-causal. • e^{−4t}u(3 − t) grows as t → −∞: unstable. "
          "• Even e^{−6|t|} is non-causal (nonzero for t < 0) though stable.")
n.exam_approach(["Causality: find the support of h; any nonzero part at t < 0 ⇒ non-causal.",
                 "Stability: compute ∫|h| (split piecewise); exponentials: check decay in both directions.",
                 "For an equation/circuit: get the ODE, solve the homogeneous part for t > 0, impose the impulse jump conditions."])
n.practice("Lesson 10", "(a) Actual — CSE 219 2022-23 Q8(b). (b) Actual — CSE 219 2023-24 Q3(b). (c) Actual — EEE 211 "
           "2023-24 Q2(b). (d) Actual — EEE 211 2020-21 Q6(c). (e) Older: EEE 211 2016-17 Q1(a), Q3(c); EEE 301 2014-15 Q2(b).",
           ["(a) Causal? stable? h₁ = e^{2t}u(−2 − t), h₂ = te^{−t}u(t). (10)",
            "(b) Causal and/or stable? (i) e^{−4t}u(3 − t); (ii) e^{−6|t|}; (iii) te^{−t}u(t). (15)",
            "(c) Find, in the time domain, the impulse response of the LC circuit (series L, output across shunt C). (17)",
            "(d) RC series circuit, output v_R, initially relaxed: h(t) by time-domain analysis. (10)",
            "(e) (i) memoryless/causal/stable: δ(t) − δ(t − 2), 2rect(t/2), 2e^{−4t}u, (1 − e^{−4t})u; (ii) y′ + 10y = 2x: "
            "h(t) and output for x = Σ_{k=−2}^{2}(−1)ᵏδ(t − 5k)."])
n.solution()
n.answer("(a)", "h₁: nonzero for t ≤ −2 ⇒ **non-causal**; ∫_{−∞}^{−2}e^{2t}dt = e^{−4}/2 < ∞ ⇒ **stable**. h₂: zero for t < 0 "
         "⇒ **causal**; ∫₀^∞ te^{−t}dt = 1 ⇒ **stable**.")
n.answer("(b)", "(i) nonzero for all t < 3 ⇒ non-causal; ∫_{−∞}^{3}e^{−4t}dt = ∞ (grows as t → −∞) ⇒ unstable. (ii) nonzero for "
         "t < 0 ⇒ non-causal; ∫e^{−6|t|} = 2·(1/6) = 1/3 ⇒ stable. (iii) causal, ∫ = 1 ⇒ stable.")
n.answer("(c)", "KVL: x = L di/dt + y, i = C dy/dt ⇒ LC y″ + y = x. For t > 0 with x = δ: LC h″ + h = 0 ⇒ h = A cos ω₀t + "
         "B sin ω₀t, ω₀ = 1/√(LC). Integrating the equation over (0⁻, 0⁺): LC[h′(0⁺) − 0] = 1 and h(0⁺) = 0. So A = 0, "
         "Bω₀ = 1/LC ⇒ B = ω₀. **h(t) = (1/√(LC)) sin(t/√(LC)) u(t)** — an undamped oscillation (marginally unstable).")
n.answer("(d)", "v_R = x − v_C, RC v_C′ + v_C = x. For x = δ: v_C jumps to 1/RC and decays: h_C = (1/RC)e^{−t/RC}u(t). Hence "
         "**h(t) = δ(t) − (1/RC)e^{−t/RC}u(t)** (the resistor passes the impulse instantly, then the capacitor's charge "
         "discharges through it).")
n.answer("(e)", "(i) δ(t) − δ(t − 2): memory, causal, stable; 2rect(t/2): memory, non-causal, stable; 2e^{−4t}u: memory, "
         "causal, stable (∫ = ½); (1 − e^{−4t})u: memory, causal, unstable (∫ → ∞). (ii) h = 2e^{−10t}u(t) (≈ 0 well "
         "before 5 s, so responses do not overlap); y = Σ_{k=−2}^{2} 2(−1)ᵏe^{−10(t−5k)}u(t − 5k): five decaying spikes of "
         "alternating sign at t = −10, −5, 0, 5, 10.")
for k in [("2022-23", "CSE 219", "8(b)"), ("2023-24", "CSE 219", "3(b)"), ("2023-24", "EEE 211", "2(b)"),
          ("2020-21", "EEE 211", "6(c)"), ("2016-17", "EEE 211", "1(a)"), ("2014-15", "EEE 301", "2(b)")]:
    mark(*k)
mark("2016-17", "EEE 211", "3(c)", "◐ Method")

n.quick_notes("Quick Notes — LTI and Convolution", "Revision points for Lessons 6–10.",
              [("L6 · System Properties", ["Linear: a x₁ + b x₂ → a y₁ + b y₂ (zero in → zero out). TI: x(t − t₀) → y(t − t₀).",
                                          "t outside x(·), x(2t), x(−t) ⇒ time-variant. x(t + a), x(−t) ⇒ non-causal.",
                                          "(1/3)[x(t) + x(t ± t₀)]: moving average — LTI, stable, non-causal."]),
               ("L7 · Discrete Convolution", ["c[n] = Σ a[k]b[n − k] = polynomial coefficients; length L + M − 1; Σy = ΣxΣh.",
                                             "{1,2,1,1} * {1,1,−1,2} = {1,3,2,2,4,1,2}."]),
               ("L8 · Impulse Response", ["x = Σx[k]δ[n − k] → y = Σx[k]h[n − k] (TI + homogeneity + additivity).",
                                         "Delay by 3: h = δ[n − 3]. Echo: h = u[n] or αⁿu[n]."]),
               ("L9 · Convolution Practice", ["αⁿu * u = (1 − α^{n+1})/(1 − α) u; e^{−at}u * u = (1 − e^{−at})/a u.",
                                             "e^{−at}u * e^{−bt}u = (e^{−bt} − e^{−at})/(a − b) u; equal a ⇒ t e^{−at}u.",
                                             "Cascade: convolve; parallel: add; δ(t − a) * h = h(t − a).",
                                             "Rect on (a, b): y = H(t − a) − H(t − b). Interval table + continuity check."]),
               ("L10 · Causality, Stability", ["Causal ⇔ h = 0 for t < 0; stable ⇔ ∫|h| < ∞. Periodic h: neither.",
                                              "y′ + ay = bx ⇒ h = b e^{−at}u. LC ⇒ ω₀ sin ω₀t u(t). RC, v_R ⇒ δ − (1/RC)e^{−t/RC}u."])],
              diagrams=[(A[4], 7, "CT convolution: slide h(t − τ) along τ and integrate the overlap (Lec 4, sl. 7)", CLIP, 10)])
n.save()
save_solved("anik_lti_conv")
print("saved", n.out_path)
