package claude_questions;

import java.util.LinkedList;
import java.util.Queue;

interface Tower {
    void requestLanding(Flight f);

    void requestTakeoff(Flight f);

    void notifyDone(Flight f);
}

class ControlTower implements Tower {
    private boolean runwayBusy = false;
    private final Queue<Flight> waiting = new LinkedList<>();

    @Override
    public void notifyDone(Flight f) {
        // TODO Auto-generated method stub
        System.out.println(f.name + " finished using the runway.");
        runwayBusy = false;
        if (!waiting.isEmpty()) {
            Flight next = waiting.poll();
            runwayBusy = true;
            System.out.println(next.name + " now cleared (was waiting).");
        }
    }

    @Override
    public void requestLanding(Flight f) {
        // TODO Auto-generated method stub
        handleRequest(f, "Land");
    }

    @Override
    public void requestTakeoff(Flight f) {
        // TODO Auto-generated method stub
        handleRequest(f, "take off");
    }

    private void handleRequest(Flight f, String action) {
        if (!runwayBusy) {
            runwayBusy = true;
            System.out.println(f.name + " cleared to " + action);
        } else {
            System.out.println(f.name + " must wait");
            waiting.add(f);
        }
    }
}

class Flight {
    final String name;
    final Tower tower;

    public Flight(String name, Tower tower) {
        this.name = name;
        this.tower = tower;
    }

    void land() {
        tower.requestLanding(this);
    }

    void takeoff() {
        tower.requestTakeoff(this);
    }

    void finish() {
        tower.notifyDone(this);
    }
}

public class M1 {
    public static void main(String[] args) {
        ControlTower tower = new ControlTower();
        Flight f101 = new Flight("Flight101", tower);
        Flight f202 = new Flight("Flight202", tower);
        Flight f303 = new Flight("Flight303", tower);
        f101.land();
        f202.takeoff(); // must hold
        f303.land(); // must hold
        f101.finish(); // frees runway -> f202 cleared
        f202.finish(); // frees runway -> f303 cleared
        f303.finish();
    }
}
