# Keep a history of past moves and be able to undo them?

import tools

class Puzzle:
    FACE_U = tools.Vector.k
    FACE_D = tools.Vector.k.negate()
    FACE_L = tools.Vector.j.negate()
    FACE_R = tools.Vector.j
    FACE_F = tools.Vector.i
    FACE_B = tools.Vector.i.negate()
    
    def __init__(self, moves, modifiers):
        self.moves = moves.split(" ")
        self.modifiers = [""] + modifiers.split(" ")
        if type(self) is Puzzle:
            raise NotImplementedError

    def applyMoves(self, algorithm):
        raise NotImplementedError

    def fitness(self):
        raise NotImplementedError

    def __str__(self):
        return "Moves: " + str(self.moves) + "\nModifiers: " + str(self.modifiers)

class ThreeByThreeCube(Puzzle):
    def __init__(self, scramble = None):
        Puzzle.__init__(self, "U D L R F B", "' 2")
        self.cubies = [tools.Cubie(tools.Vector(i, j, k))
                       for i in range(-1, 2)
                       for j in range(-1, 2)
                       for k in range(-1, 2)]
        if scramble != None:
            self.applyMoves(scramble)
        print(self)

    def arrangeCubies(self):
        array = {}
        for cubie in self.cubies:
            array.update({(cubie.location.x, cubie.location.y, cubie.location.z): cubie})
        return array

    def getColor(cubie, face):
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

    def applyMove(self, move):
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
                transform = lambda v: tools.Vector(-v.x, -v.y, v.z)
            elif move[0] in "LMRx":
                transform = lambda v: tools.Vector(-v.x, v.y, -v.z)
            elif move[0] in "FBz":
                transform = lambda v: tools.Vector(v.x, -v.y, -v.z)
        else:
            prime = 1 if (len(move) > 1) and (move[1] == "'") else -1

            if move[0] in "Uy":
                transform = lambda v: tools.Vector(-prime * v.y, prime * v.x, v.z)
            elif move[0] == 'D':
                transform = lambda v: tools.Vector(prime * v.y, -prime * v.x, v.z)
            elif move[0] in "LM":
                transform = lambda v: tools.Vector(-prime * v.z, v.y, prime * v.x)
            elif move[0] in "Rx":
                transform = lambda v: tools.Vector(prime * v.z, v.y, -prime * v.x)
            elif move[0] in "Fz":
                transform = lambda v: tools.Vector(v.x, -prime * v.z, prime * v.y)
            elif move[0] == 'B':
                transform = lambda v: tools.Vector(v.x, prime * v.z, -prime * v.y)

        for cubie in filter(keep, self.cubies):
            cubie.location = transform(cubie.location)
            cubie.orientationX = transform(cubie.orientationX)
            cubie.orientationY = transform(cubie.orientationY)

    def applyMoves(self, algorithm):
        moves = algorithm.split(" ")
        for move in moves:
            self.applyMove(move)
        print(self)

    def fitness(self):
        return 0

    # Reimplement uses ncurses library
    def __str__(self):
        s = Puzzle.__str__(self) + "\n"
        array = self.arrangeCubies()
        for k in range(-1, 2):
            for i in range(-1, 2):
                s += " "
            for j in range(-1, 2):
                s += ThreeByThreeCube.getColor(array[-1, j, k], ThreeByThreeCube.FACE_B)
            s += "\n"
        for i in range(-1, 2):
            for k in range(-1, 2):
                s += ThreeByThreeCube.getColor(array[i, -1, k], ThreeByThreeCube.FACE_L)
            for j in range(-1, 2):
                s += ThreeByThreeCube.getColor(array[i, j, 1], ThreeByThreeCube.FACE_U)
            for k in range(1, -2, -1):
                s += ThreeByThreeCube.getColor(array[i, 1, k], ThreeByThreeCube.FACE_R)
            s += "\n"
        for k in range(1, -2, -1):
            for i in range(-1, 2):
                s += " "
            for j in range(-1, 2):
                s += ThreeByThreeCube.getColor(array[1, j, k], ThreeByThreeCube.FACE_F)
            s += "\n"
        for i in range(1, -2, -1):
            for k in range(-1, 2):
                s += " "
            for j in range(-1, 2):
                s += ThreeByThreeCube.getColor(array[i, j, -1], ThreeByThreeCube.FACE_D)
            s += "\n"
        return s[:-1]
