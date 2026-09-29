package prev_C1;

public class SpecialPackage implements RamadanPackage{
    @Override
    public String description(){
        return "Special Package";
    }
    @Override
    public double price(){
        return 1500.0;
    }
}
