package B2_solve;

import java.util.ArrayList;
import java.util.List;

public class GroceryPackage implements OrderItem {
    private final String name;
    private final List<OrderItem> contents=new ArrayList<>();

    public GroceryPackage(String name){
        this.name=name;
    }
    public void add(OrderItem item){
        contents.add(item);
    }
    @Override
    public double getPrice() {
        double total = 0;
        for (OrderItem item : contents) {
            total += item.getPrice();
        }
        return total;
    }
 
    @Override
    public void print(String indent) {
        System.out.printf("%s- %s (Grocery Package) - £%.2f%n", indent, name, getPrice());
        String childIndent = indent + "    ";
        for (OrderItem item : contents) {
            item.print(childIndent);
        }
    }
}
