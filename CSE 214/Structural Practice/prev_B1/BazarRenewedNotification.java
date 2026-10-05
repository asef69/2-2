package prev_B1;

public class BazarRenewedNotification extends Notification{

    public BazarRenewedNotification(NotificationChannel channel) {
        super(channel);
    }
    @Override
    public void notifyUser(){
        channel.sendMessage("Bazar renewed");
    }
}
