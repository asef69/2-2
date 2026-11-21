import java.util.*;

interface FineCalculator { double fine(int daysLate); }
class StudentFine    implements FineCalculator { public double fine(int d) { return d * 5; } }
class FacultyFine    implements FineCalculator { public double fine(int d) { return d * 2; } }
class ResearcherFine implements FineCalculator {
    public double fine(int d) { return d * 3; } }   // new requirement (rate assumed)

interface Notifier { void notify(String message); }
class EmailNotifier implements Notifier { public void notify(String m) { System.out.println("Sending email: " + m); } }
class SmsNotifier   implements Notifier { public void notify(String m) { System.out.println("Sending SMS: " + m); } }

interface FineRepository { void save(int userId, double amount); }
class MySQLFineRepository      implements FineRepository {
    public void save(int u, double a) { System.out.println("Fine saved to MySQL"); }
}
class PostgreSQLFineRepository implements FineRepository {
    public void save(int u, double a) { System.out.println("Fine saved to PostgreSQL"); }
}

class FineService {
    private final Map<String, FineCalculator> calculators;
    private final Notifier notifier;
    private final FineRepository repository;

    FineService(Map<String, FineCalculator> c, Notifier n, FineRepository r) {
        calculators = c; notifier = n; repository = r; }

    double processFine(int userId, String userType, int daysLate) {
        FineCalculator calc = calculators.get(userType);
        double fine = calc == null ? 0 : calc.fine(daysLate);
        repository.save(userId, fine);
        notifier.notify("You owe " + fine + " for " + daysLate + " day(s) late");
        return fine;
    }
}

public class Main {
    public static void main(String[] a) {
        Map<String, FineCalculator> c = new HashMap<>();
        c.put("STUDENT", new StudentFine());
        c.put("FACULTY", new FacultyFine());
        c.put("RESEARCHER", new ResearcherFine());
        FineService s = new FineService(c, new EmailNotifier(), new PostgreSQLFineRepository());
        System.out.println(s.processFine(7, "RESEARCHER", 4));
    }
}
