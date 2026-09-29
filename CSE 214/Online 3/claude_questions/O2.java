package claude_questions;

import java.util.ArrayList;
import java.util.List;

interface AlertStrategy {
    boolean shouldFire(double lastPrice, double newPrice);

    String describe();
}

class AboveThresoldStrategy implements AlertStrategy {
    private final double thresold;

    public AboveThresoldStrategy(double thresold) {
        this.thresold = thresold;
    }

    @Override
    public boolean shouldFire(double lastPrice, double newPrice) {
        // TODO Auto-generated method stub
        return newPrice > thresold;
    }

    public String describe() {
        return "prive above:" + thresold;
    }

}

class PercentDropStrategy implements AlertStrategy {
    private final double percent;

    public PercentDropStrategy(double percent) {
        this.percent = percent;
    }

    @Override
    public String describe() {
        // TODO Auto-generated method stub
        return "drop of:" + percent + "%";
    }

    @Override
    public boolean shouldFire(double lastPrice, double newPrice) {
        // TODO Auto-generated method stub
        return lastPrice > 0 && (lastPrice - newPrice) / lastPrice * 100 >= percent;
    }

}

interface Subscriber {
    void OnPriceChange(String coin, double lastPrice, double newPrice);
}

class User implements Subscriber {
    private final String name;
    private final AlertStrategy strategy;

    public User(String name, AlertStrategy strategy) {
        this.name = name;
        this.strategy = strategy;
    }

    @Override
    public void OnPriceChange(String coin, double lastPrice, double newPrice) {
        // TODO Auto-generated method stub
        if (strategy.shouldFire(lastPrice, newPrice)) {
            System.out.println(name + " ALERT on " + coin + " (" + strategy.describe() + "): " + newPrice);
        }
    }

}

class CoinFeed {
    private final String coin;
    private double price;
    private final List<Subscriber> subscribers = new ArrayList<>();

    public CoinFeed(String coin, double price) {
        this.coin = coin;
        this.price = price;
    }

    void subscribe(Subscriber s) {
        subscribers.add(s);
    }

    void unsubscribe(Subscriber s) {
        subscribers.remove(s);
    }

    void setPrice(double newPrice) {
        double old = price;
        price = newPrice;
        for (Subscriber s : subscribers) {
            s.OnPriceChange(coin, old, newPrice);
        }
    }
}

public class O2 {
    public static void main(String[] args) {
        CoinFeed btc = new CoinFeed("BTC", 60000);
        User alice = new User("Alice", new AboveThresoldStrategy(65000));
        User bob = new User("Bob", new PercentDropStrategy(5));
        btc.subscribe(alice);
        btc.subscribe(bob);
        btc.setPrice(66000); // Alice fires
        btc.setPrice(62000); // ~6% drop -> Bob fires
        btc.unsubscribe(bob);
        btc.setPrice(58000); // Bob no longer notified
    }
}
