import java.util.HashMap;
import java.util.Map;

public class Coordinator implements ResultMediator {
    private final Map<String, Student> students = new HashMap<>();
    private final Map<String, ProcessStatus> statusForStudent = new HashMap<>();

    @Override
    public void certificateAndTranscript(String studentId, ControllerOfExam controller) {
        ProcessStatus current = statusForStudent.get(studentId);
        if (current != ProcessStatus.TESTIMONIAL_ISSUED) {
            System.out.println("  [Coordinator] REJECTED: certificate/transcript cannot be issued for " + studentId
                    + " -- testimonial not yet issued (current status: " + current + ").");
            return;
        }
        statusForStudent.put(studentId, ProcessStatus.CERTIFICATE_TRANSCRIPT_ISSUED);
        System.out.println("  [Coordinator] Certificate and transcript issued for " + studentId + ".");
        notifyStudent(studentId, "Certificate and academic transcript have been issued. Process complete.");
    }

    @Override
    public void departmentConfirmation(String studentId, DepartmentOffice deptOffice) {
        statusForStudent.put(studentId, ProcessStatus.DEPARTMENT_CONFIRMED);
        System.out.println("  [Coordinator] Departmental confirmation accepted for " + studentId + ".");
    }

    @Override
    public ProcessStatus getStatus(String studentId) {
        return statusForStudent.get(studentId);
    }

    @Override
    public void officeOrder(String studentId, ControllerOfExam controller) {
        ProcessStatus currentStatus = statusForStudent.get(studentId);
        if (currentStatus != ProcessStatus.DEPARTMENT_CONFIRMED) {
            System.out.println("  [Coordinator] REJECTED: office order cannot be issued for " + studentId
                    + " -- departmental confirmation is missing (current status: " + currentStatus + ").");
            return;
        }
        statusForStudent.put(studentId, ProcessStatus.OFFICE_ORDER_ISSUED);
        System.out.println("  [Coordinator] Office order issued for " + studentId + ".");
        notifyStudent(studentId, "Final-result office order has been issued.");
    }

    @Override
    public void registerStudent(Student student) {
        students.put(student.getStudentId(), student);
        statusForStudent.put(student.getStudentId(), ProcessStatus.NOT_STARTED);
        System.out.println("Registered student: " + student.getName() + " (" + student.getStudentId() + ")");
    }

    @Override
    public void testimonial(String studentId, DSWOffice dswOffice) {
        ProcessStatus current = statusForStudent.get(studentId);
        if (current != ProcessStatus.OFFICE_ORDER_ISSUED) {
            System.out.println("  [Coordinator] REJECTED: testimonial cannot be issued for " + studentId
                    + " -- office order not yet issued (current status: " + current + ").");
            return;
        }
        statusForStudent.put(studentId, ProcessStatus.TESTIMONIAL_ISSUED);
        System.out.println("  [Coordinator] Testimonial issued for " + studentId + ".");
        notifyStudent(studentId, "Testimonial has been issued by DSW.");
    }

    private void notifyStudent(String studentId, String message) {
        Student student = students.get(studentId);
        if (student != null) {
            student.recieveNotification(message);
        }
    }
}