package b2_23;

public class Main {
    public static void main(String[] args) {
        Report pdf = ReportFactory.construct("PDF");
        pdf.generate();
        pdf.open();

        Report word = ReportFactory.construct("Word");
        word.generate();
        word.open();

        Report html = ReportFactory.construct("HTML");
        html.generate();
        html.open();
    }
}
