package a1_22_factory;

interface Transport{
    void deliver();
}

class Truck implements Transport{
    @Override
    public void deliver(){
        System.out.println("delivering from Truck");
    }
}

class Ship implements Transport{
    @Override
    public void deliver(){
        System.out.println("delivering from Ship");
    }
}

class Factory{
    public static Transport construct(String deliveryMode){
        if(deliveryMode.equalsIgnoreCase("road")){
            return new Truck();
        }
        else if(deliveryMode.equalsIgnoreCase("sea")){
            return new Ship();
        }
        else{
            throw new IllegalAccessError("Dispossible");
        }
    }
    
}

public class Main {
    public static void main(String[] args) {
        Transport transport=Factory.construct("road");
        transport.deliver();
    }
}
