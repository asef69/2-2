package batch_21;

interface OrderState {
    void confirm(Order order);

    void ship(Order order);

    void deliver(Order order);

    void cancel(Order order);

    String name();
}

class PlacedState implements OrderState {

    @Override
    public void cancel(Order order) {
        // TODO Auto-generated method stub
        order.setState(new CancelledState());
    }

    @Override
    public void confirm(Order order) {
        // TODO Auto-generated method stub
        order.setState(new ConfirmedState());
    }

    @Override
    public void deliver(Order order) {
        // TODO Auto-generated method stub
        System.out.println("can't deliver:not confirmed");
    }

    @Override
    public String name() {
        // TODO Auto-generated method stub
        return "Placed";
    }

    @Override
    public void ship(Order order) {
        // TODO Auto-generated method stub
        System.out.println("can't ship:not confirmed");
    }

}

class ConfirmedState implements OrderState {

    @Override
    public void cancel(Order order) {
        // TODO Auto-generated method stub
        order.setState(new CancelledState());
    }

    @Override
    public void confirm(Order order) {
        // TODO Auto-generated method stub
        System.out.println("already confimed");
    }

    @Override
    public void deliver(Order order) {
        // TODO Auto-generated method stub
        System.out.println("can't deliver:not shipped");
    }

    @Override
    public String name() {
        // TODO Auto-generated method stub
        return "Confirmed";
    }

    @Override
    public void ship(Order order) {
        // TODO Auto-generated method stub
        order.setState(new ShippedState());
    }

}

class ShippedState implements OrderState {

    @Override
    public void cancel(Order order) {
        // TODO Auto-generated method stub
        System.out.println("Can't cancel:alr shipped");
    }

    @Override
    public void confirm(Order order) {
        // TODO Auto-generated method stub
        System.out.println("in the shipping");
    }

    @Override
    public void deliver(Order order) {
        // TODO Auto-generated method stub
        order.setState(new DeliverState());
    }

    @Override
    public String name() {
        // TODO Auto-generated method stub
        return "Shipped";
    }

    @Override
    public void ship(Order order) {
        // TODO Auto-generated method stub
        System.out.println("shipped");
    }

}

class DeliverState implements OrderState {

    @Override
    public void cancel(Order order) {
        // TODO Auto-generated method stub
        System.out.println("can't cancel in delivery");
    }

    @Override
    public void confirm(Order order) {
        // TODO Auto-generated method stub
        System.out.println("alr confirmed");
    }

    @Override
    public void deliver(Order order) {
        // TODO Auto-generated method stub
        System.out.println("alr delivered");
    }

    @Override
    public String name() {
        // TODO Auto-generated method stub
        return "Delivered";
    }

    @Override
    public void ship(Order order) {
        // TODO Auto-generated method stub
        System.out.println("alr shipped");
    }

}

class CancelledState implements OrderState {

    @Override
    public void cancel(Order order) {
        // TODO Auto-generated method stub
        System.out.println("can't cancel in delivery");
    }

    @Override
    public void confirm(Order order) {
        // TODO Auto-generated method stub
        System.out.println("alr confirmed");
    }

    @Override
    public void deliver(Order order) {
        // TODO Auto-generated method stub
        System.out.println("alr delivered");
    }

    @Override
    public String name() {
        // TODO Auto-generated method stub
        return "Cancelled";
    }

    @Override
    public void ship(Order order) {
        // TODO Auto-generated method stub
        System.out.println("alr shipped");
    }

}

class Order {
    private String orderId;
    private OrderState state = new PlacedState();

    public Order(String orderId) {
        this.orderId = orderId;
    }

    public void setState(OrderState order) {
        state = order;
        System.out.println("Order " + orderId + " -> " + state.name());
    }

    public void confirm() {
        state.confirm(this);
    }

    public void ship() {
        state.ship(this);
    }

    public void deliver() {
        state.deliver(this);
    }

    public void cancel() {
        state.cancel(this);
    }

    public String getStateName() {
        return state.name();
    }
}

public class HungryHippo_State {
    public static void main(String[] args) {
        System.out.println("=== Order 1: full happy path ===");
        Order order1 = new Order("HH-1001");
        System.out.println("Initial state: " + order1.getStateName());
        order1.confirm();
        order1.ship();
        order1.deliver();
        order1.ship(); // invalid, no-op

        System.out.println("\n=== Order 2: cancelled before shipment ===");
        Order order2 = new Order("HH-1002");
        order2.confirm();
        order2.cancel();
        order2.ship(); // invalid, no-op

        System.out.println("\n=== Order 3: invalid skip attempt ===");
        Order order3 = new Order("HH-1003");
        order3.deliver(); // invalid: Placed -> Delivered directly
        order3.confirm();
        order3.ship();
        order3.confirm(); // invalid: cannot revert to Confirmed once shipped
    }
}
