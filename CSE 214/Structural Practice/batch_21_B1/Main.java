package batch_21_B1;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// Step 1: Define the base Purchase component interface
interface Purchase {
    double calculatePrice();
}

class BasePurchase implements Purchase {
    private double amount;

    public BasePurchase(double amount) {
        this.amount = amount;
    }

    @Override
    public double calculatePrice() {
        // TODO Auto-generated method stub
        return amount;
    }
}

abstract class DiscountDecorator implements Purchase {
    protected Purchase product;

    public DiscountDecorator(Purchase product) {
        this.product = product;
    }

    @Override
    public double calculatePrice() {
        // TODO Auto-generated method stub
        return product.calculatePrice();
    }

}

class LoyaltyDiscount extends DiscountDecorator {

    public LoyaltyDiscount(Purchase product) {
        super(product);
    }

    @Override
    public double calculatePrice() {
        // TODO Auto-generated method stub
        return product.calculatePrice() * 0.9;
    }

}

class SeasonalDiscount extends DiscountDecorator {
    public SeasonalDiscount(Purchase product) {
        super(product);

    }

    @Override
    public double calculatePrice() {
        // TODO Auto-generated method stub
        return product.calculatePrice() - 100.0;
    }
}

class HighValueDiscount extends DiscountDecorator {

    public HighValueDiscount(Purchase product) {
        super(product);
    }

    @Override
    public double calculatePrice() {
        // TODO Auto-generated method stub
        return super.calculatePrice() * 0.98;
    }

}

public class Main {
    public static void main(String[] args) {
        double basePrice = 12000; // Initial price of the product
        boolean isPremiumMember = true;
        boolean isPromotionalSeason = true;

        // Create a base purchase
        Purchase purchase = new BasePurchase(basePrice);

        // Apply discounts conditionally
        Purchase discountedPurchase = purchase;

        if (isPremiumMember) {
            discountedPurchase = new LoyaltyDiscount(discountedPurchase);
        }
        if (isPromotionalSeason) {
            discountedPurchase = new SeasonalDiscount(discountedPurchase);
        }
        if (basePrice > 10000) {
            discountedPurchase = new HighValueDiscount(discountedPurchase);
        }

        // Calculate final price after all applicable discounts
        double finalPrice = discountedPurchase.calculatePrice();
        System.out.println("Final price after all discounts: " + finalPrice);
    }
}
