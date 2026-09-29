package prev_C1;

public class GiftPackage extends PackageDecorator{

    public GiftPackage(RamadanPackage p) {
        super(p);
    }
    @Override
    public String description(){
        return p.description()+" Gift ";
    }
    @Override
    public double price(){
        return p.price()+1000.0;
    }
}
