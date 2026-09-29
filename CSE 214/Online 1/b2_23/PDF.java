package b2_23;
public class PDF implements Report{
    @Override
    public void open(){
        System.out.println("Opening the PDF");
    }
    @Override
    public void generate(){
        System.out.println("Generating the PDF");
    }
}