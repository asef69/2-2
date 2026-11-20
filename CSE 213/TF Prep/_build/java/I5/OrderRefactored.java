// 2023-24 Q8(c) — DiscountCalculator / OrderProcessor after refactoring
// Smells: long parameter list + data clump (customerName, customerId, customerType) -> Introduce Parameter Object Customer;
// unused parameters (name, id in calculateDiscount); switch-like if-chain on type codes -> polymorphic CustomerType enum;
// duplicated code (printing customer data twice, string comparisons repeated); magic numbers -> constants in the enum;
// long method processOrder -> Extract Method; bug: discount == price*0.15 / 0.25 never match the rates (0.05, 0.1, 0.2)
// and float comparison with == -> print the rate instead; feature envy on strings -> methods on Product/Customer.
enum ProductType { ELECTRONICS, GROCERY, OTHER }
enum CustomerType {
    REGULAR(0.10, 0.05), PREMIUM(0.20, 0.10);
    private final double electronicsRate, groceryRate;
    CustomerType(double e, double g) { electronicsRate = e; groceryRate = g; }
    double rateFor(ProductType p) {
        switch (p) {
            case ELECTRONICS: return electronicsRate;
            case GROCERY:     return groceryRate;
            default:          return 0;
        }
    }
}
class Customer {
    final String name, id; final CustomerType type;
    Customer(String name, String id, CustomerType type) { this.name = name; this.id = id; this.type = type; }
}
class Product {
    final ProductType type; final double price;
    Product(ProductType type, double price) { this.type = type; this.price = price; }
}
class DiscountCalculator {
    double discountRate(Customer c, Product p) { return c.type.rateFor(p.type); }
    double calculateDiscount(Customer c, Product p) { return p.price * discountRate(c, p); }
}
class OrderProcessor {
    private final DiscountCalculator calculator = new DiscountCalculator();
    void processOrder(Customer c, Product p) {
        double rate = calculator.discountRate(c, p);
        double discount = p.price * rate;
        printCustomer(c);
        printProduct(p);
        printPrices(p.price, discount, rate);
    }
    private void printCustomer(Customer c) {
        System.out.println("Processing order for " + c.name + " (" + c.id + "), " + c.type + " customer");
    }
    private void printProduct(Product p) { System.out.println(p.type + " item processed"); }
    private void printPrices(double price, double discount, double rate) {
        System.out.println("Original price: " + price);
        System.out.println(rate == 0 ? "No discount applied" : Math.round(rate * 100) + "% discount applied: " + discount);
        System.out.println("Final price: " + (price - discount));
    }
}
public class OrderRefactored {
    public static void main(String[] args) {
        OrderProcessor op = new OrderProcessor();
        op.processOrder(new Customer("Rina", "C-17", CustomerType.PREMIUM), new Product(ProductType.ELECTRONICS, 1000));
        op.processOrder(new Customer("Karim", "C-18", CustomerType.REGULAR), new Product(ProductType.GROCERY, 200));
        op.processOrder(new Customer("Karim", "C-18", CustomerType.REGULAR), new Product(ProductType.OTHER, 50));
    }
}
