# Reading log — CSE 211 slides (slide no. = PDF page; beamer overlays → a group "a–b")

## Hakim Sir
### Lec01 Introduction (53 pp)
4–6 four "easy" things (parentheses, JSON, halting, Sudoku); prediction table · 7 four mysteries · 8–11 password rules → finite memory → FA ·
12–15 tokenizing (regex/DFA/NFA) · 16–19 balanced parens need more · 20–23 JSON → stack → PDA · 24 memory hierarchy (finite / stack / general / impossible) ·
25–31 halting problem consequences · 32–34 checking vs finding → P/NP · 35–37 AI doesn't delete complexity · 38–40 theorem proving ·
41–42 course map (DFA/NFA, CFG/PDA, TM, undecidability, complexity) · 43–45 AI as assistant · 46–47 Sipser · 48–53 ToC today.
Exam use: theory Q1(a)'s (areas of ToC, password system, hard problems, cryptography).

### Lec02 Languages (52 pp)
8–10 alphabet · 11–12 strings, length · 13–16 concatenation, power, reverse · 17–19 Σ* · 20–22 language (incl. Σ*, ∅) ·
23–27 problems = languages · 28–30 EVEN-1s · 31–34 palindromes · 35–38 JSON · 39–42 Python · 43–46 SAT · 47–48 why languages ·
49–50 machine ↔ language class table · 51 mini-assignment.

### Lec03 DFA (42 pp, diagrams vector)
5 state = compressed summary of past · 8–9 5-tuple · 10–12 EVEN1 diagram+table · 13 deterministic · 16 formal acceptance r0..rn ·
17 L(M) · 18 ε accepted iff q0∈F · 19 ε vs ∅ vs {ε} · 20 dead state · 22 design recipe · 23–24 contains 001 · 25–27 binary div by 3 (r→2r+b) ·
28–29 football scores · 31–32 product construction (even 0s ∧ len mod 3) · 33–34 2nd symbol from right · 35–36 contains ab but not ba ·
37–38 no symbol repeated (table) · 39–40 C comments · 41 skills checklist.

### Lec04 NFA (109 pp)
4–20 philosophy of nondeterminism (find vs verify, guessing / parallel / tree) · 22–29 NFA for contains 101 · 30–31 branch outcomes ·
34–35 computation trees 0101, 1000 · 36–40 acceptance; prove accept vs reject · 42–47 formal def, δ:Q×Σ→P(Q), table · 48–49 DFA⊂NFA ·
51–55 contains fed or dff · 56–62 split point w1w2 · 63–68 missing a symbol (table) · 72–74 ε-NFA def & acceptance · 75–78 {ab, acd} ·
79 ε-closure · 80–82 removing ε: δ'(q,a)=E(∪δ(r,a)), F' · 83–87 worked example (5 states) · 88–90 Sipser convention ·
92–96 subset construction (assumes no ε) · 97–108 worked example aba (6 reachable of 16) · 109 comments.

### Lec05 The Regulars (111 pp)
7–13 union/concat/star, ∅*={ε} · 14–15 regular language · 16–24 closure under ∪ ∘ * (NFA constructions + formal) · 34–35 proof template ·
38–43 complement (DFA only, complete DFA; NFA flip fails) · 44–50 intersection (product; De Morgan) · 51–52 difference · 53–57 reverse ·
58–60 closure as shortcut · 61–68 RE syntax/semantics/shorthands/precedence · 69–84 examples, ∅ vs ε, identities ·
85–86 Kleene · 87–93 RE→NFA (Thompson; (ab∪a)*) · 94–103 GNFA, rip formula · 104 non-unique RE · 105–109 div-by-3 DFA→RE = (0∪1(01*0)*1)* · 110 summary.
No minimisation in slides.

### Lec06 Non-Regulars (50 pp)
4–7 pigeonhole/cycle intuition · 8 PL statement (|y|>0, |xy|≤p) · 9–11 quantifiers, adversary game, 5-step template ·
12–21 examples 0^n1^n, palindromes a^p b a^p, a^nb^nc^n, w#w, a^(n²) · 22 summary table · 23 checklist ·
24–25 closure proofs (0^m1^n m≠n; m<n) · 26–27 table of more examples (prime, 2^n, m=n or m=2n, …) · 28 home problems (incl. a^(n!)) ·
29–31 #0≠#1 via complement ∩ 0*1* · 32–34 primes (i=q+1) · 35–37 composite via closure · 38–40 Fibonacci · 41–48 #ab=#ba over {a,b,c} · 49–50 lessons.

### Lec07 CFG (97 pp)
7–8 balanced parens grammar · 10–16 formal 4-tuple, sentential forms, L(G), "context-free means…" (14) · 18–19 nested commands ·
20–22 leftmost/rightmost a+a*a · 23–28 parse trees, yield, equivalence · 29 recursive inference · 31 design checklist ·
32–34 mixed brackets · 35–37 equal 0/1 S→0S1S|1S0S|ε (+completeness) · 38–39 w#w^R · 40 palindromes · 41–42 a^nb^mc^md^n ·
43 i=j or j=k · 44 #0≠#1 · 45 trees · 46–47 query language · 48–50 DFA→CFG, regular ⊂ CFL · 51 ww trap · 52 patterns ·
54–58 ambiguity, E→E+E|E*E, fix with E/T/F · 59–60 dangling else · 61 S→SS ambiguous · 62–63 inherent ambiguity a^nb^nc^md^m ∪ a^nb^mc^md^n ·
65–72 CFL PL statement, quantifiers, witness choice · 73–77 a^nb^nc^n · 78–80 a^nb^mc^nd^m · 81–84 primes · 85–89 a^n b^(n²) · 90–95 pitfalls/checklist.
(Learning goals list CNF/CYK but slides stop at the PL.)

### lec_08_pda (71 pp)
5–10 why a stack, trace 000111 · 11–21 6-tuple (Sipser), δ:Q×Σε×Γε→P(Q×Γε), labels a,b→c, ε roles · 22–24 configurations, final-state acceptance ·
26–28 PDA 0^n1^n · 30–33 ww^R guess midpoint · 34 w#w^R · 35 i=j or j=k · 37–41 patterns + checklist + mistakes · 42 DFA vs PDA · 43 0^n1^n2^n impossible ·
46–65 ten examples with traces: a^nb^2n, a^ib^j i≤j, i=k, w#w^R, palindromes, balanced, #0=#1, i=j or j=k, a^nb^mc^md^n, a^ib^jc^(i+j).

## Atif Sir
### Lecture 1 intro (14): 2–3 three areas automata/computability/complexity · 6 models · 7 Turing · 8–13 syllabus · 14 Hopcroft textbook.
### Lecture 2 CNF (35): 2 CNF def · 4–18 CYK (table images; example baaba, S→AB|BC A→BA|a B→CC|b C→AB|a) · 19–21 order ε→unit→useless→CNF ·
22–23 useless (generating/reachable) · 24–26 nullable/ε-elimination · 27–30 unit pairs (E,T,F,I grammar) · 31–35 terminals→variables, break long bodies.
### Lecture 3 PDA (136): Hopcroft 7-tuple (q,a,X)/(p,γ) · 20–39 ww^R PDA (δ rules) · 44–55 diagrams a,X/α · 56–80 IDs, ⊢, tree for 1111 ·
81–84 ID principles · 87–95 balanced parens · 96–101 equal a's and b's · 102–105 L(P) vs N(P) · 106–109 ES→FS, FS→ES constructions (images) ·
110–115 CFG→PDA (one state) with a+a*b trace · 116–122 PDA→CFG [pXq] · 123–129 CFL pumping lemma + proof (|w|≤2^(n−1)) · 130–133 DPDA, wcw^R · 134 LR(k) · 135 CSG · 136 Chomsky hierarchy.
### Lecture 4 TM1 (123): 2–26 TM 7-tuple · 27–41 IDs and boundary cases · 42–65 TM 0^n1^n (table sl.46) traces 0011, 0010 · 66–70 diagrams ·
71–115 monus m∸n (0^m10^n), trace 4∸2, 2∸4 · 116–119 L(M), RE · 121–123 halting.
### Lecture 5 TM2 (133): 3–26 storage in state (01*+10*) · 27–83 multiple tracks, wcw TM (14 rules, full trace) · 84–131 binary addition w1cw2c (states [q,a,b,ci], 16 rules) · 132–133 subroutines.
### Lecture 6 TM3 (68): 4–10 multitape · 11–21 one-tape simulates k-tape (2k tracks) · 22 O(n²) · 23–31 NTM→DTM (BFS, queue) · 33–36 semi-infinite tape · 37–38 multistack · 39 counter · 40–59 TM simulates computer (tapes, instruction cycle) · 60–68 polynomial time, O(n³)/O(n⁶).
### Lecture 7 Undecidability (77): 2–6 history, Church–Turing, list · 7–10 RE, recursive, classes · 11–12 decidable A_DFA etc. · 17 enumerating strings · 18–39 TM codes (example) · 40–51 Ld not RE · 52–56 complements · 57 complement of Ld · 58–66 Lu, UTM, Lu RE not recursive · 67–70 halting RE not recursive · 71 reductions · 72 Rice-type list · 73–76 PCP · 77 CFG undecidables.
### Lecture 8 Complexity (51): 3–8 P, NP · 9 poly reductions · 10–16 NPC, NP-hard · 17–28 SAT, Cook's theorem (7 rule families) · 29 Karp · 30–40 3SAT→DIRHAMCYCLE · 41–46 Clique (from IS), Max common subgraph · 47–51 Partition from Subset Sum.
### Lecture 9 Space (20): 3–5 SPACE/NSPACE/PSPACE/NPSPACE · 6 SAT linear space · 7 P⊆NP⊆PSPACE · 8–10 c^(1+p(n)) bound · 11–18 Savitch · 19 conjectured relation.
