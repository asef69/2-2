public interface ResultMediator {
    void registerStudent(Student student);

    void departmentConfirmation(String studentId, DepartmentOffice deptOffice);

    void officeOrder(String studentId, ControllerOfExam controller);

    void testimonial(String studentId, DSWOffice dswOffice);

    void certificateAndTranscript(String studentId, ControllerOfExam controller);

    ProcessStatus getStatus(String studentId);
}