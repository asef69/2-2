package prev_A1;

public class prev_A1_main {
    public static void main(String[] args) {
        Notification email = new EmailNotification();
        email.send();
        System.out.println("-----");
 
        // Email with encryption + priority label
        Notification secureUrgentEmail = new priority(
                new Encrypted(
                        new EmailNotification()));
        secureUrgentEmail.send();
        System.out.println("-----");
 
        // SMS with encryption + logging + priority label (all features combined)
        Notification fullSMS = new logging(
                new priority(
                        new Encrypted(
                                new SMSNotification())));
        fullSMS.send();
        System.out.println("-----");
 
        // Push notification with only logging enabled
        Notification loggedPush = new logging(
                new PushNotification());
        loggedPush.send();
    }
}
