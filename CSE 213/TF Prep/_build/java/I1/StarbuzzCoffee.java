// Slides 33-46 — Decorator: Starbuzz beverages and condiments (Head First)
abstract class Beverage {
    String description = "Unknown Beverage";
    public String getDescription() { return description; }
    public abstract double cost();
}
abstract class CondimentDecorator extends Beverage {
    Beverage beverage;                                   // the wrapped component
    public abstract String getDescription();
}
class Espresso extends Beverage {
    Espresso() { description = "Espresso"; }
    public double cost() { return 1.99; }
}
class DarkRoast extends Beverage {
    DarkRoast() { description = "Dark Roast Coffee"; }
    public double cost() { return .99; }
}
class HouseBlend extends Beverage {
    HouseBlend() { description = "House Blend Coffee"; }
    public double cost() { return .89; }
}
class Mocha extends CondimentDecorator {
    Mocha(Beverage b) { beverage = b; }
    public String getDescription() { return beverage.getDescription() + ", Mocha"; }
    public double cost() { return .20 + beverage.cost(); }
}
class Whip extends CondimentDecorator {
    Whip(Beverage b) { beverage = b; }
    public String getDescription() { return beverage.getDescription() + ", Whip"; }
    public double cost() { return .10 + beverage.cost(); }
}
class Soy extends CondimentDecorator {
    Soy(Beverage b) { beverage = b; }
    public String getDescription() { return beverage.getDescription() + ", Soy"; }
    public double cost() { return .15 + beverage.cost(); }
}
public class StarbuzzCoffee {
    public static void main(String[] args) {
        Beverage b1 = new Espresso();
        System.out.printf("%s $%.2f%n", b1.getDescription(), b1.cost());
        Beverage b2 = new Whip(new Mocha(new Mocha(new DarkRoast())));
        System.out.printf("%s $%.2f%n", b2.getDescription(), b2.cost());
        Beverage b3 = new Whip(new Mocha(new Soy(new HouseBlend())));
        System.out.printf("%s $%.2f%n", b3.getDescription(), b3.cost());
    }
}
