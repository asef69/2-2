// 2022-23 Q5(b) — (i) Decompose Conditional / Extract Variable, (ii) Replace Conditional with Polymorphism,
// (iii) Replace Nested Conditional with Guard Clauses
class Banner {
    String platform = "MacOS", browser = "IE 11"; boolean initialized = true; int resize = 1;
    boolean wasInitialized() { return initialized; }
    void renderBanner() {
        final boolean isMacOs = platform.toUpperCase().indexOf("MAC") > -1;
        final boolean isIE = browser.toUpperCase().indexOf("IE") > -1;
        final boolean wasResized = resize > 0;
        if (isMacOs && isIE && wasInitialized() && wasResized) {
            System.out.println("render banner for Mac + IE");    // do something
        }
    }
}
abstract class Player {                                    // (ii)
    double baseSalary() { return 50000; }
    abstract double getSalary();
}
class FootballPlayer extends Player {
    double getWeeklyIncrement() { return 1000; }
    double getSalary() { return baseSalary() + getWeeklyIncrement() * 4; }
}
class CricketPlayer extends Player {
    double getMonthlyIncrement() { return 3000; }
    double getSalary() { return baseSalary() + getMonthlyIncrement(); }
}
class BadmintonPlayer extends Player {
    double getSalary() { return baseSalary(); }
}
class Payroll {                                            // (iii)
    boolean isDead, isSeparated, isRetired;
    double deadAmount() { return 1; } double separatedAmount() { return 2; }
    double retiredAmount() { return 3; } double normalPayAmount() { return 4; }
    double getPayAmount() {
        if (isDead) return deadAmount();
        if (isSeparated) return separatedAmount();
        if (isRetired) return retiredAmount();
        return normalPayAmount();
    }
}
public class Refactor2223 {
    public static void main(String[] args) {
        new Banner().renderBanner();
        for (Player p : new Player[]{new FootballPlayer(), new CricketPlayer(), new BadmintonPlayer()})
            System.out.println(p.getClass().getSimpleName() + " " + p.getSalary());
        Payroll pr = new Payroll(); pr.isRetired = true;
        System.out.println("pay " + pr.getPayAmount());
    }
}
