// 2022-23 Q1(a) — Object Adapter: clients pass a zip code; the existing service needs a city name
import java.util.HashMap;
import java.util.Map;

class CityWeatherService {                                     // adaptee (existing, unchanged)
    double getTemperature(String city) {
        switch (city) { case "Dhaka": return 31.5; case "Chittagong": return 29.0; default: return Double.NaN; }
    }
}
interface ZipWeatherService { double getTemperature(int zipCode); }   // target expected by the client

class ZipToCityAdapter implements ZipWeatherService {           // adapter
    private final CityWeatherService service;
    private final Map<Integer, String> zipToCity = new HashMap<>();
    ZipToCityAdapter(CityWeatherService s) {
        service = s;
        zipToCity.put(1000, "Dhaka");
        zipToCity.put(4000, "Chittagong");
    }
    public double getTemperature(int zipCode) {
        String city = zipToCity.get(zipCode);
        if (city == null) throw new IllegalArgumentException("Unknown zip " + zipCode);
        return service.getTemperature(city);                    // translate, then delegate
    }
}
public class WeatherAdapter {
    public static void main(String[] args) {
        ZipWeatherService ws = new ZipToCityAdapter(new CityWeatherService());
        System.out.println("1000 -> " + ws.getTemperature(1000) + " C");
        System.out.println("4000 -> " + ws.getTemperature(4000) + " C");
    }
}
