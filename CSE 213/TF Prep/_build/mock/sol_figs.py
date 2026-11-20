"""sol_figs.py - every diagram used in the model answers of mock paper v2."""
from reportlab.lib import colors

from figs import Fig

AMB = colors.Color(0.99, 0.93, 0.78)
GRN = colors.Color(0.88, 0.96, 0.89)
RED = colors.Color(0.99, 0.89, 0.88)
BLU = colors.Color(0.90, 0.94, 0.99)


# ------------------------------------------------------------------------------------------- Q1
def d_usecase():
    f = Fig(545, 335, "Use case diagram of MediLink")
    f.frame(86, 6, 374, 322, "MediLink")
    f.actor("Patient", 14, 215, side="top")
    f.actor("Receptionist", 14, 50, side="top")
    f.actor("Doctor", 490, 235, side="top")
    f.actor("Admin", 490, 128, side="top")
    f.actor("SMS Gateway", 490, 22, side="top")
    f.ellipse("Book Appointment", 98, 290, 110, 26)
    f.ellipse("Cancel Appointment", 98, 244, 110, 26)
    f.ellipse("View Prescription", 98, 198, 110, 26)
    f.ellipse("Pay Bill", 98, 152, 110, 26)
    f.ellipse("Register Patient", 98, 106, 110, 26)
    f.ellipse("Confirm Appointment", 98, 60, 110, 26)
    f.ellipse("Collect Cash Payment", 98, 14, 110, 26, size=7)
    f.ellipse("Check Availability", 232, 290, 100, 26)
    f.ellipse("Log In", 232, 214, 100, 26)
    f.ellipse("Apply Insurance", 232, 152, 100, 26)
    f.ellipse("Send Reminder", 232, 60, 100, 26)
    f.ellipse("View Schedule", 350, 290, 100, 26)
    f.ellipse("Issue Prescription", 350, 244, 100, 26)
    f.ellipse("Manage Staff Accounts", 350, 120, 100, 28, size=7)
    for u in ("Book Appointment", "Cancel Appointment", "View Prescription", "Pay Bill", "Register Patient"):
        f.edge("Patient", u, "assoc")
    for u in ("Register Patient", "Confirm Appointment", "Collect Cash Payment"):
        f.edge("Receptionist", u, "assoc")
    f.edge("Doctor", "View Schedule", "assoc")
    f.edge("Doctor", "Issue Prescription", "assoc")
    f.edge("Admin", "Manage Staff Accounts", "assoc")
    f.edge("SMS Gateway", "Send Reminder", "assoc")
    f.edge("Book Appointment", "Check Availability", "dashed", "«include»", lpos=(220, 306))
    f.edge("Confirm Appointment", "Send Reminder", "dashed", "«include»", lpos=(222, 80))
    f.edge("Apply Insurance", "Pay Bill", "dashed", "«extend»", lpos=(222, 170))
    f.edge("Issue Prescription", "Log In", "dashed", "«include»", lpos=(332, 240))
    f.edge("View Prescription", "Log In", "dashed")
    f.edge("Manage Staff Accounts", "Log In", "dashed")
    f.text(232, 38, "every other use case also «include»s Log In", 6.8, "SegI")
    f.text(232, 29, "(arrows left out to keep the diagram readable)", 6.8, "SegI")
    return f


def d_account_state():
    f = Fig(545, 262, "State diagram of a MediLink account (Locked, Active and Expired sit inside the Enabled superstate)")
    f.frame(8, 20, 428, 232, "Enabled", dashed=True)
    f.start("s0", 24, 130)
    f.state("Active", 112, 112, 100, 46)
    f.state("Locked", 318, 190, 100, 34)
    f.state("Expired", 318, 56, 100, 34)
    f.state("Disabled", 466, 120, 72, 36)
    f.end("fin", 497, 66)
    f.edge("s0", "Active", "arrow", "account created", lpos=(66, 140))
    f.edge("Active", "Active", "arrow", via=[(140, 178), (186, 178)])
    f.text(163, 184, "wrongPassword [attempts < 3] / attempts++", 6.8, align="center")
    f.edge("Active", "Locked", "arrow")
    f.text(222, 234, "wrongPassword", 6.8)
    f.text(222, 226, "[attempts == 3]", 6.8)
    f.text(222, 218, "/ lock()", 6.8)
    f.edge("Locked", "Active", "arrow", via=[(368, 128)])
    f.text(232, 150, "after(15 min), adminUnlock", 6.8)
    f.text(232, 142, "/ attempts = 0", 6.8)
    f.edge("Active", "Expired", "arrow")
    f.text(224, 93, "after(90 days)", 6.8)
    f.edge("Expired", "Active", "arrow", via=[(368, 36), (162, 36)])
    f.text(190, 40, "changePassword / resetExpiry()", 6.8)
    f.edge((436, 138), "Disabled", "arrow")
    f.text(470, 166, "disable [by Admin]", 6.8, "SegB", align="center")
    f.text(470, 158, "(from any Enabled state)", 6.2, "SegI", align="center")
    f.edge("Disabled", "fin", "arrow")
    return f


# ------------------------------------------------------------------------------------------- Q2
def d_observer():
    f = Fig(540, 245, "Observer: Match is the subject; the three displays are observers that can attach and detach at run time")
    f.cls("Subject", 10, 175, 160, [], ["*+attach(o: Observer)", "*+detach(o: Observer)", "*+notifyObservers()"], stereo="interface")
    f.cls("Match", 10, 60, 160, ["-observers: List<Observer>", "-runs: int", "-wickets: int", "-overs: double"],
          ["+updateScore(r, w, o)", "+attach(o) / detach(o)", "+notifyObservers()"])
    f.cls("Observer", 300, 200, 175, [], ["*+update(runs, wickets, overs)"], stereo="interface")
    f.cls("MobileWidget", 215, 45, 98, [], ["+update(..)"])
    f.cls("WebsitePanel", 322, 45, 98, [], ["+update(..)"])
    f.cls("SmsAlert", 430, 45, 98, [], ["+update(..)"])
    f.edge("Match", "Subject", "realize")
    f.edge("Subject", "Observer", "arrow", "observers 0..*", lpos=(235, 224))
    for n in ("MobileWidget", "WebsitePanel", "SmsAlert"):
        f.edge(n, "Observer", "realize")
    f.text(10, 32, "roles: Subject = Subject, ConcreteSubject = Match,", 6.8, "SegI")
    f.text(10, 23, "Observer = Observer, ConcreteObservers = the three displays", 6.8, "SegI")
    return f


def d_composite():
    f = Fig(540, 235, "Composite: a Panel is a Widget that holds Widgets; Window is a top-level Panel")
    f.cls("Widget", 175, 180, 190, [], ["*+draw()", "*+getWidth(): int"], abstract=True)
    f.cls("Label", 8, 100, 110, ["-text: String"], ["+draw()", "+getWidth(): int"])
    f.cls("Button", 130, 100, 110, ["-caption: String"], ["+draw()", "+getWidth(): int"])
    f.cls("Panel", 290, 85, 190, ["-children: List<Widget>"], ["+add(w: Widget)", "+remove(w: Widget)", "+draw()", "+getWidth(): int"])
    f.cls("Window", 330, 8, 110, ["-title: String"], [])
    f.edge("Label", "Widget", "inherit")
    f.edge("Button", "Widget", "inherit")
    f.edge("Panel", "Widget", "inherit")
    f.edge("Panel", "Widget", "aggr", "children", mb="*", via=[(500, 130), (500, 215)], lpos=(517, 172))
    f.edge("Window", "Panel", "inherit")
    f.text(8, 62, "Component = Widget   •   Leaf = Label, Button", 7, "SegB")
    f.text(8, 51, "Composite = Panel (Window specialises it)", 7, "SegB")
    f.text(8, 40, "draw() on a Panel loops over children and calls draw() on each", 6.8, "SegI")
    return f


# ------------------------------------------------------------------------------------------- Q3
def d_cfg():
    f = Fig(540, 330, "Control-flow graph of averageOfPositives (node label = line number; T/F = outcome of the decision)")
    nd = {"2": (255, 305), "3": (95, 262), "4": (255, 262), "5": (255, 218), "6": (330, 172), "7": (330, 124), "inc": (415, 148),
          "11": (175, 172), "12": (120, 124), "13": (230, 124), "X": (170, 62)}
    for k, (x, y) in nd.items():
        f.circle(k, x - 12, y - 12, 24, text=k if k != "inc" else "i++", size=7.5)
    f.edge("2", "3", "arrow", "T", lpos=(175, 298))
    f.edge("2", "4", "arrow", "F", lpos=(262, 284))
    f.edge("3", "X", "arrow", via=[(38, 262), (38, 62)])
    f.edge("4", "5", "arrow")
    f.edge("5", "6", "arrow", "T", lpos=(302, 202))
    f.edge("5", "11", "arrow", "F", lpos=(208, 200))
    f.edge("6", "7", "arrow", "T", lpos=(343, 150))
    f.edge("6", "inc", "arrow", "F", lpos=(392, 170))
    f.edge("7", "inc", "arrow")
    f.edge("inc", "5", "arrow", via=[(415, 218)])
    f.edge("11", "12", "arrow", "T", lpos=(138, 152))
    f.edge("11", "13", "arrow", "F", lpos=(215, 152))
    f.edge("12", "X", "arrow")
    f.edge("13", "X", "arrow")
    notes = {"2": ("a==null || a.length==0", 18, -3), "3": ("return -1", -42, -22), "4": ("sum=0, count=0, i=0", 17, -3), "5": ("i < a.length", -75, 4),
             "6": ("a[i] > 0", 16, 8), "7": ("sum+=a[i]; count++", 16, -14), "11": ("count == 0", -62, 8), "12": ("return 0", -42, -20),
             "13": ("return sum/count", 16, -3), "X": ("exit", 16, -3)}
    for k, (t, dx, dy) in notes.items():
        x, y = nd[k]
        f.text(x + dx, y + dy, t, 7, "SegI")
    f.text(8, 18, "N = 11 nodes, E = 14 edges, P = 4 decisions (lines 2, 5, 6, 11)", 7.2, "SegB")
    return f


def d_tdd():
    f = Fig(540, 92, "The TDD cycle")
    f.state("RED", 30, 30, 120, 40, ["write a failing", "test first"], size=8, fill=RED)
    f.state("GREEN", 210, 30, 120, 40, ["write the simplest", "code that passes"], size=8, fill=GRN)
    f.state("REFACTOR", 390, 30, 120, 40, ["clean the code,", "keep the bar green"], size=8, fill=BLU)
    f.edge("RED", "GREEN", "arrow", "test fails -> code", lpos=(180, 62))
    f.edge("GREEN", "REFACTOR", "arrow", "test passes", lpos=(360, 62))
    f.edge("REFACTOR", "RED", "arrow", "next test", via=[(450, 12), (90, 12)], lpos=(270, 15))
    return f


# ------------------------------------------------------------------------------------------- Q4
def d_accounts():
    f = Fig(545, 392, "Class diagram of the accounting package")
    f.cls("Account", 170, 282, 160, ["#id: String", "#title: String", "#balance: double"],
          ["*+deposit(amount: double)", "*+withdraw(amount: double)", "*+getBalance(): double"], abstract=True)
    f.cls("LedgerGroup", 405, 290, 135, ["-name: String"], ["+add(a: Account)", "+remove(a: Account)", "+getBalance(): double"])
    f.cls("Debtor", 20, 195, 125, ["-creditLimit: double"], [])
    f.cls("Creditor", 170, 195, 135, ["-paymentDueDate: Date"], [])
    f.cls("Transaction", 395, 175, 130, ["-id: int", "-date: Date", "-amount: double"], [])
    f.cls("Clerk", 395, 62, 130, ["-id: int", "-name: String"], ["+post(a: Account, amt: double)"])
    f.cls("Authenticator", 215, 72, 125, [], ["*+authenticate(): boolean"], stereo="interface")
    f.cls("PasswordStep", 20, 8, 95, [], [])
    f.cls("OtpStep", 125, 8, 75, [], [])
    f.cls("MultiStepAuthenticator", 215, 8, 160, [], ["+authenticate(): boolean"])
    f.edge("Debtor", "Account", "inherit")
    f.edge("Creditor", "Account", "inherit")
    f.edge("LedgerGroup", "Account", "inherit")
    f.edge("LedgerGroup", "Account", "aggr", ma="", mb="0..*", via=[(472, 380), (250, 380)], lpos=(350, 383))
    f.edge("Clerk", "Transaction", "assoc", "posts", ma="1", mb="*", lpos=(480, 150))
    f.edge("Transaction", "Account", "assoc", "posted to", ma="*", mb="1", lpos=(375, 248))
    f.edge("Clerk", "Authenticator", "arrow", "uses", lpos=(368, 90))
    f.edge("PasswordStep", "Authenticator", "realize")
    f.edge("OtpStep", "Authenticator", "realize")
    f.edge("MultiStepAuthenticator", "Authenticator", "realize")
    f.text(380, 14, "holds steps: List<Authenticator> (2..*)", 6.8, "SegI")
    f.text(380, 5, "runs them in order; a 3rd step = one new class", 6.8, "SegI")
    return f


def d_isp():
    f = Fig(540, 205, "Interface Segregation: one fat interface (left) versus small role interfaces (right)")
    f.frame(2, 2, 215, 196, "Violates ISP", dashed=True)
    f.cls("OfficeMachine", 40, 118, 140, [], ["*+print()", "*+scan()", "*+fax()"], stereo="interface")
    f.cls("BasicPrinter", 40, 18, 140, [], ["+print()", "+scan()  // throws", "+fax()   // throws"])
    f.edge("BasicPrinter", "OfficeMachine", "realize")
    f.frame(228, 2, 310, 196, "Follows ISP", dashed=True)
    f.cls("Printer", 236, 128, 82, [], ["*+print()"], stereo="interface")
    f.cls("Scanner", 330, 128, 82, [], ["*+scan()"], stereo="interface")
    f.cls("FaxMachine", 422, 128, 106, [], ["*+fax()"], stereo="interface")
    f.cls("BasicPrinter2", 236, 18, 88, [], ["+print()"])
    f.cls("OfficeCopier", 330, 18, 82, [], ["+print()", "+scan()"])
    f.cls("FaxDevice", 430, 18, 90, [], ["+fax()"])
    f.edge("BasicPrinter2", "Printer", "realize")
    f.edge("OfficeCopier", "Scanner", "realize")
    f.edge("OfficeCopier", "Printer", "realize", via=[(345, 90)])
    f.edge("FaxDevice", "FaxMachine", "realize")
    f.text(232, 7, "an AllInOne machine would simply implement all three", 6.6, "SegI")
    return f


# ------------------------------------------------------------------------------------------- Q5
def d_abstract_factory():
    f = Fig(540, 262, "Abstract Factory for BrewBox: two product families (Dhaka, Tokyo), one factory per region")
    f.cls("Cafe", 215, 215, 120, ["-factory: RegionFactory"], ["+serveSet()"])
    f.cls("RegionFactory", 20, 140, 145, [], ["*+createCoffee(): Coffee", "*+createSnack(): Snack"], stereo="interface")
    f.cls("Coffee", 215, 140, 110, [], ["*+name(): String"], stereo="interface")
    f.cls("Snack", 395, 140, 110, [], ["*+name(): String"], stereo="interface")
    f.cls("DhakaFactory", 0, 70, 95, [], [])
    f.cls("TokyoFactory", 62, 8, 105, [], [])
    f.cls("CardamomLatte", 190, 70, 100, [], [])
    f.cls("MatchaLatte", 255, 8, 92, [], [])
    f.cls("Samosa", 375, 70, 80, [], [])
    f.cls("Dorayaki", 448, 8, 85, [], [])
    f.edge("Cafe", "RegionFactory", "arrow", "uses", lpos=(165, 206))
    f.edge("Cafe", "Coffee", "depend")
    f.edge("Cafe", "Snack", "depend")
    for a, b in (("DhakaFactory", "RegionFactory"), ("TokyoFactory", "RegionFactory"), ("CardamomLatte", "Coffee"),
                 ("MatchaLatte", "Coffee"), ("Samosa", "Snack"), ("Dorayaki", "Snack")):
        f.edge(a, b, "realize")
    f.edge("DhakaFactory", "CardamomLatte", "depend", "«creates»", lpos=(142, 77))
    f.edge("TokyoFactory", "MatchaLatte", "depend", "«creates»", lpos=(210, 15))
    f.edge("DhakaFactory", "Samosa", "depend", via=[(48, 52), (415, 52)], lpos=(300, 55))
    f.edge("TokyoFactory", "Dorayaki", "depend", via=[(114, -2), (490, -2)], lpos=(300, -1))
    return f


def d_adapter_decorator():
    f = Fig(540, 230, "One class, two roles: SmsNotifier adapts SmsGateway to Notifier and decorates another Notifier")
    f.cls("Client", 10, 175, 90, [], [])
    f.cls("Notifier", 165, 170, 150, [], ["*+send(msg: String)"], stereo="interface")
    f.cls("EmailNotifier", 380, 180, 120, [], ["+send(msg: String)"])
    f.cls("SmsNotifier", 120, 40, 190, ["-gateway: SmsGateway", "-phoneNo: String", "-wrapped: Notifier"], ["+send(msg: String)"])
    f.cls("SmsGateway", 380, 50, 140, [], ["+push(phoneNo, text)"], stereo="vendor class")
    f.edge("Client", "Notifier", "arrow", "uses", lpos=(132, 192))
    f.edge("EmailNotifier", "Notifier", "realize")
    f.edge("SmsNotifier", "Notifier", "realize", via=[(215, 130)])
    f.edge("SmsNotifier", "SmsGateway", "arrow", "adapts (adapter)", lpos=(343, 76))
    f.edge("SmsNotifier", "Notifier", "aggr", "wraps (Decorator role)", mb="0..1", via=[(60, 80), (60, 150), (178, 150)], lpos=(70, 158))
    return f


# ------------------------------------------------------------------------------------------- Q7
def d_waterfall():
    f = Fig(540, 175, "The waterfall model: the five framework activities done once, in order")
    names = [("Communication", ["project initiation,", "requirements gathering"]), ("Planning", ["estimating,", "scheduling, tracking"]),
             ("Modeling", ["analysis and", "design"]), ("Construction", ["code and", "test"]), ("Deployment", ["delivery, support,", "feedback"])]
    for i, (n, ls) in enumerate(names):
        f.state(n, 2 + i * 108, 112 - i * 22, 92, 46, ls, size=8)
    for i in range(4):
        f.edge(names[i][0], names[i + 1][0], "arrow")
    f.text(270, 150, "no step back: a change found late means going round the whole model again", 7.2, "SegI", align="center")
    return f


def d_kanban():
    f = Fig(540, 205, "Kanban board today (WIP limits in brackets; a shaded card is finished but cannot move)")
    cols = [("Backlog", "", ["B1", "B2", "B3", "B4", "B5"]), ("Analysis", "(2)", ["A1"]), ("Development", "(3)", ["D1", "D2", "D3"]),
            ("Review", "(2)", ["R1", "R2"]), ("Done", "", ["K1", "K2", "K3", "K4"])]
    for i, (n, w, cards) in enumerate(cols):
        x = 4 + i * 107
        f.frame(x, 4, 100, 178)
        f.text(x + 50, 170, "%s %s" % (n, w), 8, "SegB", align="center")
        for j, c in enumerate(cards):
            fill = AMB if c == "D3" else (RED if (n == "Review") else colors.white)
            f.state(c, x + 14, 138 - j * 27, 72, 20, [], size=8, fill=fill)
    f.text(270, 192, "Development 3/3 and Review 2/2 are both full: the bottleneck is Review", 7.2, "SegI", align="center")
    return f


def d_scrum():
    f = Fig(540, 160, "One Scrum sprint")
    f.state("Product Backlog", 4, 100, 100, 36, ["ordered by the", "Product Owner"], size=8)
    f.state("Sprint Planning", 130, 100, 100, 36, ["goal + Sprint", "Backlog chosen"], size=8)
    f.state("Sprint (1-4 weeks)", 256, 100, 130, 36, ["build; Daily Scrum", "(15 min) every day"], size=8, fill=GRN)
    f.state("Increment", 412, 100, 118, 36, ["potentially", "shippable product"], size=8)
    f.state("Sprint Review", 256, 20, 130, 36, ["demo to stakeholders,", "update Product Backlog"], size=8)
    f.state("Retrospective", 78, 20, 130, 36, ["team improves", "its own process"], size=8)
    f.edge("Product Backlog", "Sprint Planning", "arrow")
    f.edge("Sprint Planning", "Sprint (1-4 weeks)", "arrow")
    f.edge("Sprint (1-4 weeks)", "Increment", "arrow")
    f.edge("Increment", "Sprint Review", "arrow", via=[(471, 38)])
    f.edge("Sprint Review", "Retrospective", "arrow")
    f.edge("Retrospective", "Product Backlog", "arrow", "next sprint", via=[(30, 38), (30, 90)], lpos=(64, 66))
    return f
