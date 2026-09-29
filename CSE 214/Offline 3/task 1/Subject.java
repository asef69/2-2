public interface Subject {
    void subscribe(Observer observer, AlertCategory alertCategory);

    void unsubscribe(Observer observer, AlertCategory alertCategory);

    void notifySubscribers(Alert alert);
}
