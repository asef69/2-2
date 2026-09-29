package batch_21_B2;

interface Component {
    double getPrice();

    String getDescription();
}

// Concrete Component representing individual hardware components
class HardwareComponent implements Component {
    private String name;
    private double price;

    public HardwareComponent(String name, double price) {
        this.name = name;
        this.price = price;
    }

    @Override
    public double getPrice() {
        return price;
    }

    @Override
    public String getDescription() {
        return name;
    }
}

abstract class HardwareDecorator implements Component{
    protected Component comp;

    public HardwareDecorator(Component comp) {
        this.comp = comp;
    }

    @Override
    public String getDescription() {
        // TODO Auto-generated method stub
        return comp.getDescription();
    }

    @Override
    public double getPrice() {
        // TODO Auto-generated method stub
        return comp.getPrice();
    }
    
} 

class ExtendedWarranty extends HardwareDecorator{

    public ExtendedWarranty(Component comp) {
        super(comp);
    }

    @Override
    public String getDescription() {
        // TODO Auto-generated method stub
        return super.getDescription() +" Warranty";
    }

    @Override
    public double getPrice() {
        // TODO Auto-generated method stub
        return super.getPrice()+1500;
    }
    
}

class InstallationService extends HardwareDecorator{

    public InstallationService(Component comp) {
        super(comp);
    }

    @Override
    public String getDescription() {
        // TODO Auto-generated method stub
        return super.getDescription() +" Installation";
    }

    @Override
    public double getPrice() {
        // TODO Auto-generated method stub
        return super.getPrice()+1500;
    }
    
}
class PerformanceBoost extends HardwareDecorator{

    public PerformanceBoost(Component comp) {
        super(comp);
    }

    @Override
    public String getDescription() {
        // TODO Auto-generated method stub
        return super.getDescription()+" Performance ";
    }

    @Override
    public double getPrice() {
        // TODO Auto-generated method stub
        return super.getPrice()+2000;
    }
    
}

public class Main{
    public static void main(String[] args) {
        Component cpu = new HardwareComponent("CPU", 15000);
        System.out.println(cpu.getDescription() + " -> Price: " + cpu.getPrice());
 
        // GPU with extended warranty and performance boost
        Component gpu = new PerformanceBoost(
                new ExtendedWarranty(
                        new HardwareComponent("Graphics Card", 25000)));
        System.out.println(gpu.getDescription() + " -> Price: " + gpu.getPrice());
 
        // Storage with installation service only
        Component storage = new InstallationService(
                new HardwareComponent("SSD (1TB)", 6000));
        System.out.println(storage.getDescription() + " -> Price: " + storage.getPrice());
 
        // Memory with all three features stacked
        Component ram = new PerformanceBoost(
                new InstallationService(
                        new ExtendedWarranty(
                                new HardwareComponent("Memory (16GB)", 4000))));
        System.out.println(ram.getDescription() + " -> Price: " + ram.getPrice());
    }
}
