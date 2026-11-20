// 2022-23 Q2(a) — Mediator: flights talk only to the ATC tower
import java.util.ArrayList;
import java.util.List;

interface ATCMediator {
    void register(Flight f);
    boolean requestLanding(Flight f);
    void landed(Flight f);
}
class ControlTower implements ATCMediator {
    private final List<Flight> flights = new ArrayList<>();
    private boolean runwayFree = true;
    public void register(Flight f) { flights.add(f); }
    public boolean requestLanding(Flight f) {
        if (runwayFree) {
            runwayFree = false;
            for (Flight o : flights) if (o != f) o.receive(f.id + " is landing, hold your position");
            return true;
        }
        return false;
    }
    public void landed(Flight f) {
        runwayFree = true;
        for (Flight o : flights) if (o != f) o.receive("runway free after " + f.id);
    }
}
class Flight {                                         // colleague: knows only the mediator
    final String id; private final ATCMediator atc;
    Flight(String id, ATCMediator atc) { this.id = id; this.atc = atc; atc.register(this); }
    void land() {
        if (atc.requestLanding(this)) { System.out.println(id + ": landing"); atc.landed(this); }
        else System.out.println(id + ": waiting - runway busy");
    }
    void receive(String msg) { System.out.println(id + " <- ATC: " + msg); }
}
public class AtcDemo {
    public static void main(String[] args) {
        ATCMediator tower = new ControlTower();
        Flight bg = new Flight("BG-147", tower), ek = new Flight("EK-585", tower);
        bg.land();
        ek.land();
    }
}
