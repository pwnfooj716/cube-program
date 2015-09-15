import java.util.ArrayList;
import java.util.function.Predicate;
import java.util.function.UnaryOperator;
import java.util.function.ToIntFunction;

public class ThreeByThreeCube extends Puzzle {
    public static final Vector3 FACE_U = new Vector3(0, 0, 1);
    public static final Vector3 FACE_D = new Vector3(0, 0, -1);
    public static final Vector3 FACE_L = new Vector3(0, -1, 0);
    public static final Vector3 FACE_R = new Vector3(0, 1, 0);
    public static final Vector3 FACE_F = new Vector3(1, 0, 0);
    public static final Vector3 FACE_B = new Vector3(-1, 0, 0);
    
    private ArrayList<Cubie> cubies = new ArrayList<Cubie>();

    public ThreeByThreeCube() {
	super("U D L R F B", "' 2");
	
	for (int k = -1; k <= 1; k++) {
	    for (int j = -1; j <= 1; j++) {
		for (int i = -1; i <= 1; i++) {
		    if ((i != 0) || (j != 0) || (k != 0)) {
			cubies.add(new Cubie(i, j, k));
		    }
		}
	    }
	}
    }

    public ThreeByThreeCube(String scramble) {
	super("U D L R F B", "' 2");
	
	for (int k = -1; k <= 1; k++) {
	    for (int j = -1; j <= 1; j++) {
		for (int i = -1; i <= 1; i++) {
		    if ((i != 0) || (j != 0) || (k != 0)) {
			cubies.add(new Cubie(i, j, k));
		    }
		}
	    }
	}

	applyMoves(scramble);
    }

    protected Object clone() throws CloneNotSupportedException {
	ThreeByThreeCube newCube = (ThreeByThreeCube)super.clone();
	cubies = new ArrayList<Cubie>(cubies);
	return newCube;
    }

    public void print() {
	Cubie[][][] array = arrangeCubies();

	for (int z = 0; z < 3; z++) {
	    for (int i = 0; i < 3; i++) {
		System.out.print(' ');
	    }
	    for (int y = 0; y < 3; y++) {
		System.out.print(getColor(array[0][y][z], FACE_B));
	    }
	    System.out.println();
	}

	for (int x = 0; x < 3; x++) {
	    for (int z = 0; z < 3; z++) {
		System.out.print(getColor(array[x][0][z], FACE_L));
	    }
	    for (int y = 0; y < 3; y++) {
		System.out.print(getColor(array[x][y][2], FACE_U));
	    }
	    for (int z = 2; z >= 0; z--) {
		System.out.print(getColor(array[x][2][z], FACE_R));
	    }
	    System.out.println();
	}

	for (int z = 2; z >= 0; z--) {
	    for (int i = 0; i < 3; i++) {
		System.out.print(' ');
	    }
	    for (int y = 0; y < 3; y++) {
		System.out.print(getColor(array[2][y][z], FACE_F));
	    }
	    System.out.println();
	}

	for (int x = 2; x >= 0; x--) {
	    for (int i = 0; i < 3; i++) {
		System.out.print(' ');
	    }
	    for (int y = 0; y < 3; y++) {
		System.out.print(getColor(array[x][y][0], FACE_D));
	    }
	    System.out.println();
	}
	System.out.println();
    }

    private Cubie[][][] arrangeCubies() {
	Cubie[][][] array = new Cubie[3][3][3];
	for (Cubie cubie : cubies) {
	    Vector3 loc = cubie.getLocation();
	    array[loc.getX() + 1][loc.getY() + 1][loc.getZ() + 1] = cubie;
	}

	return array;
    }

    private char getColor(Cubie cubie, Vector3 face) {
	Vector3 oriX = cubie.getOrientationX();
	Vector3 oriY = cubie.getOrientationY();
	Vector3 oriZ = oriX.cross(oriY);
	if (face.equals(oriX)) {
	    return 'R';
	}
	else if (face.equals(oriX.negate())) {
	    return 'O';
	}
	else if (face.equals(oriY)) {
	    return 'B';
	}
	else if (face.equals(oriY.negate())) {
	    return 'G';
	}
	else if (face.equals(oriZ)) {
	    return 'W';
	}
	else if (face.equals(oriZ.negate())) {
	    return 'Y';
	}
	else {
	    return 'N';
	}
    }

    public void applyMove(String move) {
	Predicate<Cubie> filter = cubie -> false;
	UnaryOperator<Vector3> transform = v -> v;

	switch (move.charAt(0)) {
	case 'U':
	    filter = cubie -> cubie.getLocation().getZ() == 1;
	    break;
	case 'D':
	    filter = cubie -> cubie.getLocation().getZ() == -1;
	    break;
	case 'L':
	    filter = cubie -> cubie.getLocation().getY() == -1;
	    break;
	case 'M':
	    filter = cubie -> cubie.getLocation().getY() == 0;
	    break;	    
	case 'R':
	    filter = cubie -> cubie.getLocation().getY() == 1;
	    break;
	case 'F':
	    filter = cubie -> cubie.getLocation().getX() == 1;
	    break;
	case 'B':
	    filter = cubie -> cubie.getLocation().getX() == -1;
	    break;
	case 'x':
	case 'y':
	case 'z':
	    filter = cubie -> true;
	    break;
	}

	
	if ((move.length() > 1) && (move.charAt(1) == '2')) {
	    switch (move.charAt(0)) {
	    case 'U':
	    case 'D':
	    case 'y':
		transform = v -> new Vector3(-v.getX(), -v.getY(), v.getZ());
		break;
	    case 'L':
	    case 'M':
	    case 'R':
	    case 'x':
		transform = v -> new Vector3(-v.getX(), v.getY(), -v.getZ());
		break;
	    case 'F':
	    case 'B':
	    case 'z':
		transform = v -> new Vector3(v.getX(), -v.getY(), -v.getZ());
		break;
	    }
	}
	else {
	    int prime = ((move.length() > 1) && (move.charAt(1) == '\'')) ? 1 : -1;
	    switch (move.charAt(0)) {
	    case 'U':
	    case 'y':
		transform = v -> new Vector3(-prime * v.getY(), prime * v.getX(), v.getZ());
		break;
	    case 'D':
		transform = v -> new Vector3(prime * v.getY(), -prime * v.getX(), v.getZ());
		break;
	    case 'L':
	    case 'M':
		transform = v -> new Vector3(-prime * v.getZ(), v.getY(), prime * v.getX());
		break;
	    case 'R':
	    case 'x':
		transform = v -> new Vector3(prime * v.getZ(), v.getY(), -prime * v.getX());
		break;
	    case 'F':
	    case 'z':
		transform = v -> new Vector3(v.getX(), -prime * v.getZ(), prime * v.getY());
		break;
	    case 'B':
		transform = v -> new Vector3(v.getX(), prime * v.getZ(), -prime * v.getY());
		break;
	    }
	}

	for (Cubie cubie : cubies) {
	    if (filter.test(cubie)) {
		cubie.setLocation(transform.apply(cubie.getLocation()));
		cubie.setOrientation(transform.apply(cubie.getOrientationX()), transform.apply(cubie.getOrientationY()));
	    }
	}
    }

    public void applyMoves(String algorithm) {
	String[] moves = algorithm.split(" ");
	for (String move : moves) {
	    applyMove(move);
	}
    }

    public double fitness() {
	return 0;
    }

    public static void main(String[] args) {
	ThreeByThreeCube cube = new ThreeByThreeCube();
	try {
	    ThreeByThreeCube newCube = (ThreeByThreeCube)cube.clone();
	    newCube.applyMoves("R U R' U'");
	    cube.print();
	    System.out.println();
	    newCube.print();
	}
	catch (CloneNotSupportedException e) {
	    System.err.println("Cannot clone ThreeByThreeCube");
	}
    }
}
