package B2_solve;

public class Food implements OrderItem {
    private final String name;
    private final double price;
    public Food(String name, double price){
        this.name=name;
        this.price=price;
    }

    public String getName(){
        return name;
    }

    @Override
    public double getPrice(){
        return price;
    }
    @Override
    public void print(String indent){
        System.out.printf("%s- %s - £%.2f%n", indent, name, getPrice());
    }
}
