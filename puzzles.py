# Keep a history of past moves and be able to undo them?

from tools import Vector, Cubie


class Puzzle:
    
    def __init__(self, moves, modifiers):
        self.moves = moves.split(" ")
        self.modifiers = [""] + modifiers.split(" ")
        if type(self) is Puzzle:
            raise NotImplementedError

    def apply_moves(self, algorithm):
        raise NotImplementedError

    def fitness(self):
        raise NotImplementedError

    def __str__(self):
        return "Moves: " + str(self.moves) + "\nModifiers: " + str(self.modifiers)

    
class ThreeByThreeCube(Puzzle):
    
    FACE_U = Vector.k
    FACE_D = Vector.k.negate()
    FACE_L = Vector.j.negate()
    FACE_R = Vector.j
    FACE_F = Vector.i
    FACE_B = Vector.i.negate()
    

    def __init__(self, scramble = None):
        Puzzle.__init__(self, "U D L R F B", "' 2")
        self.cubies = [Cubie(Vector(i, j, k))
                       for i in range(-1, 2)
                       for j in range(-1, 2)
                       for k in range(-1, 2)]
        if scramble is not None:
            self.apply_moves(scramble)
        else:
            print(self)

    def arrange_cubies(self):
        array = {}
        for cubie in self.cubies:
            array.update({(cubie.location.x, cubie.location.y, cubie.location.z): cubie})
        return array

    @staticmethod
    def get_color(cubie, face):
        if face.equals(cubie.orientationX):
            return 'R'
        elif face.equals(cubie.orientationX.negate()):
            return 'O'
        elif face.equals(cubie.orientationY):
            return 'B'
        elif face.equals(cubie.orientationY.negate()):
            return 'G'
        else:
            orientationZ = cubie.orientationX.cross(cubie.orientationY)
            if face.equals(orientationZ):
                return 'W'
            elif face.equals(orientationZ.negate()):
                return 'Y'
        return 'N'

    def apply_move(self, move):
        keep = lambda cubie: False
        transform = lambda v: v

        if move[0] == 'U':
            keep = lambda cubie: cubie.location.z == 1
        elif move[0] == 'D':
            keep = lambda cubie: cubie.location.z == -1
        elif move[0] == 'L':
            keep = lambda cubie: cubie.location.y == -1
        elif move[0] == 'M':
            keep = lambda cubie: cubie.location.y == 0
        elif move[0] == 'R':
            keep = lambda cubie: cubie.location.y == 1
        elif move[0] == 'F':
            keep = lambda cubie: cubie.location.x == 1
        elif move[0] == 'B':
            keep = lambda cubie: cubie.location.x == -1
        elif move[0] in "xyz":
            keep = lambda cubie: True

        if (len(move) > 1) and (move[1] == '2'):
            if move[0] in "UDy":
                transform = lambda v: Vector(-v.x, -v.y, v.z)
            elif move[0] in "LMRx":
                transform = lambda v: Vector(-v.x, v.y, -v.z)
            elif move[0] in "FBz":
                transform = lambda v: Vector(v.x, -v.y, -v.z)
        else:
            prime = 1 if (len(move) > 1) and (move[1] == "'") else -1

            if move[0] in "Uy":
                transform = lambda v: Vector(-prime * v.y, prime * v.x, v.z)
            elif move[0] == 'D':
                transform = lambda v: Vector(prime * v.y, -prime * v.x, v.z)
            elif move[0] in "LM":
                transform = lambda v: Vector(-prime * v.z, v.y, prime * v.x)
            elif move[0] in "Rx":
                transform = lambda v: Vector(prime * v.z, v.y, -prime * v.x)
            elif move[0] in "Fz":
                transform = lambda v: Vector(v.x, -prime * v.z, prime * v.y)
            elif move[0] == 'B':
                transform = lambda v: Vector(v.x, prime * v.z, -prime * v.y)

        for cubie in filter(keep, self.cubies):
            cubie.location = transform(cubie.location)
            cubie.orientationX = transform(cubie.orientationX)
            cubie.orientationY = transform(cubie.orientationY)

    def apply_moves(self, algorithm):
        moves = algorithm.split(" ")
        for move in moves:
            self.apply_move(move)
        print(self)

    def fitness(self):
        return 0

    # Reimplement uses ncurses library
    def __str__(self):
        s = Puzzle.__str__(self) + "\n"
        array = self.arrange_cubies()
        for k in range(-1, 2):
            for i in range(-1, 2):
                s += " "
            for j in range(-1, 2):
                s += ThreeByThreeCube.get_color(array[-1, j, k], ThreeByThreeCube.FACE_B)
            s += "\n"
        for i in range(-1, 2):
            for k in range(-1, 2):
                s += ThreeByThreeCube.get_color(array[i, -1, k], ThreeByThreeCube.FACE_L)
            for j in range(-1, 2):
                s += ThreeByThreeCube.get_color(array[i, j, 1], ThreeByThreeCube.FACE_U)
            for k in range(1, -2, -1):
                s += ThreeByThreeCube.get_color(array[i, 1, k], ThreeByThreeCube.FACE_R)
            s += "\n"
        for k in range(1, -2, -1):
            for i in range(-1, 2):
                s += " "
            for j in range(-1, 2):
                s += ThreeByThreeCube.get_color(array[1, j, k], ThreeByThreeCube.FACE_F)
            s += "\n"
        for i in range(1, -2, -1):
            for k in range(-1, 2):
                s += " "
            for j in range(-1, 2):
                s += ThreeByThreeCube.get_color(array[i, j, -1], ThreeByThreeCube.FACE_D)
            s += "\n"
        return s[:-1]
