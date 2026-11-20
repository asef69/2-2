// 2018-19 Q3(b) — Builder: a form per user type; Director = the application
import java.util.ArrayList;
import java.util.List;

class Form {                                                    // product
    private final List<String> parts = new ArrayList<>();
    void add(String p) { parts.add(p); }
    public String toString() { return String.join(" | ", parts); }
}
abstract class FormBuilder {                                    // builder
    protected Form form;
    void createNewForm() { form = new Form(); }
    abstract void buildHeader();
    abstract void buildGradeTable();
    abstract void buildButtons();
    Form getForm() { return form; }
}
class AdminFormBuilder extends FormBuilder {                    // concrete builders
    void buildHeader()     { form.add("Header: Admin panel"); }
    void buildGradeTable() { form.add("Grades: all students (editable)"); }
    void buildButtons()    { form.add("Edit[on] Publish[on] Delete[on]"); }
}
class StudentFormBuilder extends FormBuilder {
    void buildHeader()     { form.add("Header: My grades"); }
    void buildGradeTable() { form.add("Grades: own (read-only)"); }
    void buildButtons()    { form.add("Edit[off] Publish[off] Print[on]"); }
}
class GradeApplication {                                        // director
    Form formFor(String role) {
        FormBuilder b = role.equals("admin") ? new AdminFormBuilder() : new StudentFormBuilder();
        b.createNewForm();
        b.buildHeader();
        b.buildGradeTable();
        b.buildButtons();
        return b.getForm();
    }
}
public class FormDemo {
    public static void main(String[] args) {
        GradeApplication app = new GradeApplication();
        System.out.println("admin:   " + app.formFor("admin"));
        System.out.println("student: " + app.formFor("student"));
    }
}
