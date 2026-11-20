// 2019-20 Q1(a) — one Singleton generator per identifier kind; serial ids from 1, never duplicated
class IdGenerator {
    private static IdGenerator userIds, districtIds, qualificationIds, txIds;
    private long next = 1;
    private IdGenerator() { }                                  // no outside construction

    public static synchronized IdGenerator forUser() {
        if (userIds == null) userIds = new IdGenerator();
        return userIds;
    }
    public static synchronized IdGenerator forDistrict() {
        if (districtIds == null) districtIds = new IdGenerator();
        return districtIds;
    }
    public static synchronized IdGenerator forQualification() {
        if (qualificationIds == null) qualificationIds = new IdGenerator();
        return qualificationIds;
    }
    public static synchronized IdGenerator forTransaction() {
        if (txIds == null) txIds = new IdGenerator();
        return txIds;
    }
    public synchronized long nextId() { return next++; }      // strictly serial
}
class RegistrationService {                // back end called by the UI
    long registerUser(String name)      { return IdGenerator.forUser().nextId(); }
    long createDistrict(String d)       { return IdGenerator.forDistrict().nextId(); }
    long createQualification(String q)  { return IdGenerator.forQualification().nextId(); }
    long recordTransaction()            { return IdGenerator.forTransaction().nextId(); }
}
public class IdDemo {
    public static void main(String[] args) {
        RegistrationService s = new RegistrationService();
        System.out.println("user " + s.registerUser("A") + ", user " + s.registerUser("B"));
        System.out.println("district " + s.createDistrict("Dhaka") + ", tx " + s.recordTransaction()
                + ", tx " + s.recordTransaction() + ", qualification " + s.createQualification("BSc"));
        System.out.println("same object? " + (IdGenerator.forUser() == IdGenerator.forUser()));
    }
}
