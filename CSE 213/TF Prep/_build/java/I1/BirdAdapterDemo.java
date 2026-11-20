// 2018-19 Q4(b) — Adapter: use Bird objects where ToyDuck objects are expected
interface Bird { void fly(); void makeSound(); }
class Sparrow implements Bird {
    public void fly() { System.out.println("Flying"); }
    public void makeSound() { System.out.println("Chirp Chirp"); }
}
interface ToyDuck { void squeak(); }                         // target
class PlasticToyDuck implements ToyDuck {
    public void squeak() { System.out.println("Squeak"); }
}
class BirdAdapter implements ToyDuck {                       // adapter
    private final Bird bird;                                 // adaptee
    BirdAdapter(Bird bird) { this.bird = bird; }
    public void squeak() { bird.makeSound(); }               // translate the call
}
public class BirdAdapterDemo {
    public static void main(String[] args) {
        ToyDuck[] ducks = { new PlasticToyDuck(), new BirdAdapter(new Sparrow()) };
        for (ToyDuck d : ducks) d.squeak();                  // client sees only ToyDuck
    }
}
