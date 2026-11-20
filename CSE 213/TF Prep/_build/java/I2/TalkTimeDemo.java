// 2020-21 Q2(a) — Strategy: UI depends only on the TalkTimeScheme interface; new schemes are plug-ins
import java.util.ArrayList;
import java.util.List;

interface TalkTimeScheme { String name(); double cost(int minutes); }
class PerMinuteScheme implements TalkTimeScheme {
    public String name() { return "Per minute (Tk 1.0/min)"; }
    public double cost(int m) { return m * 1.0; }
}
class BundleScheme implements TalkTimeScheme {
    public String name() { return "Bundle 300 min for Tk 199, then Tk 0.8/min"; }
    public double cost(int m) { return 199 + Math.max(0, m - 300) * 0.8; }
}
class NightScheme implements TalkTimeScheme {          // added later: no UI change
    public String name() { return "Night owl (Tk 0.5/min)"; }
    public double cost(int m) { return m * 0.5; }
}
class SchemeRegistry {                                 // the only place that knows concrete schemes
    static List<TalkTimeScheme> all() {
        List<TalkTimeScheme> l = new ArrayList<>();
        l.add(new PerMinuteScheme()); l.add(new BundleScheme()); l.add(new NightScheme());
        return l;
    }
}
class SchemePage {                                     // UI team codes against the interface only
    void show(TalkTimeScheme s, int minutes) {
        System.out.printf("%-45s %4d min -> Tk %.2f%n", s.name(), minutes, s.cost(minutes));
    }
}
public class TalkTimeDemo {
    public static void main(String[] args) {
        SchemePage ui = new SchemePage();
        for (TalkTimeScheme s : SchemeRegistry.all()) ui.show(s, 400);
    }
}
