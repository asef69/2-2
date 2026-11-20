// IJ slides p203-240 — State pattern: gumball machine
interface State { void insertQuarter(); void ejectQuarter(); void turnCrank(); void dispense(); }

class GumballMachine {                                          // context
    final State soldOut, noQuarter, hasQuarter, sold;
    private State state;
    int count;
    GumballMachine(int n) {
        soldOut = new SoldOutState(this); noQuarter = new NoQuarterState(this);
        hasQuarter = new HasQuarterState(this); sold = new SoldState(this);
        count = n; state = n > 0 ? noQuarter : soldOut;
    }
    void setState(State s) { state = s; }
    void insertQuarter() { state.insertQuarter(); }
    void ejectQuarter() { state.ejectQuarter(); }
    void turnCrank() { state.turnCrank(); state.dispense(); }
    void releaseBall() { System.out.println("A gumball comes rolling out"); if (count > 0) count--; }
}
class NoQuarterState implements State {
    private final GumballMachine m; NoQuarterState(GumballMachine m) { this.m = m; }
    public void insertQuarter() { System.out.println("You inserted a quarter"); m.setState(m.hasQuarter); }
    public void ejectQuarter() { System.out.println("You haven't inserted a quarter"); }
    public void turnCrank() { System.out.println("You turned, but there's no quarter"); }
    public void dispense() { System.out.println("You need to pay first"); }
}
class HasQuarterState implements State {
    private final GumballMachine m; HasQuarterState(GumballMachine m) { this.m = m; }
    public void insertQuarter() { System.out.println("You can't insert another quarter"); }
    public void ejectQuarter() { System.out.println("Quarter returned"); m.setState(m.noQuarter); }
    public void turnCrank() { System.out.println("You turned..."); m.setState(m.sold); }
    public void dispense() { System.out.println("No gumball dispensed"); }
}
class SoldState implements State {
    private final GumballMachine m; SoldState(GumballMachine m) { this.m = m; }
    public void insertQuarter() { System.out.println("Please wait, we're already giving you a gumball"); }
    public void ejectQuarter() { System.out.println("Sorry, you already turned the crank"); }
    public void turnCrank() { System.out.println("Turning twice doesn't get you another gumball!"); }
    public void dispense() {
        m.releaseBall();
        if (m.count > 0) m.setState(m.noQuarter);
        else { System.out.println("Oops, out of gumballs!"); m.setState(m.soldOut); }
    }
}
class SoldOutState implements State {
    private final GumballMachine m; SoldOutState(GumballMachine m) { this.m = m; }
    public void insertQuarter() { System.out.println("Machine is sold out"); }
    public void ejectQuarter() { System.out.println("You haven't inserted a quarter"); }
    public void turnCrank() { System.out.println("No gumballs"); }
    public void dispense() { System.out.println("No gumball dispensed"); }
}
public class GumballDemo {
    public static void main(String[] args) {
        GumballMachine g = new GumballMachine(1);
        g.insertQuarter(); g.turnCrank();
        g.insertQuarter();                              // sold out now
    }
}
