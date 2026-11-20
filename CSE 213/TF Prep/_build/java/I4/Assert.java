package org.junit;
public class Assert {
    public static void assertTrue(String m, boolean c) { if (!c) throw new AssertionError(m); }
    public static void assertTrue(boolean c) { assertTrue("", c); }
    public static void assertFalse(String m, boolean c) { if (c) throw new AssertionError(m); }
    public static void assertFalse(boolean c) { assertFalse("", c); }
    public static void assertEquals(String m, Object e, Object a) { if (!java.util.Objects.equals(e, a)) throw new AssertionError(m + " expected " + e + " got " + a); }
    public static void assertEquals(Object e, Object a) { assertEquals("", e, a); }
    public static void assertEquals(String m, double e, double a, double d) { if (Math.abs(e - a) > d) throw new AssertionError(m); }
    public static void fail(String m) { throw new AssertionError(m); }
}
