package claude_questions;

interface ShippingStrategy {
    void compute(double distance, double weight);
}

class Standard implements ShippingStrategy {

    @Override
    public void compute(double distance, double weight) {
        // TODO Auto-generated method stub
        double cost = 50 + 5 * distance;
        System.out.println("Standard Shipping Cost:" + cost);
    }
}

class Express implements ShippingStrategy {
    @Override
    public void compute(double distance, double weight) {
        // TODO Auto-generated method stub
        double cost = 100 + 12 * distance;
        System.out.println("Express Shipping Cost:" + cost);
    }
}

class SameDay implements ShippingStrategy {
    @Override
    public void compute(double distance, double weight) {
        // TODO Auto-generated method stub
        double cost = 150;
        if (distance <= 30) {
            cost = 150 + 20 * distance;
        }
        System.out.println("Same Day Shipping Cost:" + cost);
    }
}

class Checkout {
    private ShippingStrategy strategy;

    void setStrategy(ShippingStrategy s) {
        strategy = s;
    }

    void checkout(double distance, double weight) {
        strategy.compute(distance, weight);
    }
}

class ST1_Main {
    public static void main(String[] args) {
        Checkout checkout = new Checkout();
        checkout.setStrategy(new Standard());
        checkout.checkout(20, 3);
        checkout.setStrategy(new Express());
        checkout.checkout(20, 3);
        checkout.setStrategy(new SameDay());
        checkout.checkout(45, 3); // rejected
        checkout.checkout(10, 3); // accepted
    }
}