package prev_C1;

public class PremiumPackage implements RamadanPackage{
    @Override
    public String description(){
        return "Premium Package";
    }
    @Override
    public double price(){
        return 2500.0;
    }
}
