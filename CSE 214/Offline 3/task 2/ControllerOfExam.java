public class ControllerOfExam extends Office {

    public ControllerOfExam(ResultMediator resultMediator, String name) {
        super(resultMediator, name);
    }

    public void issueOfficeOrder(String studentId) {
        System.out.println(name + " Trying to issue final result office order for the student: " + studentId);
        resultMediator.officeOrder(studentId, this);
    }
    public void issueCertificateAndTranscript(String studentId) {
        System.out.println("[" + name + "] Attempting to issue certificate & transcript for student " + studentId);
        resultMediator.certificateAndTranscript(studentId, this);
    }
}