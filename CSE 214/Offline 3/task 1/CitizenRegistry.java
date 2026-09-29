import java.util.LinkedHashMap;
import java.util.Map;

public class CitizenRegistry {
    private final Map<String, Citizen> citizens = new LinkedHashMap<>();

    public Citizen register(String name) {
        Citizen citizen = new Citizen(name);
        citizens.put(name, citizen);
        System.out.println("Registered citizen: " + name);
        return citizen;
    }

    public Citizen get(String name) {
        return citizens.get(name);
    }
}
