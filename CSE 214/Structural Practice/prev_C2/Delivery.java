package prev_C2;

public abstract class Delivery {
    protected TransportMethod transport;

    public Delivery(TransportMethod transport) {
        this.transport = transport;
    }
    public abstract void deliverOrder(String orderId);
    public abstract double calculatePrice(double baseAmount);
}
