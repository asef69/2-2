public class RunTests {
    public static void main(String[] a) throws Exception {
        MiniRunner.main(new String[]{"LeapYearTest", "GraderTest", "QueueTest"});
        SortTester.main(a);
    }
}
