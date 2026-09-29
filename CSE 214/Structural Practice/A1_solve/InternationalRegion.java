public class InternationalRegion extends DeliveryRegion {
    private static final double SURCHARGE = 500.0;
 
    public InternationalRegion(DeliveryMode mode) {
        super(mode);
    }
 
    @Override
    protected double getRegionCharge(double distanceInMiles) {
        return SURCHARGE;
    }
 
    @Override
    protected DeliveryTime getRegionBaseTime() {
        return new DeliveryTime(2, 3, "weeks");
    }
 
    @Override
    protected boolean isInternational() {
        return true;
    }
 
    @Override
    protected String getRegionName() {
        return "International Delivery";
    }
}