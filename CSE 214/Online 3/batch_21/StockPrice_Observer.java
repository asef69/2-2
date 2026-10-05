package batch_21;

import java.util.ArrayList;
import java.util.List;

class User {
    private String name;

    public User(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void update(Stock stock) {
        System.out.println(name + " the price of :" + stock.getName() + " is now:" + stock.getPrice());
    }
}

class Stock {
    private String name;
    private double Price;
    public List<User> users = new ArrayList<>();

    public Stock(String name, double price) {
        this.name = name;
        Price = price;
    }

    public String getName() {
        return name;
    }

    public double getPrice() {
        return Price;
    }

    public void follow(User u) {
        users.add(u);
    }

    public void unfollow(User u) {
        users.remove(u);
    }

    public void setPrice(double price) {
        this.Price = price;
        notifyUsers();
    }

    private void notifyUsers() {
        for (User u : users) {
            u.update(this);
        }
    }
}

public class StockPrice_Observer {
    public static void main(String[] args) {
        // Create stocks
        Stock googleStock = new Stock("Google", 1500);
        Stock appleStock = new Stock("Apple", 1200);

        // Create users
        User user1 = new User("Asef");
        User user2 = new User("Arisha");

        // Code for following stocks
        googleStock.follow(user1);
        googleStock.follow(user2);
        appleStock.follow(user1);

        // Simulate price changes
        System.out.println("Updating Google stock price...");
        googleStock.setPrice(1550);

        System.out.println("\nUpdating Apple stock price...");
        appleStock.setPrice(1250);

        // Code for unfollowing stocks
        googleStock.unfollow(user1); // Alice unfollows Google

        // Simulate price changes again
        System.out.println("Updating Google stock price again...");
        googleStock.setPrice(1600);
    }
}
