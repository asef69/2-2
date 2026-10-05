package prev_B1;

public abstract class Notification {
    protected NotificationChannel channel;
    public Notification(NotificationChannel channel){
        this.channel=channel;
    }
    public abstract void notifyUser();
}
