// 2021-22 Q1(b) — if-else chain on names -> lookup table (HashMap): readable, O(1) amortised
import java.util.HashMap;
import java.util.Map;

class SuperHeroItem {
    final String name; SuperHeroItem(String n) { name = n; }
    public String toString() { return name; }
}
class GetSuperHeroItem {
    private final Map<String, SuperHeroItem> itemByHero = new HashMap<>();
    GetSuperHeroItem() {
        register("IronMan", new SuperHeroItem("suit"));
        register("Thor", new SuperHeroItem("hammer"));
        register("CaptainAmerica", new SuperHeroItem("shield"));
        register("Hawkeye", new SuperHeroItem("arrow"));
    }
    void register(String hero, SuperHeroItem item) { itemByHero.put(hero.toLowerCase(), item); }  // new hero = one call
    SuperHeroItem getItem(String heroName) {
        return heroName == null ? null : itemByHero.get(heroName.toLowerCase());   // case-insensitive, O(1)
    }
}
public class SuperHeroItems {
    public static void main(String[] args) {
        GetSuperHeroItem g = new GetSuperHeroItem();
        System.out.println(g.getItem("thor") + " " + g.getItem("IRONMAN") + " " + g.getItem("Hulk"));
    }
}
