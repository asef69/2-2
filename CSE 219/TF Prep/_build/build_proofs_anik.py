"""Detailed proofs for Anik Sir's part (Lec 1–7)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c219 import anik  # noqa: E402

n = anik("Required Proofs · Anik Sir's Part (Lectures 1–7)", "CSE219_Anik_Required_Proofs.docx")
n.tagline = "Detailed proofs · what to write · what is intuition only"
n.front_matter(
    contents=[("How to Use This Sheet", "status tags and exam writing style"),
              ("Lecture 1 — Signals", "P1 even–odd decomposition, P2 the x(αt+β) recipe"),
              ("Lecture 2 — Useful Signals", "P3 step and impulse relations, P4 sifting, P5 DT periodicity"),
              ("Lecture 3 — LTI and Convolution", "P6 y = x*h, P7 commutativity and distributivity"),
              ("Lecture 4 — Causality and Stability", "P8 causal ⇔ h = 0, P9 BIBO stability, P10–P11 periodic h"),
              ("Lecture 5 — Fourier Series", "P12 coefficient formula, P13 a₀, P14 square wave, P15 even/odd symmetry"),
              ("Lecture 6 — FS Properties", "P16 shift, reversal, scaling, P17 differentiation, P18 integration, P19 product, P20 impulse train"),
              ("Lecture 7 — Fourier Transform", "P21 FS → FT (intuition), P22 shifts and modulation, P23 rect and δ, P24 extra pairs/properties")],
    source_note="Anik Sir: very long proofs that build a theory (FS → FT, how convolution and the Fourier-series equation are "
                "derived) are for intuition only; short proofs must be written; slides marked (\\*) and Parseval's theorem are not "
                "in the syllabus. Each proof below has a status tag. Slide references are PDF pages of the lecture files.")

n.h1("How to Use This Sheet", new_page=False)
n.table(["Tag", "Meaning"],
        [["REQUIRED", "A short proof the slides do. Be able to write it in 3–8 lines."],
         ["REQUIRED (old papers)", "Not a slide proof but asked in past TF papers (CSE 311 / EEE) on the same content. Learn it as well."],
         ["INTUITION", "Long foundation derivation. Read for understanding; do not memorise for writing. A short version is given."]],
        widths_cm=[4.4, 12.8])
n.callout("note", "Write proofs in the style shown: state what you prove, give the key substitution, end with the result. "
          "Rough sketches help (even–odd, convolution). Do not expand everything formally.")

# =============================================================== LEC 1
n.h1("Lecture 1 — Signals")
n.h2("P1. Every signal has an even and an odd part — REQUIRED (sl. 43–44)")
n.p("**Claim.** For any x(t), define xₑ(t) = ½[x(t) + x(−t)] and xₒ(t) = ½[x(t) − x(−t)]. Then xₑ is even, xₒ is odd and x = xₑ + xₒ.")
n.code(["Even:  xₑ(−t) = ½[x(−t) + x(−(−t))] = ½[x(−t) + x(t)] = xₑ(t)",
        "Odd:   xₒ(−t) = ½[x(−t) − x(t)] = −½[x(t) − x(−t)] = −xₒ(t)",
        "Sum:   xₑ(t) + xₒ(t) = ½[x(t) + x(−t)] + ½[x(t) − x(−t)] = x(t)"])
n.p("**Uniqueness (extra, 2 lines).** If x = a + b with a even and b odd, then x(−t) = a(t) − b(t). Adding/subtracting x(t) and x(−t) "
    "gives a = xₑ, b = xₒ. The same proof works for x[n] with n in place of t.")
n.p("**Example (sl. 45–48).** x = t + 1 on [−1, 1]: x(−t) = 1 − t, so xₑ = ½[(t+1) + (1−t)] = 1 and xₒ = ½[(t+1) − (1−t)] = t. "
    "Check by graph: xₑ is a flat line (mirror-symmetric), xₒ is a straight line through the origin (point-symmetric).")

n.h2("P2. The recipe for x(αt + β) — REQUIRED (sl. 26–31)")
n.p("**Claim.** x(t) → x(t+β) → (reverse if α < 0) → scale by |α| gives x(αt+β), and the order cannot be swapped.")
n.code(["Step 1: g₁(t) = x(t + β)                       (shifts the picture left by β)",
        "Step 2: g₂(t) = g₁(−t) = x(−t + β)   (only if α < 0)",
        "Step 3: g₃(t) = g₂(|α|t).  If α < 0:  g₂(|α|t) = x(−|α|t + β) = x(αt + β).   If α > 0:  g₁(αt) = x(αt + β).",
        "Order matters: first compress then shift gives g(t) = x(2t) → g(t + 3) = x(2(t + 3)) = x(2t + 6) ≠ x(2t + 3).",
        "Where does a feature go?  If x has a feature at t = a, then αt + β = a ⇒ t = (a − β)/α in x(αt + β)."])
n.p("**Why:** each operation replaces the variable t of the *current* signal. Shifting after scaling therefore shifts the argument of the "
    "scaled signal, not of the original.")

# =============================================================== LEC 2
n.h1("Lecture 2 — Useful Signals")
n.h2("P3. Step and impulse are related — REQUIRED (sl. 11–15; CT: asked in CSE 311 2019-20 Q2(b))")
n.p("**Discrete time.**")
n.code(["(a) δ[n] = u[n] − u[n−1]:  for n ≥ 1 both are 1 → 0;  n = 0: 1 − 0 = 1;  n < 0: 0 − 0 = 0.  This is exactly δ[n].",
        "(b) u[n] = Σ_{m=−∞}^{n} δ[m]:  if n < 0 the sum window (−∞, n] does not contain m = 0 ⇒ 0;",
        "    if n ≥ 0 it contains the single spike at m = 0 ⇒ 1.  So the sum equals u[n].",
        "(c) u[n] = Σ_{k=0}^{∞} δ[n − k]:  δ[n−k] is 1 only at n = k; at a given n ≥ 0 exactly one term (k = n) is 1; for n < 0 none."])
n.p("**Continuous time (short form).** The step jumps from 0 to 1 at t = 0, so its derivative is 0 everywhere except at the jump. "
    "Replace the jump by a ramp of width Δ: the derivative is a pulse of height 1/Δ and width Δ, area 1 for every Δ. As Δ → 0 this "
    "becomes δ(t), so δ(t) = du/dt. Conversely u(t) = ∫_{−∞}^{t}δ(τ)dτ: for t < 0 the window misses the impulse (0), for t > 0 it contains "
    "it (area 1). (The slides' detailed smoothed-step derivation, sl. 20–25, is marked (\\*) — excluded; the 4-line version above is enough.)")

n.h2("P4. Sifting property of the impulse — REQUIRED (Lec 6, sl. 45–51; asked in CSE 311 2012-13 Q5(a))")
n.code(["Since δ(t − a) = 0 for t ≠ a, only the value of x at t = a matters:  x(t)δ(t − a) = x(a)δ(t − a).",
        "Integrate:  ∫ x(t)δ(t − a)dt = x(a)∫δ(t − a)dt = x(a)   — provided a lies inside the integration limits;",
        "if a is outside [L, R] the impulse is never seen and the integral is 0.",
        "Discrete: Σ_n x[n]δ[n − a] = x[a] (every other term is 0)."])
n.p("Consequence used constantly: δ(t − a) * h(t) = h(t − a); a train of impulses puts one copy of h at every impulse.")

n.h2("P5. Discrete-time periodicity condition — REQUIRED (sl. 43–50)")
n.code(["x[n] = cos(ω₀n + φ) is periodic with period N iff x[n + N] = x[n] for all n.",
        "cos(ω₀(n + N) + φ) = cos(ω₀n + φ)  for all n  ⇔  ω₀N = 2πm for some integer m.   (the phase φ plays no role)",
        "So N = 2πm/ω₀ must be an integer ⇒ 2π/ω₀ = N/m must be a rational number.",
        "The fundamental period N₀ is the numerator of 2π/ω₀ written in lowest terms.",
        "Examples:  ω₀ = 2:  2π/2 = π (irrational) → not periodic.   ω₀ = 16π/63:  2π/ω₀ = 63/8 → N₀ = 63 (m = 8).",
        "           ω₀ = 5/7:  2π/ω₀ = 14π/5 (irrational) → not periodic."])
n.p("Sums: x₁[n] + x₂[n] is periodic with N = lcm(N₁, N₂). Continuous time: T₀ = 2π/|ω₀| always exists for a single sinusoid, but a sum "
    "is periodic only if the ratio T₁/T₂ is rational.")

# =============================================================== LEC 3
n.h1("Lecture 3 — LTI Systems and Convolution")
n.h2("P6. The output of an LTI system is y = x * h — INTUITION (short version REQUIRED) (sl. 47–57; asked in CSE 311 2018-19 Q4(b))")
n.p("Anik Sir treats the general derivation as intuition, but a time-domain proof is a 4-line argument and an old paper asked it.")
n.code(["Let δ[n] → h[n]   (definition of the impulse response).",
        "1. Decompose the input into shifted, scaled impulses:  x[n] = Σ_k x[k] δ[n − k].",
        "2. Time invariance:  δ[n − k] → h[n − k].",
        "3. Homogeneity:       x[k] δ[n − k] → x[k] h[n − k].",
        "4. Additivity (the sum is a sum of inputs):   y[n] = Σ_k x[k] h[n − k] = (x * h)[n]."])
n.p("Continuous time: x(t) = ∫x(τ)δ(t − τ)dτ (sifting). Each piece x(τ)dτ·δ(t − τ) produces x(τ)dτ·h(t − τ) by TI and homogeneity. "
    "Adding (integrating) gives y(t) = ∫x(τ)h(t − τ)dτ. Only linearity and time invariance were used — so the formula holds for every LTI "
    "system.")
n.p("**Example (sl. 47–51).** x = δ[n] + 2δ[n−1] − δ[n−2] + δ[n−3], h = u[n]: y = u[n] + 2u[n−1] − u[n−2] + u[n−3], i.e. 1, 3, 2, 3, 3, 3, …")

n.h2("P7. Convolution is commutative (and distributes over addition) — REQUIRED (short) (sl. 29–30; Lec 4, sl. 41)")
n.code(["Commutativity:  (a * b)[n] = Σ_k a[k] b[n − k].  Put m = n − k (k = n − m; as k runs over all integers so does m):",
        "                = Σ_m a[n − m] b[m] = Σ_m b[m] a[n − m] = (b * a)[n].",
        "Continuous time: y(t) = ∫x(τ)h(t − τ)dτ, put σ = t − τ:  = ∫x(t − σ)h(σ)dσ = (h * x)(t).",
        "Distributivity:  x * (h₁ + h₂) = Σ_k x[k](h₁[n−k] + h₂[n−k]) = x * h₁ + x * h₂  (linearity of the sum).",
        "Polynomial view: A(z)B(z) = B(z)A(z), and the coefficient of zⁿ is Σ_k a[k]b[n−k] — this is why convolution is polynomial multiplication."])
n.p("Useful consequence: pick the easier signal to flip; split a two-sided input into left- and right-sided parts and convolve separately (Lec 4, Ex 2.10).")

# =============================================================== LEC 4
n.h1("Lecture 4 — Convolution, Causality and Stability")
n.h2("P8. Causal ⇔ h(t) = 0 for t < 0 — REQUIRED (sl. 55–56)")
n.code(["y(t) = ∫ h(τ)x(t − τ)dτ.  The input at time t − τ with τ < 0 is x at a time later than t (the future).",
        "(⇐) If h(τ) = 0 for τ < 0 the integral runs over τ ≥ 0 only: y(t) uses x(t − τ) with t − τ ≤ t — past and present only ⇒ causal.",
        "(⇒) h is the response to δ(t); a causal system cannot respond before the impulse arrives at t = 0 ⇒ h(t) = 0 for t < 0.",
        "DT: causal ⇔ h[n] = 0 for n < 0."])

n.h2("P9. BIBO stability: stable ⇔ ∫|h(t)|dt < ∞ — REQUIRED (sl. 57–59)")
n.code(["Sufficiency.  Let |x(t)| ≤ B for all t.  Then",
        "   |y(t)| = |∫h(τ)x(t − τ)dτ| ≤ ∫|h(τ)||x(t − τ)|dτ ≤ B ∫|h(τ)|dτ = B·M < ∞,   M = ∫|h|.   (bounded input → bounded output)",
        "Necessity (idea, 2 lines).  If ∫|h| = ∞, choose the bounded input x(−τ) = sgn h(τ) (|x| ≤ 1).  Then",
        "   y(0) = ∫h(τ)x(−τ)dτ = ∫|h(τ)|dτ = ∞  ⇒ the output is unbounded for a bounded input ⇒ not stable.",
        "DT:  stable ⇔ Σ_n |h[n]| < ∞."])
n.p("**Slide examples:** h₁ = e^{2t}u(−2−t): ∫_{−∞}^{−2}e^{2t}dt = e^{−4}/2 < ∞ stable (non-causal, since nonzero for t ≤ −2). "
    "h₂ = te^{−t}u(t): ∫₀^∞te^{−t}dt = 1 < ∞ stable and causal. e^{−4t}u(3−t) is non-causal and ∫_{−∞}^{3}e^{−4t}dt = ∞ ⇒ unstable.")

n.h2("P10. A nonzero periodic h cannot be causal — REQUIRED (sl. 60–61)")
n.code(["Let h be periodic with period T and h(t₀) ≠ 0 for some t₀ (≥ 0 w.l.o.g.).",
        "Periodicity gives h(t₀) = h(t₀ − T) = h(t₀ − 2T) = …  Choose k with t₀ − kT < 0: then h is nonzero at a negative time.",
        "Causality needs h(t) = 0 for t < 0 — contradiction.  So only h ≡ 0 is both causal and periodic."])
n.h2("P11. A nonzero periodic h cannot be stable — REQUIRED (sl. 60, 62)")
n.code(["If h ≢ 0 is periodic, the area of |h| over one period is some A > 0 (same in every period).",
        "∫_{−∞}^{∞}|h(t)|dt = … + A + A + A + … = ∞  ⇒ not absolutely integrable ⇒ not stable (by P9).",
        "So only h ≡ 0 is both stable and periodic."])

# =============================================================== LEC 5
n.h1("Lecture 5 — Fourier Series")
n.h2("P12. The Fourier-series coefficient formula a_k = (1/T)∫ x(t)e^{−jkω₀t}dt — INTUITION (short version REQUIRED) (sl. 18–22)")
n.p("Given x(t) = Σ_m a_m e^{jmω₀t}, how do we get a_k? Stop the k-th wave rotating and average.")
n.code(["Key fact:  (1/T)∫_T e^{jnω₀t}dt = 1 if n = 0, and = (1/T)[e^{jnω₀t}/(jnω₀)]_{t₀}^{t₀+T} = (1/T)(e^{j2πn} − 1)·(…) = 0 if n ≠ 0.",
        "Multiply x(t) by e^{−jkω₀t}:   x(t)e^{−jkω₀t} = Σ_m a_m e^{j(m − k)ω₀t}.",
        "Average over one period:        (1/T)∫_T x(t)e^{−jkω₀t}dt = Σ_m a_m·(1/T)∫_T e^{j(m − k)ω₀t}dt = a_k   (only m = k survives).",
        "Special case k = 0:  a₀ = (1/T)∫_T x(t)dt = the average value of x."])
n.p("Memorise the *result* and the *averaging idea*; the full justification (swapping sum and integral, convergence) is not required.")

n.h2("P13. Coefficients by inspection and the DC term — REQUIRED (sl. 25–29, 36–37)")
n.code(["cos θ = (e^{jθ} + e^{−jθ})/2,  sin θ = (e^{jθ} − e^{−jθ})/(2j).  Write every term with e^{jkω₀t}, collect equal k.",
        "Example: x = 1 + sin ω₀t + 2cos ω₀t + cos(2ω₀t + π/4)",
        "  sin ω₀t + 2cos ω₀t = (1/2j)(e^{jω₀t} − e^{−jω₀t}) + (e^{jω₀t} + e^{−jω₀t}) = (1 − j/2)e^{jω₀t} + (1 + j/2)e^{−jω₀t}",
        "  cos(2ω₀t + π/4) = ½e^{jπ/4}e^{j2ω₀t} + ½e^{−jπ/4}e^{−j2ω₀t}",
        "  a₀ = 1, a₁ = 1 − j/2, a₋₁ = 1 + j/2, a₂ = ½e^{jπ/4} = (√2/4)(1 + j), a₋₂ = (√2/4)(1 − j).",
        "Geometry for a₀ (sl. 37): a₀ = (area over one period)/T, e.g. triangular ramp T = 3: (½·3·1)/3 = ½."])

n.h2("P14. Fourier series of a rectangular pulse train — REQUIRED (sl. 30–34)")
n.code(["x = 1 for |t| < T₁, 0 for T₁ < |t| < T/2 (period T, ω₀ = 2π/T).  Use the period (−T/2, T/2):",
        "k = 0:  a₀ = (1/T)∫_{−T₁}^{T₁}1 dt = 2T₁/T",
        "k ≠ 0: a_k = (1/T)∫_{−T₁}^{T₁}e^{−jkω₀t}dt = (1/T)[e^{−jkω₀t}/(−jkω₀)]_{−T₁}^{T₁} = (1/T)(e^{jkω₀T₁} − e^{−jkω₀T₁})/(jkω₀)",
        "      = 2 sin(kω₀T₁)/(Tkω₀) = sin(kω₀T₁)/(kπ)      (since Tω₀ = 2π)",
        "T₁ = T/4:  a₀ = ½, a_k = sin(kπ/2)/(kπ): a±₁ = 1/π, a±₂ = 0, a±₃ = −1/(3π), a±₅ = 1/(5π), …"])

n.h2("P15. Even signals have real coefficients, odd signals imaginary; half a cycle is enough — REQUIRED (old papers: CSE 311 2018-19 Q2(b), 2022-23 Q1(a))")
n.code(["a_k = (1/T)∫_{−T/2}^{T/2} x(t)[cos kω₀t − j sin kω₀t]dt",
        "Even x:  x·sin kω₀t is odd ⇒ its integral over the symmetric period is 0, and x·cos kω₀t is even:",
        "         a_k = (2/T)∫₀^{T/2} x(t)cos kω₀t dt   — real (and a₋ₖ = a_k).",
        "Odd x:   x·cos kω₀t is odd ⇒ 0, and x·sin kω₀t is even:",
        "         a_k = −(2j/T)∫₀^{T/2} x(t)sin kω₀t dt  — purely imaginary (a₋ₖ = −a_k), and a₀ = 0.",
        "cos 2πf₀t (even) → a±₁ = ½ real;  sin 2πf₀t (odd) → a±₁ = ∓j/2 imaginary."])

# =============================================================== LEC 6
n.h1("Lecture 6 — Properties of Fourier Series")
n.p("All of these follow by substituting into x(t) = Σ a_k e^{jkω₀t}. Each is a 2–3 line proof — all REQUIRED.")
n.h2("P16. Linearity, time shift, time reversal, time scaling (sl. 5–35)")
n.code(["Linearity:  αx + βy = Σ(αa_k + βb_k)e^{jkω₀t}   (same period, same exponentials, so coefficients add).",
        "Time shift: x(t − t₀) = Σ a_k e^{jkω₀(t − t₀)} = Σ [a_k e^{−jkω₀t₀}] e^{jkω₀t}   ⇒ b_k = a_k e^{−jkω₀t₀}.",
        "            |e^{−jkω₀t₀}| = 1: the magnitude is unchanged; the phase turns by −kω₀t₀ (higher harmonics rotate more).",
        "Reversal:   x(−t) = Σ a_k e^{jkω₀(−t)} = Σ a_k e^{j(−k)ω₀t} = Σ a₋ₘ e^{jmω₀t} (m = −k)   ⇒ b_k = a₋ₖ.",
        "Scaling:    x(αt) = Σ a_k e^{jk(αω₀)t}: same coefficients a_k, but the fundamental frequency becomes αω₀ (period T/α).",
        "Combined (sl. 24–35): x(4 − t) + y(t − 3) ↔ a₋ₖe^{−j4kω₀} + b_k e^{−j3kω₀};   x(4 − 3t) ↔ a₋ₖe^{−j4kω₀}, ω₀′ = 3ω₀",
        "            (shift left 4 → a_k e^{j4kω₀};  reverse → a₋ₖe^{−j4kω₀};  scale → coefficients unchanged)."])
n.callout("trap", "Slide 26 prints y(t − 3) ↔ a_k e^{−j3kω₀}; it must be **b_k** e^{−j3kω₀} because y has coefficients b_k.")
n.h2("P17. Differentiation — REQUIRED (sl. 36–41, 57–63)")
n.code(["x(t) = Σ a_k e^{jkω₀t}  ⇒  dx/dt = Σ a_k d/dt[e^{jkω₀t}] = Σ (jkω₀ a_k) e^{jkω₀t}   ⇒  dx/dt ↔ jkω₀ a_k.",
        "Use the current fundamental: for x(4 − 3t), ω₀′ = 3ω₀ ⇒ d/dt x(4 − 3t) ↔ j(3kω₀)a₋ₖe^{−j4kω₀}.",
        "At a jump of height J at t₀ the derivative contains Jδ(t − t₀).",
        "Check on the rectangular pulse train: dx/dt = δ(t + T₁) − δ(t − T₁) per period ⇒ b_k = (1/T)(e^{jkω₀T₁} − e^{−jkω₀T₁}) = (2j/T)sin kω₀T₁",
        "   and jkω₀a_k = jkω₀·sin(kω₀T₁)/(kπ) = j(ω₀/π)sin kω₀T₁ = (2j/T)sin kω₀T₁ ✓."])
n.h2("P18. Integration — REQUIRED (sl. 64–72)")
n.code(["If y = ∫x dt is periodic, then dy/dt = x ⇒ a_k = jkω₀ b_k ⇒ b_k = a_k/(jkω₀) for k ≠ 0.",
        "The constant of integration is invisible to the derivative, so b₀ must be found separately (average value of y).",
        "Example: sawtooth x = t on [0,1), T = 1: dx/dt = 1 − Σδ(t − m): coefficients c₀ = 0 (1 − 1), c_k = −1 (k ≠ 0)",
        "   ⇒ a_k = −1/(j2πk) = j/(2πk), a₀ = ∫₀¹t dt = ½."])
n.h2("P19. Multiplication ↔ convolution of the coefficients — REQUIRED (sl. 73–81)")
n.code(["x = Σ_p a_p e^{jpω₀t},  y = Σ_q b_q e^{jqω₀t}.   x·y = Σ_p Σ_q a_p b_q e^{j(p + q)ω₀t}.",
        "The k-th harmonic collects all pairs with p + q = k, i.e. q = k − p:   c_k = Σ_p a_p b_{k−p} = (a * b)_k.",
        "Example: x = 1 + cos ω₀t, a = {½, 1, ½} (k = −1,0,1):  a * a = {¼, 1, 3/2, 1, ¼} (k = −2…2).",
        "Check: (1 + cos)² = 3/2 + 2cos ω₀t + ½cos 2ω₀t ⇒ c₀ = 3/2, c±₁ = 1, c±₂ = ¼ ✓."])
n.h2("P20. The impulse train has a flat line spectrum — a train in frequency — REQUIRED (sl. 52–56)")
n.code(["x(t) = Σ_m δ(t − mT), ω₀ = 2π/T.  Take the period (−T/2, T/2): it contains exactly one impulse, at t = 0.",
        "a_k = (1/T)∫_{−T/2}^{T/2} δ(t)e^{−jkω₀t}dt = (1/T)e^{−jkω₀·0} = 1/T     (sifting, P4)   for every integer k.",
        "So the coefficient sequence is the constant 1/T: lines of equal height 1/T at every kω₀ — an impulse train in frequency (spacing ω₀ = 2π/T).",
        "Trigonometric form: x = 1/T + (2/T)Σ_{n≥1}cos(2πnt/T)."])

# =============================================================== LEC 7
n.h1("Lecture 7 — Fourier Transform")
n.h2("P21. From Fourier series to Fourier transform — INTUITION ONLY (sl. 4–18)")
n.p("Anik Sir: do **not** memorise this derivation; understand it. The story in six lines:")
n.code(["1. Repeat an aperiodic pulse x(t) with period T:  x̃_T(t) = Σ_m x(t − mT) — now periodic, so it has a Fourier series.",
        "2. a_k = (1/T)∫_{−T/2}^{T/2} x̃_T e^{−jkω₀t}dt = (1/T)X(jkω₀),   X(jω) = ∫x(t)e^{−jωt}dt  (the pulse is zero outside one period).",
        "3. So T·a_k are samples of one smooth curve X(jω) at ω = kω₀.",
        "4. x̃_T(t) = Σ a_k e^{jkω₀t} = (1/2π)Σ X(jkω₀)e^{jkω₀t}Δω with Δω = ω₀ = 2π/T.",
        "5. T → ∞: x̃_T → x(t); Δω → dω; kω₀ → ω; the sum → ∫.",
        "6. x(t) = (1/2π)∫X(jω)e^{jωt}dω   and   X(jω) = ∫x(t)e^{−jωt}dt   — the transform pair."])
n.h2("P22. Frequency shift and cosine modulation — REQUIRED (sl. 22–28)")
n.code(["Frequency shift:  F{x(t)e^{jω₀t}} = ∫x(t)e^{jω₀t}e^{−jωt}dt = ∫x(t)e^{−j(ω − ω₀)t}dt = X(j(ω − ω₀)).",
        "                  (every component e^{jωt} becomes e^{j(ω + ω₀)t}: the whole spectrum slides right by ω₀.)",
        "Modulation:       x(t)cos ω₀t = ½x(t)e^{jω₀t} + ½x(t)e^{−jω₀t}  ⇒  ½X(j(ω − ω₀)) + ½X(j(ω + ω₀)).",
        "                  Two half-height copies of the spectrum, centred at +ω₀ and −ω₀."])
n.h2("P23. Transforms of the rectangle, the impulse, and the shifted versions — REQUIRED (sl. 29–44)")
n.code(["Rectangle (1 for |t| < T/2):  X(jω) = ∫_{−T/2}^{T/2}e^{−jωt}dt = [e^{−jωt}/(−jω)]_{−T/2}^{T/2} = (e^{jωT/2} − e^{−jωT/2})/(jω)",
        "                             = 2 sin(ωT/2)/ω         (X(0) = T).   Wider T → narrower main lobe (first zero 2π/T).",
        "Time shift:  F{x(t − t₀)} = ∫x(t − t₀)e^{−jωt}dt;  put τ = t − t₀ ⇒ e^{−jωt₀}∫x(τ)e^{−jωτ}dτ = e^{−jωt₀}X(jω).",
        "             |X| unchanged, phase −ωt₀ (a straight line in ω). Example: 1 on (4, 10) = width-6 rect shifted by 7 ⇒ e^{−j7ω}·2 sin 3ω/ω, X(0) = 6.",
        "Impulse:     F{δ(t)} = ∫δ(t)e^{−jωt}dt = e^{−jω·0} = 1   (sifting)  — flat spectrum: a spike contains all frequencies equally.",
        "             F{δ(t − t₀)} = e^{−jωt₀}.",
        "Lego block (1 on (1,4) plus 0.5 on (2,3), both centred at 2.5):  X = e^{−j2.5ω}[2 sin(1.5ω)/ω + 0.5·2 sin(0.5ω)/ω]."])
n.h2("P24. Extra results asked in the papers on the same content — REQUIRED (old papers); not in the slides")
n.p("These are not in Lecture 7, but 2022-23, 2023-24 and the older papers use them. Learn the short proofs.")
n.code(["Time delay ⇒ linear phase (CSE 311 2019-20 Q2(a)):  x(t − t₀) ↔ e^{−jωt₀}X(jω); phase −ωt₀ is linear in ω.",
        "     If a voice (many frequencies) lost linear phase, each frequency would be delayed differently (dispersion) and the sound would smear.",
        "Time scaling:  F{x(at)} = ∫x(at)e^{−jωt}dt;  τ = at ⇒ (1/|a|)∫x(τ)e^{−jωτ/a}dτ = (1/|a|)X(jω/a).",
        "     (|a| because a < 0 flips the integration limits.) Compression in time ⇒ expansion in frequency.",
        "Differentiation:  x = (1/2π)∫X e^{jωt}dω ⇒ dx/dt = (1/2π)∫jωX e^{jωt}dω ⇒ dx/dt ↔ jωX(jω).",
        "Convolution (CSE 311 2012-13 Q5(b), 2011-12 Q6(a)):",
        "     F{x*h} = ∫[∫x(τ)h(t − τ)dτ]e^{−jωt}dt = ∫x(τ)[∫h(t − τ)e^{−jωt}dt]dτ;  s = t − τ ⇒ ∫x(τ)e^{−jωτ}H(jω)dτ = X(jω)H(jω).",
        "e^{−at}u(t), a > 0:  ∫₀^∞e^{−(a + jω)t}dt = 1/(a + jω).     e^{−a|t|} = e^{−at}u(t) + e^{at}u(−t) ↔ 1/(a + jω) + 1/(a − jω) = 2a/(a² + ω²).",
        "Reversal:  x(−t) ↔ X(−jω) (put τ = −t).   sgn(t) = lim_{a→0}[e^{−at}u(t) − e^{at}u(−t)] ↔ 1/(a + jω) − 1/(a − jω) → 2/(jω).",
        "Real x:  X(−jω) = ∫x e^{jωt}dt = X*(jω) ⇒ |X| even, ∠X odd (CSE 311 2016-17 Q1(b)).",
        "Duality:  2πx(−t) = ∫X(jω)e^{−jωt}dω; rename t ↔ ω ⇒ F{X(jt)} = 2πx(−ω). (rect ↔ sinc ⇒ sinc ↔ 2π·rect.)"])
n.callout("trap", "Not required: Parseval's theorem and anything marked (\\*). Do not spend time on them.")
n.save()
print("saved", n.out_path)
