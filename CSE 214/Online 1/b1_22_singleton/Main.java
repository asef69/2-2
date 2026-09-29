package b1_22_singleton;

class Logger {
    private static Logger instance;

    private Logger() {
    }

    public static Logger getInstance() {
        if (instance == null) {
            instance = new Logger();
        }
        return instance;
    }
}

class Withdraw {
    public void withdrawing() {
        System.out.println("Withdrawing with: " + Logger.getInstance());
    }
}

class Transfer {
    public void transfering() {
        System.out.println("Transfering with: " + Logger.getInstance());
    }
}

class Deposit {
    public void cashing() {
        System.out.println("Deposit from: " + Logger.getInstance());
    }
}

public class Main {
    public static void main(String[] args) {
        new Withdraw().withdrawing();
        new Transfer().transfering();
        new Deposit().cashing();

        System.out.println(Logger.getInstance() == Logger.getInstance());
    }
}