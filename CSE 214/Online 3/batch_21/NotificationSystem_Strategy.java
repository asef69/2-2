package batch_21;

interface Notification {
    void send(String customer, String message);
}

class Email implements Notification {
    @Override
    public void send(String customer, String message) {
        System.out.println(" email Notification to:" + customer + ",message:" + message);
    }
}

class SMS implements Notification {
    @Override
    public void send(String customer, String message) {
        System.out.println("sms Notification to:" + customer + ",message:" + message);
    }
}

class AppPush implements Notification {
    @Override
    public void send(String customer, String message) {
        System.out.println("App Notification to:" + customer + ",message:" + message);
    }
}

class NotificationService {
    private Notification notification;

    public void setChannel(Notification n) {
        notification = n;
    }

    public void notifyCustomer(String customer, String message) {
        notification.send(customer, message);
    }
}

public class NotificationSystem_Strategy {
    public static void main(String[] args) {
        NotificationService service = new NotificationService();
        service.setChannel(new Email());
        service.notifyCustomer("Asef Kabir", "Here is your email notification");
        service.setChannel(new SMS());
        service.notifyCustomer("Asef Kabir", "Here is your SMS notification");
        service.setChannel(new AppPush());
        service.notifyCustomer("Asef Kabir", "Here is your app notification");
    }
}
