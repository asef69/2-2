public class DeliveryTime {
    private final double minValue;
    private final double maxValue;
    private final String unit;

    DeliveryTime(double minValue,double maxValue,String unit){
        this.maxValue=maxValue;
        this.minValue=minValue;
        this.unit=unit;
    }

    @Override
    public String toString() {
        if (minValue == maxValue) {
            return trim(minValue) + " " + unit;
        }
        return trim(minValue) + "-" + trim(maxValue) + " " + unit;
    }
 
    private String trim(double v) {
        return (v == (long) v) ? String.valueOf((long) v) : String.valueOf(v);
    }
}
