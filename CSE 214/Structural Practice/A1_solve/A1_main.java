public class A1_main {
    public static void main(String[] args) {
 

        Gift vase = new GiftItem("Decorative Vase", 40.0);
        vase = new WrappingDecorator(vase);
        DeliveryRegion local = new LocalRegion(new StandardMode());
        Order order1 = new Order(vase, local, 10);
        System.out.println("Case 1:");
        order1.printSummary();
 

        Gift souvenir = new GiftItem("Wooden Souvenir", 60.0);
        souvenir = new WrappingDecorator(souvenir);
        DeliveryRegion nationalExpress = new NationalRegion(new ExpressMode());
        Order order2 = new Order(souvenir, nationalExpress, 50);
        System.out.println("Case 2:");
        order2.printSummary(); 
 

        Gift showpiece = new GiftItem("Crystal Showpiece", 150.0);
        DeliveryRegion intlPriority = new InternationalRegion(new PriorityMode());
        Order order3 = new Order(showpiece, intlPriority, 0); 
        System.out.println("Case 3:");
        order3.printSummary(); 
    }
}
