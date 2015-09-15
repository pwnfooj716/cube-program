import java.util.ArrayList;

public abstract class Puzzle {
    public final String[] moves;
    public final String[] modifiers;

    public Puzzle(String moves, String modifiers) {
	this.moves = moves.split(" ");
	String[] mostModifiers = modifiers.split(" ");
	this.modifiers = new String[mostModifiers.length + 1];
	this.modifiers[0] = "";
	for (int i = 0; i < mostModifiers.length; i++) {
	    this.modifiers[i + 1] = mostModifiers[i];
	}
    }
    
    public abstract void applyMoves(String algorithm);
    
    public abstract double fitness();
}
