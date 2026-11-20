"""IJ 4 — Unit testing (5 - Unit Testing.pdf) + Code reviews (6 - CodeReviews.pdf) → Lessons 15–16."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import new, exam_map, src_note, java, code, IJ  # noqa: E402

UT = os.path.join(IJ, "5 - Unit Testing.pdf")
CR = os.path.join(IJ, "6 - CodeReviews.pdf")
n = new("IJ", "Unit Testing with JUnit, TDD, and Code Reviews", "CSE213_IJ_UnitTesting_CodeReview_Notes.docx")
n.front_matter([
    ("Exam Map — What the TF Papers Ask", "unit-testing and code-review questions"),
    ("Lesson 15 — Unit Testing, JUnit, Fixtures and Test-Driven Development", "5 - Unit Testing pp. 1–24"),
    ("Lesson 16 — Code Reviews: Workflow, Issues, Best Practices, Metrics", "6 - CodeReviews pp. 1–21"),
    ("Quick Notes — Unit Testing and Code Review", "revision"),
], source_note=src_note("Lesson 15: '5 - Unit Testing.pdf' (24 pages). Lesson 16: '6 - CodeReviews.pdf' (21 pages). TDD is "
                        "textbook background (asked in 2023-24 and 2016-17). The JUnit 4 test classes were compiled and run "
                        "(against small stand-ins for org.junit, sources in _build/java/I4): all 20 tests pass."))
exam_map(n, "I4", "JUnit test-class writing is ★★★ (2024-25 isLeapYear 15 marks, 2019-20 fixtures + grading BVA 20 marks); "
         "TDD (2023-24, 12 marks); code-review issues (2022-23, 2020-21) and review metrics/checklists (2018-19, 2017-18). "
         "Learn the JUnit skeleton (@Before, @Test, expected exceptions, assertEquals(expected, actual)) and the nine review "
         "issue types.")

n.lesson("Lesson 15 — Unit Testing, JUnit, Fixtures and Test-Driven Development", "Pages 1–24 (5 - Unit Testing)")
n.p("Unit tests are white-box tests written by developers to verify small units of program functionality, written "
    "concurrently with the implementation (pp. 1–2).")
n.table(["Property of a good unit test (p. 3)", "Meaning"], [
    ["Automatic", "runs completely by itself, no human input"],
    ["Atomic", "decides pass/fail by itself, no human interpretation"],
    ["Single responsibility", "tests exactly one feature"],
    ["Independent", "runs in isolation from other tests (even of the same function)"],
    ["Repeatable", "same result on every run"],
], widths_cm=[5.0, 12.2])
n.h2("JUnit (pp. 4–17)")
code(n, """public class MathTest {                      // pp. 7-11 (Math.add / Math.sub)
    private Math calc;
    @Before public void setUp()    { calc = new Math(); }   // fixture, before EACH test
    @After  public void tearDown() { calc = null; }        // clean-up after each test
    @Test public void testAdd() {
        assertEquals(11, calc.add(5, 6));  assertEquals(0, calc.add(0, 0));
        assertEquals(-10, calc.add(-5, -5)); assertEquals(1, calc.add(-5, 6));
    }
    @Test public void testSub() {
        assertEquals(-1, calc.sub(5, 6));  assertEquals(0, calc.sub(0, 0));
        assertEquals(0, calc.sub(-5, -5)); assertEquals(-11, calc.sub(-5, 6));
    }
}""")
n.table(["Assertion (p. 12)", "Fails if"], [
    ["assertTrue(test) / assertFalse(test)", "test is false / true"],
    ["assertEquals(expected, actual)", "values not equal (equals)"],
    ["assertSame / assertNotSame", "not the same object / the same object (==)"],
    ["assertNull(v) / assertNotNull(v)", "v not null / v null"],
    ["fail()", "always — e.g. after a call that should have thrown"],
], widths_cm=[7.0, 10.2])
n.p("Every assertion may take a message first: assertEquals(\"message\", expected, actual). Framework features (p. 13): "
    "**fixtures** (fixed baseline state so results are repeatable — @Before, @Test, @After), **test suites** (@RunWith + "
    "@Suite bundle test classes), **test runners**, JUnit classes.")
n.callout("trap", "Write the **expected** value first (pp. 19–20); give tests long descriptive names "
          "(test_addDays_wrapToNextMonth_2, p. 22); use expected-answer objects (assertEquals(new Date(2050,3,1), d), p. 21); "
          "messages should say what is being checked, not repeat the values JUnit already prints (pp. 23–24).")
n.h2("Test-driven development (textbook)")
n.numbered(["Add a test for the next small piece of functionality.", "Run all tests — the new one fails (red).",
            "Write the minimum code to make it pass.", "Run all tests — all pass (green).",
            "Refactor the code (and tests), re-run — still green; repeat."])
n.p("Benefits: every line is covered by a test (safety net for refactoring); forces small, decoupled, testable design; "
    "requirements clarified before coding; fewer defects and less debugging; tests document the behaviour; quick feedback.")
n.practice("Lesson 15", "(a) Actual — 2024-25 Q6(a). (b) Actual — 2019-20 Q7(a). (c) Actual — 2023-24 Q3(a) / 2016-17 Q7(a). "
           "(d) Actual — 2014-15 Q2(c) / 2013-14 Q3(c). (e) Actual — 2010-11 Q6(e).", [
    "(a) isLeapYear(int year) returns true for leap years, false otherwise, and throws IllegalArgumentException if year ≤ 0. "
    "Write a complete JUnit test class covering all logically distinct input classes including invalid input; meaningful "
    "names and assertions. (15)",
    "(b) What are fixtures in unit testing? Give 3 examples. Write a unit-test method for the partitions of a grading system "
    "A > 80, B 70–80, C 60–70, with boundary value analysis. (20)",
    "(c) Describe TDD and its benefits / five steps of TDD demonstrated on an example. (12 / 15)",
    "(d) Write an automated tester (driver) for a module that sorts floating-point data, checking the order and that "
    "output and input are the same data set; generate different sizes. (13 / 12)",
    "(e) Design test cases for a Queue class. (15)",
])
n.solution()
n.answer("(a)", "Input classes: divisible by 4 not by 100 (leap); not divisible by 4 (not leap); divisible by 100 not by "
         "400 (not leap); divisible by 400 (leap); boundary 1 and 4; invalid 0 and negative (exception).")
java(n, "I4", "LeapYearTest.java")
n.answer("(b)", "Fixture = fixed, known state created before each test so results are repeatable. Examples: an object "
         "under test created in @Before (new Grader / new Math); a set of test data arrays; a temporary file or in-memory "
         "database prepared and removed in @After. Partitions and boundaries: A {81, 90, 100}, B {71, 75, 80}, C {61, 65, "
         "70}, below C {60}, invalid {−1, 101}.")
java(n, "I4", "Grader.java")
java(n, "I4", "GraderTest.java")
n.answer("(c)", "Steps and benefits above. Example (stack of int): (1) test push then size() == 1 → fails (no class). "
         "(2) red. (3) write Stack with push and size. (4) green. (5) refactor; next test: pop returns last pushed → red → "
         "implement pop → green; next test: pop on empty throws → implement → green; refactor array growth.")
n.answer("(d)", "")
java(n, "I4", "SortTester.java")
n.answer("(e)", "Cases: new queue empty; FIFO order; wrap-around of a circular buffer; dequeue from empty throws; enqueue "
         "on full throws; invalid capacity.")
java(n, "I4", "QueueTest.java")

n.lesson("Lesson 16 — Code Reviews: Workflow, Issues, Best Practices, Metrics", "Pages 1–21 (6 - CodeReviews)")
n.p("Opening examples (pp. 1–4): style inconsistency, a silly redundant check, a buffer overflow (unterminated msgbuf), an "
    "XSS hole (unescaped text). Code review = 'the process of analyzing code written by a teammate (i.e. a peer) to judge "
    "whether it is of sufficient quality to be integrated into the main project codebase' (p. 5).")
code(n, """Author writes code -> review request -> Reviewer accepts -> reviews code -> Accepted?
     ^                                                                     | no      | yes
     +---------------------- author edits code <---------------------------+        +--> approval -> merge
                                                                         (or abandon)
Simplified (p. 11): local branch -> push to Gerrit/GitHub -> reviewer notified -> approved -> push to main""")
n.p("History (pp. 7–8): Fagan inspection — planning, overview, preparation, meeting, rework, follow-up; improves quality "
    "but is process-heavy, meetings are hard to arrange, cost is high and adoption low. Modern tool-based review: Gerrit, "
    "Review Board, Phabricator, Crucible (p. 9). Effort (p. 10): about 6 h/week, 10–15 % of developer time — for 50,000 "
    "developers at $50/h: 50,000 × 6 × 50 = $15,000,000 per week.")
n.table(["Issues identified during code review (pp. 12–13)", "Example"], [
    ["Coding style", "inconsistent naming/indentation"], ["Redundant checks", "the same null check twice"],
    ["Project design violation", "UI class calls the database directly, bypassing the service layer"],
    ["Misunderstood requirements", "discount applied before tax instead of after"],
    ["Critical security defects", "buffer overflow, SQL injection, XSS"], ["Malicious code", "hidden back door / logic bomb"],
    ["Inadequate input validation", "negative quantity accepted"], ["Unsafe methods", "strcpy, gets, eval"],
    ["Lack of exception handling", "file read without try/catch or resource close"],
], widths_cm=[6.2, 11.0], font_size=9)
n.h2("Best practices (SmartBear, pp. 14–20)")
n.numbered([
    "Review fewer than 200–400 lines at a time (defect discovery drops after that).",
    "Authors annotate the source before the review (where to look first, why each change).",
    "Set quantifiable goals and capture metrics: **inspection rate** (LOC reviewed per hour), **defect rate** (defects "
    "found per hour of review), **defect density** (defects per LOC, e.g. per KLOC).",
    "Use checklists — developers repeat the same mistakes, and omissions are the hardest defects to find.",
    "Verify that defects are actually fixed (log, discuss, approve the fix).",
    "Foster a positive culture: defects are chances to improve, not a measure of the person.",
])
n.p("Other (indirect) benefits (p. 21): project awareness, peer impression formation, consistent coding style, design "
    "discussion, knowledge dissemination.")
n.practice("Lesson 16", "(a) Actual — 2022-23 Q2(b) / 2020-21 Q6(c). (b) Actual — 2018-19 Q1(c). (c) Actual — 2017-18 Q5(c). "
           "(d) Actual — 2019-20 Q3(b). (e) Actual — 2021-22 Q8(a). (f) Actual — 2016-17 Q3(b). (g) Actual — 2012-13 Q4(a). "
           "(h) Actual — 2014-15 Q1(d).", [
    "(a) Issues commonly identified during code review — three examples. (12 / 8)",
    "(b) Defect rate and defect density; why checklists are used in code review. (9)",
    "(c) Indirect benefits of code review in a company, with examples. (9)",
    "(d) Limited budget: employ reviewers for SRS, design and code, or hire more (cheaper) testers? Justify. (15)",
    "(e) Driver and navigator in pair programming as a form of code review. (10)",
    "(f) Checklist for a code reviewer to review the non-functional requirements. (15)",
    "(g) Four data faults to check when inspecting a C project. (6)",
    "(h) Scenario of reviewing a quick-sort method: participants and sample queries. (10)",
])
n.solution()
n.answer("(a)", "Any three rows of the table, each with a two-line code example, e.g. unsafe method: strcpy(buf, input) "
         "into char buf[8] — buffer overflow → use strncpy/snprintf; inadequate validation: withdraw(amount) without "
         "checking amount > 0; lack of exception handling: FileReader opened without try-with-resources.")
n.answer("(b)", "Defect rate = defects found per hour of review (e.g. 12 defects in 3 h = 4/h). Defect density = defects "
         "per unit size (e.g. 12 defects in 2,400 LOC = 5 per KLOC). Checklists: people make the same mistakes repeatedly, "
         "and omissions (missing null checks, missing error handling) are hard to notice because the code is not there; a "
         "checklist makes reviewers look for them every time and gives consistent reviews.")
n.answer("(c)", "p. 21 list with examples: project awareness (reviewers learn what changed elsewhere); peer impression "
         "formation (trust in good engineers); consistent coding style; design discussion (better solutions proposed); "
         "knowledge dissemination (juniors learn, bus factor reduced).")
n.answer("(d)", "Keep (some) reviewers. Defects found in requirements and design reviews cost far less to fix than defects "
         "found by testers after coding (cost grows ~10× per phase); reviews also find defects testing cannot (design "
         "violations, maintainability, security holes, missing requirements) and spread knowledge. Testers still needed, "
         "so: lightweight peer reviews by the developers themselves (tool-based, checklist, < 400 LOC) instead of dedicated "
         "reviewers, reviews focused on SRS and critical modules, and the remaining budget on testers.")
n.answer("(e)", "The driver types the code; the navigator continuously reviews it — spotting bugs, thinking about design, "
         "edge cases and tests — and roles switch often. It is real-time code review: defects are caught as they are "
         "written, no separate review meeting is needed, and both share knowledge. Limits: both may share the same blind "
         "spots, so a later independent review is still useful for critical code.")
n.answer("(f)", "Performance (no N+1 queries, efficient algorithms, caching, no blocking calls in UI thread); security "
         "(input validation, parameterised queries, output encoding, secrets not hard-coded, least privilege); reliability "
         "(exception handling, resources closed, retries/timeouts); usability (clear messages, accessibility); "
         "maintainability (naming, small methods, no duplication, comments); portability (no OS-specific paths); "
         "scalability (stateless services, connection pooling); logging/auditability.")
n.answer("(g)", "Variables used before initialisation; constants not named (magic numbers); array bounds not checked "
         "(off-by-one, upper bound = size − 1); buffer overflow on character strings (missing '\\0', strcpy); pointer "
         "faults (dangling or NULL pointers, memory not freed).")
n.answer("(h)", "Participants: author (explains), moderator/lead, reader, reviewers (peer developer, tester), recorder. "
         "Sample queries: Is the pivot choice safe for already-sorted input (worst case O(n²))? Does the partition handle "
         "duplicates and the 0- and 1-element arrays? Can recursion depth overflow the stack for large n? Are the indices "
         "lo/hi inclusive and is hi = n − 1 passed? Is the sort stable — is that required? Are there unit tests for empty, "
         "sorted, reverse-sorted and all-equal arrays?")

n.quick_notes("Quick Notes — Unit Testing and Code Review", "Revision points for Lessons 15–16.", [
    ("L15 · Unit testing", ["Automatic, Atomic, Single responsibility, Independent, Repeatable.",
                            "@Before/@After fixture, @Test, @Test(expected=…), assertEquals(expected, actual).",
                            "TDD: red → green → refactor; benefits: coverage, design, fewer defects."]),
    ("L16 · Code review", ["Workflow: request → review → edit → approve → merge. Fagan inspection six steps.",
                           "Nine issue types; < 400 LOC; annotate; metrics: inspection rate, defect rate, defect density; checklists.",
                           "Indirect benefits: awareness, impressions, style, design discussion, knowledge."]),
])
print(n.save())
