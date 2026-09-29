public class StandardMode implements DeliveryMode{
    private static final double surCharge=0.0;
    @Override
    public String getModeName(){
        return "Standard";
    }

    @Override
    public double getSurCharge(){
        return surCharge;
    }
    @Override
    public DeliveryTime getEstimatedTime(boolean isInternational,DeliveryTime regionBaseTime){
        return regionBaseTime;
    }
}
