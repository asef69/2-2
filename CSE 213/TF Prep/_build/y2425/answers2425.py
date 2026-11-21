"""answers2425.py - model answers to the CSE 213 term final 2024-25 (L-2/T-II)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "mock"))
sys.path.insert(0, HERE)
from pdfkit import *  # noqa: F401,F403,E402
from reportlab.platypus import Preformatted  # noqa: E402
import figs2425 as F  # noqa: E402
import pdfkit as _pk  # noqa: E402
_pk.CODE.fontSize = 6.8
_pk.CODE.leading = 8.4


def code(text, shade=SHADE, chunk=12):
    """code block that may break across pages: one table row per `chunk` lines."""
    NL = chr(10)
    lines = text.strip(NL).split(NL)
    rows = [[Preformatted(NL.join(lines[i:i + chunk]), CODE)] for i in range(0, len(lines), chunk)]
    t = Table(rows, colWidths=[None])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), shade), ("BOX", (0, 0), (-1, -1), 0.5, RULE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, 0), 4), ("BOTTOMPADDING", (0, -1), (-1, -1), 4)]))
    return t


def H(t, m):
    return P("%s &nbsp;<font color='#6b7280' size='9'>[%s]</font>" % (t, m), "h2")


def mark(*items):
    return [P("Marking scheme", "sol")] + bullets(list(items))


def J(path, a=None, b=None):
    """a slice of a verified Java file: from the line containing a (inclusive) to the line containing b (exclusive)."""
    lines = open(os.path.join(HERE, "java", path), encoding="utf-8").read().rstrip("\n").split("\n")
    i = 0 if a is None else next(k for k, l in enumerate(lines) if a in l)
    j = len(lines) if b is None else next(k for k, l in enumerate(lines) if k > i and b in l)
    return "\n".join(lines[i:j]).rstrip("\n")


def story(fw):
    s = []
    w = fw

    # ======================================================================= cover
    s += [P("CSE 213 — TERM FINAL 2024-25 — SOLUTIONS", "title"),
          P("L-2/T-II &nbsp;•&nbsp; Software Engineering &nbsp;•&nbsp; 210 marks &nbsp;•&nbsp; 3 hours", "sub"), Spacer(1, 6),
          P("Model answers to all eight questions of the paper (Section A: answer three including Q1; Section B: Q5 compulsory plus any two). Every question carries 35 marks, so"
            " you answer six questions for 210. Every Java program in this file was compiled and run; the printed outputs are the real ones. Diagrams follow the notation of the course notes.")]
    s.append(P("The paper at a glance", "h2"))
    rows = [["Q", "Part", "Marks", "Topic", "Your notes"],
            ["1", "(a) (b) (c)", "15+12+8", "BPMN diagram; class diagram; load and stress testing", "Anindya L19–22, L9–11, L24"],
            ["2", "(a) (b) (c)", "13+12+10", "Sequence diagram; state diagram; code-review issues", "Anindya L16–17, L13–15; IJ L16"],
            ["3", "(a) (b) (c)", "15+12+8", "Abstract Factory; three SOLID violations; Open/Closed example", "Anindya L6, L2–3"],
            ["4", "(a) (b) (c)", "15+12+8", "Builder; SOLID refactoring of FineService; condition coverage", "Anindya L8, L2–3, L25"],
            ["5", "(a) (b) (c)", "10+10+15", "Observer in Java; ethics of undisclosed AI bots; JUnit suite for gcd", "IJ L7, L20, L15"],
            ["6", "(a)(i)(ii) (b)(i)(ii)", "5+5, 15+10", "State vs Strategy; Template Method; requirements elicitation; process model", "IJ L5–6, L9, L21, L11–13"],
            ["7", "(a)(i)(ii) (b)", "10+5, 20", "Transparency and accountability; refactoring claim; Bridge + Strategy (BrewBuddy)", "IJ L20, L17, L4–5"],
            ["8", "(a) (b)", "10+25", "Five non-functional requirements; six code smells + full refactoring", "IJ L21, L18–19"]]
    s.append(table(rows, [0.8 * cm, 3.0 * cm, 1.9 * cm, w - 11.4 * cm, 5.7 * cm]))
    s.append(Spacer(1, 4))
    s.append(P("<b>Assumptions and corrections.</b> (1) The paper prints <i>Srting</i> and a string without quotes in Q4(b), and Q8(b)'s <font face='Mono'>calculateDeviceCost</font> uses an undeclared"
               " <font face='Mono'>room</font>; the refactored code below is written so that it compiles. (2) Q2(a) says the officer decides whether to “change a penalty”; this is read as"
               " “charge a penalty”. (3) The researcher fine rate (Q4(b)) and the loyalty-discount rule (Q7(b)) are not given, so a rate of 3 per day and “1 % per 100 points, at most 20 %” are assumed and"
               " flagged where used. (4) Marking schemes are the usual split of the printed marks, not the examiner's own."))
    s.append(Spacer(1, 2))

    # ======================================================================= SECTION A
    s += [banner("SECTION A")]
    s.append(P("Question 1", "q"))
    s.append(H("(a) BPMN diagram of the appointment process", "15"))
    s.append(P("<b>Participants</b> (lanes of one pool): Patient, Hospital System, Payment Gateway (an external service), Doctor and Laboratory. Rounded boxes are <b>tasks</b>, diamonds with × are"
               " <b>exclusive gateways</b> (each outgoing arrow is labelled), thin circles are <b>start</b> events, thick circles are <b>end</b> events, solid arrows are <b>sequence flows</b> and dashed arrows are"
               " <b>message flows</b> between participants."))
    s.append(F.bpmn_main())
    s.append(P("<b>Cancellation</b> is a second, independent flow: it can start at any time after the appointment exists, so it is drawn as its own process that begins with a start event in the Patient lane.", "body"))
    s.append(F.bpmn_cancel())
    s += mark("pool and five lanes 2.", "start and end events (booked, not booked, done, cancelled, kept) 2.",
              "all tasks of the scenario: search/select, check availability, create pending appointment, request payment, process payment, confirm and notify, consultation, prescription, lab request, test and upload, review 4.",
              "the five gateways with labelled branches (slot available, payment OK, retry, lab tests needed, before the deadline) 4.", "message flows across lanes 1; cancellation with refund 2.")

    s.append(H("(b) Class diagram", "12"))
    s.append(F.class_hospital())
    s += bullets(["<b>Patient 1 — * Appointment</b>; <b>Doctor 1 — * TimeSlot</b>; <b>TimeSlot 1 — 0..1 Appointment</b>: a patient searches a doctor's slots, and a slot can be taken by at most one appointment, which is how an"
                  " unavailable slot is detected.",
                  "<b>Appointment — * Payment</b> (composition, filled diamond on Appointment): a failed payment can be retried, so one appointment owns several payment attempts that make no sense without it; <b>Payment depends on PaymentGateway</b>"
                  " (dashed arrow to an interface for the external service).",
                  "<b>Appointment 1 — 0..1 Refund</b>, <b>Appointment 1 — 0..1 Prescription</b>; <b>Prescription — 1..* PrescriptionItem</b> (composition: the medicines); <b>Prescription 1 — * LabTestRequest</b>;"
                  " <b>LabTestRequest 1 — 0..1 LabReport</b>; <b>Laboratory 1 — * LabTestRequest</b>.",
                  "<b>Notification * — 1 Appointment</b> records the messages to the patient and the doctor. Status attributes (SlotStatus, appointment status, PayStatus) carry the state used in the BPMN."])
    s += mark("the 13 classes with sensible attributes and operations 5.", "generalisation is not needed; correct association, composition and dependency kinds 4.", "multiplicity at every end 3.")

    s.append(H("(c) Why the application failed, and two testing methods", "8"))
    s.append(F.load_stress())
    s.append(table([["", "Load testing", "Stress testing"],
                    ["What it is", "Runs the system with the <i>expected</i> number of users, up to and at the specified limit (100), for a sustained time.",
                     "Pushes the system <i>beyond</i> its specified limit (120, 150, 200 …) until it breaks, then checks how it fails and recovers."],
                    ["How it is applied", "Ramp 10 → 100 virtual users in steps (JMeter or Locust), hold at 100 for 30 minutes, watch response time, error rate, CPU, memory and database connections.",
                     "Keep adding users and spikes past 100, kill a dependency, then check the error message, the recovery time and that no data is lost."],
                    ["Which failure it prevents", "The crash at <b>90 users</b>: the application already failed <i>inside</i> its specification (e.g. an exhausted connection pool or a memory leak). A load test exposes it before deployment.",
                     "The crash at <b>150 users</b>: the system must degrade gracefully (queue or politely refuse users, throttle, auto-scale) and not crash; a stress test finds the breaking point and the fix."]],
                   [3.0 * cm, (w - 3.0 * cm) / 2, (w - 3.0 * cm) / 2]))
    s += mark("each method named and defined 1.5 + 1.5; how it would be run 1 + 1; link to the matching failure 1.5 + 1.5 (the “recovered later” detail is recovery testing, which stress testing includes).")

    # ---------------------------------------------------------------- Q2
    s.append(P("Question 2", "q"))
    s.append(H("(a) Sequence diagram of the equipment lending service", "13"))
    s.append(P("Participants: <b>Student</b>, <b>:LendingSystem</b>, <b>Staff</b> (a person) and <b>Officer</b> (the responsible officer). Three <i>alt</i> or <i>opt</i> fragments carry the decisions: eligibility, the"
               " condition of the returned item (with a nested <i>opt</i> for the penalty), and the overdue fine."))
    s.append(F.seq_lending())
    s += mark("participants and lifelines 2; request, checks and the eligible / else fragment 3; collection (identity check, handover, Borrowed) 2; return and the good / damaged fragment 3; officer decision with the penalty option 2;"
              " overdue fine fragment 1.")

    s.append(H("(b) State diagram of the loan request", "12"))
    s.append(F.state_loan())
    s += bullets(["<b>Requested</b> is entered by <i>submitRequest</i>; the single check has two guarded exits, so the result is Approved (reserveItem and notifyApproval) or Rejected (final).",
                  "<b>Approved → Borrowed</b> only when the staff member has verified the identity; the request status changes to <b>Borrowed</b> and the handover is recorded.",
                  "<b>Borrowed</b> leaves in three ways: a good return closes the loan; a damaged return enters <b>Damage Review</b>; passing the return date is a <i>time event</i> into <b>Overdue</b>.",
                  "<b>Overdue</b> may also end in Closed (fine applied) or Damage Review; <b>Damage Review</b> stays until the officer decides, then Closed with or without a penalty."])
    s += mark("initial and the two final states 2; seven states 3; every transition with event, guard and action 5; the time event and the overdue fine 2.")

    s.append(H("(c) Issues commonly identified in a code review", "10"))
    s.append(P("A code review is a systematic examination of the source by people other than the author, done before testing or merging, to find defects and design problems early. Typical issues:"))
    s.append(table([["Category", "Typical finding"],
                    ["Logic / functional errors", "off-by-one loops, wrong operator, unhandled case"],
                    ["Missing validation and error handling", "no null check, unchecked return value, resource never closed"],
                    ["Security and performance", "SQL built from user input, a query inside a loop"],
                    ["Design and maintainability", "duplicated code, a class doing several jobs, magic numbers"],
                    ["Standards and readability", "unclear names, inconsistent style, missing comments on non-obvious code"],
                    ["Missing tests or documentation", "a new branch with no test"]], [6.0 * cm, w - 6.0 * cm]))
    s.append(P("<b>Three worked examples [6]:</b>", "lab"))
    s.append(code("""// 1. LOGIC ERROR (off by one)
for (int i = 0; i <= items.length; i++) total += items[i].price;    // ArrayIndexOutOfBounds on the last pass
//    review comment: use  i < items.length  or a for-each loop

// 2. SECURITY + RESOURCE LEAK
String q = "SELECT * FROM users WHERE name = '" + name + "'";     // SQL injection: name = x' OR '1'='1
Statement st = conn.createStatement();  ResultSet rs = st.executeQuery(q);   // never closed
//    review comment: PreparedStatement with a ? parameter, and try-with-resources

// 3. MAINTAINABILITY (duplication and magic number)
double feeA = amount * 0.15 + 20;      // the same line is copied in two other classes
//    review comment: extract  calculateFee(amount)  with named constants  FEE_RATE = 0.15, BASE_FEE = 20"""))
    s += mark("what a review is and why 1; issue categories 3; three examples each with the defect and the fix 2 each = 6.")

    # ---------------------------------------------------------------- Q3
    s.append(P("Question 3", "q"))
    s.append(H("(a) Abstract Factory for the emergency platform", "15"))
    s.append(P("<b>Pattern [3].</b> <b>Abstract Factory.</b> Each deployment needs a <i>family</i> of four compatible products, a European gateway must work only with the European console and logger, and the client must"
               " not name concrete classes. One factory per region creates its own four products, so mixing regions is impossible by construction, and a new region is a new factory plus four product classes with <i>no edit</i> of"
               " the platform code (Open/Closed). The conditional statements are replaced by polymorphism: the only place that chooses a region is the start-up registry."))
    s.append(P("<b>Class diagram [4].</b>", "lab"))
    s.append(F.af_emergency())
    s.append(P("<b>Java code [8].</b>", "body"))
    s.append(code(J("q3a/Main.java", None, "// ---- Japan family")))
    s.append(code(J("q3a/Main.java", "// ---- Japan family", None)))
    s.append(P("Output of <font face='Mono'>java Main EU</font>:", "small"))
    s.append(code("""[EU] AML / E112 location of unit-12
[EU] EU-Alert cell broadcast: Flood warning
[EU] 112 dispatch rescue team 7 -> Flood warning
[EU] GDPR-compliant record: Flood warning"""))
    s += mark("pattern and reasons 3.", "diagram: factory interface with four create methods, three factories, four product interfaces, concrete products, client uses only interfaces 4.",
              "code: four product interfaces 1.5, abstract factory 1, one complete family 2, the client built through the factory 2, region selection without region-specific conditionals in the application logic 1.5.")

    s.append(H("(b) Three SOLID violations in PaymentService", "12"))
    s.append(table([["Principle", "Where it is broken", "Why it is a problem", "Improvement"],
                    ["<b>SRP</b> Single Responsibility", "<font face='Mono'>PaymentService</font> processes payments, saves them (<font face='Mono'>savePayment</font>) and prints receipts (<font face='Mono'>generateReceipt</font>)",
                     "three reasons to change: payment rules, storage, receipt layout", "split into PaymentMethod classes, a PaymentRepository and a ReceiptGenerator; PaymentService only orchestrates"],
                    ["<b>OCP</b> Open/Closed", "the <font face='Mono'>if (method.equals(\"CARD\")) … else if (\"BKASH\")</font> chain in <font face='Mono'>processPayment</font>",
                     "Nagad or Rocket means editing and retesting a working method", "interface <font face='Mono'>PaymentMethod</font> with <font face='Mono'>CardPayment</font>, <font face='Mono'>BkashPayment</font>; look the method up in a map (Strategy)"],
                    ["<b>DIP</b> Dependency Inversion", "<font face='Mono'>new MySQLDatabase()</font> inside <font face='Mono'>savePayment</font>",
                     "the high-level service depends on a concrete database; it cannot be swapped or faked in a test", "depend on <font face='Mono'>PaymentRepository</font>; pass the implementation in through the constructor"]],
                   [2.3 * cm, 4.6 * cm, 4.2 * cm, w - 11.1 * cm]))
    s.append(P("<b>Improved code</b> (compiled and run: prints <i>Processing bkash payment 500.0, Saving to MySQL: 500.0, Generating receipt: 500.0</i>):", "lab"))
    s.append(code(J("q3b/Main.java", None, "public class Main")))
    s += mark("each violation identified with the offending code 1.5 × 3 = 4.5; explanation 1.5 × 3 = 4.5; improvement 1 × 3 = 3.")

    s.append(H("(c) An example of the Open/Closed Principle", "8"))
    s.append(P("<b>Statement [2].</b> Software entities (classes, modules, methods) should be <b>open for extension but closed for modification</b>: new behaviour is added by writing new code, not by editing code that already works and is tested."
               " It is achieved with abstraction and polymorphism."))
    s.append(P("<b>Example [6]:</b> an area calculator.", "lab"))
    s.append(code(J("q3c/Main.java", None, "public class Main")))
    s.append(P("The first <font face='Mono'>BadAreaCalculator</font> must be edited for every new shape. In the second design a <font face='Mono'>Triangle</font> is a new class only; "
               "<font face='Mono'>AreaCalculator</font> is closed for modification yet open for extension. Output for a 2×3 rectangle, a unit circle and a 4×5 triangle: <font face='Mono'>19.14159…</font>."))
    s += mark("principle stated 2; violating design 2; OCP design that really adds a shape without editing 3; explanation 1.")

    # ---------------------------------------------------------------- Q4
    s.append(P("Question 4", "q"))
    s.append(H("(a) Builder for cluster configurations", "15"))
    s.append(P("<b>Pattern [3].</b> <b>Builder.</b> A cluster has many optional and dependent parts, the constructor with many parameters and the conditionals are the problem, the university wants <i>step-by-step</i> construction of"
               " <i>valid</i> configurations and the <i>construction process separate from the final object</i>. The Builder collects the settings one call at a time, and <font face='Mono'>build()</font> is the single place that validates"
               " them (GPU libraries need GPU-capable nodes, distributed storage needs the storage service, nothing incomplete is deployed). The product is immutable and has a private constructor, so an invalid cluster cannot exist."
               " An optional <b>Director</b> holds the recipes for the common projects (machine learning, data archiving). Abstract Factory would create families, and Factory Method one product in one step, so neither fits."))
    s.append(P("<b>Class diagram [4].</b>", "lab"))
    s.append(F.builder_cluster())
    s.append(P("<b>Code [8].</b>", "body"))
    s.append(code(J("q4a/Main.java", None, "    static class Builder")))
    s.append(code(J("q4a/Main.java", "    static class Builder", "public class Main")))
    s.append(P("Output of the demo (two valid recipes, then an invalid one that is refused):", "small"))
    s.append(code("""16 nodes x 32 CPU, 512 GB (high-mem), BOTH, HIGH_SPEED_INTERCONNECT, Linux/Docker +GPU,
   auth=true, enc=true, policies=[lab-members-only]
4 nodes x 8 CPU, 64 GB, DISTRIBUTED, STANDARD, Linux/Docker, auth=true, enc=true, policies=[read-only-for-students]
Invalid cluster: [user authentication is mandatory, GPU libraries need GPU-compatible compute nodes,
   distributed storage needs the distributed-storage service]"""))
    s += mark("pattern and reasons 3.", "diagram: product, builder with step methods and build(), director, client 4.",
              "code: immutable product with private constructor 2, fluent builder steps 2.5, validation in build() with the two stated rules and incompleteness 2.5, director 1.")

    s.append(H("(b) Refactoring FineService with the SOLID principles", "12"))
    s.append(P("<b>What is wrong:</b> <b>SRP</b> — one class calculates fines, sends notifications and talks to the database; <b>OCP</b> — a new researcher rate means editing the <font face='Mono'>if / else if</font>, and a new notification"
               " channel means editing <font face='Mono'>notifyUser</font>; <b>DIP</b> — <font face='Mono'>new MySQLDatabase()</font> binds the fine logic to MySQL, so PostgreSQL cannot replace it “without modifying the fine-management logic”."
               " (The paper's code also has typos, <i>Srting</i> and an unquoted string, and the fine type and the channel are strings, which invites mistakes.)"))
    s.append(F.solid_fine())
    s.append(code(J("q4b/Main.java", None, "public class Main")))
    s.append(P("<b>How the two new requirements are met:</b> “researchers pay a different rate” = add <font face='Mono'>ResearcherFine</font> (rate 3 per day is assumed) and one line "
               "<font face='Mono'>c.put(\"RESEARCHER\", new ResearcherFine())</font>; “replace MySQL with PostgreSQL” = pass <font face='Mono'>new PostgreSQLFineRepository()</font> to the constructor. "
               "<font face='Mono'>FineService</font> is not edited. Run: <i>Fine saved to PostgreSQL / Sending email: You owe 12.0 for 4 day(s) late</i>."))
    s += mark("violations SRP, OCP, DIP identified 3; interfaces and implementations for calculation, notification and persistence 4.5; FineService with injected abstractions 2.5; both new requirements shown 2.")

    s.append(H("(c) Minimal dataset for condition coverage", "8"))
    s.append(code("""something(int x) {
    if (x < 0 || y < x) {      // C1: x < 0        C2: y < x       (y is a variable outside the method)
        y := -y;
        x := -x;
    }
    z := x;
}"""))
    s.append(P("<b>Condition coverage</b> asks that every atomic condition takes <b>both</b> truth values at least once. Two tests are enough when both conditions are evaluated:", "body"))
    s.append(table([["Test", "(x, y)", "C1 = x &lt; 0", "C2 = y &lt; x", "decision (C1 || C2)"],
                    ["T1", "(−1, 0)", "true", "false  (0 &lt; −1)", "true"],
                    ["T2", "(1, 0)", "false", "true  (0 &lt; 1)", "true"]], [1.4 * cm, 2.6 * cm, 3.3 * cm, 4.2 * cm, w - 11.5 * cm]))
    s.append(P("<b>Minimal length = 2.</b> Note that this set does <i>not</i> give decision coverage (the decision is true both times). If the language <b>short-circuits</b> <font face='Mono'>||</font>, C2 is not evaluated"
               " when C1 is true, so a test with C1 true says nothing about C2 and <b>3</b> tests are needed: <font face='Mono'>(−1, 0)</font> (C1 true), <font face='Mono'>(1, 5)</font> (C1 false, C2 false) and"
               " <font face='Mono'>(2, 1)</font> (C1 false, C2 true); this set also covers both outcomes of the decision."))
    s += mark("conditions identified 2; a correct 2-test set 3; the caveats (decision coverage and short-circuit) 3.")

    # ======================================================================= SECTION B
    s += [Spacer(1, 4), banner("SECTION B", GREEN)]
    s.append(P("Question 5", "q"))
    s.append(H("(a) Observer: the server-room Control Center", "10"))
    s.append(P("<b>Pattern.</b> <b>Observer</b> (publish–subscribe): one subject, many dependents that must be told automatically when the state changes, that can be added and removed at run time, and that the subject must not know"
               " concretely. The <i>ControlCenter</i> is the subject; <i>AcUnit</i>, <i>Alarm</i>, <i>Logger</i> and <i>SmsDevice</i> are observers; the sensor only calls the Control Center, so it never depends on a device."))
    s.append(F.observer_server())
    s.append(code(J("q5a/Main.java", None, "class SmsDevice")))
    s.append(code(J("q5a/Main.java", "class SmsDevice", None)))
    s.append(P("Output (the timestamp comes from the clock; the SMS device is unregistered before the last reading):", "small"))
    s.append(code("""LOG <time>  temperature = 26.0           SMS: server room is at 26.0 C       <- AC stays off (26 is not above 28)
AC: ON  (29.0 C)                         LOG ... 29.0   SMS ... 29.0
ALARM: 41.0 C is dangerous!              LOG ... 41.0   SMS ... 41.0       <- AC is already on, no message
AC: OFF (23.0 C)                         LOG ... 23.0                         <- no SMS: the device was removed"""))
    s += mark("pattern named and justified 2; interfaces and ControlCenter with register / unregister / notify 3; the three devices with their rules (AC hysteresis 28 / 24, alarm 40, timestamped log) 3; sensor independent of devices 1; runnable demo 1.")

    s.append(H("(b) Ethics of undisclosed AI intervention bots", "10"))
    s.append(P("<b>Yes, there are serious ethical concerns.</b> The goal (stopping cyberbullying) is good, but the means are not.", "body"))
    s.append(table([["Concern", "Why it is a problem", "Code of ethics (ACM / IEEE-CS)"],
                    ["<b>Deception</b>: bots impersonate neutral human mediators", "users are misled about who they talk to; “neutrality” is faked; trust in the platform and in real mediators is damaged", "Public (1), Judgment (4): honesty"],
                    ["<b>No informed consent or transparency</b>: users cannot identify the bots", "people cannot decide how much weight to give the intervention, and the platform manipulates conversations covertly", "Public (1), Product (3)"],
                    ["<b>Automatic, public rebuking</b> on an AI “flag”", "false positives (sarcasm, friends joking, reclaimed words) shame innocent users; no appeal; bias against dialects or groups", "Product (3), Judgment (4)"],
                    ["<b>No accountability or human oversight</b>", "nobody answers for a wrong intervention; harm to a vulnerable victim is not escalated", "Management (5), Public (1)"],
                    ["<b>Privacy</b>: all conversations are scanned", "monitoring without clear notice or data limits", "Public (1), Client and Employer (2)"]], [4.4 * cm, w - 9.9 * cm, 5.5 * cm]))
    s.append(P("<b>Redesign that keeps the goal [justified]:</b>", "lab"))
    s += bullets(["<b>Disclose the bot.</b> Clearly labelled as “Safety Assistant (AI)”, never posing as a person or a mediator; the policy is stated in the terms and in a short in-app notice. Honest, so trust is kept.",
                  "<b>Private, supportive first steps.</b> A private nudge to the likely harasser (“this message may hurt”) and private support, resources and a one-tap report to the likely target, instead of public rebuking.",
                  "<b>Human in the loop.</b> Serious or repeated cases go to trained human moderators; the bot only flags and assists. Users can contest a flag (appeal) and see why it was raised.",
                  "<b>Fairness and accountability.</b> Test the classifier for false positives and bias across languages and dialects, keep audit logs, name an accountable owner, publish transparency reports.",
                  "<b>Privacy by design.</b> Analyse only what is needed, keep little data, give an opt-out for private chats, and review the effect on bullying and on wrongly flagged users before wide release."])
    s += mark("concerns identified and linked to principles 5; redesign with at least four measures 4; justification that the goal is preserved 1.")

    s.append(H("(c) Comprehensive unit tests for gcd", "15"))
    s.append(P("<b>Test design.</b> Equivalence classes of the inputs: positive, zero, negative, equal, divisible, coprime, large; boundary values at 0, ±1 and the <font face='Mono'>int</font> limits; and two properties that must hold for"
               " every pair (commutativity, the result divides both). The function widens to <font face='Mono'>long</font> before <font face='Mono'>Math.abs</font>, which correctly handles <font face='Mono'>Integer.MIN_VALUE</font> as an <i>input</i>."))
    s.append(code("""import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import static org.junit.jupiter.api.Assertions.*;

class MathUtilsTest {
    @ParameterizedTest(name = "gcd({0}, {1}) = {2}")                       // 1. typical positive pairs
    @CsvSource({"12,18,6", "18,12,6", "17,13,1", "12,4,4", "4,12,4", "1071,462,21", "46368,75025,1", "1000000007,998244353,1"})
    void positiveInputs(int a, int b, int expected) { assertEquals(expected, MathUtils.gcd(a, b)); }

    @Test void bothZeroGivesZero() { assertEquals(0, MathUtils.gcd(0, 0)); }          // 2. zero

    @ParameterizedTest @CsvSource({"0,5,5", "5,0,5", "0,-5,5", "-5,0,5", "0,1,1"})
    void oneZeroGivesAbsoluteValueOfTheOther(int a, int b, int expected) { assertEquals(expected, MathUtils.gcd(a, b)); }

    @ParameterizedTest @CsvSource({"-12,18,6", "12,-18,6", "-12,-18,6", "-7,7,7"})   // 3. negative and mixed signs
    void negativeInputs(int a, int b, int expected) { assertEquals(expected, MathUtils.gcd(a, b)); }

    @ParameterizedTest @CsvSource({"7,7,7", "1,99,1", "99,1,1", "-1,0,1"})            // 4. equal, one, divisor
    void equalAndUnit(int a, int b, int expected) { assertEquals(expected, MathUtils.gcd(a, b)); }

    @Test void largeValues() {                                                        // 5. int limits
        assertEquals(Integer.MAX_VALUE, MathUtils.gcd(Integer.MAX_VALUE, Integer.MAX_VALUE));
        assertEquals(1, MathUtils.gcd(Integer.MAX_VALUE, 1));
        assertEquals(1, MathUtils.gcd(Integer.MAX_VALUE, Integer.MAX_VALUE - 1));
        assertEquals(1 << 20, MathUtils.gcd(1 << 30, 1 << 20));
        assertEquals(2, MathUtils.gcd(Integer.MIN_VALUE, 6));
        assertEquals(1, MathUtils.gcd(Integer.MIN_VALUE, Integer.MAX_VALUE));
    }

    @Test void propertiesHoldForManyPairs() {                                         // 6. properties
        int[] v = {0, 1, -1, 2, 12, -18, 35, 1071, 462, Integer.MAX_VALUE, Integer.MIN_VALUE + 1};
        for (int a : v) for (int b : v) {
            int g = MathUtils.gcd(a, b);
            assertTrue(g >= 0, "non-negative");
            assertEquals(g, MathUtils.gcd(b, a), "commutative");
            if (g != 0) { assertEquals(0, a % g); assertEquals(0, b % g); }
        }
    }

    @Test void resultIsAlwaysNonNegativeEvenForMinValue() {                           // 7. documented contract: "non-negative"
        assertTrue(MathUtils.gcd(Integer.MIN_VALUE, 0) >= 0);                         // FAILS: returns -2147483648
        assertTrue(MathUtils.gcd(0, Integer.MIN_VALUE) >= 0);                         // FAILS
        assertTrue(MathUtils.gcd(Integer.MIN_VALUE, Integer.MIN_VALUE) >= 0);         // FAILS
    }
}"""))
    s.append(P("<b>The suite finds a real defect.</b> The mathematical answer for <font face='Mono'>gcd(Integer.MIN_VALUE, 0)</font> (also <font face='Mono'>(0, MIN)</font> and <font face='Mono'>(MIN, MIN)</font>) is 2<super>31</super>,"
               " which does not fit in an <font face='Mono'>int</font>; the final <font face='Mono'>(int) x</font> wraps to <b>−2147483648</b>, violating the documented “non-negative” result (checked by running it). All other tests pass"
               " (the values were checked against a reference run). A fix: before the cast, <font face='Mono'>if (x &gt; Integer.MAX_VALUE) throw new ArithmeticException(\"gcd does not fit in an int\");</font> (then test with"
               " <font face='Mono'>assertThrows</font>), or return <font face='Mono'>long</font>."))
    s += mark("equivalence classes covered (positive, zero, negative, equal, divisor, coprime) 6; boundaries and large values 3; properties test 2; the MIN_VALUE defect found and explained 3; clear naming and structure 1.")

    # ---------------------------------------------------------------- Q6
    s.append(P("Question 6", "q"))
    s.append(H("(a)(i) State and Strategy", "5"))
    s.append(P("<b>Structurally similar:</b> in both, a <i>context</i> holds a reference to an interface and delegates a request to the current implementation; the concrete classes implement the same interface."))
    s.append(table([["", "Strategy", "State"],
                    ["Intent", "define a <b>family of interchangeable algorithms</b> and let the client pick one", "let an object <b>change its behaviour when its internal state changes</b>, so it seems to change class"],
                    ["Who changes it", "the <b>client</b> (or configuration) chooses and sets it, usually once", "the <b>object itself</b>: states (or the context) switch to the next state in response to events"],
                    ["Awareness", "strategies are independent and know nothing of each other", "states know the next states they lead to (transitions)"],
                    ["Example", "sort by quick, merge or insertion sort; a pricing scheme", "a gumball machine: no-coin, has-coin, sold; a document: draft, review, published"]],
                   [2.6 * cm, (w - 2.6 * cm) / 2, (w - 2.6 * cm) / 2]))
    s.append(P("<b>Key difference:</b> Strategy is about <i>how</i> a task is done and is chosen from outside; State is about <i>what the object currently is</i> and changes itself over time through transitions."))
    s += mark("intent of each 2 + 2; the key difference 1.")

    s.append(H("(a)(ii) The abstract class in Template Method", "5"))
    s.append(P("<b>Role [3].</b> The abstract class <i>defines the skeleton of an algorithm</i> in one <b>template method</b>, writes the steps that are the same for everybody (concrete methods), declares the steps that vary as <b>abstract"
               " primitive operations</b> that subclasses must implement, and may offer <b>hooks</b> (empty or default methods subclasses may override). It controls the flow and calls the subclass (the Hollywood principle: "
               "“don't call us, we'll call you”), which removes duplicated code from the subclasses."))
    s.append(code(J("q6a/Main.java", None, "class CsvParser")))
    s.append(P("<b>Why the template method is final [2].</b> The order of the steps is the invariant of the algorithm. If a subclass could override the template method it could change, skip or reorder the steps and break the guarantees"
               " (for example calling <font face='Mono'>close()</font> every time). Declaring it <font face='Mono'>final</font> lets subclasses vary only the designated steps and never the algorithm's structure."))
    s += mark("role of the abstract class (skeleton, common steps, abstract steps, hooks) 3; why final 2.")

    s.append(H("(b) Krishi Kontho: requirements elicitation and process model", "15 + 10"))
    s.append(P("<b>(i) The team lead's assumption is wrong.</b> The Ministry only says the system should be “useful”, so the requirements are neither clear nor stable, and an LLM voice service for farmers is new to everybody. The two"
               " methods are judged against the target users: rural farmers with limited literacy and smartphone or internet access, local dialects, strong seasonality (harvest time) and a preference for voice."))
    s.append(table([["", "Survey", "Co-design workshop"],
                    ["Strengths", "reaches many farmers in three upazilas cheaply; quantifiable (which crop and livestock problems are most common); quick to analyse; can be run by phone or on paper",
                     "rich, face to face; local agricultural officers and the Ministry contribute domain knowledge; ownership and early buy-in; conflicts are discussed and resolved; ideas are checked at once"],
                    ["Limitations here", "low literacy and little internet limit online surveys; farmers cannot say what they need from an LLM voice service they have never used; closed questions miss unknown needs; low response and"
                     " social-desirability bias; no follow-up; says nothing about the call context (noise, dialect)",
                     "costly and slow to organise in three upazilas, farmers may not be free in the season; officers and Ministry staff can dominate, quiet farmers and women are not heard; small sample; needs skilled facilitators;"
                     " people describe what they say they do, not what they do"]], [2.6 * cm, (w - 2.6 * cm) / 2, (w - 2.6 * cm) / 2]))
    s.append(P("<b>Verdict.</b> Both are useful but <b>insufficient</b>: they depend on farmers being able to describe a need in the abstract. Add:", "body"))
    s += bullets(["<b>Contextual inquiry / field observation and short interviews</b> in markets, farms and union offices, in the farmers' own language and setting: it reveals how farmers actually look for advice today (whom they call,"
                  " in what words), which no survey asks about.",
                  "<b>Analysis of existing records</b>, such as the call logs and question lists of an existing agriculture helpline, to find the common crop and livestock problems quickly (a document and data analysis).",
                  "<b>Prototype-based elicitation</b>: a Wizard-of-Oz voice prototype in one upazila in the first month, so farmers react to a working service instead of describing an imagined one; their reactions become the backlog."])
    s.append(P("<b>Why this suits the context:</b> it is fast (fits the four months), it respects low literacy (spoken, observed, demonstrated), and it turns the vague “useful” into measurable requirements, for example “the system"
               " answers the 20 most frequent crop problems correctly in Bangla dialects, within 60 seconds of speech, for 90 % of test calls”. Surveys can still be used to <i>validate</i> priorities, and a smaller co-design workshop with"
               " farmers (not only officers) to review the prototype."))
    s.append(P("<b>(ii) Process model [10]: Agile (Scrum) with incremental delivery.</b>", "lab"))
    s.append(table([["Reason", "Why it matters here"],
                    ["Requirements are vague and will change", "short sprints with farmers' feedback turn “useful” into concrete backlog items; waterfall needs stable requirements and would fail"],
                    ["Fixed date, fixed scope of a <i>pilot</i>", "time-boxed sprints (2 weeks) and a prioritised backlog: if time runs short, the least valuable stories are dropped, not the date"],
                    ["Technical and quality risks (speech recognition for dialects, wrong or unsafe LLM advice)", "early spikes and prototypes in the first sprints; each increment is tested with real farmers"],
                    ["Three upazilas", "increments are released to one upazila first, then widened; lessons feed the next sprint"],
                    ["Strong customer involvement is possible", "the Ministry's product owner and local officers review every sprint; documentation is kept light"]], [5.6 * cm, w - 5.6 * cm]))
    s.append(P("<b>Plan:</b> month 1 — elicitation + Wizard-of-Oz prototype and the technical spike (sprints 1–2); months 2–3 — build, test and release increments to one upazila (sprints 3–6); month 4 — harden, safety review"
               " of the LLM answers, deploy to three upazilas and rehearse for the fair (sprints 7–8). <b>Rejected:</b> waterfall (stable requirements assumed), pure prototyping (a deployable pilot is needed), and a long"
               " incremental plan without feedback loops."))
    s += mark("(i) each method's strengths and limitations in this context 3 + 3 + 3 + 3; alternative method(s) with justification 3; (ii) Agile/Scrum recommended 2, reasons linked to the scenario 5, a plan and the rejected models 3.")

    # ---------------------------------------------------------------- Q7
    s.append(P("Question 7", "q"))
    s.append(H("(a)(i) Transparency and accountability as ethical obligations", "10"))
    s.append(P("<b>Why.</b> An automated system that approves a loan, suggests a diagnosis or removes a post changes a person's money, health or voice. The people affected cannot protect themselves unless they can know that a"
               " system decided and why (<b>transparency</b>), and unless somebody can be asked to explain, correct and make good the harm (<b>accountability</b>). The ACM / IEEE-CS Code asks engineers to act for the public interest (1),"
               " deliver products that meet professional standards (3), and be honest about limits; managers must take responsibility (5)."))
    s += bullets(["<b>Transparency means:</b> telling people when an automated decision is used, what data it uses, the main reasons for a result, and the system's known limits (error rates, bias).",
                  "<b>Accountability means:</b> a named owner for the system and its harm, audit trails and logs, a way to appeal to a human, and a duty to fix and compensate. “The algorithm did it” is not an excuse."])
    s.append(P("<b>Example (loan approval).</b> A bank's credit model rejects a small-business owner. With no explanation she cannot tell whether the data was wrong (a mistaken default record), whether the rule is unfair (her"
               " postcode), or how to improve; with no accountable owner she has no appeal. Reported cases of the same kind include credit-limit models accused of giving women lower limits than men with similar finances, and diagnosis"
               " assistants whose advice clinicians could not question. With transparency (reasons, data used) and accountability (a human review and an owner) the mistake is found and corrected, and trust in the"
               " company is kept."))
    s += mark("transparency explained 2.5, accountability explained 2.5, link to the code of ethics 2, a worked example with consequences 3.")

    s.append(H("(a)(ii) “If refactoring does not reduce code size or improve performance, it has failed”", "5"))
    s.append(P("<b>The statement is wrong.</b> Refactoring is <i>improving the internal structure of code without changing its external behaviour</i>. Its success is judged by readability, lower coupling and complexity, removal of"
               " duplication, easier extension and testing, and by the tests still passing, not by size or speed."))
    s += bullets(["Code often <b>grows</b> after a good refactoring: Extract Method adds methods, Replace Conditional with Polymorphism adds classes. The result is still better.",
                  "Refactoring is <b>not performance optimisation</b>; they are separate activities. Refactoring can even cost a little speed (more small method calls); optimise later, measured, on the clean design.",
                  "<b>Partly true</b> only in one case: removing duplicated code does reduce size. Real goals are to make the code easy to understand, find bugs, and speed up <i>future</i> development."])
    s += mark("definition 1.5, why size and speed are the wrong tests 2, examples 1.5.")

    s.append(H("(b) BrewBuddy: Bridge and Strategy", "20"))
    s.append(P("<b>Two independent variations, so two patterns.</b>"))
    s.append(table([["Requirement", "Pattern", "Justification"],
                    ["Three set menus × a drink that can be Coke, Lemonade or Mango Juice (and new drinks later); every menu works with every drink; no class per combination; the receipt shows the combined description and"
                     " calories", "<b>Bridge</b>", "the set menu (<i>abstraction</i>) and the drink (<i>implementor</i>) vary independently. The menu holds a <font face='Mono'>Drink</font> reference (the bridge) and delegates the name"
                                                      " and the calories to it. 3 menus + 3 drinks = <b>6</b> classes instead of 3 × 3 = 9, and a new drink is <b>one</b> class instead of one per menu (4th drink: 7 versus 12)."],
                    ["Regular, Happy Hour and Loyalty pricing; exactly one per order, chosen at checkout and changeable at run time; a new scheme must not edit existing classes; no if / switch on scheme names",
                     "<b>Strategy</b>", "each scheme is a class implementing <font face='Mono'>PricingStrategy.price(basePrice, customer)</font>, which sees only the base price and the customer data. The order holds the current strategy and"
                                        " <font face='Mono'>setPricing</font> swaps it at run time. A new scheme is a new class (Open/Closed)."]], [6.6 * cm, 2.4 * cm, w - 9.0 * cm]))
    s.append(P("<b>Why not the alternatives:</b> a subclass per menu-and-drink pair (9 classes and growing) is the class explosion Bridge avoids; Decorator adds responsibilities optionally and can be stacked, but here exactly one drink is"
               " mandatory and never changes the price; an <font face='Mono'>if / else</font> on scheme names violates the stated rule and Open/Closed.", "small"))
    s.append(P("<b>Class diagram:</b>", "lab"))
    s.append(F.bridge_strategy())
    s.append(code(J("q7b/Main.java", "abstract class SetMenu", "class Customer") + "\n// ... Drink, Coke, Lemonade, MangoJuice as above;  strategies:\n" + J("q7b/Main.java", "interface PricingStrategy", "class Order")))
    s.append(P("Output of the demo (Burger Meal 650 kcal + Lemonade 200 kcal; customer has 450 points): <i>Burger Meal with Lemonade, 850 kcal | pay 350.0</i>; with Happy Hour 10 % <i>… | pay 315.0</i>; with Loyalty (4 %) <i>… | pay 336.0</i>"
               " (the loyalty rule is assumed)."))
    s += mark("Bridge identified and justified 6; Strategy identified and justified 6; class diagram with both patterns 6; alternatives or extension discussion 2.")

    # ---------------------------------------------------------------- Q8
    s.append(P("Question 8", "q"))
    s.append(H("(a) Five non-functional requirements of UniConnect", "10"))
    s.append(table([["NFR (type)", "Measurable form", "Justification from the scenario"],
                    ["<b>1. Performance and scalability</b>", "handle 40,000 registered users and 10,000+ simultaneous logins in the two-hour window; login and page response ≤ 3 s at the 95th percentile; scale out under load",
                     "tens of thousands log in at once during registration and “frequently overwhelm” the current system"],
                    ["<b>2. Usability and localisation</b>", "a first-time user completes course registration in ≤ 5 minutes without help; Bangla and English interface; accessible design",
                     "international students unfamiliar with the local interface; every interaction must feel “intuitive”"],
                    ["<b>3. Compatibility / efficiency on low-end devices and slow networks</b>", "works on Android 8+ with 2 GB RAM; page weight ≤ 1 MB; usable on a 3G connection (pages load in ≤ 5 s); responsive layout",
                     "many students use low-end Android phones on slow mobile connections"],
                    ["<b>4. Reliability, availability and data integrity</b>", "no submitted assignment is ever lost: each upload is acknowledged only after it is stored durably (replicated), with a receipt; availability ≥ 99.9 % in the registration window; automatic failover and backups",
                     "“no submitted assignment should ever be lost due to a system failure”"],
                    ["<b>5. Extensibility and maintainability</b>", "a new service (library, hostel, scholarships) can be added as a module without changing existing modules and without more than 5 % loss of response time",
                     "library, hostel and scholarship services are planned “without any degradation in performance”"]], [4.0 * cm, w - 10.0 * cm, 6.0 * cm]))
    s.append(P("Security and privacy (single sign-on, tuition payment, results) is also implied; it is a sixth NFR that would score as a bonus mention.", "small"))
    s += mark("each of five distinct NFRs with a measurable statement 1.2 and a justification tied to the scenario 0.8.")

    s.append(H("(b) Six code smells and the refactored code", "25"))
    s.append(table([["#", "Smell", "Where", "Refactoring used"],
                    ["1", "<b>Switch statements / conditionals on type codes</b>", "<font face='Mono'>\"LIGHT\"</font> / <font face='Mono'>\"FAN\"</font> tests in <font face='Mono'>turnOn</font> and again in <font face='Mono'>activateNightMode</font>; the user-type if-chains",
                     "Replace Type Code with Subclasses / Replace Conditional with Polymorphism (<font face='Mono'>Light</font>, <font face='Mono'>Fan</font>); user type moved into an enum with its brightness and surcharge"],
                    ["2", "<b>Long method / deep nesting</b>", "<font face='Mono'>turnOn</font>: loop, id test, type test, user test, logging in one method", "Extract Method, Replace Nested Conditional, <font face='Mono'>findDevice</font> with Optional"],
                    ["3", "<b>Long parameter list</b>", "<font face='Mono'>log</font> has 7 parameters; <font face='Mono'>calculateDeviceCost</font> 5; the <font face='Mono'>Device</font> constructor 5",
                     "Preserve Whole Object: <font face='Mono'>log(device, user, action)</font>"],
                    ["4", "<b>Data clumps</b>", "(userId, userName, userType) are fields, constructor and log parameters; (deviceId, deviceName, room) travel together", "Extract Class <font face='Mono'>User</font>; pass the <font face='Mono'>Device</font>"],
                    ["5", "<b>Primitive obsession and magic numbers</b>", "strings for types, roles and the action; <font face='Mono'>100/70/50/30</font>, <font face='Mono'>35/28</font>, <font face='Mono'>12.5</font>, <font face='Mono'>1.30</font>, <font face='Mono'>5</font> hours,"
                     " parallel lists <font face='Mono'>deviceNames</font> / <font face='Mono'>deviceCosts</font>", "enums (<font face='Mono'>UserRole</font>, <font face='Mono'>Action</font>), named constants, <font face='Mono'>BillItem</font> instead of parallel lists"],
                    ["6", "<b>Feature envy and a large class / divergent change</b>", "<font face='Mono'>SmartHomeSystem</font> controls devices, logs and bills; <font face='Mono'>calculateBill</font> and <font face='Mono'>BillManagement</font> use almost only <font face='Mono'>Device</font> data;"
                     " <font face='Mono'>Device</font> is a pure data class", "Move Method (<font face='Mono'>usageHours</font> into Device), Extract Class (<font face='Mono'>AuditLog</font>, <font face='Mono'>BillingService</font>, <font face='Mono'>Bill</font>)"]],
                   [0.6 * cm, 3.5 * cm, w - 10.6 * cm, 6.5 * cm]))
    s.append(P("Also present: <b>hard-coded <font face='Mono'>int temperature = 30</font></b> inside <font face='Mono'>turnOn</font> (it never reads a sensor), a <b>wrong log entry</b> for device types other than LIGHT and FAN"
               " (it is logged as “ON” although nothing was switched on), the undeclared <font face='Mono'>room</font> in <font face='Mono'>calculateDeviceCost</font>, and the unused parameter <font face='Mono'>deviceId</font>.", "small"))
    s.append(P("<b>Refactored design:</b>", "lab"))
    s.append(F.refactor_design())
    s.append(P("<b>Refactored code (compiled and run):</b>", "body"))
    s.append(code(J("q8b/Main.java", None, "class AuditLog")))
    s.append(code(J("q8b/Main.java", "// ---------- the long parameter list", None)))
    s.append(P("Output for a GUEST user with one lamp (0.06) and one fan (0.07), after night mode (guest surcharge 1.3, 5 hours, rate 12.5):", "small"))
    s.append(code("""LOG -> Device: L1, Name: Lamp, Room: Bedroom, User: U1, User Name: Rafi, User Type: GUEST, Action: ON
LOG -> Device: F1, Name: Ceiling fan, Room: Hall, User: U1, User Name: Rafi, User Type: GUEST, Action: ON
Night mode activated
Device: Lamp Room: Bedroom Cost: 4.875
Device: Ceiling fan Room: Hall Cost: 5.6875
Lamp = 4.875
Ceiling fan = 5.6875
TOTAL = 10.5625"""))
    s.append(P("<b>Behaviour kept:</b> brightness 100 / 70 / 50 by role, fan speed from the temperature (&gt; 35 → 3, &gt; 28 → 2, else 1), night mode 30 and 1, and bill = power × hours × 12.5 with the 30 % guest surcharge are exactly the original rules."
               " The only intended change is that a device of an unknown type is now really switched on (it used to be logged as ON without being switched on)."))
    s += mark("six smells named with the evidence 12 (2 each); refactored code that removes all six and compiles 10; behaviour preserved / explanation 3.")

    s += [Spacer(1, 10), P("— End of solutions —", "sub")]
    return s
