import java.util.*;

// ---------- implementor side of the BRIDGE ----------
interface Drink { String getName(); List<String> getIngredients(); int getCalories(); }
class Coke implements Drink {
    public String getName() { return "Coke"; }
    public List<String> getIngredients() { return List.of("carbonated water", "sugar", "caramel"); }
    public int getCalories() { return 140; }
}
class Lemonade implements Drink {
    public String getName() { return "Lemonade"; }
    public List<String> getIngredients() { return List.of("lemon juice", "sugar", "water"); }
    public int getCalories() { return 200; }
}
class MangoJuice implements Drink {
    public String getName() { return "Mango Juice"; }
    public List<String> getIngredients() { return List.of("mango pulp", "water"); }
    public int getCalories() { return 180; }
}

// ---------- abstraction side of the BRIDGE ----------
abstract class SetMenu {
    private final String name;
    private final double basePrice;
    private final List<String> foodItems;
    private final int foodCalories;
    protected final Drink drink;                                      // the bridge

    protected SetMenu(String n, double p, List<String> f, int c, Drink d) {
        name = n; basePrice = p; foodItems = f; foodCalories = c; drink = d; }
    double getBasePrice()    { return basePrice; }                    // the drink never affects the price
    String getDescription()  { return name + " with " + drink.getName(); }
    int getTotalCalories()   { return foodCalories + drink.getCalories(); }
    String receiptLine()     { return getDescription() + ", " + getTotalCalories() + " kcal"; }
}
class BurgerMeal extends SetMenu {
    BurgerMeal(Drink d) { super("Burger Meal", 350, List.of("burger", "fries"), 650, d); }
}
class RiceMeal   extends SetMenu {
    RiceMeal(Drink d)   { super("Rice Meal",   300, List.of("rice", "chicken curry"), 700, d); }
}
class PastaMeal  extends SetMenu {
    PastaMeal(Drink d)  { super("Pasta Meal",  380, List.of("pasta", "garlic bread"), 760, d); }
}

class Customer { final String name; final int loyaltyPoints; Customer(String n, int p) { name = n; loyaltyPoints = p; } }

// ---------- STRATEGY ----------
interface PricingStrategy { double price(double basePrice, Customer customer); }
class RegularPricing implements PricingStrategy { public double price(double b, Customer c) { return b; } }
class HappyHourPricing implements PricingStrategy {
    private final double percent;
    HappyHourPricing(double percent) { this.percent = percent; }
    public double price(double b, Customer c) { return b - b * percent / 100; }
}
class LoyaltyPricing implements PricingStrategy {
    // 1 % off per 100 points, at most 20 % (assumed rule)
    public double price(double b, Customer c) {
        double pct = Math.min(20, c.loyaltyPoints / 100); return b - b * pct / 100; }
}

class Order {
    private final SetMenu menu;
    private final Customer customer;
    private PricingStrategy pricing = new RegularPricing();
    Order(SetMenu m, Customer c) { menu = m; customer = c; }
    void setPricing(PricingStrategy p) { pricing = p; }                // chosen at checkout, changeable at run time
    double amountPayable() { return pricing.price(menu.getBasePrice(), customer); }
    String receipt() { return menu.receiptLine() + " | pay " + amountPayable(); }
}

public class Main {
    public static void main(String[] a) {
        Customer c = new Customer("Rina", 450);
        Order o = new Order(new BurgerMeal(new Lemonade()), c);
        System.out.println(o.receipt());
        o.setPricing(new HappyHourPricing(10));  System.out.println(o.receipt());
        o.setPricing(new LoyaltyPricing());      System.out.println(o.receipt());
    }
}
