"""IJ 1 — Structural design patterns (1 - StructuralDesignPattern.pdf + Misc) → Lessons 1–4."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import new, exam_map, src_note, java, code, IJ  # noqa: E402

ST = os.path.join(IJ, "1 - StructuralDesignPattern.pdf")
MI = os.path.join(IJ, "3 - Design Pattern Misc.pdf")
n = new("IJ", "Structural Design Patterns — Decorator, Composite, Adapter, Bridge",
        "CSE213_IJ_Structural_Patterns_Notes.docx")
n.front_matter([
    ("Exam Map — What the TF Papers Ask", "structural-pattern questions by year"),
    ("Lesson 1 — Decorator", "pp. 1–50; Starbuzz, network packet layers, java.io"),
    ("Lesson 2 — Composite", "pp. 51–60; menus, employee hierarchy, FinCorp reports"),
    ("Lesson 3 — Adapter (object vs class)", "pp. 61–95; ducks/turkeys, zip-code weather, Bird/ToyDuck"),
    ("Lesson 4 — Bridge", "pp. 96–111; shapes × colours, notifications × channels"),
    ("Quick Notes — Structural Patterns", "revision + key structures"),
], source_note=src_note("Page numbers refer to '1 - StructuralDesignPattern.pdf' (113 pages; many pages are animation "
                        "build-ups of the same slide, so ranges are given) and '3 - Design Pattern Misc.pdf' (8 pages). "
                        "All Java here was compiled and run with javac (sources in _build/java/I1)."))
exam_map(n, "I1", "One structural-pattern design question in almost every paper: 2024-25 Composite + Decorator (20, "
         "★★★), 2022-23 Adapter (15), 2021-22 Decorator (20), 2020-21 and 2019-20 "
         "Composite (15, 20), 2018-19 Adapter (18). Learn the four structure diagrams and the 'cue words' table at the end "
         "of each lesson. Facade, Proxy and Flyweight are not in this term's syllabus (2023-24 Q5(b), Adapter + Facade, "
         "is listed in the tracker's Outside Notes).")

# ---------------------------------------------------------------- L1
n.lesson("Lesson 1 — Decorator", "Pages 1–50 (1 - StructuralDesignPattern) · Misc p. 2")
n.p("Structural patterns explain how to assemble objects and classes into larger structures while keeping these "
    "structures flexible and efficient (pp. 2–4).")
n.h2("1. The Starbuzz problem (pp. 5–21)")
n.bullets([
    "Beverage (description, getDescription(), abstract cost()) with HouseBlend, DarkRoast, Decaf, Espresso; customers add "
    "condiments — steamed milk, soy, mocha, whip — or not.",
    "Subclass per combination (DarkRoastWithMochaAndWhip …) → **class explosion** (pp. 11–13).",
    "Boolean flags in Beverage (hasMilk(), setMocha() …) and cost() adds them (pp. 14–21). Problems: a new condiment "
    "changes the superclass; iced tea inherits condiments it cannot take; no double mocha.",
])
n.h2("2. Decorate instead (pp. 22–46)")
n.p("Start with a beverage and wrap it: DarkRoast inside Mocha inside Whip. cost() is delegated inward and each wrapper "
    "adds its own price: Whip.cost() = .10 + Mocha.cost() = .10 + .20 + DarkRoast.cost() (.99) = $1.29.")
java(n, "I1", "StarbuzzCoffee.java")
n.p("Output (as on p. 46): Espresso $1.99 · Dark Roast Coffee, Mocha, Mocha, Whip $1.49 · House Blend Coffee, Soy, Mocha, Whip $1.34.")
n.h2("3. Definition and structure (pp. 47–50)")
n.callout("memorize", "**Decorator** lets you attach new behaviours to objects by placing them inside special wrapper "
          "objects that contain the behaviours. (GoF: attach additional responsibilities to an object dynamically; a "
          "flexible alternative to subclassing.)")
code(n, """        «interface» Component  <------------------------------+
        + execute()                                           | wraps (has-a)
           ^                    ^                             |
   ConcreteComponent       BaseDecorator {abstract} ----------+
   + execute()             - wrappee: Component
                           + BaseDecorator(c: Component)
                           + execute() { wrappee.execute(); }
                                   ^                 ^
                     ConcreteDecoratorA     ConcreteDecoratorB
                     + execute() { super.execute(); extra(); }
Client:  a = new ConcreteComponent();  b = new ConcreteDecoratorA(a);  c = new ConcreteDecoratorB(b);  c.execute();""")
n.figure_from_pdf(ST, 50, "Figure 1.1 — Decorator structure (p. 50)", clip=(0.22, 0.1, 1, 0.97), width_cm=10)
n.table(["Participant", "Role"], [
    ["Component", "common interface of wrappers and wrapped objects"],
    ["ConcreteComponent", "the object being wrapped; basic behaviour"],
    ["BaseDecorator", "holds a reference of the Component type and delegates all work to it"],
    ["ConcreteDecorators", "add behaviour before/after calling the wrapped object"],
    ["Client", "wraps components in as many layers as needed, working through the Component interface"],
], widths_cm=[3.8, 13.4])
n.p("Real-world: java.io (Misc p. 2) — new BufferedReader(new InputStreamReader(new FileInputStream(\"data.txt\"))): "
    "FileInputStream reads bytes (core), InputStreamReader adds byte→char conversion, BufferedReader adds buffering and "
    "readLine(). Open for extension, closed for modification.")
n.table(["Use Decorator when", "Prefer instead"], [
    ["extras are optional, combinable, repeatable, chosen at run time", "Strategy — to swap the whole algorithm, not stack layers"],
    ["subclassing would explode or is impossible (final class)", "Adapter — when the interface must change, not be kept"],
    ["each layer adds one responsibility and keeps the interface", "Composite — when objects form a part–whole tree"],
], widths_cm=[8.6, 8.6], font_size=9)
n.practice("Lesson 1", "(a) Actual — 2021-22 Q2(a).", [
    "(a) A five-layer network model: the user creates Packet(message, length) e.g. ('hello', 5); the Application layer adds "
    "APPHEADER_ (length 15), Transport TRHEADER_ (24), Network NETHEADER_ (34), Data-link DHEADER_ and _DTRAILER (51), "
    "Physical PHEADER_ (59) and returns the final Packet. Identify the pattern, implement it and give the UML class "
    "diagram. (20)",
])
n.solution()
n.answer("(a)", "**Decorator.** Every layer has the same interface (send a packet), wraps the layer above it, and adds "
         "one header (data-link: header and trailer) without changing the others. Layers can be added, removed or "
         "re-ordered by changing the wrapping only.")
code(n, """«interface» Layer + send(msg): Packet  <----------------------------+
   ^ RawPacket (creates Packet(msg))                                   | inner
   ^ LayerDecorator {abstract} - inner: Layer ---------------------------+
        ^ ApplicationLayer  ^ TransportLayer  ^ NetworkLayer  ^ DataLinkLayer  ^ PhysicalLayer
Packet - message: String  + length(): int""")
java(n, "I1", "NetworkStack.java")
n.p("Output: message: PHEADER_DHEADER_NETHEADER_TRHEADER_APPHEADER_hello_DTRAILER, length: 59 — the lengths 5, 15, 24, "
    "34, 51, 59 match the question.")

# ---------------------------------------------------------------- L2
n.lesson("Lesson 2 — Composite", "Pages 51–60 (1 - StructuralDesignPattern)")
n.p("Pancake House and Diner menus are merged; the Waitress must print all menus, a submenu (desserts inside the diner "
    "menu) or the whole hierarchy (pp. 51–55). Menus contain menu items **and** other menus → a tree of nodes (Menu) and "
    "leaves (MenuItem) (p. 56).")
code(n, """Waitress --> «abstract» MenuComponent: getName(), getDescription(), getPrice(), isVegetarian(), print(),
                                       add(c), remove(c), getChild(i)      (default: throw UnsupportedOperation)
              ^ MenuItem (leaf): name, description, vegetarian, price; print()
              ^ Menu (composite): menuComponents: List<MenuComponent>; add, remove, getChild,
                                  print() { print own name; for each child: child.print(); }""")
n.callout("memorize", "**Composite** lets you compose objects into tree structures and then work with these structures as "
          "if they were individual objects (p. 58).")
code(n, """Client --> «interface» Component + execute()  <-----------+
             ^ Leaf + execute()  (does the real work)      | children (0..*)
             ^ Composite - children: Component[] ----------+
                         + add(c), remove(c), getChildren()
                         + execute() { for each child: child.execute(); combine results }""")
n.figure_from_pdf(ST, 60, "Figure 2.1 — Composite structure (p. 60)", clip=(0.42, 0.12, 1, 0.97), width_cm=10)
n.h2("Implementation issues and consequences (2011-12 Q1(a) — GoF background)")
n.table(["Issue", "Choice"], [
    ["Where to declare add/remove", "in Component (**transparency**: client treats all alike, but a leaf must reject add) "
     "or only in Composite (**safety**: compile-time check, but client must know the type)"],
    ["Parent references", "keep a parent link for upward navigation / deletion; maintain it in add/remove"],
    ["Child ordering & storage", "List if order matters (menus, layers); cache aggregated values if expensive"],
    ["Who deletes children", "the composite, when it is deleted (unless children are shared)"],
    ["Sharing components", "possible (Flyweight) but complicates parent references"],
], widths_cm=[4.4, 12.8], font_size=9)
n.p("Consequences: uniform treatment of leaves and composites; easy to add new component kinds; simple client code with "
    "recursion. Liability: the design can become overly general — hard to restrict which components a composite may hold.")
n.practice("Lesson 2", "(a) Actual — 2019-20 Q2(a) / 2020-21 Q3(a). (b) Actual — 2024-25 Q2(a). (c) Actual — 2010-11 Q4(d). "
           "(d) Actual — 2011-12 Q1(a).", [
    "(a) A Managing Director heads Technical, Administration and Finance divisions, each with a Manager; five developers "
    "under the technical manager, three executives under admin, two officers under finance. Implement the hierarchy with "
    "Composite; any employee must be able to show all employees under him/her (direct and indirect). (20 / 15)",
    "(b) FinCorp: offices in cities within states within countries; state, country and global reports aggregate their "
    "subordinates and attach level-specific analysis; optional sections (tax, investment, compliance) may be added in "
    "any combination without changing the core report. Identify the pattern(s) and implement minimally. (20)",
    "(c) Extend the Facebook-group design (Observer) so a group page can itself be a member of another group ('CSE BUET "
    "08' joins 'BUETIANS'). Which pattern, and how? (12⅔)",
    "(d) Discuss the implementation issues and consequences of the Composite pattern. (14)",
])
n.solution()
n.answer("(a)", "Component = Employee; leaf = Worker (developer, executive, officer); composite = Manager (MD and the three "
         "managers). showAll() prints the employee and recursively everyone below; countAll() counts direct + indirect.")
java(n, "I1", "CompanyHierarchy.java")
n.p("Output: the tree with MD at the top and 'Under MD: 13, under Technical Manager: 5'.")
n.answer("(b)", "**Composite** for requirement (i): CityOffice is a leaf; State, Country and Global are composites that "
         "sum their children's expenditure and run their own analysis(); all share the ReportUnit interface, so every "
         "stakeholder calls report() the same way. **Decorator** for requirement (ii): TaxSection, InvestmentSection and "
         "ComplianceSection wrap any ReportUnit and append their section, in any combination, without touching the core "
         "classes.")
code(n, """«interface» ReportUnit: name(), expenditure(), report()
   ^ CityOffice (leaf)
   ^ Region {abstract} (composite) - children: List<ReportUnit>; add(u); expenditure() = own + Σ children; analysis()
        ^ State   ^ Country   ^ Global
   ^ ReportSection {abstract} (decorator) - inner: ReportUnit
        ^ TaxSection   ^ InvestmentSection   ^ ComplianceSection""", size=8)
java(n, "I1", "FinCorpReports.java", size=8)
n.p("Output: New York total = 700 [highest-spending city: NYC] · USA total = 1250 + tax 187.5 · FinCorp Global total = "
    "1550 [USA 81 %, Germany 19 %] + investment + compliance sections.")
n.answer("(c)", "**Composite.** Make the group itself a member: introduce GroupMember (Component) with receive(update); "
         "User is a leaf, Group is a composite that holds members (users or groups). When a post is published in "
         "BUETIANS, it calls receive() on each member; the 'CSE BUET 08' group forwards to all its own members, so they "
         "automatically become members of BUETIANS. Group keeps its Observer role (subject) and now also implements the "
         "observer/member interface.")
code(n, """«interface» GroupMember + receive(post: String)              (Observer + Component)
   ^ User (leaf): receive(p) { newsFeed.add(p); }
   ^ Group (composite + subject): members: List<GroupMember>; join(m); leave(m);
                                  publish(p) { for m in members: m.receive(p); }
                                  receive(p) { publish(p); }      // a member group re-broadcasts""")
n.answer("(d)", "The issues table and consequences above.")

# ---------------------------------------------------------------- L3
n.lesson("Lesson 3 — Adapter (object vs class)", "Pages 61–95 (1 - StructuralDesignPattern)")
n.p("An adapter sits between your existing system and a vendor class with a different interface, like a plug adapter "
    "(pp. 61–65). Duck simulator (pp. 66–79): Duck (quack, fly), MallardDuck; vendor Turkey (gobble, fly — short "
    "distance), WildTurkey. TurkeyAdapter implements Duck: quack() → turkey.gobble(); fly() → five turkey.fly() calls.")
code(n, """public class TurkeyAdapter implements Duck {
    Turkey turkey;
    public TurkeyAdapter(Turkey turkey) { this.turkey = turkey; }
    public void quack() { turkey.gobble(); }
    public void fly() { for (int i = 0; i < 5; i++) turkey.fly(); }
}""")
n.callout("memorize", "**Adapter** — Convert the interface of a class into another interface clients expect. Adapter lets "
          "classes work together that couldn't otherwise because of incompatible interfaces (p. 83).")
code(n, """OBJECT ADAPTER (composition, p. 86-88)             CLASS ADAPTER (inheritance, p. 89-90)
Client --> «interface» Target + request()           Client --> «interface» Target + request()
                ^                                                  ^
             Adapter - adaptee: Adaptee ---->  Adaptee          Adapter ------------|>  Adaptee
             + request() {                     + specificRequest()  + request() { specificRequest(); }
                 adaptee.specificRequest(); }                   (extends Adaptee AND implements Target)""")
n.figure_from_pdf(ST, 88, "Figure 3.1 — Object adapter (p. 88)", clip=(0.42, 0.12, 1, 0.97), width_cm=10)
n.table(["", "Object adapter", "Class adapter"], [
    ["Mechanism", "composition: holds an Adaptee", "inheritance: subclasses Adaptee and implements Target"],
    ["Language", "works in every OO language", "needs multiple inheritance (C++); in Java only if Target is an interface"],
    ["Pros", "adapts the Adaptee **and all its subclasses**; can be swapped at run time; keeps Adaptee hidden",
     "no extra object; can **override** Adaptee behaviour; no need to re-implement the whole Adaptee"],
    ["Cons", "cannot override Adaptee methods easily; one more object/indirection", "tied to one concrete Adaptee class; "
     "exposes Adaptee's public methods; inflexible"],
], widths_cm=[2.4, 7.4, 7.4], font_size=9)
n.p("XML → JSON example (p. 85): a stock app downloads XML data but the analytics library wants JSON; an XML-to-JSON "
    "adapter converts the data before calling the library. Decorator vs Adapter (pp. 94–95): a decorator adds "
    "responsibilities and **keeps** the interface; an adapter **converts** the interface.")
n.practice("Lesson 3", "(a) Actual — 2022-23 Q1(a). (b) Actual — 2018-19 Q4(b). (c) Actual — 2016-17 Q5(d). "
           "(d) Actual — 2010-11 Q4(e).", [
    "(a) A service returns the temperature for a city name; the client wants to pass a zip code. Class diagram + code. (15)",
    "(b) Bird (fly(), makeSound()) and ToyDuck (squeak()): use Bird objects in place of ToyDucks. Class diagram + code. (18)",
    "(c) Draw the class-adapter UML; pros and cons of object adapter vs class adapter. (6⅔)",
    "(d) The application uses LibX (vendor out of business); LibY offers the same functionality with different interfaces; "
    "no source code for either. Which pattern? Class diagram. (7)",
])
n.solution()
n.answer("(a)", "**Object Adapter.** Target = ZipWeatherService.getTemperature(int zip); Adaptee = existing "
         "CityWeatherService.getTemperature(String city); Adapter maps the zip code to a city and delegates.")
code(n, """Client --> «interface» ZipWeatherService + getTemperature(zip: int): double
                 ^
          ZipToCityAdapter - service: CityWeatherService - zipToCity: Map<int,String> ---> CityWeatherService
          + getTemperature(zip) { return service.getTemperature(zipToCity.get(zip)); }   + getTemperature(city: String)""", size=8)
java(n, "I1", "WeatherAdapter.java")
n.answer("(b)", "Target = ToyDuck; Adaptee = Bird; BirdAdapter implements ToyDuck and holds a Bird; squeak() → makeSound().")
java(n, "I1", "BirdAdapterDemo.java")
n.answer("(c)", "Class-adapter diagram in the box above (Adapter extends Adaptee, implements Target); pros/cons table.")
n.answer("(d)", "**Adapter.** Keep the application's code written against LibX's interface (extract it as an interface "
         "LibXApi if needed); write LibXToLibYAdapter classes that implement those interfaces and delegate each call to "
         "the corresponding LibY classes (object adapters, since we cannot modify either library).")
code(n, """Application --> «interface» LibXApi (the old method signatures)
                      ^
               LibXToLibYAdapter - y: LibYClass  ---> LibYClass (new, different interface)
               + oldMethod(args) { convert args; return y.newMethod(converted); }""")

# ---------------------------------------------------------------- L4
n.lesson("Lesson 4 — Bridge", "Pages 96–111 (1 - StructuralDesignPattern) · Misc pp. 5–8")
n.p("Shapes (Circle, Square) × colours (Red, Blue): subclassing every combination (RedCircle, BlueSquare …) grows as "
    "shapes × colours (pp. 96–103). Split into two hierarchies — form and colour — and let Shape **contain** a Color: "
    "inheritance becomes composition (p. 104).")
n.callout("memorize", "**Bridge** lets you split a large class or a set of closely related classes into two separate "
          "hierarchies — abstraction and implementation — which can be developed independently of each other (p. 108).")
code(n, """Client --> Abstraction  - i: Implementation  <>--------------> «interface» Implementation
           + feature1() { i.method1(); }                            + method1(), method2(), method3()
           + feature2()                                                ^                 ^
              ^                                               ConcreteImplA     ConcreteImplB
        RefinedAbstraction + featureN()""")
n.figure_from_pdf(ST, 108, "Figure 4.1 — Bridge structure (p. 108)", clip=(0.42, 0.18, 1, 0.97), width_cm=10)
n.p("Abstraction = high-level control layer (GUI); it delegates the real work to the implementation layer (platform APIs: "
    "Linux, Windows, macOS) (pp. 105–107). Implementations are interchangeable; the same GUI works under different OSs.")
n.h3("Notification example (Misc pp. 7–8)")
n.p("Abstractions: Alert, Promotion, OTP notifications; implementations: Email, SMS, Push. Without Bridge 3 × 3 = 9 classes; "
    "with Bridge 3 + 3 classes and any combination at run time.")
java(n, "I1", "NotificationBridge.java")
n.table(["Pattern", "Intent in one line", "Cue words"], [
    ["Decorator", "add responsibilities by wrapping; same interface", "optional add-ons, layers, extra cheese, headers"],
    ["Composite", "part–whole trees treated uniformly", "hierarchy, sub-menu, subordinates, group in a group, aggregate totals"],
    ["Adapter", "convert one interface to the one clients expect", "existing/vendor class, incompatible, zip vs city, LibX → LibY"],
    ["Bridge", "abstraction and implementation vary independently", "two dimensions, platform, channel, colour × shape"],
], widths_cm=[2.6, 7.4, 7.2], font_size=9)
n.practice("Lesson 4", "(a) Constructed (Bridge vs Adapter). (b) Constructed.", [
    "(a) Bridge and Adapter both delegate to another object. What is the difference in intent and timing?",
    "(b) A drawing app draws Circle and Rectangle using either a vector or a raster renderer. Give the Bridge diagram.",
])
n.solution()
n.answer("(a)", "Bridge is designed **up front** to let two dimensions vary independently (abstraction ↔ implementation "
         "chosen at run time). Adapter is applied **after the fact** to make an existing, incompatible class fit an "
         "expected interface.")
code(n, """Shape {abstract} - renderer: Renderer ------> «interface» Renderer + drawCircle(x,y,r), drawRect(x,y,w,h)
  + draw()                                         ^ VectorRenderer     ^ RasterRenderer
  ^ Circle  draw() { renderer.drawCircle(...) }
  ^ Rectangle draw() { renderer.drawRect(...) }""")

n.quick_notes("Quick Notes — Structural Patterns", "Revision points for Lessons 1–4.", [
    ("L1 · Decorator", ["Wrapper with the same interface; cost/behaviour delegated inward + own addition.",
                        "Starbuzz: DarkRoast + Mocha + Mocha + Whip = $1.49. java.io BufferedReader.",
                        "Network packet layers = Decorator (each always adds a header)."]),
    ("L2 · Composite", ["Component, Leaf, Composite(children); operation recurses over children.",
                        "Transparency vs safety of add/remove; parent links; ordering.",
                        "Employee hierarchy, FinCorp (Composite + Decorator), group inside group."]),
    ("L3 · Adapter", ["Target, Adapter, Adaptee; object (composition) vs class (inheritance).",
                               "Zip → city, Bird → ToyDuck, Turkey → Duck, LibX → LibY.",
                               "Decorator keeps the interface; Adapter converts it."]),
    ("L4 · Bridge", ["Abstraction has an Implementation; both hierarchies vary independently.",
                     "Shapes × colours; notifications × channels (9 → 6 classes)."]),
], diagrams=[(ST, 60, "Composite (p. 60)", (0.42, 0.12, 1, 0.97), 9),
             (ST, 108, "Bridge (p. 108)", (0.42, 0.18, 1, 0.97), 9)])
print(n.save())
