// IJ Misc deck p7-8 — Bridge: notification kind x sending channel
interface MessageSender { void send(String msg); }                    // implementation hierarchy
class EmailSender implements MessageSender { public void send(String m) { System.out.println("Email: " + m); } }
class SmsSender   implements MessageSender { public void send(String m) { System.out.println("SMS: " + m); } }
class PushSender  implements MessageSender { public void send(String m) { System.out.println("Push: " + m); } }

abstract class Notification {                                         // abstraction
    protected final MessageSender sender;                             // the bridge
    Notification(MessageSender s) { sender = s; }
    abstract void notifyUser();
}
class AlertNotification extends Notification {
    AlertNotification(MessageSender s) { super(s); }
    void notifyUser() { sender.send("Server is down!"); }
}
class OtpNotification extends Notification {
    OtpNotification(MessageSender s) { super(s); }
    void notifyUser() { sender.send("Your OTP is 482913"); }
}
class PromotionNotification extends Notification {
    PromotionNotification(MessageSender s) { super(s); }
    void notifyUser() { sender.send("50% off this weekend"); }
}
public class NotificationBridge {
    public static void main(String[] args) {
        new AlertNotification(new SmsSender()).notifyUser();
        new OtpNotification(new EmailSender()).notifyUser();
        new PromotionNotification(new PushSender()).notifyUser();
    }
}
