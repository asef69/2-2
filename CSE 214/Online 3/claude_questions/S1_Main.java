package claude_questions;

interface LockState {
    void enterPin(SmartLock ctx, int pin);

    void lockButton(SmartLock ctx);

    void forceUnlock(SmartLock ctx, String masterKey);
}

class LockedState implements LockState {
    public void enterPin(SmartLock ctx, int pin) {
        if (ctx.correctPin == pin) {
            System.out.println("Pin correct:Unlocking");
            ctx.wrongAttempts = 0;
            ctx.setState(ctx.unlockedState);
        } else {
            ctx.wrongAttempts++;
            System.out.println("Wrong pin:" + ctx.wrongAttempts + "/3");
            if (ctx.wrongAttempts >= 3) {
                System.out.println("Lock jammed");
                ctx.setState(ctx.jammedState);
            }
        }
    }

    public void lockButton(SmartLock ctx) {
        System.out.println("Already locked");
    }

    public void forceUnlock(SmartLock ctx, String key) {
        System.out.println("Not jammed: use PIN");
    }
}

class UnlockedState implements LockState {
    public void enterPin(SmartLock ctx, int pin) {
        System.out.println("Already unlocked");
    }

    public void lockButton(SmartLock ctx) {
        System.out.println("Locking");
        ctx.setState(ctx.lockedState);
    }

    public void forceUnlock(SmartLock ctx, String key) {
        System.out.println("Already unlocked(from force)");
    }
}

class JammedState implements LockState {
    public void enterPin(SmartLock ctx, int pin) {
        System.out.println("Already jammed");
    }

    public void lockButton(SmartLock ctx) {
        System.out.println("Locked jammed");
    }

    public void forceUnlock(SmartLock ctx, String key) {
        if (key.equals("MASTER")) {
            System.out.println("Master key accepted");
            ctx.wrongAttempts = 0;
            ctx.setState(ctx.lockedState);
        } else {
            System.out.println("Wrong master key");
        }
    }
}

class LowBatteryState implements LockState {
    public void enterPin(SmartLock ctx, int pin) {
        System.out.println("Low battery: please recharge.");
    }

    public void lockButton(SmartLock ctx) {
        System.out.println("Low battery: please recharge.");
    }

    public void forceUnlock(SmartLock ctx, String key) {
        if (key.equals("MASTER")) {
            System.out.println("Master key accepted despite low battery.");
            ctx.setState(ctx.lockedState);
        } else {
            System.out.println("Wrong master key.");
        }
    }
}

class SmartLock {

    LockState lockedState = new LockedState();
    LockState unlockedState = new UnlockedState();
    LockState jammedState = new JammedState();
    LockState lowBatteryState = new LowBatteryState();

    LockState current = lockedState;
    int correctPin = 1234;
    int wrongAttempts = 0;
    int battery = 100;

    void setState(LockState s) {
        current = s;
    }

    void enterPin(int pin) {
        current.enterPin(this, pin);
    }

    void lockButton() {
        current.lockButton(this);
    }

    void forceUnlock(String key) {
        current.forceUnlock(this, key);
    }

    void drainBattery(int amount) {
        battery -= amount;
        System.out.println("Battery now at " + battery + "%.");
        if (battery < 15 && current != jammedState) {
            System.out.println("Battery critical! Switching to LowBattery mode.");
            setState(lowBatteryState);
        }
    }
}

class S1_Main {
    public static void main(String[] args) {
        SmartLock lock = new SmartLock();
        lock.enterPin(9999);
        lock.enterPin(9999);
        lock.enterPin(9999);
        lock.forceUnlock("WRONG");
        lock.forceUnlock("MASTER");
        lock.enterPin(1234);
        lock.lockButton();
        lock.drainBattery(90);
        lock.enterPin(1234);
        lock.forceUnlock("MASTER");
    }
}