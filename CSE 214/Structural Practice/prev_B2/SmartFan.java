package prev_B2;

public class SmartFan implements SmartDevice{
    @Override
    public void turnOn(){
        System.out.println("Smart fan on");
    }
    @Override
    public void turnOff(){
        System.out.println("Smart fan off");
    }
}
