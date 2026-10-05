import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;

public class AlertPublisher implements Subject {
    private final Map<AlertCategory, List<Observer>> subscribers = new EnumMap<>(AlertCategory.class);

    public AlertPublisher() {
        for (AlertCategory category : AlertCategory.values()) {
            subscribers.put(category, new ArrayList<>());
        }
    }

    @Override
    public void notifySubscribers(Alert alert) {
        List<Observer> observers = subscribers.get(alert.getCategory());
        for (Observer observer : observers) {
            observer.update(alert);
        }
    }

    @Override
    public void subscribe(Observer observer, AlertCategory alertCategory) {
        List<Observer> observers = subscribers.get(alertCategory);
        if (!observers.contains(observer)) {
            observers.add(observer);
        }
    }

    @Override
    public void unsubscribe(Observer observer, AlertCategory alertCategory) {
        subscribers.get(alertCategory).remove(observer);
    }

    public void publishAlert(String title, AlertCategory category, String location,
            String severity, String instructions) {
        Alert alert = new Alert(title, category, location, severity, instructions);
        System.out.println("\n=== Publishing Alert: " + alert + " ===");
        notifySubscribers(alert);
    }

}
