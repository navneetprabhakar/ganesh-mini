class SolutionTest {
    public static void main(String[] args) {
        Solution.SortTrace result = Solution.traceDescending(new int[]{1, 2});
        if (result.getPasses().size() != 2) {
            throw new AssertionError("must retain swap pass and final no-swap pass; got "
                    + result.getPasses().size());
        }
    }
}
