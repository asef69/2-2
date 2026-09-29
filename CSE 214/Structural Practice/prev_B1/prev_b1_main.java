package prev_B1;

public class prev_b1_main {
    public static void main(String[] args) {
        // Any event type can be paired with any channel, independently.
        Notification n1 = new BazarConfirmedNotification(new EmailChannel());
        Notification n2 = new BazarDispatchedNotification(new SMSChannel());
        Notification n3 = new PaymentFailedNotification(new PushChannel());
        Notification n4 = new BazarRenewedNotification(new WhatsAppChannel());
 
        n1.notifyUser();
        n2.notifyUser();
        n3.notifyUser();
        n4.notifyUser();
 
        // Adding a new channel (e.g. Telegram) or new event type later requires
        // no change to the other dimension's classes.
    }
}
