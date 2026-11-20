// 2016-17 Q5(c) — choose a parser from the file extension (factory with a registry)
import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;

interface Parser { void parse(String fileName); }
class CParser    implements Parser { public void parse(String f) { System.out.println("C parser: " + f); } }
class CppParser  implements Parser { public void parse(String f) { System.out.println("C++ parser: " + f); } }
class JavaParser implements Parser { public void parse(String f) { System.out.println("Java parser: " + f); } }
class HtmlParser implements Parser { public void parse(String f) { System.out.println("HTML parser: " + f); } }

class ParserFactory {
    private static final Map<String, Supplier<Parser>> REG = new HashMap<>();
    static {
        REG.put("c", CParser::new);
        REG.put("cpp", CppParser::new);
        REG.put("java", JavaParser::new);
        REG.put("html", HtmlParser::new);
    }
    static void register(String ext, Supplier<Parser> s) { REG.put(ext, s); }  // new language
    static Parser getParser(String fileName) {
        String ext = fileName.substring(fileName.lastIndexOf('.') + 1).toLowerCase();
        Supplier<Parser> s = REG.get(ext);
        if (s == null) throw new IllegalArgumentException("No parser for ." + ext);
        return s.get();
    }
}
public class ParserDemo {
    public static void main(String[] args) {
        for (String f : new String[]{"main.c", "a.cpp", "App.java", "index.html"})
            ParserFactory.getParser(f).parse(f);
    }
}
