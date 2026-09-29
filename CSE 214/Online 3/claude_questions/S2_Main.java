package claude_questions;

import java.util.ArrayList;
import java.util.List;

interface RideObserver {
    void update(Ride ride, String newState);
}

class Rider implements RideObserver {

    @Override
    public void update(Ride ride, String newState) {
        // TODO Auto-generated method stub
        System.out.println("Rider is now in:" + newState);
    }
}

class Driver implements RideObserver {

    @Override
    public void update(Ride ride, String newState) {
        // TODO Auto-generated method stub
        System.out.println("Driver is now in:" + newState);
    }
}

interface RideState {
    void accept(Ride ride);

    void startTrip(Ride ride);

    void complete(Ride ride);

    void cancel(Ride ride);
}

class RequestedState implements RideState {

    @Override
    public void accept(Ride ride) {
        // TODO Auto-generated method stub
        ride.setState(new AcceptedState(), "Accepted");
    }

    @Override
    public void cancel(Ride ride) {
        // TODO Auto-generated method stub
        ride.setState(new CancelState(), "cancelled");

    }

    @Override
    public void complete(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("ride not started");

    }

    @Override
    public void startTrip(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("ride not accepted");
    }

}

class AcceptedState implements RideState {
    @Override
    public void accept(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("Already accepted");
    }

    @Override
    public void cancel(Ride ride) {
        // TODO Auto-generated method stub
        ride.setState(new CancelState(), "cancelled");

    }

    @Override
    public void complete(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("ride not started");

    }

    @Override
    public void startTrip(Ride ride) {
        // TODO Auto-generated method stub
        ride.setState(new OnTripState(), "on the way");
    }
}

class OnTripState implements RideState {
    @Override
    public void accept(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("Already accepted");
    }

    @Override
    public void cancel(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("Can't cancel");

    }

    @Override
    public void complete(Ride ride) {
        // TODO Auto-generated method stub
        ride.setState(new CompletedState(), "trip completed");

    }

    @Override
    public void startTrip(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("already on the trip");
    }
}

class CompletedState implements RideState {
    @Override
    public void accept(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("Can't start rn");
    }

    @Override
    public void cancel(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("can't be canceled rn");

    }

    @Override
    public void complete(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("ride ended");

    }

    @Override
    public void startTrip(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("ride can't be undone");
    }
}

class CancelState implements RideState {
    @Override
    public void accept(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("Ride is cancelled");
    }

    @Override
    public void cancel(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("Ride is cancelled");

    }

    @Override
    public void complete(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("Ride is cancelled");

    }

    @Override
    public void startTrip(Ride ride) {
        // TODO Auto-generated method stub
        System.out.println("Ride is cancelled");
    }
}

class Ride {
    private RideState state = new RequestedState();
    private final List<RideObserver> observers = new ArrayList<>();

    void addObserver(RideObserver o) {
        observers.add(o);
    }

    void removeObserver(RideObserver o) {
        observers.remove(o);
    }

    void setState(RideState s, String label) {
        this.state = s;
        for (RideObserver o : observers) {
            o.update(this, label);
        }
    }

    void accept() {
        state.accept(this);
    }

    void complete() {
        state.complete(this);
    }

    void startTrip() {
        state.startTrip(this);
    }

    void cancel() {
        state.cancel(this);
    }

}

public class S2_Main {
    public static void main(String[] args) {
        Ride ride1 = new Ride();
        Rider r1 = new Rider();
        Driver d1 = new Driver();
        ride1.addObserver(r1);
        ride1.addObserver(d1);
        ride1.accept();
        ride1.startTrip();
        ride1.complete();
        System.out.println("---");
        Ride ride2 = new Ride();
        ride2.addObserver(new Rider());
        ride2.addObserver(new Driver());
        ride2.accept();
        ride2.cancel();
        ride2.startTrip(); // rejected: cancelled
    }
}
