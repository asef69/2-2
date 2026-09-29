package prev_B1;

public class PaymentFailedNotification extends Notification{

    public PaymentFailedNotification(NotificationChannel channel) {
        super(channel);
    }
    @Override
    public void notifyUser(){
        channel.sendMessage("Payment Failed");
    }
}
