// 2020-21 Q3(b) — Observer: end-of-day temperature summary pushed to dashboards
import java.util.ArrayList;
import java.util.List;

interface DayObserver { void update(double max, double avg); }
class TemperatureLog {                                    // subject
    private final List<Double> readings = new ArrayList<>();
    private final List<DayObserver> observers = new ArrayList<>();
    void attach(DayObserver o) { observers.add(o); }
    void record(double t) { readings.add(t); }
    void endOfDay() {
        double max = readings.stream().mapToDouble(Double::doubleValue).max().orElse(0);
        double avg = readings.stream().mapToDouble(Double::doubleValue).average().orElse(0);
        for (DayObserver o : observers) o.update(max, avg);
        readings.clear();
    }
}
class MaxTempWidget implements DayObserver {
    public void update(double max, double avg) { System.out.println("Max today: " + max); }
}
class AvgTempWidget implements DayObserver {
    public void update(double max, double avg) { System.out.printf("Average today: %.2f%n", avg); }
}
public class TempDashboard {
    public static void main(String[] args) {
        TemperatureLog log = new TemperatureLog();
        log.attach(new MaxTempWidget()); log.attach(new AvgTempWidget());
        for (double t : new double[]{24.5, 31.0, 29.5, 27.0}) log.record(t);
        log.endOfDay();
    }
}
