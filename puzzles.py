# Keep a history of past moves and be able to undo them?
import math
import random

from tools import Vector, Cubie


class Puzzle:
    
    def __init__(self, moves, modifiers):
        self.moves = moves.split(" ")
        self.modifiers = [""] + modifiers.split(" ")
        if type(self) is Puzzle:
            raise NotImplementedError

    def apply_moves(self, algorithm):
        raise NotImplementedError

    @staticmethod
    def is_parallel(move1, move2):
        raise NotImplementedError

    def fitness(self):
        raise NotImplementedError

    def __str__(self):
        return "Moves: " + str(self.moves) + "\nModifiers: " + str(self.modifiers)

    
class ThreeSCube(Puzzle):    

    def __init__(self, scramble = None):
        Puzzle.__init__(self, "U D L R F B", "' 2")
        self.cubies = [Cubie(Vector(i, j, k))
                       for i in range(-1, 2)
                       for j in range(-1, 2)
                       for k in range(-1, 2) if (i!=0) or (j!=0) or (k!=0)]
        if scramble is not None:
            self.apply_moves(scramble)

    def arrange_cubies(self):
        array = {}
        for cubie in self.cubies:
            array.update({(cubie.location.x, cubie.location.y, cubie.location.z): cubie})
        return array

    @staticmethod
    def get_color(cubie, face):
        if face.equals(cubie.orientation_x):
            return 'R'
        elif face.equals(cubie.orientation_x.negate()):
            return 'O'
        elif face.equals(cubie.orientation_y):
            return 'B'
        elif face.equals(cubie.orientation_y.negate()):
            return 'G'
        else:
            orientation_z = cubie.orientation_x.cross(cubie.orientation_y)
            if face.equals(orientation_z):
                return 'W'
            elif face.equals(orientation_z.negate()):
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
            cubie.orientation_x = transform(cubie.orientation_x)
            cubie.orientation_y = transform(cubie.orientation_y)

    def apply_moves(self, algorithm):
        if algorithm == "":
            return
        moves = algorithm.split(" ")
        for move in moves:
            if move == "":
                print("What the fuck?")
                break
            else:
                self.apply_move(move)

    @staticmethod
    def is_parallel(move1, move2):
        try:
            return ThreeSCube.get_vector[move1].parallel_to(ThreeSCube.get_vector[move2])
        except KeyError:
            return False

    def fitness(self):
        matches = 0
        for cubie1 in self.cubies:
            for cubie2 in self.cubies:
                x_matches = cubie1.orientation_x.equals(cubie2.orientation_x)
                y_matches = cubie1.orientation_y.equals(cubie2.orientation_y)
                if x_matches and y_matches:
                    matches += 1
        return math.sqrt(matches) / len(self.cubies)

    def scramble(self):
        for i in range(1, 20):
            self.apply_move(random.choice(self.moves) + random.choice(self.modifiers))

    def __str__(self):
        s = Puzzle.__str__(self) + "\n"
        array = self.arrange_cubies()
        for k in range(-1, 2):
            for i in range(-1, 2):
                s += " "
            for j in range(-1, 2):
                s += ThreeSCube.get_color(array[-1, j, k], ThreeSCube.get_vector["B"])
            s += "\n"
        for i in range(-1, 2):
            for k in range(-1, 2):
                s += ThreeSCube.get_color(array[i, -1, k], ThreeSCube.get_vector["L"])
            for j in range(-1, 2):
                s += ThreeSCube.get_color(array[i, j, 1], ThreeSCube.get_vector["U"])
            for k in range(1, -2, -1):
                s += ThreeSCube.get_color(array[i, 1, k], ThreeSCube.get_vector["R"])
            s += "\n"
        for k in range(1, -2, -1):
            for i in range(-1, 2):
                s += " "
            for j in range(-1, 2):
                s += ThreeSCube.get_color(array[1, j, k], ThreeSCube.get_vector["F"])
            s += "\n"
        for i in range(1, -2, -1):
            for k in range(-1, 2):
                s += " "
            for j in range(-1, 2):
                s += ThreeSCube.get_color(array[i, j, -1], ThreeSCube.get_vector["D"])
            s += "\n"
        return s[:-1]

ThreeSCube.get_vector = {"U": Vector.k, "D": Vector.k.negate(), "L": Vector.j.negate(),
                               "R": Vector.j, "F": Vector.i, "B": Vector.i.negate()}


class ThreeByThreeCube(ThreeSCube):

    def __init__(self):
        pass