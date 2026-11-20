"""IJ 5 — Refactoring and code smells (7 - Refactoring.pdf) → Lessons 17–19."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import new, exam_map, src_note, java, code, IJ  # noqa: E402

RF = os.path.join(IJ, "7 - Refactoring.pdf")
n = new("IJ", "Refactoring and Code Smells", "CSE213_IJ_Refactoring_Notes.docx")
n.front_matter([
    ("Exam Map — What the TF Papers Ask", "refactoring questions — every recent paper"),
    ("Lesson 17 — What Refactoring Is; Why, When and Its Problems", "pp. 1–14"),
    ("Lesson 18 — Code Smells", "pp. 15–29"),
    ("Lesson 19 — The Refactoring Catalogue and Worked TF Refactorings", "pp. 30–47"),
    ("Quick Notes — Refactoring", "smell → refactoring map"),
], source_note=src_note("Page numbers refer to '7 - Refactoring.pdf' (48 pages). Smells not shown on the slides "
                        "(refused bequest, parallel inheritance hierarchies) follow Fowler and refactoring.guru (marked "
                        "'textbook'). All refactored Java was compiled and run (sources in _build/java/I5)."))
exam_map(n, "I5", "★★★ every year: identify smells and refactor given code — 2024-25 (20 marks), 2023-24 (20), 2022-23 "
         "(15 + 20), 2021-22 (13 + 10), 2019-20 (20). Learn the smell → refactoring map (Quick Notes) and practise naming "
         "the smell, then the refactoring, then writing the after-code.")

n.lesson("Lesson 17 — What Refactoring Is; Why, When and Its Problems", "Pages 1–14 (7 - Refactoring)")
n.callout("memorize", "**Refactoring** (Fowler, noun): a change made to the internal structure of software to make it easier "
          "to understand and cheaper to modify without changing its observable behavior. (Verb): to restructure software "
          "by applying a series of refactorings without changing its observable behavior (p. 8).")
n.bullets([
    "External behaviour unchanged (functional requirements kept), internal structure improved — 'improving the design "
    "after it has been written' (p. 2).",
    "Simple examples: consolidate duplicate conditional fragments (send() moved after the if/else, p. 3); replace magic "
    "number 9.81 with GRAVITATIONAL_CONSTANT (p. 4).",
    "Dangerous: can introduce bugs; managers see time not spent on features → make it systematic, incremental and safe (p. 5).",
    "Useful: designs are rarely right first time and requirements change; code often shrinks and becomes simpler (p. 6).",
    "Contrast with performance optimisation: also keeps functionality but often makes code harder to understand (p. 9).",
    "Safe refactoring: use named refactoring patterns, and **test constantly** — run the tests after every step (p. 10).",
])
n.table(["Why refactor (p. 11)", "When (p. 12)", "Problems (p. 13)"], [
    ["improves design (stops decay); easier to understand; helps find bugs; helps program faster",
     "Rule of Three (third duplication → refactor); when adding a function (before or after); when fixing a bug; during code review",
     "databases are tightly coupled and hard to change; published interfaces cannot change"],
], widths_cm=[5.8, 6.0, 5.4], font_size=9)
n.p("Finding where to refactor: look for **bad smells** (p. 14); tools such as Codegrip, Checkstyle, PMD, FindBugs and "
    "SonarQube detect them automatically.")
n.callout("note", "Technical debt (2024-25 Q4(b), textbook): the future cost of rework caused by choosing a quick or easy "
          "solution now; code smells are its symptoms, refactoring is how it is repaid. Interest = the extra effort every "
          "change costs while the debt remains.")
n.practice("Lesson 17", "(a) Actual — 2024-25 Q4(b). (b) Actual — 2017-18 Q2(c).", [
    "(a) Define code smell, tech-debt and code refactoring. Differentiate proactive and reactive risk-management "
    "strategies with examples. (15)",
    "(b) Why is refactoring important in agile development? Examples. (7)",
])
n.solution()
n.answer("(a)", "Code smell = a surface symptom in code that usually indicates a deeper design problem (e.g. a 200-line "
         "method, duplicated code). Technical debt = NOTE above. Refactoring = Fowler's definition. Reactive risk "
         "strategy: act only after a risk occurs (fire-fighting) — e.g. a key developer leaves and the team then scrambles "
         "to hire and learn the code. Proactive: identify, analyse and plan for risks before they happen (risk table, "
         "mitigation, monitoring, contingency) — e.g. pair programming and documentation so knowledge is shared before "
         "anyone leaves. Proactive is cheaper and is real risk management; reactive is crisis management.")
n.answer("(b)", "Agile builds the design incrementally with little up-front design, and requirements change every "
         "sprint; without refactoring the code decays into duplication and long methods, and velocity falls. Refactoring "
         "with automated tests (TDD) keeps the design simple (XP 'simple design', 'refactor mercilessly'). Examples: "
         "extract a duplicated validation into one method after the third user story needs it; replace a growing switch "
         "on payment type with polymorphic classes when a new payment method is added.")

n.lesson("Lesson 18 — Code Smells", "Pages 15–29 (7 - Refactoring)")
n.table(["Group (p. 15)", "Smells"], [
    ["Bloaters", "Long Method, Large Class, Primitive Obsession, Long Parameter List, Data Clumps"],
    ["OO abusers", "Alternative Classes with Different Interfaces, Refused Bequest, Switch Statements, Temporary Field"],
    ["Change preventers", "Divergent Change, Parallel Inheritance Hierarchies, Shotgun Surgery"],
    ["Dispensables", "Comments, Duplicate Code, Data Class, Dead Code, Lazy Class, Speculative Generality"],
    ["Couplers", "Feature Envy, Inappropriate Intimacy, Incomplete Library Class, Message Chains, Middle Man"],
], widths_cm=[3.6, 13.6])
n.table(["Smell", "Symptom (slides)", "Refactoring"], [
    ["Duplicated code (p. 17)", "same lookup + exception in CustomerNameChanger and CustomerAddressChanger", "Extract Method / Pull Up Method"],
    ["Long method (p. 18)", "processOrder validates, totals, discounts, formats and prints", "Extract Method per step"],
    ["Large class", "does too much, low cohesion", "Extract Class"],
    ["Long parameter list (p. 19)", "processPayment(name, email, cardNumber, expiry, amount)", "Introduce Parameter Object"],
    ["Divergent change (p. 21)", "Employee changes for personal info, report format, email, pay rules", "Extract Class per reason"],
    ["Shotgun surgery (p. 22)", "minimum-balance rule and message copied in debit, transfer …", "Move Method / Inline into one class"],
    ["Feature envy (p. 24)", "Invoice.calculateDiscount uses only Customer's data", "Move Method to Customer"],
    ["Data clumps (p. 23)", "fields that always travel together (street, postOffice, district)", "Extract Class / Parameter Object"],
    ["Primitive obsession (p. 25)", "parallel arrays std_ID, std_name, std_marks", "Replace Data Value with Object (Student class)"],
    ["Switch statements (p. 25)", "the same switch on a type code in many places", "Replace Conditional with Polymorphism"],
    ["Lazy class (p. 26)", "Logger that only calls println", "Inline Class"],
    ["Data class (pp. 27–28)", "only fields + getters/setters; behaviour elsewhere", "Move Method into it (Order.getTotalPrice)"],
    ["Comments (p. 29)", "comments used as deodorant for bad code", "Extract Method with a good name"],
    ["Refused bequest (textbook)", "subclass ignores/throws in inherited methods", "Replace Inheritance with Delegation; Push Down"],
    ["Parallel inheritance (textbook)", "each new subclass in one hierarchy needs one in another", "Move methods so one hierarchy absorbs the other"],
], widths_cm=[3.8, 7.6, 5.8], font_size=8.5)
n.practice("Lesson 18", "(a) Actual — 2022-23 Q5(a). (b) Actual — 2019-20 Q6(a). (c) Actual — 2021-22 Q6(c).", [
    "(a) Define with short code examples: shotgun surgery, parallel inheritance hierarchies, refused bequest, feature envy. (4+4+4+3)",
    "(b) Two program snippets showing the smells Data Clump and Refused Bequest. (20)",
    "(c) Define code smell; three examples. (10)",
])
n.solution()
n.answer("(a)/(b)", "Each smell with before → after (compiled):")
java(n, "I5", "SmellExamples.java")
n.answer("(c)", "Definition (Lesson 17) + any three rows of the table with a two-line example each.")

n.lesson("Lesson 19 — The Refactoring Catalogue and Worked TF Refactorings", "Pages 30–47 (7 - Refactoring)")
n.table(["Refactoring (p. 30)", "Do", "Slide example"], [
    ["Extract Method (pp. 31–32)", "turn a fragment into a method named after its purpose", "print_invoice → calculate_total"],
    ["Extract Class (p. 33)", "one class doing two jobs → move fields/methods to a new class", "Person → TelephoneNumber"],
    ["Extract Variable (pp. 34–35)", "name parts of a complex expression", "basePrice, isBulkOrder, discountRate"],
    ["Replace Temp with Query (pp. 36–38)", "temp → private method usable elsewhere", "basePrice → getBasePrice()"],
    ["Move Method (pp. 39–40)", "move to the class whose data it uses", "Car.calculateFuelEfficiency → Engine"],
    ["Replace Conditional with Polymorphism (pp. 41–42)", "each branch → overriding method", "Bird.getSpeed per subclass"],
    ["Separate Query from Modifier (pp. 43–44)", "split a method that returns and changes state", "getTotalOutstanding + setReadyForSummaries"],
    ["Introduce Parameter Object (pp. 45–46)", "group parameters that travel together", "DateRange(start, end, includes)"],
    ["Also: Introduce Null Object, Encapsulate Collection, Replace Nested Conditional with Guard Clauses", "", ""],
], widths_cm=[5.0, 6.6, 5.6], font_size=8.5)
code(n, """// Extract Variable (p. 35)
double calculatePrice(double quantity, double itemPrice) {
    double basePrice = quantity * itemPrice;
    boolean isBulkOrder = quantity > 100;
    double discountRate = isBulkOrder ? 0.9 : 0.95;
    return basePrice * discountRate;
}""")
n.practice("Lesson 19", "(a) Actual — 2022-23 Q5(b). (b) Actual — 2021-22 Q1(b). (c) Actual — 2023-24 Q8(c). (d) Actual — "
           "2024-25 Q4(a).", [
    "(a) Which refactorings, and the refactored code: (i) renderBanner with if ((platform.toUpperCase().indexOf(\"MAC\") > "
    "-1) && (browser.toUpperCase().indexOf(\"IE\") > -1) && wasInitialized() && resize > 0) (ii) getSalary() with switch "
    "(type) Football / Cricket / Badminton (iii) getPayAmount() with nested if-else on isDead, isSeparated, isRetired. (6+7+7)",
    "(b) GetSuperHeroItem.getItem(heroName) is an if-else chain (IronMan → suit, Thor → hammer, CaptainAmerica → shield, "
    "Hawkeye → arrow, else null). Rewrite it to be easier to read and maintain, with constant amortised run time. (13)",
    "(c) Define bad smells and refactoring; identify the smells in DiscountCalculator.calculateDiscount(customerType, "
    "productType, price, customerName, customerId) (if-chain on REGULAR/PREMIUM × ELECTRONICS/GROCERY with 10/5/20/10 %) "
    "and OrderProcessor.processOrder(...) (prints customer data twice, if-chains on the same strings, compares discount == "
    "price × 0.1 / 0.15 / 0.25), and revise the code. (20)",
    "(d) Identify five bad smells in Student (type code 1 = UG / 2 = PG, street/postOffice/district, yearWiseGpa, isFulltime "
    "for PG only, calculateFee and printDetails switching on type) and Scholarship (isRegular(Student), checkEligibility "
    "with deep nesting and duplicated CGPA loop) and refactor each. (20)",
])
n.solution()
n.answer("(a)", "(i) **Decompose Conditional / Extract Variable** — name each part (isMacOs, isIE, wasResized). "
         "(ii) **Replace Conditional with Polymorphism** — Player subclasses override getSalary() (type code removed). "
         "(iii) **Replace Nested Conditional with Guard Clauses** — return early; no temp 'result'.")
java(n, "I5", "Refactor2223.java")
n.answer("(b)", "Smells: long if-else chain (switch smell), magic strings, public fields. Refactoring: **replace "
         "conditional with a lookup table** (HashMap) filled once — getItem is O(1) amortised, a new hero is one "
         "register() call, and keys are lower-cased to keep equalsIgnoreCase behaviour.")
java(n, "I5", "SuperHeroItems.java")
n.answer("(c)", "Smells: **long parameter list** and **data clump** (customerName, customerId, customerType); **unused "
         "parameters** (name and id in calculateDiscount); **switch statements** — if-chains on the type strings, "
         "repeated in both classes; **magic numbers/strings**; **duplicated code** (customer data printed twice); **long "
         "method** (processOrder); a logic bug hidden by the smells — discount is compared with price × 0.1 / 0.15 / 0.25 "
         "though the rates are 0.05, 0.1, 0.2, and doubles are compared with ==. Refactorings: Introduce Parameter Object "
         "(Customer, Product), Replace Type Code with enum + Replace Conditional with Polymorphism (rates inside "
         "CustomerType), Extract Method for printing, compute and print the rate instead of comparing doubles.")
java(n, "I5", "OrderRefactored.java")
n.answer("(d)", "Five smells → refactorings: (1) **type code + switch** (type 1/2 in calculateFee and printDetails) → "
         "Replace Type Code with Subclasses (UndergraduateStudent, PostgraduateStudent) + polymorphism; (2) **data clump** "
         "street/postOffice/district → Extract Class Address; (3) **temporary field** isFulltime used only for PG → move "
         "into PostgraduateStudent; (4) **feature envy** — Scholarship computes regularity and CGPA from Student's data → "
         "Move Method (isRegular, cgpa into Student); (5) **duplicated code** — CGPA loop in Student and Scholarship → "
         "Extract Method cgpa(); plus **long method / deep nesting** in checkEligibility → guard clauses, and magic "
         "numbers 50000/40000/48000/3.5 → named constants. ('stuent.type' typo also fixed.)")
java(n, "I5", "StudentRefactored.java", size=8)

n.quick_notes("Quick Notes — Refactoring", "Revision points for Lessons 17–19.", [
    ("L17 · Basics", ["Behaviour unchanged, structure improved; small safe steps + tests after each.",
                      "Why: design, understanding, bugs, speed. When: rule of three, adding feature, fixing bug, review.",
                      "Problems: databases, published interfaces. Tech debt = cost of quick fixes."]),
    ("L18 · Smells → cure", ["Duplicated → Extract Method · Long method → Extract Method · Long params / data clump → Parameter Object / Extract Class",
                             "Switch / type code → Polymorphism · Feature envy → Move Method · Shotgun surgery → Move into one class",
                             "Divergent change → Extract Class · Refused bequest → Delegation · Lazy class → Inline · Comments → Extract Method"]),
    ("L19 · Catalogue", ["Extract Method/Class/Variable, Replace Temp with Query, Move Method, Replace Conditional with Polymorphism,",
                         "Separate Query from Modifier, Introduce Parameter Object, Guard Clauses, lookup table for long if-chains."]),
])
print(n.save())
