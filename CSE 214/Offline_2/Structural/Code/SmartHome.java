import java.util.*;

interface SmartDevice {
    void activate();

    void deactivate();

    double getPowerUsage();

    String getStatus();

    boolean isActive();
}

interface GroupDevice extends SmartDevice {
    String getName();

    List<SmartDevice> getChildren();
}

class SmartLight implements SmartDevice {
    private boolean on = false;

    @Override
    public void activate() {
        on = true;
    }

    @Override
    public void deactivate() {
        on = false;
    }

    @Override
    public double getPowerUsage() {
        return on ? 10.0 : 0.0;
    }

    @Override
    public String getStatus() {
        return "Light: " + (on ? "ON" : "OFF");
    }

    @Override
    public boolean isActive() {
        return on;
    }
}

class SmartThermostat implements SmartDevice {
    private boolean on = false;

    @Override
    public void activate() {
        on = true;
    }

    @Override
    public void deactivate() {
        on = false;
    }

    @Override
    public double getPowerUsage() {
        return on ? 150.0 : 0.0;
    }

    @Override
    public String getStatus() {
        return "Thermostat: " + (on ? "ON" : "OFF");
    }

    @Override
    public boolean isActive() {
        return on;
    }
}

class SmartSpeaker implements SmartDevice {
    private boolean on = false;

    @Override
    public void activate() {
        on = true;
    }

    @Override
    public void deactivate() {
        on = false;
    }

    @Override
    public double getPowerUsage() {
        return on ? 5.0 : 0.0;
    }

    @Override
    public String getStatus() {
        return "Speaker: " + (on ? "Playing" : "Idle");
    }

    @Override
    public boolean isActive() {
        return on;
    }
}

class Room implements GroupDevice {
    private final String name;
    private final List<SmartDevice> devices = new ArrayList<>();

    public Room(String name) {
        this.name = name;
    }

    public void addDevice(SmartDevice d) {
        devices.add(d);
    }

    public List<SmartDevice> getDevices() {
        return devices;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public List<SmartDevice> getChildren() {
        return devices;
    }

    @Override
    public void activate() {
        for (SmartDevice d : devices) {
            d.activate();
        }
    }

    @Override
    public void deactivate() {
        for (SmartDevice d : devices) {
            d.deactivate();
        }
    }

    @Override
    public double getPowerUsage() {
        double total = 0;
        for (SmartDevice d : devices) {
            total += d.getPowerUsage();
        }
        return total;
    }

    @Override
    public boolean isActive() {
        for (SmartDevice d : devices) {
            if (d.isActive()) {
                return true;
            }
        }
        return false;
    }

    @Override
    public String getStatus() {
        StringBuilder sb = new StringBuilder("[" + name + "]");
        for (SmartDevice d : devices) {
            sb.append("\n  ").append(d.getStatus());
        }
        return sb.toString();
    }
}

class Home implements GroupDevice {
    private final String name;
    private final List<SmartDevice> rooms = new ArrayList<>();

    public Home(String name) {
        this.name = name;
    }

    public void addRoom(SmartDevice room) {
        rooms.add(room);
    }

    public List<SmartDevice> getRooms() {
        return rooms;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public List<SmartDevice> getChildren() {
        return rooms;
    }

    @Override
    public void activate() {
        for (SmartDevice r : rooms) {
            r.activate();
        }
    }

    @Override
    public void deactivate() {
        for (SmartDevice r : rooms) {
            r.deactivate();
        }
    }

    @Override
    public double getPowerUsage() {
        double total = 0;
        for (SmartDevice r : rooms) {
            total += r.getPowerUsage();
        }
        return total;
    }

    @Override
    public boolean isActive() {
        for (SmartDevice r : rooms) {
            if (r.isActive()) {
                return true;
            }
        }
        return false;
    }

    @Override
    public String getStatus() {
        StringBuilder sb = new StringBuilder("=== " + name + " ===");
        for (SmartDevice r : rooms) {
            sb.append("\n").append(r.getStatus());
        }
        return sb.toString();
    }
}

abstract class DeviceDecorator implements SmartDevice {
    protected final SmartDevice wrapped;

    public DeviceDecorator(SmartDevice wrapped) {
        this.wrapped = wrapped;
    }

    public SmartDevice getWrapped() {
        return wrapped;
    }

    @Override
    public void activate() {
        wrapped.activate();
    }

    @Override
    public void deactivate() {
        wrapped.deactivate();
    }

    @Override
    public double getPowerUsage() {
        return wrapped.getPowerUsage();
    }

    @Override
    public String getStatus() {
        return wrapped.getStatus();
    }

    @Override
    public boolean isActive() {
        return wrapped.isActive();
    }
}

class AccessRestricted extends DeviceDecorator {
    private final int pin;
    private boolean locked = true;

    public AccessRestricted(SmartDevice wrapped, int pin) {
        super(wrapped);
        this.pin = pin;
    }

    public void unlock(int pin) {
        if (this.pin == pin) {
            this.locked = false;
        }
    }

    @Override
    public void activate() {
        if (!locked) {
            super.activate();
        }
    }

    @Override
    public void deactivate() {
        if (!locked) {
            super.deactivate();
        }
    }

    @Override
    public String getStatus() {
        String baseStatus = super.getStatus();
        if (locked) {
            return baseStatus + " [LOCKED]";
        }
        return baseStatus;
    }
}

class TimerControlled extends DeviceDecorator {
    private final int seconds;
    private boolean timerRunning = false;

    public TimerControlled(SmartDevice wrapped, int seconds) {
        super(wrapped);
        this.seconds = seconds;
    }

    public void simulateTimerExpiry() {
        if (timerRunning) {
            deactivate();
        }
    }

    @Override
    public void activate() {
        super.activate();
        if (isActive()) {
            timerRunning = true;
        }
    }

    @Override
    public void deactivate() {
        super.deactivate();
        timerRunning = false;
    }

    @Override
    public String getStatus() {
        String baseStatus = super.getStatus();
        if (timerRunning) {
            return baseStatus + " (auto-off in " + seconds + "s)";
        }
        return baseStatus;
    }
}

class PowerThrottled extends DeviceDecorator {
    private final double cap;

    public PowerThrottled(SmartDevice wrapped, double cap) {
        super(wrapped);
        this.cap = cap;
    }

    @Override
    public double getPowerUsage() {
        double power = super.getPowerUsage();
        if (isActive() && power > cap) {
            return cap;
        }
        return power;
    }

    @Override
    public String getStatus() {
        String baseStatus = super.getStatus();
        if (isActive()) {
            double unthrottledPower = wrapped.getPowerUsage();
            if (unthrottledPower > cap) {
                return baseStatus + " [throttled to " + cap + "W]";
            }
        }
        return baseStatus;
    }
}

class EcoMode implements GroupDevice {
    private final GroupDevice group;
    private final double budget;

    public EcoMode(GroupDevice group, double budget) {
        this.group = group;
        this.budget = budget;
    }

    @Override
    public String getName() {
        return group.getName();
    }

    @Override
    public List<SmartDevice> getChildren() {
        return group.getChildren();
    }

    @Override
    public void activate() {
        group.activate();
        List<SmartDevice> children = group.getChildren();
        for (int i = children.size() - 1; i >= 0 && group.getPowerUsage() > budget; i--) {
            children.get(i).deactivate();
        }
    }

    @Override
    public void deactivate() {
        group.deactivate();
    }

    @Override
    public double getPowerUsage() {
        double power = group.getPowerUsage();
        return power > budget ? budget : power;
    }

    @Override
    public boolean isActive() {
        return group.isActive();
    }

    @Override
    public String getStatus() {
        return "[ECO: " + budget + "W budget]\n" + group.getStatus();
    }
}

class GuestMode implements GroupDevice {
    private final GroupDevice group;
    private final Set<Class<?>> allowed;

    public GuestMode(GroupDevice group, Set<Class<?>> allowed) {
        this.group = group;
        this.allowed = allowed;
    }

    @Override
    public String getName() {
        return group.getName();
    }

    @Override
    public List<SmartDevice> getChildren() {
        return group.getChildren();
    }

    @Override
    public void activate() {
        activateDevice(group);
    }

    private void activateDevice(SmartDevice d) {
        if (d instanceof GroupDevice) {
            for (SmartDevice child : ((GroupDevice) d).getChildren()) {
                activateDevice(child);
            }
        } else {
            if (isAllowed(d)) {
                d.activate();
            }
        }
    }

    @Override
    public void deactivate() {
        group.deactivate();
    }

    @Override
    public double getPowerUsage() {
        return getPowerUsageDevice(group);
    }

    private double getPowerUsageDevice(SmartDevice d) {
        if (d instanceof GroupDevice) {
            double total = 0;
            for (SmartDevice child : ((GroupDevice) d).getChildren()) {
                total += getPowerUsageDevice(child);
            }
            return total;
        } else {
            if (isAllowed(d)) {
                return d.getPowerUsage();
            } else {
                return 0.0;
            }
        }
    }

    @Override
    public boolean isActive() {
        return group.isActive();
    }

    private boolean isAllowed(SmartDevice d) {
        SmartDevice core = unwrap(d);
        for (Class<?> allowedClass : allowed) {
            if (allowedClass.isInstance(core)) {
                return true;
            }
        }
        return false;
    }

    private SmartDevice unwrap(SmartDevice d) {
        while (d instanceof DeviceDecorator) {
            d = ((DeviceDecorator) d).getWrapped();
        }
        return d;
    }

    private void collectLeafDevices(SmartDevice d, List<SmartDevice> result) {
        if (d instanceof GroupDevice) {
            for (SmartDevice child : ((GroupDevice) d).getChildren()) {
                collectLeafDevices(child, result);
            }
        } else {
            result.add(d);
        }
    }

    @Override
    public String getStatus() {
        String baseStatus = group.getStatus();
        String[] lines = baseStatus.split("\n");
        StringBuilder sb = new StringBuilder();
        sb.append("[GUEST MODE]\n");

        List<SmartDevice> leafDevices = new ArrayList<>();
        collectLeafDevices(group, leafDevices);

        int deviceIndex = 0;
        for (int i = 0; i < lines.length; i++) {
            String line = lines[i];
            if (line.startsWith("  ")) {
                sb.append(line);
                if (deviceIndex < leafDevices.size()) {
                    SmartDevice d = leafDevices.get(deviceIndex);
                    if (!isAllowed(d)) {
                        sb.append(" [guest-restricted]");
                    }
                    deviceIndex++;
                }
            } else {
                sb.append(line);
            }
            if (i < lines.length - 1) {
                sb.append("\n");
            }
        }
        return sb.toString();
    }
}
