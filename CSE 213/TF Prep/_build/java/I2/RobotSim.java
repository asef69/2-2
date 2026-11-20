// 2018-19 Q2(a) — Strategy: robot behaviours changed at run time
interface Behaviour { int moveCommand(String robot, int position, boolean obstacleClose); }
class AggressiveBehaviour implements Behaviour {
    public int moveCommand(String r, int pos, boolean obs) {
        System.out.println(r + ": aggressive - attack the robot found"); return obs ? 1 : 0; }
}
class DefensiveBehaviour implements Behaviour {
    public int moveCommand(String r, int pos, boolean obs) {
        System.out.println(r + ": defensive - run away in the opposite direction"); return obs ? -1 : 0; }
}
class NormalBehaviour implements Behaviour {
    public int moveCommand(String r, int pos, boolean obs) {
        System.out.println(r + ": normal - ignore other robots"); return 0; }
}
class Robot {                                         // context
    private final String name; private Behaviour behaviour; private int position;
    Robot(String name) { this.name = name; }
    void setBehaviour(Behaviour b) { behaviour = b; }
    void move(boolean obstacleClose) {                // passes sensor info to the strategy
        position += behaviour.moveCommand(name, position, obstacleClose);
    }
}
public class RobotSim {
    public static void main(String[] args) {
        Robot r1 = new Robot("Big Robot"), r2 = new Robot("George v.2.1"), r3 = new Robot("R2");
        r1.setBehaviour(new AggressiveBehaviour());
        r2.setBehaviour(new DefensiveBehaviour());
        r3.setBehaviour(new NormalBehaviour());
        r1.move(true); r2.move(true); r3.move(true);
        System.out.println("-- behaviours changed --");
        r1.setBehaviour(new DefensiveBehaviour());
        r2.setBehaviour(new NormalBehaviour());
        r3.setBehaviour(new AggressiveBehaviour());
        r1.move(true); r2.move(true); r3.move(true);
    }
}
