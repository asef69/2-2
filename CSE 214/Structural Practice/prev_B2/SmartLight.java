package prev_B2;

public class SmartLight implements SmartDevice{
    @Override
    public void turnOn(){
        System.out.println("Smart light on");
    }
    @Override
    public void turnOff(){
        System.out.println("Smart light off");
    }
}
