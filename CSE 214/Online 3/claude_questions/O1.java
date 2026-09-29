package claude_questions;

import java.util.ArrayList;
import java.util.List;

interface Display {
    void update(double temp, double humidity);
}

class CurrentConditionDisplay implements Display {
    public void update(double temp, double humidity) {
        System.out.println("Current:[Temp:" + temp + ",Humidity:" + humidity + "]");
    }
}

class StatisticsDisplay implements Display {
    private double min = Double.MAX_VALUE, max = Double.MIN_VALUE, sum = 0;
    private int count = 0;

    public void update(double temp, double humidity) {
        min = Math.min(min, temp);
        max = Math.max(max, temp);
        sum += temp;
        count++;
        System.out.println("[Stats] min=" + min + " max=" + max + " avg=" + (sum / count));
    }
}

class AlertDisplay implements Display {
    public void update(double temp, double humidity) {
        if (temp > 40)
            System.out.println("[Alert] Heat warning! Temp = " + temp);
    }
}

class WeatherStation {
    private final List<Display> displays = new ArrayList<>();

    void subscribe(Display d) {
        displays.add(d);
    }

    void unsubscribe(Display d) {
        displays.remove(d);
    }

    void setMeasurements(double temp, double humidity) {
        for (Display d : displays) {
            d.update(temp, humidity);
        }
    }
}

public class O1 {

}
