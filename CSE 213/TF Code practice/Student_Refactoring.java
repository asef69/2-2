class Address {
    private final String address, postOffice, district;

    public Address(String address, String postOffice, String district) {
        this.address = address;
        this.postOffice = postOffice;
        this.district = district;
    }

    @Override
    public String toString() {
        return "Address [address=" + address + ", postOffice=" + postOffice + ", district=" + district + "]";
    }

}

abstract class Student {
    private final String name, id;
    private final int year;
    private final Address address;
    private final float[] yearWiseGPA;

    public Student(String name, String id, int year, Address address, float[] yearWiseGPA) {
        this.name = name;
        this.id = id;
        this.year = year;
        this.address = address;
        this.yearWiseGPA = yearWiseGPA;
    }

    public String getName() {
        return name;
    }

    public int getYear() {
        return year;
    }

    float getCGPA() {
        float sum = 0;
        for (float gpa : yearWiseGPA) {
            sum += gpa;
        }
        return yearWiseGPA.length == 0 ? 0 : sum / yearWiseGPA.length;
    }

    boolean isRegular() {
        return yearWiseGPA.length == year;
    }

    abstract float calculateFee();

    abstract boolean isScholarShipApplicable();

    protected abstract void printSpecificDetails();

    final void printDetails() {
        System.out.println("Name:" + name);
        System.out.println("StudentID:" + id);
        System.out.println("Address:" + address);
        printSpecificDetails();
    }
}

class UGStudent extends Student {
    private static final float UG_FEE = 50000;

    public UGStudent(String name, String id, int year, Address address, float[] yearWiseGPA) {
        super(name, id, year, address, yearWiseGPA);
    }

    @Override
    float calculateFee() {
        return UG_FEE;
    }

    @Override
    boolean isScholarShipApplicable() {
        return true;
    }

    @Override
    protected void printSpecificDetails() {
        System.out.println("Undergraduate, year " + getYear());
    }

}

class PGStudent extends Student {
    private static final float HIGH_CGPA = 3.5f;
    private static final float REDUCED_FEE = 40000;
    private static final float STANDARD_FEE = 48000;
    private final boolean isFulltime;
    public PGStudent(String name, String id, int year, Address address, float[] yearWiseGPA,boolean isFulltime) {
        super(name, id, year, address, yearWiseGPA);
        this.isFulltime=isFulltime;
    }
    @Override
    float calculateFee() {
        return getCGPA() > HIGH_CGPA ? REDUCED_FEE : STANDARD_FEE;
    }

    @Override
    boolean isScholarShipApplicable() {
        return false;
    }

    @Override
    protected void printSpecificDetails() {
        System.out.println("Postgraduate, " + (isFulltime ? "full-time" : "part-time"));
    }
}

class Scholarship {
    private static final int MIN_YEAR = 2;
    private final String name;
    private final int amount;
    private final float cgpaThreshold;

    Scholarship(String name, int amount, float cgpaThreshold) {
        this.name = name;
        this.amount = amount;
        this.cgpaThreshold = cgpaThreshold;
    }

    void checkEligibility(Student student) {
        if (!student.isScholarShipApplicable() || !meetsCriteria(student)) {
            System.out.println(student.getName() + " is not eligible.");
            return;
        }
        System.out.println(student.getName() + " is awarded scholarship: " + amount);
    }

    private boolean meetsCriteria(Student student) {
        return student.isRegular()
                && student.getYear() >= MIN_YEAR
                && student.getCGPA() >= cgpaThreshold;
    }
}