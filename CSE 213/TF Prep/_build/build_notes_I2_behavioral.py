"""IJ 2 — Behavioral design patterns (2 - BehavioralDesignPattern.pdf + Misc) → Lessons 5–11."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import new, exam_map, src_note, java, code, IJ  # noqa: E402

BH = os.path.join(IJ, "2 - BehavioralDesignPattern.pdf")
n = new("IJ", "Behavioral Design Patterns — Strategy, Template Method, Observer, Mediator, State",
        "CSE213_IJ_Behavioral_Patterns_Notes.docx")
n.front_matter([
    ("Exam Map — What the TF Papers Ask", "behavioral-pattern questions by year"),
    ("Lesson 5 — Strategy", "pp. 4–48; SimUDuck, robots, sorting, talk-time, grading"),
    ("Lesson 6 — Template Method", "pp. 49–81; caffeine beverages, data miner, Template + Strategy"),
    ("Lesson 7 — Observer", "pp. 82–128; Weather-O-Rama, stock grabber, blogs, dashboards"),
    ("Lesson 8 — Mediator", "pp. 129–167; dialog, ATC tower, sort broker"),
    ("Lesson 9 — State (and State vs Strategy)", "pp. 203–260; gumball machine, document"),
    ("Lesson 10 — Identifying the Pattern", "mixed TF questions"),
    ("Quick Notes — Behavioral Patterns", "revision + key structures"),
], source_note=src_note("Page numbers refer to '2 - BehavioralDesignPattern.pdf' (261 pages, with animation build-ups). "
                        "The Command pattern (pp. 168–202) is NOT in this term's syllabus, and neither are Chain of Responsibility "
                        "and Interpreter, so they are left out; their past questions are in the tracker's Outside Notes tab. "
                        "All Java compiled with javac "
                        "(sources in _build/java/I2)."))
exam_map(n, "I2", "The biggest topic of IJ Mam's part. Observer is asked in 2024-25, 2023-24 (22 marks), 2022-23, 2020-21, "
         "2017-18 and 2010-11; Strategy in 2020-21 (three parts) and 2018-19; Mediator in 2024-25, 2022-23 and 2019-20; "
         "Template + Strategy and State vs Strategy in 2024-25. Learn the five structures, then the "
         "comparison tables (Strategy vs Template, Mediator vs Observer, State vs Strategy) — they are "
         "asked directly.")

# ---------------------------------------------------------------- L5
n.lesson("Lesson 5 — Strategy", "Pages 4–48 (2 - BehavioralDesignPattern)")
n.p("Behavioral patterns deal with how objects behave and interact: communication, flow of responsibility and how tasks "
    "are carried out between objects (pp. 2–3).")
n.h2("1. SimUDuck (pp. 4–39)")
n.bullets([
    "Duck superclass with quack(), swim(), display(), and later fly() → RubberDuck inherits fly() and flies (p. 8).",
    "Override fly() to do nothing in RubberDuck, DecoyDuck … → every new duck must be checked (pp. 9–12).",
    "Flyable / Quackable interfaces → duplicated fly code in every class; a change touches all (pp. 13–18).",
    "Principle (p. 19): identify the aspects that vary and separate them from what stays the same.",
    "Duck **has** FlyBehavior and QuackBehavior (FlyWithWings, FlyNoWay; Quack, Squeak, MuteQuack); performFly() "
    "delegates; setFlyBehavior() changes it at run time — ModelDuck gets FlyRocketPowered (pp. 20–39).",
])
n.callout("memorize", "**Strategy** — Define a family of algorithms, encapsulate each one, and make them interchangeable. "
          "Strategy lets the algorithm vary independently from the clients that use it (p. 45).")
code(n, """Client --creates strategy--> Context - strategy: Strategy ---------> «interface» Strategy + execute(data)
                              + setStrategy(s)                          ^            ^
                              + doSomething() { strategy.execute(data); }  ConcreteStrategyA  ConcreteStrategyB""")
n.p("Navigator example (pp. 42–44): routeStrategy = Road / PublicTransport / Walking, each buildRoute(A, B). Payment "
    "(p. 47): Credit card vs PayPal.")
n.table(["Use Strategy when", "Not when"], [
    ["several variants of one algorithm/behaviour; choose or switch at run time",
     "the variants are steps of one fixed skeleton → Template Method"],
    ["a class has a big conditional choosing the behaviour", "behaviour depends on the object's own state and changes itself → State"],
], widths_cm=[8.6, 8.6], font_size=9)
n.practice("Lesson 5", "(a) Actual — 2018-19 Q2(a). (b) Actual — 2020-21 Q2(b). (c) Actual — 2020-21 Q2(a). (d) Actual — "
           "2020-21 Q2(c).", [
    "(a) Robots: interface IBehaviour, AggressiveBehaviour, DefensiveBehaviour, NormalBehaviour; Robot passes sensor data "
    "(position, close obstacles) to its behaviour; Big Robot is aggressive, George v.2.1 defensive, R2 normal; later the "
    "behaviours change. Class diagram + code. (20)",
    "(b) Three sorting routines (selection, insertion, quicksort): demonstrate Strategy. (10)",
    "(c) A web system shows mobile talk-time schemes and their cost; new schemes are added often. Decouple the UI "
    "programmers from the scheme classes. (10)",
    "(d) Student IDs with marks: find grades and prepare the merit list of the students with the highest grade, using a "
    "pattern; any grading scheme. (15)",
])
n.solution()
n.answer("(a)", "Strategy: Robot = context, Behaviour = strategy interface, three concrete behaviours; setBehaviour() "
         "switches at run time.")
code(n, """Robot - name, position, behaviour: Behaviour --------> «interface» Behaviour + moveCommand(name, pos, obstacle): int
  + setBehaviour(b)  + move(obstacleClose)                   ^ AggressiveBehaviour ^ DefensiveBehaviour ^ NormalBehaviour""")
java(n, "I2", "RobotSim.java")
n.answer("(b)", "Sorter (context) holds a SortStrategy; three concrete strategies.")
java(n, "I2", "SortStrategyDemo.java")
n.answer("(c)", "Strategy: every scheme implements TalkTimeScheme (name(), cost(minutes)); the UI page depends only on "
         "that interface and receives the list from a registry/factory. Adding a scheme = one new class + one registry "
         "line; the UI code never changes.")
java(n, "I2", "TalkTimeDemo.java")
n.answer("(d)", "Strategy for the grading scheme (BUET letter grades or pass/fail chosen at run time); ResultProcessor "
         "computes grades and the merit list (students with the top grade, sorted by marks).")
java(n, "I2", "MeritListDemo.java")

# ---------------------------------------------------------------- L6
n.lesson("Lesson 6 — Template Method", "Pages 49–81 (2 - BehavioralDesignPattern) · Misc pp. 3–4")
n.p("Coffee: boil water, brew coffee grinds, pour in cup, add sugar and milk. Tea: boil water, steep tea bag, pour in "
    "cup, add lemon. Same skeleton (pp. 49–63) → CaffeineBeverage.prepareRecipe() is **final**: boilWater(); brew(); "
    "pourInCup(); addCondiments(); — brew() and addCondiments() are abstract; Coffee and Tea implement them.")
n.p("Hook (p. 72): if (customerWantsCondiments()) addCondiments(); — customerWantsCondiments() returns true by default and "
    "subclasses may override it.")
n.callout("memorize", "**Template Method** defines the skeleton of an algorithm in the superclass but lets subclasses "
          "override specific steps of the algorithm without changing its structure (p. 73).")
code(n, """AbstractClass
 + templateMethod() {final}  { step1(); step2(); if (hook()) step3(); step4(); }
 # step1(), step4()          (implemented: common)
 # step2(), step3()          {abstract}
 # hook(): boolean           (default implementation, may be overridden)
        ^                         ^
 ConcreteClass1             ConcreteClass2   (override step2, step3, optionally hook)""")
n.p("Data mining (pp. 75–77): DocDataMiner, CSVDataMiner, PDFDataMiner repeat openFile, extractData, parseData, "
    "analyzeData, sendReport, closeFile → DataMiner.mine(path) template; format-specific steps abstract; analyzeData and "
    "sendReport shared.")
n.table(["", "Template Method", "Strategy"], [
    ["Based on", "inheritance — alter parts by extending them in subclasses", "composition — alter behaviour by supplying a different strategy object"],
    ["Level / time", "class level, static (fixed at compile time)", "object level, can switch at run time"],
    ["Controls", "superclass controls the order of steps", "context delegates the whole algorithm"],
], widths_cm=[2.6, 7.3, 7.3], font_size=9)
n.practice("Lesson 6", "(a) Actual — 2024-25 Q8(a).", [
    "(a) A DataParser reads data files in different formats (CSV, JSON …) through the same steps (open, extract, parse, "
    "analyse, report, close) but the analysis algorithm must be selectable. Redesign it using Template Method and "
    "Strategy together, in Java. (15)",
])
n.solution()
n.answer("(a)", "Template Method fixes the pipeline in a final process() method; format-specific steps (extractData, "
         "parseData) are abstract and implemented by CsvParser and JsonParser; wantsReport() is a hook. The analysis step "
         "varies independently of the format, so it is a Strategy object injected into the parser — any format can be "
         "combined with any analysis without new subclasses.")
code(n, """DataParser {abstract} - analysis: AnalysisStrategy -------> «interface» AnalysisStrategy + analyze(values)
 + process(raw) {final}  (template)                             ^ AverageAnalysis   ^ MaxAnalysis
 # openFile(), extractData(){abstract}, parseData(){abstract}, wantsReport() (hook), sendReport(), closeFile()
     ^ CsvParser    ^ JsonParser""")
java(n, "I2", "DataMinerDemo.java")

# ---------------------------------------------------------------- L7
n.lesson("Lesson 7 — Observer", "Pages 82–128 (2 - BehavioralDesignPattern)")
n.p("Weather-O-Rama (pp. 82–94): WeatherData has getTemperature(), getHumidity(), getPressure() and measurementsChanged(); "
    "three displays (current conditions, statistics, forecast) must update, and more may be added. Coding the displays "
    "into measurementsChanged() couples WeatherData to concrete classes. Newspaper subscription (pp. 95–107): publisher "
    "+ subscribers who can subscribe and unsubscribe.")
n.callout("memorize", "**Observer** — Define a one-to-many dependency between objects so that when one object changes "
          "state, all its dependents are notified and updated automatically (p. 121).")
code(n, """«interface» Subject                                «interface» Observer
 + registerObserver(o)  + removeObserver(o)          + update(temp, humidity, pressure)
 + notifyObservers()                                   ^            ^              ^
        ^                                      CurrentConditions  StatisticsDisplay  ForecastDisplay
   WeatherData - observers: List<Observer>     (each has display(); its constructor calls
   + measurementsChanged() { notifyObservers(); }  weatherData.registerObserver(this))""")
n.p("General form (p. 121–127): Publisher (subscribers[], mainState; subscribe(s), unsubscribe(s), notifySubscribers() { "
    "for each s: s.update(this) }) and «interface» Subscriber update(context). **Push** = subject sends the data in "
    "update(); **pull** = subject sends itself and observers read what they need. Observer = event listener (p. 128).")
n.practice("Lesson 7", "(a) Actual — 2023-24 Q2(a). (b) Actual — 2022-23 Q4(a) / 2017-18 Q8(b). (c) Actual — 2020-21 Q3(b). "
           "(d) Actual — 2024-25 Q8(b). (e) Actual — 2010-11 Q4(c).", [
    "(a) StockMarket: StockGrabber holds the prices; StockObserver objects must be updated when any price changes. "
    "(i) UML with the pattern (6) (ii) code StockGrabber and StockObserver (8×2).",
    "(b) BUET alumni register to a blog; when a new article is posted the blog notifies them; they then open the blog and "
    "read it. Class diagram + code. (15 / 5+12)",
    "(c) A dashboard shows the max and average temperature, updated at the end of each day. Pattern + design. (10)",
    "(d) Breaking-news items must appear on several displays (TV ticker, mobile app, website) as soon as they arrive. (10)",
    "(e) Facebook group: users join and leave; every wall post is broadcast to all members' news feeds. Pattern, class "
    "diagram and code fragments. (12)",
])
n.solution()
n.answer("(a)", "")
code(n, """«interface» Subject + register(o), unregister(o), notifyObservers()      «interface» Observer + update(ibm, aapl, goog)
        ^                                                                       ^
StockGrabber - observers: List<Observer>                                 StockObserver - id, stockGrabber: Subject
  - ibmPrice, aaplPrice, googPrice                                        + update(...)  (prints the prices)
  + setIBMPrice(p) / setAAPLPrice(p) / setGOOGPrice(p) -> notifyObservers()
StockObserver ----registers with----> StockGrabber (1 subject, 0..* observers)""", size=8)
java(n, "I2", "StockDemo.java")
n.answer("(b)", "Pull model: update(blog) tells the user that a new article is posted; the user then calls "
         "blog.getLatestArticle() — exactly 'then the user will access the blog and read'.")
java(n, "I2", "BlogDemo.java")
n.answer("(c)", "Observer: TemperatureLog (subject) collects readings and at endOfDay() pushes (max, avg) to every "
         "attached widget; new widgets just attach.")
java(n, "I2", "TempDashboard.java")
n.answer("(d)", "**Observer**: NewsAgency (subject) keeps a list of NewsDisplay observers (TvTicker, MobileApp, Website); "
         "publish(news) calls display.update(news) on each. Displays subscribe/unsubscribe at run time; the agency does "
         "not know their concrete classes. Same code shape as (a).")
n.answer("(e)", "**Observer**: Group = subject with join(user) = register, leave(user) = remove, postOnWall(msg) → "
         "notifyMembers() → user.update(group, msg) adds it to the user's news feed. Group also has title, admins, "
         "type (open/closed) and related groups. For groups inside groups see the Composite extension in the Structural "
         "notes (2010-11 Q4(d)).")

# ---------------------------------------------------------------- L8
n.lesson("Lesson 8 — Mediator", "Pages 129–167 (2 - BehavioralDesignPattern)")
n.p("Air-traffic control (p. 129): pilots do not talk to each other; all communication goes through the tower. Customer "
    "profile dialog (pp. 131–150): checkboxes, text fields and buttons that react to each other create a web of "
    "dependencies; instead the Dialog is the mediator — components only notify it.")
n.callout("memorize", "**Mediator** restricts direct communications between objects and forces them to collaborate only "
          "via a mediator object; it reduces chaotic dependencies (p. 157).")
code(n, """ComponentA - m: Mediator   ComponentB - m: Mediator  ...   (each calls m.notify(this, event))
        \\                     |                      /
         +--------> «interface» Mediator + notify(sender, event) <-------+
                              ^
                   ConcreteMediator - componentA, componentB, ...
                   + notify(sender, event) { if (sender == componentA) reactOnA(); ... }""")
n.table(["", "Mediator", "Observer"], [
    ["Goal", "eliminate mutual dependencies among a set of components; all depend on one mediator",
     "establish dynamic one-way connections: subscribers follow a publisher"],
    ["Direction", "many ↔ one ↔ many (two-way coordination logic in the mediator)", "one → many notifications"],
    ["Note", "a mediator is often implemented with observer-style notify()", "observers can come and go at run time"],
], widths_cm=[2.4, 7.4, 7.4], font_size=9)
n.practice("Lesson 8", "(a) Actual — 2022-23 Q2(a). (b) Actual — 2019-20 Q1(b). (c) Actual — 2024-25 Q5(b)(i).", [
    "(a) ATC coordinates landing and take-off; flights must not depend on each other. Class diagram + code. (15)",
    "(b) Three servers sort with selection, insertion and quicksort; a central broker receives (algorithm, data), forwards "
    "to the right server, returns the sorted array, and queues requests that arrive together. Demonstrate Mediator. (20)",
    "(c) A Smart Home Hub coordinates motion sensors, lights, alarms and other devices. A motion event may trigger one or "
    "more coordinated actions (light on, alarm, notify the hub): show why Mediator is preferable to letting the motion "
    "sensor talk to the devices directly. (Part (ii) of this question — record/queue/replay — needs Command, which is not "
    "in this term's syllabus.)",
])
n.solution()
code(n, """«interface» ATCMediator + register(f), requestLanding(f): boolean, landed(f)
        ^ ControlTower - flights: List<Flight> - runwayFree: boolean
Flight - id - atc: ATCMediator + land() + receive(msg)       Flight 0..* ---- 1 ControlTower""")
java(n, "I2", "AtcDemo.java")
n.answer("(b)", "CentralBroker is the concrete mediator; clients and servers are colleagues that never reference each "
         "other. A FIFO queue holds simultaneous requests.")
code(n, """Client - broker: Broker + requestSort(alg, data) + receive(sorted)
«interface» Broker + submit(client, alg, data) + processAll()
   ^ CentralBroker - servers: Map<String, SortServer> - queue: Queue<Request>
SortServer {abstract} + algorithm() + sort(a)   ^ SelectionServer ^ InsertionServer ^ QuickServer""")
java(n, "I2", "SortBroker.java")
n.answer("(c)", "Direct links: MotionSensor would hold references to Light, Alarm, Notifier and contain the rules → "
         "N sensors × M devices dependencies; adding a device or changing a rule edits every sensor. With **Mediator** the "
         "sensor only calls hub.notify(this, \"motion\"); the hub owns the coordination rules, devices and sensors stay "
         "independent and reusable, and rules change in one place.")
java(n, "I2", "SmartHomeDemo.java")

# ---------------------------------------------------------------- L9
n.lesson("Lesson 9 — State (and State vs Strategy)", "Pages 203–260 (2 - BehavioralDesignPattern)")
n.p("Mighty Gumball (pp. 203–216): states No Quarter, Has Quarter, Gumball Sold, Out of Gumballs; actions insertQuarter, "
    "ejectQuarter, turnCrank, dispense. Coding it with int constants and an if-else on the state in every action works, "
    "but the new 'winner' rule (10 % of the time two gumballs) forces changes in every method — the nightmare of change.")
n.p("New design (pp. 217–240): a State interface with the four actions; one class per state (NoQuarterState, "
    "HasQuarterState, SoldState, SoldOutState, WinnerState); GumballMachine holds the state objects and the current state "
    "and delegates every action to it; states call machine.setState(next).")
n.callout("memorize", "**State** — Allow an object to alter its behavior when its internal state changes. The object will "
          "appear to change its class (p. 241).")
code(n, """Context - state: State                         «interface» State + doThis() + doThat()
 + Context(initialState)                               ^                    ^
 + changeState(s) { state = s; }                ConcreteStateA        ConcreteStateB
 + doThis() { state.doThis(); }                 - context: Context    (may call context.changeState(new B()))""")
java(n, "I2", "GumballDemo.java")
n.p("Document example (pp. 252–253): publish() behaves differently in Draft (→ Moderation, or Published if admin), "
    "Moderation (→ Published if approved) and Published (do nothing).")
n.table(["", "State", "Strategy"], [
    ["Common", "both use composition and delegate to a helper object ('twins separated at birth', p. 254)", ""],
    ["Who changes the helper", "the context or the **states themselves**, as a result of actions", "the **client** chooses/sets it"],
    ["Knowledge", "states may know each other and the context", "strategies are independent and unaware of each other"],
    ["Models", "behaviour that depends on the object's current state (life cycle)", "interchangeable algorithms for one task"],
    ["Example", "gumball machine, document workflow, TCP connection", "sorting algorithms, payment methods, routes"],
], widths_cm=[3.6, 6.8, 6.8], font_size=9)
n.practice("Lesson 9", "(a) Actual — 2024-25 Q8(c).", ["(a) State vs Strategy. (10)"])
n.solution()
n.answer("(a)", "The comparison table above with one diagram each (Context → State with transitions between "
         "ConcreteStates; Context → Strategy set by the client) and the gumball vs sorting examples.")

# ---------------------------------------------------------------- L10
n.lesson("Lesson 10 — Identifying the Pattern", "Mixed TF questions")
n.p("Read the scenario for cue words: 'subscribe / notify when X changes' → Observer; 'choose or switch an algorithm at "
    "run time' → Strategy; 'fixed steps, some vary' → Template Method; 'objects must not talk directly, go through a hub' "
    "→ Mediator; 'behaviour depends on the current state, which changes itself' → State. Name the pattern, justify it in "
    "one or two lines, then draw the minimal UML.")
n.practice("Lesson 10", "(b) Actual — 2021-22 Q4(a).", [
    "(b) Identify the most specific pattern: (i) NuetFlix recommends a newly released movie to users interested in its "
    "genre (Horror, Thriller, Comedy) (ii) jit: kommit / pussh / stashh (iii) BanglaPhone switches between a stable-but-slow "
    "and a fast-but-unstable implementation depending on the number of users under a cell tower, without affecting other "
    "code (iv) R2-D2 journal: authors and reviewers communicate only through an internal team, never knowing each "
    "other's identity. (20)",
])
n.solution()
n.answer("(b)", "")
n.table(["Case", "Pattern", "Justification"], [
    ["(i) NuetFlix", "Observer", "users subscribe to genres (one subject per genre); a release notifies all subscribers of that genre"],
    ["(ii) jit", "Command (not in this term's syllabus)", "each operation would be an object with execute() acting on the repository; name the pattern only"],
    ["(iii) BanglaPhone", "Strategy (State also accepted)", "two interchangeable implementations of the same service selected at run "
     "time by user count; context code unchanged. If the switch is driven internally by the tower's load as a life-cycle, "
     "call it State — justify either"],
    ["(iv) R2-D2", "Mediator", "authors and reviewers never reference each other; the committee's internal team routes all "
     "submissions, reviews and decisions, hiding identities"],
], widths_cm=[2.8, 3.6, 10.8], font_size=9)
code(n, """(i)  Genre (Subject) + subscribe(u), unsubscribe(u), release(movie) -> for u: u.recommend(movie)
     User (Observer) + recommend(movie)          (a user may subscribe to Horror, Thriller and/or Comedy)
(iv) «interface» JournalMediator + submit(author, paper), review(reviewer, paperId, comments), decide(...)
     EditorialTeam (ConcreteMediator) — Author and Reviewer hold only the mediator""", size=8)

n.quick_notes("Quick Notes — Behavioral Patterns", "Revision points for Lessons 5–10.", [
    ("L5 · Strategy", ["Context has-a Strategy; setStrategy() at run time. Ducks, robots, sorting, schemes, grading."]),
    ("L6 · Template Method", ["final templateMethod() calls steps; abstract steps + hooks. Inheritance vs Strategy's composition."]),
    ("L7 · Observer", ["Subject register/remove/notify; Observer update(). Push vs pull. Stock, blog, dashboard, news, groups."]),
    ("L8 · Mediator", ["Colleagues call mediator.notify(this, event). ATC, dialog, sort broker. vs Observer: mutual vs one-way."]),
    ("L9 · State", ["Context delegates to current State; states switch themselves. Gumball. vs Strategy: who changes it."]),
    ("L10 · Identify", ["Cue words → pattern: subscribe/notify = Observer, swap algorithm = Strategy, via a hub = Mediator, behaviour changes with state = State."]),
])
print(n.save())
