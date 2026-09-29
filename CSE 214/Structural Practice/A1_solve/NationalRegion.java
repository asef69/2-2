public class NationalRegion extends DeliveryRegion{
 
    private static final double surCharge=20.0;
    public NationalRegion(DeliveryMode mode) {
        super(mode);
    }
 
    @Override
    protected double getRegionCharge(double distanceInMiles) {
        return distanceInMiles * 1.0+surCharge;
    }
 
    @Override
    protected DeliveryTime getRegionBaseTime() {
        return new DeliveryTime(1, 2, "week");
    }
 
    @Override
    protected boolean isInternational() {
        return false;
    }
 
    @Override
    protected String getRegionName() {
        return "Naional Delivery";
    }
}

