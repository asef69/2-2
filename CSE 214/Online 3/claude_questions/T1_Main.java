package claude_questions;

import java.util.List;

abstract class ReportExporter {
    final void export(String title, List<String> rows) {
        List<String> data = gatherData(rows);
        applyHeader(title);
        writeBody(data);
        applyFooter();
        finalizeFile();
    }

    private List<String> gatherData(List<String> rows) {
        System.out.println("Gathering " + rows.size() + " data");
        return rows;
    }

    protected abstract void applyHeader(String title);

    protected abstract void writeBody(List<String> data);

    protected void applyFooter() {

    }

    private void finalizeFile() {
        System.out.println("File saved finally");
    }
}

class PdfReportExporter extends ReportExporter {
    protected void applyHeader(String title) {
        System.out.println("Title of PDF:" + title);
    }

    protected void writeBody(List<String> data) {
        for (int i = 0; i < data.size(); i++) {
            System.out.println("Row:" + data.get(i));
            if ((i + 1) % 3 == 0)
                System.out.println("--- page break ---");
        }
    }

    protected void applyFooter() {
        System.out.println("Page footer: generated report");
    }
}

class CSVReportExporter extends ReportExporter {
    protected void applyHeader(String title) {
        System.out.println("Title of CSV:" + title);
    }

    protected void writeBody(List<String> data) {
        for (String row : data)
            System.out.println(row.replace(" ", ","));
    }
}

public class T1_Main {
    public static void main(String[] args) {
        List<String> rows = List.of("1 apple", "2 banana", "3 cherry", "4 date", "5 fig");
        new PdfReportExporter().export("Sales Report", rows);
        new CSVReportExporter().export("Sales Report", rows);
    }
}
