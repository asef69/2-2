package prev_B2;

public class OldSmartBulbAdapter implements SmartDevice{
    private OldSmartBulb bulb;
    
    public OldSmartBulbAdapter(OldSmartBulb bulb) {
        this.bulb = bulb;
    }

    @Override
    public void turnOn(){
        bulb.powerOn();
    }
    @Override
    public void turnOff(){
        bulb.powerOff();
    }
}