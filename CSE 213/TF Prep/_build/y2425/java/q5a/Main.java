import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

interface TemperatureObserver { void update(double temperature); }

interface TemperatureSubject {
    void register(TemperatureObserver o);
    void unregister(TemperatureObserver o);
    void notifyDevices();
}

class ControlCenter implements TemperatureSubject {
    private final List<TemperatureObserver> devices = new ArrayList<>();
    private double temperature;

    public void register(TemperatureObserver o)   { if (!devices.contains(o)) devices.add(o); }
    public void unregister(TemperatureObserver o) { devices.remove(o); }
    public void notifyDevices() {
        for (TemperatureObserver o : new ArrayList<>(devices)) o.update(temperature);
    }
    void newReading(double t) { temperature = t; notifyDevices(); }
}

class TemperatureSensor {                       // knows only the ControlCenter, never a device
    private final ControlCenter center;
    TemperatureSensor(ControlCenter center) { this.center = center; }
    void read(double celsius) { center.newReading(celsius); }
}

class AcUnit implements TemperatureObserver {
    private boolean on = false;
    public void update(double t) {
        if (!on && t > 28)      { on = true;  System.out.println("AC: ON  (" + t + " C)"); }
        else if (on && t < 24)  { on = false; System.out.println("AC: OFF (" + t + " C)"); }
    }
}

class Alarm implements TemperatureObserver {
    public void update(double t) { if (t > 40) System.out.println("ALARM: " + t + " C is dangerous!"); }
}

class Logger implements TemperatureObserver {
    public void update(double t) {
        System.out.println("LOG " + LocalDateTime.now().withNano(0) + "  temperature = " + t); }
}

class SmsDevice implements TemperatureObserver {
    public void update(double t) { System.out.println("SMS: server room is at " + t + " C"); }
}

public class Main {
    public static void main(String[] a) {
        ControlCenter center = new ControlCenter();
        TemperatureSensor sensor = new TemperatureSensor(center);
        AcUnit ac = new AcUnit(); Alarm alarm = new Alarm(); Logger logger = new Logger(); SmsDevice sms = new SmsDevice();
        center.register(ac); center.register(alarm); center.register(logger); center.register(sms);
        sensor.read(26);
        sensor.read(29);
        sensor.read(41);
        center.unregister(sms);                  // SMS device disabled at night
        sensor.read(23);
    }
}
