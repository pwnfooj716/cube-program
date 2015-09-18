import random

POP_SIZE = 50
INITIAL_LENGTH = 5


class PuzzleSolver:
    
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def generate(self, length):
        chromosome = ""
        prevMove = ""
        for i in range(length):
            move = random.choice(self.puzzle.moves)
            while move == prevMove:
                move = random.choice(self.puzzle.moves)
            prevMove = move
            modifier = random.choice(self.puzzle.modifiers)
            chromosome += move + modifier + " "
        return chromosome[:-1]
