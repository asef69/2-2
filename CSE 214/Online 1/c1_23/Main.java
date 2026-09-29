package c1_23;

public class Main {
    public static void main(String[] args) {
        new QuestionManagement().run();
        new ResultProcessing().run();
        new StudentLogin().run();

        System.out.println(AuditLogger.getInstance()==AuditLogger.getInstance());
    }
}
