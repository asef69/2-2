package prev_B2;

public class prev_b2_main {
    public static void main(String[] args) {
        java.util.List<SmartDevice> devices = new java.util.ArrayList<>();
        devices.add(new SmartLight());
        devices.add(new SmartFan());
        devices.add(new SmartAC());
        devices.add(new OldSmartBulbAdapter(new OldSmartBulb()));   // 3rd-party device 1
        devices.add(new LegacyHeaterAdapter(new LegacyHeater()));   // 3rd-party device 2
 
        // App controls every device uniformly through SmartDevice interface
        for (SmartDevice device : devices) {
            device.turnOn();
            device.turnOff();
            System.out.println("-----");
        }
    }
}
