// 2020-21 Q1(a) — the orders built with three patterns: Decorator (cheese), Composite (orders), Builder (combo meals)
import java.util.ArrayList;
import java.util.List;

interface MenuItem { String desc(); double price(); }          // common component interface
class ShopPizza implements MenuItem {
    private final String kind; private final double p;
    ShopPizza(String kind, double p) { this.kind = kind; this.p = p; }
    public String desc() { return kind + " pizza"; }
    public double price() { return p; }
}
class SimpleItem implements MenuItem {                         // drinks, appetizers
    private final String n; private final double p;
    SimpleItem(String n, double p) { this.n = n; this.p = p; }
    public String desc() { return n; }
    public double price() { return p; }
}
// assumed prices: Veggi 300, Beef 400, Chicken 350, cheese +50; Coffee 80, Water 20, Coke 40;
//                 French Fry 100, Onion Rings 120

// Pattern 1 — DECORATOR: extra cheese wraps any pizza
abstract class PizzaDecorator implements MenuItem {
    protected final MenuItem inner;
    PizzaDecorator(MenuItem i) { inner = i; }
}
class ExtraCheese extends PizzaDecorator {
    ExtraCheese(MenuItem i) { super(i); }
    public String desc() { return inner.desc() + " + cheese"; }
    public double price() { return inner.price() + 50; }
}

// Pattern 2 — COMPOSITE: an order is a MenuItem made of MenuItems
class Order implements MenuItem {
    private final String name;
    private final List<MenuItem> parts = new ArrayList<>();
    Order(String name) { this.name = name; }
    Order add(MenuItem m) { parts.add(m); return this; }
    public String desc() {
        List<String> d = new ArrayList<>();
        for (MenuItem m : parts) d.add(m.desc());
        return name + " [" + String.join(", ", d) + "]";
    }
    public double price() { double s = 0; for (MenuItem m : parts) s += m.price(); return s; }
}

// Pattern 3 — BUILDER: a combo meal is assembled step by step (appetizer, pizza, drinks)
class ComboMeal {
    final List<MenuItem> items = new ArrayList<>();
    double price() { double s = 0; for (MenuItem m : items) s += m.price(); return s; }
}
class ComboBuilder {
    private final ComboMeal meal = new ComboMeal();
    ComboBuilder pizza(String kind, double p, boolean cheese) {
        MenuItem pz = new ShopPizza(kind, p);
        meal.items.add(cheese ? new ExtraCheese(pz) : pz);
        return this;
    }
    ComboBuilder appetizer(String n, double p) { meal.items.add(new SimpleItem(n, p)); return this; }
    ComboBuilder drink(String n, double p)     { meal.items.add(new SimpleItem(n, p)); return this; }
    ComboMeal build() { return meal; }
}
public class BurgerShop {
    public static void main(String[] args) {
        MenuItem o1 = new Order("Order 1").add(new ExtraCheese(new ShopPizza("Beef", 400)))
                                          .add(new SimpleItem("French Fry", 100));
        MenuItem o2 = new Order("Order 2").add(new ShopPizza("Chicken", 350))
                                          .add(new SimpleItem("Onion Rings", 120)).add(new SimpleItem("Water", 20));
        ComboMeal o3 = new ComboBuilder().pizza("Veggi", 300, false).appetizer("French Fry", 100)
                                         .drink("Coke", 40).drink("Coke", 40).build();
        ComboMeal o4 = new ComboBuilder().pizza("Veggi", 300, false).appetizer("Onion Rings", 120)
                                         .drink("Coffee", 80).drink("Water", 20).build();
        System.out.println(o1.desc() + " = " + o1.price());
        System.out.println(o2.desc() + " = " + o2.price());
        System.out.println("Order 3 (combo) = " + o3.price());
        System.out.println("Order 4 (combo) = " + o4.price());
    }
}
