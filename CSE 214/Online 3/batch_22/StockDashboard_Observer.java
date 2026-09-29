package batch_22;

import java.util.ArrayList;
import java.util.List;

interface Widget {
    void update(String stockSymbol, double price);
}

class TickerTape implements Widget {

    @Override
    public void update(String stockSymbol, double price) {
        // TODO Auto-generated method stub
        System.out.println("Ticker Tape shows:" + stockSymbol + ",with price:" + price);
    }

}

class Graph implements Widget {

    @Override
    public void update(String stockSymbol, double price) {
        // TODO Auto-generated method stub
        System.out.println("Graph shows:" + stockSymbol + ",with price:" + price);
    }

}

class BuySellBot implements Widget {

    @Override
    public void update(String stockSymbol, double price) {
        // TODO Auto-generated method stub
        String suggestion = price > 100 ? "BUY" : "SELL";
        System.out.println("BuySell Bot shows:" + stockSymbol + ",with price:" + price + ",suggestion:" + suggestion);
    }

}

class StockData {
    private List<Widget> widgets = new ArrayList<>();

    public void addWidget(Widget w) {
        widgets.add(w);
    }

    public void removeWidget(Widget w) {
        widgets.remove(w);
    }

    public void priceChanged(String symbol, double price) {
        System.out.println("\nPrice update: " + symbol + " -> " + price);
        for (Widget w : widgets)
            w.update(symbol, price);
    }
}

public class StockDashboard_Observer {
    public static void main(String[] args) {
        StockData feed = new StockData();
        TickerTape ticker = new TickerTape();
        Graph graph = new Graph();
        BuySellBot bot = new BuySellBot();

        feed.addWidget(ticker);
        feed.addWidget(graph);
        feed.addWidget(bot);

        feed.priceChanged("GOOG", 150.5);
        feed.priceChanged("AAPL", 95.0);

        System.out.println("\n-- Removing Graph widget --");
        feed.removeWidget(graph);

        feed.priceChanged("GOOG", 152.0);
    }
}
