public abstract class GiftDecorator implements Gift{
    protected final Gift wrappedGift;

     protected GiftDecorator(Gift wrappedGift){
        this.wrappedGift=wrappedGift;
    }

    @Override
    public String getDescription(){
        return wrappedGift.getDescription();
    }
    @Override
    public double getPrice(){
        return wrappedGift.getPrice();
    }
}
