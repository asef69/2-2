package batch_21;

interface TrafficLightState {
    void next(TrafficLight light);

    void display();

    int duration();
}

class Red implements TrafficLightState {

    @Override
    public void display() {
        // TODO Auto-generated method stub
        System.out.println("Red light. STOPPPPPP");
    }

    @Override
    public int duration() {
        // TODO Auto-generated method stub
        return 5;
    }

    @Override
    public void next(TrafficLight light) {
        // TODO Auto-generated method stub
        light.setState(new Yellow());
    }
}

class Yellow implements TrafficLightState {

    @Override
    public void display() {
        // TODO Auto-generated method stub
        System.out.println("Yellow light. GO SLOW");
    }

    @Override
    public int duration() {
        // TODO Auto-generated method stub
        return 2;
    }

    @Override
    public void next(TrafficLight light) {
        // TODO Auto-generated method stub
        light.setState(new Green());
    }
}

class Green implements TrafficLightState {

    @Override
    public void display() {
        // TODO Auto-generated method stub
        System.out.println("Green light. GOOOOOO");
    }

    @Override
    public int duration() {
        // TODO Auto-generated method stub
        return 10;
    }

    @Override
    public void next(TrafficLight light) {
        // TODO Auto-generated method stub
        light.setState(new Red());
    }
}

class TrafficLight {
    private TrafficLightState state = new Red();

    public void setState(TrafficLightState state) {
        this.state = state;
    }

    public void run(int cycles) {
        for (int i = 0; i < cycles; i++) {
            state.display();
            sleepSeconds(state.duration());
            state.next(this);
        }
    }

    private void sleepSeconds(int seconds) {
        try {
            Thread.sleep(seconds * 1000L);
        } catch (Exception e) {
            // TODO: handle exception
            Thread.currentThread().interrupt();
        }
    }
}

public class TrafficLight_State {
    public static void main(String[] args) {
        TrafficLight light = new TrafficLight();
        light.run(10);
    }
}
