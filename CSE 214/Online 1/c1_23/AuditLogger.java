package c1_23;

public class AuditLogger {
    private static AuditLogger audit;
    private AuditLogger(){
        
    }
    public static AuditLogger getInstance(){
        if(audit==null){
            audit=new AuditLogger();
        }
        return audit;
    }

    public void show(){
        System.out.println(AuditLogger.getInstance()+ " is printed");
    }
}
