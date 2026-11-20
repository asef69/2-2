"""Exam suggestion for Anik Sir's part (Lec 1–7), built from his own syllabus instructions."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c219 import anik  # noqa: E402

n = anik("Exam Suggestion · Anik Sir's Part (Lectures 1–7)", "CSE219_Anik_Exam_Suggestion.docx")
n.tagline = "Syllabus rules · What to study · Likely questions · Short proofs · How to write"
n.front_matter(
    contents=[("1. Syllabus Rules from Anik Sir", "what is in, what is out"),
              ("2. How the Paper Is Likely to Look", "structure copied from 2022-23 and 2023-24"),
              ("3. Lecture-by-Lecture Priorities", "must-do problems and the slides to read"),
              ("4. The Short Proofs You Must Be Able to Write", "five small proofs"),
              ("5. Application-Type Questions", "convolution, Fourier series, Fourier transform in practice"),
              ("6. How to Do the Maths in the Exam", "visualise, rough sketches, steps not essays"),
              ("7. One-Week Plan", "order of revision")],
    source_note="Built from Anik Sir's syllabus message and from the 2022-23 and 2023-24 CSE 219 papers, plus the earlier EEE 211 / "
                "CSE 311 papers on the same content. Lesson numbers (L1–L19) refer to CSE219_Anik_*_Notes.pdf. "
                "This is a suggestion, not a guarantee: the questions below are the types most likely given the slides and the pattern.")

# ------------------------------------------------------------------ 1
n.h1("1. Syllabus Rules from Anik Sir", new_page=False)
n.bullets(["**Read all slides, Lectures 1–7, carefully.** That is enough. Questions are mathematical problems, proofs, or "
           "application-based theory.",
           "**Not needed for the exam:** very long proofs that are the foundation of a theory — how the Fourier transform "
           "comes from the Fourier series (Lec 7, sl. 4–18), how convolution and the Fourier-series equation are derived. "
           "Read them for intuition only; do not memorise them to write.",
           "**Excluded:** every slide whose title is marked **(\\*)** — in Lec 2 the smoothed-step derivation of δ(t) "
           "(sl. 20–25) and in Lec 5 the coordinate/projection intuition (sl. 44–52).",
           "**Excluded:** Parseval's theorem (taught briefly in one class, not in Part 1). Skip the Parseval questions "
           "in the old papers (e.g. 2023-24 Q2(b)).",
           "**Short proofs are in** (see section 4): even–odd decomposition, impulse-train transform is a train, the "
           "stability condition, and similar small ones.",
           "**Application questions** will be like the labs: where and how convolution, Fourier series and the Fourier transform are "
           "used. The practice sheet has sample problems.",
           "Ask Anik Sir if anything is unclear."])
n.callout("note", "Because the notes were written from the whole TF collection, a few parts of them go beyond the slides: "
          "orthogonal functions and Dirichlet conditions (L11), the Fourier-series symmetry rules and Parseval (L13, L15), "
          "the transform-pair table beyond the rectangle/impulse and Parseval (L18), filters and bandwidth (L19). "
          "Treat those as **low priority** — read them only after everything below.")

# ------------------------------------------------------------------ 2
n.h1("2. How the Paper Is Likely to Look")
n.p("In 2023-24 Anik Sir's part was Section A: **Q1 compulsory (45 marks, three parts of 15)** and **two of Q2–Q4 (30 each)**. "
    "2022-23 had the same shape (Q5 compulsory 45; two of Q6–Q8). Expect:")
n.table(["Slot", "What it was", "What to expect this time"],
        [["Q1(a), 15", "2023-24: sketch x(−2(t−1)) + x((t+2)/2). 2022-23: even–odd decomposition of a piecewise signal",
          "Transformation sketch of a piecewise signal (shift, reversal, scale in the right order) **or** even–odd parts with graphs"],
         ["Q1(b), 15", "2023-24: DT LTI interconnection, h_eq and y[n]. 2022-23: inverse FT chain with properties",
          "Interconnected LTI systems / convolution; or a short chain using FT properties"],
         ["Q1(c), 15", "2023-24: FT of rect(t), then rect((t−τ)/T)cos 2πf₀t. 2022-23: periodicity and FS check",
          "FT of a simple signal, then a property (shift, modulation); or periodicity of a sinusoid"],
         ["Q2–Q4, 30 each", "2023-24: FT of e^{−at}u and e^{−a|t|}; DT periodicity + causal/stable; odd square wave with a shift. "
                            "2022-23: FT of f(t), sign(t); x(−2t+2) by properties; 2-sided DT convolution",
          "One FT-properties problem; one convolution (DT or CT, graphical) with causal/stable; one Fourier-series problem; "
          "plus one application/theory part inside a question"]],
        widths_cm=[2.6, 7.2, 7.4], font_size=8.5)

# ------------------------------------------------------------------ 3
n.h1("3. Lecture-by-Lecture Priorities")
rows = [
    ("Lec 1 — Signals (L1–L3)",
     "★★★ x(αt+β) recipe: shift by β, reverse if α<0, scale by |α|; write the intermediate signal each time (sl. 26–39). "
     "★★★ Even–odd parts: xₑ = ½[x(t)+x(−t)], xₒ = ½[x(t)−x(−t)] and the graphs (sl. 40–52). "
     "★★ Energy and power, E and P of the half-sine, periodic signals, 1/|t| signal with finite energy (sl. 6–16).",
     "Practice-sheet 1.1–1.8 (esp. 1.5, 1.6, 1.7, 1.8). Notes L2 Q7 and 2023-24 Q1(a); L3 2022-23 Q5(a)."),
    ("Lec 2 — Useful signals (L4, L5)",
     "★★★ DT periodicity: 2π/ω₀ must be rational (cos 2n no, cos(2πn/5) yes, 2cos(16πn/63+π/3) N = 63) (sl. 43–50). "
     "★★ Step/impulse: δ[n] = u[n]−u[n−1], u[n] = Σδ[m] (sl. 11–15); jumps → impulses in the derivative; e^{−t}u(t−2), e^tu(3−t) (sl. 31–35). "
     "Skip the (\\*) slides 20–25.",
     "Practice-sheet 2.1–2.6. Notes L5 Q(a)–(c) (periodicity of x[n] = (3−4j)e^{j13πn/7}); L4 jump-signal derivative."),
    ("Lec 3 — LTI and convolution (L6–L8)",
     "★★★ Linearity and time invariance tests; impulse response; y[n] = Σx[k]h[n−k] by reflect–shift–multiply–add (sl. 13–28, 47–57). "
     "★★ Convolution = polynomial multiplication; echo and delay systems h[n] = u[n], αⁿu[n], δ[n−3]. "
     "Understand, do not memorise, the derivation of y = x*h.",
     "Practice-sheet 3.1–3.3. Notes L6 and L7 practice; 2023-24 Q1(b) (interconnection) in L9."),
    ("Lec 4 — Convolution, causality, stability (L9, L10)",
     "★★★ DT and CT convolution of one-sided exponentials with the overlap/case split (αⁿu*u, 2ⁿu[−n]*u, e^{−at}u*u, e^tu(−t)*e^{−t}u) (sl. 11–52). "
     "★★★ Causal ⇔ h = 0 for t<0; stable ⇔ ∫|h| < ∞; do h₁ = e^{2t}u(−2−t) and h₂ = te^{−t}u(t) (sl. 55–69). "
     "★★ A periodic h cannot be causal or stable.",
     "Practice-sheet 4.1–4.8. Notes L9 Q(a) (2022-23 Q8(a), 20 marks) and L10 (b), (a)."),
    ("Lec 5 — Fourier series (L11, L12)",
     "★★★ Coefficients by inspection (Euler) and by integration: a₀ = average, a_k = (1/T)∫x e^{−jkω₀t}dt (sl. 18–29). "
     "★★★ Square wave: a₀ = 2T₁/T, a_k = sin(kω₀T₁)/(kπ), T₁ = T/4 spectrum (sl. 30–34). "
     "★★ Ramp/triangle example (sl. 35–41; the slide prints 6k²ω₀² — the correct factor is 2k²ω₀²). "
     "Skip (\\*) sl. 44–52.",
     "Practice-sheet 5.1–5.6. Notes L12 practice; mean value by area (5.4)."),
    ("Lec 6 — FS properties (L13, L14, L15 partly)",
     "★★★ Shift a_ke^{−jkω₀t₀}, reversal a₋ₖ, scaling (same a_k, ω₀→αω₀), linearity, combined x(4−3t) (sl. 9–35). "
     "★★★ Differentiation jkω₀a_k and impulses at jumps; integration a_k/(jkω₀) with a₀ separately; sifting; impulse train a_k = 1/T (sl. 36–72). "
     "★★ Multiplication ↔ convolution of coefficients: (1+cos ω₀t)² (sl. 73–81).",
     "Practice-sheet 6.1–6.5. Notes L13 Q(a) (odd square wave with shift, 2023-24 Q4), L14."),
    ("Lec 7 — Fourier transform (L16, L17, parts of L18)",
     "★★★ Rect ↔ 2 sin(ωT/2)/ω, shifted rect, Lego-block decomposition (sl. 29–38). "
     "★★★ Frequency shift and cosine modulation x cos ω₀t ↔ ½X(ω−ω₀)+½X(ω+ω₀); time shift e^{−jωt₀}X (sl. 19–28, 35). "
     "★★★ δ(t) ↔ 1, δ(t−t₀) ↔ e^{−jωt₀} (sl. 41–44). "
     "★★ Applications (sl. 45–59): denoising, JPEG, MRI, music ID, vibration, ECG. "
     "Pairs beyond the slides (e^{−at}u, sgn, e^{−a|t|}, duality) are asked in the older papers and in 2022-23/2023-24 — "
     "learn them from L18 after the slide material. Skip the FS→FT derivation (sl. 4–18).",
     "Practice-sheet 7.1–7.7. Notes L17 Q(a) (2023-24 Q1(c)), L18 Q(a)–(b) except the Parseval part.")]
n.table(["Lecture", "Study (★★★ must, ★★ should)", "Practice from"], [[a, b, c] for a, b, c in rows],
        widths_cm=[3.0, 9.4, 4.8], font_size=8)

# ------------------------------------------------------------------ 4
n.h1("4. The Short Proofs You Must Be Able to Write")
n.p("Each takes 3–6 lines. Write the statement, the key step, the conclusion.")
n.table(["Proof", "Key step"],
        [["1. Every signal has an even and an odd part (Lec 1, sl. 43–44)",
          "Define xₑ = ½[x(t)+x(−t)], xₒ = ½[x(t)−x(−t)]. xₑ(−t) = xₑ(t) and xₒ(−t) = −xₒ(t) by substitution, and xₑ + xₒ = x."],
         ["2. Impulse train in time is an impulse train in frequency (Lec 6, sl. 52–56)",
          "Period −T/2 < t < T/2 contains one impulse; sifting gives a_k = (1/T)∫δ(t)e^{−jkω₀t}dt = 1/T for every k — a flat line "
          "spectrum, i.e. a train in k (and in ω at kω₀)."],
         ["3. Stability condition ∫|h| < ∞ (Lec 4, sl. 58–59)",
          "|y(t)| = |∫h(τ)x(t−τ)dτ| ≤ B∫|h(τ)|dτ for |x| ≤ B. So finite area ⇒ bounded output."],
         ["4. A periodic h cannot be causal or stable (Lec 4, sl. 60–62)",
          "Causal: a nonzero h(t₀) repeats at t₀ − kT < 0. Stable: area A per period × infinitely many periods = ∞."],
         ["5. Time shift ↔ phase, frequency shift ↔ modulation, FS time shift (Lec 6 sl. 11–12; Lec 7 sl. 22–25)",
          "x(t−t₀) = Σa_k e^{jkω₀(t−t₀)} = Σ[a_ke^{−jkω₀t₀}]e^{jkω₀t}; FT: substitute τ = t−t₀. Frequency shift: "
          "x e^{jω₀t} ↔ X(ω−ω₀) because every e^{jωt} component becomes e^{j(ω+ω₀)t}."],
         ["6. Reversal/scaling/differentiation of FS coefficients (Lec 6)",
          "Substitute into x = Σa_ke^{jkω₀t}: x(−t) → a₋ₖ; x(αt) → same a_k with ω₀′ = αω₀; dx/dt → jkω₀a_k."],
         ["7. y = x*h for LTI (Lec 3, sl. 52–57) — understand, do not memorise",
          "x = Σx[k]δ[n−k]; TI gives δ[n−k]→h[n−k]; linearity gives y = Σx[k]h[n−k]. Three lines are enough if asked."]],
        widths_cm=[6.0, 11.2], font_size=8.5)
n.callout("trap", "Not expected as full derivations: Fourier series → Fourier transform (T → ∞), the general convolution/FS "
          "equations from scratch, and anything about Parseval.")

# ------------------------------------------------------------------ 5
n.h1("5. Application-Type Questions")
n.p("These are theory + common sense, like the labs. Prepare two or three sentences for each:")
n.table(["Topic", "Say this"],
        [["Convolution", "Output of any LTI system = input * impulse response. Room reverb: convolve the dry voice with the hall's measured "
                         "impulse response (clap/pop). Echo: h = δ[n] + aδ[n−D] (D = delay, a = strength). Smoothing sensor noise: "
                         "convolve with a moving-average kernel. Image blur/sharpen: 2-D convolution."],
         ["Fourier series", "Periodic signal = sum of harmonics kω₀: solve each easy sine, add the answers (vibrating string, heat "
                            "diffusion). Square/triangle waves, harmonic analysis of a periodic voltage, AC circuit response harmonic by harmonic."],
         ["Fourier transform", "Aperiodic signals have a continuous spectrum. Audio/image denoising (remove noise frequencies), JPEG "
                               "(drop small high-frequency coefficients), MRI (data measured in the frequency domain), music "
                               "recognition (fingerprint from frequency peaks), vibration diagnosis, ECG 50 Hz notch."],
         ["Practice-sheet sample problems", "4.9 room acoustics, 4.10 smoothing sensor readings, 4.11 echo, 7.5 hidden signals in space, "
                                            "7.6 removing a tone, 7.7 audio compression — write 3–4 lines each."]],
        widths_cm=[3.4, 13.8], font_size=8.5)

# ------------------------------------------------------------------ 6
n.h1("6. How to Do the Maths in the Exam")
n.bullets(["**Visualise.** Sketch the signal roughly. Even–odd: draw x(t), x(−t), then xₑ and xₒ — you will see at once whether "
           "xₑ is mirror-symmetric and xₒ is point-symmetric. Convolution: draw x(τ) and h(t−τ), slide h and watch where "
           "they overlap; the interval table follows from the picture.",
           "**Rough is fine.** The sketch is for you; mark the key points (break points, heights) and move on.",
           "**Do not write everything formally.** Show the main steps in your own way, with the right sketch and the "
           "correct limits; finish in time.",
           "**For transformation sketches** write the intermediate signal after every operation (the slides ask for it), "
           "and check one break point with t = (a−β)/α.",
           "**For convolution** always give the case split (n<0, 0≤n, …) and check: support = sum of supports, continuity at the boundaries.",
           "**For causal/stable questions** state the support of h first (causal), then compute ∫|h| (stable).",
           "**For Fourier-series questions** try inspection first (Euler); integrate only if the signal is a standard waveform; "
           "use the properties to avoid a second integral."])

# ------------------------------------------------------------------ 7
n.h1("7. One-Week Plan")
n.table(["Day", "Do"],
        [["1", "Lec 1: transformation recipe (all examples), even–odd; practice-sheet 1.1–1.8"],
         ["2", "Lec 2: periodicity, step/impulse, exponential-step signals; practice-sheet 2.1–2.6; Lec 3 systems and discrete convolution"],
         ["3", "Lec 4: CT/DT convolution cases, causality, stability (all slide examples twice); practice-sheet 4.1–4.8"],
         ["4", "Lec 5: coefficients by inspection and integration; square wave, ramp; practice-sheet 5.1–5.6"],
         ["5", "Lec 6: FS properties (shift/reversal/scaling/derivative/integration/product); practice-sheet 6.1–6.5"],
         ["6", "Lec 7: rect, shifts, modulation, δ; then pairs and properties from L18 (e^{−at}u, sgn, e^{−a|t|}); practice-sheet 7.1–7.4"],
         ["7", "Past CSE 219 papers (2022-23 Q5–Q8, 2023-24 Q1–Q4) timed; the short proofs; application sentences; read the notes' Quick Notes"]],
        widths_cm=[1.4, 15.8], font_size=9)
n.save()
print("saved", n.out_path)
