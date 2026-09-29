import java.util.ArrayList;
import java.util.List;

public class Citizen implements Observer {
    private final String name;
    private final List<Alert> receivedAlert = new ArrayList<>();

    public Citizen(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    @Override
    public void update(Alert alert) {
        receivedAlert.add(alert);
        System.out.println("Notification to:" + name + " for:" + alert);
    }

    public void displayNotifications() {
        System.out.println("Notifications for " + name + ":");
        if (receivedAlert.isEmpty()) {
            System.out.println("  (no notifications received yet)");
            return;
        }
        int i = 1;
        for (Alert alert : receivedAlert) {
            System.out.println("  " + (i++) + ". " + alert);
        }
    }
}
