public class SolutionTest {
    public static void main(String[] args) {
        Solution.NewProfileCommand c=new Solution.NewProfileCommand("A",1,new Solution.AddressCommand("S","C"),java.util.List.of("a@b")); if(Solution.mapProfile(c).getEmails().size()!=1) throw new AssertionError("missing email");
    }
}
