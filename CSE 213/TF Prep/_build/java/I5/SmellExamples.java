// 2019-20 Q6(a), 2022-23 Q5(a) — code smells with short examples and fixes (compile-checked)
import java.util.ArrayList;
import java.util.List;

// DATA CLUMP: the same three fields travel together  ->  Extract Class / Introduce Parameter Object
class MeetingBefore {
    void schedule(int startDay, int startMonth, int startYear, int endDay, int endMonth, int endYear) { }
}
class SimpleDate { final int d, m, y; SimpleDate(int d, int m, int y) { this.d = d; this.m = m; this.y = y; } }
class MeetingAfter { void schedule(SimpleDate start, SimpleDate end) { } }

// REFUSED BEQUEST: subclass inherits methods it does not want  ->  Replace Inheritance with Delegation / push down
class Bird { void fly() { System.out.println("flying"); } void eat() { } }
class PenguinBefore extends Bird {
    void fly() { throw new UnsupportedOperationException("penguins can't fly"); }   // refuses the bequest
}
abstract class Animal { void eat() { } }
class FlyingBird extends Animal { void fly() { } }
class Penguin extends Animal { void swim() { } }                                 // after: no unwanted method

// FEATURE ENVY: a method uses another class's data more than its own -> Move Method
class Customer2 { double totalSpent; int yearsAsMember;
    double loyaltyDiscount() {                                                    // after: moved here
        if (totalSpent > 1000 && yearsAsMember > 2) return totalSpent * 0.15;
        if (totalSpent > 500) return totalSpent * 0.10;
        return 0;
    }
}
class Invoice2 { double discountFor(Customer2 c) { return c.loyaltyDiscount(); } }

// SHOTGUN SURGERY: one rule copied into many classes -> Move Method / Extract Class to one place
class AccountRules { static final double MIN_BALANCE = 500;
    static void checkMinimum(double balanceAfter) {
        if (balanceAfter < MIN_BALANCE) throw new IllegalStateException("Balance would fall below " + MIN_BALANCE);
    }
}
class Debit    { void run(double bal, double amt) { AccountRules.checkMinimum(bal - amt); } }
class Transfer { void run(double bal, double amt) { AccountRules.checkMinimum(bal - amt); } }

// PARALLEL INHERITANCE HIERARCHIES: every new Employee subclass needs a new Printer subclass -> merge via polymorphism
abstract class Employee2 { abstract String report(); }           // after: each employee reports itself
class Engineer2 extends Employee2 { String report() { return "Engineer report"; } }
class Salesman2 extends Employee2 { String report() { return "Salesman report"; } }
// before: Engineer/EngineerPrinter, Salesman/SalesmanPrinter grew in parallel

public class SmellExamples {
    public static void main(String[] args) {
        List<Employee2> staff = new ArrayList<>(List.of(new Engineer2(), new Salesman2()));
        for (Employee2 e : staff) System.out.println(e.report());
        Customer2 c = new Customer2(); c.totalSpent = 1200; c.yearsAsMember = 3;
        System.out.println("discount " + new Invoice2().discountFor(c));
    }
}
