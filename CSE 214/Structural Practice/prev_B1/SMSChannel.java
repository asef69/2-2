package prev_B1;

public class SMSChannel implements NotificationChannel{
    @Override
    public void sendMessage(String indent){
        System.out.println("Email: "+ indent);
    }
}
