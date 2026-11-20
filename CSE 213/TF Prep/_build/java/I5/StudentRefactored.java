// 2024-25 Q4(a) — Student / Scholarship after refactoring
// Smells fixed: (1) type code + switch on type (UG/PG) -> Replace Conditional with Polymorphism;
// (2) data clump street/postOffice/district -> Extract Class Address; (3) feature envy: Scholarship computes CGPA and
// regularity from Student's data -> Move Method into Student; (4) duplicated code: CGPA loop in two places -> Extract Method
// cgpa(); (5) long method / deep nesting in checkEligibility -> guard clauses; also temporary field isFulltime only for PG
// -> moved into PostgraduateStudent; magic numbers -> named constants.
class Address {
    private final String street, postOffice, district;
    Address(String street, String postOffice, String district) {
        this.street = street; this.postOffice = postOffice; this.district = district;
    }
    public String toString() { return street + ", " + postOffice + ", " + district; }
}
abstract class Student {
    final String name, id;
    final int year;
    final Address address;
    private final float[] yearWiseGpa;
    Student(String name, String id, int year, Address address, float[] yearWiseGpa) {
        this.name = name; this.id = id; this.year = year; this.address = address; this.yearWiseGpa = yearWiseGpa;
    }
    float cgpa() {                                        // extracted once
        float sum = 0;
        for (float g : yearWiseGpa) sum += g;
        return yearWiseGpa.length == 0 ? 0 : sum / yearWiseGpa.length;
    }
    boolean isRegular() { return yearWiseGpa.length == year; }    // moved from Scholarship
    abstract float calculateFee();
    void printDetails() {
        System.out.println("Name: " + name);
        System.out.println("Student ID: " + id);
        System.out.println("Address: " + address);
        printSpecificDetails();
    }
    protected abstract void printSpecificDetails();
}
class UndergraduateStudent extends Student {
    private static final float UG_FEE = 50000;
    UndergraduateStudent(String n, String id, int y, Address a, float[] g) { super(n, id, y, a, g); }
    float calculateFee() { return UG_FEE; }
    protected void printSpecificDetails() { System.out.println("Undergraduate, year " + year); }
}
class PostgraduateStudent extends Student {
    private static final float HIGH_CGPA = 3.5f, PG_FEE_HIGH_CGPA = 40000, PG_FEE = 48000;
    private final boolean fulltime;
    PostgraduateStudent(String n, String id, int y, Address a, float[] g, boolean fulltime) {
        super(n, id, y, a, g); this.fulltime = fulltime;
    }
    float calculateFee() { return cgpa() > HIGH_CGPA ? PG_FEE_HIGH_CGPA : PG_FEE; }
    protected void printSpecificDetails() { System.out.println("Postgraduate, " + (fulltime ? "full-time" : "part-time")); }
}
class Scholarship {
    private static final int MIN_YEAR = 2;
    final String name; final int amount; final float cgpaThreshold;
    Scholarship(String name, int amount, float cgpaThreshold) {
        this.name = name; this.amount = amount; this.cgpaThreshold = cgpaThreshold;
    }
    boolean isEligible(Student s) {                       // guard clauses instead of nested ifs
        if (!(s instanceof UndergraduateStudent)) return false;
        if (!s.isRegular()) return false;
        if (s.year < MIN_YEAR) return false;
        return s.cgpa() >= cgpaThreshold;
    }
    void checkEligibility(Student s) {
        System.out.println(s.name + (isEligible(s) ? " is awarded scholarship: " + amount : " is not eligible."));
    }
}
public class StudentRefactored {
    public static void main(String[] args) {
        Address a = new Address("Road 3", "Palashi", "Dhaka");
        Student ug = new UndergraduateStudent("Asef", "2205001", 3, a, new float[]{3.6f, 3.8f, 3.7f});
        Student pg = new PostgraduateStudent("Nadia", "0423001", 1, a, new float[]{3.9f}, true);
        ug.printDetails(); System.out.println("Fee: " + ug.calculateFee());
        pg.printDetails(); System.out.println("Fee: " + pg.calculateFee());
        Scholarship s = new Scholarship("Dean's", 20000, 3.5f);
        s.checkEligibility(ug); s.checkEligibility(pg);
    }
}
