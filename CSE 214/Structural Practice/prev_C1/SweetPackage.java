package prev_C1;

public class SweetPackage extends PackageDecorator{

    public SweetPackage(RamadanPackage p) {
        super(p);
    }
    @Override
    public String description(){
        return p.description()+" Gift ";
    }
    @Override
    public double price(){
        return p.price()+450.0;
    }
}
