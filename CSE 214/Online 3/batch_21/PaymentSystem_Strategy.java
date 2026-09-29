package batch_21;

interface PaymentStrategy {
    void pay(double amount);
}

class CreditCardPayment implements PaymentStrategy {
    private String cardNumber;

    public CreditCardPayment(String cardNumber) {
        this.cardNumber = cardNumber;
    }

    public void pay(double amount) {
        System.out.println("Paid BDT " + amount + " using Credit Card ending in "
                + cardNumber.substring(cardNumber.length() - 4));
    }
}

class BkashPayment implements PaymentStrategy {
    private String phoneNumber;

    public BkashPayment(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public void pay(double amount) {
        System.out.println("Paid BDT " + amount + " using BKash account " + phoneNumber);
    }
}

class CryptoPayment implements PaymentStrategy {
    private String walletAddress;

    public CryptoPayment(String walletAddress) {
        this.walletAddress = walletAddress;
    }

    public void pay(double amount) {
        System.out.println("Paid BDT " + amount + " worth of Bitcoin from wallet " + walletAddress);
    }
}

class CheckoutContext {
    private PaymentStrategy strategy;

    public void setPaymentMethod(PaymentStrategy strategy) {
        this.strategy = strategy;
    }

    public void checkout(double amount) {
        strategy.pay(amount);
    }
}

public class PaymentSystem_Strategy {
    public static void main(String[] args) {
        CheckoutContext checkout = new CheckoutContext();

        checkout.setPaymentMethod(new CreditCardPayment("4111222233334444"));
        checkout.checkout(1500);

        System.out.println("\n-- Customer switches to BKash --");
        checkout.setPaymentMethod(new BkashPayment("017XXXXXXXX"));
        checkout.checkout(750);

        System.out.println("\n-- Customer switches to Crypto --");
        checkout.setPaymentMethod(new CryptoPayment("1A1zP1eP5QGefi2DMPTfTL5"));
        checkout.checkout(3000);
    }
}
