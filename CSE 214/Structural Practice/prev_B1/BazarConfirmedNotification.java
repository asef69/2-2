package prev_B1;

/**
 * BazarConfirmedNotification
 */
public class BazarConfirmedNotification extends Notification{
    public BazarConfirmedNotification(NotificationChannel channel){
        super(channel);
    }
    @Override
    public void notifyUser(){
        channel.sendMessage("Bazar is confirmed");
    }
}
