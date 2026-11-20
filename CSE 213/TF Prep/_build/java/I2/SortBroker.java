// 2019-20 Q1(b) — Mediator: central broker forwards sorting requests to servers, queueing them
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;

interface Broker { void submit(Client c, String algorithm, int[] data); void processAll(); }

abstract class SortServer {                                  // colleague
    abstract String algorithm();
    abstract int[] sort(int[] a);
}
class SelectionServer extends SortServer {
    String algorithm() { return "selection"; }
    int[] sort(int[] a) {
        int[] c = a.clone();
        for (int i = 0; i < c.length - 1; i++) { int m = i;
            for (int j = i + 1; j < c.length; j++) if (c[j] < c[m]) m = j;
            int t = c[i]; c[i] = c[m]; c[m] = t; }
        return c;
    }
}
class InsertionServer extends SortServer {
    String algorithm() { return "insertion"; }
    int[] sort(int[] a) {
        int[] c = a.clone();
        for (int i = 1; i < c.length; i++) { int k = c[i], j = i - 1;
            while (j >= 0 && c[j] > k) { c[j + 1] = c[j]; j--; } c[j + 1] = k; }
        return c;
    }
}
class QuickServer extends SortServer {
    String algorithm() { return "quick"; }
    int[] sort(int[] a) { int[] c = a.clone(); Arrays.sort(c); return c; }   // library quicksort for primitives
}
class Client {                                               // colleague
    private final String name; private final Broker broker;
    Client(String name, Broker b) { this.name = name; broker = b; }
    void requestSort(String alg, int[] data) { broker.submit(this, alg, data); }
    void receive(int[] sorted) { System.out.println(name + " got " + Arrays.toString(sorted)); }
}
class CentralBroker implements Broker {                      // concrete mediator
    private record Request(Client c, String alg, int[] data) { }
    private final Map<String, SortServer> servers = new HashMap<>();
    private final Queue<Request> queue = new ArrayDeque<>();
    void addServer(SortServer s) { servers.put(s.algorithm(), s); }
    public void submit(Client c, String alg, int[] data) { queue.add(new Request(c, alg, data)); }
    public void processAll() {                               // FIFO when several requests arrive together
        while (!queue.isEmpty()) {
            Request r = queue.poll();
            r.c().receive(servers.get(r.alg()).sort(r.data()));
        }
    }
}
public class SortBroker {
    public static void main(String[] args) {
        CentralBroker b = new CentralBroker();
        b.addServer(new SelectionServer()); b.addServer(new InsertionServer()); b.addServer(new QuickServer());
        Client c1 = new Client("C1", b), c2 = new Client("C2", b);
        c1.requestSort("quick", new int[]{4, 1, 3});
        c2.requestSort("selection", new int[]{9, 7, 8});
        c1.requestSort("insertion", new int[]{2, 0, 1});
        b.processAll();
    }
}
