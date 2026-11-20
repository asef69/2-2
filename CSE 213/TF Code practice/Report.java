import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

interface Report {
    String getTitle();

    double getTotal();

    String render();
}

class ExpenditureReport implements Report {
    private final String title;
    private final String analysis;
    private final double total;
    private final List<Report> subReports;

    ExpenditureReport(String title, double total, List<Report> subReports, String analysis) {
        this.title = title;
        this.analysis = analysis;
        this.total = total;
        this.subReports = subReports;
    }

    public String getTitle() {
        return title;
    }

    public double getTotal() {
        return total;
    }

    public String render() {
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("==%s: total $%,.0f%n", title, total));
        for (Report report : subReports) {
            sb.append(String.format("- %-22s $%,.0f%n", report.getTitle(), report.getTotal()));
        }
        if (!analysis.isEmpty()) {
            sb.append(" Analysis: ").append(analysis).append('\n');
        }
        return sb.toString();
    }
}

abstract class ReportSection implements Report {
    protected final Report report;

    ReportSection(Report report) {
        this.report = report;
    }

    public String getTitle() {
        return report.getTitle();
    }

    public double getTotal() {
        return report.getTotal();
    }

    public String render() {
        return report.render() + section();
    }

    protected abstract String section();
}

class TaxSection extends ReportSection {
    private final double rate;

    TaxSection(Report report, double rate) {
        super(report);
        this.rate = rate;
    }

    protected String section() {
        return String.format(" [Tax] deductible $%,.0f, saving @ %.0f%% = $%,.0f%n",
                getTotal(), rate * 100, getTotal() * rate);
    }
}

class InvestmentSummary extends ReportSection {
    InvestmentSummary(Report report) {
        super(report);
    }

    protected String section() {
        return String.format(" [Investment] reinvest 10%% = $%,.0f%n", getTotal() * 0.10);
    }
}

class ComplianceSection extends ReportSection {
    private final String authority;

    ComplianceSection(Report report, String authority) {
        super(report);
        this.authority = authority;
    }

    protected String section() {
        return " [Compliance] report filed with " + authority + "\n";
    }
}

abstract class OrgUnit {
    protected final String name;

    OrgUnit(String name) {
        this.name = name;
    }

    String getName() {
        return name;
    }

    abstract double getExpenditure();

    abstract Report generateReport();
}

class CityOffice extends OrgUnit {
    private final Map<String, Double> expenses = new LinkedHashMap<>();

    CityOffice(String name) {
        super(name);
    }

    void addExpense(String head, double amount) {
        expenses.merge(head, amount, Double::sum);
    }

    double getExpenditure() {
        return expenses.values().stream().mapToDouble(Double::doubleValue).sum();
    }

    Report generateReport() {
        List<Report> lines = new ArrayList<>();
        expenses.forEach((head, amount) ->
                lines.add(new ExpenditureReport(head, amount, Collections.emptyList(), "")));
        return new ExpenditureReport("City " + name, getExpenditure(), lines, "");
    }
}

abstract class CompositeUnit extends OrgUnit {
    private final double ownExpense;
    protected final List<OrgUnit> children = new ArrayList<>();

    CompositeUnit(String name, double ownExpense) {
        super(name);
        this.ownExpense = ownExpense;
    }

    void add(OrgUnit unit) {
        children.add(unit);
    }

    void remove(OrgUnit unit) {
        children.remove(unit);
    }

    double getExpenditure() {
        double total = ownExpense;
        for (OrgUnit child : children) {
            total += child.getExpenditure();
        }
        return total;
    }

    final Report generateReport() {
        List<Report> subReports = new ArrayList<>();
        for (OrgUnit child : children) {
            subReports.add(child.generateReport());
        }
        String analysis = analyse(subReports);
        return new ExpenditureReport(level() + " " + name, getExpenditure(), subReports, analysis);
    }

    protected double own() {
        return ownExpense;
    }

    protected abstract String level();

    protected abstract String analyse(List<Report> subReports);
}

class StateOffice extends CompositeUnit {
    StateOffice(String name, double ownExpense) {
        super(name, ownExpense);
    }

    protected String level() {
        return "State";
    }

    protected String analyse(List<Report> subReports) {
        if (subReports.isEmpty()) {
            return "no cities";
        }
        Report max = Collections.max(subReports, Comparator.comparingDouble(Report::getTotal));
        double average = subReports.stream().mapToDouble(Report::getTotal).average().orElse(0);
        return String.format("highest-spending city = %s, average per city = $%,.0f",
                max.getTitle(), average);
    }
}

class CountryOffice extends CompositeUnit {
    CountryOffice(String name, double ownExpense) {
        super(name, ownExpense);
    }

    protected String level() {
        return "Country";
    }

    protected String analyse(List<Report> subReports) {
        if (subReports.isEmpty()) {
            return "no states";
        }
        StringBuilder sb = new StringBuilder("state shares: ");
        for (Report report : subReports) {
            sb.append(String.format("%s %.1f%% ", report.getTitle(),
                    100 * report.getTotal() / getExpenditure()));
        }
        return sb.toString().trim();
    }
}

class GlobalHQ extends CompositeUnit {
    GlobalHQ(String name, double ownExpense) {
        super(name, ownExpense);
    }

    protected String level() {
        return "Global";
    }

    protected String analyse(List<Report> subReports) {
        if (subReports.isEmpty()) {
            return "no markets";
        }
        Report max = Collections.max(subReports, Comparator.comparingDouble(Report::getTotal));
        return String.format("largest market = %s; HQ overhead = %.1f%% of world spend",
                max.getTitle(), 100 * own() / getExpenditure());
    }
}

class FinCorpReporting {
    static CityOffice city(String name, double rent, double salary) {
        CityOffice city = new CityOffice(name);
        city.addExpense("Rent", rent);
        city.addExpense("Salary", salary);
        return city;
    }

    public static void main(String[] args) {
        CityOffice la = city("Los Angeles", 30000, 90000);
        CityOffice sf = city("San Francisco", 40000, 70000);
        CityOffice nyc = city("New York", 50000, 120000);
        CityOffice mun = city("Munich", 25000, 60000);

        StateOffice ca = new StateOffice("California", 10000);
        ca.add(la);
        ca.add(sf);
        StateOffice ny = new StateOffice("New York", 8000);
        ny.add(nyc);
        StateOffice by = new StateOffice("Bavaria", 5000);
        by.add(mun);

        CountryOffice usa = new CountryOffice("USA", 20000);
        usa.add(ca);
        usa.add(ny);
        CountryOffice ger = new CountryOffice("Germany", 7000);
        ger.add(by);

        GlobalHQ world = new GlobalHQ("FinCorp", 50000);
        world.add(usa);
        world.add(ger);

        Report stateDirector = ca.generateReport();
        Report countryHead = new TaxSection(usa.generateReport(), 0.21);
        Report globalCfo = new ComplianceSection(
                new InvestmentSummary(
                        new TaxSection(world.generateReport(), 0.21)),
                "SEC (US) and BaFin (EU)");

        System.out.println(stateDirector.render());
        System.out.println(countryHead.render());
        System.out.println(globalCfo.render());
    }
}
