package a2_23;

class Travel {
    private String transportation;
    private String accomodation;
    private String dailyActivities;

    public void setTransportation(String transportation) {
        this.transportation = transportation;
    }

    public void setAccomodation(String accomodation) {
        this.accomodation = accomodation;
    }

    public void setDailyActivities(String dailyActivities) {
        this.dailyActivities = dailyActivities;
    }

    @Override
    public String toString() {
        return "Travel: " + transportation + "," + accomodation + "," + dailyActivities;
    }
}

interface Builder {
    void setTransportation();

    void setAccomodation();

    void setDailyActivities();

    Travel getTravel();
}

class LuxuryPlan implements Builder {
    private Travel travel = new Travel();

    @Override
    public Travel getTravel() {
        return travel;
    }

    @Override
    public void setAccomodation() {
        travel.setAccomodation("Luxury Hotel");
    }

    @Override
    public void setDailyActivities() {
        travel.setDailyActivities("Private City Tour");
    }

    @Override
    public void setTransportation() {
        travel.setTransportation("Business Class Flight");
    }
}

class BudgetPlan implements Builder {
    private Travel travel = new Travel();

    @Override
    public Travel getTravel() {
        return travel;
    }

    @Override
    public void setAccomodation() {
        travel.setAccomodation("Hostel");
    }

    @Override
    public void setDailyActivities() {
        travel.setDailyActivities("Group Walking");
    }

    @Override
    public void setTransportation() {
        travel.setTransportation("Economy Bus");
    }
}

class travelDirector{
    private Builder builder;

    public travelDirector(Builder builder) {
        this.builder = builder;
    }
    
    public Travel construct(){
        builder.setTransportation();
        builder.setAccomodation();
        builder.setDailyActivities();
        return builder.getTravel();
    }
}

public class Main {
    public static void main(String[] args) {
        Builder builder=new LuxuryPlan();
        travelDirector director=new travelDirector(builder);
        Travel luxury=director.construct();

        System.out.println("Luxury Plan: "+luxury);

        Builder builder2=new BudgetPlan();
        travelDirector director2=new travelDirector(builder2);
        Travel budget=director2.construct();

        System.out.println("Budget Plan: "+budget);
    }
}
