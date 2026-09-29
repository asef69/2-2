public class Main {
    public static void main(String[] args) {
        CitizenRegistry registry = new CitizenRegistry();
        AlertPublisher publisher = new AlertPublisher();

        Citizen asef = registry.register("Asef");
        Citizen iztihad = registry.register("Iztihad");
        Citizen rayyan = registry.register("Rayyan");

        publisher.subscribe(asef, AlertCategory.EARTHQUAKE);
        publisher.subscribe(asef, AlertCategory.FIRE);

        publisher.subscribe(iztihad, AlertCategory.FLOOD);

        publisher.subscribe(rayyan, AlertCategory.EARTHQUAKE);
        publisher.subscribe(rayyan, AlertCategory.FLOOD);
        publisher.subscribe(rayyan, AlertCategory.FIRE);

        System.out.println("\n--- Initial subscriptions set. Publishing first round of alerts. ---");

        publisher.publishAlert(
                "Magnitude 6.1 Earthquake",
                AlertCategory.EARTHQUAKE,
                "Chittagong",
                "High",
                "Move to open ground, avoid damaged buildings.");

        publisher.publishAlert(
                "Flash Flood Warning",
                AlertCategory.FLOOD,
                "Sylhet",
                "Medium",
                "Move valuables to higher ground, avoid riverbanks.");

        publisher.publishAlert(
                "Residential Fire Outbreak",
                AlertCategory.FIRE,
                "Dhaka - Mirpur",
                "Critical",
                "Evacuate immediately, do not use elevators.");

        System.out.println("\n--- Updating subscriptions: Iztihad -> +EARTHQUAKE, Asef -> -FIRE ---");
        publisher.subscribe(iztihad, AlertCategory.EARTHQUAKE);
        publisher.unsubscribe(asef, AlertCategory.FIRE);

        publisher.publishAlert(
                "Aftershock Detected",
                AlertCategory.EARTHQUAKE,
                "Chittagong",
                "Medium",
                "Stay alert, aftershocks may continue for hours.");

        publisher.publishAlert(
                "Warehouse Fire",
                AlertCategory.FIRE,
                "Dhaka - Tejgaon",
                "High",
                "Avoid the area, thick smoke reported.");

        System.out.println("\n=== Final Notification Logs ===");
        asef.displayNotifications();
        iztihad.displayNotifications();
        rayyan.displayNotifications();
    }
}
