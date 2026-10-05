package batch_21_C1;

// CSE-214 Online - 2 (C1) : Structural Design Pattern -> DECORATOR
// Problem: Base coffees (Black Coffee, Milk Coffee) are enhanced with extra
// ingredients to become specific drinks (Americano, Cappuccino). Decorator
// wraps a base Coffee and adds its own ingredient + cost contribution, so
// new coffee types can be added later without touching existing classes.

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

interface Coffee {
    String getIngredients();
    int getCost();
}

// ---------- Concrete Components (base coffees) ----------
class BasicBlackCoffee implements Coffee {
    @Override
    public String getIngredients() {
        return "Mug, Water, Grinded Coffee Beans";
    }
    @Override
    public int getCost() {
        return 100 + 30; // mug + grinded coffee beans
    }
}

class BasicMilkCoffee implements Coffee {
    @Override
    public String getIngredients() {
        return "Mug, Milk, Grinded Coffee Beans";
    }
    @Override
    public int getCost() {
        return 100 + 30 + 50; // mug + grinded coffee beans + milk
    }
}

// ---------- Base Decorator ----------
abstract class CoffeeDecorator implements Coffee {
    protected Coffee wrapped;
    public CoffeeDecorator(Coffee wrapped) { this.wrapped = wrapped; }
    @Override
    public String getIngredients() { return wrapped.getIngredients(); }
    @Override
    public int getCost() { return wrapped.getCost(); }
}

// ---------- Concrete Decorators ----------
class Americano extends CoffeeDecorator {
    public Americano(Coffee wrapped) { super(wrapped); }
    @Override
    public String getIngredients() {
        return wrapped.getIngredients() + ", Extra Grinded Coffee Beans";
    }
    @Override
    public int getCost() {
        return wrapped.getCost() + 30;
    }
}

class Cappuccino extends CoffeeDecorator {
    public Cappuccino(Coffee wrapped) { super(wrapped); }
    @Override
    public String getIngredients() {
        return wrapped.getIngredients() + ", Cinnamon Powder";
    }
    @Override
    public int getCost() {
        return wrapped.getCost() + 50;
    }
}

// Order class to handle multiple coffee orders
class Order {
    private List<Coffee> coffees = new ArrayList<>();

    public void addCoffee(Coffee coffee) {
        coffees.add(coffee);
    }

    public void printOrderDetails() {
        int totalCost = 0;
        int coffeeCount = 1;
        for (Coffee coffee : coffees) {
            System.out.println("Coffee " + coffeeCount + ":");
            System.out.println("Ingredients: " + coffee.getIngredients());
            System.out.println("Cost: " + coffee.getCost() + " taka");
            System.out.println();
            totalCost += coffee.getCost();
            coffeeCount++;
        }
        System.out.println("Total Cost for Order: " + totalCost + " taka");
    }
}

// Main Class
public class C1_Decorator {
    public static void main(String[] args) {
        Order order = new Order();

        // Simulated selections instead of interactive Scanner input,
        // demonstrating: 1 Americano, 1 Cappuccino
        int[] choices = {1, 3, 0};

        for (int choice : choices) {
            if (choice == 0) break;
            Coffee coffee;
            switch (choice) {
                case 1:
                    coffee = new Americano(new BasicBlackCoffee());
                    break;
                case 3:
                    coffee = new Cappuccino(new BasicMilkCoffee());
                    break;
                default:
                    System.out.println("Invalid choice.");
                    continue;
            }
            order.addCoffee(coffee);
        }

        order.printOrderDetails();
    }
}