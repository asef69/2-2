"""solutions.py - model answers and marking scheme for the mock paper."""
from pdfkit import *  # noqa: F401,F403
import sol_figs as F

SPLIT = "•"


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
    s.append(P("What each question tests", "h2"))
    rows = [["Q", "Topic", "Marks", "Where it is in your notes"],
            ["1(a)", "Abstract Factory (class diagram + Java)", "15", "Anindya notes, Lesson 6"],
            ["1(b)", "SRP, OCP, DIP violations and refactoring", "10", "Anindya notes, Lessons 1–3"],
            ["1(c)", "Thread-safe Singleton", "10", "Anindya notes, Lesson 7"],
            ["2(a)", "Class diagram from a scenario (association class)", "20", "Anindya notes, Lessons 9–11"],
            ["2(b)", "State diagram, event kinds", "15", "Anindya notes, Lessons 13–15"],
            ["3(a)", "Use case diagram + use case description", "20", "Anindya notes, Lessons 19–20"],
            ["3(b)", "Sequence diagram with alt; collaboration diagram", "15", "Anindya notes, Lessons 16–18"],
            ["4(a)", "Equivalence classes, weak/strong ECT, robust BVA", "15", "Anindya notes, Lesson 27"],
            ["4(b)", "CFG, V(G), basis paths, branch/condition coverage", "20", "Anindya notes, Lessons 25–26"],
            ["5(a)", "Decorator (class diagram + Java)", "15", "IJ notes, Lesson 1"],
            ["5(b)", "Observer", "10", "IJ notes, Lesson 7"],
            ["5(c)", "Adapter (object vs class)", "10", "IJ notes, Lesson 3"],
            ["6(a)", "Mediator", "15", "IJ notes, Lesson 8"],
            ["6(b)", "Composite", "10", "IJ notes, Lesson 2"],
            ["6(c)", "Bridge", "10", "IJ notes, Lesson 4"],
            ["7(a)", "Choosing a process model", "15", "IJ notes, Lesson 12"],
            ["7(b)", "Scrum", "10", "IJ notes, Lesson 14"],
            ["7(c)", "Kanban, WIP, lead and cycle time", "10", "IJ notes, Lesson 14"],
            ["8(a)", "Code smells and refactoring", "15", "IJ notes, Lessons 17–19"],
            ["8(b)", "JUnit test class", "10", "IJ notes, Lesson 15"],
            ["8(c)", "Ethics (ACM/IEEE-CS) and requirement quality", "10", "IJ notes, Lessons 20–21"]]
    s.append(table(rows, [1.2 * cm, 7.4 * cm, 1.4 * cm, w1 - 10.0 * cm]))
    s.append(Spacer(1, 4))
    s.append(P("<b>Not on this paper</b> (so practise them from the topic-wise book): Factory Method, Builder, Strategy, Template Method, State pattern, BPMN,"
               " CRC cards, loop testing, XP/agile principles, code review and MoSCoW. A paper of 6 answered questions cannot touch every lesson; because"
               " you may choose 2 of 3, it is worth solving the questions you did <i>not</i> choose as well."))
    s.append(P("Score sheet", "h2"))
    s.append(table([["Section A", "Q1 /35", "Q2 /35", "Q3 /35", "Q4 /35", "Choice used", "Total /105"],
                    ["Your marks", "", "", "", "", "", ""],
                    ["Section B", "Q5 /35", "Q6 /35", "Q7 /35", "Q8 /35", "Choice used", "Total /105"],
                    ["Your marks", "", "", "", "", "", ""]], [2.6 * cm] + [(w1 - 2.6 * cm) / 6] * 6, header=False))
    s.append(Spacer(1, 3))
    s.append(P("Bands (out of 210): <b>170+</b> exam-ready &nbsp;•&nbsp; <b>140–169</b> good, patch the lost topics &nbsp;•&nbsp; <b>105–139</b>"
               " revise the weak lessons, redo the question &nbsp;•&nbsp; <b>below 105</b> go back to the notes before another mock."))
    s.append(P("Time plan for the real sitting: about 25 minutes per question, leaving 30 minutes for the compulsory questions' diagrams and a final check.", "small"))
    s.append(Spacer(1, 4))

    # =================================================================== SECTION A
    s += [banner("SECTION A — model answers")]

    # ---------------------------------------------------------------- Q1
    s.append(P("Question 1", "q"))
    s.append(H("(a) Abstract Factory", "15"))
    s.append(P("<b>(i) Pattern [3].</b> <b>Abstract Factory.</b> The client needs a <i>family</i> of two related products (fee calculator + rider allocator)"
               " that must belong to the same city, and it must not name concrete classes. Each city is one concrete factory that creates its own pair, so"
               " the pair can never be mixed (Dhaka fees with Chattogram allocation). A third city means a new factory and two new product classes and"
               " <i>no change</i> to <font face='Mono'>OrderService</font> (Open/Closed). Factory Method would create only one product, and Builder assembles one"
               " complex object step by step, so neither fits."))
    s.append(P("<b>(ii) Class diagram [6].</b>", "lab"))
    s.append(F.d_abstract_factory())
    s.append(P("<b>(iii) Code [6].</b>", "lab"))
    s.append(code("""interface FeeCalculator  { double fee(int km); }
interface RiderAllocator { Rider allocate(Order o); }

class DhakaFee implements FeeCalculator {
    public double fee(int km) { return 40 + 10 * km; }
}
class NearestRider implements RiderAllocator {
    public Rider allocate(Order o) { return RiderPool.nearestFreeTo(o.pickup()); }   // helper assumed
}

interface CityFactory {
    FeeCalculator createFeeCalculator();
    RiderAllocator createAllocator();
}
class DhakaFactory implements CityFactory {
    public FeeCalculator createFeeCalculator() { return new DhakaFee(); }
    public RiderAllocator createAllocator()    { return new NearestRider(); }
}
// ChattogramFactory: new ChattogramFee() (30 + 12 * km) and new LeastBusyRider()

class OrderService {                                   // knows only the abstract types
    private final CityFactory factory;
    OrderService(CityFactory factory) { this.factory = factory; }
    void placeOrder(Order o) {
        FeeCalculator calc  = factory.createFeeCalculator();
        RiderAllocator alloc = factory.createAllocator();
        double fee = calc.fee(o.distanceKm());
        Rider rider = alloc.allocate(o);
        // ... charge the customer, notify the rider
    }
}
// startup:  new OrderService(new DhakaFactory())   /   new OrderService(new ChattogramFactory())"""))
    s += mark("(i) pattern name 1, reasons 2.", "(ii) factory interface with both create methods 1.5, abstract products 1, concrete factories 1, concrete products 1.5, client depends only on abstract types 1.",
              "(iii) abstract products 1.5, concrete Dhaka products 1.5, factory interface + DhakaFactory 1.5, OrderService via factory 1.5.")

    s.append(H("(b) SRP, OCP and DIP", "10"))
    s.append(P("<b>(i) Violations [4].</b>", "lab"))
    s += bullets(["<b>SRP</b> — <font face='Mono'>generate()</font> adds up sales, formats the text <i>and</i> saves to a database: three reasons to change.",
                  "<b>OCP</b> — the <font face='Mono'>if / else if</font> chain on <font face='Mono'>format</font>: every new format means editing this tested method.",
                  "<b>DIP / program to an interface</b> — <font face='Mono'>new MySqlDatabase()</font> makes the high-level report logic depend on a concrete low-level class; the"
                  " database cannot be swapped or faked in a test."])
    s.append(P("<b>(ii) Refactored design [6].</b> Encapsulate what varies (the format) behind an interface, and inject the abstractions."))
    s.append(code("""interface Formatter { String format(double total); }
class PdfFormatter implements Formatter { public String format(double t) { return "PDF:" + t; } }
class CsvFormatter implements Formatter { public String format(double t) { return "CSV," + t; } }
class TxtFormatter implements Formatter { public String format(double t) { return "TXT " + t; } }

interface Database { void save(String text); }
class MySqlDatabase implements Database { public void save(String text) { /* INSERT ... */ } }

class ReportService {
    private final Formatter formatter;
    private final Database db;
    ReportService(Formatter formatter, Database db) { this.formatter = formatter; this.db = db; }

    String generate(List<Sale> sales) {
        double total = 0;
        for (Sale s : sales) total += s.amount;     // could move to a TotalCalculator for strict SRP
        String out = formatter.format(total);
        db.save(out);
        return out;
    }
}"""))
    s += mark("(i) each violation with the offending line 1.3 (three of them = 4).", "(ii) Formatter hierarchy 2, Database interface 1.5, constructor injection 1.5, tidy generate() 1.")

    s.append(H("(c) Thread-safe lazy Singleton", "10"))
    s.append(code("""public final class ConfigManager {
    private static volatile ConfigManager instance;          // volatile is required for double-checked locking
    private final Properties props = new Properties();

    private ConfigManager() { load(); }                      // private constructor: nobody else can call new
    private void load() { /* read the settings file into props, once */ }

    public static ConfigManager getInstance() {
        if (instance == null) {                              // 1st check: no lock on the fast path
            synchronized (ConfigManager.class) {
                if (instance == null)                        // 2nd check: only one thread gets past this
                    instance = new ConfigManager();
            }
        }
        return instance;
    }
    public String get(String key) { return props.getProperty(key); }
}"""))
    s += bullets(["<b>Why the naive version fails [3].</b> With <font face='Mono'>if (instance == null) instance = new ...</font> two threads can both see <i>null</i> before either assigns,"
                  " so two objects are built and the settings load twice; callers then hold different copies. Synchronising the whole <font face='Mono'>getInstance()</font> is correct but makes every call"
                  " pay for a lock; double-checked locking removes that cost, but needs <font face='Mono'>volatile</font> so another thread can never see a half-constructed object"
                  " (instruction reordering). Alternatives: eager initialisation, the initialisation-on-demand holder idiom, or a one-element <font face='Mono'>enum</font>.",
                  "<b>Poor choices for a Singleton [2], any two:</b> it is hidden global state and makes unit tests hard (cannot be replaced by a mock); it couples every user to one concrete class;"
                  " it breaks if you later need one instance per tenant/user; it mixes the class's job with controlling its own lifecycle (SRP); it needs extra care in a multi-threaded or"
                  " multi-class-loader setting."])
    s += mark("code: private constructor 1, static volatile field 1, lazy getInstance 1, synchronised double check 1.5, use/loading 0.5; explanation 3; two drawbacks 2.")

    # ---------------------------------------------------------------- Q2
    s.append(P("Question 2", "q"))
    s.append(H("(a) Library class diagram", "20"))
    s.append(F.d_library())
    s += bullets(["Member is <i>abstract</i> (italic) because “a plain Member is never created”; Student and Faculty are its subclasses (generalisation, hollow triangle at Member).",
                  "Library has <b>aggregation</b> (hollow diamond) to Book and to Member: both exist independently. Book–Copy and Loan–Fine are <b>composition</b> (filled diamond): the part"
                  " cannot exist without the whole (“cannot exist without its Book”, “deleted with it”).",
                  "<b>Association class:</b> Loan hangs from the Member–Copy association by a dashed line, so each Member–Copy link carries issueDate, dueDate and returnDate."
                  " Multiplicities: a Member has 0..5 Copies; a Copy is on 0..1 Member at a time.",
                  "Loan–Librarian: many loans, exactly one issuing Librarian. Loan–Fine: composition, 1 to 0..1."])
    s += mark("classes and attributes 4, operations 1, generalisation with abstract Member 3, aggregation 2, the two compositions 3, association class drawn correctly 3, other associations 2, multiplicities 2.")

    s.append(H("(b) Order state diagram", "15"))
    s.append(F.d_order_state())
    s += bullets(["The retry is a <b>self-transition</b> on Placed with guard <font face='Mono'>[attempts &lt; 3]</font> and action <font face='Mono'>attempts++</font>; the same event with"
                  " the opposite guard <font face='Mono'>[attempts == 3]</font> leaves for Cancelled. Both guards are mutually exclusive, so the choice is deterministic.",
                  "Cancellation exists only from Placed and Paid; Shipped has no cancel transition. A Paid cancellation carries the action <font face='Mono'>refund()</font>."])
    s.append(P("<b>(ii) Event kinds [4].</b>", "lab"))
    s.append(table([["Trigger", "Kind", "Why"],
                    ["pay", "call event", "an operation is invoked on the Order object by the customer"],
                    ["payFail", "signal event", "an asynchronous message sent to the Order by the payment gateway"],
                    ["after(7 days)", "time event", "fires when the stated time has elapsed since the state was entered"],
                    ["when(attempts = 3)", "change event", "fires when a Boolean condition becomes true"]], [3.2 * cm, 2.6 * cm, w1 - 5.8 * cm]))
    s.append(P("A <b>guard</b> is a condition in square brackets that is evaluated <i>when</i> an event occurs and decides whether the transition may fire; a <b>change event</b> is itself the"
               " trigger and fires the moment the condition becomes true. (Pay as signal and payFail as call are also accepted if you justify them.)"))
    s += mark("(i) initial and final states 2, all states 3, transitions with correct events 3, guards and actions 2, self-loop with counter 1; (ii) four kinds 3, guard vs change event 1.")

    # ---------------------------------------------------------------- Q3
    s.append(P("Question 3", "q"))
    s.append(H("(a) PayPoint use cases", "20"))
    s.append(F.d_usecase())
    s += bullets(["<b>Verify PIN</b> is a mandatory shared step, so the three use cases <b>«include»</b> it (arrow from the base use case to Verify PIN). <b>Send OTP Check</b> and"
                  " <b>Apply Promo Code</b> are optional behaviour, so they <b>«extend»</b> Send Money / Pay Bill (arrow from the extension to the base, with the extension condition on Send Money).",
                  "Customer and Agent specialise the actor <i>User</i> (hollow triangle). The Bank is an external <i>secondary actor</i> of Link Bank Account. Check Balance has no include, as the text says."])
    s.append(P("<b>(ii) Use case description — Send Money [8]</b>", "lab"))
    s.append(table([["Item", "Content"],
                    ["Name / actor", "Send Money — primary actor: Customer"],
                    ["Precondition", "The customer is registered, logged in to the app and the account is active."],
                    ["Main flow", "1. Customer chooses Send Money and enters receiver number and amount.<br/>2. System checks the receiver exists.<br/>3. System runs <i>Verify PIN</i> (included).<br/>"
                                  "4. If the amount is above 25,000 BDT the system runs <i>Send OTP Check</i> (extension).<br/>5. System checks that the balance covers the amount.<br/>"
                                  "6. System debits the sender and credits the receiver.<br/>7. System shows a confirmation and records the transaction."],
                    ["Alternate flows", "2a. Receiver not found: system shows an error and returns to step 1.<br/>3a. Wrong PIN (3 times): system blocks the transaction and the use case ends.<br/>"
                                        "4a. OTP wrong or expired: transfer cancelled, no money moves.<br/>5a. Balance too low: system shows “insufficient funds”; nothing is debited."],
                    ["Postcondition", "Success: sender balance reduced and receiver balance increased by the amount, transaction stored. Failure: all balances unchanged."]],
                   [3.0 * cm, w1 - 3.0 * cm]))
    s += mark("(i) actors and boundary 2, use cases 3, associations 2, actor generalisation 1, includes 2, extends with correct direction 2; (ii) header 2, main flow 3, two alternate flows 2, postcondition 1.")

    s.append(H("(b) Send Money interaction", "15"))
    s.append(P("<b>(i) Sequence diagram [10]</b>", "lab"))
    s.append(F.d_sequence())
    s.append(P("<b>(ii) Collaboration diagram, success path [5].</b> Same objects, drawn as a network of links; the numbers carry the order and the nesting (1.1 happens <i>inside</i> 1)."))
    s.append(F.d_collab())
    s += mark("(i) lifelines/objects 2, messages in the right order with names 3, return messages 1, activation bars 1, alt with both guards 3; (ii) objects and links 2, numbering 3.")

    # ---------------------------------------------------------------- Q4
    s.append(P("Question 4", "q"))
    s.append(H("(a) Fare: equivalence classes and BVA", "15"))
    s.append(P("<b>(i) Classes [3].</b>", "lab"))
    s.append(table([["Input", "Valid class", "Invalid classes"],
                    ["distance (km)", "V1: 1 ≤ d ≤ 50", "I1: d &lt; 1 &nbsp;&nbsp; I2: d &gt; 50"],
                    ["passengers", "V2: 1 ≤ p ≤ 6", "I3: p &lt; 1 &nbsp;&nbsp; I4: p &gt; 6"]], [3.0 * cm, 5.0 * cm, w1 - 8.0 * cm]))
    s.append(P("<b>(ii) ECT counts [4].</b> Each input has 3 classes. <b>Weak ECT</b> = the largest number of classes of any one input = <b>3</b> tests, chosen so every class of every input"
               " appears at least once: (25, 3) [V1,V2], (0, 0) [I1,I3], (60, 9) [I2,I4]. <b>Strong ECT</b> = product of class counts = 3 × 3 = <b>9</b> tests (every combination)."
               " Weak tests with two invalid inputs can <i>mask</i> a defect (one error message hides the other check); if you insist on one fault per test you need 1 valid + 4 invalid = 5 tests."))
    s.append(P("<b>(iii) BVA [8].</b> Boundary values: distance <b>0, 1, 2, 49, 50, 51</b>; passengers <b>0, 1, 2, 5, 6, 7</b>. Robust BVA (single fault: vary one input, hold the other at its nominal) gives"
               " 6n + 1 = <b>13</b> tests:"))
    s.append(table([["Vary distance (passengers = 3)", "Expected", "Vary passengers (distance = 25)", "Expected"],
                    ["(0, 3)", "error", "(25, 0)", "error"], ["(1, 3)", "valid", "(25, 1)", "valid"], ["(2, 3)", "valid", "(25, 2)", "valid"],
                    ["(49, 3)", "valid", "(25, 5)", "valid"], ["(50, 3)", "valid", "(25, 6)", "valid"], ["(51, 3)", "error", "(25, 7)", "error"],
                    ["nominal (25, 3)", "valid", "", ""]], [4.6 * cm, 2.4 * cm, 5.0 * cm, w1 - 12.0 * cm]))
    s += mark("(i) 3; (ii) counts 2 + weak set 2; (iii) values 3, 13 tests with nominals 4, expected results 1.")

    s.append(H("(b) White-box testing of process(n, k)", "20"))
    s.append(P("<b>(i) Control-flow graph [4].</b> Node labels are line numbers; the compound condition on line 4 is split into 4a (<font face='Mono'>i%2==0</font>) and 4b (<font face='Mono'>i&gt;k</font>),"
               " as instructed. The short-circuit <font face='Mono'>||</font> means 4b is reached only when 4a is false."))
    s.append(F.d_cfg())
    s.append(P("<b>(ii) Cyclomatic complexity [4].</b> Edges E = 13, nodes N = 10, predicate nodes P = 4 (3, 4a, 4b, 10), regions R = 5 (4 enclosed + the outside)."))
    s.append(table([["Method", "Working", "V(G)"], ["E − N + 2", "13 − 10 + 2", "5"], ["P + 1", "4 + 1", "5"], ["Regions", "4 enclosed + 1 outer", "5"]],
                   [4.0 * cm, 6.0 * cm, w1 - 10.0 * cm]))
    s.append(P("<b>(iii) Five independent basis paths [8].</b> One flip of a predicate from a baseline path gives each new path."))
    s.append(table([["#", "Path (line labels)", "Input (n, k)", "Return"],
                    ["P1", "2-3-10-12", "(0, any)", "0"],
                    ["P2", "2-3-4a-4b-5-8-3-10-12", "(1, 0)", "1"],
                    ["P3", "2-3-4a-4b-5-8-3-4a-5-8-3-10-12", "(2, 0)", "3"],
                    ["P4", "2-3-4a-4b-7-8-3-4a-5-8-3-4a-4b-7-8-3-10-12", "(3, 5)", "0"],
                    ["P5", "2-3-4a-4b-7-8-3-10-11-12", "(1, 5)", "0"]], [1.0 * cm, 9.0 * cm, 3.0 * cm, w1 - 13.0 * cm]))
    s.append(P("Check by hand: (3, 5): i=1 odd and 1≤5 → s=−1; i=2 even → s=1; i=3 odd → s=0; 0 is not &lt; 0, so 0. (1, 5): s=−1 so line 11 sets s=0. (2, 0): i=1 → 1&gt;0 so s=1; i=2 even → s=3.", "small"))
    s.append(P("<b>(iv) Coverage [4].</b> <b>Two</b> tests give 100 % branch coverage (one is not enough because line 10 must go both ways, which needs two runs): <b>T1 = (2, 0)</b> covers while T/F, 4a T (i=2) and F (i=1),"
               " 4b T (i=1), 10 F; <b>T2 = (1, 5)</b> covers 4b F (1&gt;5 is false) and 10 T. The same two tests also give <b>condition coverage</b>: i&lt;=n is true then false, i%2==0 true/false,"
               " i&gt;k true (T1) and false (T2), s&lt;0 false (T1) and true (T2). Note 4b is not evaluated for even i (short-circuit), which is why T1 needs the odd iteration i=1."))
    s += mark("(i) 4; (ii) three methods 3 + V(G) stated 1; (iii) five independent paths 5 + inputs and returns 3; (iv) two tests 2, branch table 1, condition coverage verdict 1.")

    # =================================================================== SECTION B
    s += [Spacer(1, 4), banner("SECTION B — model answers", GREEN)]

    # ---------------------------------------------------------------- Q5
    s.append(P("Question 5", "q"))
    s.append(H("(a) TalkNet plans: Decorator", "15"))
    s.append(P("<b>(i) Pattern [3].</b> <b>Decorator</b> — add responsibilities (extra cost and description) to an object <i>at run time</i>, in any combination, without subclassing. With inheritance every"
               " combination is its own class: 3 add-ons give 2³ = 8 plans (Basic + 7 non-empty combinations), a fourth add-on doubles that to 16, and a customer cannot add one later to an"
               " existing plan. With decorators there is one class per add-on."))
    s.append(P("<b>(ii) Class diagram [6].</b>", "lab"))
    s.append(F.d_decorator())
    s.append(P("<b>(iii) Code [6].</b>", "lab"))
    s.append(code("""interface Plan { int cost(); String description(); }

class BasicPlan implements Plan {
    public int cost()           { return 500; }
    public String description() { return "Basic"; }
}
abstract class PlanDecorator implements Plan {          // is-a Plan and has-a Plan
    protected final Plan plan;
    PlanDecorator(Plan plan) { this.plan = plan; }
    public int cost()           { return plan.cost(); }
    public String description() { return plan.description(); }
}
class VideoPack extends PlanDecorator {
    VideoPack(Plan p) { super(p); }
    public int cost()           { return plan.cost() + 150; }
    public String description() { return plan.description() + " + Video"; }
}
// SocialPack (+100, " + Social") and RoamingPack (+200, " + Roaming") have the same shape

public class Client {
    public static void main(String[] args) {
        Plan p = new VideoPack(new SocialPack(new BasicPlan()));
        System.out.println(p.description() + " = " + p.cost() + " BDT");   // Basic + Social + Video = 750 BDT
    }
}"""))
    s += mark("(i) pattern 1, explosion argument with the count 2; (ii) interface + concrete component 2, decorator holding a Plan 2, three concrete decorators 1, correct arrows 1; "
              "(iii) interface/component 1.5, decorator base 1.5, VideoPack 1.5, client wrapping order and 750 1.5.")

    s.append(H("(b) Flood station: Observer", "10"))
    s.append(P("<b>(i) Pattern and roles [3].</b> <b>Observer</b>. Subject = <font face='Mono'>FloodStation</font> (holds the list, notifies), Observer = the <font face='Mono'>Observer</font>"
               " interface with <font face='Mono'>update()</font>, ConcreteObservers = SMS gateway, dashboard, siren controller. The station depends only on the interface, so subscribers can be added or removed at run time."))
    s.append(F.d_observer())
    s.append(P("<b>(iii) Code [3].</b>", "lab"))
    s.append(code("""interface Observer { void update(FloodStation station); }

class FloodStation implements Subject {
    private final List<Observer> observers = new ArrayList<>();
    private double level;

    public void attach(Observer o) { observers.add(o); }
    public void detach(Observer o) { observers.remove(o); }
    public void notifyObservers() {
        for (Observer o : observers) o.update(this);      // pull model: observers call getLevel()
    }
    public void setLevel(double l) {
        if (l != level) { level = l; notifyObservers(); }   // notify only on a real change
    }
    public double getLevel() { return level; }
}"""))
    s += mark("(i) pattern 1, roles 2; (ii) interfaces and three observers 2, subject–observer association 1, realisations 1; (iii) attach/detach 1, notify loop 1, call on change 1.")

    s.append(H("(c) Adapter", "10"))
    s.append(code("""interface Printer { void print(Document d); }

class OldLaser {                                     // vendor class, cannot be changed
    void printText(String text, int copies) { /* ... */ }
}

class OldLaserAdapter implements Printer {           // OBJECT adapter
    private final OldLaser laser;                    // composition: the adapter holds the adaptee
    OldLaserAdapter(OldLaser laser) { this.laser = laser; }
    public void print(Document d) {
        laser.printText(d.getText(), 1);             // translate the Target call into the Adaptee call
    }
}"""))
    s += bullets(["<b>Class adapter:</b> <font face='Mono'>class OldLaserAdapter extends OldLaser implements Printer</font> — it <i>inherits</i> the adaptee instead of holding it.",
                  "<b>Why object adapters are usually preferred in Java [4]:</b> Java has single class inheritance, so a class adapter burns the only <font face='Mono'>extends</font> slot and works only if the target is an interface;"
                  " an object adapter can adapt <i>OldLaser and any of its subclasses</i> and can be handed a different instance at run time; it does not expose the adaptee's methods through the adapter;"
                  " and it follows “favour composition over inheritance”. The class adapter's one advantage is that it can override adaptee behaviour directly and has no extra object to forward through."])
    s += mark("code: interface 1, Target/Adaptee shown 1, composition field 1.5, constructor 1, delegating print with the translation 1.5; class adapter described 1; reasons 3.")

    # ---------------------------------------------------------------- Q6
    s.append(P("Question 6", "q"))
    s.append(H("(a) Group chat: Mediator", "15"))
    s.append(P("<b>(i) Pattern [2].</b> <b>Mediator.</b> Mediator = <font face='Mono'>ChatMediator</font>, ConcreteMediator = <font face='Mono'>ChatRoom</font>, Colleague = <font face='Mono'>User</font>."
               " Users no longer know each other: n² links become n links, and the rules (muting) live in one place."))
    s.append(P("<b>(ii) Class diagram [5].</b>", "lab"))
    s.append(F.d_mediator())
    s.append(P("<b>(iii) Code [8].</b>", "lab"))
    s.append(code("""interface ChatMediator {
    void register(User u);
    void send(String msg, User from);
}
class ChatRoom implements ChatMediator {
    private final List<User> users = new ArrayList<>();
    private final Set<User> muted = new HashSet<>();
    public void register(User u) { users.add(u); }
    public void mute(User u)     { muted.add(u); }
    public void send(String msg, User from) {
        if (muted.contains(from)) return;                       // the muting rule lives in the mediator
        for (User u : users)
            if (u != from) u.receive(from.getName() + ": " + msg);
    }
}
class User {
    private final String name;
    private final ChatMediator room;                           // the only reference a user has
    User(String name, ChatMediator room) { this.name = name; this.room = room; room.register(this); }
    String getName()          { return name; }
    void post(String msg)     { room.send(msg, this); }
    void receive(String msg)  { System.out.println(name + " got " + msg); }
}"""))
    s += mark("(i) 2; (ii) interface + concrete mediator 2, User with mediator reference 1, arrows 2; (iii) interface 1.5, ChatRoom with list 2, muting rule 2, User posting through the mediator 2.5.")

    s.append(H("(b) File explorer: Composite", "10"))
    s.append(F.d_composite())
    s.append(code("""interface FileSystemItem { String getName(); int getSize(); }

class File implements FileSystemItem {                          // leaf
    private final String name; private final int sizeKb;
    File(String name, int sizeKb) { this.name = name; this.sizeKb = sizeKb; }
    public String getName() { return name; }
    public int getSize()    { return sizeKb; }
}
class Folder implements FileSystemItem {                        // composite
    private final String name;
    private final List<FileSystemItem> children = new ArrayList<>();
    Folder(String name) { this.name = name; }
    public void add(FileSystemItem i)    { children.add(i); }
    public void remove(FileSystemItem i) { children.remove(i); }
    public String getName() { return name; }
    public int getSize() {
        int total = 0;
        for (FileSystemItem c : children) total += c.getSize();   // recursion: any depth, empty folder = 0
        return total;
    }
}"""))
    s += mark("pattern 1, diagram 3 (common interface, leaf, composite holding the interface type), code 6 (interface 1, leaf 1.5, composite and list 1.5, recursive getSize 2).")

    s.append(H("(c) Shapes and renderers: Bridge", "10"))
    s.append(P("<b>(i) With plain inheritance [3].</b> Every shape–renderer pair is a class: 2 × 2 = <b>4</b> concrete classes (VectorCircle, RasterCircle, VectorSquare, RasterSquare). After adding Triangle and"
               " GpuRenderer: 3 × 3 = <b>9</b> (5 more), and each further shape or renderer multiplies the count."))
    s.append(P("<b>(ii) Bridge [4 + 3].</b> Split the two dimensions into separate hierarchies joined by a reference (the bridge): <font face='Mono'>Shape</font> holds a <font face='Mono'>Renderer</font>."))
    s.append(F.d_bridge())
    s.append(P("Classes needed: shapes + renderers = 2 + 2 = <b>4</b>; after the additions 3 + 3 = <b>6</b>, i.e. only <b>2 new classes</b> (Triangle and GpuRenderer) instead of 5. The count grows as m + n, not m × n."))
    s += mark("(i) 4 and 9 with the formula 3; (ii) abstraction and implementor hierarchies 2, the bridge reference 2, counts 6 and 2 new classes 3.")

    # ---------------------------------------------------------------- Q7
    s.append(P("Question 7", "q"))
    s.append(H("(a) Process model for the results portal", "15"))
    s.append(P("<b>Recommended: the Incremental model</b>, with a small early risk spike for the legacy database [7]."))
    s += bullets(["The requirements are stable and understood, so the work can be split into increments up front; each increment is a small waterfall (communication, planning, modelling, construction, deployment).",
                  "The two delivery dates map directly onto increments: increment 1 (core results processing for one board) is a working <b>pilot by month 4</b>, later increments add boards and finish by month 8.",
                  "Early increments give real feedback and a fallback if the project slips (the earlier boards already work), which suits a <b>fixed deadline</b>.",
                  "The legacy-database risk is attacked first: a vertical slice or spike in month 1 proves the integration before the bulk of the work is committed."])
    s.append(F.d_incremental())
    s.append(P("<b>Why two others are weaker [6].</b>", "lab"))
    s += bullets(["<b>Waterfall</b> (also the simplest fit for stable requirements) delivers nothing working until month 8, so the one-board-by-month-4 demand cannot be met and the database integration problem would be discovered at the very end, when it is most expensive.",
                  "<b>Prototyping</b> is for <i>unclear</i> requirements; here they are clear, and a throw-away prototype costs time inside a fixed 8-month contract.",
                  "<b>Spiral</b> is built for large, evolving, high-risk projects with heavy risk analysis each loop; the overhead is not justified for stable requirements, and the cost/deadline is fixed. Its risk-first idea is borrowed by the spike."])
    s.append(P("Another model (e.g. Scrum, or RAD) is accepted if it is justified against the same scenario facts: stable requirements, fixed deadline, two staged releases, one risky integration.", "small"))
    s += mark("choice 1 + justification 6 (staged delivery 2, fixed deadline and stable requirements 2, risk handling 2); two rejected models 3 each; process flow 2.")

    s.append(H("(b) Scrum", "10"))
    s.append(table([["Part", "Answer"],
                    ["Roles [3]", "<b>Product Owner</b> — owns and orders the product backlog, speaks for the stakeholders. <b>Scrum Master</b> — coaches the team, removes impediments, protects the process."
                                  " <b>Development team</b> — small, self-organising, cross-functional; builds the increment."],
                    ["Events in order [4]", "1. <b>Sprint</b> (time-box of 1–4 weeks that contains all the rest). 2. <b>Sprint planning</b> — choose backlog items and plan the work (what and how). 3. <b>Daily scrum</b> — 15-minute"
                                            " sync every day. 4. <b>Sprint review</b> — demonstrate the finished increment to stakeholders and adapt the backlog. 5. <b>Sprint retrospective</b> — the team improves its own way of working."],
                    ["Backlogs [3]", "<b>Product backlog</b>: the ordered list of everything the product may need, owned by the Product Owner, changes continuously. <b>Sprint backlog</b>: the items chosen for this sprint plus the plan to deliver them,"
                                     " owned by the team, and fixed in scope for the sprint. The product backlog feeds the sprint backlog."]],
                   [3.0 * cm, w1 - 3.0 * cm]))
    s += mark("roles 3 (one each), events 4 (all five in order), backlog difference 3.")

    s.append(H("(c) Kanban board", "10"))
    s.append(P("<b>(i) Board [3]</b>", "lab"))
    s.append(table([["To Do", "Develop (WIP 3)", "Test (WIP 2)", "Done"],
                    ["D8, D9, D10,<br/>D11, D12, D13 (6)", "D5, D6, <b>D7 (finished)</b> &nbsp;3/3", "D3, D4 &nbsp;2/2", "D1, D2"]], [fw / 4] * 4))
    s.append(P("<b>(ii) What now [4].</b> She <b>may not</b> pull a new item: Develop is at its limit (3/3), and D7 cannot move on because Test is also full (2/2). The Test column is the <b>bottleneck</b>."
               " Kanban is a <i>pull</i> system governed by WIP limits: stop starting, start finishing. She should help the downstream work (test or review D3/D4), let one of them move to Done, move D7 into Test, and only then"
               " pull the next To Do item when Develop drops below 3. The limit prevents work piling up in front of the slow stage and makes the problem visible."))
    s.append(P("<b>(iii) Times [3].</b> Lead time = delivered − requested = day 9 − day 1 = <b>8 days</b>. Cycle time = delivered − work started = day 9 − day 4 = <b>5 days</b>."))
    s += mark("board with WIP limits 3; refusal with the reason 2 + corrective action 2; lead time 1.5, cycle time 1.5.")

    # ---------------------------------------------------------------- Q8
    s.append(P("Question 8", "q"))
    s.append(H("(a) Invoice: smells and refactoring", "15"))
    s.append(P("<b>(i) Four smells [6].</b>", "lab"))
    s.append(table([["Smell", "Evidence", "Refactoring"],
                    ["Switch statements / conditional chains", "if/else ladders on <font face='Mono'>customerType</font> and <font face='Mono'>country</font>", "Replace Type Code with enum/class carrying the rate; Replace Conditional with Polymorphism"],
                    ["Long method", "<font face='Mono'>total()</font> does discount, tax and bulk rebate in one block", "Extract Method (applyDiscount, applyTax, applyBulkRebate)"],
                    ["Magic numbers / primitive obsession", "0.15, 0.10, 0.02, 0.18, 0.25, 50, 100 and type codes held in Strings", "Replace Magic Number with Symbolic Constant; enums for type codes"],
                    ["Duplicate code", "the same <font face='Mono'>t = t ± t * rate</font> arithmetic repeated six times", "Extract Method / pass the rate as a parameter"],
                    ["(Also accepted) Divergent change / large class", "pricing rules and printing live in one class", "Extract Class (InvoicePrinter)"]],
                   [3.6 * cm, 6.0 * cm, w1 - 9.6 * cm]))
    s.append(P("<b>(ii) Refactored code [9].</b> Behaviour is unchanged: discount first, then tax, then the bulk rebate.", "body"))
    s.append(code("""enum CustomerType {
    GOLD(0.15), SILVER(0.10), REGULAR(0.02);
    private final double discountRate;
    CustomerType(double r) { discountRate = r; }
    double discountRate() { return discountRate; }
}
enum Country {
    BD(0.15), IN(0.18), OTHER(0.25);
    private final double taxRate;
    Country(double r) { taxRate = r; }
    double taxRate() { return taxRate; }
}
class Invoice {
    private static final int    BULK_ITEMS  = 50;
    private static final double BULK_REBATE = 100;
    private final CustomerType customerType;
    private final Country country;
    private final double amount;
    private final int items;
    Invoice(CustomerType t, Country c, double amount, int items) {
        this.customerType = t; this.country = c; this.amount = amount; this.items = items;
    }
    double total() {
        return applyBulkRebate(applyTax(applyDiscount(amount)));
    }
    private double applyDiscount(double t)   { return t - t * customerType.discountRate(); }
    private double applyTax(double t)        { return t + t * country.taxRate(); }
    private double applyBulkRebate(double t) { return items > BULK_ITEMS ? t - BULK_REBATE : t; }
    CustomerType getCustomerType() { return customerType; }
    Country getCountry()           { return country; }
}
class InvoicePrinter {                                           // Extract Class
    void print(Invoice inv) {
        System.out.println("Customer: " + inv.getCustomerType() + ", " + inv.getCountry());
        System.out.println("Total: " + inv.total());
    }
}"""))
    s.append(P("If the customer types later need different <i>rules</i> (not just a different number), use a <font face='Mono'>DiscountPolicy</font> interface with one class per type (Strategy), which is the full "
               "Replace Conditional with Polymorphism.", "small"))
    s += mark("(i) four smells with evidence 1.5 each; (ii) enums or polymorphism 3, Extract Method 3, constants 1.5, Extract Class or equivalent 1.5; the refactoring must be named for each smell.")

    s.append(H("(b) JUnit test class", "10"))
    s.append(code("""import org.junit.*;
import static org.junit.Assert.*;

public class AccountTest {
    private Account acc;

    @Before
    public void setUp() { acc = new Account(1000); }               // fixture: a fresh account before every test

    @Test
    public void withdrawReducesBalance() throws Exception {
        acc.withdraw(300);
        assertEquals(700.0, acc.getBalance(), 0.001);              // delta needed when comparing doubles
    }
    @Test
    public void withdrawExactBalanceLeavesZero() throws Exception { // boundary: amt == balance is allowed
        acc.withdraw(1000);
        assertEquals(0.0, acc.getBalance(), 0.001);
    }
    @Test(expected = InsufficientFundsException.class)
    public void withdrawMoreThanBalanceFails() throws Exception { acc.withdraw(1000.01); }

    @Test(expected = IllegalArgumentException.class)
    public void withdrawZeroFails() throws Exception { acc.withdraw(0); }

    @Test(expected = IllegalArgumentException.class)
    public void withdrawNegativeFails() throws Exception { acc.withdraw(-5); }

    @Test
    public void failedWithdrawalKeepsBalance() {                   // state unchanged after the exception
        try { acc.withdraw(5000); fail("expected InsufficientFundsException"); }
        catch (InsufficientFundsException e) { assertEquals(1000.0, acc.getBalance(), 0.001); }
    }
    @After
    public void tearDown() { acc = null; }
}"""))
    s += mark("@Before fixture 2, normal withdrawal 2, exact-balance boundary 2, three failure cases with expected= or try/fail 3, delta for doubles 1. A test that asserts the checked exception without declaring <font face='Mono'>throws</font> will not compile — take a mark off.")

    s.append(H("(c) Ethics and requirements", "10"))
    s.append(P("<b>(i) Principles [3] and action [3].</b>", "lab"))
    s.append(table([["Principle (ACM / IEEE-CS)", "How it is at stake"],
                    ["1. <b>Public</b>", "Act consistently with the public interest: users' privacy is being violated against their explicit choice; the engineer must not approve software that diminishes privacy and must disclose a known danger to the public."],
                    ["3. <b>Product</b>", "Ensure the product meets the highest professional standards: the “Do not share” switch is a specified behaviour, and software that ignores it fails its own requirement."],
                    ["2. <b>Client and Employer</b>", "Act in the employer's best interest <i>consistently with the public interest</i>: hiding a privacy defect exposes the company to legal and reputational damage, so silence is not in its real interest."],
                    ["(also) 4. <b>Judgment</b>", "Maintain independent professional judgement; do not let commercial pressure override it."]], [4.2 * cm, w1 - 4.2 * cm]))
    s += bullets(["<b>Rahim's steps:</b> 1) confirm and document the evidence (reproducible steps, logs). 2) Report it in writing to the product manager. 3) If ignored, escalate inside the company (engineering head, privacy or legal officer)"
                  " and refuse to approve the release until the switch is honoured; propose a quick fix. 4) Only if the company still refuses and the harm continues, report to the proper external authority (data-protection regulator),"
                  " limiting disclosure to what is necessary. 5) Keep a record of every step."])
    s.append(P("<b>(ii) Requirements [4].</b> Both are <b>non-functional</b> requirements and, as written, untestable."))
    s.append(table([["Vague", "Kind", "Verifiable version"],
                    ["The system should be fast", "performance", "95 % of search requests shall return results within 2 seconds with 500 concurrent users."],
                    ["The app must be user-friendly", "usability", "A first-time user shall register without help within 3 minutes; at least 9 of 10 test users must succeed."]],
                   [4.0 * cm, 2.4 * cm, w1 - 6.4 * cm]))
    s += mark("principles 3 (1 each, with the link to the case), steps 3; two rewrites 1.5 each with a number and a condition, kind of requirement 0.5 each.")

    s += [Spacer(1, 10), P("— End of model answers —", "sub")]
    return s
