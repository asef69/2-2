package prev_C1;
public class prev_c1_main{
    public static void main(String[] args) {
        // Plain Standard package, no add-ons
        RamadanPackage plainStandard = new StandardPackage();
        System.out.println(plainStandard.description() + " -> Price: " + plainStandard.price());
 
        // Special package with fruit + gift packaging, sent as a gift
        RamadanPackage giftSpecial = new GiftPackage(
                new FruitPackage(
                        new SpecialPackage()));
        System.out.println(giftSpecial.description() + " -> Price: " + giftSpecial.price());
 
        // Premium package with all three enhancements
        RamadanPackage fullPremium = new GiftPackage(
                new SweetPackage(
                        new FruitPackage(
                                new PremiumPackage())));
        System.out.println(fullPremium.description() + " -> Price: " + fullPremium.price());
    }
}