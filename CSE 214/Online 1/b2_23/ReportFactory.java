package b2_23;

public abstract class ReportFactory {
    public static Report construct(String type){
        if(type.equalsIgnoreCase("PDF")){
            return new PDF();
        }
        else if(type.equalsIgnoreCase("Word")){
            return new Word();
        }
        else if(type.equalsIgnoreCase("HTML")){
            return new HTML();
        }
        else{
            throw new IllegalAccessError("Unknown type: "+type);
        }
    }
}
