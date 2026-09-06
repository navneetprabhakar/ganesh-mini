class SolutionTest {
    public static void main(String[] args) {
        if (!Character.isWhitespace('\u2003')) throw new AssertionError("probe setup");
        String actual = Solution.collapseDuplicates("a\u2003a");
        if (!"a".equals(actual)) {
            throw new AssertionError("Java whitespace must delimit duplicate tokens; got " + actual);
        }
    }
}
