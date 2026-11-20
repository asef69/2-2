"""paper.py - the mock question paper, v2: layout, mark split and question types copied from the 2023-24 and 2022-23 term finals."""
from pdfkit import *  # noqa: F401,F403

Q3B = """ 1  double averageOfPositives(int[] a) {
 2      if (a == null || a.length == 0)
 3          return -1;
 4      int sum = 0, count = 0;
 5      for (int i = 0; i < a.length; i++) {
 6          if (a[i] > 0) {
 7              sum += a[i];
 8              count++;
 9          }
10      }
11      if (count == 0)
12          return 0;
13      return (double) sum / count;
14  }"""

Q4B = """1  int rate(int age, int years) {
2      int r = 5;
3      if (age > 60 || years >= 10)
4          r = r + 3;
5      if (age < 18 && years > 0)
6          r = r - 2;
7      return r;
8  }"""

Q8_1 = """if (applicant.getAge() >= 18 && applicant.getAge() <= 60
        && (applicant.getMonthlyIncome() > 30000 || applicant.hasGuarantor())
        && !applicant.isBlacklisted()) {
    approve(applicant);
}"""

Q8_2 = """class Employee {
    static final int ENGINEER = 0, MANAGER = 1, INTERN = 2;
    int type;
    double salary;

    double getBonus() {
        switch (type) {
            case ENGINEER: return salary * 0.10;
            case MANAGER:  return salary * 0.20 + 5000;
            case INTERN:   return 0;
            default: throw new IllegalArgumentException("bad type");
        }
    }
}"""

Q8_3 = """double deliveryCharge(Order o) {
    double result;
    if (o.isCancelled()) {
        result = 0;
    } else {
        if (o.isPickup()) {
            result = 0;
        } else {
            if (o.total() >= 1000) {
                result = 30;
            } else {
                result = 60;
            }
        }
    }
    return result;
}"""


def story(fw):
    s = []
    A = lambda *a: s.append(part(*a, fw))  # noqa: E731

    # ---------------------------------------------------------------- cover
    s += [P("MOCK TERM FINAL EXAMINATION", "title"), P("CSE 213 &nbsp;•&nbsp; Software Engineering", "sub"),
          P("Full marks: 210 &nbsp;•&nbsp; Time: 3 hours &nbsp;•&nbsp; Practice paper (not a real past paper)", "sub"),
          P("Laid out like the 2023-24 and 2022-23 term finals: same sections, same marks per question, same kinds of parts.", "small"),
          Spacer(1, 4)]
    s.append(P("Instructions", "h2"))
    s.append(table([
        ["<b>#</b>", "<b>Rule</b>"],
        ["1", "There are <b>8 questions</b> in two sections, A (Q1–Q4) and B (Q5–Q8). Marks for each part are printed in square brackets."],
        ["2", "<b>Section A:</b> Question 1 (45 marks) is <b>compulsory</b>; answer <b>any two</b> of Questions 2, 3 and 4 (30 marks each). Section total 105."],
        ["3", "<b>Section B:</b> Question 5 (35 marks) is <b>compulsory</b>; answer <b>any two</b> of Questions 6, 7 and 8 (35 marks each). Section total 105."],
        ["4", "Draw diagrams neatly and label every class, state, actor and message. Java code may be written in outline"
              " but must be logically correct (types, constructors, method signatures)."],
        ["5", "Show every step of a calculation. Sit the paper under exam conditions (3 hours, no notes), then mark yourself with the separate solutions file."],
    ], [1.0 * cm, fw - 1.0 * cm]))
    s.append(Spacer(1, 6))

    # ================================================================ SECTION A
    s += [banner("SECTION A — answer Question 1 and any two of Questions 2, 3 and 4"), Spacer(1, 2)]

    # ---- Q1
    s.append(P("Question 1 &nbsp;(compulsory) &nbsp;[45]", "q"))
    s.append(P("<b>MediLink</b> is a web and mobile system used by a chain of clinics. <i>Patients</i> register, book and cancel appointments, view"
               " their prescriptions and pay bills online. <i>Doctors</i> see their daily schedule, record a diagnosis and issue a prescription."
               " <i>Receptionists</i> register walk-in patients, confirm appointments and collect cash payments. An <i>Admin</i> creates and disables"
               " staff accounts. Everyone must log in before using the system. Booking an appointment always checks the doctor's availability."
               " A patient who has health insurance may <i>optionally</i> apply the insurance while paying a bill. Appointment reminders are sent by an"
               " external SMS gateway. Answer all parts."))
    A("(a)", 7, [P("Draw the <b>use case diagram</b> of MediLink. Show the actors, the system boundary, the use cases and the include / extend"
                   " relationships. Name one <i>include</i> and one <i>extend</i> from your diagram and justify each in one sentence.")])
    A("(b)", 14, [P("MediLink locks accounts to protect them. <i>After three consecutive wrong passwords an account becomes Locked. A Locked account"
                    " is unlocked automatically after 15 minutes, or at once by an Admin. A password becomes Expired 90 days after it was set; the user"
                    " must then change it, after which the account is Active again. An Admin may Disable an account permanently at any time."
                    " A new account starts Active.</i>"),
                  P("(i) Write <b>two functional</b> and <b>two non-functional</b> requirements about logging in, each in a <b>verifiable</b> form,"
                    " and label each. [4] &nbsp;(ii) Draw the UML <b>state diagram</b> of a MediLink account with events, guards, actions, the initial state"
                    " and the final state. [10]")])
    A("(c)", 10, [P("A new password is accepted only if its length is <b>8 to 16 characters inclusive</b> and it contains <b>at least one digit</b>"
                    " and <b>at least one uppercase letter</b>."),
                  P("(i) List the valid and invalid <b>equivalence classes</b> for the three properties. [3] &nbsp;(ii) Give the <b>boundary-value</b> tests for the"
                    " length (robust BVA, the digit and the uppercase rule always satisfied). [3] &nbsp;(iii) Give a smallest set of concrete passwords that"
                    " achieves <b>weak</b> equivalence class coverage, mark each case as a <i>positive</i> or a <i>negative</i> test with the expected result, and"
                    " state how many cases <b>strong</b> equivalence class testing would need. [4]")])
    A("(d)", 6, [P("Each fragment of MediLink code breaks one design principle. Name the principle, say in one line how it is broken, and give the fix. [2 + 2 + 2]"),
                 *bullets(["<font face='Mono'>AppointmentManager</font> books appointments, calculates bills, sends SMS reminders and prints PDF reports.",
                           "<font face='Mono'>PaymentProcessor.pay(String mode)</font> is an <font face='Mono'>if (mode.equals(\"CASH\")) … else if (mode.equals(\"CARD\")) …</font> chain that is edited"
                           " for every new payment method.",
                           "<font face='Mono'>interface ClinicStaff { void treat(); void register(); void managePayroll(); }</font> is implemented by"
                           " <font face='Mono'>Receptionist</font>, which leaves <font face='Mono'>treat()</font> and <font face='Mono'>managePayroll()</font> empty."])])
    A("(e)", 8, [P("MediLink has four modules: Login, Appointment, Billing and Notification; Notification calls the external SMS gateway."),
                 P("(i) Differentiate <b>internal</b> and <b>external integration testing</b> and give one MediLink test case for each. [4] &nbsp;(ii) Billing is finished"
                   " but the Appointment module that supplies its bill items is not. Name the <i>stub</i> or <i>driver</i> you would write, and say whether this is"
                   " a top-down or a bottom-up integration step. [4]")])

    # ---- Q2
    s.append(P("Question 2 &nbsp;[30]", "q"))
    A("(a)", 22, [P("<b>LiveScore</b> is a cricket app. A <font face='Mono'>Match</font> object holds the current runs, wickets and overs."
                    " A <font face='Mono'>MobileWidget</font>, a <font face='Mono'>WebsitePanel</font> and an <font face='Mono'>SmsAlert</font> must each show or send"
                    " the current score <i>whenever it changes</i>. Viewers can start and stop following a match at any time, and"
                    " <font face='Mono'>Match</font> must not know the concrete display classes."),
                  P("(i) Draw the UML class diagram using the appropriate pattern and name each role. [6] &nbsp;(ii) Write the Java code of the subject interface and the"
                    " <font face='Mono'>Match</font> class (<font face='Mono'>attach</font>, <font face='Mono'>detach</font>, <font face='Mono'>notifyObservers</font>,"
                    " <font face='Mono'>updateScore</font>). [8] &nbsp;(iii) Write the observer interface, <font face='Mono'>MobileWidget</font> and a"
                    " <font face='Mono'>main</font> that attaches two viewers, updates the score, detaches one viewer and updates again. [8]")])
    A("(b)", 8, [P("A GUI toolkit has a <font face='Mono'>Widget</font> with <font face='Mono'>draw()</font> and <font face='Mono'>getWidth()</font>."
                   " <font face='Mono'>Label</font> and <font face='Mono'>Button</font> are simple widgets. A <font face='Mono'>Panel</font> can hold any"
                   " widgets, including other Panels, and drawing a Panel draws everything inside it. A <font face='Mono'>Window</font> is a top-level Panel with a title."),
                 P("Draw the UML class diagram using the suitable pattern and label every role. [6 + 2]")])

    # ---- Q3
    s.append(P("Question 3 &nbsp;[30]", "q"))
    A("(a)", 12, [P("(i) Explain <b>Test-Driven Development</b>. Show one complete cycle for a method <font face='Mono'>boolean isLeap(int year)</font>: the failing JUnit"
                    " test, the minimal code that passes it, and one refactoring step. [6] &nbsp;(ii) State the benefits of TDD and one limitation. [6]")])
    A("(b)", 10, [P("Design white-box test cases for this method. <i>Treat the compound condition on line 2 as one decision.</i>"), code(Q3B),
                  P("(i) Draw the control-flow graph. [3] &nbsp;(ii) Compute the cyclomatic complexity. [2] &nbsp;(iii) Give the smallest set of test inputs, with the expected"
                    " return value of each, that gives 100 % <b>branch</b> coverage. [5]")])
    A("(c)", 8, [P("(i) State the <b>equivalence-partitioning</b> principle and explain why it is used. [4] &nbsp;(ii) A blood-donor registration form accepts an"
                   " integer <i>age</i>; donors must be 18 to 60 inclusive. List the equivalence classes and one test value from each. [4]")])

    # ---- Q4
    s.append(P("Question 4 &nbsp;[30]", "q"))
    A("(a)", 12, [P("Draw the UML <b>class diagram</b> of a small accounting package. Show attributes, key operations, generalisation, aggregation/composition and the"
                    " multiplicity at every association end."),
                  *bullets(["An <i>Account</i> has an id, a title and a balance, and supports <font face='Mono'>deposit(amount)</font>, <font face='Mono'>withdraw(amount)</font>"
                            " and <font face='Mono'>getBalance()</font>. It is never created directly.",
                            "A <i>Debtor</i> is a customer who owes the business money (it also records a creditLimit); a <i>Creditor</i> is a supplier the business"
                            " owes (it also records a paymentDueDate). Both are Accounts.",
                            "A <i>LedgerGroup</i> (for example “Suppliers”) holds any number of Accounts and other LedgerGroups, to any depth; asking a group for its"
                            " balance returns the total of everything inside it, exactly as for a single Account.",
                            "A <i>Clerk</i> posts <i>Transactions</i> (id, date, amount). A Transaction is posted to exactly one Account by exactly one Clerk.",
                            "Before posting, a Clerk must pass a <i>two-step authentication</i> (password, then a one-time code). The design must let a third step be added later"
                            " without changing the Clerk class."])])
    A("(b)", 10, [P("Consider this method. <i>Every simple condition (<font face='Mono'>age &gt; 60</font>, <font face='Mono'>years &gt;= 10</font>, …) is a separate"
                    " condition; <font face='Mono'>||</font> and <font face='Mono'>&amp;&amp;</font> short-circuit.</i>"), code(Q4B),
                  P("(i) List the simple conditions and the decisions. [2] &nbsp;(ii) Give the smallest test set for 100 % <b>decision</b> coverage with the expected return"
                    " values. [3] &nbsp;(iii) Give the smallest test set for 100 % <b>condition</b> coverage, showing which conditions each test evaluates. [3] &nbsp;"
                    "(iv) Does your condition-coverage set also give decision coverage? Can condition coverage ever fail to give it? [2]")])
    A("(c)", 8, [P("State the <b>Interface Segregation Principle</b>. Give an example of a design that violates it (an office-equipment example is suggested) and show the"
                   " corrected design with a class diagram or code outline. [2 + 3 + 3]")])

    # ================================================================ SECTION B
    s += [Spacer(1, 4), banner("SECTION B — answer Question 5 and any two of Questions 6, 7 and 8", GREEN), Spacer(1, 2)]

    # ---- Q5
    s.append(P("Question 5 &nbsp;(compulsory) &nbsp;[35]", "q"))
    A("(a)", 15, [P("<b>BrewBox</b> is a café chain with branches in Dhaka and Tokyo. Every branch serves a <i>Coffee</i> and a <i>Snack</i>, but the recipes depend on the"
                    " region: Dhaka serves a <i>CardamomLatte</i> with a <i>Samosa</i>; Tokyo serves a <i>MatchaLatte</i> with a <i>Dorayaki</i>. The ordering code"
                    " (<font face='Mono'>Cafe.serveSet()</font>) must not name any regional class, a branch in a new city must be addable by writing new classes only,"
                    " and a branch must never serve a Dhaka coffee with a Tokyo snack."),
                  P("(i) Name the pattern and justify the choice. [3] &nbsp;(ii) Draw the class diagram. [5] &nbsp;(iii) Write the Java code for the abstract products, the Dhaka products,"
                    " the factory types and the <font face='Mono'>Cafe</font> class. [7]")])
    A("(b)", 12, [P("A single class can sometimes play the roles of an <b>Adapter</b> and a <b>Decorator</b> at the same time. Give a concrete example, draw its class diagram,"
                    " and show the key code, saying which part adapts and which part decorates. [3 + 5 + 4]")])
    A("(c)", 8, [P("(i) Why is high test coverage important? [3] &nbsp;(ii) What risks does low coverage bring? [2] &nbsp;(iii) Why does 100 % statement coverage still not"
                   " guarantee a bug-free method? Give a short example. [3]")])

    # ---- Q6
    s.append(P("Question 6 &nbsp;[35]", "q"))
    A("(a)", 8, [P("A junior developer at a fintech start-up finds that the interest-calculation module over-charges about 2 % of loan customers by a small amount. The manager says:"
                   " “It is tiny. Ship on Friday, fix it next quarter, and do not tell the customers.” Which principles of the ACM / IEEE-CS Software Engineering Code of"
                   " Ethics are breached, and what should the developer do? [8]")])
    A("(b)", 7, [P("Explain the principle “software engineers shall act in a manner that is in the best interests of their client and employer, <i>consistent with the public"
                   " interest</i>”. Give two situations in which the two interests conflict and say how the conflict is resolved. [7]")])
    A("(c)", 20, [P("(i) A university registrar needs a course-registration system. The registration rules are fixed by regulation and the core must be live in 3 months,"
                    " before the semester starts; the extras (waiting lists, fee payment, an advising dashboard) are still vague and the registrar's office keeps changing its mind"
                    " about them. Should the team use an <b>incremental</b> or an <b>agile</b> approach? Justify with the scenario and compare the two. [8]"),
                  P("(ii) List at least <b>five</b> kinds of issues commonly identified in a code review, with a short concrete example of each, and name two practices that make a"
                    " review effective. [12]")])

    # ---- Q7
    s.append(P("Question 7 &nbsp;[35]", "q"))
    A("(a)", 10, [P("(i) What are the <b>core (framework) activities</b> of the generic process model? [4] &nbsp;(ii) Draw the <b>waterfall</b> model and give two advantages and"
                    " two disadvantages. [6]")])
    A("(b)", 10, [P("A team uses a Kanban board with the columns <i>Backlog → Analysis (WIP 2) → Development (WIP 3) → Review (WIP 2) → Done</i>."
                    " <i>Today:</i> Backlog holds B1–B5; Analysis holds A1; Development holds D1, D2, D3 (D3 is finished); Review holds R1 and R2. The first four cards the"
                    " team delivered were:"),
                  table([["Card", "Requested (day)", "Work started (day)", "Delivered (day)"],
                         ["K1", "1", "2", "6"], ["K2", "1", "3", "9"], ["K3", "2", "5", "8"], ["K4", "3", "4", "10"]],
                        [2.0 * cm, 3.4 * cm, 3.6 * cm, 3.4 * cm]),
                  P("(i) Draw today's board. [3] &nbsp;(ii) Find the lead time and the cycle time of each delivered card and their averages. [4] &nbsp;(iii) The developer who has just"
                    " finished D3 wants to pull the next card. May she? What should she do, and which Kanban principle does this show? [3]")])
    A("(c)", 15, [P("(i) Describe one <b>Scrum sprint</b>: the roles, the artefacts and the activities (events) in order. [9] &nbsp;(ii) Differentiate the <b>product backlog</b> and the"
                    " <b>sprint backlog</b>. [6]")])

    # ---- Q8
    s.append(P("Question 8 &nbsp;[35]", "q"))
    A("(a)", 15, [P("Define each code smell, give a short code or class example, and name the refactoring that removes it: <b>Divergent Change</b> [4], <b>Data Clumps</b> [4],"
                    " <b>Primitive Obsession</b> [4], <b>Lazy Class</b> [3].")])
    A("(b)", 20, [P("Refactor each fragment. Name the smell, name the refactoring and show the resulting code."),
                  P("(i) A complex condition [6]:", "lab"), code(Q8_1),
                  P("(ii) A type code [7]:", "lab"), code(Q8_2),
                  P("(iii) Nested conditionals [7]:", "lab"), code(Q8_3)])

    s += [Spacer(1, 10), P("— End of paper —", "sub")]
    return s
