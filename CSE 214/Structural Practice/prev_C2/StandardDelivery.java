package prev_C2;

public class StandardDelivery extends Delivery{

    public StandardDelivery(TransportMethod transport) {
        super(transport);
    }

    @Override
    public double calculatePrice(double baseAmount) {
        return baseAmount+30.0;
    }

    @Override
    public void deliverOrder(String orderId) {
       System.out.println("within 24 hrs");
       transport.dispatch(orderId);
    }
    
}
