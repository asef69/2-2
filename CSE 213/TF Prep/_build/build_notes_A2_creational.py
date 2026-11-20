"""Anindya 2 — Creational Design Patterns (Lec 3) → Lessons 5–8."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import new, exam_map, src_note, java, code, AN  # noqa: E402

L3 = os.path.join(AN, "Lec 3 - Creational Design Patterns.pdf")
n = new("Anindya", "Creational Design Patterns — Factory Method, Abstract Factory, Singleton, Builder",
        "CSE213_Anindya_Creational_Patterns_Notes.docx")
n.front_matter([
    ("Exam Map — What the TF Papers Ask", "creational-pattern questions by year"),
    ("Lesson 5 — UML Recap and Factory Method", "sl. 2–16; travel packages, parser by extension"),
    ("Lesson 6 — Abstract Factory", "sl. 17–35; pizza regions, set menus, Uber/Pathao"),
    ("Lesson 7 — Singleton", "sl. 36–42; eager/lazy, serial id generator, limited instances"),
    ("Lesson 8 — Builder and Choosing a Creational Pattern", "sl. 43–53; HTML page, forms, set meals, burger shop, comparison"),
    ("Quick Notes — Creational Patterns", "revision + key structures"),
], source_note=src_note("Slide numbers refer to 'Lec 3 - Creational Design Patterns.pdf' (53 slides). "
                        "All Java in this file was compiled and run with javac (sources in _build/java/A2)."))

exam_map(n, "A2", "The highest-scoring part of Anindya Sir's section: a 15–28-mark 'identify the pattern, draw the "
         "class diagram, write the code' question appears in every paper since 2017-18 (2024-25 Factory Method, "
         "2023-24 Abstract Factory, 2022-23 Builder, 2021-22 Abstract Factory + comparison, 2020-21 three-pattern burger "
         "shop, 2019-20 Singleton, 2018-19 Builder, 2017-18 Builder + Abstract Factory). Learn the four structures by "
         "heart, then the cue words in the Lesson 8 decision table.")

# ---------------------------------------------------------------- L5
n.lesson("Lesson 5 — UML Recap and Factory Method", "Slides 2–16 (Lec 3 - Creational Design Patterns)")
n.h2("1. UML relationships used in pattern diagrams (sl. 2)")
n.table(["Relationship", "Arrow", "Reading", "Slide example"], [
    ["Generalization", "solid line, hollow triangle → parent", "is-a / implements", "Rectangle → Shape"],
    ["Dependency", "dashed line, open arrow", "uses temporarily", "Lottery ⇢ Random"],
    ["Aggregation", "hollow diamond at the whole", "is part of (part can live alone)", "Car ◇— Engine"],
    ["Composition", "filled diamond at the whole", "is entirely made of (parts die with whole)", "Book ◆— Page"],
], widths_cm=[3.0, 5.0, 4.6, 4.6])
n.h2("2. Intent and problem (sl. 4)")
n.callout("memorize", "**Factory Method** — Define an interface for creating an object, but let subclasses decide which "
          "class to instantiate. Factory Method lets a class defer instantiation to subclasses.")
n.p("Problem: a framework standardises the architecture for a range of applications, but each application defines its own "
    "domain objects and their creation. The creator defers product creation to a subclass.")
n.h2("3. Structure and participants (sl. 5)")
code(n, """        Creator                                   «interface»
 ---------------------                          Product
 # factoryMethod(): Product   - - - creates - ->  + operation()
 + anOperation()  { p = factoryMethod(); ... }        ^
           ^                                          |
           |                                          |
    ConcreteCreator                              ConcreteProduct
 # factoryMethod(): Product  { return new ConcreteProduct(); }""")
n.table(["Participant", "Role"], [
    ["Product", "Interface of the objects the factory method creates"],
    ["ConcreteProduct", "Implements Product"],
    ["Creator", "Declares factoryMethod() returning Product; its other code works only with Product"],
    ["ConcreteCreator", "Overrides factoryMethod() to return one ConcreteProduct"],
], widths_cm=[4.0, 13.2])
n.figure_from_pdf(L3, 5, "Figure 5.1 — Factory Method structure (sl. 5)", clip=(0, 0.12, 1, 0.95), width_cm=11)
n.h2("4. Slide examples (sl. 6–14)")
n.bullets([
    "**Drawing (sl. 6–7):** Shape interface (draw), Circle/Square/Rectangle; ShapeFactory.getShape(type) returns the right "
    "shape; the client asks the factory instead of calling new. (This parameterised version is often called a 'simple factory'.)",
    "**Kiosk (sl. 8):** PaymentProcessor (processPayment) with Cash, CreditCard, Coupon; GetPayment.getProcessor(type).",
    "**Electricity bill (sl. 9–11):** abstract Plan(rate; getRate(); calculateBill(units) = units × rate); DomesticPlan 3.50, "
    "CommercialPlan 7.50, InstitutionalPlan 5.50; GetPlanFactory.getPlan(planType); GenerateBill reads plan + units and prints "
    "the bill. E.g. 100 commercial units → 100 × 7.50 = 750.",
    "**Logistics (sl. 12–13):** code coupled to Truck; adding Ship would touch everything. Logistics.createTransport() is "
    "overridden by RoadLogistics (Truck) and SeaLogistics (Ship); planDelivery() works with Transport. Dialog.createButton(): "
    "WindowsDialog → WindowsButton, WebDialog → HTMLButton.",
    "**UI framework (sl. 14):** to make the framework use RoundButton, subclass UIFramework as UIWithRoundButtons and override "
    "createButton(). Use Factory Method when users of a library must be able to extend its internal components.",
])
n.h2("5. Consequences (sl. 15–16)")
n.bullets([
    "Code for an interface, not an implementation; instantiation is removed from client code → less coupling, easy to extend.",
    "Single Responsibility (creation in one place) and Open/Closed (new products without breaking clients).",
    "Cost: many new subclasses (one creator per product).",
])
n.exam_approach([
    "Cue words: 'client must not construct the concrete class', 'centralised creation', 'add new types without modifying'.",
    "Draw Product interface + concrete products, Creator with abstract factory method + concrete creators.",
    "Write the interface, two products, the creator hierarchy and a main() that uses only the abstract types.",
    "End with one line on extension: 'new type = new product + new creator; no existing class changes' (OCP).",
])
n.practice("Lesson 5", "(a) Actual — 2024-25 (22 batch) Q1(a). (b) Actual — 2016-17 Q5(c). (c) Actual — 2010-11 Q3(d).", [
    "(a) A travel company offers Adventure and Regular packages, each with its own activities, pricing and description. "
    "Implement it with a pattern so that client code never constructs a concrete class, packages are created through a "
    "centralised creation component, and new package types need no change to existing code. (15)",
    "(b) Syntax highlighting: choose a parser (.c, .cpp, .java, .html …), all implementing Parser, from the file extension. "
    "Which pattern? Give a Java implementation. (3+7)",
    "(c) XMLReaderFactory has a static createXMLReader() that returns an XMLReader implementation chosen from a system "
    "property. Does it implement the Factory pattern? (5)",
])
n.solution()
n.answer("(a)", "**Factory Method.** The creator PackageCreator owns the creation step (createPackage()); each concrete "
         "creator decides the class. Client code holds only PackageCreator and TourPackage references.")
code(n, """«interface» TourPackage                      PackageCreator {abstract}
 + getName(), getPrice(),                     # createPackage(): TourPackage   «factory method»
   getDescription(), getActivities()          + orderPackage(): TourPackage
     ^                ^                              ^                  ^
AdventurePackage  RegularPackage            AdventureCreator      RegularCreator
                                            createPackage() -> new AdventurePackage()
                                            createPackage() -> new RegularPackage()""")
java(n, "A2", "TravelDemo.java")
n.p("Output: Booked Adventure (25000.0): [Mountain hiking, River rafting] / Booked Regular (12000.0): [City sightseeing, Museum visits].")
n.answer("(b)", "Factory (Factory Method family): the selection logic is one creation component that maps an extension to "
         "a Parser; the editor uses only the Parser interface. Assumptions: extension = text after the last dot; unknown "
         "extension → exception. A registry map keeps the factory closed for modification (new language = register()).")
java(n, "A2", "ParserDemo.java")
n.answer("(c)", "Yes. createXMLReader() is a static factory method: it returns an object of some class implementing "
         "XMLReader, the concrete class is chosen inside the method (from a system property), and the client depends only "
         "on the XMLReader interface. Strictly it is the 'simple/static factory' variant — no subclass overrides a creator "
         "method — so it is the Factory idea, not the full GoF Factory Method structure.")

# ---------------------------------------------------------------- L6
n.lesson("Lesson 6 — Abstract Factory", "Slides 17–35 (Lec 3 - Creational Design Patterns)")
n.callout("memorize", "**Abstract Factory** — Provide an interface for creating **families** of related or dependent "
          "objects without specifying their concrete classes.")
n.p("Problem (sl. 17): a portable application must encapsulate platform dependencies — several look-and-feels, several DBMSs.")
n.h2("1. Structure (sl. 18)")
code(n, """«interface» AbstractFactory              «interface» ProductA      «interface» ProductB
 + createProductA(): ProductA                  ^          ^              ^          ^
 + createProductB(): ProductB              ProductA1  ProductA2      ProductB1  ProductB2
        ^                 ^
 ConcreteFactory1    ConcreteFactory2      Client --> AbstractFactory, ProductA, ProductB only
 createA()->A1        createA()->A2
 createB()->B1        createB()->B2        (factory 1 always makes family 1: A1 + B1)""")
n.figure_from_pdf(L3, 18, "Figure 6.1 — Abstract Factory structure (sl. 18)", clip=(0, 0.12, 1, 0.95), width_cm=12)
n.h2("2. Slide examples (sl. 19–33)")
n.bullets([
    "**Furniture shop (sl. 19–22):** products Chair, Sofa, CoffeeTable × variants ArtDeco, Victorian, Modern. Customers get "
    "angry with non-matching furniture. Declare an interface per product, then FurnitureFactory (createChair, createSofa, "
    "createCoffeeTable); ModernFurnitureFactory makes only Modern pieces.",
    "**Cross-platform GUI (sl. 23–29):** GUIFactory (createButton, createCheckbox) with WinFactory and MacFactory. "
    "ApplicationConfigurator reads the OS at start-up and passes the right factory to Application; the rest of the code "
    "works with Button and Checkbox interfaces only.",
    "**Car factory (sl. 30):** HondaFactory (createEngine, createTrans) with CivicFactory and AccordFactory → CivicEngine/"
    "CivicTrans or AccordEngine/AccordTrans.",
    "**Factory of factories (sl. 31–33):** AbstractFactory (getShape, getColor), ShapeFactory, ColorFactory, "
    "FactoryProducer.getFactory(\"SHAPE\" | \"COLOR\").",
])
n.h2("3. Consequences (sl. 34–35)")
n.table(["Benefit", "Liability"], [
    ["Isolates concrete classes; client sees only interfaces", "Supporting a **new kind of product** is hard: every factory "
     "interface and class must get a new create method"],
    ["Exchanging a whole product family is easy (swap one factory object)", "More interfaces and classes"],
    ["Promotes consistency — products of one family are used together", ""],
    ["No conditional logic in the client (unlike a parameterised factory)", ""],
], widths_cm=[8.6, 8.6])
n.callout("trap", "Factory Method creates **one** product through inheritance (subclass overrides one method). Abstract "
          "Factory creates a **family** through object composition (the client is given a factory object). Each create "
          "method inside an Abstract Factory is often a factory method.")
n.exam_approach([
    "Cue words: 'families', 'region/platform/brand-specific', 'must match', 'consistent', 'sensitive to their orders', "
    "'easily extendable to new countries/platforms'.",
    "Make a table: rows = families (countries, menus, companies), columns = product kinds (crust/sauce, rice/main/fry, car/moto).",
    "One interface per column; one concrete factory per row with one create method per column.",
    "Client receives the factory once and never names a concrete product.",
])
n.practice("Lesson 6", "(a) Actual — 2023-24 Q5(a). (b) Actual — 2021-22 Q3(a). (c) Actual — 2017-18 Q7(b). "
           "(d) Actual — 2014-15 Q6(b).", [
    "(a) Pizza delivery in Italy and America with distinct crust and toppings; each pizza must use region-specific "
    "ingredients and the system must extend easily to more countries. Identify the pattern, justify, and implement. (15)",
    "(b) Four set menus (Veggie Harvest, Chicken Delight, Beef Fiesta, Sea Shanty), each a rice item + a main dish + a "
    "fried item made in kitchens Rice Station, Main Mania and Fry More; users are very sensitive to their orders. "
    "Identify the pattern, give the UML and an implementation. (20)",
    "(c) Uber and Pathao compute car fares n·d·18·f (f = 1.8/1.2/0.9) and n·d·20·f (f = 1.5/1.15/0.9), and moto fares "
    "25 + 12d and 30 + 11d. Input distance, passengers and t (1, 2, 3); output the cost for each app. Class diagram + code. (6+15)",
    "(d) Give one design pattern that reduces dependence on hardware and/or software platforms and explain how. (12)",
])
n.solution()
n.answer("(a)", "**Abstract Factory.** Each country is a family of matching ingredients (crust, sauce, topping). The pizza "
         "code receives a PizzaIngredientFactory and cannot accidentally mix an Italian crust with an American topping; a "
         "new country is one new factory class plus its ingredient classes, with no change to RegionalPizza (OCP).")
code(n, """PizzaIngredientFactory «interface»: createCrust(), createSauce(), createTopping()
   ^ ItalyIngredientFactory   -> ThinCrust,     MarinaraSauce,   Mozzarella
   ^ AmericaIngredientFactory -> DeepDishCrust, PlumTomatoSauce, Pepperoni
Crust, Sauce, Topping «interface»     RegionalPizza(f: PizzaIngredientFactory) -- uses --> the three interfaces""")
java(n, "A2", "PizzaDemo.java")
n.answer("(b)", "**Abstract Factory.** Rows = set menus (families), columns = kitchens (product kinds). 'Users are very "
         "sensitive to their orders' means a menu's three items must come from the same family — exactly the consistency "
         "Abstract Factory guarantees. (A Builder would assemble one order, but would not stop a builder step from mixing "
         "items of two menus.)")
code(n, """SetMenuFactory «interface»: prepareRice(): RiceItem, prepareMain(): MainDish, prepareFried(): FriedItem
  ^ VeggieHarvestFactory   Mushroom Rice      | Paneer Masala    | Fried Vegetable Pakora
  ^ ChickenDelightFactory  Chicken Fried Rice | Butter Chicken   | Fried Chicken Wings
  ^ BeefFiestaFactory      Beef Fried Rice    | Beef Chili Onion | Fried Beef Bacon
  ^ SeaShantyFactory       Rice with Shrimp   | Crab Masala      | Fried Calamari
Restaurant.deliver(f: SetMenuFactory) — the client""")
java(n, "A2", "SetMenuDemo.java")
n.answer("(c)", "**Abstract Factory**: families = companies (Uber, Pathao); products = CarFare and MotoFare. Each fare "
         "object holds its company's formula. (Strategy for the fare formula is also acceptable; Abstract Factory is the "
         "better answer because each company supplies a matching pair.)")
java(n, "A2", "RideDemo.java")
n.p("Check, d = 10 km, n = 2, t = 1: Uber car 2 × 10 × 18 × 1.8 = 648; Pathao car 2 × 10 × 20 × 1.5 = 600; "
    "Uber moto 25 + 120 = 145; Pathao moto 30 + 110 = 140 — matches the program output.")
n.answer("(d)", "**Abstract Factory** (sl. 17, 23–29). All platform-specific classes (WinButton, MacButton …) are created "
         "only inside one concrete factory. At start-up the configurator inspects the OS and creates WinFactory or "
         "MacFactory; the rest of the program talks to GUIFactory, Button and Checkbox interfaces. Porting to a new "
         "platform = writing one new factory and its products; no application code changes. (Bridge is a valid second "
         "answer: it separates the abstraction from a platform implementation hierarchy — IJ Mam's notes.)")

# ---------------------------------------------------------------- L7
n.lesson("Lesson 7 — Singleton", "Slides 36–42 (Lec 3 - Creational Design Patterns)")
n.callout("memorize", "**Singleton** — Ensure a class has only one instance, and provide a global point of access to it. "
          "Encapsulated 'just-in-time initialisation' (initialisation on first use).")
n.h2("1. Structure (sl. 37) and implementation steps (sl. 39)")
code(n, """          Singleton
 ---------------------------------
 - instance: Singleton            (static)
 ---------------------------------
 - Singleton()                    (private constructor)
 + getInstance(): Singleton       (static)  { if (instance == null) instance = new Singleton(); return instance; }""")
n.numbered([
    "Add a private static field to hold the instance.",
    "Declare a public static creation method getInstance().",
    "Implement lazy initialisation inside it: create on the first call, return the same object afterwards.",
    "Make the constructor private so other code cannot use new.",
    "Replace direct constructor calls in client code with getInstance().",
])
n.p("Slide example (sl. 38): DbConnection with private static instance and a private constructor that opens the SQL "
    "connection; DbConnection.getDbConnection() returns the shared connection.")
n.h2("2. Applicability and consequences (sl. 40–42)")
n.bullets([
    "Use it when a class must have exactly one instance available to all clients (database connection, configuration, logger).",
    "Unlike a global variable, nothing except the class itself can replace the cached instance.",
    "Consequences: controlled access to the sole instance; reduced name space (no globals); permits a variable number "
    "of instances — the same code can be changed to allow n instances (used in 2011-12 Q1(b) below).",
    "Criticism: it violates SRP (it solves two problems at once) and makes unit testing harder.",
])
n.h2("3. Eager vs lazy initialisation (textbook — asked 2016-17, 2012-13)")
n.table(["", "Eager", "Lazy"], [
    ["When created", "When the class is loaded (static final field)", "On the first getInstance() call"],
    ["Thread safety", "Safe automatically (class loading is thread-safe)", "Needs synchronized / double-checked locking / holder class"],
    ["Cost", "Wastes memory/time if never used", "Pays only when used; small check on every call"],
    ["Prefer when", "Object is cheap and always needed", "Object is expensive (DB connection, large cache) or may never be used"],
], widths_cm=[3.0, 7.1, 7.1])
java(n, "A2", "SingletonKinds.java")
n.practice("Lesson 7", "(a) Actual — 2019-20 Q1(a). (b) Actual — 2016-17 Q5(a) / 2012-13 Q2(a). (c) Actual — 2010-11 Q4(a). "
           "(d) Actual — 2011-12 Q1(b).", [
    "(a) A web app creates userID, home-district, qualification and transaction (TxID) identifiers in the back end, each "
    "never duplicated and created serially from 1, used as primary keys. Demonstrate their creation with a suitable "
    "pattern. (15)",
    "(b) Describe eager and lazy initialisation of a singleton; give an example where lazy should be preferred; draw the "
    "structure. (15)",
    "(c) Which of the two implementations is a valid Singleton? (i) eager field but getInstance() is private; (ii) "
    "SingletonHolder nested class with public getInstance(). (5)",
    "(d) Class Base is inherited by Derived1 and Derived2; at most 5 Derived1 and 10 Derived2 objects can exist. Write the "
    "Java code and a main that creates arrays of both. (18⅔)",
])
n.solution()
n.answer("(a)", "**Singleton** (one generator object per identifier kind). If two generator objects existed, both would "
         "start at 1 and hand out duplicate primary keys; a single shared instance with a synchronized counter guarantees "
         "serial, unique values for the whole back end. In a real system the counter would be initialised from MAX(id) in "
         "the table at start-up.")
java(n, "A2", "IdDemo.java")
n.p("Output: user 1, user 2 / district 1, tx 1, tx 2, qualification 1 / same object? true.")
n.answer("(b)", "Use the table in §3 and the code above. Lazy preferred example: a DatabaseConnectionPool or report "
         "generator that opens many connections — creating it at start-up slows launch and wastes resources if the user "
         "never opens a report. Structure: the box in §1.")
n.answer("(c)", "(i) is **not usable**: the eager field is fine, but getInstance() is private, so no other class can obtain "
         "the instance — there is no global access point. (ii) is **valid** (initialisation-on-demand holder): the private "
         "constructor stops new, the nested class is loaded only when getInstance() is first called (lazy), and the JVM's "
         "class loading makes it thread-safe without synchronized.")
n.answer("(d)", "Generalise the private constructor + static access method so the class counts its instances and refuses "
         "the (limit+1)-th one.")
java(n, "A2", "LimitedDemo.java")
n.p("Output: Derived1 created: 5 of 7 / Derived2 created: 10 of 12.")

# ---------------------------------------------------------------- L8
n.lesson("Lesson 8 — Builder and Choosing a Creational Pattern", "Slides 43–53 (Lec 3 - Creational Design Patterns)")
n.callout("memorize", "**Builder** — Separate the construction of a complex object from its representation so that the "
          "same construction process can create different representations.")
n.p("Problem (sl. 43): an application builds the parts of a complex aggregate; one construction specification must be "
    "able to produce several different representations.")
n.h2("1. Structure (sl. 44)")
code(n, """   Director                      «interface» Builder                 Product
 - builder: Builder  <>---------> + buildPartA()                  (complex object,
 + construct() {                    + buildPartB()                   assembled in parts)
     builder.buildPartA();          + getResult(): Product                ^
     builder.buildPartB(); }               ^          ^                   | creates
                                   ConcreteBuilder1  ConcreteBuilder2 ----+""")
n.figure_from_pdf(L3, 44, "Figure 8.1 — Builder structure (sl. 44)", clip=(0, 0.12, 1, 0.95), width_cm=11)
n.table(["Participant", "Role (kids-meal analogy, sl. 45)"], [
    ["Director", "Fixes the order of the steps (the cashier tells the crew: burger, drink, toy)"],
    ["Builder", "Interface with one method per part"],
    ["ConcreteBuilder", "Builds and remembers one representation (the restaurant crew for one meal type)"],
    ["Product", "The finished complex object (the bagged meal)"],
    ["Client", "Picks the concrete builder, gives it to the director, collects the product (the customer)"],
], widths_cm=[3.6, 13.6])
n.h2("2. Slide examples (sl. 45–53)")
n.bullets([
    "Computer assembled from parts per order (500 GB disk + Intel vs 250 GB disk + AMD).",
    "Vehicle (sl. 47–49): IBuilder (BuildBody, InsertWheels, AddHeadlights, GetVehicle); Car and MotorCycle builders; "
    "Product keeps a list of parts and Show(); Director.Construct(builder) calls the three steps in order.",
    "CD packing (sl. 50–53): Packing (pack, price); CD → Company → Sony (20), Samsung (15); CDType holds items (addItem, "
    "getCost, showItems); CDBuilder.buildSonyCD() / buildSamsungCD(); BuilderDemo prints the costs.",
])
n.h2("3. Consequences (sl. 46)")
n.bullets(["Lets you vary a product's internal representation.", "Isolates construction code from representation code.",
           "Gives finer control over the construction process (step by step, under the director)."])
n.h2("4. Choosing a creational pattern (2021-22 Q1(a))")
n.table(["Pattern", "Use when", "Example"], [
    ["Factory Method", "One product; the subclass (or a parameter) decides which concrete class; client must not call new",
     "Logistics.createTransport() → Truck / Ship; travel packages"],
    ["Abstract Factory", "A family of related products must be created together and stay consistent; swap the family as a whole",
     "GUIFactory → WinButton + WinCheckbox; pizza ingredients per country"],
    ["Builder", "One complex object built step by step; same steps give different representations; many optional parts",
     "HTML page; meals; forms per user type"],
    ["Singleton", "Exactly one shared instance with global access", "DB connection, id generator"],
    ["Bridge (structural)", "Two independent dimensions (abstraction × implementation) would explode into subclasses; "
     "connect two hierarchies by composition", "Shape × Color; Notification × Email/SMS/Push"],
], widths_cm=[3.2, 8.2, 5.8], font_size=8.5)
n.practice("Lesson 8", "(a) Actual — 2022-23 Q3(a). (b) Actual — 2018-19 Q3(b). (c) Actual — 2017-18 Q6(a). "
           "(d) Actual — 2020-21 Q1(a)–(b). (e) Actual — 2021-22 Q1(a).", [
    "(a) HTMLPageDirector tells the builder HTMLPageBuilder the pageTitle, pageHeading and several lines of text, then has it "
    "assemble the parts and return the page. Class diagram + code. (15)",
    "(b) A grades application shows different forms (enabled/disabled buttons) to admin and student. Builder gives the form "
    "interface, concrete builders are the per-user forms, the product is the final form and the director is the "
    "application. Class diagram + code. (20)",
    "(c) Lalbagh food shop: set meals with a main item (rice or bread); rice comes with gravy curries, bread with chicken or "
    "beef kebabs; drinks are ordered separately; the bill must be paid before eating. Class diagram + code. (7+15)",
    "(d) Burger shop: Veggi/Beef/Chicken pizza, optional extra cheese, drinks (Coffee, Water, Coke — one or more), "
    "appetizers (Onion Rings, French Fries), and meals (appetizer + pizza with cheese + drinks). Construct the four orders "
    "(1 Beef pizza + French fry + cheese, 2 Chicken pizza + onion rings + water, 3 combo Veggi + French fry + two Cokes, "
    "4 combo Veggi + Onion Rings + Coffee + Water) using three patterns, with price methods; then compare the patterns. (28+7)",
    "(e) Differentiate the use cases of Factory Method, Abstract Factory, Builder and Bridge. (16)",
])
n.solution()
n.answer("(a)", "**Builder** with the names given in the question.")
code(n, """HTMLPageDirector                  «interface» PageBuilder                 HTMLPage (product)
 - builder: PageBuilder <>-----> + setPageTitle(t)                      - title, heading, lines
 + construct(title, heading,       + setPageHeading(h)                    + render(): String
             lines...): HTMLPage   + addText(line)                              ^ creates
                                    + getPage(): HTMLPage                       |
                                            ^ HTMLPageBuilder ------------------+""")
java(n, "A2", "HtmlDemo.java")
n.answer("(b)", "**Builder** exactly as the question maps it: FormBuilder (interface/abstract), AdminFormBuilder and "
         "StudentFormBuilder (concrete builders), Form (product), GradeApplication (director, chooses the builder from the "
         "login role and calls the steps in a fixed order).")
java(n, "A2", "FormDemo.java")
n.answer("(c)", "**Builder**: every set meal is built by the same steps (main item, sides, optional drink, bill) but each "
         "concrete builder gives a different representation. Waiter = director; the bill is computed from the product "
         "before it is served. Prices are assumed.")
code(n, """Waiter (director) <>--> SetMealBuilder {abstract}: addMainItem(), addSides(), addDrink(n,p), getMeal()
                              ^ RiceMealBuilder     (rice + gravy curry + dal)
                              ^ ChickenKebabMealBuilder (naan + chicken kebab)
                              ^ BeefKebabMealBuilder    (naan + beef kebab)
SetMeal (product) — list of Food; bill()""")
java(n, "A2", "LalbaghDemo.java")
n.answer("(d)", "Three patterns, each fitting one requirement (prices assumed: Veggi 300, Beef 400, Chicken 350, cheese "
         "+50, Coffee 80, Water 20, Coke 40, French Fry 100, Onion Rings 120): **Decorator** — extra cheese wraps a pizza "
         "and adds to price(); **Composite** — an order is a MenuItem containing MenuItems, so price() of an order = sum of "
         "its parts; **Builder** — a combo meal is assembled step by step (pizza, appetizer, drinks) by ComboBuilder.")
java(n, "A2", "BurgerShop.java")
n.p("Output: Order 1 = 400 + 50 + 100 = 550; Order 2 = 350 + 120 + 20 = 490; Order 3 = 300 + 100 + 2 × 40 = 480; "
    "Order 4 = 300 + 120 + 80 + 20 = 520.")
n.table(["Pattern", "Advantages", "Disadvantages"], [
    ["Decorator", "Add any number of extras at run time (double cheese = two wrappers); no subclass explosion "
     "(BeefWithCheese …); OCP", "Many small objects; order of wrapping can matter; harder to debug"],
    ["Composite", "Orders and items are treated uniformly; nested combos; price() recursion is automatic",
     "Hard to restrict what a composite may contain (e.g. 'exactly one pizza')"],
    ["Builder", "Step-by-step construction; fixed recipe for combos; validation before build()",
     "Extra builder classes; overkill for single items"],
], widths_cm=[2.6, 8.0, 6.6], font_size=8.5)
n.answer("(e)", "Use the table in §4. Key contrasts: Factory Method vs Abstract Factory — one product via subclass override "
         "vs a consistent family via a factory object; Builder — one complex product in steps, versus factories that return "
         "a product in one call; Bridge — structural, not creational: it avoids an abstraction × implementation class "
         "explosion by composition (Notification has a MessageSender). Draw one tiny diagram per pattern.")

n.quick_notes("Quick Notes — Creational Patterns", "Revision points for Lessons 5–8.", [
    ("L5 · Factory Method", [
        "Intent: interface for creating an object, subclasses decide the class.",
        "Creator.factoryMethod() abstract; ConcreteCreator returns ConcreteProduct; client sees Product only.",
        "Cues: client must not call new; centralised creation; add types without editing.",
        "Slides: ShapeFactory, PaymentProcessor kiosk, electricity Plan (3.50/7.50/5.50), Logistics, Dialog.",
    ]),
    ("L6 · Abstract Factory", [
        "Families of related products, consistent; one concrete factory per family.",
        "Rows = families, columns = product kinds. Pizza (Italy/America), set menus, Uber/Pathao, GUI per OS.",
        "Liability: adding a new product kind changes every factory.",
    ]),
    ("L7 · Singleton", [
        "Private static instance + private constructor + public static getInstance().",
        "Eager = at class load (thread-safe); lazy = on first call (needs synchronized / DCL / holder).",
        "Variable number of instances: count in constructor (Derived1 ≤ 5, Derived2 ≤ 10).",
    ]),
    ("L8 · Builder", [
        "Director fixes the steps; ConcreteBuilder makes one representation; getResult() returns the product.",
        "Cues: 'complex object', 'step by step', 'same process, different representations', director named.",
        "Burger shop: Decorator (cheese) + Composite (orders) + Builder (combos).",
    ]),
], diagrams=[(L3, 5, "Factory Method (sl. 5)", (0, 0.12, 1, 0.95), 10),
             (L3, 18, "Abstract Factory (sl. 18)", (0, 0.12, 1, 0.95), 10),
             (L3, 44, "Builder (sl. 44)", (0, 0.12, 1, 0.95), 10)])
print(n.save())
