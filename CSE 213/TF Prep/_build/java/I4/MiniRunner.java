// Runs @Test methods (with @Before/@After) of the given classes — replaces the JUnit runner for this check
import java.lang.reflect.*;
import org.junit.*;
public class MiniRunner {
    public static void main(String[] args) throws Exception {
        int pass = 0, fail = 0;
        for (String cn : args) {
            Class<?> c = Class.forName(cn);
            for (Method m : c.getDeclaredMethods()) {
                Test t = m.getAnnotation(Test.class);
                if (t == null) continue;
                Object o = c.getDeclaredConstructor().newInstance();
                for (Method b : c.getDeclaredMethods()) if (b.isAnnotationPresent(Before.class)) b.invoke(o);
                boolean ok;
                try { m.invoke(o); ok = t.expected() == Test.None.class; }
                catch (InvocationTargetException e) { ok = t.expected().isInstance(e.getCause()); if (!ok) System.out.println(e.getCause()); }
                for (Method a : c.getDeclaredMethods()) if (a.isAnnotationPresent(After.class)) a.invoke(o);
                System.out.println((ok ? "PASS " : "FAIL ") + cn + "." + m.getName());
                if (ok) pass++; else fail++;
            }
        }
        System.out.println(pass + " passed, " + fail + " failed");
    }
}
