import java.util.List;

public class PuzzleSolver {
    private Puzzle puzzle;

    public PuzzleSolver(Puzzle puzzle) {
	this.puzzle = puzzle;
    }

    private String chooseFromSet(String[] set) {
	int chosen = (int)(Math.random() * set.length);
	return set[chosen];
    }

    private String generate(int length) {
	String chromosome = "";

	String prevMove = "";
	for (int i = 0; i < length; i++) {
	    String move;
	    while ((move = chooseFromSet(puzzle.moves)).equals(prevMove));
	    prevMove = move;
	    String modifier = chooseFromSet(puzzle.modifiers);
	    chromosome += move + modifier + " ";
	}
	
	return chromosome.substring(0, chromosome.length() - 1);
    }

    private String[] select(List<String> population, List<Double> fitnesses) {
	return null;
    }

    private String mutate(String chromosome, double p) {
	return null;
    }

    public void run(Puzzle puzzle, double p_m) {
	
    }

    public void run(Puzzle puzzle, double p_m, int iterations) {
	
    }

    public static void main(String[] args) {
	PuzzleSolver solver = new PuzzleSolver(new ThreeByThreeCube());
	System.out.print("Moves: ");
	for (String s : solver.puzzle.moves) {
	    System.out.print(s + " ");
	}
	System.out.println();
	System.out.print("Modifiers: ");
	for (String s : solver.puzzle.modifiers) {
	    System.out.print(s + " ");
	}
	System.out.println();
	System.out.println(solver.generate(20));
    }
}
