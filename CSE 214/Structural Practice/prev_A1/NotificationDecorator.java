package prev_A1;

public abstract class NotificationDecorator  extends Notification{
     protected Notification notification;
    public NotificationDecorator(Notification n){
        this.notification=n;
    }
    @Override
    public void send(){
        System.out.println("Decorating the notification");
    }
}
