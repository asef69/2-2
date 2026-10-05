package prev_C2;

public class DroneDelivery implements TransportMethod{

    @Override
    public void dispatch(String orderId) {
        System.out.println(orderId+" dispatched through drone");
        
    }
    
}
