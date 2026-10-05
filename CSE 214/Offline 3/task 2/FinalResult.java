public class FinalResult {
    public static void main(String[] args) {
        ResultMediator coordinator = new Coordinator();
        DepartmentOffice csedept = new DepartmentOffice(coordinator, "CSE Department Office");
        ControllerOfExam controller = new ControllerOfExam(coordinator, "Controller of Examinations");
        DSWOffice dsw = new DSWOffice(coordinator, "Directorate of Students' Welfare");
        Student student = new Student(coordinator, "2305084", "Kazi Asef Kabir");

        coordinator.registerStudent(student);

        System.out.println("\nEarly office-order attempt (should be REJECTED)");
        controller.issueOfficeOrder(student.getStudentId());

        System.out.println("\nDepartmental confirmation");
        csedept.confirmationCompletion(student.getStudentId());

        System.out.println("\nEarly certificate/transcript attempt (should be REJECTED)");
        controller.issueCertificateAndTranscript(student.getStudentId());

        System.out.println("\nIssue final-result office order");
        controller.issueOfficeOrder(student.getStudentId());

        System.out.println("\nIssue testimonial");
        dsw.issueTestimonial(student.getStudentId());

        System.out.println("\nIssue certificate and transcript");
        controller.issueCertificateAndTranscript(student.getStudentId());

        System.out.println("\nNotifications ans status  got by student");
        student.displayNotification();
        student.displayStatus();
    }
}
