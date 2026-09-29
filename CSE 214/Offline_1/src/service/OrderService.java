package service;

import model.DeliveryType;
import model.MenuItem;
import model.Order;
import model.OrderItem;
import model.PaymentMethod;
import model.Size;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * Coordinates order creation.
 *
 * Several methods below repeat long Order constructor calls with many optional
 * parameters. That is intentional assignment material for refactoring.
 */
public class OrderService {
    private int nextNumber = 1001;

    public OrderItem createOrderItem(MenuItem item, int quantity, Size size, boolean extraCheese, boolean spicy,
            String note) {
        return new OrderItem.Builder(item, quantity).size(size).extraCheese(extraCheese).spicy(spicy).note(note)
                .build();
    }

    public Order createDeliveryOrder(String customerName,
            String phone,
            String address,
            List<OrderItem> items,
            String couponCode,
            boolean rushOrder,
            String specialInstructions) {
        return new Order.Builder(nextOrderId(), customerName, phone, items).deliveryType(DeliveryType.DELIVERY)
                .deliveryAddress(address).couponCode(couponCode).rushOrder(rushOrder)
                .specialInstructions(specialInstructions).build();
    }

    public Order createPickupOrder(String customerName, String phone, List<OrderItem> items) {
        return new Order.Builder(phone, customerName, phone, items).deliveryType(DeliveryType.PICKUP).build();
    }

    public Order createScheduledGiftOrder(String customerName,
            String phone,
            String address,
            List<OrderItem> items,
            LocalDateTime scheduledTime) {
        return new Order.Builder(address, customerName, phone, items).deliveryType(DeliveryType.DELIVERY)
                .deliveryAddress(address).paymentMethod(PaymentMethod.CARD).scheduledTime(scheduledTime)
                .couponCode("WELCOME10").giftWrap(true).cutleryRequired(false).loyaltyPointsToRedeem(25)
                .specialInstructions("Please call before delivery").build();
    }

    public Order createSampleFamilyOrder(MenuCatalog catalog) {
        List<OrderItem> items = new ArrayList<>();
        items.add(new OrderItem.Builder(catalog.findByCode("P01"), 2).size(Size.LARGE).extraCheese(true)
                .note("half spicy").build());
        items.add(new OrderItem.Builder(catalog.findByCode("B02"), 3).size(Size.MEDIUM).extraCheese(true).spicy(true)
                .build());
        items.add(new OrderItem.Builder(catalog.findByCode("D02"), 4).size(Size.MEDIUM).note("less sugar").build());
        items.add(new OrderItem.Builder(catalog.findByCode("S02"), 2).size(Size.LARGE).spicy(true).build());

        return new Order.Builder(nextOrderId(), "Sample Family", "01711111111", items)
                .deliveryType(DeliveryType.DELIVERY)
                .deliveryAddress("House 25, Road 4, Dhanmondi")
                .paymentMethod(PaymentMethod.MOBILE_BANKING)
                .couponCode("FAMILY15")
                .loyaltyPointsToRedeem(50)
                .rushOrder(true)
                .specialInstructions("Deliver Together")
                .build();
    }

    private String nextOrderId() {
        return "FF-" + nextNumber++;
    }
}
