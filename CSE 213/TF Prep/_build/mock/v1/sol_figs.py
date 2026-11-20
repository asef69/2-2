"""sol_figs.py - every diagram used in the mock-paper model answers."""
from figs import Fig, sequence

FA = "≥"


def d_abstract_factory():
    f = Fig(540, 262, "Abstract Factory for TastyGo: two product families (Dhaka, Chattogram), one factory per city")
    f.cls("OrderService", 205, 215, 130, ["-factory: CityFactory"], ["+placeOrder(o: Order)"])
    f.cls("CityFactory", 20, 140, 135, [], ["*+createFeeCalculator(): FeeCalculator", "*+createAllocator(): RiderAllocator"], stereo="interface")
    f.cls("FeeCalculator", 205, 140, 130, [], ["*+fee(km: int): double"], stereo="interface")
    f.cls("RiderAllocator", 385, 140, 140, [], ["*+allocate(o: Order): Rider"], stereo="interface")
    f.cls("DhakaFactory", 0, 70, 95, [], [], size=7.5)
    f.cls("ChattogramFactory", 62, 8, 105, [], [], size=7.5)
    f.cls("DhakaFee", 190, 70, 85, [], [], size=7.5)
    f.cls("ChattogramFee", 255, 8, 92, [], [], size=7.5)
    f.cls("NearestRider", 375, 70, 92, [], [], size=7.5)
    f.cls("LeastBusyRider", 448, 8, 92, [], [], size=7.5)
    f.edge("OrderService", "CityFactory", "arrow", "uses", lpos=(160, 206))
    f.edge("OrderService", "FeeCalculator", "depend")
    f.edge("OrderService", "RiderAllocator", "depend")
    for a, b in (("DhakaFactory", "CityFactory"), ("ChattogramFactory", "CityFactory"), ("DhakaFee", "FeeCalculator"),
                 ("ChattogramFee", "FeeCalculator"), ("NearestRider", "RiderAllocator"), ("LeastBusyRider", "RiderAllocator")):
        f.edge(a, b, "realize")
    f.edge("DhakaFactory", "DhakaFee", "depend", "«creates»", lpos=(140, 77))
    f.edge("ChattogramFactory", "ChattogramFee", "depend", "«creates»", lpos=(210, 15))
    f.edge("DhakaFactory", "NearestRider", "depend", via=[(48, 52), (421, 52)], lpos=(300, 55))
    f.edge("ChattogramFactory", "LeastBusyRider", "depend", via=[(114, -2), (493, -2)], lpos=(300, -1))
    return f


def d_library():
    f = Fig(540, 340, "Campus library class diagram (Loan is an association class on Member–Copy)")
    f.cls("Library", 215, 300, 100, ["-name: String"], [])
    f.cls("Book", 20, 262, 110, ["-isbn: String", "-title: String"], ["+availableCopies(): int"])
    f.cls("Member", 385, 250, 130, ["-id: String", "-name: String", "-email: String"], ["*+borrowLimit(): int"], abstract=True)
    f.cls("Copy", 20, 150, 110, ["-copyId: String", "-status: String"], ["+isAvailable(): boolean"])
    f.cls("Student", 340, 110, 105, ["-department: String", "-level: int"], [])
    f.cls("Faculty", 455, 110, 85, ["-designation: String"], [])
    f.cls("Loan", 165, 105, 120, ["-issueDate: Date", "-dueDate: Date", "-returnDate: Date"], ["+isOverdue(): boolean"])
    f.cls("Librarian", 20, 20, 100, ["-staffId: String", "-name: String"], [])
    f.cls("Fine", 340, 20, 100, ["-amount: double", "-paid: boolean"], ["+pay()"])
    f.edge("Library", "Book", "aggr", ma="1", mb="*", via=[(75, 318)])
    f.edge("Library", "Member", "aggr", ma="1", mb="*", via=[(450, 318)])
    f.edge("Book", "Copy", "comp", ma="1", mb="1..*")
    f.edge("Student", "Member", "inherit")
    f.edge("Faculty", "Member", "inherit")
    f.edge("Copy", "Member", "assoc", "borrows", via=[(235, 215)], ma="0..5", mb="0..1", lpos=(235, 222))
    f.edge("Loan", (235, 215), "note")
    f.edge("Loan", "Librarian", "assoc", "issued by", ma="*", mb="1", lpos=(150, 70))
    f.edge("Loan", "Fine", "comp", ma="1", mb="0..1", lpos=(310, 90))
    return f


def d_order_state():
    f = Fig(540, 285, "State diagram of an Order")
    f.start("s0", 6, 214)
    f.state("Placed", 40, 200, 78, 36)
    f.state("Paid", 160, 200, 70, 36)
    f.state("Packed", 275, 200, 70, 36)
    f.state("Shipped", 390, 200, 78, 36)
    f.state("Delivered", 390, 110, 78, 36)
    f.state("Returned", 255, 110, 78, 36)
    f.state("Cancelled", 85, 95, 80, 36)
    f.state("Closed", 390, 30, 78, 36)
    f.end("e1", 118, 36)
    f.end("e2", 495, 41)
    f.edge("s0", "Placed", "arrow", "place order", lpos=(26, 246))
    f.edge("Placed", "Paid", "arrow", "pay [paymentOK]", lpos=(139, 240))
    f.edge("Placed", "Placed", "arrow", "payFail [attempts < 3] / attempts++", via=[(55, 258), (105, 258)], lpos=(80, 263))
    f.edge("Paid", "Packed", "arrow", "pack", lpos=(253, 240))
    f.edge("Packed", "Shipped", "arrow", "dispatch", lpos=(368, 240))
    f.edge("Shipped", "Delivered", "arrow", "delivered", lpos=(462, 175))
    f.edge("Delivered", "Closed", "arrow", "after(7 days)", lpos=(470, 83))
    f.edge("Delivered", "Returned", "arrow", "returnRequest", lpos=(361, 131))
    f.edge("Returned", "Closed", "arrow", "refunded / refund()", lpos=(300, 70))
    f.edge("Placed", "Cancelled", "arrow", "payFail" + chr(10) + "[attempts == 3]", lpos=(70, 172))
    f.edge("Paid", "Cancelled", "arrow", "cancel / refund()", lpos=(236, 168))
    f.edge("Placed", "Cancelled", "arrow", "cancel", via=[(28, 150), (28, 113)], lpos=(48, 125))
    f.edge("Cancelled", "e1", "arrow")
    f.edge("Closed", "e2", "arrow")
    return f


def d_usecase():
    f = Fig(545, 325, "Use case diagram of PayPoint")
    f.frame(88, 6, 372, 313, "PayPoint")
    f.actor("Customer", 14, 240, side="top")
    f.actor("User", 14, 130, side="right")
    f.actor("Agent", 14, 20, side="right")
    f.actor("Bank", 490, 112)
    f.actor("Admin", 490, 190)
    f.ellipse("Check Balance", 100, 277, 100, 26)
    f.ellipse("Send Money", 100, 232, 100, 26)
    f.ellipse("Pay Bill", 100, 182, 100, 26)
    f.ellipse("Link Bank Account", 100, 118, 100, 28, size=7)
    f.ellipse("Cash In", 100, 42, 100, 26)
    f.ellipse("Send OTP Check", 228, 272, 105, 26)
    f.ellipse("Apply Promo Code", 228, 222, 105, 26, size=7)
    f.ellipse("Verify PIN", 228, 165, 105, 26)
    f.ellipse("Block Account", 350, 231, 100, 26)
    f.ellipse("Generate Report", 350, 182, 100, 26)
    f.edge("Customer", "User", "inherit")
    f.edge("Agent", "User", "inherit")
    for u in ("Check Balance", "Send Money", "Pay Bill", "Link Bank Account"):
        f.edge("Customer", u, "assoc")
    f.edge("Agent", "Cash In", "assoc")
    f.edge("Bank", "Link Bank Account", "assoc")
    f.edge("Admin", "Block Account", "assoc")
    f.edge("Admin", "Generate Report", "assoc")
    f.edge("Send Money", "Verify PIN", "dashed")
    f.edge("Pay Bill", "Verify PIN", "dashed")
    f.edge("Cash In", "Verify PIN", "dashed")
    f.text(232, 150, "the three dashed arrows into Verify PIN are «include»", 6.8, "SegI")
    f.edge("Send OTP Check", "Send Money", "dashed", "«extend»", lpos=(214, 280))
    f.text(338, 282, "[amount > 25,000]", 7, "SegI")
    f.edge("Apply Promo Code", "Pay Bill", "dashed", "«extend»", lpos=(214, 228))
    return f


def d_sequence():
    parts = [("Customer", 45, True), (":App", 165, False), (":TransferService", 305, False), (":Ledger", 450, False)]
    msgs = [
        (285, "Customer", ":App", "sendMoney(receiver, amt)", "call"),
        (264, ":App", ":TransferService", "transfer(from, to, amt)", "call"),
        (243, ":TransferService", ":Ledger", "getBalance(from)", "call"),
        (226, ":Ledger", ":TransferService", "balance", "ret"),
        (190, ":TransferService", ":Ledger", "debit(from, amt)", "call"),
        (168, ":TransferService", ":Ledger", "credit(to, amt)", "call"),
        (147, ":TransferService", ":App", "success", "ret"),
        (127, ":App", "Customer", "show confirmation", "ret"),
        (88, ":TransferService", ":App", "insufficientFunds", "ret"),
        (68, ":App", "Customer", "show error", "ret"),
    ]
    acts = [(":App", 288, 50), (":TransferService", 266, 60), (":Ledger", 245, 222), (":Ledger", 192, 164)]
    f = sequence(540, 318, parts, msgs, frames=[(212, 48, "alt", 15, 525, 108)], acts=acts,
                 caption="Sequence diagram: Send Money (alt fragment for the balance check)")
    f.text(70, 200, "[balance " + FA + " amt]", 7, "SegB")
    f.text(70, 98, "[else]", 7, "SegB")
    return f


def d_collab():
    f = Fig(540, 150, "Collaboration diagram, success path (numbering shows the order)")
    f.actor("Customer", 14, 52)
    f.cls("a:App", 150, 60, 80, [], [])
    f.cls("t:TransferService", 290, 60, 110, [], [])
    f.cls("l:Ledger", 450, 60, 80, [], [])
    f.edge("Customer", "a:App", "assoc")
    f.edge("a:App", "t:TransferService", "assoc")
    f.edge("t:TransferService", "l:Ledger", "assoc")
    f.text(95, 98, "1: sendMoney(receiver, amt) →", 6.8)
    f.text(95, 38, "← 2: showConfirmation()", 6.8)
    f.text(238, 92, "1.1: transfer(from, to, amt) →", 6.8)
    f.text(403, 111, "1.1.1: getBalance(from) →", 6.8)
    f.text(403, 100, "1.1.2: debit(from, amt) →", 6.8)
    f.text(403, 89, "1.1.3: credit(to, amt) →", 6.8)
    return f


def d_cfg():
    f = Fig(540, 340, "Control-flow graph (node label = line number; T/F = predicate outcome)")
    nd = {"2": (240, 305), "3": (240, 262), "4a": (240, 218), "4b": (300, 172), "5": (190, 135), "7": (330, 120),
          "8": (240, 70), "10": (105, 262), "11": (55, 190), "12": (105, 120)}
    for k, (x, y) in nd.items():
        f.circle(k, x - 12, y - 12, 24, text=k, size=7.5)
    f.edge("2", "3", "arrow")
    f.edge("3", "4a", "arrow", "T", lpos=(250, 240))
    f.edge("3", "10", "arrow", "F", lpos=(175, 266))
    f.edge("4a", "5", "arrow", "T", lpos=(205, 182))
    f.edge("4a", "4b", "arrow", "F", lpos=(282, 205))
    f.edge("4b", "5", "arrow", "T", lpos=(250, 160))
    f.edge("4b", "7", "arrow", "F", lpos=(325, 150))
    f.edge("5", "8", "arrow")
    f.edge("7", "8", "arrow")
    f.edge("8", "3", "arrow", via=[(385, 70), (385, 262)])
    f.edge("10", "11", "arrow", "T", lpos=(65, 232))
    f.edge("10", "12", "arrow", "F", lpos=(118, 195))
    f.edge("11", "12", "arrow")
    notes = {"2": "s=0, i=1", "3": "while (i<=n)", "4a": "i%2==0", "4b": "i>k", "5": "s+=i", "7": "s-=1", "8": "i++", "10": "if (s<0)",
             "11": "s=0", "12": "return s"}
    pos = {"3": (16, 8), "8": (16, -16), "10": (-62, -3), "11": (-42, -3), "12": (16, -3)}
    for k, t in notes.items():
        x, y = nd[k]
        dx, dy = pos.get(k, (16, -3))
        f.text(x + dx, y + dy, t, 7, "SegI")
    f.text(395, 170, "loop back-edge 8→3", 7, "SegI")
    return f


def d_decorator():
    f = Fig(540, 250, "Decorator: add-ons wrap a plan and add to cost() and description()")
    f.cls("Plan", 195, 200, 150, [], ["*+cost(): int", "*+description(): String"], stereo="interface")
    f.cls("BasicPlan", 10, 110, 115, [], ["+cost(): int", "+description(): String"])
    f.cls("PlanDecorator", 190, 100, 160, ["#plan: Plan"], ["+cost(): int", "+description(): String"], abstract=True)
    f.cls("SocialPack", 10, 8, 120, [], ["+cost(): int  // +100"], size=7.2)
    f.cls("VideoPack", 195, 8, 120, [], ["+cost(): int  // +150"], size=7.2)
    f.cls("RoamingPack", 395, 8, 125, [], ["+cost(): int  // +200"], size=7.2)
    f.edge("BasicPlan", "Plan", "realize")
    f.edge("PlanDecorator", "Plan", "realize", via=[(270, 175)])
    f.edge("PlanDecorator", "Plan", "arrow", "wraps 1", via=[(400, 135), (400, 225)], lpos=(425, 180))
    for n in ("SocialPack", "VideoPack", "RoamingPack"):
        f.edge(n, "PlanDecorator", "inherit")
    return f


def d_observer():
    f = Fig(540, 235, "Observer: FloodStation is the subject, three subscribers are observers")
    f.cls("Subject", 10, 170, 150, [], ["*+attach(o: Observer)", "*+detach(o: Observer)", "*+notifyObservers()"], stereo="interface")
    f.cls("FloodStation", 10, 60, 150, ["-observers: List<Observer>", "-level: double"], ["+setLevel(l: double)", "+getLevel(): double"])
    f.cls("Observer", 300, 190, 150, [], ["*+update(station: FloodStation)"], stereo="interface")
    f.cls("SmsGateway", 215, 40, 95, [], ["+update(..)"])
    f.cls("CityDashboard", 320, 40, 100, [], ["+update(..)"])
    f.cls("SirenController", 430, 40, 105, [], ["+update(..)"])
    f.edge("FloodStation", "Subject", "realize")
    f.edge("Subject", "Observer", "arrow", "observers 0..*", lpos=(230, 232))
    for n in ("SmsGateway", "CityDashboard", "SirenController"):
        f.edge(n, "Observer", "realize")
    return f


def d_mediator():
    f = Fig(540, 215, "Mediator: users talk only to the ChatRoom")
    f.cls("ChatMediator", 15, 150, 190, [], ["*+register(u: User)", "*+send(msg: String, from: User)"], stereo="interface")
    f.cls("ChatRoom", 15, 40, 190, ["-users: List<User>", "-muted: Set<User>"], ["+register(u: User)", "+send(msg, from)", "+mute(u: User)"])
    f.cls("User", 330, 100, 170, ["-name: String", "-room: ChatMediator"], ["+post(msg: String)", "+receive(msg: String)"])
    f.edge("ChatRoom", "ChatMediator", "realize")
    f.edge("User", "ChatMediator", "arrow", "knows only the mediator", via=[(415, 185)], lpos=(330, 189))
    f.edge("ChatRoom", "User", "arrow", "users *", lpos=(268, 78))
    return f


def d_composite():
    f = Fig(540, 205, "Composite: a Folder is a FileSystemItem that holds FileSystemItems")
    f.cls("FileSystemItem", 170, 150, 190, [], ["*+getName(): String", "*+getSize(): int"], stereo="interface")
    f.cls("File", 20, 40, 150, ["-name: String", "-sizeKb: int"], ["+getSize(): int"])
    f.cls("Folder", 235, 40, 190, ["-name: String", "-children: List<FileSystemItem>"], ["+add(i: FileSystemItem)", "+remove(i: FileSystemItem)", "+getSize(): int"])
    f.edge("File", "FileSystemItem", "realize")
    f.edge("Folder", "FileSystemItem", "realize")
    f.edge("Folder", "FileSystemItem", "aggr", ma="", mb="*", via=[(460, 95), (460, 165)])
    return f


def d_bridge():
    f = Fig(540, 200, "Bridge: shapes and renderers vary independently")
    f.cls("Shape", 20, 135, 165, ["#renderer: Renderer"], ["*+draw()"], abstract=True)
    f.cls("Circle", 5, 30, 90, [], ["+draw()"])
    f.cls("Square", 110, 30, 90, [], ["+draw()"])
    f.cls("Renderer", 330, 135, 170, [], ["*+drawShape(kind: String)"], stereo="interface")
    f.cls("VectorRenderer", 285, 30, 110, [], ["+drawShape(..)"])
    f.cls("RasterRenderer", 410, 30, 110, [], ["+drawShape(..)"])
    f.edge("Circle", "Shape", "inherit")
    f.edge("Square", "Shape", "inherit")
    f.edge("VectorRenderer", "Renderer", "realize")
    f.edge("RasterRenderer", "Renderer", "realize")
    f.edge("Shape", "Renderer", "aggr", "the bridge", ma="", mb="1", lpos=(258, 172))
    return f


def d_incremental():
    f = Fig(540, 120, "Incremental delivery with an early risk spike")
    f.state("Spike", 5, 40, 80, 46, ["legacy-DB", "prototype"], size=8)
    f.state("Increment 1", 115, 40, 120, 46, ["core + results for", "one board (m1–4)"], size=8)
    f.state("Increment 2", 265, 40, 120, 46, ["3 more boards +", "reports (m5–6)"], size=8)
    f.state("Increment 3", 415, 40, 120, 46, ["all boards, load", "test, hardening (m7–8)"], size=8)
    f.edge("Spike", "Increment 1", "arrow")
    f.edge("Increment 1", "Increment 2", "arrow")
    f.edge("Increment 2", "Increment 3", "arrow")
    f.text(270, 108, "each increment: communication → planning → modelling → construction → deployment (user feedback feeds the next)",
           7.2, "SegI", align="center")
    f.text(125, 22, "pilot release, month 4", 7.2, "SegB")
    f.text(415, 22, "full release, month 8", 7.2, "SegB")
    return f
