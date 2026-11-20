// 2014-15 Q2(c) / 2013-14 Q3(c) — automated tester (driver) for a float sort: order + same multiset of data
import java.util.Arrays;
import java.util.Random;

public class SortTester {
    static void sortDescending(float[] a) {              // module under test
        Arrays.sort(a);
        for (int i = 0, j = a.length - 1; i < j; i++, j--) { float t = a[i]; a[i] = a[j]; a[j] = t; }
    }
    static boolean isDescending(float[] a) {
        for (int i = 1; i < a.length; i++) if (a[i - 1] < a[i]) return false;
        return true;
    }
    static boolean sameData(float[] in, float[] out) {   // 'originality': permutation of the input
        float[] x = in.clone(), y = out.clone();
        Arrays.sort(x); Arrays.sort(y);
        return Arrays.equals(x, y);
    }
    public static void main(String[] args) {
        Random r = new Random(42);
        int[] sizes = {0, 1, 2, 10, 1000};                // driver generates different sizes
        boolean all = true;
        for (int n : sizes) {
            float[] in = new float[n];
            for (int i = 0; i < n; i++) in[i] = r.nextInt(50) - 25 + r.nextFloat();   // duplicates and negatives
            float[] out = in.clone();
            sortDescending(out);
            boolean ok = isDescending(out) && sameData(in, out);
            all &= ok;
            System.out.println("n=" + n + (ok ? " PASS" : " FAIL"));
        }
        System.out.println(all ? "ALL PASS" : "SOME FAILED");
    }
}
