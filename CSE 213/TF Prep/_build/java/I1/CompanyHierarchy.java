// 2019-20 Q2(a), 2020-21 Q3(a) — Composite: employees and their (direct + indirect) subordinates
import java.util.ArrayList;
import java.util.List;

abstract class Employee {                                     // component
    protected final String name, designation;
    Employee(String n, String d) { name = n; designation = d; }
    void add(Employee e)    { throw new UnsupportedOperationException(); }
    void remove(Employee e) { throw new UnsupportedOperationException(); }
    List<Employee> getSubordinates() { return new ArrayList<>(); }
    abstract void showAll(String indent);                     // shows this employee and everyone below
    public String toString() { return designation + ": " + name; }
}
class Worker extends Employee {                               // leaf
    Worker(String n, String d) { super(n, d); }
    void showAll(String indent) { System.out.println(indent + this); }
}
class Manager extends Employee {                              // composite
    private final List<Employee> subordinates = new ArrayList<>();
    Manager(String n, String d) { super(n, d); }
    void add(Employee e)    { subordinates.add(e); }
    void remove(Employee e) { subordinates.remove(e); }
    List<Employee> getSubordinates() { return subordinates; }
    void showAll(String indent) {
        System.out.println(indent + this);
        for (Employee e : subordinates) e.showAll(indent + "   ");
    }
    int countAll() {                                         // direct + indirect
        int c = 0;
        for (Employee e : subordinates) c += 1 + (e instanceof Manager ? ((Manager) e).countAll() : 0);
        return c;
    }
}
public class CompanyHierarchy {
    public static void main(String[] args) {
        Manager md = new Manager("Karim", "Managing Director");
        Manager tech = new Manager("Rahim", "Technical Manager");
        Manager admin = new Manager("Salma", "Admin Manager");
        Manager fin = new Manager("Nabil", "Finance Manager");
        md.add(tech); md.add(admin); md.add(fin);
        for (int i = 1; i <= 5; i++) tech.add(new Worker("Dev" + i, "Developer"));
        for (int i = 1; i <= 3; i++) admin.add(new Worker("Exec" + i, "Executive"));
        for (int i = 1; i <= 2; i++) fin.add(new Worker("Officer" + i, "Officer"));
        md.showAll("");
        System.out.println("Under MD: " + md.countAll() + ", under Technical Manager: " + tech.countAll());
    }
}
