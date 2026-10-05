package prev_C2;

public class prev_c2_main {
    public static void main(String[] args) {
        // Existing combinations
        Delivery order1 = new StandardDelivery(new BikeCourier());
        order1.deliverOrder("ORD-1001");
        System.out.println("Price: " + order1.calculatePrice(500) + "\n-----");
 
        Delivery order2 = new ExpressDelivery(new VanDelivery());
        order2.deliverOrder("ORD-1002");
        System.out.println("Price: " + order2.calculatePrice(500) + "\n-----");
 
        // New transport tech (Drone) plugged into an existing delivery type
        // with zero changes to ExpressDelivery or DroneDelivery classes.
        Delivery order3 = new ExpressDelivery(new DroneDelivery());
        order3.deliverOrder("ORD-1003");
        System.out.println("Price: " + order3.calculatePrice(500) + "\n-----");
 
        // Another new transport tech (Robot) combined with Scheduled delivery
        Delivery order4 = new ScheduledDelivery(new RobotDelivery(), "6:00 PM - 7:00 PM");
        order4.deliverOrder("ORD-1004");
        System.out.println("Price: " + order4.calculatePrice(500));
    }
}
