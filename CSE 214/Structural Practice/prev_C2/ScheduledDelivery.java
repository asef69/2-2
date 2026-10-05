package prev_C2;

public class ScheduledDelivery extends Delivery{
    private String timeslot;
    public ScheduledDelivery(TransportMethod transport,String timeslot) {
        super(transport);
        this.timeslot=timeslot;
    }
    @Override
    public double calculatePrice(double baseAmount) {
        return baseAmount+35.0;
    }

    @Override
    public void deliverOrder(String orderId) {
       System.out.println("at time slot");
       transport.dispatch(orderId);
    }
}
