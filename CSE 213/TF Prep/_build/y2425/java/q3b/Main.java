import java.util.*;

interface PaymentMethod { void pay(double amount); }
class CardPayment  implements PaymentMethod {
    public void pay(double a) { System.out.println("Processing Card payment " + a); }
}
class BkashPayment implements PaymentMethod {
    public void pay(double a) { System.out.println("Processing bkash payment " + a); }
}

interface PaymentRepository { void save(double amount); }
class MySQLDatabase implements PaymentRepository {
    public void save(double a) { System.out.println("Saving to MySQL: " + a); }
}

class ReceiptGenerator { void generate(double amount) { System.out.println("Generating receipt: " + amount); } }

class PaymentService {
    private final Map<String, PaymentMethod> methods;
    private final PaymentRepository repository;
    private final ReceiptGenerator receipts;

    PaymentService(Map<String, PaymentMethod> methods, PaymentRepository repository, ReceiptGenerator receipts) {
        this.methods = methods; this.repository = repository; this.receipts = receipts;
    }
    void checkout(String method, double amount) {
        PaymentMethod m = methods.get(method);
        if (m == null) throw new IllegalArgumentException("unknown method " + method);
        m.pay(amount);
        repository.save(amount);
        receipts.generate(amount);
    }
}

public class Main {
    public static void main(String[] a) {
        Map<String, PaymentMethod> m = new HashMap<>();
        m.put("CARD", new CardPayment());
        m.put("BKASH", new BkashPayment());
        new PaymentService(m, new MySQLDatabase(), new ReceiptGenerator()).checkout("BKASH", 500);
    }
}
