import math


class Vector:

    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def equals(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def plus(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def minus(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def times(self, k):
        return Vector(k * self.x, k * self.y, k * self.z)

    def over(self, k):
        return Vector(self.x / k, self.y / k, self.z / k)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        new_x = self.y * other.z - self.z * other.y
        new_y = self.z * other.x - self.x * other.z
        new_z = self.x * other.y - self.y * other.x
        return Vector(new_x, new_y, new_z)

    def negate(self):
        return Vector(-self.x, -self.y, -self.z)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def comp(self, onto):
        return self.dot(onto) / onto.magnitude()

    def proj(self, onto):
        return onto.times(self.dot(onto) / (onto.magnitude() ** 2))

    def parallel_to(self, other):
        return self.cross(other).equals(Vector.zero)

    # Version 1: <x, y, z> notation
    def __str__(self):
        return "<" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ">"

    # Version 2: xi + yj + zk notation
    # def __str__(self):
    #     s = ""
    #     if self.x != 0:
    #         if self.x != 1:
    #             s += str(self.x)
    #         s += "i"
    #     if self.y != 0:
    #         if s != "":
    #             if self.y > 0:
    #                 s += " + "
    #             else:
    #                 s += " - "
    #         if self.y != 1:
    #             s += str(abs(self.y))
    #         s += "j"
    #     if self.z != 0:
    #         if s != "":
    #             if self.z > 0:
    #                 s += " + "
    #             else:
    #                 s += " - "
    #         if self.z != 1:
    #             s += str(abs(self.z))
    #         s += "k"
    #     return s

Vector.zero = Vector(0, 0, 0)
Vector.i = Vector(1, 0, 0)
Vector.j = Vector(0, 1, 0)
Vector.k = Vector(0, 0, 1)


class Cubie:
    
    def __init__(self, identity, location = None, orientation_x = Vector.i, orientation_y = Vector.j):
        self.identity = identity
        if location == None:
            self.location = identity
        else:
            self.location = location
        self.orientation_x = orientation_x
        self.orientation_y = orientation_y

    def __str__(self):
        s = "Identity: " + str(self.identity) + " \t"
        s += "Location: " + str(self.location) + " \t"
        s += "Orientation_x: " + str(self.orientation_x) + "\t"
        s += "Orientation_y: " + str(self.orientation_y)
        return s

    def is_edge(self):
        return (abs(self.location.x)+abs(self.location.y)+abs(self.location.z) == 2)

    def is_corner(self):
        return (abs(self.location.x)+abs(self.location.y)+abs(self.location.z) == 3)

    def is_center(self):
        return (abs(self.location.x)+abs(self.location.y)+abs(self.location.z) == 1)
