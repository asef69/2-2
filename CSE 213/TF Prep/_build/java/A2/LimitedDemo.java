// 2011-12 Q1(b) — Base inherited by Derived1 (max 5) and Derived2 (max 10): Singleton generalised
import java.util.HashMap;
import java.util.Map;

abstract class Base {
    private static final Map<Class<?>, Integer> COUNT = new HashMap<>();
    protected Base(int limit) {                       // each subclass passes its own limit
        int c = COUNT.getOrDefault(getClass(), 0);
        if (c >= limit)
            throw new IllegalStateException(getClass().getSimpleName() + ": limit " + limit + " reached");
        COUNT.put(getClass(), c + 1);
    }
}
class Derived1 extends Base {
    private static final int MAX = 5;
    private Derived1() { super(MAX); }                // private: only getInstance() creates
    public static synchronized Derived1 getInstance() {
        try { return new Derived1(); } catch (IllegalStateException e) { return null; }
    }
}
class Derived2 extends Base {
    private static final int MAX = 10;
    private Derived2() { super(MAX); }
    public static synchronized Derived2 getInstance() {
        try { return new Derived2(); } catch (IllegalStateException e) { return null; }
    }
}
public class LimitedDemo {
    public static void main(String[] args) {
        Derived1[] a = new Derived1[7];
        Derived2[] b = new Derived2[12];
        int ok1 = 0, ok2 = 0;
        for (int i = 0; i < a.length; i++) if ((a[i] = Derived1.getInstance()) != null) ok1++;
        for (int i = 0; i < b.length; i++) if ((b[i] = Derived2.getInstance()) != null) ok2++;
        System.out.println("Derived1 created: " + ok1 + " of " + a.length);
        System.out.println("Derived2 created: " + ok2 + " of " + b.length);
    }
}
