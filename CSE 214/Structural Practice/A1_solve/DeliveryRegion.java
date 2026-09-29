public abstract class DeliveryRegion {
    protected final DeliveryMode mode;

    protected DeliveryRegion(DeliveryMode mode){
        this.mode=mode;
    }

    protected abstract double getRegionCharge(double distance);
    protected abstract DeliveryTime getRegionBaseTime();
    protected abstract boolean isInternational();
    protected abstract String getRegionName();

    public final double getTotalDeliveryCharge(double distance){
        return getRegionCharge(distance)+mode.getSurCharge();
    }

    public final DeliveryTime getDeliveryTime(){
        return mode.getEstimatedTime(isInternational(), getRegionBaseTime());
    }

    public final String getDescription(){
        return getRegionName()+"("+mode.getModeName()+")";
    }
}
