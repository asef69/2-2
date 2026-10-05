package batch_21_A1;

class LegacyWeatherService {
    public String getWeatherData() {
        return "Legacy weather data";
    }
}

// Client Interface expected by the application
interface WeatherProvider {
    String fetchWeather();
}

class LegacyWeatherServiceAdapter implements WeatherProvider{
    private LegacyWeatherService service;

    public LegacyWeatherServiceAdapter(LegacyWeatherService service) {
        this.service = service;
    }

    @Override
    public String fetchWeather() {
        return service.getWeatherData();
    }
    
}

// Application class that depends on the WeatherProvider interface
class WeatherApp {
    private WeatherProvider weatherProvider;

    public WeatherApp(WeatherProvider weatherProvider) {
        this.weatherProvider = weatherProvider;
    }

    public void displayWeather() {
        System.out.println(weatherProvider.fetchWeather());
    }
}

public class Main {
    public static void main(String[] args) {
        // Legacy service instance
        LegacyWeatherService legacyWeatherService = new LegacyWeatherService();

        WeatherProvider provider=new LegacyWeatherServiceAdapter(legacyWeatherService);

        WeatherApp app = new WeatherApp(provider);// Output: Legacy weather data
        app.displayWeather();
    }
}
