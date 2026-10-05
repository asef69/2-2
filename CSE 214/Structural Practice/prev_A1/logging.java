package prev_A1;

public class logging extends NotificationDecorator{
    public logging(Notification n){
        super(n);
    }
    @Override
    public void send(){
        notification.send();
        System.out.println("Audit logging");
    }
}
