// 2019-20 Q7(a) — fixture + equivalence partitions + boundary values
import static org.junit.Assert.*;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class GraderTest {
    private int[] aMarks, bMarks, cMarks;

    @Before                                    // fixture: fresh test data before every test
    public void setUp() {
        aMarks = new int[]{81, 90, 100};       // just above 80, nominal, upper limit
        bMarks = new int[]{71, 75, 80};        // just above 70, nominal, boundary 80
        cMarks = new int[]{61, 65, 70};        // just above 60, nominal, boundary 70
    }
    @After
    public void tearDown() { aMarks = bMarks = cMarks = null; }

    @Test
    public void partitionA_above80() {
        for (int m : aMarks) assertEquals("mark " + m, 'A', Grader.grade(m));
    }
    @Test
    public void partitionB_71to80() {
        for (int m : bMarks) assertEquals("mark " + m, 'B', Grader.grade(m));
    }
    @Test
    public void partitionC_61to70() {
        for (int m : cMarks) assertEquals("mark " + m, 'C', Grader.grade(m));
    }
    @Test
    public void boundary60_isNotC() {
        assertEquals("mark 60", 'F', Grader.grade(60));
    }
    @Test(expected = IllegalArgumentException.class)
    public void invalid_aboveRange() { Grader.grade(101); }
    @Test(expected = IllegalArgumentException.class)
    public void invalid_negative() { Grader.grade(-1); }
}
