// 2024-25 Q1(a) — Factory Method: client never names a concrete package class
import java.util.List;

interface TourPackage {
    String getName();
    double getPrice();
    String getDescription();
    List<String> getActivities();
}
class AdventurePackage implements TourPackage {
    public String getName() { return "Adventure"; }
    public double getPrice() { return 25000; }
    public String getDescription() { return "For thrill-seekers"; }
    public List<String> getActivities() { return List.of("Mountain hiking", "River rafting"); }
}
class RegularPackage implements TourPackage {
    public String getName() { return "Regular"; }
    public double getPrice() { return 12000; }
    public String getDescription() { return "For leisure travellers"; }
    public List<String> getActivities() { return List.of("City sightseeing", "Museum visits"); }
}

// Creator = the centralised creation component
abstract class PackageCreator {
    protected abstract TourPackage createPackage();          // the factory method
    public TourPackage orderPackage() {                       // common logic works on the interface
        TourPackage p = createPackage();
        System.out.println("Booked " + p.getName() + " (" + p.getPrice() + "): " + p.getActivities());
        return p;
    }
}
class AdventureCreator extends PackageCreator {
    protected TourPackage createPackage() { return new AdventurePackage(); }
}
class RegularCreator extends PackageCreator {
    protected TourPackage createPackage() { return new RegularPackage(); }
}
// New type later: HoneymoonPackage + HoneymoonCreator. No existing class is edited.

public class TravelDemo {
    public static void main(String[] args) {
        PackageCreator creator = new AdventureCreator();   // chosen by configuration / UI
        creator.orderPackage();
        new RegularCreator().orderPackage();
    }
}
