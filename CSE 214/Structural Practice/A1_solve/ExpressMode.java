public class ExpressMode implements DeliveryMode {

    private static final double surCharge=10.0;
    @Override
    public String getModeName(){
        return "Express";
    }

    @Override
    public double getSurCharge(){
        return surCharge;
    }
    @Override
    public DeliveryTime getEstimatedTime(boolean isInternational,DeliveryTime regionBaseTime){
        return isInternational? new DeliveryTime(1, 1, "week"): new DeliveryTime(2, 2, "days");
    }


}
