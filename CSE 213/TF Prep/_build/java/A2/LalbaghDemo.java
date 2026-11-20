// 2017-18 Q6(a) — Builder: set meals (rice + curries, or bread + kebabs), optional drinks, bill first
import java.util.ArrayList;
import java.util.List;

class Food {
    final String name; final double price;
    Food(String name, double price) { this.name = name; this.price = price; }
}
class SetMeal {                                                // product
    private final List<Food> items = new ArrayList<>();
    void add(Food f) { items.add(f); }
    double bill() { double s = 0; for (Food f : items) s += f.price; return s; }
    void show() {
        for (Food f : items) System.out.printf("  %-20s %6.1f%n", f.name, f.price);
        System.out.printf("  %-20s %6.1f%n", "BILL (pay first)", bill());
    }
}
abstract class SetMealBuilder {                                // builder
    protected final SetMeal meal = new SetMeal();
    abstract void addMainItem();
    abstract void addSides();
    void addDrink(String name, double price) { meal.add(new Food(name, price)); }
    SetMeal getMeal() { return meal; }
}
class RiceMealBuilder extends SetMealBuilder {
    void addMainItem() { meal.add(new Food("Plain rice", 40)); }
    void addSides()    { meal.add(new Food("Chicken gravy curry", 90)); meal.add(new Food("Dal", 20)); }
}
class ChickenKebabMealBuilder extends SetMealBuilder {
    void addMainItem() { meal.add(new Food("Naan x2", 30)); }
    void addSides()    { meal.add(new Food("Chicken kebab", 110)); }
}
class BeefKebabMealBuilder extends SetMealBuilder {
    void addMainItem() { meal.add(new Food("Naan x2", 30)); }
    void addSides()    { meal.add(new Food("Beef kebab", 140)); }
}
class Waiter {                                                 // director
    SetMeal prepare(SetMealBuilder b, String drink, double drinkPrice) {
        b.addMainItem();
        b.addSides();
        if (drink != null) b.addDrink(drink, drinkPrice);       // drinks are optional extras
        return b.getMeal();
    }
}
public class LalbaghDemo {
    public static void main(String[] args) {
        Waiter w = new Waiter();
        System.out.println("Rice set + lemonade:");
        w.prepare(new RiceMealBuilder(), "Lemonade", 35).show();
        System.out.println("Bread + beef kebab, no drink:");
        w.prepare(new BeefKebabMealBuilder(), null, 0).show();
    }
}
