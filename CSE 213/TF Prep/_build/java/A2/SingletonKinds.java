// 2016-17 Q5(a), 2012-13 Q2(a), 2010-11 Q4(a) — eager, lazy, double-checked, holder
class EagerSingleton {
    private static final EagerSingleton INSTANCE = new EagerSingleton();  // made at class load
    private EagerSingleton() { }
    public static EagerSingleton getInstance() { return INSTANCE; }
}
class LazySingleton {
    private static LazySingleton instance;                                // made on first use
    private LazySingleton() { }
    public static synchronized LazySingleton getInstance() {
        if (instance == null) instance = new LazySingleton();
        return instance;
    }
}
class DclSingleton {
    private static volatile DclSingleton instance;
    private DclSingleton() { }
    public static DclSingleton getInstance() {
        if (instance == null) {
            synchronized (DclSingleton.class) {
                if (instance == null) instance = new DclSingleton();
            }
        }
        return instance;
    }
}
class HolderSingleton {                                // 2010-11 Q4(a)(ii): valid, lazy, thread-safe
    private HolderSingleton() { }
    private static class SingletonHolder {
        private static final HolderSingleton instance = new HolderSingleton();
    }
    public static HolderSingleton getInstance() { return SingletonHolder.instance; }
}
public class SingletonKinds {
    public static void main(String[] args) {
        System.out.println(EagerSingleton.getInstance() == EagerSingleton.getInstance());
        System.out.println(LazySingleton.getInstance() == LazySingleton.getInstance());
        System.out.println(DclSingleton.getInstance() == DclSingleton.getInstance());
        System.out.println(HolderSingleton.getInstance() == HolderSingleton.getInstance());
    }
}
