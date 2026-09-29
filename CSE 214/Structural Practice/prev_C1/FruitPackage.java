package prev_C1;

public class FruitPackage extends PackageDecorator{

    public FruitPackage(RamadanPackage p) {
        super(p);
    }
    @Override
    public String description(){
        return p.description()+" Fruit ";
    }
    @Override
    public double price(){
        return p.price()+200.0;
    }
}
