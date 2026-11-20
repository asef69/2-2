// 2024-25 Q6(a) — one test per logically distinct input class
import static org.junit.Assert.*;
import org.junit.Test;

public class LeapYearTest {
    @Test
    public void divisibleBy4NotBy100_isLeap() {
        assertTrue("2024 is divisible by 4 but not by 100", LeapYear.isLeapYear(2024));
    }
    @Test
    public void notDivisibleBy4_isNotLeap() {
        assertFalse("2023 is not divisible by 4", LeapYear.isLeapYear(2023));
    }
    @Test
    public void divisibleBy100NotBy400_isNotLeap() {
        assertFalse("1900 is a century year not divisible by 400", LeapYear.isLeapYear(1900));
    }
    @Test
    public void divisibleBy400_isLeap() {
        assertTrue("2000 is divisible by 400", LeapYear.isLeapYear(2000));
    }
    @Test
    public void smallestValidYear_isNotLeap() {
        assertFalse("year 1 (boundary)", LeapYear.isLeapYear(1));
    }
    @Test
    public void firstLeapYear_isLeap() {
        assertTrue("year 4", LeapYear.isLeapYear(4));
    }
    @Test(expected = IllegalArgumentException.class)
    public void zero_throws() {
        LeapYear.isLeapYear(0);
    }
    @Test(expected = IllegalArgumentException.class)
    public void negativeYear_throws() {
        LeapYear.isLeapYear(-4);
    }
}
