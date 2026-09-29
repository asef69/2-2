package prev_C2;

public class ExpressDelivery extends Delivery{

    public ExpressDelivery(TransportMethod transport) {
        super(transport);
    }
    @Override
    public double calculatePrice(double baseAmount) {
        return baseAmount+60.0;
    }

    @Override
    public void deliverOrder(String orderId) {
       System.out.println("within 4 hrs");
       transport.dispatch(orderId);
    }
}
