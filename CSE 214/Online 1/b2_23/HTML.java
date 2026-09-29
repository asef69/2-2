package b2_23;

public class HTML implements Report{
    @Override
    public void open(){
        System.out.println("Opening the HTML");
    }
    @Override
    public void generate(){
        System.out.println("Generating the HTML");
    }
}
