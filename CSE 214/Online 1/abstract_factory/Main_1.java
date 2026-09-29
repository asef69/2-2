package abstract_factory;

interface Sofa{
    void run();
}
interface Chair{
    void run();
}

class ModernSofa implements Sofa{
    @Override
    public void run(){
        System.out.println("Modern Sofa");
    }
}
class VictorianSofa implements Sofa{
    @Override
    public void run(){
        System.out.println("Victorian Sofa");
    }
}

class ModernChair implements Chair{
    @Override
    public void run(){
        System.out.println("Modern Chair");
    }
}

class VictorianChair implements Chair{
    @Override
    public void run(){
        System.out.println("Victorian Chair");
    }
}

interface FurnitureFactory{
    Sofa createSofa();
    Chair createChair();
}

class ModernFactory implements FurnitureFactory{


    @Override
    public Chair createChair() {
        
        return new ModernChair();
    }

    @Override
    public Sofa createSofa() {
        return new ModernSofa();
    }
    
}

class VictorianFactory implements FurnitureFactory{


    @Override
    public Chair createChair() {
        
        return new VictorianChair();
    }

    @Override
    public Sofa createSofa() {
        return new VictorianSofa();
    }
    
}

class Application{
    private Chair chair;
    private Sofa sofa;

    

    public Application(FurnitureFactory factory) {
        chair=factory.createChair();
        sofa=factory.createSofa();
    }



    public void run(){
        chair.run();
        sofa.run();
    }
}

public class Main_1 {
    public static void main(String[] args) {
        FurnitureFactory factory=new ModernFactory();
        FurnitureFactory newFactory=new VictorianFactory();
        Application app=new Application(factory);
        app.run();

        app=new Application(newFactory);
        app.run();
    }
}
