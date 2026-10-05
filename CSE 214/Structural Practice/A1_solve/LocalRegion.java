public class LocalRegion extends DeliveryRegion {
 
    public LocalRegion(DeliveryMode mode) {
        super(mode);
    }
 
    @Override
    protected double getRegionCharge(double distanceInMiles) {
        return distanceInMiles * 1.0;
    }
 
    @Override
    protected DeliveryTime getRegionBaseTime() {
        return new DeliveryTime(1, 1, "week");
    }
 
    @Override
    protected boolean isInternational() {
        return false;
    }
 
    @Override
    protected String getRegionName() {
        return "Local Delivery";
    }
}