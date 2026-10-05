package prev_A2;

import java.util.ArrayList;
import java.util.List;

public class bazarpackage implements bazarcomponent{
    private String name;
    private List<bazarcomponent> bazar=new ArrayList<>();

    public bazarpackage(String name){
        this.name=name;
    }

    public void add(bazarcomponent b){
        bazar.add(b);
    }
    public void remove(bazarcomponent b){
        bazar.remove(b);
    }

    @Override
    public String name(){
        return name;
    }
    @Override
    public double weight(){
        double total=0.0;
        for(bazarcomponent b:bazar){
            total+=b.weight();
        }
        return total;
    }
    @Override
    public double price(){
        double total=0.0;
        for(bazarcomponent b :bazar){
            total+=b.price();
        }
        return total;
    }
    @Override
    public void print(String indent){
        System.out.printf("%s- %s (Price: %.2f, Weight: %.2fkg)%n", indent, name, price(), weight());
        for (bazarcomponent b : bazar) {
            b.print(indent + "    ");
        }
    }
}
