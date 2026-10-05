public class PriorityMode implements DeliveryMode{
    private static final double surCharge=25.0;
    @Override
    public String getModeName(){
        return "Priority";
    }

    @Override
    public double getSurCharge(){
        return surCharge;
    }
    @Override
    public DeliveryTime getEstimatedTime(boolean isInternational,DeliveryTime regionBaseTime){
        return isInternational? new DeliveryTime(5, 5, "days"): new DeliveryTime(1, 1, "days");
    }
}
