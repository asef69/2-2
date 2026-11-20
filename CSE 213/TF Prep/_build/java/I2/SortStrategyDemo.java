// 2020-21 Q2(b) — Strategy: selection / insertion / quick sort
import java.util.Arrays;

interface SortStrategy { void sort(int[] a); }
class SelectionSort implements SortStrategy {
    public void sort(int[] a) {
        for (int i = 0; i < a.length - 1; i++) {
            int m = i;
            for (int j = i + 1; j < a.length; j++) if (a[j] < a[m]) m = j;
            int t = a[i]; a[i] = a[m]; a[m] = t;
        }
    }
}
class InsertionSort implements SortStrategy {
    public void sort(int[] a) {
        for (int i = 1; i < a.length; i++) {
            int k = a[i], j = i - 1;
            while (j >= 0 && a[j] > k) { a[j + 1] = a[j]; j--; }
            a[j + 1] = k;
        }
    }
}
class QuickSort implements SortStrategy {
    public void sort(int[] a) { qs(a, 0, a.length - 1); }
    private void qs(int[] a, int lo, int hi) {
        if (lo >= hi) return;
        int p = a[hi], i = lo;
        for (int j = lo; j < hi; j++) if (a[j] < p) { int t = a[i]; a[i] = a[j]; a[j] = t; i++; }
        int t = a[i]; a[i] = a[hi]; a[hi] = t;
        qs(a, lo, i - 1); qs(a, i + 1, hi);
    }
}
class Sorter {                                          // context
    private SortStrategy strategy;
    Sorter(SortStrategy s) { strategy = s; }
    void setStrategy(SortStrategy s) { strategy = s; }
    int[] sort(int[] data) { int[] c = data.clone(); strategy.sort(c); return c; }
}
public class SortStrategyDemo {
    public static void main(String[] args) {
        int[] d = {5, 2, 9, 1, 7, 3};
        Sorter s = new Sorter(new SelectionSort());
        System.out.println("selection " + Arrays.toString(s.sort(d)));
        s.setStrategy(new InsertionSort());
        System.out.println("insertion " + Arrays.toString(s.sort(d)));
        s.setStrategy(new QuickSort());
        System.out.println("quick     " + Arrays.toString(s.sort(d)));
    }
}
