public class SolutionTest {
    public static void main(String[] args) {
        Solution.Page p=Solution.listRooms(java.util.List.of(),null,0,1); if(!p.getItems().isEmpty()) throw new AssertionError("expected empty page");
    }
}
