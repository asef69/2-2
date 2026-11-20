// 2020-21 Q2(c) — Strategy: grading scheme chosen at run time; merit list of the top grade
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

interface GradingStrategy { String grade(int marks); String topGrade(); }
class BuetGrading implements GradingStrategy {
    public String grade(int m) {
        if (m >= 80) return "A+"; if (m >= 75) return "A"; if (m >= 70) return "A-";
        if (m >= 65) return "B+"; if (m >= 60) return "B"; if (m >= 55) return "B-";
        if (m >= 50) return "C+"; if (m >= 45) return "C"; if (m >= 40) return "D"; return "F";
    }
    public String topGrade() { return "A+"; }
}
class PassFailGrading implements GradingStrategy {
    public String grade(int m) { return m >= 50 ? "P" : "F"; }
    public String topGrade() { return "P"; }
}
class ResultProcessor {                                // context
    private GradingStrategy strategy;
    ResultProcessor(GradingStrategy s) { strategy = s; }
    void setStrategy(GradingStrategy s) { strategy = s; }
    Map<String, String> grades(Map<String, Integer> marks) {
        Map<String, String> g = new LinkedHashMap<>();
        for (Map.Entry<String, Integer> e : marks.entrySet()) g.put(e.getKey(), strategy.grade(e.getValue()));
        return g;
    }
    List<String> meritList(Map<String, Integer> marks) {   // students with the highest grade, by marks
        List<String> ids = new ArrayList<>();
        for (Map.Entry<String, Integer> e : marks.entrySet())
            if (strategy.grade(e.getValue()).equals(strategy.topGrade())) ids.add(e.getKey());
        ids.sort((a, b) -> marks.get(b) - marks.get(a));
        return ids;
    }
}
public class MeritListDemo {
    public static void main(String[] args) {
        Map<String, Integer> marks = new LinkedHashMap<>();
        marks.put("2205001", 86); marks.put("2205002", 74); marks.put("2205003", 91); marks.put("2205004", 38);
        ResultProcessor rp = new ResultProcessor(new BuetGrading());
        System.out.println(rp.grades(marks));
        System.out.println("Merit list: " + rp.meritList(marks));
    }
}
