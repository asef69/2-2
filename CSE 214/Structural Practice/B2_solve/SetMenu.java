package B2_solve;

import java.util.ArrayList;
import java.util.List;

public class SetMenu implements OrderItem{
    private final String name;
    private final List<Food> foods=new ArrayList<>();
    private static final double discount=0.10;

    public SetMenu(String name){
        this.name=name;
    }
    public void addFood(Food food){
        foods.add(food);
    }
    @Override
    public double getPrice() {
        double total = 0;
        for (Food food : foods) {
            total += food.getPrice();
        }
        return total * (1 - discount);
    }

    @Override
    public void print(String indent){
        System.out.printf("%s- %s (Set Menu) - £%.2f%n", indent, name, getPrice());
        String childIndent = indent + "    ";
        for (Food food : foods) {
            food.print(childIndent);
        }
    }

}