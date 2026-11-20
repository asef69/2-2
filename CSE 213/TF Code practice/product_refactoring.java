import java.util.*;

enum productType {
    ELECTRONICS("Electronics item processed"),
    GROCERY("Grocery item processed"),
    OTHER("Other item processed");

    private final String processedNote;

    private productType(String processedNote) {
        this.processedNote = processedNote;
    }

    String processedNote() {
        return processedNote;
    }

    static productType from(String code) {
        for (productType t : values()) {
            if (t != OTHER && t.name().equals(code)) {
                return t;
            }
        }
        return OTHER;
    }
}

enum customerType {
    REGULAR("regular customer", Map.of(productType.ELECTRONICS, 0.1, productType.GROCERY, 0.05)),
    PREMIUM("premium customer", Map.of(productType.ELECTRONICS, 0.2, productType.GROCERY, 0.1)),
    OTHER(null, Map.of());

    private final String processedNote;
    private final Map<productType, Double> discountRates;

    private customerType(String processedNote, Map<productType, Double> discountRates) {
        this.processedNote = processedNote;
        this.discountRates = discountRates;
    }

    String processedNote() {
        return processedNote;
    }

    double discountRateFor(productType p) {
        return discountRates.getOrDefault(p, 0.0);
    }

    static customerType from(String code) {
        for (customerType t : values()) {
            if (t != OTHER && t.name().equals(code)) {
                return t;
            }
        }
        return OTHER;
    }
}

class Customer {
    private final String name, id, typeCode;

    public Customer(String name, String id, String typeCode) {
        this.name = name;
        this.id = id;
        this.typeCode = typeCode;
    }

    public String getName() {
        return name;
    }

    public String getId() {
        return id;
    }

    public String getTypeCode() {
        return typeCode;
    }

    customerType getType() {
        return customerType.from(typeCode);
    }
}

class Product {
    private final String typeCode;
    private final double price;

    public Product(String typeCode, double price) {
        this.typeCode = typeCode;
        this.price = price;
    }

    public String getTypeCode() {
        return typeCode;
    }

    public double getPrice() {
        return price;
    }

    productType getType() {
        return productType.from(typeCode);
    }
}

class DiscountCalculator {
    double discountRate(Customer c, Product p) {
        return c.getType().discountRateFor(p.getType());
    }

    double calculateDiscount(Customer c, Product p) {
        return p.getPrice() * discountRate(c, p);
    }
}

class OrderProcessor {
    private static final Map<Double, String> DISCOUNT_NOTES = Map.of(
            0.05, "5% discount",
            0.1, "10% discount",
            0.2, "20% discount");

    private final DiscountCalculator discountCalculator = new DiscountCalculator();

    public void processOrder(Customer customer, Product product) {
        printHeader(customer);
        double rate = discountCalculator.discountRate(customer, product);
        double discount = discountCalculator.calculateDiscount(customer, product);
        printProcessingNotes(customer, product);
        printSummary(customer, product, discount);
        printDiscountNote(discount, rate);
    }

    private void printHeader(Customer customer) {
        System.out.println("Processing Order for Customer: " + customer.getName());
        System.out.println("Customer ID: " + customer.getId());
    }

    private void printProcessingNotes(Customer customer, Product product) {
        if (customer.getType().processedNote() != null) {
            System.out.println(customer.getType().processedNote());
        }
        // Keep the original behavior: show the "Other item" note only for premium customers.
        if (product.getType() != productType.OTHER || customer.getType() == customerType.PREMIUM) {
            System.out.println(product.getType().processedNote());
        }
    }

    private void printSummary(Customer customer, Product product, double discount) {
        System.out.println("Customer Name: " + customer.getName());
        System.out.println("Customer Type: " + customer.getTypeCode());
        System.out.println("Customer ID: " + customer.getId());
        System.out.println("Product Type: " + product.getTypeCode());
        System.out.println("Original Price: " + product.getPrice());
        System.out.println("Discount: " + discount);
        System.out.println("Final Price: " + (product.getPrice() - discount));
    }

    private void printDiscountNote(double discount, double rate) {
        if (discount == 0) {
            System.out.println("No discount applied");
            return;
        }
        String note = DISCOUNT_NOTES.get(rate);
        if (note != null) {
            System.out.println(note);
        }
    }
}
