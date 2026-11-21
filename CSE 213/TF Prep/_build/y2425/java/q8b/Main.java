import java.util.*;
import java.util.function.DoubleSupplier;

// ---------- value types replace Primitive Obsession and Data Clumps ----------
enum UserRole {
    OWNER(100, 1.00), GUEST(70, 1.30), OTHER(50, 1.00);
    private final int lightBrightness;
    private final double billingMultiplier;
    UserRole(int lightBrightness, double billingMultiplier) {
        this.lightBrightness = lightBrightness; this.billingMultiplier = billingMultiplier; }
    int lightBrightness()      { return lightBrightness; }
    double billingMultiplier() { return billingMultiplier; }
}

class User {
    private final String id, name;
    private final UserRole role;
    User(String id, String name, UserRole role) { this.id = id; this.name = name; this.role = role; }
    String getId() { return id; }   String getName() { return name; }   UserRole getRole() { return role; }
}

enum Action { ON }

// ---------- polymorphism replaces the "LIGHT" / "FAN" type switch ----------
abstract class Device {
    private static final int DEFAULT_HOURS_ON = 5;
    private final String id, name, room;
    private final double power;
    private boolean on;

    protected Device(String id, String name, String room, double power) {
        this.id = id; this.name = name; this.room = room; this.power = power; }

    final void turnOn(User user) {
        on = true; applyOnSettings(user); }          // template: the common part is written once
    protected abstract void applyOnSettings(User user);
    abstract void applyNightMode();

    double usageHours() {
        return on ? DEFAULT_HOURS_ON : 0; }                    // moved here: the device knows its own usage
    String getId() { return id; }   String getName() { return name; }   String getRoom() { return room; }
    double getPower() { return power; }   boolean isOn() { return on; }
}

class Light extends Device {
    private static final int NIGHT_BRIGHTNESS = 30;
    private int brightness;
    Light(String id, String name, String room, double power) { super(id, name, room, power); }
    protected void applyOnSettings(User user) { brightness = user.getRole().lightBrightness(); }
    void applyNightMode() { brightness = NIGHT_BRIGHTNESS; }
    int getBrightness() { return brightness; }
}

class Fan extends Device {
    private static final int NIGHT_SPEED = 1;
    private final DoubleSupplier temperature;                                    // injected (was a hard-coded 30)
    private int fanSpeed;
    Fan(String id, String name, String room, double power, DoubleSupplier temperature) {
        super(id, name, room, power); this.temperature = temperature; }
    protected void applyOnSettings(User user) { fanSpeed = speedFor(temperature.getAsDouble()); }
    private static int speedFor(double t) { if (t > 35) return 3; if (t > 28) return 2; return 1; }
    void applyNightMode() { fanSpeed = NIGHT_SPEED; }
    int getFanSpeed() { return fanSpeed; }
}

class BasicDevice extends Device {                                               // any other type: just switched on
    BasicDevice(String id, String name, String room, double power) { super(id, name, room, power); }
    protected void applyOnSettings(User user) { }
    void applyNightMode() { }
}

// ---------- the long parameter list of log() disappears: it receives objects ----------
class AuditLog {
    void record(Device d, User u, Action action) {
        System.out.println("LOG -> Device: " + d.getId() + ", Name: " + d.getName() + ", Room: " + d.getRoom()
                + ", User: " + u.getId() + ", User Name: " + u.getName()
                + ", User Type: " + u.getRole() + ", Action: " + action);
    }
}

// ---------- billing: a real class with BillItem instead of two parallel lists ----------
class BillItem {
    final String deviceName, room; final double cost;
    BillItem(String deviceName, String room, double cost) {
        this.deviceName = deviceName; this.room = room; this.cost = cost; }
}

class Bill {
    private final List<BillItem> items = new ArrayList<>();
    void add(BillItem item) { items.add(item); }
    double total() { double t = 0; for (BillItem i : items) t += i.cost; return t; }
    void print() {
        for (BillItem i : items) System.out.println(i.deviceName + " = " + i.cost);
        System.out.println("TOTAL = " + total());
    }
}

class BillingService {
    private static final double RATE_PER_UNIT = 12.5;
    Bill calculate(List<Device> devices, User user) {
        Bill bill = new Bill();
        for (Device d : devices) {
            double cost = d.getPower() * d.usageHours() * RATE_PER_UNIT * user.getRole().billingMultiplier();
            System.out.println("Device: " + d.getName() + " Room: " + d.getRoom() + " Cost: " + cost);
            bill.add(new BillItem(d.getName(), d.getRoom(), cost));
        }
        return bill;
    }
}

// ---------- the system now only coordinates ----------
public class Main {
    static class SmartHomeSystem {
        private final List<Device> devices = new ArrayList<>();
        private final User user;
        private final AuditLog log = new AuditLog();
        private final BillingService billing = new BillingService();

        SmartHomeSystem(User user) { this.user = user; }
        void add(Device d) { devices.add(d); }

        void turnOn(String deviceId) {
            findDevice(deviceId).ifPresent(d -> { d.turnOn(user); log.record(d, user, Action.ON); });
        }
        void activateNightMode() {
            System.out.println("Night mode activated");
            devices.forEach(Device::applyNightMode);
        }
        void calculateBill() { billing.calculate(devices, user).print(); }

        private Optional<Device> findDevice(String id) {
            return devices.stream().filter(d -> d.getId().equals(id)).findFirst();
        }
    }

    public static void main(String[] args) {
        SmartHomeSystem home = new SmartHomeSystem(new User("U1", "Rafi", UserRole.GUEST));
        home.add(new Light("L1", "Lamp", "Bedroom", 0.06));
        home.add(new Fan("F1", "Ceiling fan", "Hall", 0.07, () -> 30));
        home.turnOn("L1");
        home.turnOn("F1");
        home.activateNightMode();
        home.calculateBill();
    }
}
