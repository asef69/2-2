package c1_22;

import java.util.function.BiConsumer;

class Bicycle{
    private String frame;
    private String gear;
    private String tire;
    public void setFrame(String frame) {
        this.frame = frame;
    }
    public void setGear(String gear) {
        this.gear = gear;
    }
    public void setTire(String tire) {
        this.tire = tire;
    }
    @Override
    public String toString() {
        return "Bicycle [frame=" + frame + ", gear=" + gear + ", tire=" + tire + "]";
    }
    
}

interface Builder{
    void setFrame();
    void setGear();
    void setTire();

    Bicycle getCycle();
}

class Commuter implements Builder{
    private Bicycle cycle=new Bicycle();

    @Override
    public Bicycle getCycle() {
        return cycle;
    }

    @Override
    public void setFrame() {
        cycle.setFrame("Aluminium Frame");
    }

    @Override
    public void setGear() {
        cycle.setGear("Single Speed Gear");
    }

    @Override
    public void setTire() {
        cycle.setTire("Road Tire");
    } 
}

class MountainBeast implements Builder{
    private Bicycle cycle=new Bicycle();

    @Override
    public Bicycle getCycle() {
        return cycle;
    }

    @Override
    public void setFrame() {
        cycle.setFrame("Carbon Fibre Frame");
    }

    @Override
    public void setGear() {
        cycle.setGear("12 Speed Gear");
    }

    @Override
    public void setTire() {
        cycle.setTire("Off Road Grip Tire");
    } 
}

class Director{
    public Bicycle construct(Builder builder){
        builder.setFrame();
        builder.setGear();
        builder.setTire();
        return builder.getCycle();
    }
}

public class Main {
    public static void main(String[] args) {
        
        Director director=new Director();
        Bicycle commuter=director.construct(new Commuter());
        System.out.println(commuter);
        Bicycle mountain=director.construct(new MountainBeast()) ;
        System.out.println(mountain);
    }
}
