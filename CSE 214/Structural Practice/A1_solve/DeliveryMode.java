public interface DeliveryMode {
    String getModeName();
    double getSurCharge();
    DeliveryTime getEstimatedTime(boolean isInternational,DeliveryTime regionBaseTime);
}
