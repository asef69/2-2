// 2024-25 Q8(a) — Template Method (fixed parsing pipeline) + Strategy (pluggable analysis)
import java.util.Arrays;
import java.util.List;

interface AnalysisStrategy { String analyze(List<Double> values); }     // strategy
class AverageAnalysis implements AnalysisStrategy {
    public String analyze(List<Double> v) {
        return "average = " + v.stream().mapToDouble(Double::doubleValue).average().orElse(0); }
}
class MaxAnalysis implements AnalysisStrategy {
    public String analyze(List<Double> v) {
        return "max = " + v.stream().mapToDouble(Double::doubleValue).max().orElse(0); }
}
abstract class DataParser {                                             // template
    private final AnalysisStrategy analysis;
    DataParser(AnalysisStrategy a) { analysis = a; }
    public final String process(String raw) {                          // the template method
        String content = openFile(raw);
        List<Double> data = parseData(extractData(content));
        String result = analysis.analyze(data);                        // varying algorithm = strategy
        if (wantsReport()) sendReport(result);                         // hook
        closeFile();
        return result;
    }
    protected String openFile(String raw) { return raw.trim(); }       // common steps
    protected abstract String extractData(String content);             // format-specific steps
    protected abstract List<Double> parseData(String data);
    protected boolean wantsReport() { return true; }                   // hook with default
    protected void sendReport(String r) { System.out.println("Report: " + r); }
    protected void closeFile() { }
}
class CsvParser extends DataParser {
    CsvParser(AnalysisStrategy a) { super(a); }
    protected String extractData(String c) { return c; }
    protected List<Double> parseData(String d) {
        return Arrays.stream(d.split(",")).map(String::trim).map(Double::valueOf).toList(); }
}
class JsonParser extends DataParser {
    JsonParser(AnalysisStrategy a) { super(a); }
    protected String extractData(String c) { return c.substring(c.indexOf('[') + 1, c.indexOf(']')); }
    protected List<Double> parseData(String d) {
        return Arrays.stream(d.split(",")).map(String::trim).map(Double::valueOf).toList(); }
    protected boolean wantsReport() { return false; }
}
public class DataMinerDemo {
    public static void main(String[] args) {
        System.out.println(new CsvParser(new AverageAnalysis()).process("3, 5, 10"));
        System.out.println(new JsonParser(new MaxAnalysis()).process("{\"v\": [4, 9, 2]}"));
    }
}
