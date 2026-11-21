abstract class DataParser {
    public final void parse(String source) {          // TEMPLATE METHOD: final, so the order of steps cannot be changed
        open(source);
        String raw = read();
        Object model = parseData(raw);                // varies
        validate(model);                              // hook with a default
        close();
    }
    private void open(String s)  { System.out.println("open " + s); }       // common steps are written once
    private String read()        { return "a,b,c"; }
    private void close()         { System.out.println("close"); }
    protected abstract Object parseData(String raw);                           // primitive operation: subclasses must supply
    protected void validate(Object model) { }                                  // hook: subclasses may override
}
class CsvParser extends DataParser {
    protected Object parseData(String raw) { System.out.println("CSV fields: " + raw.split(",").length); return raw; }
}
public class Main { public static void main(String[] a) { new CsvParser().parse("data.csv"); } }
