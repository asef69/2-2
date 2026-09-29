public class DSWOffice extends Office {

    public DSWOffice(ResultMediator resultMediator, String name) {
        super(resultMediator, name);
    }

    public void issueTestimonial(String studentId) {
        System.out.println(name + " Trying to issue testimonial of the student: " + studentId);
        resultMediator.testimonial(studentId, this);
    }
}
