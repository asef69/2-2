public class Order {
    private final Gift gift;
    private final DeliveryRegion delivery; 
    private final double distance;
 
    public Order(Gift gift, DeliveryRegion delivery, double distance) {
        this.gift = gift;
        this.delivery = delivery;
        this.distance = distance;
    }
 
    public double getTotalCost() {
        double total = gift.getPrice();
        if (delivery != null) {
            total += delivery.getTotalDeliveryCharge(distance);
        }
        return total;
    }
 
    public void printSummary() {
        System.out.println("Item: " + gift.getDescription());
        System.out.printf("Total Cost: $%.2f%n", getTotalCost());
        if (delivery != null) {
            System.out.println("Delivery: " + delivery.getDescription());
            System.out.println("Estimated Delivery Time: " + delivery.getDeliveryTime());
        } else {
            System.out.println("No delivery requested (in-store pickup).");
        }
        System.out.println("------------------------------------------------");
    }
}