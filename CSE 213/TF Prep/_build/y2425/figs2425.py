"""figs2425.py - every diagram of the 2024-25 CSE 213 term-final solutions."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mock"))
from reportlab.lib import colors  # noqa: E402

from figs import Fig, sequence, INK, GREY, BOLD, FONT  # noqa: E402

AMB = colors.Color(0.99, 0.93, 0.78)
GRN = colors.Color(0.88, 0.96, 0.89)
RED = colors.Color(0.99, 0.89, 0.88)
BLU = colors.Color(0.90, 0.94, 0.99)
LANE = colors.Color(0.97, 0.98, 0.99)


def _lanes(f, x0, x1, bounds, names):
    """bounds: list of y edges from the top lane downwards (n+1 values); names: lane titles."""
    def paint(c):
        for i, nm in enumerate(names):
            top, bot = bounds[i], bounds[i + 1]
            c.setFillColor(LANE if i % 2 == 0 else colors.white)
            c.rect(x0, bot, x1 - x0, top - bot, stroke=1, fill=1)
            c.setFillColor(colors.Color(0.89, 0.93, 0.98))
            c.rect(x0, bot, 16, top - bot, stroke=1, fill=1)
            c.setFillColor(INK)
            c.saveState()
            c.translate(x0 + 11, (top + bot) / 2)
            c.rotate(90)
            c.setFont(BOLD, 7)
            c.drawCentredString(0, 0, nm)
            c.restoreState()
    f.raw(paint)


# ----------------------------------------------------------------------------------------------- Q1(a)
def bpmn_main():
    f = Fig(545, 398, "BPMN: booking, payment, consultation and lab test (one pool, five lanes)")
    _lanes(f, 6, 540, [380, 310, 240, 170, 100, 30], ["Patient", "Hospital System", "Payment Gateway", "Doctor", "Laboratory"])
    P, S, G, D, L = 345, 275, 205, 135, 65
    f.bstart("S", 31, P - 7)
    f.task("T1", 53, P - 15, 62, 30, "Search doctor,\nselect slot")
    f.xor("R", 249, P - 13)
    f.text(262, P + 20, "Retry payment?", 6.6, "SegB", align="center")
    f.bend("Efail", 323, P - 7)
    f.text(323, P - 18, "not booked", 6.4, "SegI", align="center")
    f.task("T2", 53, S - 15, 62, 30, "Check slot\navailability")
    f.xor("X1", 129, S - 13)
    f.text(142, S + 20, "Slot available?", 6.6, "SegB", align="center")
    f.task("T3", 173, S - 18, 62, 36, "Create pending\nappointment,\nrequest payment")
    f.xor("X2", 249, S - 13)
    f.text(268, S - 22, "Payment", 6.6, "SegB")
    f.text(268, S - 30, "OK?", 6.6, "SegB")
    f.task("T4", 299, S - 18, 62, 36, "Confirm appt;\nnotify patient\nand doctor")
    f.task("T5", 173, G - 15, 62, 30, "Process\npayment")
    f.task("T6", 299, D - 18, 62, 36, "Consultation;\nissue\nprescription")
    f.xor("X3", 371, D - 13)
    f.text(384, D - 24, "Lab tests needed?", 6.6, "SegB", align="center")
    f.task("T7", 413, D - 15, 42, 30, "Request\nlab tests", size=6)
    f.task("T8", 467, D - 15, 42, 30, "Review\nreport", size=6)
    f.bend("Edone", 522, D - 6, 12)
    f.text(528, D - 18, "done", 6.4, "SegI", align="center")
    f.task("T9", 408, L - 15, 52, 30, "Perform tests,\nupload report", size=6)
    f.edge("S", "T1", "arrow")
    f.edge("T1", "T2", "arrow")
    f.edge("T2", "X1", "arrow")
    f.edge("X1", "T3", "arrow", "Yes", lpos=(163, S + 4))
    f.edge("X1", "T1", "arrow", "No: choose another slot", via=[(142, P)], lpos=(178, P + 18))
    f.edge("T3", "T5", "arrow", dashed=True)
    f.edge("T5", "X2", "arrow", via=[(262, G)], dashed=True)
    f.edge("X2", "T4", "arrow", "Yes", lpos=(287, S + 4))
    f.edge("X2", "R", "arrow", "No", lpos=(270, S + 34))
    f.edge("R", "T3", "arrow", "Yes: retry", via=[(204, P)], lpos=(226, P - 14))
    f.edge("R", "Efail", "arrow", "No", lpos=(297, P + 4))
    f.edge("T4", "T6", "arrow")
    f.edge("T6", "X3", "arrow")
    f.edge("X3", "T7", "arrow", "Yes", lpos=(401, D + 3))
    f.edge("X3", "Edone", "arrow", "No", via=[(384, 160), (528, 160)], lpos=(450, 163))
    f.edge("T7", "T9", "arrow", dashed=True)
    f.edge("T9", "T8", "arrow", via=[(488, L)], dashed=True)
    f.edge("T8", "Edone", "arrow")
    f.text(26, 33, "solid arrow = sequence flow, dashed arrow = message flow between lanes, diamond with × = exclusive (XOR) gateway", 6.4, "SegI")
    return f


def bpmn_cancel():
    f = Fig(545, 232, "BPMN: cancellation sub-process (can start any time after the appointment exists)")
    _lanes(f, 6, 540, [222, 150, 12], ["Patient", "Hospital System"])
    P = 186
    f.bstart("S", 31, P - 7)
    f.text(48, P - 22, "wants to cancel", 6.4, "SegI", align="center")
    f.task("T1", 69, P - 15, 70, 30, "Request\ncancellation")
    f.xor("X", 163, 70)
    f.text(162, 66, "Before the", 6.6, "SegB", align="right")
    f.text(162, 58, "deadline?", 6.6, "SegB", align="right")
    f.task("T2", 215, 94, 68, 30, "Cancel\nappointment")
    f.task("T3", 300, 94, 76, 30, "Initiate refund per\nhospital policy")
    f.task("T4", 393, 94, 72, 30, "Notify patient\nand doctor")
    f.bend("E1", 480, 101, 14)
    f.text(487, 90, "cancelled", 6.4, "SegI", align="center")
    f.task("T5", 215, 30, 76, 30, "Reject request,\ninform patient")
    f.bend("E2", 316, 38, 14)
    f.text(323, 27, "appointment kept", 6.4, "SegI", align="center")
    f.edge("S", "T1", "arrow")
    f.edge("T1", "X", "arrow", via=[(104, 83)], dashed=True)
    f.edge("X", "T2", "arrow", "Yes", via=[(176, 109)], lpos=(196, 113))
    f.edge("X", "T5", "arrow", "No", via=[(176, 45)], lpos=(196, 49))
    f.edge("T2", "T3", "arrow")
    f.edge("T3", "T4", "arrow")
    f.edge("T4", "E1", "arrow")
    f.edge("T5", "E2", "arrow")
    return f


# ----------------------------------------------------------------------------------------------- Q1(b)
def class_hospital():
    f = Fig(545, 450, "Class diagram of the online hospital appointment system")
    c1, c2, c3, c4 = 4, 148, 292, 433
    W1, W2, W3, W4 = 112, 112, 112, 108
    R1, R2, R3, R4 = 352, 240, 128, 16
    f.cls("Notification", c1, R1, W1, ["-message: String", "-sentAt: DateTime", "-channel: String"], ["+send()"], size=7)
    f.cls("TimeSlot", c2, R1, W2, ["-date: Date", "-startTime, endTime", "-status: SlotStatus"], ["+isAvailable(): boolean", "+reserve()"], size=7)
    f.cls("Doctor", c3, R1, W3, ["-id, name", "-specialization"], ["+issuePrescription()", "+requestLabTest()", "+reviewReport()"], size=7)
    f.cls("Laboratory", c4, R1, W4, ["-id, name"], ["+uploadReport()"], size=7)
    f.cls("Patient", c1, R2, W1, ["-id, name, phone"], ["+searchDoctor()", "+book(slot)", "+cancel(appt)", "+pay(appt)"], size=7)
    f.cls("Appointment", c2, R2, W2, ["-id", "-status: PENDING|", "   CONFIRMED|CANCELLED"], ["+confirm()", "+cancel()", "+isCancellable(): boolean"], size=7)
    f.cls("Prescription", c3, R2, W3, ["-issuedOn: Date", "-advice: String"], [], size=7)
    f.cls("LabTestRequest", c4, R2, W4, ["-testName: String", "-status: String"], [], size=7)
    f.cls("Payment", c1, R3, W1, ["-amount: double", "-status: PayStatus", "-txnRef: String"], ["+pay()", "+retry()"], size=7)
    f.cls("Refund", c2, R3, W2, ["-amount: double", "-date: Date"], ["+process()"], size=7)
    f.cls("PrescriptionItem", c3, R3, W3, ["-medicine: String", "-dosage: String", "-days: int"], [], size=7)
    f.cls("LabReport", c4, R3, W4, ["-fileUrl: String", "-uploadedOn: Date"], [], size=7)
    f.cls("PaymentGateway", c1, R4, W1, [], ["*+charge(amount)", "*+refund(txnRef)"], stereo="interface", size=7)
    f.edge("Notification", "Appointment", "assoc", "about", ma="*", mb="1", lpos=(88, 326))
    f.edge("Patient", "Appointment", "assoc", "books", ma="1", mb="*", lpos=(132, 290))
    f.edge("TimeSlot", "Appointment", "assoc", "reserved for", ma="1", mb="0..1", lpos=(240, 337))
    f.edge("Doctor", "TimeSlot", "assoc", "offers", ma="1", mb="*", lpos=(276, 393))
    f.edge("Doctor", "Prescription", "assoc", "issues", ma="1", mb="*", lpos=(370, 331))
    f.edge("Appointment", "Prescription", "assoc", "results in", ma="1", mb="0..1", lpos=(276, 286))
    f.edge("Appointment", "Payment", "comp", "paid by", ma="", mb="*", lpos=(100, 225))
    f.edge("Appointment", "Refund", "assoc", "may get", ma="1", mb="0..1", lpos=(230, 213))
    f.edge("Prescription", "PrescriptionItem", "comp", ma="", mb="1..*")
    f.edge("Prescription", "LabTestRequest", "assoc", "orders", ma="1", mb="*", lpos=(418, 286))
    f.edge("Laboratory", "LabTestRequest", "assoc", "performs", ma="1", mb="*", lpos=(514, 331))
    f.edge("LabTestRequest", "LabReport", "assoc", "produces", ma="1", mb="0..1", lpos=(514, 213))
    f.edge("Payment", "PaymentGateway", "depend", "uses", lpos=(84, 92))
    f.text(148, 44, "A Doctor also reviews a LabReport (operation reviewReport()).", 6.8, "SegI")
    f.text(148, 35, "Appointment, TimeSlot and Payment carry the booking state;", 6.8, "SegI")
    f.text(148, 26, "PaymentGateway is an external service behind an interface.", 6.8, "SegI")
    return f


# ----------------------------------------------------------------------------------------------- Q2
def seq_lending():
    parts = [("Student", 45, True), (":LendingSystem", 205, False), ("Staff", 360, True), ("Officer", 480, True)]
    step = 23
    msgs = []
    marks = {}
    y = [601]

    def add(a, b, label, kind):
        msgs.append((y[0], a, b, label, kind))
        y[0] -= step if kind != "self" else step + 3
        return len(msgs) - 1

    S, L, T, O = "Student", ":LendingSystem", "Staff", "Officer"
    add(S, L, "submitRequest(equipment, returnDate)", "call")
    add(L, L, "checkEligibility(student)", "self")
    add(L, L, "checkFines(student)", "self")
    add(L, L, "checkAvailability(equipment)", "self")
    a1 = y[0] + 18
    add(L, L, "reserveItem()", "self")
    add(L, S, "sendApprovalNotification()", "ret")
    d1 = y[0] + 12
    add(L, S, "rejectRequest(reason)", "ret")
    b1 = y[0] + 10
    y[0] -= 6
    add(S, T, "collectEquipment()", "call")
    add(T, T, "verifyIdentity(student)", "self")
    add(T, L, "recordHandover(request)", "call")
    add(L, L, "status = Borrowed", "self")
    y[0] -= 4
    add(S, T, "returnEquipment()", "call")
    add(T, T, "inspectCondition()", "self")
    a2 = y[0] + 18
    add(T, L, "closeLoan(request)", "call")
    add(L, L, "status = Closed", "self")
    d2 = y[0] + 12
    add(T, L, "reportDamage(request)", "call")
    add(L, L, "status = DamageReview", "self")
    add(L, O, "requestDecision(request)", "call")
    add(O, L, "decision(penalty?)", "ret")
    a3 = y[0] + 18
    add(L, S, "notifyPenalty(amount)", "call")
    b3 = y[0] + 9
    add(L, L, "status = Closed", "self")
    b2 = y[0] + 10
    y[0] -= 6
    a4 = y[0] + 18
    add(L, L, "calculateFine(daysLate)", "self")
    add(L, S, "notifyFine(amount)", "call")
    b4 = y[0] + 10
    H = 640
    frames = [(a1, b1, "alt", 20, 252, d1), (a2, b2, "alt", 20, 530, d2), (a3, b3, "opt", 28, 522, None), (a4, b4, "opt", 20, 252, None)]
    acts = []
    f = sequence(545, H, parts, msgs, frames=frames, acts=acts, caption="Sequence diagram: smart equipment lending (request, collection, return)")
    f.text(46, a1 - 9, "[eligible && available]", 6.8, "SegB")
    f.text(26, d1 - 9, "[else]", 6.8, "SegB")
    f.text(46, a2 - 9, "[good condition]", 6.8, "SegB")
    f.text(26, d2 - 9, "[damaged]", 6.8, "SegB")
    f.text(54, a3 - 9, "[officer imposes a penalty]", 6.8, "SegB")
    f.text(46, a4 - 9, "[returned after the return date]", 6.8, "SegB")
    return f


def state_loan():
    f = Fig(545, 300, "State diagram of a loan request")
    f.start("s0", 8, 252)
    f.state("Requested", 38, 235, 86, 36)
    f.state("Rejected", 38, 120, 86, 36)
    f.state("Approved", 180, 235, 86, 36)
    f.state("Borrowed", 322, 235, 86, 36)
    f.state("Overdue", 322, 120, 86, 36, fill=AMB)
    f.state("Damage Review", 140, 120, 96, 36, fill=RED)
    f.state("Closed", 455, 120, 82, 36)
    f.end("e1", 74, 70)
    f.end("e2", 504, 56)
    f.edge("s0", "Requested", "arrow", "submitRequest", lpos=(30, 280))
    f.edge("Requested", "Approved", "arrow")
    f.text(128, 286, "check [eligible && available]", 6.6)
    f.text(128, 278, "/ reserveItem(); notifyApproval()", 6.6)
    f.edge("Requested", "Rejected", "arrow")
    f.text(86, 202, "check [not eligible or", 6.6)
    f.text(86, 194, "item unavailable]", 6.6)
    f.text(86, 186, "/ notifyRejection()", 6.6)
    f.edge("Approved", "Borrowed", "arrow")
    f.text(272, 286, "collect [identity verified]", 6.6)
    f.text(272, 278, "/ recordHandover()", 6.6)
    f.edge("Borrowed", "Overdue", "arrow")
    f.text(368, 198, "after(returnDate)", 6.6)
    f.edge("Borrowed", "Closed", "arrow")
    f.text(432, 214, "return [good]", 6.6)
    f.text(432, 206, "/ closeLoan()", 6.6)
    f.edge("Borrowed", "Damage Review", "arrow")
    f.text(248, 214, "return [damaged]", 6.6, align="right")
    f.text(248, 206, "/ startReview()", 6.6, align="right")
    f.edge("Overdue", "Closed", "arrow")
    f.text(410, 152, "return [good]", 6.6)
    f.text(410, 144, "/ applyFine()", 6.6)
    f.edge("Overdue", "Damage Review", "arrow")
    f.text(244, 152, "return [damaged]", 6.6)
    f.text(244, 144, "/ applyFine()", 6.6)
    f.edge("Damage Review", "Closed", "arrow", via=[(188, 84), (455, 84)])
    f.text(200, 74, "decision / [penalty] applyPenalty(); [no penalty] nothing", 6.6)
    f.edge("Rejected", "e1", "arrow")
    f.edge("Closed", "e2", "arrow")
    return f


# ----------------------------------------------------------------------------------------------- Q3
def af_emergency():
    f = Fig(545, 300, "Abstract Factory for the emergency platform (one factory per region, one product per component)")
    f.cls("EmergencyPlatform", 195, 245, 150, ["-alerts: AlertGateway", "-tracker: LocationTracker", "-console: DispatchConsole", "-logger: IncidentLogger"],
          ["+handleIncident(i, unit)"], size=7)
    f.cls("EmergencyFactory", 14, 150, 160, [], ["*+createAlertGateway()", "*+createLocationTracker()", "*+createDispatchConsole()", "*+createIncidentLogger()"],
          stereo="interface", size=7)
    f.cls("NorthAmericaFactory", 4, 70, 110, [], [], size=7)
    f.cls("EuropeFactory", 124, 22, 100, [], [], size=7)
    f.cls("JapanFactory", 236, 70, 100, [], [], size=7)
    f.edge("EmergencyPlatform", "EmergencyFactory", "arrow", "uses", lpos=(170, 232))
    for n in ("NorthAmericaFactory", "EuropeFactory", "JapanFactory"):
        f.edge(n, "EmergencyFactory", "realize")
    f.cls("AlertGateway", 360, 238, 120, [], ["*+sendAlert(msg)"], stereo="interface", size=7)
    f.cls("LocationTracker", 360, 180, 120, [], ["*+locate(unit)"], stereo="interface", size=7)
    f.cls("DispatchConsole", 360, 122, 120, [], ["*+dispatch(team, inc)"], stereo="interface", size=7)
    f.cls("IncidentLogger", 360, 64, 120, [], ["*+record(incident)"], stereo="interface", size=7)
    f.edge("EmergencyPlatform", "AlertGateway", "depend")
    f.edge("EmergencyPlatform", "LocationTracker", "depend")
    f.edge("EmergencyPlatform", "DispatchConsole", "depend")
    f.edge("EmergencyPlatform", "IncidentLogger", "depend")
    f.text(358, 52, "12 concrete products (NaAlertGateway,", 6.6, "SegI")
    f.text(358, 44, "EuAlertGateway, JpAlertGateway, NaLocation-", 6.6, "SegI")
    f.text(358, 36, "Tracker … JpIncidentLogger) implement the", 6.6, "SegI")
    f.text(358, 28, "interfaces; each factory «creates» only the", 6.6, "SegI")
    f.text(358, 20, "four products of its own region.", 6.6, "SegI")
    return f


def solid_fine():
    f = Fig(545, 245, "Refactored fine management: one reason to change per class, everything depends on abstractions")
    f.cls("FineService", 190, 190, 165, ["-calculators: Map<String, FineCalculator>", "-notifier: Notifier", "-repository: FineRepository"],
          ["+processFine(userId, type, daysLate)"], size=7)
    f.cls("FineCalculator", 5, 105, 120, [], ["*+fine(daysLate): double"], stereo="interface", size=7)
    f.cls("Notifier", 215, 105, 110, [], ["*+notify(message)"], stereo="interface", size=7)
    f.cls("FineRepository", 405, 105, 130, [], ["*+save(userId, amount)"], stereo="interface", size=7)
    f.cls("StudentFine", 0, 8, 62, [], [], size=6.6)
    f.cls("FacultyFine", 68, 8, 62, [], [], size=6.6)
    f.cls("ResearcherFine", 136, 8, 76, [], [], size=6.6)
    f.cls("EmailNotifier", 218, 8, 66, [], [], size=6.6)
    f.cls("SmsNotifier", 290, 8, 58, [], [], size=6.6)
    f.cls("MySQLFineRepository", 358, 8, 90, [], [], size=6.6)
    f.cls("PostgreSQLFineRepository", 452, 8, 92, [], [], size=6.2)
    for n, t in (("StudentFine", "FineCalculator"), ("FacultyFine", "FineCalculator"), ("ResearcherFine", "FineCalculator"),
                 ("EmailNotifier", "Notifier"), ("SmsNotifier", "Notifier"), ("MySQLFineRepository", "FineRepository"),
                 ("PostgreSQLFineRepository", "FineRepository")):
        f.edge(n, t, "realize")
    for t in ("FineCalculator", "Notifier", "FineRepository"):
        f.edge("FineService", t, "arrow")
    f.text(4, 232, "ResearcherFine and PostgreSQLFineRepository", 6.8, "SegI")
    f.text(4, 223, "are the two new requirements: each is one", 6.8, "SegI")
    f.text(4, 214, "new class, FineService is not edited.", 6.8, "SegI")
    return f


# ----------------------------------------------------------------------------------------------- Q4
def builder_cluster():
    f = Fig(545, 275, "Builder: step-by-step construction of a valid ClusterConfig, with an optional Director")
    f.cls("Client", 4, 200, 90, [], [], size=7.5)
    f.cls("ClusterDirector", 4, 100, 130, [], ["+machineLearning(b)", "+dataArchive(b)"], size=7)
    f.cls("ClusterConfig.Builder", 170, 40, 175, ["-nodes, cpuPerNode, ramGbPerNode", "-highMemory, gpuLibs, gpuNodes", "-storage, storageService, network",
                                                  "-os, containerRuntime, security…"],
          ["+computeNodes(n, cpu): Builder", "+memory(ram, high): Builder", "+storage(type, service): Builder", "+network(n) / software(..) / security(..)",
           "+gpuCapableNodes() / gpuLibraries()", "+build(): ClusterConfig   // validates"], size=7)
    f.cls("ClusterConfig", 395, 140, 145, ["-nodes, cpuPerNode, ramGbPerNode", "-storage, network, os", "-gpuLibraries, authentication…", "(all final)"],
          ["-ClusterConfig(b)   // private", "+toString()"], size=7)
    f.edge("Client", "ClusterDirector", "arrow", "asks for a recipe", lpos=(95, 168))
    f.edge("ClusterDirector", "ClusterConfig.Builder", "arrow", "calls the steps", via=[(70, 78)], lpos=(110, 85))
    f.edge("ClusterConfig.Builder", "ClusterConfig", "depend", "«creates» (after validation)", via=[(370, 120)], lpos=(430, 125))
    f.edge("Client", "ClusterConfig.Builder", "arrow", "or builds directly", via=[(250, 227)], lpos=(255, 232))
    return f


# ----------------------------------------------------------------------------------------------- Q5
def observer_server():
    f = Fig(545, 250, "Observer: ControlCenter is the subject, the devices are observers; the sensor only knows the ControlCenter")
    f.cls("TemperatureSensor", 4, 170, 130, ["-center: ControlCenter"], ["+read(celsius)"], size=7)
    f.cls("TemperatureSubject", 190, 190, 150, [], ["*+register(o)", "*+unregister(o)", "*+notifyDevices()"], stereo="interface", size=7)
    f.cls("ControlCenter", 190, 80, 150, ["-devices: List<TemperatureObserver>", "-temperature: double"], ["+newReading(t)", "+register / unregister / notifyDevices"], size=7)
    f.cls("TemperatureObserver", 385, 190, 150, [], ["*+update(temperature)"], stereo="interface", size=7)
    f.cls("AcUnit", 360, 20, 46, [], [], size=7)
    f.cls("Alarm", 412, 20, 40, [], [], size=7)
    f.cls("Logger", 458, 20, 40, [], [], size=7)
    f.cls("SmsDevice", 504, 20, 40, [], [], size=6)
    f.edge("TemperatureSensor", "ControlCenter", "arrow", "newReading(t)", via=[(70, 125)], lpos=(110, 129))
    f.edge("ControlCenter", "TemperatureSubject", "realize")
    f.edge("TemperatureSubject", "TemperatureObserver", "arrow", "0..*", lpos=(362, 206))
    for n in ("AcUnit", "Alarm", "Logger", "SmsDevice"):
        f.edge(n, "TemperatureObserver", "realize")
    f.text(4, 80, "Subject = ControlCenter", 6.8, "SegB")
    f.text(4, 70, "Observers = AcUnit, Alarm,", 6.8, "SegB")
    f.text(4, 60, "Logger, SmsDevice (add or remove", 6.8, "SegB")
    f.text(4, 50, "at run time with register /", 6.8, "SegB")
    f.text(4, 40, "unregister)", 6.8, "SegB")
    return f


# ----------------------------------------------------------------------------------------------- Q7
def bridge_strategy():
    f = Fig(545, 432, "BrewBuddy: Bridge (set menu x drink) and Strategy (pricing scheme)")
    f.cls("SetMenu", 24, 322, 190, ["#name: String", "#basePrice: double", "#foodItems: List<String>", "#foodCalories: int", "#drink: Drink"],
          ["+getBasePrice(): double", "+getDescription(): String", "+getTotalCalories(): int"], abstract=True, size=7.2)
    f.cls("BurgerMeal", 18, 245, 62, [], [], size=7)
    f.cls("RiceMeal", 86, 245, 56, [], [], size=7)
    f.cls("PastaMeal", 148, 245, 64, [], [], size=7)
    f.cls("Drink", 330, 330, 190, [], ["*+getName(): String", "*+getIngredients(): List<String>", "*+getCalories(): int"], stereo="interface", size=7.2)
    f.cls("Coke", 305, 245, 50, [], [], size=7)
    f.cls("Lemonade", 361, 245, 60, [], [], size=7)
    f.cls("MangoJuice", 427, 245, 70, [], [], size=7)
    for n in ("BurgerMeal", "RiceMeal", "PastaMeal"):
        f.edge(n, "SetMenu", "inherit")
    for n in ("Coke", "Lemonade", "MangoJuice"):
        f.edge(n, "Drink", "realize")
    f.edge("SetMenu", "Drink", "aggr", "the bridge  (1 drink per menu)", mb="1", lpos=(272, 396))
    f.cls("Order", 24, 110, 150, ["-menu: SetMenu", "-customer: Customer", "-pricing: PricingStrategy"], ["+setPricing(p: PricingStrategy)", "+amountPayable(): double", "+receipt(): String"], size=7.2)
    f.cls("Customer", 24, 20, 130, ["-name: String", "-loyaltyPoints: int"], [], size=7.2)
    f.cls("PricingStrategy", 300, 130, 215, [], ["*+price(basePrice, customer): double"], stereo="interface", size=7.2)
    f.cls("RegularPricing", 262, 20, 82, [], [], size=7)
    f.cls("HappyHourPricing", 350, 20, 96, [], ["-percent: double"], size=7)
    f.cls("LoyaltyPricing", 452, 20, 80, [], [], size=7)
    for n in ("RegularPricing", "HappyHourPricing", "LoyaltyPricing"):
        f.edge(n, "PricingStrategy", "realize")
    f.edge("Order", "SetMenu", "assoc", ma="*", mb="1", via=[(8, 150), (8, 370)])
    f.edge("Order", "Customer", "assoc", ma="*", mb="1")
    f.edge("Order", "PricingStrategy", "arrow", "uses (set at checkout)", lpos=(238, 160))
    f.text(305, 222, "Receipt = getDescription() + \", \" + getTotalCalories() + \" kcal\"", 6.8, "SegI")
    f.text(305, 213, "= \"Burger Meal with Lemonade, 850 kcal\"", 6.8, "SegI")
    return f


# ----------------------------------------------------------------------------------------------- Q8
def refactor_design():
    f = Fig(545, 300, "Refactored SmartHome design (each class has one reason to change)")
    f.cls("SmartHomeSystem", 190, 232, 165, ["-devices: List<Device>", "-user: User"], ["+turnOn(deviceId)", "+activateNightMode()", "+calculateBill()"], size=7)
    f.cls("User", 5, 232, 110, ["-id, name", "-role: UserRole"], [], size=7)
    f.cls("UserRole", 5, 160, 110, ["OWNER(100, 1.0)", "GUEST(70, 1.3)", "OTHER(50, 1.0)"], [], stereo="enumeration", size=7)
    f.cls("Device", 190, 130, 165, ["-id, name, room, power", "-on: boolean"], ["+turnOn(user)  // final", "#applyOnSettings(user)", "+applyNightMode()", "+usageHours(): double"],
          abstract=True, size=7)
    f.cls("Light", 150, 30, 90, ["-brightness"], [], size=7)
    f.cls("Fan", 246, 30, 90, ["-fanSpeed"], [], size=7)
    f.cls("BasicDevice", 342, 30, 80, [], [], size=7)
    f.cls("AuditLog", 420, 232, 120, [], ["+record(device, user, action)"], size=7)
    f.cls("BillingService", 395, 150, 140, [], ["+calculate(devices, user): Bill"], size=7)
    f.cls("Bill", 395, 85, 140, [], ["+add(item)", "+total()", "+print()"], size=7)
    f.cls("BillItem", 440, 12, 100, ["-deviceName, room", "-cost"], [], size=7)
    for n in ("Light", "Fan", "BasicDevice"):
        f.edge(n, "Device", "inherit")
    f.edge("SmartHomeSystem", "Device", "aggr", ma="", mb="*", lpos=(270, 215))
    f.edge("SmartHomeSystem", "User", "arrow")
    f.edge("User", "UserRole", "arrow")
    f.edge("SmartHomeSystem", "AuditLog", "arrow", via=[(400, 280)])
    f.edge("SmartHomeSystem", "BillingService", "arrow", via=[(380, 200)])
    f.edge("BillingService", "Bill", "depend", "«creates»", lpos=(372, 140))
    f.edge("Bill", "BillItem", "comp", ma="", mb="*")
    return f


# ----------------------------------------------------------------------------------------------- Q1(c)
def load_stress():
    f = Fig(545, 150, "Load testing covers the specified range; stress testing goes beyond it")
    x0, x1, y0 = 40, 520, 40

    def X(u):
        return x0 + (x1 - x0) * u / 200.0

    def paint(c):
        c.setFillColor(GRN)
        c.rect(X(0), y0, X(100) - X(0), 60, stroke=1, fill=1)
        c.setFillColor(RED)
        c.rect(X(100), y0, X(200) - X(100), 60, stroke=1, fill=1)
        c.setFillColor(INK)
        c.setFont(BOLD, 8)
        c.drawCentredString((X(0) + X(100)) / 2, y0 + 40, "LOAD TESTING: 1 … 100 users")
        c.setFont(FONT, 7)
        c.drawCentredString((X(0) + X(100)) / 2, y0 + 28, "specified capacity; ramp up and hold")
        c.drawCentredString((X(0) + X(100)) / 2, y0 + 18, "(finds the failure at 90 users)")
        c.setFont(BOLD, 8)
        c.drawCentredString(X(175), y0 + 40, "STRESS: beyond 100")
        c.setFont(FONT, 7)
        c.drawCentredString(X(175), y0 + 28, "breaking point, graceful")
        c.drawCentredString(X(175), y0 + 18, "degradation, recovery")
        c.setStrokeColor(INK)
        c.line(x0, y0, x1, y0)
        for u in (0, 50, 90, 100, 150, 200):
            c.line(X(u), y0, X(u), y0 - 4)
            c.setFont(FONT, 7)
            c.drawCentredString(X(u), y0 - 13, str(u))
        c.setFont(FONT, 7)
        c.drawString(x1 - 62, y0 - 24, "concurrent users")
        for u, t in ((90, "failed at 90"), (150, "crashed at 150")):
            c.setStrokeColor(colors.Color(0.75, 0.1, 0.1))
            c.setLineWidth(1.4)
            c.line(X(u), y0, X(u), y0 + 78)
            c.setLineWidth(0.8)
            c.setFillColor(colors.Color(0.75, 0.1, 0.1))
            c.setFont(BOLD, 7.5)
            c.drawCentredString(X(u), y0 + 84, t)
            c.setFillColor(INK)
    f.raw(paint)
    return f
