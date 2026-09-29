package prev_A2;

public class prev_a2_main {
    public static void main(String[] args) {
        singleitem rice = new singleitem("Rice (5kg)", 350.0, 5.0);
        singleitem oil = new singleitem("Soybean Oil (2L)", 300.0, 2.0);
        singleitem pulse = new singleitem("Pulse (1kg)", 120.0, 1.0);
        singleitem sugar = new singleitem("Sugar (1kg)", 90.0, 1.0);
 
        // Preset package: "Small" made of a few single items
        bazarpackage smallPackage = new bazarpackage("Small Package");
        smallPackage.add(rice);
        smallPackage.add(oil);
 
        // Preset package: "Family" made of more items
        bazarpackage familyPackage = new bazarpackage("Family Package");
        familyPackage.add(rice);
        familyPackage.add(oil);
        familyPackage.add(pulse);
        familyPackage.add(sugar);
 
        // Custom Bazar: mixture of preset package + single items + another custom bazar
        bazarpackage previousCustom = new bazarpackage("My Old Custom Bazar");
        previousCustom.add(pulse);
        previousCustom.add(sugar);
 
        bazarpackage myCustomBazar = new bazarpackage("My Custom Bazar");
        myCustomBazar.add(smallPackage);      // preset package
        myCustomBazar.add(new singleitem("Onion (2kg)", 80.0, 2.0)); // single item
        myCustomBazar.add(previousCustom);    // previously created custom package
 
        // Print full structure and totals
        myCustomBazar.print("");
        System.out.printf("%nGrand Total => Price: %.2f, Weight: %.2fkg%n",
                myCustomBazar.price(), myCustomBazar.weight());
    }
}
