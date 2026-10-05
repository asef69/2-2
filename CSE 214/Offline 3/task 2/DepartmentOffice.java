public class DepartmentOffice extends Office {

    public DepartmentOffice(ResultMediator resultMediator, String name) {
        super(resultMediator, name);
    }

    public void confirmationCompletion(String studentId) {
        System.out.println(name + " Submitting Department confirmation of the student: " + studentId);
        resultMediator.departmentConfirmation(studentId, this);
    }
}
