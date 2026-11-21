// ---- product interfaces (one per component of the family)
interface AlertGateway    { void sendAlert(String message); }
interface LocationTracker { String locate(String unitId); }
interface DispatchConsole { void dispatch(String team, String incident); }
interface IncidentLogger  { void record(String incident); }

// ---- abstract factory
interface EmergencyFactory {
    AlertGateway    createAlertGateway();
    LocationTracker createLocationTracker();
    DispatchConsole createDispatchConsole();
    IncidentLogger  createIncidentLogger();
}

// ---- North America family
class NaAlertGateway implements AlertGateway {
    public void sendAlert(String m) { System.out.println("[NA] Wireless Emergency Alert: " + m); }
}
class NaLocationTracker implements LocationTracker {
    public String locate(String u) { return "[NA] E911 Phase II location of " + u; }
}
class NaDispatchConsole implements DispatchConsole {
    public void dispatch(String t, String i) { System.out.println("[NA] CAD dispatch " + t + " -> " + i); }
}
class NaIncidentLogger implements IncidentLogger {
    public void record(String i) { System.out.println("[NA] NIEM-format record: " + i); }
}
class NorthAmericaFactory implements EmergencyFactory {
    public AlertGateway createAlertGateway()       { return new NaAlertGateway(); }
    public LocationTracker createLocationTracker() { return new NaLocationTracker(); }
    public DispatchConsole createDispatchConsole() { return new NaDispatchConsole(); }
    public IncidentLogger createIncidentLogger()   { return new NaIncidentLogger(); }
}

// ---- Europe family
class EuAlertGateway implements AlertGateway {
    public void sendAlert(String m) { System.out.println("[EU] EU-Alert cell broadcast: " + m); }
}
class EuLocationTracker implements LocationTracker {
    public String locate(String u) { return "[EU] AML / E112 location of " + u; }
}
class EuDispatchConsole implements DispatchConsole {
    public void dispatch(String t, String i) { System.out.println("[EU] 112 dispatch " + t + " -> " + i); }
}
class EuIncidentLogger implements IncidentLogger {
    public void record(String i) { System.out.println("[EU] GDPR-compliant record: " + i); }
}
class EuropeFactory implements EmergencyFactory {
    public AlertGateway createAlertGateway()       { return new EuAlertGateway(); }
    public LocationTracker createLocationTracker() { return new EuLocationTracker(); }
    public DispatchConsole createDispatchConsole() { return new EuDispatchConsole(); }
    public IncidentLogger createIncidentLogger()   { return new EuIncidentLogger(); }
}

// ---- Japan family
class JpAlertGateway implements AlertGateway {
    public void sendAlert(String m) { System.out.println("[JP] J-Alert broadcast: " + m); }
}
class JpLocationTracker implements LocationTracker {
    public String locate(String u) { return "[JP] 119 location of " + u; }
}
class JpDispatchConsole implements DispatchConsole {
    public void dispatch(String t, String i) { System.out.println("[JP] 119 dispatch " + t + " -> " + i); }
}
class JpIncidentLogger implements IncidentLogger {
    public void record(String i) { System.out.println("[JP] FDMA-format record: " + i); }
}
class JapanFactory implements EmergencyFactory {
    public AlertGateway createAlertGateway()       { return new JpAlertGateway(); }
    public LocationTracker createLocationTracker() { return new JpLocationTracker(); }
    public DispatchConsole createDispatchConsole() { return new JpDispatchConsole(); }
    public IncidentLogger createIncidentLogger()   { return new JpIncidentLogger(); }
}

// ---- client: knows only the abstract types
class EmergencyPlatform {
    private final AlertGateway alerts;
    private final LocationTracker tracker;
    private final DispatchConsole console;
    private final IncidentLogger logger;

    EmergencyPlatform(EmergencyFactory factory) {
        this.alerts  = factory.createAlertGateway();
        this.tracker = factory.createLocationTracker();
        this.console = factory.createDispatchConsole();
        this.logger  = factory.createIncidentLogger();
    }
    void handleIncident(String incident, String unit) {
        System.out.println(tracker.locate(unit));
        alerts.sendAlert(incident);
        console.dispatch("rescue team 7", incident);
        logger.record(incident);
    }
}

public class Main {
    public static void main(String[] args) {
        java.util.Map<String, java.util.function.Supplier<EmergencyFactory>> regions = new java.util.HashMap<>();
        regions.put("NA", NorthAmericaFactory::new);
        regions.put("EU", EuropeFactory::new);
        regions.put("JP", JapanFactory::new);          // a new region = one new factory + one new line here
        String region = args.length > 0 ? args[0] : "EU";
        new EmergencyPlatform(regions.get(region).get()).handleIncident("Flood warning", "unit-12");
    }
}
