package prev_B1;

/**
 * BazarDispatchedNotification
 */
public class BazarDispatchedNotification extends Notification{

    public BazarDispatchedNotification(NotificationChannel channel) {
        super(channel);
    }

    @Override
    public void notifyUser(){
        channel.sendMessage("Bazar dispatched");
    }
}
