// This class represents a 3 dimensional vector that the normal vector operations can be applied to

public class Vector3 {
    private int x;
    private int y;
    private int z;

    public Vector3() {
	x = 0;
	y = 0;
	z = 0;
    }

    public Vector3(int x, int y, int z) {
	set(x, y, z);
    }

    public void set(int x, int y, int z) {
	this.x = x;
	this.y = y;
	this.z = z;
    }

    public int getX() {
	return x;
    }

    public int getY() {
	return y;
    }

    public int getZ() {
	return z;
    }
    
    public boolean equals(Vector3 other) {
	return ((x == other.x) && (y == other.y) && (z == other.z));
    }

    public int dot(Vector3 other) {
	return x * other.getX() + y * other.getY() + z * other.getZ();
    }

    public Vector3 cross(Vector3 other) {
	return new Vector3(y * other.getZ() - z * other.getY(), z * other.getX() - x * other.getZ(), x * other.getY() - y * other.getX());
    }

    public Vector3 negate() {
	return new Vector3(-x, -y, -z);
    }

    public String toString() {
	return "(" + x + ", " + y + ", " + z + ")";
    }
}
