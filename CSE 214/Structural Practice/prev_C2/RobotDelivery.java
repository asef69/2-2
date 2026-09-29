package prev_C2;

public class RobotDelivery implements TransportMethod{

    @Override
    public void dispatch(String orderId) {
        System.out.println(orderId+" dispatched through robot");    
    }

}
