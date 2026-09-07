public class SolutionTest {
    public static void main(String[] args) {
        int[][] rows=new int[500000][]; java.util.Arrays.fill(rows, new int[]{Integer.MAX_VALUE, Integer.MAX_VALUE}); long[] got=Solution.summarize(rows); if(got[2]!=10000) throw new AssertionError("expected 10000 basis points, got "+got[2]);
    }
}
