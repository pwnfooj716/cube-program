public class Cubie {
    private Vector3 identity;
    private Vector3 location;
    private Vector3 orientationX;
    private Vector3 orientationY;

    public Cubie(int ideX, int ideY, int ideZ) {
	identity = new Vector3(ideX, ideY, ideZ);
	location = new Vector3(ideX, ideY, ideZ);
	orientationX = new Vector3(1, 0, 0);
	orientationY = new Vector3(0, 1, 0);
    }
    
    public Cubie(int ideX, int ideY, int ideZ, int oriXX, int oriXY, int oriXZ, int oriYX, int oriYY, int oriYZ) {
	identity = new Vector3(ideX, ideY, ideZ);
	location = new Vector3(ideX, ideY, ideZ);
	orientationX = new Vector3(oriXX, oriXY, oriXZ);
	orientationY = new Vector3(oriYX, oriYY, oriYZ);
    }

    public Cubie(int ideX, int ideY, int ideZ, int locX, int locY, int locZ, int oriXX, int oriXY, int oriXZ, int oriYX, int oriYY, int oriYZ) {
	identity = new Vector3(ideX, ideY, ideZ);
	location = new Vector3(locX, locY, locZ);
	orientationX = new Vector3(oriXX, oriXY, oriXZ);
	orientationY = new Vector3(oriYX, oriYY, oriYZ);
    }

    public Vector3 getIdentity() {
	return identity;
    }
    
    public Vector3 getLocation() {
	return location;
    }

    public void setLocation(int x, int y, int z) {
	location.set(x, y, z);
    }

    public void setLocation(Vector3 loc) {
	location = loc;
    }

    public Vector3 getOrientationX() {
	return orientationX;
    }

    public Vector3 getOrientationY() {
	return orientationY;
    }

    public void setOrientation(int xx, int xy, int xz, int yx, int yy, int yz) {
	orientationX.set(xx, xy, xz);
	orientationY.set(yx, yy, yz);
    }

    public void setOrientation(Vector3 x, Vector3 y) {
	orientationX = x;
	orientationY = y;
    }
}
