public class WrappingDecorator extends GiftDecorator {
    private static final double WRAPPING_CHARGE = 2.0;
 
    public WrappingDecorator(Gift gift) {
        super(gift);
    }
 
    @Override
    public String getDescription() {
        return wrappedGift.getDescription() + " (Gift Wrapped)";
    }
 
    @Override
    public double getPrice() {
        return wrappedGift.getPrice() + WRAPPING_CHARGE;
    }
}