package a2_22;

class HolidayPackage{
    private String flight;
    private String hotel;
    private String dailyActivities;
    public void setFlight(String flight) {
        this.flight = flight;
    }
    public void setHotel(String hotel) {
        this.hotel = hotel;
    }
    public void setDailyActivities(String dailyActivities) {
        this.dailyActivities = dailyActivities;
    }
    @Override
    public String toString() {
        return "HolidayPackage [flight=" + flight + ", hotel=" + hotel + ", dailyActivities=" + dailyActivities + "]";
    }
}

interface Builder{
    void setFlight();
    void setHotel();
    void setDailyActivities();

    HolidayPackage getHolidayPackage();
}

class Relaxation implements Builder{

    private HolidayPackage packagers =new HolidayPackage();

    @Override
    public HolidayPackage getHolidayPackage() {
        return packagers;
    }

    @Override
    public void setDailyActivities() {
        packagers.setDailyActivities("Spa Treatment");
    }

    @Override
    public void setFlight() {
        packagers.setFlight("Business Class Flight");
    }

    @Override
    public void setHotel() {
        packagers.setHotel("5 star resort");
    }
}

class Adventure implements Builder{

    private HolidayPackage packagers =new HolidayPackage();

    @Override
    public HolidayPackage getHolidayPackage() {
        return packagers;
    }

    @Override
    public void setDailyActivities() {
        packagers.setDailyActivities("Hiking Tour");
    }

    @Override
    public void setFlight() {
        packagers.setFlight("Economy Class");
    }

    @Override
    public void setHotel() {
        packagers.setHotel("Mountain Cabin");
    }
}

class Director{
    public HolidayPackage construct(Builder builder){
        builder.setFlight();
        builder.setHotel();
        builder.setDailyActivities();
        return builder.getHolidayPackage();
    }
}

public class Main {
    public static void main(String[] args) {
        Director director=new Director();

        HolidayPackage adventure=director.construct(new Adventure());
        HolidayPackage relax=director.construct(new Relaxation());

        System.out.println(adventure);
        System.out.println(relax);
    }
}
