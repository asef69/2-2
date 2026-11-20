// 2023-24 Q5(a) — Abstract Factory: each region creates a consistent family of ingredients
interface Crust   { String name(); }
interface Sauce   { String name(); }
interface Topping { String name(); }

class ThinCrust       implements Crust   { public String name() { return "thin crust"; } }
class MarinaraSauce   implements Sauce   { public String name() { return "marinara"; } }
class Mozzarella      implements Topping { public String name() { return "fresh mozzarella, basil"; } }
class DeepDishCrust   implements Crust   { public String name() { return "deep-dish crust"; } }
class PlumTomatoSauce implements Sauce   { public String name() { return "plum-tomato sauce"; } }
class Pepperoni       implements Topping { public String name() { return "cheddar, pepperoni"; } }

interface PizzaIngredientFactory {                 // abstract factory
    Crust createCrust();
    Sauce createSauce();
    Topping createTopping();
}
class ItalyIngredientFactory implements PizzaIngredientFactory {
    public Crust createCrust()     { return new ThinCrust(); }
    public Sauce createSauce()     { return new MarinaraSauce(); }
    public Topping createTopping() { return new Mozzarella(); }
}
class AmericaIngredientFactory implements PizzaIngredientFactory {
    public Crust createCrust()     { return new DeepDishCrust(); }
    public Sauce createSauce()     { return new PlumTomatoSauce(); }
    public Topping createTopping() { return new Pepperoni(); }
}
class RegionalPizza {                              // client: never names a concrete ingredient
    private final Crust crust; private final Sauce sauce; private final Topping topping;
    RegionalPizza(PizzaIngredientFactory f) {
        crust = f.createCrust(); sauce = f.createSauce(); topping = f.createTopping();
    }
    public String toString() { return crust.name() + " + " + sauce.name() + " + " + topping.name(); }
}
public class PizzaDemo {
    static PizzaIngredientFactory factoryFor(String country) {   // chosen once
        switch (country) {
            case "Italy":   return new ItalyIngredientFactory();
            case "America": return new AmericaIngredientFactory();
            default: throw new IllegalArgumentException(country);
        }
    }
    public static void main(String[] args) {
        System.out.println("Italy:   " + new RegionalPizza(factoryFor("Italy")));
        System.out.println("America: " + new RegionalPizza(factoryFor("America")));
    }
}
