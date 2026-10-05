import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

public class SmartHomeTestCases {

    public static void main(String[] args) {
        demoA();
        demoB();
        demoC();
        demoD();
        demoE();
        demoF();
    }

    static void header(String title) {
        System.out.println("\n" + "=".repeat(55));
        System.out.println("  " + title);
        System.out.println("=".repeat(55));
    }

    static void demoA() {
        header("DEMO A: Home Overview");

        Room living = new Room("Living Room");
        living.addDevice(new SmartLight());
        living.addDevice(new SmartSpeaker());

        Room bedroom = new Room("Bedroom");
        bedroom.addDevice(new SmartLight());
        bedroom.addDevice(new SmartThermostat());

        Home home = new Home("My Home");
        home.addRoom(living);
        home.addRoom(bedroom);

        System.out.println("Before activation:");
        System.out.println(home.getStatus());
        System.out.println("Power: " + home.getPowerUsage() + "W");

        home.activate();
        System.out.println("\nAfter activation:");
        System.out.println(home.getStatus());
        System.out.println("Power: " + home.getPowerUsage() + "W");
    }

    static void demoB() {
        header("DEMO B: AccessRestricted + TimerControlled");

        SmartLight light = new SmartLight();
        AccessRestricted secured = new AccessRestricted(light, 1234);
        TimerControlled timed = new TimerControlled(secured, 60);

        System.out.println("Step 1 - Activate while locked:");
        timed.activate();
        System.out.println("  Status: " + timed.getStatus());
        System.out.println("  Power:  " + timed.getPowerUsage() + "W");

        System.out.println("\nStep 2 - Wrong PIN:");
        secured.unlock(0);
        System.out.println("    >> Unlock attempt failed");
        System.out.println("  Status: " + timed.getStatus());

        System.out.println("\nStep 3 - Correct PIN, activate:");
        secured.unlock(1234);
        System.out.println("    >> Unlock SUCCESS");
        timed.activate();
        System.out.println("  Status: " + timed.getStatus());
        System.out.println("  Power:  " + timed.getPowerUsage() + "W");

        System.out.println("\nStep 4 - Timer expires:");
        timed.simulateTimerExpiry();
        System.out.println("    >> Timer expired - auto-deactivating.");
        System.out.println("  Status: " + timed.getStatus());
        System.out.println("  Power:  " + timed.getPowerUsage() + "W");
    }

    static void demoC() {
        header("DEMO C: EcoMode (budget = 100W)");

        Room office = new Room("Office");
        office.addDevice(new SmartLight());
        office.addDevice(new SmartLight());
        office.addDevice(new SmartThermostat());

        EcoMode ecoOffice = new EcoMode(office, 100);

        System.out.println("Activating with EcoMode:");
        ecoOffice.activate();
        System.out.println("\n" + ecoOffice.getStatus());
        System.out.println("Power: " + ecoOffice.getPowerUsage() + "W");
    }

    static void demoD() {
        header("DEMO D: Order Matters");

        Room room1 = new Room("Lab-1");
        room1.addDevice(new SmartLight());
        room1.addDevice(new SmartLight());
        room1.addDevice(new PowerThrottled(new SmartThermostat(), 80));
        EcoMode eco1 = new EcoMode(room1, 100);

        System.out.println("Setup 1: Throttled thermostat (80W) + EcoMode(100W)");
        eco1.activate();
        System.out.println(eco1.getStatus());
        System.out.println("Power: " + eco1.getPowerUsage() + "W");

        Room room2 = new Room("Lab-2");
        room2.addDevice(new SmartLight());
        room2.addDevice(new SmartLight());
        room2.addDevice(new SmartThermostat());
        EcoMode eco2 = new EcoMode(room2, 100);

        System.out.println("\nSetup 2: Raw thermostat (150W) + EcoMode(100W)");
        eco2.activate();
        System.out.println(eco2.getStatus());
        System.out.println("Power: " + eco2.getPowerUsage() + "W");
    }

    static void demoE() {
        header("DEMO E: GuestMode + Mixed Enhancements");

        Room guest = new Room("Guest Room");
        SmartSpeaker speaker = new SmartSpeaker();
        SmartThermostat lockedThermo = new SmartThermostat();
        SmartLight timedLight = new SmartLight();

        guest.addDevice(speaker);
        guest.addDevice(new AccessRestricted(lockedThermo, 9999));
        guest.addDevice(new TimerControlled(timedLight, 120));

        Set<Class<?>> allowed = new HashSet<>(Arrays.asList(SmartLight.class, SmartSpeaker.class));
        GuestMode guestMode = new GuestMode(guest, allowed);

        System.out.println("Activating GuestMode room:");
        guestMode.activate();
        System.out.println("\n" + guestMode.getStatus());
        System.out.println("Guest-visible power: " + guestMode.getPowerUsage() + "W");
    }

    static void demoF() {
        header("DEMO F: prepareForNight wraps a Room");

        Room kids = new Room("Kids Room");
        kids.addDevice(new SmartLight());
        kids.addDevice(new SmartSpeaker());
        kids.addDevice(new SmartThermostat());

        AccessRestricted lockedRoom = new AccessRestricted(kids, 0);
        TimerControlled nightMode = new TimerControlled(lockedRoom, 3600);

        System.out.println("Step 1 - Activate while locked (nothing happens):");
        nightMode.activate();
        System.out.println("  Status:\n" + nightMode.getStatus());
        System.out.println("  Power: " + nightMode.getPowerUsage() + "W");

        System.out.println("\nStep 2 - Unlock and activate:");
        lockedRoom.unlock(0);
        System.out.println("    >> Unlock SUCCESS");
        nightMode.activate();
        System.out.println("  Status:\n" + nightMode.getStatus());
        System.out.println("  Power: " + nightMode.getPowerUsage() + "W");

        System.out.println("\nStep 3 - Timer expires (entire room shuts off):");
        nightMode.simulateTimerExpiry();
        System.out.println("    >> Timer expired - auto-deactivating.");
        System.out.println("  Status:\n" + nightMode.getStatus());
        System.out.println("  Power: " + nightMode.getPowerUsage() + "W");

        System.out.println("\nStep 4 - Add to Home:");
        Home home = new Home("Night Home");
        home.addRoom(nightMode);
        System.out.println("  Home power: " + home.getPowerUsage() + "W");
    }
}
