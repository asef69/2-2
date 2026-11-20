"""paper.py - the mock question paper (story builder)."""
from pdfkit import *  # noqa: F401,F403

Q1B = """class ReportService {
    String generate(List<Sale> sales, String format) {
        double total = 0;
        for (Sale s : sales) total += s.amount;
        String out;
        if (format.equals("PDF"))      out = "PDF:" + total;
        else if (format.equals("CSV")) out = "CSV," + total;
        else                           out = "TXT " + total;
        Database db = new MySqlDatabase();
        db.save(out);
        return out;
    }
}"""

Q4B = """ 1  int process(int n, int k) {
 2      int s = 0, i = 1;
 3      while (i <= n) {
 4          if (i % 2 == 0 || i > k)
 5              s += i;
 6          else
 7              s -= 1;
 8          i++;
 9      }
10      if (s < 0)
11          s = 0;
12      return s;
13  }"""

Q8A = """class Invoice {
    String customerType;   // "GOLD", "SILVER" or "REGULAR"
    String country;        // "BD", "IN" or anything else
    double amount;
    int items;

    double total() {
        double t = amount;
        if (customerType.equals("GOLD"))         t = t - t * 0.15;
        else if (customerType.equals("SILVER"))  t = t - t * 0.10;
        else if (customerType.equals("REGULAR")) t = t - t * 0.02;
        if (country.equals("BD"))      t = t + t * 0.15;
        else if (country.equals("IN")) t = t + t * 0.18;
        else                           t = t + t * 0.25;
        if (items > 50) t = t - 100;
        return t;
    }

    void print() {
        System.out.println("Customer: " + customerType + ", " + country);
        System.out.println("Total: " + total());
    }
}"""

Q8B = """public class Account {
    private double balance;
    public Account(double opening) {
        if (opening < 0) throw new IllegalArgumentException("opening < 0");
        balance = opening;
    }
    // throws a checked InsufficientFundsException
    public void withdraw(double amt) throws InsufficientFundsException {
        if (amt <= 0)      throw new IllegalArgumentException("amount must be positive");
        if (amt > balance) throw new InsufficientFundsException();
        balance -= amt;
    }
    public double getBalance() { return balance; }
}"""


def story(fw):
    s = []
    A = lambda *a: s.append(part(*a, fw))  # noqa: E731

    # ---------------------------------------------------------------- cover
    s += [P("MOCK TERM FINAL EXAMINATION", "title"), P("CSE 213 &nbsp;•&nbsp; Software Engineering", "sub"),
          P("Full marks: 210 &nbsp;•&nbsp; Time: 3 hours &nbsp;•&nbsp; Practice paper (not a real past paper)", "sub"), Spacer(1, 6)]
    s.append(P("Instructions", "h2"))
    s.append(table([
        ["<b>#</b>", "<b>Rule</b>"],
        ["1", "There are <b>8 questions</b>, 4 in Section A and 4 in Section B. Every question carries <b>35 marks</b>."],
        ["2", "In each section, <b>Question 1 (Q1 / Q5) is compulsory</b>. Answer <b>any two</b> of the remaining three questions."
              " So you answer 6 questions in all: 6 × 35 = 210."],
        ["3", "Draw diagrams neatly and label every class, state, actor and message. Java code may be written in outline"
              " but must compile logically (types, constructors, method signatures)."],
        ["4", "Show every step of calculations. Marks for each part are printed in square brackets."],
        ["5", "Sit the paper under exam conditions (3 hours, no notes), then mark yourself with the separate solutions file."],
    ], [1.0 * cm, fw - 1.0 * cm]))
    s.append(Spacer(1, 6))

    # ================================================================ SECTION A
    s += [banner("SECTION A — Design principles, creational patterns, UML diagrams, software testing"), Spacer(1, 2)]

    # ---- Q1
    s.append(P("Question 1 &nbsp;(compulsory) &nbsp;[35]", "q"))
    A("(a)", 15, [P("<b>TastyGo</b> is a food-delivery app that runs in Dhaka and Chattogram. Each city has its own <i>delivery-fee"
                    " calculator</i> (Dhaka: 40 + 10 per km; Chattogram: 30 + 12 per km) and its own <i>rider allocator</i> (Dhaka:"
                    " nearest free rider; Chattogram: rider with the fewest deliveries today). The fee calculator and the allocator"
                    " of one city must always be used together. The order-processing code must not name any city-specific class,"
                    " and a third city must be addable without editing the order-processing code."),
                  P("(i) Name the design pattern and justify it. [3] &nbsp;(ii) Draw the class diagram. [6] &nbsp;(iii) Write the Java code for the"
                    " abstract products, the Dhaka concrete classes, the factory types and the client <font face='Mono'>OrderService</font>. [6]")])
    A("(b)", 10, [P("The class below breaks several design principles."), code(Q1B),
                  P("(i) Name <b>three</b> violated principles and point to the code that violates each. [4] &nbsp;(ii) Refactor the design"
                    " (class outline and key code) so that all three are fixed. [6]")])
    A("(c)", 10, [P("Write a <b>thread-safe, lazily initialised Singleton</b> <font face='Mono'>ConfigManager</font> that loads application"
                    " settings once. Explain why the naive lazy version is unsafe with several threads, and give two situations where a Singleton is a"
                    " poor design choice. [5 + 3 + 2]")])

    # ---- Q2
    s.append(P("Question 2 &nbsp;[35]", "q"))
    A("(a)", 20, [P("Draw a UML <b>class diagram</b> for the following <b>campus library</b> system. Show attributes, key operations,"
                    " generalisation, aggregation/composition, multiplicity at every association end, and model <i>Loan</i> as an"
                    " <b>association class</b>."),
                  *bullets(["A <i>Library</i> keeps many <i>Books</i> and many <i>Members</i> (both exist independently of the library object).",
                            "A <i>Member</i> (id, name, email) is either a <i>Student</i> (department, level) or a <i>Faculty</i> (designation)."
                            " A plain Member is never created directly.",
                            "A <i>Book</i> (isbn, title) has one or more physical <i>Copies</i> (copyId, status). A Copy cannot exist without its Book.",
                            "A Member may borrow up to 5 Copies at a time. A Copy is on at most one open loan. Each <i>Loan</i> records issueDate,"
                            " dueDate and returnDate and is issued by exactly one <i>Librarian</i> (staff id, name).",
                            "A late return creates a <i>Fine</i> (amount, paid). A Fine belongs to one Loan only and is deleted with it; a Loan has"
                            " at most one Fine."])])
    A("(b)", 15, [P("An online <b>Order</b> behaves as follows. It starts as <i>Placed</i>. Payment succeeding moves it to <i>Paid</i>; a failed payment"
                    " is retried (the order stays Placed) up to 3 times, after the third failure the order is <i>Cancelled</i>. The customer may cancel"
                    " in Placed or Paid (a Paid cancellation also refunds the money). Paid orders become <i>Packed</i>, then <i>Shipped</i>."
                    " Cancellation is impossible once Shipped. A shipped order becomes <i>Delivered</i>. A Delivered order is <i>Closed</i>"
                    " automatically after 7 days unless the customer requests a return within that period, in which case it becomes <i>Returned</i>"
                    " and is Closed after the refund."),
                  P("(i) Draw the UML state diagram with events, guards, actions, the initial state and the final states. [11] &nbsp;(ii) State the"
                    " kind of UML event (call, signal, time or change) of each trigger: <i>pay</i> (the customer invokes it on the order),"
                    " <i>payFail</i> (a notification sent by the payment gateway), <i>after(7 days)</i> and <i>when(attempts = 3)</i>."
                    " How does a guard differ from a change event? [4]")])

    # ---- Q3
    s.append(P("Question 3 &nbsp;[35]", "q"))
    A("(a)", 20, [P("<b>PayPoint</b> is a mobile wallet. Read the description and answer (i) and (ii)."),
                  *bullets(["<i>Customers</i> and <i>Agents</i> are both kinds of <i>User</i>.",
                            "A Customer can <i>send money</i>, <i>pay a bill</i>, <i>check balance</i> and <i>link a bank account</i>."
                            " The bank (an external system) confirms every link request.",
                            "Sending money, paying a bill and cash-in all require <i>verifying the PIN</i> first (the same step every time).",
                            "A transfer above 25,000 BDT additionally triggers an OTP check (only for such transfers)."
                            " A customer may optionally apply a promo code while paying a bill.",
                            "An Agent performs <i>cash-in</i> for a customer.",
                            "An <i>Admin</i> can block an account and generate reports."]),
                  P("(i) Draw the use case diagram. [12] &nbsp;(ii) Write the use case description (name, actor, precondition, main flow,"
                    " two alternate flows, postcondition) for <i>Send Money</i>. [8]")])
    A("(b)", 15, [P("From the <i>Send Money</i> use case: the Customer enters receiver and amount in the App; the App asks the TransferService to"
                    " transfer; the TransferService asks the Ledger for the sender's balance. If the balance is enough, the Ledger is told to debit the"
                    " sender and credit the receiver and the customer sees a confirmation; otherwise the customer sees an “insufficient funds” error."),
                  P("(i) Draw the UML sequence diagram (use an <font face='Mono'>alt</font> fragment and activation bars). [10] &nbsp;"
                    "(ii) Redraw the <i>success path</i> as a collaboration diagram with numbered messages. [5]")])

    # ---- Q4
    s.append(P("Question 4 &nbsp;[35]", "q"))
    A("(a)", 15, [P("A ride-hailing app computes <font face='Mono'>fare(distance, passengers)</font>. <i>distance</i> is an integer"
                    " number of km that must be from 1 to 50 inclusive; <i>passengers</i> is an integer that must be from 1 to 6 inclusive;"
                    " anything outside these ranges is rejected with an error."),
                  P("(i) List the valid and invalid equivalence classes for each input. [3] &nbsp;(ii) How many test cases are needed for"
                    " <b>weak</b> and for <b>strong</b> equivalence class testing? Write the weak set. [4] &nbsp;(iii) Derive the boundary-value"
                    " (BVA) values for both inputs and give the complete <b>robust BVA</b> test set (single-fault assumption), with the"
                    " nominal values 25 km and 3 passengers. [8]")])
    A("(b)", 20, [P("Consider this method. <i>Treat every simple condition of a compound condition as its own predicate node.</i>"), code(Q4B),
                  P("(i) Draw the control-flow graph (number nodes by line, merging straight-line code). [4] &nbsp;(ii) Compute the cyclomatic"
                    " complexity three ways. [4] &nbsp;(iii) Give a set of independent basis paths with concrete input values and the expected"
                    " return value for each. [8] &nbsp;(iv) What is the smallest number of test cases giving 100 % <b>branch</b> coverage? Give them,"
                    " and say whether the same set also achieves <b>condition</b> coverage. [4]")])

    # ================================================================ SECTION B
    s += [Spacer(1, 4), banner("SECTION B — Structural and behavioural patterns, process models and agile, unit testing, refactoring, ethics and requirements", GREEN), Spacer(1, 2)]

    # ---- Q5
    s.append(P("Question 5 &nbsp;(compulsory) &nbsp;[35]", "q"))
    A("(a)", 15, [P("<b>TalkNet</b>, a mobile operator, sells a <i>Basic plan</i> (500 BDT, “10 GB data”). Customers can add any combination of"
                    " add-ons at run time: <i>SocialPack</i> (+100 BDT), <i>VideoPack</i> (+150 BDT) and <i>RoamingPack</i> (+200 BDT). Every plan"
                    " must report its total <font face='Mono'>cost()</font> and a <font face='Mono'>description()</font> such as"
                    " “Basic + Social + Video”. More add-ons will be launched next year."),
                  P("(i) Name the pattern; say why plain inheritance fails here (how many subclasses would it need for the three add-ons?). [3]"
                    " &nbsp;(ii) Draw the class diagram. [6] &nbsp;(iii) Write the Java code for the component interface, the Basic plan, the decorator base class,"
                    " <font face='Mono'>VideoPack</font>, and a client that builds <i>Basic + Social + Video</i> and prints its cost and"
                    " description. [6]")])
    A("(b)", 10, [P("A river-flood <b>early-warning station</b> reads the water level every minute. An SMS gateway, a city dashboard and a siren"
                    " controller must all be informed whenever the level changes. Subscribers must be attachable and removable at run time, and"
                    " the station must not depend on any concrete subscriber class."),
                  P("(i) Name the pattern and map its roles to this scenario. [3] &nbsp;(ii) Draw the class diagram. [4] &nbsp;(iii) Write the Java"
                    " <font face='Mono'>attach</font>, <font face='Mono'>detach</font> and <font face='Mono'>notifyObservers</font> methods of the"
                    " subject. [3]")])
    A("(c)", 10, [P("The new system uses <font face='Mono'>interface Printer { void print(Document d); }</font>. A vendor library class"
                    " <font face='Mono'>OldLaser</font> has <font face='Mono'>void printText(String text, int copies)</font> and cannot be changed."
                    " Write an <b>object adapter</b> so the new system can use <font face='Mono'>OldLaser</font> (assume"
                    " <font face='Mono'>Document</font> has <font face='Mono'>getText()</font>), and explain how a <b>class adapter</b> would differ and why Java"
                    " programmers usually prefer the object adapter. [6 + 4]")])

    # ---- Q6
    s.append(P("Question 6 &nbsp;[35]", "q"))
    A("(a)", 15, [P("A campus group-chat tool lets users post messages to a room. At present every <font face='Mono'>User</font> object keeps"
                    " references to all other users and calls <font face='Mono'>receive()</font> on each of them (n² links), and adding a"
                    " “muted users” rule means editing the User class. Redesign it with a suitable pattern."),
                  P("(i) Name the pattern and list its roles in this scenario. [2] &nbsp;(ii) Draw the class diagram. [5] &nbsp;(iii) Write the Java code"
                    " (<font face='Mono'>ChatMediator</font>, <font face='Mono'>ChatRoom</font>, <font face='Mono'>User</font>), including the"
                    " muting rule inside the mediator. [8]")])
    A("(b)", 10, [P("A file explorer shows <i>Files</i> (with a size in KB) and <i>Folders</i> that can contain Files or other Folders to any depth."
                    " The client must call <font face='Mono'>getSize()</font> on a file or a folder in exactly the same way; a folder's size is the sum"
                    " of its contents. Name the pattern, draw its class diagram [4] and write the Java code. [6]")])
    A("(c)", 10, [P("A UI toolkit has shapes <i>Circle</i> and <i>Square</i>, each of which can be drawn by a <i>VectorRenderer</i> or a"
                    " <i>RasterRenderer</i>. (i) How many concrete classes are needed if every combination is a subclass of Shape, and how many after"
                    " you add <i>Triangle</i> and a third renderer, <i>GpuRenderer</i>? [3] &nbsp;(ii) Redesign with the <b>Bridge</b> pattern: class diagram"
                    " [4] and the number of classes needed after the same two additions. [3]")])

    # ---- Q7
    s.append(P("Question 7 &nbsp;[35]", "q"))
    A("(a)", 15, [P("The Ministry of Education asks your company to build a <b>result-publication portal</b>. The requirements are well understood"
                    " and will not change much; the contract deadline is fixed at 8 months. The ministry wants a working version for <i>one</i> board"
                    " by month 4 and for all boards by month 8. The riskiest part is integration with an unreliable legacy database."),
                  P("Recommend a process model and justify the choice against the scenario. [7] Explain why <b>two</b> other models you reject are less"
                    " suitable. [6] Draw the process flow of your model. [2]")])
    A("(b)", 10, [P("Describe the <b>Scrum</b> framework: the three roles [3], the events of one sprint in order [4], and the difference between the"
                    " product backlog and the sprint backlog. [3]")])
    A("(c)", 10, [P("A team uses a <b>Kanban</b> board with columns <i>To Do → Develop (WIP 3) → Test (WIP 2) → Done</i>. Today Develop holds"
                    " 3 items (one of them finished), Test holds 2 items, To Do holds 6 items. (i) Draw the board. [3] &nbsp;(ii) A developer has just finished item D7. May"
                    " she pull the next To Do item? What should she do? Explain the principle. [4] &nbsp;(iii) Item D2 was requested on day 1, work started on"
                    " day 4 and it was delivered on day 9. Find its lead time and cycle time. [3]")])

    # ---- Q8
    s.append(P("Question 8 &nbsp;[35]", "q"))
    A("(a)", 15, [P("Study this class."), code(Q8A),
                  P("(i) Identify <b>four</b> code smells, quoting the evidence. [6] &nbsp;(ii) Refactor the class; name the refactoring you apply for"
                    " each smell and show the resulting code. [9]")])
    A("(b)", 10, [P("Using the <font face='Mono'>Account</font> class below, write a <b>JUnit 4</b> test class. Use a fixture, test a normal withdrawal, the"
                    " exact-balance boundary, and the three failure cases. Show how floating-point results and exceptions are asserted."), code(Q8B)])
    A("(c)", 10, [P("<b>Ethics.</b> While testing a fitness app, Rahim finds that it sends users' precise location to an advertising partner even when the"
                    " “Do not share” switch is on. The product manager asks him to say nothing until after launch, because a delay would lose the"
                    " contract. (i) Which <b>three</b> principles of the ACM / IEEE-CS Software Engineering Code of Ethics are at stake? What should Rahim do,"
                    " step by step? [6] &nbsp;<b>Requirements.</b> (ii) Rewrite “The system should be fast” and “The app must be user-friendly”"
                    " as verifiable requirements, and say which kind of requirement they are. [4]")])

    s += [Spacer(1, 10), P("— End of paper —", "sub")]
    return s
