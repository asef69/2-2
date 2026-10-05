package builder_pattern;

class MealPlan{
    private String MainCourse;
    private String SideDish;
    private String Dessert;
    public void setMainCourse(String mainCourse) {
        MainCourse = mainCourse;
    }
    public void setSideDish(String sideDish) {
        SideDish = sideDish;
    }
    public void setDessert(String dessert) {
        Dessert = dessert;
    }
    @Override
    public String toString() {
        return "MealPlan [MainCourse=" + MainCourse + ", SideDish=" + SideDish + ", Dessert=" + Dessert + "]";
    }
}

interface Builder{
    void setMainCourse();
    void setSideDish();
    void setDessert();

    MealPlan getPlan();
}

class KetoPlan implements Builder{
    private MealPlan plan=new MealPlan();

    @Override
    public MealPlan getPlan() {
        return plan;
    }

    @Override
    public void setDessert() {
        plan.setDessert("Sugar Free Jello");
    }

    @Override
    public void setMainCourse() {
        plan.setMainCourse("Grilled Chicken");
    }

    @Override
    public void setSideDish() {
       plan.setSideDish("Steamed Brocolli");
    }
}
class VeganPlan implements Builder{
    private MealPlan plan=new MealPlan();

    @Override
    public MealPlan getPlan() {
        return plan;
    }

    @Override
    public void setDessert() {
        plan.setDessert("Fruit Bowl");
    }

    @Override
    public void setMainCourse() {
        plan.setMainCourse("Tofu Stir-fry");
    }

    @Override
    public void setSideDish() {
       plan.setSideDish("Quinoa Salad");
    }
}

class Director{
    private Builder builder;

    public Director(Builder builder) {
        this.builder = builder;
    }
    public MealPlan construct(){
        builder.setMainCourse();
        builder.setDessert();
        builder.setSideDish();
        return builder.getPlan();
    }
}

public class main_1 {
    public static void main(String[] args) {
        Builder keto=new KetoPlan();
        Director ketoDirector=new Director(keto);
        MealPlan ketoPlan=ketoDirector.construct();

        System.out.println("Keto Plan:"+ketoPlan);

        Builder vegan=new VeganPlan();
        Director veganDirector=new Director(vegan);
        MealPlan veganPlan=veganDirector.construct();

        System.out.println("Vegan Plan:"+veganPlan);


    }
}
