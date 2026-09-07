public class SolutionTest {
    public static void main(String[] args) {
        Solution.Reading reading = new Solution.Reading("id", "label", 80, "120/80", Double.NaN);
        if (!Solution.alerts(reading).contains("temperature")) {
            throw new AssertionError("NaN is outside the normal temperature interval but produces no alert");
        }
    }
}
