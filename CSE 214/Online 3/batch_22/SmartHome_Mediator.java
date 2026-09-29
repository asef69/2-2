package batch_22;


interface HubMediator {
    void notify(Object sender, String event);
}

class CentralHub implements HubMediator {
    private LightSensor lightSensor;
    private Blinds blinds;
    private AirConditioner ac;

    public void registerLightSensor(LightSensor s) {
        this.lightSensor = s;
    }

    public void registerBlinds(Blinds b) {
        this.blinds = b;
    }

    public void registerAC(AirConditioner a) {
        this.ac = a;
    }

    public void notify(Object sender, String event) {
        if (sender == lightSensor && event.equals("HIGH_BRIGHTNESS")) {
            System.out.println("Hub: High brightness detected -> instructing Blinds to close.");
            blinds.close();
        } else if (sender == blinds && event.equals("CLOSED")) {
            System.out.println("Hub: Blinds closed -> turning on Air Conditioner (room will get stuffy).");
            ac.turnOn();
        }
    }
}

class LightSensor {
    private HubMediator hub;

    public LightSensor(HubMediator hub) {
        this.hub = hub;
    }

    public void detectHighBrightness() {
        System.out.println("LightSensor: High Brightness detected.");
        hub.notify(this, "HIGH_BRIGHTNESS");
    }
}

class Blinds {
    private HubMediator hub;

    public Blinds(HubMediator hub) {
        this.hub = hub;
    }

    public void close() {
        System.out.println("Blinds: Closing...");
        hub.notify(this, "CLOSED");
    }
}

class AirConditioner {
    public void turnOn() {
        System.out.println("AirConditioner: Turned ON.");
    }
}

public class SmartHome_Mediator {
    public static void main(String[] args) {
        CentralHub hub = new CentralHub();
        LightSensor sensor = new LightSensor(hub);
        Blinds blinds = new Blinds(hub);
        AirConditioner ac = new AirConditioner();

        hub.registerLightSensor(sensor);
        hub.registerBlinds(blinds);
        hub.registerAC(ac);

        sensor.detectHighBrightness();
    }
}