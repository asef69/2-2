package prev_A1;

public class Encrypted extends NotificationDecorator{
    public Encrypted(Notification n){
        super(n);
    }
    @Override
    public void send(){
        notification.send();
        System.out.println("Encrypted");
    }
}
