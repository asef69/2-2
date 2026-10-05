import java.util.ArrayList;
import java.util.List;

public class Student extends Office {
    private final String studentId;
    private final List<String> notifications = new ArrayList<>();

    public Student(ResultMediator resultMediator, String name, String studentId) {
        super(resultMediator, name);
        this.studentId = studentId;
    }

    public String getStudentId() {
        return studentId;
    }

    public void recieveNotification(String message) {
        notifications.add(message);
        System.out.println("Notification to:" + name + "(" + studentId + ")" + ": " + message);
    }

    public void displayStatus() {
        System.out.println(name + " (" + studentId + ") current status: " + resultMediator.getStatus(studentId));
    }

    public void displayNotification() {
        System.out.println("Notification for:" + name + "(" + studentId + ")");
        if (notifications.isEmpty()) {
            System.out.println("No notification yet");
            return;
        }
        int i = 1;
        for (String note : notifications) {
            System.out.println("  " + (i++) + ". " + note);
        }
    }
}