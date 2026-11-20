// 2022-23 Q3(a) — Builder: HTMLPageDirector drives HTMLPageBuilder
import java.util.ArrayList;
import java.util.List;

class HTMLPage {                                       // product
    private String title = "", heading = "";
    private final List<String> lines = new ArrayList<>();
    void setTitle(String t)   { title = t; }
    void setHeading(String h) { heading = h; }
    void addLine(String l)    { lines.add(l); }
    String render() {
        StringBuilder sb = new StringBuilder("<html><head><title>" + title + "</title></head><body>\n");
        sb.append("<h1>").append(heading).append("</h1>\n");
        for (String l : lines) sb.append("<p>").append(l).append("</p>\n");
        return sb.append("</body></html>").toString();
    }
}
interface PageBuilder {                                // builder
    void setPageTitle(String t);
    void setPageHeading(String h);
    void addText(String line);
    HTMLPage getPage();                                // final assembly
}
class HTMLPageBuilder implements PageBuilder {         // concrete builder
    private final HTMLPage page = new HTMLPage();
    public void setPageTitle(String t)   { page.setTitle(t); }
    public void setPageHeading(String h) { page.setHeading(h); }
    public void addText(String line)     { page.addLine(line); }
    public HTMLPage getPage()            { return page; }
}
class HTMLPageDirector {                               // director
    private final PageBuilder builder;
    HTMLPageDirector(PageBuilder b) { builder = b; }
    HTMLPage construct(String title, String heading, String... lines) {
        builder.setPageTitle(title);
        builder.setPageHeading(heading);
        for (String l : lines) builder.addText(l);
        return builder.getPage();
    }
}
public class HtmlDemo {
    public static void main(String[] args) {
        HTMLPageDirector d = new HTMLPageDirector(new HTMLPageBuilder());
        System.out.println(d.construct("CSE 213", "Builder Pattern", "Line one.", "Line two.").render());
    }
}
