// 2023-24 Q2(a) — Observer: StockGrabber (subject) and StockObserver (observer)
import java.util.ArrayList;
import java.util.List;

interface Subject {
    void register(Observer o);
    void unregister(Observer o);
    void notifyObservers();
}
interface Observer { void update(double ibmPrice, double aaplPrice, double googPrice); }

class StockGrabber implements Subject {
    private final List<Observer> observers = new ArrayList<>();
    private double ibmPrice, aaplPrice, googPrice;
    public void register(Observer o)   { observers.add(o); }
    public void unregister(Observer o) { observers.remove(o); }
    public void notifyObservers() {
        for (Observer o : observers) o.update(ibmPrice, aaplPrice, googPrice);
    }
    public void setIBMPrice(double p)  { ibmPrice = p;  notifyObservers(); }
    public void setAAPLPrice(double p) { aaplPrice = p; notifyObservers(); }
    public void setGOOGPrice(double p) { googPrice = p; notifyObservers(); }
}
class StockObserver implements Observer {
    private static int count = 0;
    private final int id;
    private final Subject stockGrabber;
    StockObserver(Subject s) {
        stockGrabber = s;
        id = ++count;
        s.register(this);                                // subscribes itself
        System.out.println("New observer " + id);
    }
    public void update(double ibm, double aapl, double goog) {
        System.out.printf("Observer %d: IBM %.2f AAPL %.2f GOOG %.2f%n", id, ibm, aapl, goog);
    }
    void stop() { stockGrabber.unregister(this); }
}
public class StockDemo {
    public static void main(String[] args) {
        StockGrabber g = new StockGrabber();
        StockObserver o1 = new StockObserver(g);
        g.setIBMPrice(197.00);
        StockObserver o2 = new StockObserver(g);
        g.setAAPLPrice(677.60);
        o1.stop();
        g.setGOOGPrice(676.40);                          // only observer 2 is told
    }
}
