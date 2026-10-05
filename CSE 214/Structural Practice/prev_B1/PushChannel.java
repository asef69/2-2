package prev_B1;

public class PushChannel implements NotificationChannel{
    @Override
    public void sendMessage(String indent){
        System.out.println("Email: "+ indent);
    }
}
