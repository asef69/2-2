package b2_23;

public class Word implements Report{
    @Override
    public void open(){
        System.out.println("Opening the Word");
    }
    @Override
    public void generate(){
        System.out.println("Generating the Word");
    }
}
