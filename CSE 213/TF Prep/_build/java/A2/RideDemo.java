// 2017-18 Q7(b) — Abstract Factory: each company supplies a matching (car, moto) fare family
interface CarFare  { double cost(int passengers, double d, int t); }
interface MotoFare { double cost(double d); }

class UberCar implements CarFare {
    public double cost(int n, double d, int t) {
        double f = (t == 1) ? 1.8 : (t == 2) ? 1.2 : 0.9;
        return n * d * 18 * f;
    }
}
class PathaoCar implements CarFare {
    public double cost(int n, double d, int t) {
        double f = (t == 1) ? 1.5 : (t == 2) ? 1.15 : 0.9;
        return n * d * 20 * f;
    }
}
class UberMoto   implements MotoFare { public double cost(double d) { return 25 + d * 12; } }
class PathaoMoto implements MotoFare { public double cost(double d) { return 30 + d * 11; } }

interface RideFactory { CarFare carFare(); MotoFare motoFare(); String name(); }
class UberFactory implements RideFactory {
    public CarFare carFare()   { return new UberCar(); }
    public MotoFare motoFare() { return new UberMoto(); }
    public String name()       { return "Uber"; }
}
class PathaoFactory implements RideFactory {
    public CarFare carFare()   { return new PathaoCar(); }
    public MotoFare motoFare() { return new PathaoMoto(); }
    public String name()       { return "Pathao"; }
}
public class RideDemo {
    public static void main(String[] args) {
        double d = 10; int n = 2; int t = 1;   // in the exam read these with a Scanner
        for (RideFactory f : new RideFactory[]{ new UberFactory(), new PathaoFactory() })
            System.out.printf("%s car: %.2f   %s moto: %.2f%n",
                    f.name(), f.carFare().cost(n, d, t), f.name(), f.motoFare().cost(d));
    }
}
