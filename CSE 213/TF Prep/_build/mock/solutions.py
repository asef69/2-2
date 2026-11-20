"""solutions.py - model answers and marking scheme for mock paper v2 (2023-24 / 2022-23 layout)."""
from pdfkit import *  # noqa: F401,F403
import sol_figs as F


def H(t, m):
    return P("%s &nbsp;<font color='#6b7280' size='9'>[%s]</font>" % (t, m), "h2")


def mark(*items):
    """small 'marking scheme' list."""
    return [P("Marking scheme", "sol")] + bullets(list(items))


def story(fw):
    s = []
    w1 = fw

    # =================================================================== cover + map
    s += [P("MOCK TERM FINAL — MODEL ANSWERS", "title"), P("CSE 213 &nbsp;•&nbsp; Software Engineering &nbsp;•&nbsp; 210 marks", "sub"),
          Spacer(1, 6),
          P("Use this file <b>after</b> you have sat the paper. The answers are written the way a full-mark script would look; where the course allows"
            " more than one acceptable answer this is said. Be strict when you mark yourself: a diagram earns its marks only if every class, state,"
            " actor or message is <b>named</b> and every association end carries the right <b>multiplicity or label</b>.")]
    s.append(P("What each question tests, and which real question it copies", "h2"))
    rows = [["Q", "Topic", "Marks", "Modelled on", "Your notes"],
            ["1(a)", "Use case diagram", "7", "2023-24 Q1(a)", "Anindya L19–20"],
            ["1(b)", "Requirements + state diagram", "4+10", "2023-24 Q1(b)", "IJ L21; Anindya L13–15"],
            ["1(c)", "Equivalence classes, BVA, weak ECT", "10", "2023-24 Q1(c); 2022-23 Q1(b)", "Anindya L27"],
            ["1(d)", "SRP / OCP / ISP violations", "6", "2023-24 Q1(d) slot", "Anindya L2–3"],
            ["1(e)", "Internal / external integration testing", "8", "2022-23 Q1(c)", "Anindya L24"],
            ["2(a)", "Observer: UML + two code halves", "6+8+8", "2023-24 Q2(a); 2022-23 Q4(a)", "IJ L7"],
            ["2(b)", "UML using a pattern (Composite)", "8", "2023-24 Q2(b)", "IJ L2"],
            ["3(a)", "TDD and its benefits", "6+6", "2023-24 Q3(a)", "IJ L15"],
            ["3(b)", "White-box test cases for a method", "10", "2023-24 Q3(b)", "Anindya L25–26"],
            ["3(c)", "Equivalence-partitioning principle", "8", "2023-24 Q3(c)", "Anindya L27"],
            ["4(a)", "Class diagram: accounts, composite, 2-step login", "12", "2022-23 Q4(b)", "Anindya L9–11; IJ L2"],
            ["4(b)", "Smallest dataset for condition coverage", "10", "2022-23 Q4(c)", "Anindya L25"],
            ["4(c)", "Interface Segregation Principle example", "8", "2022-23 Q2(c)", "Anindya L3"],
            ["5(a)", "Abstract Factory: pattern + diagram + code", "15", "2023-24 Q5(a)", "Anindya L6"],
            ["5(b)", "One class as Adapter and Decorator", "12", "2023-24 Q5(b)", "IJ L1, L3"],
            ["5(c)", "Why high test coverage matters", "8", "2023-24 Q5(c)", "Anindya L25"],
            ["6(a)", "Ethics scenario: breaches", "8", "2023-24 Q6(a)", "IJ L20"],
            ["6(b)", "“Public interest” principle", "7", "2023-24 Q6(b)", "IJ L20"],
            ["6(c)", "Incremental vs agile; code-review issues", "8+12", "2023-24 Q8(a); 2022-23 Q2(b)", "IJ L12–13, L16"],
            ["7(a)", "Core activities; waterfall", "4+6", "2022-23 Q6(a)", "IJ L11–12"],
            ["7(b)", "Kanban: lead time, WIP", "10", "2022-23 Q6(b)", "IJ L14"],
            ["7(c)", "Scrum sprint; two backlogs", "9+6", "2022-23 Q6(c)", "IJ L14"],
            ["8(a)", "Four code smells defined", "15", "2022-23 Q5(a)", "IJ L18"],
            ["8(b)", "Three refactorings of code fragments", "6+7+7", "2022-23 Q5(b); 2023-24 Q8(c)", "IJ L19"]]
    s.append(table(rows, [1.1 * cm, 6.0 * cm, 1.4 * cm, 4.7 * cm, w1 - 13.2 * cm]))
    s.append(Spacer(1, 4))
    s.append(P("<b>Mark split copied exactly:</b> Section A = a 45-mark compulsory case study + two of three 30-mark questions; Section B = a 35-mark compulsory"
               " question + two of three 35-mark questions (2023-24 layout). Inside each question the parts are 15 / 12 / 8 (2022-23 style) or one big part with"
               " (i)(ii)(iii) sub-marks (2023-24 style)."))
    s.append(P("<b>Slots that had to be swapped.</b> The real papers also ask about security (CIA, encryption, buffer overflow, SQL injection), earned-value"
               " management, risk tables, critical-path slack, DevOps and caching, “manager vs leader”, and the Chain-of-Responsibility and Facade patterns. None of these is in"
               " your current slide sets (Facade, CoR, Command and Interpreter were removed from the syllabus), so each slot was filled by the nearest in-syllabus question of the"
               " same size: security case study → state diagram + test design on a login; EVM / risk → Kanban and Scrum; CoR → Composite UML; Adapter + Facade → Adapter + Decorator."
               " Section A also has no state or sequence diagram as a stand-alone question because neither paper asked one."))
    s.append(P("Score sheet", "h2"))
    s.append(table([["Section A", "Q1 /45", "Q2 /30", "Q3 /30", "Q4 /30", "Two used", "Total /105"],
                    ["Your marks", "", "", "", "", "", ""],
                    ["Section B", "Q5 /35", "Q6 /35", "Q7 /35", "Q8 /35", "Two used", "Total /105"],
                    ["Your marks", "", "", "", "", "", ""]], [2.6 * cm] + [(w1 - 2.6 * cm) / 6] * 6, header=False))
    s.append(Spacer(1, 3))
    s.append(P("Bands (out of 210): <b>170+</b> exam-ready &nbsp;•&nbsp; <b>140–169</b> good, patch the lost topics &nbsp;•&nbsp; <b>105–139</b>"
               " revise the weak lessons, redo the question &nbsp;•&nbsp; <b>below 105</b> go back to the notes before another mock."))
    s.append(P("Time plan: Q1 about 45 minutes, Q5 about 35 minutes, the four chosen questions about 25 minutes each, and 10 minutes at the end for a final check.", "small"))
    s.append(Spacer(1, 4))

    # =================================================================== SECTION A
    s += [banner("SECTION A — model answers")]

    # ---------------------------------------------------------------- Q1
    s.append(P("Question 1 &nbsp;(MediLink case study)", "q"))
    s.append(H("(a) Use case diagram", "7"))
    s.append(F.d_usecase())
    s += bullets(["<b>Include</b> — <i>Book Appointment</i> «include» <i>Check Availability</i>: the check happens <b>every</b> time an appointment is booked, so it is a mandatory,"
                  " reusable sub-behaviour (the arrow points from the base to the included use case).",
                  "<b>Extend</b> — <i>Apply Insurance</i> «extend» <i>Pay Bill</i>: it happens only <b>sometimes</b> (only for insured patients), so it is optional behaviour that"
                  " extends the base use case (the arrow points from the extension to the base)."])
    s += mark("actors: Patient, Doctor, Receptionist, Admin and the external SMS Gateway 2 (an external system is an actor).", "system boundary 1.",
              "use cases with the right associations 2.", "one correct include + one correct extend, each justified 2.")

    s.append(H("(b) Requirements and the account state diagram", "14"))
    s.append(P("<b>(i) Verifiable requirements [4].</b>", "lab"))
    s.append(table([["Label", "Requirement", "Why it is verifiable"],
                    ["Functional", "If a user enters a wrong password three times in a row, the system shall lock the account.", "enter 3 wrong passwords, see the account locked"],
                    ["Functional", "The system shall require a user whose password is older than 90 days to set a new one before any other action.", "age a password, log in, see the forced change"],
                    ["Non-functional (performance)", "A login attempt shall finish (accepted or rejected) within 2 seconds for 95 % of attempts with 500 users logging in at the same time.", "load test, measure the 95th percentile"],
                    ["Non-functional (security)", "Passwords shall be stored only as salted hashes, and the login page shall be served only over HTTPS (TLS 1.2 or higher).", "inspect the database and the TLS configuration"]],
                   [3.3 * cm, w1 - 9.3 * cm, 6.0 * cm]))
    s.append(P("“Fast” or “secure” alone would earn nothing: a requirement must contain a quantity or a test.", "small"))
    s.append(P("<b>(ii) State diagram [10].</b>", "lab"))
    s.append(F.d_account_state())
    s += bullets(["The three live states share one exit, so they are drawn inside an <b>Enabled</b> superstate: <i>disable [by Admin]</i> from the superstate to <b>Disabled</b> means"
                  " “from Active, Locked or Expired”. Drawing three separate arrows is equally correct.",
                  "A successful login resets the counter (<font face='Mono'>login [ok] / attempts = 0</font> as an internal transition of Active); it is optional but shows care.",
                  "<i>after(15 min)</i> and <i>after(90 days)</i> are <b>time events</b>; <i>wrongPassword</i>, <i>changePassword</i>, <i>adminUnlock</i> and <i>disable</i> are call/signal events."])
    s += mark("(i) each requirement 1 (type correct and verifiable).", "(ii) initial + final state 1.5, Active/Locked/Expired/Disabled 3, the guarded wrongPassword pair 2,"
              " the two time events with actions 2, changePassword and the Admin transitions 1.5.")

    s.append(H("(c) Password rule: equivalence classes and boundary values", "10"))
    s.append(P("<b>(i) Equivalence classes [3]</b> (1 valid + 2 invalid for the length, 1 + 1 for each of the other two):", "lab"))
    s.append(table([["Property", "Valid class", "Invalid classes"],
                    ["length", "8 ≤ length ≤ 16", "length &lt; 8;   length &gt; 16"],
                    ["digit", "at least one digit", "no digit"],
                    ["uppercase", "at least one uppercase letter", "no uppercase letter"]], [3.0 * cm, 6.5 * cm, w1 - 9.5 * cm]))
    s.append(P("<b>(ii) Robust BVA on the length [3]</b> (digit and uppercase satisfied in every case; nominal value 12):", "lab"))
    s.append(table([["Length", "Password", "Expected"],
                    ["7  (min − 1)", "Abcdef1", "rejected"], ["8  (min)", "Abcdefg1", "accepted"], ["9  (min + 1)", "Abcdefgh1", "accepted"],
                    ["12 (nominal)", "Abcdefghij12", "accepted"], ["15 (max − 1)", "Abcdefghijklmn1", "accepted"], ["16 (max)", "Abcdefghijklmno1", "accepted"],
                    ["17 (max + 1)", "Abcdefghijklmnop1", "rejected"]], [3.3 * cm, 6.0 * cm, 3.0 * cm]))
    s.append(P("<b>(iii) Weak equivalence class set [4].</b> Weak ECT needs one test per class, so the number of tests is the size of the <i>largest</i> variable, which is 3 (the length):", "lab"))
    s.append(table([["Test", "Password", "Classes covered", "Expected", "Kind"],
                    ["T1", "Secret12", "length valid, digit valid, uppercase valid", "accepted", "positive"],
                    ["T2", "ab", "length &lt; 8, no digit, no uppercase", "rejected", "negative"],
                    ["T3", "Abcdefghijklmnopqrs1", "length &gt; 16 (20 chars), digit valid, uppercase valid", "rejected", "negative"]],
                   [1.2 * cm, 4.2 * cm, w1 - 11.4 * cm, 2.6 * cm, 3.4 * cm]))
    s.append(P("<b>Strong</b> equivalence class testing takes every combination: 3 × 2 × 2 = <b>12</b> cases. Note on T2: it breaks three rules at once, so if it is rejected you cannot tell which check"
               " worked; under the single-fault assumption add <font face='Mono'>Abcdefgh</font> (no digit only) and <font face='Mono'>abcdefg1</font> (no uppercase only)."))
    s += mark("(i) 3 for the seven classes (−1 for each missing invalid class, minimum 0).", "(ii) the six boundary lengths 1.5, concrete passwords 1, expected results 0.5.",
              "(iii) a valid 3-case set 2, positive/negative labels 1, strong = 12 with working 1.")

    s.append(H("(d) Design principles", "6"))
    s.append(table([["Fragment", "Principle", "How it is broken", "Fix"],
                    ["AppointmentManager does booking, billing, SMS and PDFs", "<b>SRP</b> (Single Responsibility)",
                     "four reasons to change in one class", "split into AppointmentService, BillingService, SmsNotifier, ReportPrinter"],
                    ["PaymentProcessor.pay(String mode) if-chain", "<b>OCP</b> (Open/Closed)",
                     "each new payment method means editing and retesting pay()", "interface PaymentMethod with Cash, Card, Mobile classes (Strategy); pay() just calls method.pay(amount)"],
                    ["ClinicStaff with treat(), register(), managePayroll()", "<b>ISP</b> (Interface Segregation)",
                     "Receptionist is forced to implement methods it does not use", "split into Treats, Registers, ManagesPayroll; each class implements only the roles it has"]],
                   [4.4 * cm, 3.1 * cm, 4.5 * cm, w1 - 12.0 * cm]))
    s += mark("2 per fragment: name 0.5, reason 0.75, fix 0.75.")

    s.append(H("(e) Integration testing", "8"))
    s += bullets(["<b>Internal integration testing [2 + 1]</b> checks modules that <i>we</i> build against each other through our own interfaces. <i>MediLink test:</i> after Login succeeds for patient P1, booking"
                  " an appointment stores it under P1's id, and Billing later lists exactly that appointment's items.",
                  "<b>External integration testing [1 + 1]</b> checks our system against a third-party or outside system. <i>MediLink test:</i> Notification sends a reminder through the real SMS gateway"
                  " (sandbox) and the phone number is accepted in the gateway's format; a gateway time-out is handled without losing the appointment."])
    s.append(P("<b>(ii) Missing module [4].</b> If Billing <i>calls</i> Appointment to fetch bill items, Billing is the caller and Appointment is below it, so write an <b>AppointmentStub</b> that returns a fixed list of items"
               " (and a few error cases). Starting from the higher-level module and stubbing the lower one is <b>top-down integration</b>. (If the call went the other way — Appointment calling"
               " Billing — you would write a <b>driver</b> that calls Billing, and the step would be bottom-up.) Say which direction you assumed; both earn the marks."))
    s += mark("(i) internal vs external definitions 2, one MediLink test each 2.", "(ii) stub named and its job 2, top-down (or driver / bottom-up with the matching reason) 2.")

    # ---------------------------------------------------------------- Q2
    s.append(P("Question 2", "q"))
    s.append(H("(a) Observer: LiveScore", "22"))
    s.append(P("<b>(i) Class diagram [6].</b> The score must be pushed to several independent displays that come and go, and the Match must not know their classes: <b>Observer</b> (one-to-many dependency,"
               " publish–subscribe).", "lab"))
    s.append(F.d_observer())
    s.append(P("<b>(ii) Subject interface and Match [8].</b>", "lab"))
    s.append(code("""import java.util.ArrayList;
import java.util.List;

interface Subject {
    void attach(Observer o);
    void detach(Observer o);
    void notifyObservers();
}

class Match implements Subject {
    private final List<Observer> observers = new ArrayList<>();
    private int runs, wickets;
    private double overs;

    public void attach(Observer o) { if (!observers.contains(o)) observers.add(o); }
    public void detach(Observer o) { observers.remove(o); }

    public void notifyObservers() {
        for (Observer o : new ArrayList<>(observers))      // copy: an observer may detach itself inside update()
            o.update(runs, wickets, overs);                 // push model: the state travels with the call
    }

    public void updateScore(int runs, int wickets, double overs) {
        this.runs = runs;  this.wickets = wickets;  this.overs = overs;
        notifyObservers();                                  // every state change informs all observers
    }
}"""))
    s.append(P("<b>(iii) Observer, a concrete observer and main [8].</b>", "lab"))
    s.append(code("""interface Observer {
    void update(int runs, int wickets, double overs);
}

class MobileWidget implements Observer {
    private final String owner;
    MobileWidget(String owner) { this.owner = owner; }
    public void update(int runs, int wickets, double overs) {
        System.out.println(owner + "'s phone: " + runs + "/" + wickets + " in " + overs + " overs");
    }
}

class WebsitePanel implements Observer {
    public void update(int runs, int wickets, double overs) {
        System.out.println("Website: " + runs + "/" + wickets + " (" + overs + ")");
    }
}

public class LiveScoreDemo {
    public static void main(String[] args) {
        Match match = new Match();
        Observer rafi = new MobileWidget("Rafi");
        Observer web  = new WebsitePanel();
        match.attach(rafi);
        match.attach(web);
        match.updateScore(120, 3, 20.0);     // both are told
        match.detach(rafi);                   // Rafi stops following
        match.updateScore(135, 4, 22.3);     // only the website is told
    }
}
// output:  Rafi's phone: 120/3 in 20.0 overs
//          Website: 120/3 (20.0)
//          Website: 135/4 (22.3)"""))
    s += mark("(i) Subject + Observer interfaces 2, Match and the three displays with realisation arrows 2.5, the 0..* observers association 1, roles named 0.5.",
              "(ii) list + attach/detach 3, notifyObservers loops and calls update 2.5, updateScore stores state then notifies 2.5.",
              "(iii) Observer interface 1.5, MobileWidget 2.5, main: attach two, update, detach one, update 4.")

    s.append(H("(b) Composite UML", "8"))
    s.append(F.d_composite())
    s += mark("Widget as the common abstract type 1, Label and Button as leaves 1, Panel inheriting Widget 1, Panel aggregating Widget with multiplicity * (children) 2, Window extending Panel 1,"
              " the three roles named (component, leaf, composite) 2.")

    # ---------------------------------------------------------------- Q3
    s.append(P("Question 3", "q"))
    s.append(H("(a) Test-Driven Development", "12"))
    s.append(P("<b>(i) The cycle [6].</b> In TDD the test is written <b>before</b> the code. Work in tiny steps: <b>Red</b> — write one failing test; <b>Green</b> — write the simplest code that makes"
               " it pass; <b>Refactor</b> — clean up the code and the test while everything stays green; then pick the next test.", "lab"))
    s.append(F.d_tdd())
    s.append(code("""// RED: write the test first. It does not even compile, because LeapYear does not exist yet.
public class LeapYearTest {
    @Test public void divisibleBy4IsLeap()      { assertTrue (LeapYear.isLeap(2024)); }
    @Test public void centuryIsNotLeap()        { assertFalse(LeapYear.isLeap(1900)); }
    @Test public void every400thCenturyIsLeap() { assertTrue (LeapYear.isLeap(2000)); }
}

// GREEN for the first test only: the simplest code that passes
class LeapYear { static boolean isLeap(int year) { return year % 4 == 0; } }

// the 1900 test turns RED -> grow the code just enough:  year % 4 == 0 && year % 100 != 0
// the 2000 test turns RED -> (year % 4 == 0 && year % 100 != 0) || year % 400 == 0

// REFACTOR with all three tests green: give the conditions names (this replaces the version above)
class LeapYear {
    static boolean isLeap(int year) {
        boolean ordinaryLeap = year % 4 == 0 && year % 100 != 0;
        boolean centuryLeap  = year % 400 == 0;
        return ordinaryLeap || centuryLeap;
    }
}"""))
    s.append(P("<b>(ii) Benefits and a limitation [6].</b>", "lab"))
    s += bullets(["Every feature has a test, so the suite is a <b>safety net</b> against regressions and coverage is high by construction.",
                  "Writing the test first forces you to think about the <b>interface and behaviour</b> before the implementation, giving small, decoupled, testable units (a design benefit).",
                  "Bugs are found minutes after they are written, when they are <b>cheapest to fix</b>; less time is spent in the debugger.",
                  "The tests are <b>executable documentation</b> of what the code should do.",
                  "Refactoring is <b>safe</b> because the green bar tells you at once if behaviour changed.",
                  "<b>Limitation:</b> it slows the very first steps and needs discipline; the test code must be maintained; it is awkward for GUIs, databases and legacy code, and unit tests"
                  " cannot replace integration, system and acceptance testing."])
    s += mark("(i) the three phases explained 3, the worked leap-year cycle (failing test, minimal code, a refactoring) 3.", "(ii) five benefits 1 each, one limitation 1.")

    s.append(H("(b) White-box test design", "10"))
    s.append(P("<b>(i) Control-flow graph [3].</b> One node per statement group (line 4 and the loop initialisation merged); the loop increment gets its own node <font face='Mono'>i++</font>.", "lab"))
    s.append(F.d_cfg())
    s.append(P("<b>(ii) Cyclomatic complexity [2].</b> V(G) = E − N + 2 = 14 − 11 + 2 = <b>5</b>; V(G) = P + 1 = 4 + 1 = <b>5</b> (decisions on lines 2, 5, 6, 11); V(G) = number of regions = <b>5</b>.", "body"))
    s.append(P("<b>(iii) Branch coverage with the fewest tests [5].</b> Every decision must take its true and its false outcome:", "lab"))
    s.append(table([["Test", "Input", "Decisions taken", "Expected result"],
                    ["TC1", "a = { }", "line 2 = T", "−1"],
                    ["TC2", "a = { −2, 4, 6 }", "line 2 = F; line 5 = T,T,T,F; line 6 = F,T,T; line 11 = F", "10 / 2 = 5.0"],
                    ["TC3", "a = { −1, −5 }", "line 2 = F; line 5 = T,T,F; line 6 = F,F; line 11 = T", "0"]],
                   [1.4 * cm, 3.6 * cm, w1 - 9.4 * cm, 4.4 * cm]))
    s.append(P("<b>Why three is the minimum:</b> line 11 needs one test with no positive element (true) and one with a positive element (false), and line 2 = T returns immediately, so it needs a test of its own."
               " TC1 + TC2 + TC3 cover every branch. <i>Extra:</i> the fifth basis path (loop skipped) is infeasible because line 2 already rejects empty arrays, so only four independent path tests"
               " can actually be run; to also cover the two conditions inside line 2, add a test with <font face='Mono'>a = null</font>."))
    s += mark("(i) nodes 1.5, edges and T/F labels 1.5.", "(ii) 1 for each correct method used, 2 in all.", "(iii) three valid tests 3, expected values 1, minimality argument 1.")

    s.append(H("(c) Equivalence partitioning", "8"))
    s.append(P("<b>(i) [4].</b> The input domain is divided into <b>classes</b> whose members the program is expected to treat in the same way (they trigger the same behaviour, so if one member exposes a fault the others"
               " would too). Testing <b>one representative per class</b> is enough. It is used because exhaustive testing is impossible: it shrinks an enormous or infinite input space to a handful of"
               " meaningful tests, guarantees that every kind of behaviour and every kind of invalid input is tried, and avoids redundant tests. It is combined with boundary-value analysis, since faults cluster at the edges of classes."))
    s.append(P("<b>(ii) [4].</b>", "lab"))
    s.append(table([["Class", "Kind", "Test value", "Expected"],
                    ["age &lt; 18", "invalid", "10", "rejected"], ["18 ≤ age ≤ 60", "valid", "35", "accepted"], ["age &gt; 60", "invalid", "75", "rejected"],
                    ["not an integer (text, empty, decimal)", "invalid", "“abc”", "rejected with a type error"]], [6.0 * cm, 2.4 * cm, 3.0 * cm, w1 - 11.4 * cm]))
    s += mark("(i) principle 2, why used 2.", "(ii) the three range classes, each with a test value, 3; the non-integer class 1.")

    # ---------------------------------------------------------------- Q4
    s.append(P("Question 4", "q"))
    s.append(H("(a) Class diagram of the accounting package", "12"))
    s.append(F.d_accounts())
    s += bullets(["<b>Account</b> is <i>abstract</i> (italic name): it is never created directly. <b>Debtor</b> and <b>Creditor</b> specialise it with their own attribute.",
                  "<b>LedgerGroup</b> is an Account <i>and</i> aggregates 0..* Accounts: this is the <b>Composite</b> structure, so a group answers <font face='Mono'>getBalance()</font> by summing its members,"
                  " exactly like a single Account. Aggregation (open diamond) fits because the members also exist outside the group.",
                  "<b>Clerk</b> 1 — * <b>Transaction</b> and <b>Transaction</b> * — 1 <b>Account</b> give the “exactly one Clerk, exactly one Account” rule.",
                  "<b>Authentication:</b> Clerk depends only on the <i>Authenticator</i> interface. <i>PasswordStep</i> and <i>OtpStep</i> implement it and <i>MultiStepAuthenticator</i> runs a list of steps in order, so a"
                  " third step is one new class and Clerk never changes (Open/Closed)."])
    s += mark("Account hierarchy with abstract class, Debtor and Creditor attributes 3.", "LedgerGroup as Account + aggregate with 0..* 3.", "Clerk–Transaction–Account with all multiplicities 3.",
              "an extensible authentication design (any version that leaves Clerk unchanged is accepted) 3.")

    s.append(H("(b) Decision and condition coverage", "10"))
    s.append(P("<b>(i) [2].</b> Simple conditions: C1 <font face='Mono'>age &gt; 60</font>, C2 <font face='Mono'>years &gt;= 10</font>, C3 <font face='Mono'>age &lt; 18</font>, C4 <font face='Mono'>years &gt; 0</font>."
               " Decisions: D1 (line 3) = C1 || C2 and D2 (line 5) = C3 &amp;&amp; C4."))
    s.append(P("<b>(ii) Decision coverage, two tests [3].</b> D1 needs a true and a false outcome, so one test is not enough:", "lab"))
    s.append(table([["Test", "(age, years)", "D1 (line 3)", "D2 (line 5)", "Returns"],
                    ["A", "(70, 0)", "T  (C1 true, C2 not evaluated)", "F  (C3 false, C4 not evaluated)", "5 + 3 = 8"],
                    ["B", "(10, 5)", "F  (C1 F, C2 F)", "T  (C3 T, C4 T)", "5 − 2 = 3"]], [1.2 * cm, 2.6 * cm, w1 - 11.0 * cm, 4.6 * cm, 2.6 * cm]))
    s.append(P("<b>(iii) Condition coverage, three tests [3].</b> Each of C1…C4 must be evaluated true and false. With short-circuiting, C2 is evaluated only when C1 is false and C4 only when C3 is true, so a"
               " test with C1 true says nothing about C2; therefore at least 3 tests are needed:", "lab"))
    s.append(table([["Test", "(age, years)", "C1", "C2", "C3", "C4", "Returns"],
                    ["X", "(70, 0)", "T", "—", "F", "—", "8"], ["Y", "(10, 12)", "F", "T", "T", "T", "8 − 2 = 6"], ["Z", "(10, 0)", "F", "F", "T", "F", "5"]],
                   [1.2 * cm, 2.6 * cm, 1.6 * cm, 1.6 * cm, 1.6 * cm, 1.6 * cm, w1 - 10.2 * cm]))
    s.append(P("C1: T (X), F (Y, Z) &nbsp;•&nbsp; C2: T (Y), F (Z) &nbsp;•&nbsp; C3: T (Y, Z), F (X) &nbsp;•&nbsp; C4: T (Y), F (Z). All eight outcomes appear (— = not evaluated).", "small"))
    s.append(P("<b>(iv) [2].</b> Yes: D1 is T for X and Y and F for Z; D2 is F for X and Z and T for Y, so this set is also decision-covering. In general it does not have to be: for"
               " <font face='Mono'>if (p || q)</font> the tests (p = T, q = F) and (p = F, q = T) make both conditions true and false, but the decision is true both times and never false."
               " That is why <b>condition/decision</b> coverage (or MC/DC) is used."))
    s += mark("(i) 2.", "(ii) two valid tests 2, expected values 1.", "(iii) three tests 2, shows which conditions are evaluated and the short-circuit reasoning 1.", "(iv) answer 1, the counter-example 1.")

    s.append(H("(c) Interface Segregation Principle", "8"))
    s.append(P("<b>Statement [2].</b> No client should be forced to depend on methods it does not use; prefer several small, client-specific interfaces to one large “fat” interface."))
    s.append(F.d_isp())
    s.append(code("""// VIOLATION: one fat interface
interface OfficeMachine { void print(); void scan(); void fax(); }
class BasicPrinter implements OfficeMachine {
    public void print() { /* ... */ }
    public void scan()  { throw new UnsupportedOperationException(); }   // forced to implement what it cannot do
    public void fax()   { throw new UnsupportedOperationException(); }
}

// FIX: role interfaces
interface Printer    { void print(); }
interface Scanner    { void scan(); }
interface FaxMachine { void fax(); }
class BasicPrinter implements Printer { public void print() { /* ... */ } }
class OfficeCopier implements Printer, Scanner { public void print() { } public void scan() { } }"""))
    s.append(P("<b>Why the first design is bad [3 in all with the example]:</b> a client that only needs <font face='Mono'>print()</font> still depends on <font face='Mono'>scan()</font> and"
               " <font face='Mono'>fax()</font>; a change to <font face='Mono'>fax()</font> forces recompilation of printer clients; callers can call methods that blow up at run time; the empty or throwing"
               " methods also violate the Liskov Substitution Principle."))
    s += mark("statement 2, a clear violating example 3, a corrected design that really segregates the interface 3.")

    # =================================================================== SECTION B
    s += [Spacer(1, 4), banner("SECTION B — model answers", GREEN)]

    # ---------------------------------------------------------------- Q5
    s.append(P("Question 5", "q"))
    s.append(H("(a) Abstract Factory: BrewBox", "15"))
    s.append(P("<b>(i) Pattern [3].</b> <b>Abstract Factory.</b> The café needs a <i>family</i> of two related products (a coffee and a snack) that must come from the same region, and the ordering code must not name any"
               " concrete class. One concrete factory per region creates its own matching pair, so a Dhaka coffee can never be mixed with a Tokyo snack, and a new city is a new factory plus new product"
               " classes with <i>no edit</i> to <font face='Mono'>Cafe</font> (Open/Closed). Factory Method would create one product only, Builder assembles one complex object step by step, and an"
               " <font face='Mono'>if (region == …)</font> chain inside Cafe would break the Open/Closed Principle. Trade-off: adding a third product kind (a dessert) means changing every factory."))
    s.append(P("<b>(ii) Class diagram [5].</b>", "lab"))
    s.append(F.d_abstract_factory())
    s.append(P("<b>(iii) Code [7].</b>", "lab"))
    s.append(code("""interface Coffee { String name(); }
interface Snack  { String name(); }

class CardamomLatte implements Coffee { public String name() { return "Cardamom latte"; } }
class Samosa        implements Snack  { public String name() { return "Samosa"; } }
// Tokyo: class MatchaLatte implements Coffee {..}   class Dorayaki implements Snack {..}

interface RegionFactory {
    Coffee createCoffee();
    Snack  createSnack();
}
class DhakaFactory implements RegionFactory {
    public Coffee createCoffee() { return new CardamomLatte(); }
    public Snack  createSnack()  { return new Samosa(); }
}
// class TokyoFactory implements RegionFactory { new MatchaLatte(), new Dorayaki() }

class Cafe {                                          // knows only the abstract types
    private final RegionFactory factory;
    Cafe(RegionFactory factory) { this.factory = factory; }
    void serveSet() {
        Coffee coffee = factory.createCoffee();
        Snack  snack  = factory.createSnack();
        System.out.println("Serving " + coffee.name() + " with " + snack.name());
    }
}
// new Cafe(new DhakaFactory()).serveSet();    // Serving Cardamom latte with Samosa
// new Cafe(new TokyoFactory()).serveSet();    // Serving Matcha latte with Dorayaki"""))
    s += mark("(i) pattern name 1, reasons 2.", "(ii) factory interface with both create methods 1, abstract products 1, concrete factories 1, concrete products 1, Cafe depends only on abstractions 1.",
              "(iii) abstract products 1.5, Dhaka products 1.5, factory interface + DhakaFactory 2, Cafe built through the factory 2.")

    s.append(H("(b) One class that is both an Adapter and a Decorator", "12"))
    s.append(P("<b>Explanation [3].</b> An <b>Adapter</b> converts the interface of an existing class into the one the client expects. A <b>Decorator</b> implements the <i>same</i> interface as the object it wraps and adds"
               " behaviour to it, so decorators can be stacked. A class can do both when it implements the target interface, holds an <i>adaptee</i> with a different interface (adapter role) and also holds"
               " another object of the target type that it extends (decorator role). Strictly, a pure Decorator does not change the interface; here the class converts <i>and</i> enriches."))
    s.append(F.d_adapter_decorator())
    s.append(code("""interface Notifier { void send(String msg); }

class EmailNotifier implements Notifier {
    public void send(String msg) { System.out.println("EMAIL: " + msg); }
}

class SmsGateway {                                        // vendor class: its API cannot be changed
    void push(String phoneNo, String text) { System.out.println("SMS to " + phoneNo + ": " + text); }
}

// SmsNotifier = ADAPTER (SmsGateway -> Notifier) + DECORATOR (adds SMS to another Notifier)
class SmsNotifier implements Notifier {
    private final SmsGateway gateway;                     // adaptee
    private final String phoneNo;
    private final Notifier wrapped;                       // decorated component, may be null
    SmsNotifier(SmsGateway gateway, String phoneNo, Notifier wrapped) {
        this.gateway = gateway;  this.phoneNo = phoneNo;  this.wrapped = wrapped;
    }
    public void send(String msg) {
        if (wrapped != null) wrapped.send(msg);           // decorator: keep the existing behaviour first
        gateway.push(phoneNo, msg);                       // adapter: translate send(msg) into push(phoneNo, msg)
    }
}
// Notifier n = new SmsNotifier(new SmsGateway(), "01700000000", new EmailNotifier());
// n.send("Server down");     // prints the EMAIL line, then the SMS line"""))
    s += mark("explanation of both roles and how they combine 3.", "class diagram: Notifier, EmailNotifier, SmsGateway, SmsNotifier with the realisation, the adapts arrow and the wraps 0..1 association 5.",
              "code: constructor 1, adapter translation 1.5, decorator delegation 1.5.", "Any sensible dual-role example is accepted if both roles are visible in the code.")

    s.append(H("(c) Test coverage", "8"))
    s += bullets(["<b>Why high coverage matters [3]:</b> coverage measures how much of the code the tests actually execute; high coverage means few untested corners, so more faults are found before release,"
                  " regressions are caught when code changes, refactoring is safe, and dead or unreachable code is spotted. It also shows where more tests are needed.",
                  "<b>Risks of low coverage [2]:</b> faults hide in the untested statements and branches and reach production; changes break old behaviour unnoticed; fixing a field bug costs far more than"
                  " fixing it in testing; the team loses confidence and avoids refactoring.",
                  "<b>100 % statement coverage is not enough [3]:</b> it only proves every statement ran once, not that every decision took both outcomes, or that boundaries and combinations of conditions were tried."])
    s.append(code("""double finalPrice(int qty, double price) {
    double d = 0;
    if (qty > 10) d = 0.10;            // requirement: 10 or more items get the discount
    return price - price * d;
}
// finalPrice(20, 100) = 90 executes every statement (100 % statement coverage) and passes,
// yet the false branch was never taken and the boundary qty = 10 was never tried: the bug
// (> should be >=) is still there. Branch coverage forces qty <= 10 and BVA forces qty = 10."""))
    s += mark("(i) 3, (ii) 2, (iii) explanation 1.5 + working example 1.5.")

    # ---------------------------------------------------------------- Q6
    s.append(P("Question 6", "q"))
    s.append(H("(a) Ethics scenario", "8"))
    s.append(P("<b>Breaches [4].</b> Principles of the ACM/IEEE-CS Software Engineering Code of Ethics:"))
    s += bullets(["<b>1 PUBLIC</b> — customers lose money and the engineer knowingly lets it go on; the public interest includes disclosing an actual danger or harm to the people affected.",
                  "<b>3 PRODUCT</b> — the product must meet the highest professional standards; shipping a known calculation defect does not.",
                  "<b>5 MANAGEMENT</b> — a manager must not ask an engineer to act unethically, and must promote an ethical approach to development and maintenance.",
                  "<b>Honesty / integrity (1 and 4 JUDGMENT)</b> — telling the customers nothing about a defect that charges them wrongly is deception, and the manager's “it is tiny” is a business excuse, not a professional judgment."])
    s.append(P("<b>What the developer should do [4]:</b> (1) record the defect with evidence (affected loans, amounts, test data); (2) report it to the manager in writing and propose a quick hotfix and a refund plan;"
               " (3) if the manager refuses, escalate inside the company (senior engineer, quality or compliance, the ethics channel); (4) refuse to take part in hiding it; (5) as a last resort, and with advice, report it to the"
               " regulator; protect themself by keeping copies of the written requests."))
    s += mark("each principle with the link to the facts 1 (maximum 4); an ordered action plan that puts the public first and ends with outside reporting only as a last step 4.")

    s.append(H("(b) “Consistent with the public interest”", "7"))
    s.append(P("<b>Principle 2, CLIENT AND EMPLOYER [2]:</b> engineers act in the best interest of their client and employer — keep confidences, deliver what was agreed, work within the budget — but <b>only so far as it is"
               " consistent with the public interest</b> (Principle 1). When the two clash, the public interest wins, because the client's authority does not extend to harming third parties."))
    s.append(table([["Conflict", "Why the interests clash", "Resolution"],
                    ["The employer wants to skip security testing to meet a launch date", "saves money for the employer but risks users' data", "refuse to sign off, document the risk, escalate; ship only after the test"],
                    ["A client wants user data sold to advertisers without consent", "profit for the client versus privacy of the users", "decline, explain the legal and ethical limits, offer a consented design"]],
                   [5.0 * cm, 5.4 * cm, w1 - 10.4 * cm]))
    s += mark("principle stated correctly 2, two realistic conflicts 2 each, a resolution that ranks the public interest first 1.")

    s.append(H("(c) (i) Incremental or agile?", "8"))
    s.append(P("<b>Decision [4].</b> Use an <b>incremental</b> approach for the core and bring in <b>agile (Scrum) practices</b> for the vague extras. The core — fixed regulation rules and a hard 3-month date — is"
               " well understood, so it can be planned up front and delivered in increment 1 before the semester. The extras (waiting list, fee payment, advising dashboard) will keep changing, so they"
               " are best built in short sprints with the registrar's office reviewing each one. If the exam forces a single choice, choose <b>incremental</b>: the fixed deadline and the stable core outweigh the"
               " changeable extras."))
    s.append(table([["", "Incremental", "Agile"],
                    ["Planning", "overall plan and architecture first, increments scheduled", "light plan; re-planned every sprint"],
                    ["Requirements", "core fixed up front; later increments added in order", "expected to change; backlog re-prioritised"],
                    ["Delivery", "each increment is a usable release", "working software every 1–4 weeks"],
                    ["Customer", "feedback after each increment", "customer takes part daily"],
                    ["Documentation", "moderate to heavy", "just enough; code and tests"]],
                   [3.0 * cm, (w1 - 3.0 * cm) / 2, (w1 - 3.0 * cm) / 2]))
    s += mark("a clear decision tied to the scenario (fixed core, hard date, vague extras) 4, a correct comparison of at least four aspects 4.")

    s.append(H("(c) (ii) Code review", "12"))
    s.append(table([["Issue category", "Concrete example"],
                    ["Coding-standard / naming violations", "a field called <font face='Mono'>d</font> instead of <font face='Mono'>daysOverdue</font>; inconsistent brace style"],
                    ["Logic and functional errors", "off-by-one in a loop (<font face='Mono'>i &lt;= n</font> instead of <font face='Mono'>i &lt; n</font>); wrong operator in a condition"],
                    ["Missing error handling or validation", "no null check on a method argument; a file or connection that is never closed"],
                    ["Duplicated or badly structured code", "the same 10 lines copied into two classes; a 200-line method doing five jobs"],
                    ["Security and performance problems", "SQL built by string concatenation; a database query inside a loop"],
                    ["Missing tests or documentation", "a new branch with no test; a public method with no explanation"]],
                   [5.8 * cm, w1 - 5.8 * cm]))
    s.append(P("<b>Practices that make a review effective [2]:</b> review small chunks (about 200–400 lines) for no longer than an hour, using a <b>checklist</b>; let the author explain the change first;"
               " critique the code, not the person; use static-analysis tools for the mechanical issues so reviewers can focus on logic and design; track metrics such as defect rate and defect density."))
    s += mark("five issue categories with examples 2 each = 10, two practices 1 each.")

    # ---------------------------------------------------------------- Q7
    s.append(P("Question 7", "q"))
    s.append(H("(a) Core activities and the waterfall model", "10"))
    s.append(P("<b>(i) [4].</b> The generic process model has five framework (core) activities: <b>Communication</b> (talk to the customer, gather requirements), <b>Planning</b> (estimate, schedule, plan the work),"
               " <b>Modeling</b> (analysis and design models), <b>Construction</b> (code generation and testing) and <b>Deployment</b> (deliver, support, collect feedback). Umbrella activities such as quality assurance,"
               " risk and configuration management run across all of them."))
    s.append(P("<b>(ii) Waterfall [6].</b>", "lab"))
    s.append(F.d_waterfall())
    s.append(table([["Advantages (any two)", "Disadvantages (any two)"],
                    ["simple and easy to manage; each phase has a clear deliverable and milestone", "real projects rarely run strictly in sequence; going back is costly"],
                    ["good documentation, a clear audit trail", "all requirements must be fixed at the start, but customers cannot state them completely"],
                    ["works well when the requirements are stable and well understood", "a working product appears only at the end, so serious faults are found late"]],
                   [(w1) / 2, (w1) / 2]))
    s += mark("(i) five activities 0.8 each. (ii) diagram 2, two advantages 2, two disadvantages 2.")

    s.append(H("(b) Kanban", "10"))
    s.append(P("<b>(i) Board [3].</b>", "lab"))
    s.append(F.d_kanban())
    s.append(P("<b>(ii) Times [4].</b> Lead time = delivered − requested; cycle time = delivered − work started (days counted as differences).", "lab"))
    s.append(table([["Card", "Lead time", "Cycle time", "Waiting before work (lead − cycle)"],
                    ["K1", "6 − 1 = 5", "6 − 2 = 4", "1"], ["K2", "9 − 1 = 8", "9 − 3 = 6", "2"], ["K3", "8 − 2 = 6", "8 − 5 = 3", "3"], ["K4", "10 − 3 = 7", "10 − 4 = 6", "1"],
                    ["<b>Average</b>", "<b>26 / 4 = 6.5 days</b>", "<b>19 / 4 = 4.75 days</b>", "1.75"]], [2.4 * cm, 4.0 * cm, 4.0 * cm, w1 - 10.4 * cm]))
    s.append(P("<b>(iii) The finished card D3 [3].</b> She <b>may not</b> pull a new card: Development is at its WIP limit (3 of 3, and a finished card still occupies a slot until it moves on), and D3 cannot move to Review because"
               " Review is also full (2 of 2). The right move is to <b>help clear the bottleneck</b> — review R1 or R2, or pair with the reviewers — and only then move D3 across and pull new work. This is the"
               " Kanban principle of <b>limiting work in progress</b> with a <b>pull system</b>: stop starting, start finishing. A full column makes the bottleneck visible, so the team fixes the flow instead of piling up unfinished work."))
    s += mark("(i) columns with WIP limits 1.5, cards in the right columns 1.5.", "(ii) the four lead times 1, the four cycle times 1, the two averages 2.", "(iii) answer “no” with both reasons 1.5, correct action 1, principle 0.5.")

    s.append(H("(c) Scrum", "15"))
    s.append(P("<b>(i) One sprint [9].</b>", "lab"))
    s.append(F.d_scrum())
    s += bullets(["<b>Roles [3]:</b> <b>Product Owner</b> — owns and orders the product backlog, represents the customer; <b>Scrum Master</b> — coaches the team, protects it and removes impediments; <b>Development Team</b> —"
                  " self-organising and cross-functional, builds the increment.",
                  "<b>Artefacts [2]:</b> product backlog, sprint backlog and the increment (a burn-down chart is optional).",
                  "<b>Activities in order [4]:</b> <b>Sprint Planning</b> (choose items from the product backlog, agree a sprint goal and form the sprint backlog) → the <b>Sprint</b> itself, 1–4 weeks, with a"
                  " 15-minute <b>Daily Scrum</b> (what I did, what I will do, what blocks me) → <b>Sprint Review</b> (demonstrate the increment to stakeholders and update the product backlog) →"
                  " <b>Sprint Retrospective</b> (the team improves its way of working) → the next sprint."])
    s.append(P("<b>(ii) Two backlogs [6].</b>", "lab"))
    s.append(table([["", "Product backlog", "Sprint backlog"],
                    ["Owner", "Product Owner", "Development Team"],
                    ["Content", "all features, fixes and ideas wanted in the product, ordered by value", "only the items chosen for this sprint, broken into tasks"],
                    ["Scope and life", "lives as long as the product; always changing", "fixed for one sprint; ends with the sprint"],
                    ["Detail", "coarse at the bottom, detailed at the top", "tasks estimated in hours"]],
                   [2.6 * cm, (w1 - 2.6 * cm) / 2, (w1 - 2.6 * cm) / 2]))
    s += mark("(i) roles 3, artefacts 2, four events in the right order 4.", "(ii) three correct contrasts 2 each.")

    # ---------------------------------------------------------------- Q8
    s.append(P("Question 8", "q"))
    s.append(H("(a) Four code smells", "15"))
    s.append(table([["Smell", "Meaning", "Example", "Refactoring"],
                    ["<b>Divergent Change</b> [4]", "one class is changed for many different reasons",
                     "<font face='Mono'>Employee</font> has updatePersonalInfo(), formatForReport(), sendEmail(), calculatePay(): DB, report and pay-rule changes all edit it",
                     "<b>Extract Class</b> — one class per reason to change"],
                    ["<b>Data Clumps</b> [4]", "the same few data items always travel together",
                     "<font face='Mono'>processPayment(name, email, cardNumber, expiry, amount)</font>; <font face='Mono'>(startDate, endDate)</font> in many signatures",
                     "<b>Introduce Parameter Object</b> / Extract Class (<font face='Mono'>PaymentDetails</font>, <font face='Mono'>DateRange</font>)"],
                    ["<b>Primitive Obsession</b> [4]", "domain concepts are held in primitives, strings or parallel arrays",
                     "<font face='Mono'>int[] std_ID; String[] std_name; double[] std_marks;</font> or a phone number as a String, a status as int 0/1/2",
                     "<b>Replace Data Value with Object</b> / Extract Class (<font face='Mono'>Student</font>); Replace Type Code with class or enum"],
                    ["<b>Lazy Class</b> [3]", "a class that does too little to justify its existence",
                     "a <font face='Mono'>Logger</font> with one method that just calls System.out.println; a subclass that adds nothing",
                     "<b>Inline Class</b> / Collapse Hierarchy"]],
                   [2.9 * cm, 3.4 * cm, w1 - 10.7 * cm, 4.4 * cm]))
    s += mark("each smell: definition 1.5 (Lazy Class 1), example 1.5, correct refactoring 1.")

    s.append(H("(b) Three refactorings", "20"))
    s.append(P("<b>(i) Complex condition [6].</b> Smell: a long, hard-to-read boolean expression with magic numbers. Refactoring: <b>Decompose Conditional</b> (<b>Extract Variable</b> / Extract Method) and"
               " <b>Replace Magic Number with Symbolic Constant</b>."))
    s.append(code("""private static final int MIN_AGE = 18, MAX_AGE = 60;
private static final double MIN_INCOME = 30000;

boolean isEligible(Applicant a) {
    boolean workingAge = a.getAge() >= MIN_AGE && a.getAge() <= MAX_AGE;
    boolean canRepay   = a.getMonthlyIncome() > MIN_INCOME || a.hasGuarantor();
    boolean cleanRecord = !a.isBlacklisted();
    return workingAge && canRepay && cleanRecord;
}
"""))
    s.append(P("<b>(ii) Type code [7].</b> Smell: a <b>switch statement</b> on a type code (repeated wherever behaviour depends on the type; a new type means editing it). Refactoring:"
               " <b>Replace Conditional with Polymorphism</b> (Replace Type Code with Subclasses).", "body"))
    s.append(code("""abstract class Employee {
    double salary;
    abstract double getBonus();
}
class Engineer extends Employee { double getBonus() { return salary * 0.10; } }
class Manager  extends Employee { double getBonus() { return salary * 0.20 + 5000; } }
class Intern   extends Employee { double getBonus() { return 0; } }
// a new kind of employee = one new class; no default branch or exception is needed any more"""))
    s.append(P("<b>(iii) Nested conditionals [7].</b> Smell: deeply nested <font face='Mono'>if / else</font> with a temporary <font face='Mono'>result</font> variable. Refactoring:"
               " <b>Replace Nested Conditional with Guard Clauses</b> (the first two tests can also be merged with <b>Consolidate Conditional Expression</b>).", "body"))
    s.append(code("""double deliveryCharge(Order o) {
    if (o.isCancelled() || o.isPickup()) return 0;     // guard clauses: exit early for the special cases
    if (o.total() >= 1000)               return 30;
    return 60;                                         // the normal case is the last line, not buried in an else
}"""))
    s += mark("(i) smell 1.5, refactoring named 1.5, correct code 3 (caller: <font face='Mono'>if (isEligible(applicant)) approve(applicant);</font>).", "(ii) smell 2, refactoring named 1, polymorphic classes 3, benefit (new type = new class) 1.",
              "(iii) smell 2, refactoring named 1.5, guard-clause code 3.5. The refactored code must give the same results as the original in every case.")

    s += [Spacer(1, 10), P("— End of model answers —", "sub")]
    return s
