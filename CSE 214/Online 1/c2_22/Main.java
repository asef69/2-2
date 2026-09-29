package c2_22;

class GameConfig{
    private static GameConfig instance;
    private GameConfig(){

    } 
    public static GameConfig getInstance(){
        if(instance==null){
            instance=new GameConfig();
        }
        return instance;
    }
}

class Graphics{
    public void run(){
        System.out.println("Graphics: "+GameConfig.getInstance());
    }
}

class Audio{
    public void run(){
        System.out.println("Audio: "+GameConfig.getInstance());
    }
}

class AI{
    public void run(){
        System.out.println("AI: "+GameConfig.getInstance());
    }
}

public class Main {
    public static void main(String[] args) {
        new Graphics().run();
        new Audio().run();
        new AI().run();

        System.out.println(GameConfig.getInstance()==GameConfig.getInstance());
    }
}
