// 2024-25 Q5(b)(i) — Mediator: sensors talk only to the hub; the hub owns the coordination rules
import java.util.ArrayList;
import java.util.List;

interface HubMediator { void notify(Device sender, String event); }

abstract class Device {                                  // colleague: knows only the mediator
    protected final HubMediator hub; final String name;
    Device(String name, HubMediator hub) { this.name = name; this.hub = hub; }
}
class MotionSensor extends Device {
    MotionSensor(HubMediator h) { super("MotionSensor", h); }
    void detect() { hub.notify(this, "motion"); }
}
class DoorSensor extends Device {
    DoorSensor(HubMediator h) { super("DoorSensor", h); }
    void forced() { hub.notify(this, "forced"); }
}
class Light extends Device {
    Light(HubMediator h) { super("Light", h); }
    void on() { System.out.println("Light ON"); }
}
class Alarm extends Device {
    Alarm(HubMediator h) { super("Alarm", h); }
    void activate() { System.out.println("Alarm ACTIVATED"); }
}
class SmartHomeHub implements HubMediator {             // concrete mediator
    Light light; Alarm alarm;
    final List<String> log = new ArrayList<>();
    public void notify(Device sender, String event) {
        log.add(sender.name + ":" + event);
        if (sender instanceof MotionSensor && event.equals("motion")) {
            light.on();
            System.out.println("Hub notified: motion in hallway");
        } else if (sender instanceof DoorSensor && event.equals("forced")) {
            alarm.activate();
            light.on();
        }
    }
}
public class SmartHomeDemo {
    public static void main(String[] args) {
        SmartHomeHub hub = new SmartHomeHub();
        hub.light = new Light(hub);
        hub.alarm = new Alarm(hub);
        new MotionSensor(hub).detect();
        new DoorSensor(hub).forced();
        System.out.println("events: " + hub.log);
    }
}
