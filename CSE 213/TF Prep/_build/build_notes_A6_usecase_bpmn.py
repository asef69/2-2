"""Anindya 6 — Use case diagrams (Use case.pptx) + BPMN (3 - BPMN.pptx) → Lessons 19–22."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import new, exam_map, src_note, code, SCR  # noqa: E402

UC = os.path.join(SCR, "pp_Use_case.pdf")
BP = os.path.join(SCR, "pp_3_-_BPMN.pdf")
n = new("Anindya", "Use Case Diagrams and BPMN Process Models", "CSE213_Anindya_UseCase_BPMN_Notes.docx")
n.front_matter([
    ("Exam Map — What the TF Papers Ask", "use-case and UML-overview questions; BPMN = insurance"),
    ("Lesson 19 — UML Overview, Actors, Use Cases and Their Relationships", "Use case.pptx sl. 1–16"),
    ("Lesson 20 — Worked Use Case Diagrams and Use Case Narratives", "TF scenarios: Mentcare, bank, hotel, rent-a-car …"),
    ("Lesson 21 — BPMN Core: Events, Activities, Gateways", "3 - BPMN.pptx sl. 1–20"),
    ("Lesson 22 — BPMN Pools, Lanes, Message Flows and Artifacts", "3 - BPMN.pptx sl. 21–34"),
    ("Quick Notes — Use Cases and BPMN", "revision + key diagrams"),
], source_note=src_note("Lessons 19–20: 'Use case.pptx' (16 slides). Lessons 21–22: '3 - BPMN.pptx' (34 slides). "
                        "Figures are taken from PDF copies of the pptx decks made with PowerPoint; slide numbers are the "
                        "pptx slide numbers. Diagrams in solutions are written as text: actor —— (use case), "
                        "(A) ··«include»··> (B), and for BPMN ○ start, ◎ end, [task], <X> XOR, <+> AND, <O> OR."))
exam_map(n, "A6", "Use case diagrams: 2023-24 Q1(a) (Mentcare, ★★★) and five older papers; use case narratives: "
         "2016-17, 2013-14, 2011-12. UML overview questions (diagram types, kinds of things, extensibility) are 5–12 marks "
         "in older papers. BPMN has not been asked yet — it is new in this syllabus, so treat Lessons 21–22 as insurance and "
         "learn the gateway rules (a 10-mark 'model this process in BPMN' is the likely form).")

n.lesson("Lesson 19 — UML Overview, Actors, Use Cases and Their Relationships", "Slides 1–16 (Use case.pptx)")
n.h2("1. UML (sl. 1–2)")
n.p("UML = Unified Modeling Language: an international industry-standard graphical notation for describing software "
    "analysis and design — pictures (views) of an OO system. Diagrams listed: use case, class, sequence, collaboration, "
    "statechart, object, activity, component, deployment.")
n.table(["Static (structure)", "Dynamic (behaviour)"], [
    ["Class, Object, Component, Deployment, Package, Composite structure", "Use case, Activity, State machine (statechart), "
     "Sequence, Communication (collaboration), Timing, Interaction overview"],
], widths_cm=[8.6, 8.6])
n.callout("note", "Textbook background for older questions. **Four kinds of things in UML:** structural things (class, "
          "interface, use case, component, node), behavioural things (interaction, state machine), grouping things "
          "(package), annotational things (note). **Extensibility mechanisms:** stereotypes («entity», «include»), tagged "
          "values ({version = 2.1}) and constraints ({ordered}, {balance ≥ 0}). **Behavioural diagrams:** use case "
          "(functions from the user's view), activity (workflow), state machine (life of one object), and the interaction "
          "diagrams sequence / communication / timing / interaction overview (message exchange).")
n.h2("2. Use cases, actors, stakeholders (sl. 3–7)")
n.bullets([
    "A use case is a sequence of actions a system performs that yields a valuable result for a particular actor — a "
    "scenario-based description of how the system interacts with its environment.",
    "**Actor:** anything with behaviour outside the system that acts on it — a human role, a hardware device, an external "
    "system, or time. Drawn as a stick figure with its name. A single actor may represent many people.",
    "**Primary actor** initiates the interaction to achieve a goal; **supporting actor** performs sub-goals; a "
    "**stakeholder** is anyone interested in the system and may never act in a scenario.",
    "Finding actors (sl. 5): who is interested, where is it used, who benefits, who supplies/uses/removes information, does "
    "one person play several roles (one actor per role), do several people play the same role (one actor).",
])
n.h2("3. Diagram elements and relationships (sl. 8–15)")
n.table(["Element", "Notation", "Rule / example"], [
    ["Use case", "ellipse with a verb–noun name", "one function, may contain several scenarios (paths): Make appointment"],
    ["Association", "plain line (or double-headed arrow) actor — use case", "communication; Patient — Make appointment"],
    ["System boundary", "rectangle around the use cases, actors outside", "defines scope; may be one module of an ERP"],
    ["Generalisation", "line with hollow triangle from child to parent", "New Patient, Old Patient → Patient; Make new/old patient appt → Make appointment"],
    ["«extend»", "dashed arrow **from the extension to the base**", "optional behaviour: Update patient information ··> Make appointment"],
    ["«include»", "dashed arrow **from the base to the included** use case", "mandatory reused behaviour: Manage schedule ··> Record availability"],
], widths_cm=[3.0, 6.4, 7.8], font_size=9)
n.figure_from_pdf(UC, 15, "Figure 19.1 — Appointment system with generalisation, include and extend (sl. 15)",
                  clip=(0, 0.12, 1, 0.98), width_cm=12)
n.callout("trap", "Directions: «include» points to the use case that is always executed as part of the base; «extend» "
          "points to the base it may optionally extend. (Slide 14's picture draws the include arrow from Record availability "
          "to Manage schedule; slide 14's text and standard UML say base → included. Follow the text and say so.) Old "
          "papers call «include» 'uses'.")
n.practice("Lesson 19", "(a) Actual — 2013-14 Q1(c). (b) Actual — 2014-15 Q5(c). (c) Actual — 2013-14 Q5(b) / 2012-13 "
           "Q7(d). (d) Actual — 2016-17 Q1(a). (e) Actual — 2010-11 Q1(b).", [
    "(a) Define extends and uses relationships in use case diagrams with real-life examples. (7⅔)",
    "(b) What types of UML diagrams exist? Name each, give its purpose, classify as static or dynamic. (10)",
    "(c) What are the (four) kinds of things in UML? (12 / 4⅔)",
    "(d) Discuss some extensibility mechanisms of UML. (12)",
    "(e) List all behavioral UML diagrams and describe the purpose of each. (8)",
])
n.solution()
n.answer("(a)", "«extend» (extends): optional or conditional behaviour inserted into a base use case at an extension point; "
         "the base is complete without it; arrow from extension to base. Example (ATM): (Print receipt) ··«extend»··> "
         "(Withdraw cash) — only if the customer asks. «include» (uses): behaviour common to several use cases factored out "
         "and always executed; arrow from base to included. Example: (Withdraw cash) ··«include»··> (Authenticate user) and "
         "(Transfer funds) ··«include»··> (Authenticate user).")
n.answer("(b)", "Table in §1 plus one-line purpose each: class — static structure; object — snapshot of instances; "
         "component — physical modules; deployment — hardware nodes and artifacts; package — grouping; use case — "
         "functionality from the users' view; activity — workflow/business process; state machine — life cycle of one "
         "object; sequence — time-ordered messages; communication — messages over links; timing — state changes over time.")
n.answer("(c)", "Structural, behavioural, grouping, annotational things (NOTE above), each with two examples.")
n.answer("(d)", "Stereotypes — new model element kinds derived from existing ones, shown «name» or with an icon "
         "(«interface», «entity», «include»); tagged values — name=value properties attached to elements ({author = Rahim}, "
         "{version = 1.2}); constraints — conditions in braces, possibly in OCL ({ordered}, {ward.gender = patient.gender}). "
         "Profiles bundle them for a domain.")
n.answer("(e)", "Use case, activity, state machine, sequence, communication (collaboration), timing, interaction overview "
         "— purpose of each as in (b).")

n.lesson("Lesson 20 — Worked Use Case Diagrams and Use Case Narratives", "TF scenarios (method from Use case.pptx sl. 3–15)")
n.h2("1. Use case narrative (textbook format — needed for 2016-17, 2013-14, 2011-12)")
n.table(["Section", "Content"], [
    ["Use case name / ID", "verb–noun name"], ["Primary actor, stakeholders", "who initiates; who cares"],
    ["Preconditions", "must be true before it starts"], ["Trigger", "event that starts it"],
    ["Main success scenario", "numbered actor / system steps"], ["Extensions (alternate flows)", "2a, 4a … with the step they branch from"],
    ["Postconditions (success guarantee)", "true after success"], ["Special requirements, frequency, open issues", "non-functional notes"],
], widths_cm=[5.2, 12.0])
n.practice("Lesson 20", "(a) Actual — 2023-24 Q1(a). (b) Actual — 2016-17 Q2(a)–(b). (c) Actual — 2011-12 Q2(a). "
           "(d) Actual — 2012-13 Q8(a). (e) Actual — 2013-14 Q6(d). (f) Actual — 2014-15 Q6(d) / 2010-11 Q2(c). "
           "(g) Actual — 2013-14 Q1(d).", [
    "(a) Mentcare: clinic staff log on with username and password (≥ 8 letters, no other checks); a receptionist may transfer "
    "data to the national PRS. A criminal poses as a relative, learns nurses' names from badges and family details, and "
    "guesses passwords. Draw a use case diagram showing the processes through which the criminal can gain access. (7)",
    "(b) Bank with Normal and Foreign users (create account, deposit, withdraw with limits, update balance, bonus, interest, "
    "convert currency): (i) use case diagram (13) (ii) narrative for 'Withdraw money' (7⅔).",
    "(c) ABC Car Rentals: write the narrative for 'Rent a Car'. (18⅔)",
    "(d) Northeast Hotel: reservation (registered or new customer), unique reservation code, amend/cancel, check-in by "
    "receptionist, check-out with card payment validation, optional printed invoice, room types, monthly reports for the "
    "manager. (i) System use case diagram (ii) use case dependency diagram. (15+5)",
    "(e) Online bus reservation (buses, trips normal/express, seats, pay online or not, cancellation, authentication of "
    "customers and staff). Use case diagram. (22)",
    "(f) A book is written by an author, published by a publisher, sold by a book store and read by a reader, who must buy "
    "it from a store selling it. Use case diagram with relationships. (9⅔ / 8)",
    "(g) A bank teller serves students depositing exam fees in a queue: show the extended version of the use case. (15)",
])
n.solution()
n.answer("(a)", "Misuse-case style: the criminal is an extra (hostile) actor; the processes he exploits are the normal log-on "
         "path plus the social-engineering steps outside the system.")
code(n, """                    +--------------------------- Mentcare system ---------------------------+
 Clinic staff ------|---- (Log on) ··«include»··> (Validate username/password)               |
 (nurse, doctor)    |---- (View / update patient record)  ··«include»··> (Log on)              |
 Receptionist ------|---- (Transfer data to PRS) ··«include»··> (Log on)                     |
                    |          ··«extend»·· (Send personal info) , (Send diagnosis summary)    |
 Criminal ----------|---- (Guess password)  ··«extend»··> (Log on)                           |
   (misuser)        |---- (Access patient record illegally) ··«include»··> (Log on)          |
                    +-----------------------------------------------------------------------+
 Outside the system: Criminal -- (Pose as relative) -- (Collect nurses' names & family info)
                               ··leads to··> (Guess password)              PRS -------- national DB (external actor)""", size=8)
n.p("Engagement points: (1) collecting names (badges, talking to nurses) — social engineering; (2) Log on with guessed "
    "passwords — weak policy (only length ≥ 8, no lockout); (3) once logged on, View patient record and Transfer data to PRS "
    "expose the star's diagnosis.")
n.answer("(b)(i)", "")
code(n, """                 +------------------------------ Bank System ------------------------------+
 User <|-- Normal|  (Create account)      (Deposit money) ··«include»··> (Update balance)          |
 User <|-- Foreign  (Withdraw money) ··«include»··> (Update balance)                              |
                 |  (Deposit money) <··«extend»·· (Calculate bonus)   [balance >= 20,00,000]       |
 User -----------|- Create account, Deposit money, Withdraw money                                  |
 Foreign user ---|- (Convert to foreign currency)                                                  |
 Time (actor) ---|- (Calculate interest) ··«include»··> (Update balance)   [every 3 months]         |
                 +------------------------------------------------------------------------------+""", size=8)
n.answer("(b)(ii)", "Narrative — Withdraw money")
n.table(["Field", "Content"], [
    ["Primary actor", "User (normal or foreign)"], ["Precondition", "User has an account and is authenticated"],
    ["Main flow", "1 User requests withdrawal and enters amount. 2 System checks amount ≤ 1,00,000. 3 System checks today's "
     "total + amount ≤ 3,00,000 and withdrawals today < 5. 4 System checks balance ≥ amount. 5 System debits the account "
     "(Update balance), increments today's count and total. 6 System dispenses money and shows the new balance."],
    ["Alternate flows", "2a amount > 1,00,000: reject, ask for a smaller amount. 3a daily amount or count exceeded: reject, "
     "end. 4a insufficient balance: reject, end."],
    ["Postcondition", "Balance reduced by amount; daily counters updated; transaction logged"],
], widths_cm=[3.4, 13.8], font_size=9)
n.answer("(c)", "Narrative — Rent a Car")
n.table(["Field", "Content"], [
    ["Primary actor / others", "Customer (at the office); supporting actor: Employee (operates the system)"],
    ["Precondition", "Customer is at the office; employee logged in"],
    ["Main flow", "1 Customer gives time and duration. 2 Employee checks the system; system shows available car models. "
     "3 Customer chooses a model. 4 System confirms availability for that time. 5 Employee asks for national ID and other "
     "information and enters it. 6 System books the specific car for the period. 7 Employee states rental cost and asks "
     "for 50 % advance. 8 Customer pays; system records payment and confirms the booking."],
    ["Alternate flows", "4a model not available: system reports it; continue at step 3. 8a customer cannot pay the "
     "advance: booking cancelled, car released; use case ends."],
    ["Postcondition", "Car booked for the period, customer recorded, advance received"],
], widths_cm=[3.4, 13.8], font_size=9)
n.answer("(d)", "")
code(n, """                 +---------------------------- Hotel Reservation System ----------------------------+
 Guest ----------|-- (Make reservation) ··«include»··> (Generate reservation code)                 |
                 |      <··«extend»·· (Register new customer)   [not registered]                    |
 Guest ----------|-- (Amend reservation)  ··«include»··> (Find reservation by code)               |
 Guest ----------|-- (Cancel reservation) ··«include»··> (Find reservation by code)               |
 Receptionist ---|-- (Check in)  ··«include»··> (Find reservation by code)                        |
 Receptionist ---|-- (Check out) ··«include»··> (Validate payment) ------------- Card Payment System|
                 |      <··«extend»·· (Print invoice)   [guest requests]                            |
 Hotel Manager --|-- (View monthly report)        Time ---- (Prepare monthly report)               |
                 +--------------------------------------------------------------------------------+
Use case DEPENDENCY diagram (order in which use cases must happen):
 Register customer --> Make reservation --> {Amend reservation | Cancel reservation} --> Check in --> Check out
 Check out --> Prepare monthly report --> View monthly report""", size=8)
n.answer("(e)", "")
code(n, """                 +------------------------------ Bus Reservation System ------------------------------+
 Customer -------|-- (Search trips)   (Reserve seat) ··«include»··> (Authenticate)                    |
                 |   (Reserve seat) <··«extend»·· (Pay online)    [then seat cannot be cancelled]      |
                 |   (Cancel unpaid reservation) ··«include»··> (Authenticate)                       |
 Staff ----------|-- (Manage buses)  (Manage schedules & trips)  (Assign driver and hostess)          |
                 |   (Cancel no-show seats) [unpaid, 1 hour before trip] ··«include»··> (Authenticate) |
                 |   (Sell freed seat)                                                                |
 Trip <|-- Normal trip, Express trip  (generalised use cases: Plan normal trip / Plan express trip)    |
 Time -----------|-- (Release unpaid seats 1 h before departure)                                     |
 Payment gateway --- (Pay online)                                                                    |
                 +------------------------------------------------------------------------------------+""", size=8)
n.answer("(f)", "System boundary = book trade; four actors.")
code(n, """ Author ---- (Write book)          Publisher ---- (Publish book) ---- Author
 Book store ---- (Sell book) ---- Reader          Reader ---- (Read book)
 (Read book) ··«include»··> (Buy book)    (Buy book) ··«include»··> (Sell book)   [only from a store selling it]
 (Sell book) ··«include»··> (Publish book)        (Publish book) ··«include»··> (Write book)""")
n.answer("(g)", "Extended use case = base use case plus its «include»/«extend» refinements.")
code(n, """ Student ---- (Deposit exam fee) ---- Teller
 (Deposit exam fee) ··«include»··> (Join queue / take token)
 (Deposit exam fee) ··«include»··> (Verify student ID and fee amount)
 (Deposit exam fee) ··«include»··> (Receive cash & issue receipt)
 (Pay late fine) ··«extend»··> (Deposit exam fee)        [after deadline]
 (Reject deposit) ··«extend»··> (Deposit exam fee)       [ID invalid / wrong amount]""")

n.lesson("Lesson 21 — BPMN Core: Events, Activities, Gateways", "Slides 1–20 (3 - BPMN.pptx)")
n.h2("1. Core elements (sl. 1, 8)")
n.table(["Element", "Symbol", "Meaning"], [
    ["Activity (task)", "rounded rectangle", "work done: verb + noun ('Check stock availability')"],
    ["Start event", "thin circle ○", "trigger; creates a token (token source)"],
    ["End event", "thick circle ◎", "outcome; consumes the token (token sink)"],
    ["Gateway", "diamond ◇", "split or join of the flow"],
    ["Sequence flow", "solid arrow", "order of activities"],
], widths_cm=[3.4, 4.2, 9.6])
n.h2("2. Worked example — order-to-cash (sl. 2–7, 13)")
n.p("Narrative: triggered by receipt of a purchase order; check stock; confirm or reject; if confirmed, emit invoice and "
    "ship goods; finish by archiving the order (or when rejected).")
code(n, """○ Purchase order received -> [Check stock availability] -> <X>
     <X> [items not in stock] -> [Reject order] -> ◎ Order rejected
     <X> [items in stock]     -> [Confirm order] -> <+> -> [Emit invoice] ---> <+> -> [Archive order] -> ◎ Order fulfilled
                                                  <+> -> [Ship goods]  ---> <+>""")
n.figure_from_pdf(BP, 13, "Figure 21.1 — Revised order-to-cash model with XOR and AND gateways (sl. 13)", clip=(0, 0.15, 0.96, 0.97), width_cm=13)
n.h2("3. Gateways (sl. 9–18)")
n.table(["Gateway", "Split", "Join", "Example"], [
    ["XOR ◇ with ×", "takes exactly one branch (labelled conditions; optional default flow)", "proceeds when one incoming branch completes",
     "invoice checking: post / re-send / block (sl. 10)"],
    ["AND ◇ with +", "takes all branches (parallel)", "waits for all incoming branches", "airport: security screening ‖ luggage screening (sl. 12)"],
    ["OR ◇ with ○", "takes one or more branches by condition", "waits for all **active** branches",
     "order distribution: Amsterdam and/or Hamburg (sl. 17–18)"],
], widths_cm=[2.6, 5.4, 4.0, 5.2], font_size=8.5)
n.p("Order distribution without OR (sl. 14–16): Solution 1 = XOR with three branches (only Amsterdam, only Hamburg, both → "
    "AND split/join); Solution 2 = AND split with an XOR 'skip' on each branch. The OR gateway (sl. 18) expresses it in one "
    "split/join pair.")
n.callout("trap", "Beginner's mistake (sl. 19): pairing an XOR split with an AND join deadlocks — the AND join waits forever "
          "for the branch that was not taken. Also, two activities on parallel branches need not run at the same time; "
          "they are only independent.")
n.h2("4. Naming guidelines (sl. 20)")
n.numbered(["Name every event and task.", "Task = verb + business object (+ complement): Issue driver licence.",
            "Message event = object + past participle: Invoice received, Claim settled.",
            "Avoid generic verbs: Handle, Record …", "Label every XOR-split branch with a condition: Policy is invalid."])

n.lesson("Lesson 22 — BPMN Pools, Lanes, Message Flows and Artifacts", "Slides 21–34 (3 - BPMN.pptx)")
n.bullets([
    "**Pool** (sl. 21): a resource class — usually a business party (a whole company). **Lane**: a sub-class inside a pool — "
    "department (Sales, Warehouse), role (Manager), or software system (ERP). Lanes can be nested.",
    "**Message flow** (sl. 23): dashed line with open arrowhead between pools; to the pool boundary = informative message, "
    "to an activity/event = message that triggers it.",
    "**Syntactic rules** (sl. 25): sequence flow cannot cross pool boundaries (message flow can); both may cross lanes; a "
    "message flow cannot connect two elements in the same pool.",
    "**Data object** (sl. 28): artifact required or produced by an activity, with state in brackets (Purchase order "
    "[approved]). **Data store**: persistent storage (Warehouse DB, Orders DB). **Text annotation** (sl. 29): open bracket "
    "joined by a dotted line; does not affect token flow.",
])
n.figure_from_pdf(BP, 24, "Figure 22.1 — Order-to-cash with lanes and a black-box Customer pool (sl. 24)", clip=(0, 0.12, 0.96, 0.98), width_cm=14)
n.practice("Lesson 22", "(a) Constructed (likely TF form). (b) Constructed.", [
    "(a) Model in BPMN: a student submits an online course-drop request; the advisor reviews it; if rejected the student is "
    "notified; if approved, the accounts office computes the refund while the registrar updates the record, then the "
    "student is notified. Use pools/lanes and gateways.",
    "(b) Why must an XOR-split not be closed by an AND-join? Give the fix.",
])
n.solution()
code(n, """Pool Student (black box)  ··drop request··> Pool University
Pool University, lanes: Advisor | Accounts | Registrar | System
 Advisor:   ○ Drop request received -> [Review drop request] -> <X>
            <X> [request rejected] -> [Notify rejection] -> ◎ Request rejected   ··rejection··> Student pool
            <X> [request approved] -> <+>
 Accounts:  <+> -> [Compute refund] ------------> <+>
 Registrar: <+> -> [Update academic record] ----> <+>
 System:    <+> (join) -> [Notify student of drop] -> ◎ Course dropped          ··confirmation··> Student pool
 Data: Drop request [submitted] -> Review ; Student record (data store) <- Update academic record""", size=8)
n.answer("(b)", "The XOR split passes the token to only one branch; an AND join waits for a token on every incoming branch, "
         "so it never fires — deadlock. Close an XOR split with an XOR join (or use AND split + AND join if both branches "
         "must run).")

import ai_diagram  # noqa: E402
ai_diagram.section(n, "A6", code)

n.quick_notes("Quick Notes — Use Cases and BPMN", "Revision points for Lessons 19–22.", [
    ("L19 · Use case basics", [
        "Actor = role outside the system (human, device, system, time); stakeholder may never act.",
        "Association line; boundary box; generalisation ▷; «include» base → included (always); «extend» extension → base (optional).",
        "UML things: structural, behavioural, grouping, annotational; extensibility: stereotypes, tagged values, constraints.",
    ]),
    ("L20 · Worked", [
        "Narrative: actor, precondition, main flow, alternate flows (2a…), postcondition.",
        "Mentcare: criminal as misuser actor; Guess password extends Log on.",
    ]),
    ("L21 · BPMN core", [
        "○ start, ◎ end, rounded task, ◇ gateway, arrow sequence flow.",
        "XOR = one branch; AND = all; OR = some, join waits for active ones. XOR split + AND join = deadlock.",
    ]),
    ("L22 · Pools", [
        "Pool = party; lane = department/role/system; message flow only between pools.",
        "Data object [state], data store, annotation.",
    ]),
], diagrams=[(UC, 15, "Use case diagram with relationships (sl. 15)", (0, 0.12, 1, 0.98), 11),
             (BP, 18, "OR gateway solution (sl. 18)", (0, 0.15, 1, 0.97), 11)])
print(n.save())
