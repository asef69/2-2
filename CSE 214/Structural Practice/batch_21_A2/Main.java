package batch_21_A2;

import java.util.*;


interface ComputerPart {
    String getName();
    double getPrice();
    void print(String indent);
}

class HardwarePart implements ComputerPart{

    private String name;
    private double price;

    
    public HardwarePart(String name, double price) {
        this.name = name;
        this.price = price;
    }

    @Override
    public String getName() {
        // TODO Auto-generated method stub
        return name;
    }

    @Override
    public double getPrice() {
        // TODO Auto-generated method stub
        return price;
    }

    @Override
    public void print(String indent) {
        // TODO Auto-generated method stub
        System.out.printf("%s- %s: %.2f%n", indent, name, price);
    }
    
}

class Bundle implements ComputerPart{
    private String name;
    private List<ComputerPart> parts=new ArrayList<>();
    public Bundle(String name) {
        this.name = name;
    }

    void addPart(ComputerPart c){
        parts.add(c);
    }
    void removePart(ComputerPart c){
        parts.remove(c);
    }
    @Override
    public String getName() {
        // TODO Auto-generated method stub
        return name;
    }

    @Override
    public double getPrice() {
        // TODO Auto-generated method stub
        double total = 0;
        for (ComputerPart p : parts) total += p.getPrice();
        return total;
    }

    @Override
    public void print(String indent) {
        // TODO Auto-generated method stub
        System.out.printf("%s+ %s (Total: %.2f)%n", indent, name, getPrice());
        for (ComputerPart p : parts) p.print(indent + "    ");
    }
}

public class Main {
    public static void main(String[] args) {
        // Individual components
        HardwarePart cpu = new HardwarePart("CPU", 15000);
        HardwarePart ram = new HardwarePart("Memory (16GB)", 4000);
        HardwarePart storage = new HardwarePart("SSD (1TB)", 6000);
        HardwarePart gpu = new HardwarePart("Graphics Card", 25000);
        HardwarePart extraCoolingFan = new HardwarePart("Extra Cooling Fan", 800);
        HardwarePart rgbKit = new HardwarePart("RGB Lighting Kit", 1200);
 
        // Basic Gaming Setup bundle
        Bundle basicGamingSetup = new Bundle("Basic Gaming Setup");
        basicGamingSetup.addPart(cpu);
        basicGamingSetup.addPart(ram);
        basicGamingSetup.addPart(storage);
        basicGamingSetup.addPart(gpu);
 
        System.out.println("A customer buys an individual component:");
        cpu.print("");
        System.out.printf("Price: %.2f%n%n", cpu.getPrice());
 
        System.out.println("Basic Gaming Setup bundle:");
        basicGamingSetup.print("");
        System.out.println();
 
        // Ultimate Gaming Setup bundle contains the Basic bundle + extras (bundle of bundles)
        Bundle ultimateGamingSetup = new Bundle("Ultimate Gaming Setup");
        ultimateGamingSetup.addPart(basicGamingSetup);
        ultimateGamingSetup.addPart(extraCoolingFan);
        ultimateGamingSetup.addPart(rgbKit);
 
        System.out.println("Ultimate Gaming Setup bundle (contains Basic bundle + extras):");
        ultimateGamingSetup.print("");
 
        // Removing a part from a bundle
        System.out.println("\nRemoving RGB Lighting Kit from Ultimate Gaming Setup...");
        ultimateGamingSetup.removePart(rgbKit);
        ultimateGamingSetup.print("");
    }
}
