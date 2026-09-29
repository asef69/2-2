package prev_B2;

public class SmartAC implements SmartDevice{
    @Override
    public void turnOn(){
        System.out.println("Smart ac on");
    }
    @Override
    public void turnOff(){
        System.out.println("Smart ac off");
    }
}
