public class Grader {
    // A: mark > 80, B: 70 < mark <= 80, C: 60 < mark <= 70, otherwise F; valid marks 0..100
    public static char grade(int mark) {
        if (mark < 0 || mark > 100) throw new IllegalArgumentException("mark out of range");
        if (mark > 80) return 'A';
        if (mark > 70) return 'B';
        if (mark > 60) return 'C';
        return 'F';
    }
}
