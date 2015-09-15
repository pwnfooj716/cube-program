// Test for empty modifiers list output
// Get cloning to work properly

import java.util.ArrayList;

public abstract class Puzzle implements Cloneable {
    public String[] moves;
    public String[] modifiers;

    public Puzzle(String moves, String modifiers) {
	this.moves = moves.split(" ");
	String[] mostModifiers = modifiers.split(" ");
	this.modifiers = new String[mostModifiers.length + 1];
	this.modifiers[0] = "";
	for (int i = 0; i < mostModifiers.length; i++) {
	    this.modifiers[i + 1] = mostModifiers[i];
	}
    }

    protected Object clone() throws CloneNotSupportedException {
	Puzzle newPuzzle = (Puzzle)super.clone();
	newPuzzle.moves = newPuzzle.moves.clone();
	newPuzzle.modifiers = newPuzzle.modifiers.clone();
	return newPuzzle;
    }
    
    public abstract void applyMoves(String algorithm);
    
    public abstract double fitness();

    public static void main(String[] args) {
	ThreeByThreeCube puzzle = new ThreeByThreeCube();
	try {
	    ThreeByThreeCube newPuzzle = (ThreeByThreeCube)puzzle.clone();
	    // newPuzzle.applyMoves("R U R' U'");
	    // puzzle.print();
	    // System.out.println();
	    // newPuzzle.print();
	    newPuzzle.moves[0] = "@";
	    for (String s : puzzle.moves) {
		System.out.print(s + " ");
	    }
	    System.out.println();
	    for (String s : newPuzzle.moves) {
		System.out.print(s + " ");
	    }
	    System.out.println();
	}
	catch (CloneNotSupportedException e) {
	    System.err.println("Cannot clone Puzzle");
	}
    }
}
