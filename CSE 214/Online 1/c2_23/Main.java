package c2_23;

class GamingSetup{
    private String monitor;
    private String keyboard;
    private String mouse;
    public void setMonitor(String monitor) {
        this.monitor = monitor;
    }
    public void setKeyboard(String keyboard) {
        this.keyboard = keyboard;
    }
    public void setMouse(String mouse) {
        this.mouse = mouse;
    }

    @Override
    public String toString(){
        return "GamingSetup [Monitor=" + monitor + ", Keyboard=" + keyboard + ", Mouse=" + mouse + "]";
    }
}

interface setupBuilder{
    void buildMonitor();
    void buildKeyboard();
    void buildMouse();

    GamingSetup gamingSetup();
}

class competitiveSetup implements setupBuilder{
    private GamingSetup setup=new GamingSetup();

    @Override
    public void buildKeyboard() {
        setup.setKeyboard("Mechanical Keyboard");
    }

    @Override
    public void buildMonitor() {
      setup.setMonitor("240 Hz Monitor");
    }

    @Override
    public void buildMouse() {
       setup.setMouse("Lightweight Mouse");
        
    }

    @Override
    public GamingSetup gamingSetup() {
        return setup;
    }
    
}


class casualSetup implements setupBuilder{
    private GamingSetup setup=new GamingSetup();

    @Override
    public void buildKeyboard() {
        setup.setKeyboard("Wireless Keyboard");
    }

    @Override
    public void buildMonitor() {
      setup.setMonitor("Standard Monitor");
    }

    @Override
    public void buildMouse() {
       setup.setMouse("Wireless Mouse");
        
    }

    @Override
    public GamingSetup gamingSetup() {
        return setup;
    }
    
}

class setupDirector{
    private setupBuilder setup;

    public setupDirector(setupBuilder builder){
        this.setup=builder;
    }
    public GamingSetup construct(){
        setup.buildMonitor();
        setup.buildKeyboard();
        setup.buildMouse();

        return setup.gamingSetup();
    }
}



public class Main {
    public static void main(String[] args) {
        setupBuilder competitiveBuilder = new competitiveSetup();
        setupDirector director = new setupDirector(competitiveBuilder);
        
        GamingSetup compSetup = director.construct();
        System.out.println("Competitive: " + compSetup);

        // Client requests a Casual Setup
        setupBuilder casualBuilder = new casualSetup();
        setupDirector newDirector=new setupDirector(casualBuilder);
        
        GamingSetup casualSetup = newDirector.construct();
        System.out.println("Casual: " + casualSetup);
    }
}
