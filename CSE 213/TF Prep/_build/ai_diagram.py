"""ai_diagram.py — diagram questions from AI Sir's senior course (CSE 325 Information System Design,
folder 'CSE 213/AI Sir Diagram question from seniors') with full solutions.

ROWS feeds questions_data.py (course 'CSE 325', page 'AI Sir <session> p.N').
section(n, key) writes the 'Senior Diagram Practice' section into note file A3/A4/A5/A6.
"""


def P(y, n):
    return f"AI Sir {y} p.{n}"


# year, qno, marks, page, question, file, lesson, key, type
ROWS = [
    # ---------------- A3 class diagrams
    ("2017-18", "1(a)", 20, P("2017-18", 1), "Language-course assignment: list the inconsistencies in the given class diagram (AssignCourseUI, AssignCourse, Student, Language, Course, CourseAssignmentInfo)", "A3", "L11", "class-diagram", "Design"),
    ("2018-19", "1(a)", 22, P("2018-19", 1), "Office loans: eligibility (age, experience, clean record), loan parameters changing over time — class diagram", "A3", "L11", "class-diagram", "Design"),
    ("2019-20", "2(b)", 20, P("2019-20", 1), "Sonali Bank ATM withdrawal: show the steps of identifying classes from the use case scenario", "A3", "L11", "class-identify", "Design"),
    ("2020-21", "2(a)", 13, P("2020-21", 1), "Course offerings, joint teachers, enrollments, grades from test items by a grading rule — class diagram with business-logic classes", "A3", "L11", "class-diagram", "Design"),
    ("2023-24", "6(b)", 5, P("2023-24", 4), "Show aggregation, composition and dependency with examples", "A3", "L10", "agg-comp", "Design"),
    # ---------------- A4 state diagrams
    ("2018-19", "4(a)", 22, P("2018-19", 1), "Inventory management: requisition, approval, issue, re-order below threshold, return of non-consumables — state diagram of a product", "A4", "L15", "statechart", "Design"),
    ("2020-21", "4(a)", 12, P("2020-21", 2), "Inventory management (same scenario) — state diagram of a product", "A4", "L15", "statechart", "Design"),
    ("2019-20", "5(b)", 12, P("2019-20", 2), "Tour package booking (customise for groups > 10, advance, final payment, refund) — state diagram of a booking", "A4", "L15", "statechart", "Design"),
    ("2021-22", "8(a)", 13, P("2021-22", 4), "University seminar: proposed, scheduled, open for enrolment, full, closed — state diagram", "A4", "L15", "statechart", "Design"),
    ("2022-23", "4(a)", 14, P("2022-23", 3), "Garage controller (modes off/auto/closed/open, entry/exit gates, count/max) — state diagram", "A4", "L15", "statechart", "Design"),
    ("2023-24", "2(a)", 15, P("2023-24", 1), "Online food delivery order: pending, payment retries, confirmed, parallel cooking + rider, out for delivery, escalation after 60 min — state diagram", "A4", "L14", "statechart", "Design"),
    # ---------------- A5 interaction diagrams
    ("2017-18", "2(a)", 13, P("2017-18", 2), "Language-course assignment scenario — collaboration diagram", "A5", "L18", "collaboration", "Design"),
    ("2017-18", "2(c)", 10, P("2017-18", 2), "One/two-word answers on sequence diagrams (execution, async message, returns, focus of control, sequence vs collaboration)", "A5", "L16", "sequence", "Theory"),
    ("2018-19", "3(a)", 21, P("2018-19", 1), "Bank with normal and foreign users (deposit bonus, withdrawal limits, interest, conversion) — sequence diagram", "A5", "L17", "sequence", "Design"),
    ("2019-20", "6(b)", 12, P("2019-20", 3), "Payroll: bulk annual salary increment within grade maximum — sequence diagram", "A5", "L17", "sequence", "Design"),
    ("2019-20", "7(a)", 15, P("2019-20", 3), "Gym membership renewal SMS, follow-up survey, discount offer — collaboration diagram", "A5", "L18", "collaboration", "Design"),
    ("2020-21", "2(b)", 14, P("2020-21", 1), "Grade computation for course offerings — collaboration diagram with boundary and controller classes", "A5", "L18", "collaboration", "Design"),
    ("2020-21", "3(a)", 15, P("2020-21", 2), "Tour package booking portal — sequence diagram", "A5", "L17", "sequence", "Design"),
    ("2021-22", "3(c)", 19, P("2021-22", 2), "ATM withdrawal — collaboration diagram, then derive the class diagram from it", "A5", "L18", "collaboration", "Design"),
    ("2022-23", "2(a)", 15, P("2022-23", 1), "MPO teacher recruitment: check eligibility of an applicant — collaboration diagram", "A5", "L18", "collaboration", "Design"),
    ("2022-23", "3(a)", 15, P("2022-23", 2), "Scheduler app: add appointment, validation, conflict, join existing meeting, reminders — sequence diagram", "A5", "L17", "sequence", "Design"),
    ("2023-24", "1(a)", 16, P("2023-24", 1), "Hospital emergency admission: register, verify insurance, triage, doctor or waiting queue, store, SMS — collaboration diagram", "A5", "L18", "collaboration", "Design"),
    ("2023-24", "3(a)", 15, P("2023-24", 1), "Ride sharing: request, nearby drivers, offers one by one, accept or timeout — sequence diagram", "A5", "L17", "sequence", "Design"),
    # ---------------- A6 use case + BPMN
    ("2017-18", "3(a)", 24, P("2017-18", 2), "Multi-seller shopping site: complete the given use case diagram with include/extend and extension points", "A6", "L20", "usecase-diagram", "Design"),
    ("2017-18", "3(b)", 10, P("2017-18", 3), "Types of structural things in UML; four relationships in a class diagram", "A6", "L19", "uml-basics", "Theory"),
    ("2018-19", "1(b)", 8, P("2018-19", 1), "Show an example of 'extends' in a use case diagram", "A6", "L19", "usecase-rel", "Design"),
    ("2020-21", "3(c)", 8, P("2020-21", 2), "Show an example of 'extends' in a use case diagram", "A6", "L19", "usecase-rel", "Design"),
    ("2018-19", "2(a)", 20, P("2018-19", 1), "Bank with normal and foreign users — BPMN diagram", "A6", "L22", "bpmn", "Design"),
    ("2019-20", "1(b)", 25, P("2019-20", 1), "Microwave oven: use case diagram, detailed scenarios for set timer and heating, acceptance test cases", "A6", "L20", "usecase-diagram", "Design"),
    ("2019-20", "5(a)", 15, P("2019-20", 2), "Tourism operator portal (packages, customisation, advance and final payment, refund) — BPMN diagram", "A6", "L22", "bpmn", "Design"),
    ("2020-21", "1(a)", 14, P("2020-21", 1), "Life-insurance premium calculation (gold rate, +20 %, monthly/yearly, penalty, SMS, cancel after 2 misses) — BPMN diagram", "A6", "L22", "bpmn", "Design"),
    ("2021-22", "3(a)", 8, P("2021-22", 2), "ATM operations (withdraw, balance, change PIN, deposit, transfer, recharge) — use case diagram", "A6", "L20", "usecase-diagram", "Design"),
    ("2021-22", "3(b)", 8, P("2021-22", 2), "Write the use cases for withdrawing money and changing PIN", "A6", "L20", "usecase-narrative", "Design"),
    ("2021-22", "5(a)", 13, P("2021-22", 3), "MPO teacher recruitment: match qualifications against criteria — BPMN diagram", "A6", "L22", "bpmn", "Design"),
    ("2022-23", "1(a)", 15, P("2022-23", 1), "Bangla Academy book stock: online orders, outlet sales, book fairs with reconciliation, discounts — BPMN diagram", "A6", "L22", "bpmn", "Design"),
    ("2023-24", "6(a)", 15, P("2023-24", 3), "Fantasy adventure game: Quest & Player Interaction subsystem — use case diagram with actors, ≥ 6 use cases, 2 include, 1 extend", "A6", "L20", "usecase-diagram", "Design"),
    ("2023-24", "7(b)", 10, P("2023-24", 4), "Three types of flow objects in BPMN (event, activity, gateway) with examples", "A6", "L21", "bpmn", "Theory"),
    ("2023-24", "7(c)", 15, P("2023-24", 4), "Choose the most appropriate diagram (BPMN, use case, class) for three projects; justify and give one limitation", "A6", "L19", "uml-basics", "Theory"),
]


# --------------------------------------------------------------------------- solutions
def _q(n, text):
    n.h2(text)


def sec_A3(n, code):
    _q(n, "2017-18 Q1(a) — Inconsistencies in the language-course class diagram (20)")
    n.p("The scenario needs: show students → select student → show languages → select language → show the French "
        "courses the student has **not** taken → select course → create the assignment. Inconsistencies (no redraw):")
    n.numbered([
        "**Boundary class is incomplete**: AssignCourseUI has only SelectStudent(), SelectLanguage(), AssignCourse(); it "
        "has no StartInterface()/display operations (DisplayStudents(), DisplayLanguages(), DisplayCourses()) although "
        "the controller's StartInterface() must open it and the lists must be shown.",
        "**Controller lacks needed operations**: AssignCourse has no GetStudents(), no AssignCourse() and no "
        "GetStudentCourses(); GetLanguageInfo() is not needed by the scenario.",
        "**No associations from the boundary to the control and from the control to the entities** — the "
        "messages in the scenario cannot be sent.",
        "**Language holds CourseID** — wrong: one language has many courses, so the foreign key belongs in Course (Course "
        "already has LanguageID). This is redundant and contradicts the 1-to-many relation.",
        "**Language is not associated with Course** although Course.LanguageID refers to it (missing Language 1 — * Course).",
        "**Course holds StudentName** — a course does not belong to one student; the student–course link is "
        "CourseAssignmentInfo. StudentName also duplicates Student data.",
        "**Course has no operation to return the courses of a language not taken by a student** "
        "(GetLanguageCourses(languageID, studentID)); GetCourses() has no parameters.",
        "**Student has AssignCourse()** — creating an assignment is the responsibility of CourseAssignmentInfo "
        "(e.g. AddAssignment(studentID, courseID)), coordinated by the controller.",
        "**GetStudentCourses() appears in both Student and CourseAssignmentInfo** — duplicated responsibility.",
        "**CourseAssignmentInfo has no operation to create a record** and should be an association class between "
        "Student and Course (it only has StudentID, CourseID, RegistrationDate).",
        "**No multiplicities** on any association (Student 1 — 0..* CourseAssignmentInfo 0..* — 1 Course).",
        "**The teacher's log-in is not supported** (no Teacher/User class or Login operation), and operations have no "
        "parameters (SelectStudent(studentID), SelectLanguage(languageID)).",
    ])
    _q(n, "2018-19 Q1(a) — Office loan system: class diagram (22)")
    n.p("'Conditions may change over time' → keep loan parameters and rules as dated versions, not constants.")
    code(n, """Employee [empId, name, dob, joiningDate, salary; age(), yearsOfExperience(), hasCleanRecord()]
Employee 1 ---- 0..* DisciplinaryRecord [date, offence, status]
Employee 1 ---- 0..* LoanApplication [appId, amount, appliedOn, status: ApplicationStatus; submit(), withdraw()]
LoanApplication * ---- 1 LoanScheme [name; currentVersion(): SchemeVersion; maxAllowed(e: Employee): double]
LoanScheme 1 ◆---- 1..* SchemeVersion [interestRate, yearsToRepay, maxSalaryMultiple, effectiveFrom, effectiveTo]
LoanScheme 1 ◆---- 1..* EligibilityRule {abstract} [effectiveFrom, effectiveTo; isSatisfied(e: Employee): boolean]
      △ AgeRule [minAge, maxAge]   △ ExperienceRule [minYears]   △ DisciplinaryRule [maxOpenCases = 0]
LoanEvaluator «control» [evaluate(app): boolean]  ---uses---> EligibilityRule, SchemeVersion
Manager [id, name; approve(app), reject(app, reason)] 1 ---- 0..* LoanApplication (decides ▶)
LoanApplication 1 ---- 0..1 Loan [loanId, principal, rate, startDate; monthlyInstalment(), outstanding()]
Loan 1 ◆---- 0..* Repayment [date, amount]
«enumeration» ApplicationStatus { SUBMITTED, APPROVED, REJECTED, WITHDRAWN }
{maxAllowed = employee.salary x version.maxSalaryMultiple}""", size=8)
    _q(n, "2019-20 Q2(b) — ATM withdrawal: steps of identifying classes (20)")
    n.numbered([
        "**Underline the nouns** in the scenario: account holder, Sonali Bank, amount, account, debit card, ATM booth/"
        "machine, card, PIN, keypad, balance, bank account, notification, registered phone number, central server, transaction.",
        "**Remove synonyms**: ATM booth = ATM machine; account = bank account; card = debit card.",
        "**Remove attributes**: amount (of a withdrawal), PIN (of a card), balance (of an account), phone number (of the holder).",
        "**Remove things outside the system / actors**: account holder (actor, but its data is kept as Customer), "
        "central server (external system → boundary/proxy class), Sonali Bank (the system itself).",
        "**Classify (boundary / control / entity)** and add the event 'withdrawal' as a class (it has amount, time, status).",
        "**Assign responsibilities and associations**:",
    ])
    n.table(["Class", "Stereotype", "Attributes / responsibilities"], [
        ["Customer", "entity", "name, registeredPhone"],
        ["Account", "entity", "accountNo, balance; hasBalance(amount), debit(amount)"],
        ["DebitCard", "entity", "cardNo, pinHash, expiry, status; verifyPIN(pin)"],
        ["Withdrawal (Transaction)", "entity", "amount, dateTime, status; record()"],
        ["ATMScreen / Keypad", "boundary", "showMessage(), readPIN(), readAmount()"],
        ["CardReader", "boundary", "readCard(), ejectCard()"],
        ["CashDispenser", "boundary", "dispense(amount)"],
        ["CentralServerGateway / SMSGateway", "boundary", "sendNotification(phone, text)"],
        ["WithdrawalController", "control", "authorise(card, pin), withdraw(amount), notify()"],
    ], widths_cm=[4.4, 2.4, 10.4], font_size=8.5)
    code(n, """Customer 1 ---- 1..* Account      Account 1 ---- 1..* DebitCard      Account 1 ---- 0..* Withdrawal
WithdrawalController ---> CardReader, ATMScreen, CashDispenser, DebitCard, Account, Withdrawal, SMSGateway""")
    _q(n, "2020-21 Q2(a) — Course offerings and grades: class diagram with logic classes (13)")
    code(n, """Teacher [id, name] 1..* ---- 0..* CourseOffering (teaches ▶ — joint offering allowed)
Course [code, title, credit] 1 ---- 0..* CourseOffering [section, year]  * ---- 1 Semester [name, start, end]
Student [id, name] 0..* ---- 0..* CourseOffering   via association class  Enrollment [enrolledOn]
CourseOffering 1 ◆---- 1..* TestItem [name, fullMarks, weight%]
Enrollment 1 ◆---- 0..* Mark [obtained] * ---- 1 TestItem
CourseOffering * ---- 1 GradingRule {abstract} [toGrade(total): String]
        △ AbsoluteGradingRule [ranges: (min, max, grade, point)]   △ RelativeGradingRule [curve]
GradeCalculator «business logic» [computeTotal(e: Enrollment): double; computeGrade(e): GradeRecord]
        ----uses----> GradingRule, Mark, TestItem
Enrollment 1 ---- 0..1 GradeRecord «stores computed values» [totalMarks, letterGrade, gradePoint, computedOn]""", size=8)
    _q(n, "2023-24 Q6(b) — Aggregation, composition, dependency (5)")
    code(n, """Aggregation  (hollow ◇, 'has-a', part can exist alone):   Department 1 ◇---- 0..* Professor
Composition  (filled ◆, part lives and dies with whole):  Order 1 ◆---- 1..* OrderLine
Dependency   (dashed --->, temporary use):                ReportGenerator - - -> PdfWriter   (used only inside generate())""")


def sec_A4(n, code):
    _q(n, "2018-19 Q4(a) / 2020-21 Q4(a) — Inventory: states of a product (22 / 12)")
    n.p("Two concurrent views of a product: its **stock level** (one per product) and the life of an **issued unit**.")
    code(n, """[Product] — region STOCK LEVEL
 ● --> (In Stock)
 (In Stock)   --requisition(q) [q <= stock] / approve(); stock -= q--> (In Stock)            → unit becomes Ready to Issue
 (In Stock)   --requisition(q) [q > stock] / putOnHold()--> (In Stock)
 (In Stock)   --when [stock < threshold] / generateReorderRequest()--> (Reorder Requested)
 (Reorder Requested) --goodsReceived(n) / stock += n [stock >= threshold]--> (In Stock)
 (Reorder Requested) --when [stock = 0]--> (Out of Stock) --goodsReceived(n) / stock += n--> (In Stock)
 (In Stock) --discontinue()--> ◉
[Product unit] — region ISSUED UNIT
 ● --> (Available) --requisitionApproved--> (Ready to Issue) --issue(employee)--> (Issued)
 (Issued) --[consumable]--> (Consumed) --> ◉
 (Issued) --employeeRetired or employeeTransferred [not consumable] / requestReturn()--> (Return Pending)
 (Return Pending) --returned / stock += 1--> (Available)
 (Return Pending) --after [30 days] / reportLoss()--> (Written Off) --> ◉""", size=8)
    _q(n, "2019-20 Q5(b) — Tour booking: state diagram (12)")
    code(n, """● --selectPackage(pkg)--> (Package Selected)
(Package Selected) --customise() [groupSize > 10] / adjustPrice()--> (Package Selected)
(Package Selected) --payAdvance(a)--> (Booked)                       entry / issueBookingRef()
(Booked) --payRemaining() [before deadline]--> (Confirmed)            entry / confirmAllComponents()
(Booked) --when [deadline passed && not paid] / forfeitAdvance()--> (Cancelled) --> ◉
(Booked) --cancel() / refundAsPerPolicy()--> (Cancelled)
(Confirmed) --activityUnavailable(x) / scheduleRefund(x)--> (Confirmed)      (refund made later)
(Confirmed) --tourStarts--> (In Tour) --tourEnds--> (Completed) --> ◉""", size=8)
    _q(n, "2021-22 Q8(a) — Seminar: state diagram (13)")
    code(n, """● --propose(professor)--> (Proposed)
(Proposed) --arrange(dates, times, rooms)--> (Scheduled)
(Scheduled) --when [date = second Monday of August] / advertise()--> (Open For Enrolment)
(Open For Enrolment) --enrol(student) [placesLeft > 1] / placesLeft----> (Open For Enrolment)
(Open For Enrolment) --enrol(student) [placesLeft = 1] / placesLeft = 0--> (Full)
(Full) --enrol(student) / reject()--> (Full)
(Full) --drop(student) / placesLeft++--> (Open For Enrolment)
(Open For Enrolment), (Full) --when [today = startDate - 2 days]--> (Enrolment Closed)
(Enrolment Closed) --startDate--> (Running) --lastSession--> ◉""", size=8)
    _q(n, "2022-23 Q4(a) — Garage controller: state diagram (14)")
    n.p("This is the garage example of Lec 7 sl. 25–26 (Lesson 15 §1). Full answer:")
    code(n, """● --> (NoCentralControl)                       gates in no particular state
any state --mode-off--> (NoCentralControl)
(NoCentralControl) --mode-open--> [Manual: Open    entry / unlockGates]
(NoCentralControl) --mode-closed--> [Manual: Closed entry / lockGates]
(NoCentralControl) --mode-auto--> [Automatic]
[Manual: Open] <--mode-open / mode-closed--> [Manual: Closed] ;  both --mode-auto--> [Automatic]
[Automatic] = ● -> (AutoOpen entry / unlockGates) --entrygate / count++ [count + 1 = max]--> (AutoFull entry / lockGates)
                   (AutoOpen) --entrygate / count++ [count + 1 < max]--> (AutoOpen)
                   (AutoFull) --exitgate / count----> (AutoOpen)
In every mode: entrygate / count++ ; exitgate / count--   (internal transitions; count kept across modes)""", size=8)
    _q(n, "2023-24 Q2(a) — Online food delivery order: state diagram (15)")
    code(n, """● --placeOrder() / attempts := 0--> (Pending)
(Pending) --paymentSucceeded--> [Confirmed]
(Pending) --paymentFailed [attempts < 2] / attempts++--> (Pending)
(Pending) --paymentFailed [attempts = 2] / attempts++; notifyCustomer()--> (Cancelled) --> ◉      (3rd failure)
[Confirmed] = composite with two concurrent regions (fork):
     Kitchen:  ● -> (Preparing Food) --foodReady--> (Food Ready) -> ◉
     Rider:    ● -> (Assigning Rider) --riderAssigned(r)--> (Rider Assigned) -> ◉
   join (both regions done) --> (Out For Delivery)              entry / startTimer(60 min)
(Out For Delivery) --delivered / recordDelivery()--> (Delivered) --> ◉
(Out For Delivery) --after [60 min] [not delivered] / markEscalated(); alertSupport()--> (Escalated)
(Escalated) --delivered / recordDelivery()--> (Delivered)""", size=8)


def sec_A5(n, code):
    _q(n, "2017-18 Q2(a) — Language-course assignment: collaboration diagram (13)")
    code(n, """Teacher --1: login(id, pw)--> [:AssignCourseUI] --1.1: startInterface()--> [:AssignCourse «control»]
  1.2: *getStudents() --> [:Student] ;  1.3: displayStudents(list) --> [:AssignCourseUI]
Teacher --2: selectStudent(sid)--> [:AssignCourseUI] --2.1: selectStudent(sid)--> [:AssignCourse]
  2.2: *getLanguages() --> [:Language] ;  2.3: displayLanguages(list) --> [:AssignCourseUI]
Teacher --3: selectLanguage(lid)--> [:AssignCourseUI] --3.1: selectLanguage(lid)--> [:AssignCourse]
  3.2: taken := getStudentCourses(sid) --> [:CourseAssignmentInfo]
  3.3: *getLanguageCourses(lid) --> [:Course] ;  3.4: notTaken := filter(courses, taken) (self)
  3.5: displayCourses(notTaken) --> [:AssignCourseUI]
Teacher --4: selectCourse(cid)--> [:AssignCourseUI] --4.1: assignCourse(sid, cid)--> [:AssignCourse]
  4.2: «create» addAssignment(sid, cid, today) --> [:CourseAssignmentInfo] ;  4.3: showConfirmation() --> [:AssignCourseUI]""", size=8)
    _q(n, "2017-18 Q2(c) — One/two-word answers on sequence diagrams (10)")
    n.table(["Question", "Answer"], [
        ["(i) Execution of an operation is shown by", "an activation bar (execution occurrence)"],
        ["(ii) An asynchronous message is drawn with", "an open (stick) arrowhead"],
        ["(iii) Returns are drawn with", "a dashed line with an open arrowhead"],
        ["(iv) Is focus of control the same as activation?", "Yes"],
        ["(v) Major difference sequence vs collaboration", "sequence shows time order; collaboration shows object links (order by numbers)"],
    ], widths_cm=[8.0, 9.2])
    _q(n, "2018-19 Q3(a) — Bank (normal / foreign users): sequence diagram (21)")
    n.p("The withdraw part is the same as 2016-17 Q2(c) (Lesson 17). Full scenario:")
    code(n, """:User  :BankUI «boundary»  :AccountCtrl «control»  :Account  :DailyLimit  :FXService
 |--createAccount(info)->|--createAccount(info)-->|--«create»--> :Account
 |                       |<--accountNo------------|
 |--deposit(acc, amt)--->|--deposit(acc, amt)----->|--getBalance()-->|
 |                       |   alt [balance >= 2,000,000]  |--credit(amt * 1.02)-->|   (2 % bonus)
 |                       |   [else]                      |--credit(amt)--------->|
 |--withdraw(acc, amt)-->|--withdraw(acc, amt)---->|--check(amt)-------------------->:DailyLimit
 |                       |   alt [amt <= 100,000 && today+amt <= 300,000 && count < 5 && balance >= amt]
 |                       |                         |--debit(amt)--->|   --record(amt)--> :DailyLimit
 |<--cash, receipt-------|   [else] <--error(reason)
 |   opt [user is foreign]
 |--convert(acc, amt, cur)->|--convert(acc, amt, cur)->|--rate(cur)--------------------------------->:FXService
 |                       |                         |--debit(amt)--->|
 |<--foreign amount------|
 :Scheduler (every 3 months) --addInterest()--> :AccountCtrl --*credit(interest)--> :Account""", size=7.5)
    _q(n, "2019-20 Q6(b) — Payroll: bulk salary increment sequence diagram (12)")
    code(n, """:PayrollOfficer :IncrementUI :IncrementCtrl :IncrementRule :Employee :SalaryGrade :AuditLog
 |--startBulkIncrement(fy)-->|--run(fy)-->|--getRate(fy)-->:IncrementRule  <--pct--|
 |                           |            |--*getActiveEmployees()-->:Employee
 |                           |  loop [for each employee e]
 |                           |            |--basic := e.getBasic()-->|
 |                           |            |--max := getMaxBasic(e.grade)-->:SalaryGrade
 |                           |            |--newBasic := min(basic * (1 + pct), max) (self)
 |                           |            |--e.setBasic(newBasic)-->|   (house rent etc. recomputed from basic)
 |                           |            |--log(e, basic, newBasic)----------------------->:AuditLog
 |                           |<--summary(count, capped)--|
 |<--showSummary-------------|""", size=8)
    _q(n, "2019-20 Q7(a) — Gym renewal: collaboration diagram (15)")
    code(n, """[:Scheduler] --1: *dailyCheck()--> [:RenewalCtrl «control»]
  1.1: *members := getExpiringIn(7 days) --> [:Membership]
  1.2: *sendSMS(phone, renewalMsg) --> [:SMSGateway «boundary»]
[:Member] --2: renew(months, fee)--> [:MemberPortal] --2.1: renew(id, months)--> [:RenewalCtrl]
  2.2: extend(months) --> [:Membership] ;  2.3: record(fee) --> [:Payment]
[:Scheduler] --3: *afterExpiry()--> [:RenewalCtrl]
  3.1: *lapsed := getNotRenewed() --> [:Membership]
  3.2: *sendSurvey(member) --> [:SurveyService] ;  3.3: *response := getReason() --> [:SurveyResponse]
  3.4 [reason = cost]: offer := «create» Discount(member, rate) --> [:DiscountOffer]
  3.5 [reason = cost]: sendSMS(phone, offerMsg) --> [:SMSGateway]
[:Member] --4: acceptOffer(code)--> [:MemberPortal] --4.1--> [:RenewalCtrl] --4.2: reactivate(discount)--> [:Membership]""", size=8)
    _q(n, "2020-21 Q2(b) — Grade computation: collaboration diagram (14)")
    code(n, """Teacher --1: computeGrades(offeringId)--> [:GradeEntryUI «boundary»] --1.1: computeGrades(offeringId)--> [:GradeCtrl «control»]
  1.2: offering := find(offeringId) --> [:CourseOffering]
  1.3: *items := getTestItems() --> [:CourseOffering] ;  1.4: rule := getGradingRule() --> [:CourseOffering]
  1.5: *enrollments := getEnrollments() --> [:CourseOffering]
  1.6: *total := computeTotal(enrollment) --> [:GradeCalculator]
        1.6.1: *getMark(item) --> [:Mark]  ;  1.6.2: weight := getWeight() --> [:TestItem]
  1.7: *grade := toGrade(total) --> [:GradingRule]
  1.8: *«create» save(total, grade, point) --> [:GradeRecord]
  1.9: showGradeSheet(records) --> [:GradeEntryUI]""", size=8)
    _q(n, "2020-21 Q3(a) — Tour booking portal: sequence diagram (15)")
    code(n, """:Customer  :TourPortalUI  :BookingCtrl  :Package  :Booking  :PaymentGateway  :Supplier
 |--browse()-->|--*getPackages()-->:Package
 |--select(pkg, days, groupSize)-->|--price(pkg, days)--> :Package <--basePrice
 |   opt [groupSize > 10]  |--customise(pkg, groupSize) / adjustedPrice (self)
 |--book(pkg)--------------|--«create» Booking(pkg, price)--> :Booking
 |--payAdvance(amt)--------|--charge(amt)------------------------------>:PaymentGateway <--ok
 |                         |--setStatus(BOOKED)--> :Booking
 |   ... before the tour ...
 |--payRemaining()---------|--charge(remaining)------------------------>:PaymentGateway <--ok
 |                         |--*confirm(component)---------------------------------------->:Supplier
 |                         |   alt [all available]  --setStatus(CONFIRMED)--> :Booking
 |                         |   [activity unavailable] --scheduleRefund(cost)-->:PaymentGateway (later)
 |<--confirmation / refund notice--|""", size=7.5)
    _q(n, "2021-22 Q3(c) — ATM withdrawal: collaboration diagram and derived class diagram (19)")
    code(n, """Customer --1: insertCard()--> [:CardReader] --1.1: cardInserted(cardNo)--> [:ATMCtrl «control»]
  1.2: askPIN() --> [:ATMScreen]
Customer --2: enterPIN(pin)--> [:ATMScreen] --2.1: verify(cardNo, pin)--> [:ATMCtrl]
  2.2: ok := verifyPIN(pin) --> [:DebitCard]  ;  2.3a [not ok]: showError() --> [:ATMScreen]
Customer --3: withdraw(amount)--> [:ATMScreen] --3.1: withdraw(amount)--> [:ATMCtrl]
  3.2: ok := hasBalance(amount) --> [:Account] ;  3.3 [ok]: debit(amount) --> [:Account]
  3.4 [ok]: «create» Transaction(amount, now) --> [:Transaction]
  3.5 [ok]: dispense(amount) --> [:CashDispenser]
  3.6 [ok]: notify(phone, amount) --> [:CoreBankingGateway]
  3.7: ejectCard() --> [:CardReader]""", size=8)
    n.p("**Deriving the class diagram**: every object becomes a class; every message received becomes an operation of the "
        "receiver's class; every link becomes an association (navigable towards the receiver); data passed or stored "
        "become attributes.")
    code(n, """ATMCtrl «control» + cardInserted(cardNo), verify(cardNo, pin), withdraw(amount)
CardReader «boundary» + ejectCard()          ATMScreen «boundary» + askPIN(), showError()
CashDispenser «boundary» + dispense(amount)  CoreBankingGateway «boundary» + notify(phone, amount)
DebitCard «entity» [cardNo, pinHash] + verifyPIN(pin)
Account «entity» [accountNo, balance] + hasBalance(amount), debit(amount)
Transaction «entity» [amount, dateTime]
ATMCtrl ---> CardReader, ATMScreen, CashDispenser, CoreBankingGateway, DebitCard, Account, Transaction
DebitCard * ---- 1 Account ;  Account 1 ---- 0..* Transaction""", size=8)
    _q(n, "2022-23 Q2(a) — MPO recruitment: eligibility collaboration diagram (15)")
    code(n, """Candidate --1: apply(postId, profile)--> [:ApplicationUI «boundary»] --1.1: apply(postId, profile)--> [:EligibilityCtrl «control»]
  1.2: post := find(postId) --> [:Post]  (subject, salary grade, institution type)
  1.3: criteria := getCriteria(post.subject, post.grade, instType) --> [:QualificationCriteria]
  1.4: *quals := getQualifications() --> [:Candidate]   (degree, subject, results per level, dob)
  1.5: ageOk := checkAge(dob, criteria.maxAge, quotaRelaxation) (self)
  1.6: degreeOk := checkDegree(quals, criteria.subjects) --> [:QualificationCriteria]
  1.7: resultOk := checkResults(quals, criteria.minResults) --> [:QualificationCriteria]
  1.8: «create» Application(candidate, post, eligible, reasons) --> [:Application]
  1.9a [eligible]: issueAdmitCard() --> [:ApplicationUI]
  1.9b [not eligible]: showReasons(reasons) --> [:ApplicationUI]""", size=8)
    _q(n, "2022-23 Q3(a) — Scheduler: add appointment sequence diagram (15)")
    code(n, """:User  :CalendarUI  :AddApptWindow  :Calendar  :Appointment  :Meeting  :ReminderList
 |--addAppointment()-->|--date := activeSlot() (self)
 |                     |--«create» open(date, time)--> :AddApptWindow
 |--enter(name, loc, start, end, reminder)-->|
 |                     |   loop [name empty or end <= start]  --showError()--> :AddApptWindow
 |--ok()-------------->|--add(appt)----------------------->:Calendar
 |                     |                                   |--conflict := findAt(start, end) (self)
 |   alt [conflict]    |<--askChooseOrReplace()------------|
 |--choose(newTime) / replace()-->|--update / replace-------->:Calendar
 |   [same name and duration as a meeting m]
 |                     |<--askJoin(m)----------------------|
 |--yes()------------->|--join(user)---------------------------------------->:Meeting (add participant)
 |   [else]            |                                   |--«create» Appointment(...)-->:Appointment
 |   opt [reminder selected]                               |--add(reminder)----------------------->:ReminderList
 |<--showAppointment---|""", size=7.5)
    _q(n, "2023-24 Q1(a) — Hospital emergency admission: collaboration diagram (16)")
    code(n, """Receptionist --1: register(patientInfo)--> [:ReceptionUI «boundary»] --1.1: register(info)--> [:AdmissionCtrl «control»]
  1.2: «create» Patient(info) --> [:Patient]
  1.3: valid := verify(policyNo) --> [:InsuranceService «boundary»]
Nurse --2: assess(patientId, severity)--> [:TriageUI «boundary»] --2.1: assess(id, severity)--> [:AdmissionCtrl]
  2.2a [critical]: doctor := assignAvailable() --> [:EmergencyDoctor]
  2.2b [not critical]: enqueue(patient) --> [:WaitingQueue]
  2.3: «create» Admission(patient, severity, doctor | queuePos) --> [:Admission]
  2.4: save(admission) --> [:HospitalDB «entity/DAO»]
  2.5: send(emergencyContact, message) --> [:SMSGateway «boundary»]""", size=8)
    _q(n, "2023-24 Q3(a) — Ride sharing: sequence diagram (15)")
    code(n, """:Passenger  :MobileApp  :Backend  :DriverLocator  :Driver  :RideDB  :NotificationSvc
 |--requestRide(src, dst)-->|--rideRequest(pid, src, dst)-->|
 |                          |                |--drivers := findNearby(src)-->:DriverLocator
 |                          |   loop [for each driver d in drivers, until accepted or timeout]
 |                          |                |--offer(ride)----------------------------->:Driver (async)
 |                          |                |<--accept / reject / no response----------|
 |                          |   alt [a driver accepted]
 |                          |                |--save(ride, driver)-------------------------------->:RideDB
 |                          |                |--notify(passenger, driverInfo)--------------------------->:NotificationSvc
 |<--driver assigned, ETA---|<--------------------------------------------------------------------|
 |                          |   [timeout, no driver]
 |<--'no driver available'--|<--noDriver()---|""", size=7.5)


def sec_A6(n, code):
    _q(n, "2017-18 Q3(a) — Multi-seller shopping site: completed use case diagram (24)")
    n.p("Existing use cases are kept; relationships labelled; one new use case (Check Availability) added.")
    code(n, """Customer ---- (Search Product), (Navigate Deals), (Checkout), (Handle Order Status)
(Search Product) ··«include»··> (View Product Details)        both show a product list, then details
(Navigate Deals) ··«include»··> (View Product Details)
(Add to Cart)   ··«extend»··> (View Product Details)   extension point: 'add to cart' [product available]
(Rank Supplier) ··«extend»··> (View Product Details)   extension point: 'rate supplier'
(Write Review)  ··«extend»··> (View Product Details)   extension point: 'write review'
(Add to Cart)   ··«include»··> (Check Availability)          (new use case)
(Checkout)      ··«include»··> (Login)                       system must check the user is logged in
(Handle Order Status) ··«include»··> (Login)
(Register)      ··«extend»··> (Login)    extension point: 'not registered' [unregistered user]
(Checkout) requires a non-empty cart: precondition 'cart has items' (written as a note)""", size=8)
    _q(n, "2017-18 Q3(b) — Structural things; relationships in a class diagram (10)")
    n.p("(i) Structural things: class, interface, collaboration, use case, active class, component, node (artifact). "
        "(ii) Relationships: association, aggregation/composition, generalisation (inheritance), dependency (and realisation).")
    _q(n, "2018-19 Q1(b) / 2020-21 Q3(c) — Example of «extend» (8)")
    code(n, """Customer ---- (Withdraw Cash)
(Print Receipt) ··«extend»··> (Withdraw Cash)
    extension point: 'after dispense'   condition: [customer requests receipt]
(Withdraw Cash) is complete without Print Receipt; the arrow goes from the extension to the base.""")
    _q(n, "2018-19 Q2(a) — Bank (normal / foreign users): BPMN diagram (20)")
    code(n, """Pool: Bank — lanes: Customer | Bank System | Scheduler
 Customer:  ○ Customer request received -> <X> [type of request]
   [create]   -> [Submit account info] -> (System) [Create account] -> ◎ Account created
   [deposit]  -> [Submit deposit] -> (System) [Check balance] -> <X> [balance >= 20,00,000] -> [Credit amount + 2 % bonus]
                                                              [else] -> [Credit amount] -> <X> -> ◎ Deposit completed
   [withdraw] -> [Enter amount] -> (System) [Check limits] -> <X>
         [amount <= 1,00,000 and daily total <= 3,00,000 and count < 5 and balance >= amount] -> [Debit account]
              -> [Update daily counters] -> [Dispense cash] -> ◎ Withdrawal completed
         [limit exceeded / insufficient] -> [Reject withdrawal] -> ◎ Withdrawal rejected
   [convert, foreign user only] -> [Choose currency] -> (System) [Get rate] -> [Debit taka] -> [Give foreign currency] -> ◎ Converted
 Scheduler: ○(timer) Every 3 months -> [Calculate interest] -> [Add interest to balances] -> ◎ Interest posted
 Data store: Accounts DB (read/written by Create, Credit, Debit, Interest)""", size=7.5)
    _q(n, "2019-20 Q1(b) — Microwave oven: use case diagram, scenarios, acceptance tests (6+12+7)")
    code(n, """Actors: User (primary), Timer/Clock (secondary, time actor)
User ---- (Open/Close Door), (Set Timer), (Start Heating), (Stop Heating)
(Start Heating) ··«include»··> (Check Door Closed)     (Start Heating) ··«include»··> (Run Timer)
Timer ---- (Run Timer)        (Beep on Completion) ··«extend»··> (Run Timer) [time = 0]""")
    n.table(["Use case", "Scenario"], [
        ["Set Timer", "Pre: oven idle, food inside. 1 User presses digits on the keypad. 2 System shows the time. 3 User "
         "confirms (or presses Start). Alt: 1a invalid time (0 or > 99:99) → error beep, display cleared."],
        ["Heating", "Pre: time set, door closed. 1 User presses Start. 2 System checks door is closed, turns on magnetron "
         "and light, counts down. 3 At 0 the system stops and beeps. Alt: 2a door open → no start, message; "
         "2b user presses Stop or opens the door → heating stops, remaining time kept."],
    ], widths_cm=[3.0, 14.2], font_size=9)
    n.table(["Test", "Steps", "Expected"], [
        ["AT1", "Close door, set 0:30, Start", "heats 30 s, then beeps and stops"],
        ["AT2", "Door open, set 0:30, Start", "does not start; shows 'close door'"],
        ["AT3", "Heating, press Stop at 0:12", "stops, display shows 0:12"],
        ["AT4", "Heating, open door", "stops immediately"],
        ["AT5", "Enter 0:00 or > 99:99", "rejected, error beep"],
    ], widths_cm=[1.4, 7.0, 8.8], font_size=9)
    _q(n, "2019-20 Q5(a) — Tourism operator portal: BPMN diagram (15)")
    code(n, """Pools: Customer (black box) ··· Tour Operator (lanes: Portal | Sales | Operations) ··· Suppliers (hotels, transport)
 Portal:  ○ Package request received -> [Show packages] -> [Compute price (components, days)] -> <X> [group > 10?]
            [yes] -> (Sales) [Customise package and adjust price] -> <X>
            [no] -----------------------------------------------> <X> -> [Take booking with advance payment] ··advance··< Customer
 Operations: -> [Reserve components] ··requests··> Suppliers
 Portal:  ○(timer) Before tour -> [Request remaining payment] -> [Receive remaining payment] ··payment··< Customer
          -> <+> [Confirm hotel] [Confirm transport] [Confirm activities] <+>
          -> <X> [all available] -> ◎ Tour confirmed
                 [activity unavailable] -> [Record refund] -> [Pay refund later] -> ◎ Tour confirmed with refund
 Data stores: Packages DB, Bookings DB""", size=7.5)
    _q(n, "2020-21 Q1(a) — Life-insurance premium: BPMN diagram (14)")
    code(n, """Pool: Insurance Company — lanes: Underwriting | Billing | Client (black box pool, message flows)
 Underwriting: ○ Policy application received -> [Check job and salary and age] -> <X>
     [stable job and salary > 50,000 and age < 40] -> [Set Gold rate]
     [otherwise] -> [Set Gold rate + 20 %] -> <X> -> [Record payment mode (monthly/yearly; cheque/mobile)]
 Billing: ○(timer) Before each due date -> [Compute amount (+10 % penalty if previous missed)] -> [Send SMS with amount] ··SMS··> Client
          -> <event-based gateway> -> (payment received) -> [Record payment; reset missed count] -> ◎ Premium paid
                                    -> (timer: due date passed) -> [Increment missed count] -> <X>
                                          [missed = 2 successive] -> [Cancel policy] -> ◎ Policy cancelled
                                          [missed = 1] -> [Flag 10 % penalty on next premium] -> ◎ Premium overdue""", size=7.5)
    _q(n, "2021-22 Q3(a)(b) — ATM: use case diagram and use cases (8+8)")
    code(n, """Actors: Customer (primary); Core Banking System, Mobile Operator (secondary)
Customer ---- (Withdraw Money), (Check Balance), (Change PIN), (Deposit Money), (Transfer Money), (Recharge Mobile)
each ··«include»··> (Authenticate (insert card + PIN))
(Check Balance) ---- Core Banking System    (Transfer Money), (Withdraw), (Deposit) ---- Core Banking System
(Recharge Mobile) ---- Mobile Operator      (Print Receipt) ··«extend»··> (Withdraw Money) [receipt requested]""")
    n.table(["Use case", "Main flow / alternatives"], [
        ["Withdraw Money", "Pre: card valid. 1 Customer inserts card, enters PIN; system authenticates. 2 Selects Withdraw, "
         "enters amount. 3 System checks balance and limits with core banking. 4 Debits account, dispenses cash, sends "
         "SMS. 5 Ejects card. Alt: 1a wrong PIN (3 times → card retained); 3a insufficient balance → message; "
         "4a dispenser fault → reverse debit."],
        ["Change PIN", "1 Customer authenticates. 2 Selects Change PIN, enters old PIN, new PIN twice. 3 System checks "
         "new PIN format (4 digits, not equal to old) and match. 4 Updates PIN in core banking, confirms. Alt: 3a "
         "mismatch or weak PIN → re-enter; 2a old PIN wrong → abort."],
    ], widths_cm=[3.0, 14.2], font_size=9)
    _q(n, "2021-22 Q5(a) — MPO teacher recruitment: BPMN diagram (13)")
    code(n, """Pools: Candidate ··· Recruitment Authority (lanes: Online Portal | Verification Committee)
 Portal: ○ Application received ··application··< Candidate -> [Identify post (subject, grade, institution type)]
         -> [Load qualification criteria] -> <+> [Check age (with quota relaxation)] [Check degree subject] [Check results per level] <+>
         -> <X> [all criteria met] -> [Mark eligible] -> [Issue admit card for recruitment test] ··admit card··> Candidate -> ◎ Eligible
                [any criterion failed] -> [Record failed criteria] -> [Notify rejection with reasons] ··notice··> Candidate -> ◎ Not eligible
 Data stores: Qualification Criteria DB, Applications DB""", size=7.5)
    _q(n, "2022-23 Q1(a) — Bangla Academy book stock: BPMN diagram (15)")
    code(n, """Pool: Bangla Academy — lanes: Online Sales (Facebook page) | Outlet | Fair Team | Stock & Accounts
 Online:  ○ Order received ··order··< Customer -> [Check stock] -> [Apply discount] -> [Deliver from stock] -> [Record sale] -> ◎ Order delivered
 Outlet:  ○ Customer at outlet -> [Sell copies (apply member/bulk discount)] -> [Record sale] -> ◎ Sale done
 Fair:    ○ Fair demand received -> [Allocate books from stock] -> [Transfer to fair] -> [Sell at fair (fair discount)]
          -> ○(timer) Fair ends -> [Count unsold books] -> [Return unsold to stock]
          -> (Stock & Accounts) [Reconcile: sent = sold + returned] -> <X> [mismatch] -> [Investigate / adjust] -> ◎ Reconciled
                                                                        [match] ------------------------------> ◎ Reconciled
 Stock & Accounts: every [Record sale] -> [Update stock] -> [Post financial transaction] -> (Dashboard: real-time stock & sales)
 Data stores: Stock DB, Sales & Finance DB, Discount rules DB""", size=7.5)
    _q(n, "2023-24 Q6(a) — Quest & Player Interaction subsystem: use case diagram (15)")
    code(n, """System boundary: Quest & Player Interaction Subsystem
Primary actors: Player, Game Master, Healer, Item Merchant, Lobby Manager
Secondary actors: Authentication System, Payment Gateway, Reward System
Player ---- (Join Quest), (Complete Quest), (View Achievements), (Purchase In-game Item)
Game Master ---- (Assign Quest), (Update Mission Outcome), (View Player Profile)
Healer ---- (Update Player Health), (View Active Missions)
Item Merchant ---- (Deliver Virtual Item)        Lobby Manager ---- (Schedule Tournament Match)
(Join Quest), (Complete Quest), (Assign Quest) ··«include»··> (Log In) ---- Authentication System
(Purchase In-game Item) ··«include»··> (Verify Payment Eligibility) ---- Payment Gateway
(Complete Quest) ··«include»··> (Generate Bonus Points) ---- Reward System
(Request Healing) ··«extend»··> (Join Quest)   extension point: 'player health low'""", size=8)
    _q(n, "2023-24 Q7(b) — Three types of BPMN flow objects (10)")
    n.table(["Flow object", "Symbol", "Kinds / example"], [
        ["Event", "circle (thin start, double intermediate, thick end)", "start: Order received; timer: Every 3 months; end: Order fulfilled"],
        ["Activity", "rounded rectangle", "task 'Check stock availability'; sub-process 'Handle payment'"],
        ["Gateway", "diamond", "XOR (one branch): stock available?; AND (all branches): ship ‖ invoice; OR (some): Amsterdam/Hamburg"],
    ], widths_cm=[2.6, 5.4, 9.2], font_size=9)
    _q(n, "2023-24 Q7(c) — Choosing the diagram for three projects (15)")
    n.table(["Project", "Diagram and why", "Limitation"], [
        ["1 Fitness app for non-technical investors", "Use case diagram — shows who uses the system and what they can do, in "
         "simple pictures without technical detail", "shows no order of steps, data or business rules"],
        ["2 Role-based access (admin, manager, employee)", "Use case diagram (actors as roles, generalisation of actors) — "
         "makes each role's permitted functions explicit", "does not show how permissions are enforced or data structure"],
        ["3 CRM order fulfilment, departments, bottlenecks", "BPMN with pools/lanes — shows flow across departments, who does "
         "which task, waits and gateways where bottlenecks occur", "does not model the software's data/class structure"],
    ], widths_cm=[4.4, 8.0, 4.8], font_size=8.5)


SECTIONS = {"A3": sec_A3, "A4": sec_A4, "A5": sec_A5, "A6": sec_A6}


def section(n, key, code):
    """Writes the senior diagram practice section for note file `key` (A3–A6)."""
    n.h1("Senior Diagram Practice — AI Sir (CSE 325 Information System Design)")
    n.source("Questions from 'CSE 213/AI Sir Diagram question from seniors' (CSE 325 papers 2017-18 to 2023-24), "
             "cited as 'AI Sir <session> p.N'. Each is solved below in the notation of this note file.")
    n.callout("focus", "These are the diagram questions AI Sir set in CSE 325. They use the same notations as this note "
              "file, so practise them after the lessons above. Draw the diagram first, then check it against the solution.")
    SECTIONS[key](n, code)
