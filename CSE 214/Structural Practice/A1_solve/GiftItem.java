public class GiftItem implements Gift {
    private final String description;
    private final double price;

    GiftItem(String description, double price){
        this.description=description;
        this.price=price;
    }

    @Override
    public String getDescription(){
        return description;
    }
    @Override
    public double getPrice(){
        return price;
    }
}
