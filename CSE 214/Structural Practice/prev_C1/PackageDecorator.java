package prev_C1;

public abstract class PackageDecorator implements RamadanPackage{
    protected RamadanPackage p;
    public PackageDecorator(RamadanPackage p) {
        this.p=p;
    }
    @Override
    public String description(){
        return p.description();
    }
    @Override
    public double price(){
        return p.price();
    }
    

}
