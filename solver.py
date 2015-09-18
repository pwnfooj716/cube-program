import random
import copy

POP_SIZE = 50
INITIAL_LENGTH = 5


class PuzzleSolver:
    
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def generate(self, length):
        chromosome = ""
        temp_moves = self.puzzle.moves
        prev_move = ""
        for i in range(length):
            move = random.choice(temp_moves)
            if not self.puzzle.is_parallel(move, prev_move):
                temp_moves = copy.copy(self.puzzle.moves)
            temp_moves.remove(move)
            prev_move = move
            modifier = random.choice(self.puzzle.modifiers)
            chromosome += move + modifier + " "

        return chromosome[:-1]
