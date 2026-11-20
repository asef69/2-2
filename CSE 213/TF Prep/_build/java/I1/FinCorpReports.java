// 2024-25 Q2(a) — Composite (city/state/country/global) + Decorator (optional report sections)
import java.util.ArrayList;
import java.util.List;

interface ReportUnit {                                 // the one consistent reporting interface
    String name();
    double expenditure();
    String report();
}
class CityOffice implements ReportUnit {               // leaf
    private final String name; private final double exp;
    CityOffice(String n, double e) { name = n; exp = e; }
    public String name() { return name; }
    public double expenditure() { return exp; }
    public String report() { return name + " expenditure = " + exp; }
}
abstract class Region implements ReportUnit {          // composite
    private final String name; private final double ownExpenditure;
    protected final List<ReportUnit> children = new ArrayList<>();
    Region(String n, double own) { name = n; ownExpenditure = own; }
    Region add(ReportUnit u) { children.add(u); return this; }
    public String name() { return name; }
    public double expenditure() {                      // aggregates subordinate units
        double s = ownExpenditure;
        for (ReportUnit u : children) s += u.expenditure();
        return s;
    }
    protected abstract String analysis();              // varies by level
    public String report() {
        return name + " total = " + expenditure() + " [" + analysis() + "]";
    }
}
class State extends Region {
    State(String n, double own) { super(n, own); }
    protected String analysis() {
        double max = 0; String top = "";
        for (ReportUnit u : children) if (u.expenditure() > max) { max = u.expenditure(); top = u.name(); }
        return "highest-spending city: " + top;
    }
}
class Country extends Region {
    Country(String n, double own) { super(n, own); }
    protected String analysis() { return "average per state: " + expenditure() / Math.max(1, children.size()); }
}
class Global extends Region {
    Global(String n) { super(n, 0); }
    protected String analysis() {
        StringBuilder sb = new StringBuilder("share:");
        for (ReportUnit u : children) sb.append(String.format(" %s %.0f%%", u.name(), 100 * u.expenditure() / expenditure()));
        return sb.toString();
    }
}
abstract class ReportSection implements ReportUnit {   // decorator: same interface, wraps any unit
    protected final ReportUnit inner;
    ReportSection(ReportUnit u) { inner = u; }
    public String name() { return inner.name(); }
    public double expenditure() { return inner.expenditure(); }
}
class TaxSection extends ReportSection {
    TaxSection(ReportUnit u) { super(u); }
    public String report() { return inner.report() + "\n  + Tax details: 15% = " + 0.15 * expenditure(); }
}
class InvestmentSection extends ReportSection {
    InvestmentSection(ReportUnit u) { super(u); }
    public String report() { return inner.report() + "\n  + Investment summary attached"; }
}
class ComplianceSection extends ReportSection {
    ComplianceSection(ReportUnit u) { super(u); }
    public String report() { return inner.report() + "\n  + Government compliance report attached"; }
}
public class FinCorpReports {
    public static void main(String[] args) {
        State ny = (State) new State("New York", 0).add(new CityOffice("NYC", 500)).add(new CityOffice("Buffalo", 200));
        State ca = (State) new State("California", 50).add(new CityOffice("LA", 400));
        Country usa = (Country) new Country("USA", 100).add(ny).add(ca);
        Country de = (Country) new Country("Germany", 0).add(new State("Bavaria", 0).add(new CityOffice("Munich", 300)));
        Global world = (Global) new Global("FinCorp Global").add(usa).add(de);
        System.out.println(ny.report());                                   // State Director
        System.out.println(new TaxSection(usa).report());                  // Country Head + tax
        System.out.println(new ComplianceSection(new InvestmentSection(world)).report());  // CFO + 2 sections
    }
}
