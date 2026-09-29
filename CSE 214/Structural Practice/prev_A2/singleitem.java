package prev_A2;

public class singleitem implements bazarcomponent {
    private String name;
    private double weight,price;
    public singleitem(String name, double weight,double price){
        this.name=name;
        this.weight=weight;
        this.price=price;
    }

    @Override
    public String name(){
        return name;
    }
    @Override
    public double weight(){
        return weight;
    }
    @Override
    public double price(){
        return price;
    }
    @Override
    public void print(String indent){
        System.out.printf("%s- %s (Price: %.2f, Weight: %.2fkg)%n", indent, name, price, weight);
    }
}
