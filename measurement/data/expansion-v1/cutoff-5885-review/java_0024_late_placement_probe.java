public class SolutionTest {
    public static void main(String[] args) {
        Solution.Board b=Solution.createBoard(2); if(Solution.attack(b,"A1")!=Solution.Shot.MISS) throw new AssertionError("setup"); Solution.place(b,"A1",1,Solution.Orientation.HORIZONTAL); if(!Solution.renderShots(b)[0].equals("o.")) throw new AssertionError("previous miss became a hit without a hit: "+Solution.renderShots(b)[0]);
    }
}
