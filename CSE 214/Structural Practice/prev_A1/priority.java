package prev_A1;

public class priority extends NotificationDecorator{
    public priority(Notification n){
        super(n);
    }
    @Override
    public void send(){
        notification.send();
        System.out.println("priority labeling");
    }
}
