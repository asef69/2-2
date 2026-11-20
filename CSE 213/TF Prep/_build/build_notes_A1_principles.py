"""Anindya 1 — Design Principles + Basics of Design Patterns (Lec 1, Lec 2) → Lessons 1–4."""
import os
import sys, os as _o; sys.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
from common import new, exam_map, src_note, AN

L1 = os.path.join(AN, "Lec 1 - Design Principle.pdf")
n = new("Anindya", "Design Principles (SOLID) & Basics of Design Patterns",
        "CSE213_Anindya_Design_Principles_Notes.docx")
n.front_matter([
    ("Exam Map — What the TF Papers Ask", "principle and pattern-basics questions"),
    ("Lesson 1 — Encapsulate What Varies, Program to an Interface, Composition", "Lec 1 sl. 2–9; cohesion & coupling"),
    ("Lesson 2 — SRP and the Open/Closed Principle", "Lec 1 sl. 10–17; OCP rewrite"),
    ("Lesson 3 — LSP, ISP and DIP", "Lec 1 sl. 18–31; ISP bad example"),
    ("Lesson 4 — What a Design Pattern Is", "Lec 2 sl. 1–10; GoF catalogue, essential elements"),
    ("Quick Notes — Design Principles", "revision + key diagrams"),
], source_note=src_note("Lessons 1–3: 'Lec 1 - Design Principle.pdf' (32 slides). Lesson 4: 'Lec 2 - Basics of Design Pattern.pdf' (10 slides)."))

exam_map(n, "A1", "Small but steady: ISP (2022-23 Q2(c), 2012-13 Q4(b)), OCP rewrite (2016-17 Q8(d)), "
         "cohesion/coupling (2018-19, 2017-18), pattern basics (2014-15, 2011-12). Learn one clean example per SOLID "
         "letter — the ISP and OCP examples below are exam-ready. Every pattern answer in the other note files is "
         "also judged by these principles, so read this file first.")

# ---------------------------------------------------------------- L1
n.lesson("Lesson 1 — Encapsulate What Varies, Program to an Interface, Composition", "Slides 2–9 (Lec 1 - Design Principle)")
n.h2("1. Encapsulate what varies (sl. 2–5)")
n.p("Find the parts of the program that change, and separate them from the parts that stay the same. The change is then "
    "localised: you edit one method or one class, not many.")
n.h3("Method level (sl. 2–3)")
n.code("""// BEFORE: tax rules are mixed into the total computation
double getOrderTotal(Order order) {
    double total = 0;
    for (Item item : order.items) total += item.price * item.quantity;
    if (order.country.equals("US")) total += total * 0.07;   // US sales tax
    else if (order.country.equals("EU")) total += total * 0.20; // EU VAT
    return total;
}
// AFTER: the part that varies (tax rate) gets its own method
double getOrderTotal(Order order) {
    double total = 0;
    for (Item item : order.items) total += item.price * item.quantity;
    total += total * getTaxRate(order.country);
    return total;
}
double getTaxRate(String country) {
    if (country.equals("US")) return 0.07;
    if (country.equals("EU")) return 0.20;
    return 0;
}""")
n.h3("Class level (sl. 4–5)")
n.p("When the tax logic grows (state rules, product rules, Chinese tax …), move it out of Order into its own class "
    "TaxCalculator(getTaxRate(country, state, product), getUSTax, getEUTax, getChineseTax). Order now delegates; it has one job.")
n.h2("2. Program to an interface, not an implementation (sl. 6)")
n.p("Depend on abstractions. Example: Cat.eat(Sausage) works only for sausages. Introduce interface Food (getNutrition()) "
    "and write Cat.eat(Food). Any new food can be added without touching Cat.")
n.p("The slide warns: right after this change you feel no benefit and the code is more complex. Do it only where you expect "
    "an extension point.")
n.h2("3. Favour composition over inheritance (sl. 7–9)")
n.bullets([
    "**Diamond problem (sl. 7):** if ClassA and ClassB both implement doSomething() and ClassC extends both, the compiler "
    "cannot decide which one ClassC inherits. Java therefore forbids multiple class inheritance.",
    "**Tight coupling (sl. 8):** Company creates Designer, Programmer, Tester directly — Company depends on every concrete "
    "employee class, so a new kind of company or employee forces edits in Company.",
    "**Fix (sl. 9):** abstract Company with abstract getEmployees(); GameDevCompany and OutsourcingCompany override it; "
    "Employee is an interface with doWork(). Company now depends only on Employee. (This is the Factory Method idea — Lesson 5.)",
])
n.figure_from_pdf(L1, 9, "Figure 1.1 — Removing tight coupling: Company depends on the Employee interface (sl. 9)",
                  clip=(0, 0.12, 1, 0.95), width_cm=13)
n.h2("4. Cohesion and coupling (textbook — asked 2018-19, 2017-18)")
n.table(["", "Meaning", "Want"], [
    ["Cohesion", "How strongly the responsibilities inside one module/class belong together", "High (tight) cohesion — one focused job"],
    ["Coupling", "How much one module depends on the internals of another", "Low (loose) coupling — talk through narrow interfaces"],
], widths_cm=[2.6, 8.6, 6.0])
n.callout("answer", "Tight cohesion means each class does one well-defined job (SRP); loose coupling means classes interact "
          "only through abstract interfaces and know little about each other (DIP). Together they make a design easy to "
          "understand, test and change: a change stays inside one cohesive class, and because coupling is low it does not "
          "ripple into others. Example: Order with an embedded tax algorithm has low cohesion; moving tax to TaxCalculator "
          "behind an interface raises cohesion and lowers coupling.")
n.h2("5. Subclassing vs delegation (2010-11 Q3(c))")
n.p("The two techniques in that question are **inheritance (subclassing)** and **delegation (object composition)**. "
    "Both fix the added behaviour at compile time. Composition/delegation should be preferred: it does not expose the "
    "parent's internals, avoids the diamond problem and deep hierarchies, and the delegate can be swapped at run time "
    "(this is how Strategy, Decorator and Bridge work).")
n.exam_approach([
    "Name the principle in one line (quote the slide wording).",
    "Show a 'before' with the smell (conditionals, concrete dependencies, fat class).",
    "Show the 'after' with the extracted method/class or interface.",
    "Finish with the benefit: what change is now local.",
])
n.practice("Lesson 1", "(a) Actual — 2017-18 Q7(c). (b) Actual — 2018-19 Q3(c). (c) Actual — 2010-11 Q3(c).", [
    "(a) What is tight cohesion and loose coupling? How does it influence software design? (8)",
    "(b) Discuss cohesion and coupling in brief in the context of software engineering. (8)",
    "(c) Extending a system by subclassing vs by copying operations and delegating to another class: name the two techniques. Should one get preferential treatment? (5)",
])
n.solution()
n.answer("(a)", "Use the EXAM-READY ANSWER in §4, then add an example: Company that creates Designer/Programmer/Tester "
         "itself is tightly coupled (sl. 8); after introducing Employee and getEmployees() it is loosely coupled (sl. 9). "
         "Influence: changes stay local, classes are reusable and testable in isolation, parallel development is easier.")
n.answer("(b)", "Cohesion = degree to which elements of a module belong together (aim high: functional cohesion). "
         "Coupling = degree of interdependence between modules (aim low: data coupling through parameters/interfaces, not "
         "content or common coupling). Good design = high cohesion + low coupling.")
n.answer("(c)", "Inheritance (subclassing) and delegation (composition). Prefer delegation: it keeps encapsulation, "
         "allows behaviour to be changed at run time, and avoids multiple-inheritance problems — 'favour composition over inheritance'.")

# ---------------------------------------------------------------- L2
n.lesson("Lesson 2 — SRP and the Open/Closed Principle", "Slides 10–17 (Lec 1 - Design Principle)")
n.h2("1. SOLID (sl. 10)")
n.table(["Letter", "Principle", "One-line rule"], [
    ["S", "Single Responsibility", "A class should have just one reason to change."],
    ["O", "Open/Closed", "Classes should be open for extension but closed for modification."],
    ["L", "Liskov Substitution", "A subclass object must work wherever the parent object works."],
    ["I", "Interface Segregation", "Clients shouldn't be forced to depend on methods they do not use."],
    ["D", "Dependency Inversion", "High- and low-level classes both depend on abstractions."],
], widths_cm=[1.5, 4.0, 11.7])
n.p("Cost (sl. 10): applying them blindly can make a program more complicated than it should be.")
n.h2("2. Single Responsibility Principle (sl. 11)")
n.p("Every class has a single responsibility, entirely encapsulated by the class. Example: Employee that also prints a "
    "time-sheet report has two reasons to change (employee data, report format). Move printing to TimeSheetReport.print(employee).")
n.p("Benefits listed on the slide: less fragile code, low coupling, high cohesion, changeability, maintainability, "
    "testability and easier debugging.")
n.h2("3. Open/Closed Principle (sl. 12–17)")
n.p("Once a class is complete, it is modified only to fix errors; new features come through new classes (sl. 13). "
    "Shipping example (sl. 12): Order.getShippingCost() with if (shipping == ground) … else if (air) … must be edited for every "
    "new method. Extract interface Shipping with Ground and Air implementations — a Strategy.")
n.h3("Worked example — AreaCalculator (sl. 14–17, C# on the slides, Java here)")
n.code("""// sl. 15 — every new shape forces an edit here (VIOLATES OCP)
double area(Object[] shapes) {
    double a = 0;
    for (Object s : shapes) {
        if (s instanceof Rectangle) { Rectangle r = (Rectangle) s; a += r.width * r.height; }
        else { Circle c = (Circle) s; a += c.radius * c.radius * Math.PI; }
    }
    return a;
}
// sl. 16–17 — closed for modification, open for extension
abstract class Shape { abstract double area(); }
class Rectangle extends Shape { double width, height; double area() { return width * height; } }
class Circle    extends Shape { double radius;        double area() { return Math.PI * radius * radius; } }
class Ellipse   extends Shape { double major, minor;  double area() { return Math.PI * major * minor; } } // added later
class AreaCalculator {
    double area(Shape[] shapes) { double a = 0; for (Shape s : shapes) a += s.area(); return a; }
}""")
n.callout("memorize", "OCP smell = a type code or instanceof chain that must be edited for every new type. Cure = "
          "polymorphism: push each branch into an overriding method (refactoring 'Replace Conditional with Polymorphism').")
n.practice("Lesson 2", "(a) Actual — 2016-17 Q8(d). (b) Constructed.", [
    "(a) Which class design principle does the following code violate? Rewrite the code to remove the violation.",
    "(b) State SRP. Show a class that violates it and fix it.",
])
n.code("""class GraphicEditor {
    public float getArea(Shape s) {
        if (s.m_type == 1) return s.width * s.width;
        else if (s.m_type == 2) return 3.1416 * s.r * s.r;
    }
}
class Shape { int m_type; }
class Rectangle extends Shape { int width; Rectangle(int width) { super.m_type = 1; this.width = width; } }
class Circle extends Shape { int r; Circle(int radius) { super.m_type = 1; this.r = radius; } }""")
n.solution()
n.answer("(a)", "It violates the **Open/Closed Principle**: GraphicEditor must be modified every time a new shape is added "
         "(another m_type branch), and it reaches into the fields of every subclass. (There is also a bug: Circle sets m_type = 1, "
         "so a circle's area is computed as a square.) Rewrite — each shape computes its own area:")
n.code("""abstract class Shape { abstract double getArea(); }
class Rectangle extends Shape {          // the paper's 'Rectangle' is a square: width * width
    private final int width;
    Rectangle(int width) { this.width = width; }
    double getArea() { return width * width; }
}
class Circle extends Shape {
    private final int r;
    Circle(int radius) { this.r = radius; }
    double getArea() { return 3.1416 * r * r; }
}
class GraphicEditor {                    // closed for modification
    double getArea(Shape s) { return s.getArea(); }
}
// new Triangle extends Shape { double getArea() {...} }  -> no change to GraphicEditor""")
n.answer("(b)", "SRP: a class should have only one reason to change. Violation: class Employee { calculatePay(); "
         "saveToDatabase(); printTimeSheetReport(); } — pay rules, storage and report format are three reasons. Fix: Employee "
         "(data + calculatePay), EmployeeRepository.save(e), TimeSheetReport.print(e).")

# ---------------------------------------------------------------- L3
n.lesson("Lesson 3 — LSP, ISP and DIP", "Slides 18–31 (Lec 1 - Design Principle)")
n.h2("1. Liskov Substitution Principle (sl. 18–20)")
n.bullets([
    "You must be able to pass a subclass object wherever a parent object is expected without breaking the client.",
    "When overriding, extend the parent's behaviour; do not replace it with something different.",
    "Violation (sl. 19): ReadOnlyDocument extends Document and overrides save() to throw an exception. Project.saveAll() "
    "must now check the type — the subclass is not substitutable.",
    "Fix (sl. 20): Document has only open(); WritableDocument extends Document and adds save(). Project keeps allDocs and "
    "writableDocs, and saves only writable ones.",
])
n.figure_from_pdf(L1, 20, "Figure 3.1 — LSP fix: only WritableDocument has save() (sl. 20)", clip=(0, 0.1, 1, 0.95), width_cm=12)
n.h2("2. Interface Segregation Principle (sl. 21–22)")
n.p("Clients shouldn't be forced to depend on methods they do not use. Make interfaces narrow.")
n.p("Example: a fat CloudProvider interface (storeFile, getFile, createServer, listServers, getCDNAddress). Amazon can "
    "implement all, but a Dropbox adapter must leave hosting/CDN methods empty or throwing. Split into CloudHostingProvider, "
    "CDNProvider and CloudStorageProvider; Amazon implements all three, Dropbox only CloudStorageProvider.")
n.figure_from_pdf(L1, 22, "Figure 3.2 — ISP: the fat interface split into three (sl. 22)", clip=(0, 0.1, 1, 0.95), width_cm=12)
n.h2("3. Dependency Inversion Principle (sl. 23–31)")
n.bullets([
    "High-level classes shouldn't depend on low-level classes; both depend on abstractions.",
    "Abstractions shouldn't depend on details; details depend on abstractions.",
    "sl. 24–25: BudgetReport → MySQLDatabase is inverted to BudgetReport → «interface» Database ← MySQL, MongoDB.",
    "How it works (sl. 26): the high-level module defines the interface it needs; low-level modules implement it.",
])
n.h3("Worked example — the power switch (sl. 27–31)")
n.code("""// Without DIP: ElectricPowerSwitch can only switch a LightBulb
public class ElectricPowerSwitch { public LightBulb lightBulb; ... lightBulb.turnOn(); ... }

// With DIP
public interface Switch     { boolean isOn(); void press(); }
public interface Switchable { void turnOn(); void turnOff(); }
public class ElectricPowerSwitch implements Switch {
    public Switchable client; public boolean on;
    public ElectricPowerSwitch(Switchable client) { this.client = client; this.on = false; }
    public boolean isOn() { return on; }
    public void press() {
        if (isOn()) { client.turnOff(); on = false; } else { client.turnOn(); on = true; }
    }
}
public class Fan implements Switchable { public void turnOn()  { System.out.println("Fan: Fan turned on..."); }
                                          public void turnOff() { System.out.println("Fan: Fan turned off..."); } }
public class LightBulb implements Switchable { /* same with 'Bulb' messages */ }""")
n.callout("trap", "DIP is not the same as 'dependency injection'. Injection (passing the Switchable in the constructor) is "
          "just a technique; the principle is that both sides depend on the Switchable abstraction.")
n.practice("Lesson 3", "(a) Actual — 2022-23 Q2(c). (b) Actual — 2012-13 Q4(b). (c) Constructed.", [
    "(a) Give an example of the Interface Segregation Principle. (8)",
    "(b) What is the primary motivation behind ISP? Explain ISP with a suitable 'bad example'. (14⅔)",
    "(c) Show an LSP violation with Rectangle/Square and fix it.",
])
n.solution()
n.answer("(a)/(b)", "Motivation: a fat interface couples every client to every method; implementers are forced to write "
         "dummy methods, and a change to one method forces recompiling/retesting clients that never use it. Bad example:")
n.code("""interface Worker { void work(); void eat(); void attendMeeting(); }
class Robot implements Worker {
    public void work() { ... }
    public void eat() { throw new UnsupportedOperationException(); }        // forced, meaningless
    public void attendMeeting() { throw new UnsupportedOperationException(); }
}
// ISP: split by client need
interface Workable  { void work(); }
interface Eatable   { void eat(); }
interface Meetable  { void attendMeeting(); }
class Human implements Workable, Eatable, Meetable { ... }
class Robot implements Workable { public void work() { ... } }""")
n.p("The CloudProvider/Dropbox example of sl. 21–22 is an equally good answer.")
n.answer("(c)", "Square extends Rectangle and setWidth() also sets height. A client that does r.setWidth(5); r.setHeight(4); "
         "expects area 20 but gets 16 → Square is not substitutable. Fix: make Rectangle and Square siblings under "
         "abstract Shape { double area(); } with no setters that break invariants.")

# ---------------------------------------------------------------- L4
n.lesson("Lesson 4 — What a Design Pattern Is", "Slides 1–10 (Lec 2 - Basics of Design Pattern)")
n.h2("1. Definition (sl. 2)")
n.bullets([
    "A standard solution to a common programming problem — a design structure that achieves a particular purpose.",
    "A description or template of how to solve a problem, usable in many situations.",
    "A technique for flexible/efficient code: reduces coupling and memory overhead.",
    "Shorthand for describing a design (a vocabulary).",
])
n.h2("2. The Gang of Four catalogue (sl. 3–6)")
n.table(["Category", "Concern", "Patterns (23)"], [
    ["Creational (5)", "How objects are instantiated", "Factory Method, Abstract Factory, Builder, Prototype, Singleton"],
    ["Structural (6 in syllabus)", "How objects/classes are combined into larger structures", "Adapter, Bridge, Composite, Decorator, Flyweight, Proxy"],
    ["Behavioral (8 in syllabus)", "How objects communicate and share responsibilities", "Template Method, Iterator, Mediator, Memento, Observer, State, Strategy, Visitor"],
], widths_cm=[3.0, 5.4, 8.8])
n.h2("3. Essential elements of a pattern (sl. 7)")
n.table(["Element", "What it states"], [
    ["Intent (name)", "Design goal of the pattern; the name gives a shared vocabulary"],
    ["Problem", "When to apply it: the problem and its context"],
    ["Solution", "Elements of the design, their relationships, responsibilities and collaborations (a template, not code)"],
    ["Consequences", "Benefits and trade-offs of applying it"],
], widths_cm=[3.4, 13.8])
n.h2("4. Why patterns are needed (sl. 8–10)")
n.p("Requirements always change: users' view changes after talking to developers; developers' view of the domain changes as "
    "they learn it; the environment changes. Design should accommodate change, and patterns give code that absorbs change easily.")
n.p("Reasons to study (sl. 10): reuse proven solutions; common terminology; higher-level thinking; decide whether a design is "
    "right, not just working; individual and team learning; modifiability; better alternatives even without the pattern; "
    "alternatives to large inheritance hierarchies.")
n.practice("Lesson 4", "(a) Actual — 2011-12 Q4(c). (b) Actual — 2014-15 Q6(a).", [
    "(a) What are the four essential elements of a design pattern? Discuss briefly. (8)",
    "(b) What is the difference between structural and behavioral patterns? Give criteria for classifying a new pattern, explaining why current patterns are classified as they are. (10)",
])
n.solution()
n.answer("(a)", "Name/intent, problem, solution, consequences — table in §3, one sentence each with Observer as the example "
         "(problem: dependents must be updated on change; solution: Subject keeps a list of Observer interfaces and calls update(); "
         "consequence: loose coupling, but unexpected update cascades).")
n.answer("(b)", "Structural patterns are about **composition** — how classes and objects are assembled into larger structures "
         "while staying flexible (Adapter wraps to change an interface, Composite builds trees, Decorator wraps to add "
         "responsibilities). Behavioral patterns are about **interaction** — algorithms, control flow and assignment of "
         "responsibility between objects (Observer: who notifies whom; Strategy: which algorithm runs; Mediator: who talks to whom).")
n.p("Criteria for a new pattern: (1) If its main purpose is to define the static shape of a structure — which object contains, "
    "wraps or refers to which, so that a larger object is formed — it is structural. (2) If its main purpose is to distribute "
    "a run-time responsibility or communication protocol among objects — message flow, choice of algorithm, state changes — "
    "it is behavioral. (3) If it is mainly about creating objects, it is creational. Decorator is structural because its essence "
    "is a wrapping structure with the same interface; Strategy is behavioral because its essence is selecting an algorithm at run time, "
    "even though both use composition.")

n.quick_notes("Quick Notes — Design Principles", "Revision points for Lessons 1–4.", [
    ("L1 · Encapsulate, interfaces, composition", [
        "Encapsulate what varies: getTaxRate() method → TaxCalculator class.",
        "Program to an interface: Cat.eat(Food), not eat(Sausage).",
        "Diamond problem → Java bans multiple class inheritance. Favour composition/delegation.",
        "High cohesion + low coupling; subclassing vs delegation → prefer delegation.",
    ]),
    ("L2 · SRP, OCP", [
        "SRP: one reason to change (TimeSheetReport out of Employee).",
        "OCP: open for extension, closed for modification. Type-code if-chains → abstract method per subclass.",
        "2016-17 Q8(d): GraphicEditor violates OCP; each Shape gets getArea().",
    ]),
    ("L3 · LSP, ISP, DIP", [
        "LSP: subclass substitutable; ReadOnlyDocument.save() throwing = violation → WritableDocument.",
        "ISP: no fat interfaces; CloudProvider → Hosting / CDN / Storage; Worker → Workable / Eatable.",
        "DIP: both depend on abstraction; Switch/Switchable with Fan and LightBulb.",
    ]),
    ("L4 · Pattern basics", [
        "Syllabus slide lists: creational 5, structural 6, behavioral 8 (Facade, Command, Chain of Responsibility, Interpreter are not in this term's syllabus).",
        "Elements: intent/name, problem, solution, consequences.",
        "Structural = composition of structure; behavioral = interaction/responsibility.",
    ]),
], diagrams=[(L1, 22, "ISP split of CloudProvider (sl. 22)", (0, 0.1, 1, 0.95), 11),
             (L1, 25, "Inverted dependency (sl. 25)", (0, 0.1, 1, 0.95), 11)])
print(n.save())
