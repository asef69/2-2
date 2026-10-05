package b2_22;

interface Notification{
    void notifyUser();
}

class SMS implements Notification{
    @Override
    public void notifyUser(){
        System.out.println("SMS notification");
    }
}

class Email implements Notification{
    @Override
    public void notifyUser(){
        System.out.println("Email notification");
    }
}

class Push implements Notification{
    @Override
    public void notifyUser(){
        System.out.println("Push notification");
    }
}

class Factory{
    public static Notification construct(String type){
        if(type.equalsIgnoreCase("SMS")){
            return new SMS();
        }
        else if(type.equalsIgnoreCase("Push")){
            return new Push();
        }
        else if(type.equalsIgnoreCase("Email")){
            return new Email();
        }
        else{
            throw new IllegalAccessError("Wrong access");
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Notification notification=Factory.construct("SMS");
        notification.notifyUser();
    }
}
