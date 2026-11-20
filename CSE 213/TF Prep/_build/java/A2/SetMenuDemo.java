// 2021-22 Q3(a) — Abstract Factory: one factory per set menu; one product type per kitchen
interface RiceItem  { String name(); }   // made in Rice Station
interface MainDish  { String name(); }   // made in Main Mania
interface FriedItem { String name(); }   // made in Fry More

class Dish implements RiceItem, MainDish, FriedItem {
    private final String n;
    Dish(String n) { this.n = n; }
    public String name() { return n; }
}
interface SetMenuFactory {
    RiceItem prepareRice();
    MainDish prepareMain();
    FriedItem prepareFried();
}
class VeggieHarvestFactory implements SetMenuFactory {
    public RiceItem prepareRice()   { return new Dish("Mushroom Rice"); }
    public MainDish prepareMain()   { return new Dish("Paneer Masala"); }
    public FriedItem prepareFried() { return new Dish("Fried Vegetable Pakora"); }
}
class ChickenDelightFactory implements SetMenuFactory {
    public RiceItem prepareRice()   { return new Dish("Chicken Fried Rice"); }
    public MainDish prepareMain()   { return new Dish("Butter Chicken"); }
    public FriedItem prepareFried() { return new Dish("Fried Chicken Wings"); }
}
class BeefFiestaFactory implements SetMenuFactory {
    public RiceItem prepareRice()   { return new Dish("Beef Fried Rice"); }
    public MainDish prepareMain()   { return new Dish("Beef Chili Onion"); }
    public FriedItem prepareFried() { return new Dish("Fried Beef Bacon"); }
}
class SeaShantyFactory implements SetMenuFactory {
    public RiceItem prepareRice()   { return new Dish("Rice with Shrimp"); }
    public MainDish prepareMain()   { return new Dish("Crab Masala"); }
    public FriedItem prepareFried() { return new Dish("Fried Calamari"); }
}
class Restaurant {                 // client: assembles one family; cannot mix menus by mistake
    String deliver(SetMenuFactory f) {
        return f.prepareRice().name() + ", " + f.prepareMain().name() + ", " + f.prepareFried().name();
    }
}
public class SetMenuDemo {
    public static void main(String[] args) {
        Restaurant r = new Restaurant();
        SetMenuFactory[] menus = { new VeggieHarvestFactory(), new ChickenDelightFactory(),
                                   new BeefFiestaFactory(), new SeaShantyFactory() };
        for (SetMenuFactory m : menus)
            System.out.println(m.getClass().getSimpleName().replace("Factory", "") + ": " + r.deliver(m));
    }
}
