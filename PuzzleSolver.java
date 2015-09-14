import java.util.List;

public class PuzzleSolver<Puzzle> {
    private Puzzle puzzle;

    public PuzzleSolver(Puzzle puzzle) {
	
    }

    private String generate(int length) {
	String chromosome = "";
	for (int i = 0; i < length; i++) {
	    switch ((int)(Math.random() * 6)) {
	    case 0:
		
	    }
	}
	return null;
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
	
    }
}
