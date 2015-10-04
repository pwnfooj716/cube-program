import random
import copy
import tools

from puzzles import ThreeSCube
from tools import Vector

POP_SIZE = 10
POP_MULTIPLY = 5
INITIAL_LENGTH = 5
P_M = 0.2
P_LC = 0.1

# 10 initial chromosomes
# each one mutates into 4 different chromosomes
# now have 50 chromosomes
# then pick the top 10 from those 50
# repeat

class PuzzleSolverGenetic:
    
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

    def mutate(self, chromosome):
        new_chromosome = ""
        for move in chromosome.split(" "):
            if random.random() < P_M:
                new_chromosome += random.choice(self.puzzle.moves) + random.choice(self.puzzle.modifiers) + " "
            else:
                new_chromosome += move + " "
        
        r = random.random()
        if r < (P_LC / 2):  # Remove last move from chromosome
            space_position = new_chromosome[-2:-5:-1].find(" ")
            if space_position == -1:
                return new_chromosome
            new_chromosome = new_chromosome[:-(space_position + 1)]
        elif r < P_LC:  # Add new move to chromosome
            new_chromosome += random.choice(self.puzzle.moves) + random.choice(self.puzzle.modifiers) + " "
        return new_chromosome[:-1]

    def select(self, population):
        while len(population) > POP_SIZE:
            sum = 0
            for chromosome in population.keys():
                fitness = population[chromosome] # Revert this when the bsfix is not needed
                sum += 1 - fitness
            r = random.random()
            accumulation = 0
            for chromosome in population.keys():
                fitness = population[chromosome]
                accumulation += (1 - fitness) / sum
                if accumulation >= r:
                    break
            del population[chromosome]

    def run(self, iterations):
        population = {}
        for i in range(POP_SIZE):
            chromosome = self.generate(INITIAL_LENGTH)
            new_puzzle = copy.deepcopy(self.puzzle)
            new_puzzle.apply_moves(chromosome)
            population.update({chromosome: new_puzzle.fitness()})
        print(population)
        
        for i in range(iterations):
            print("Iteration: " + str(i))
            extra_population = {}
            for chromosome in population.keys():
                for j in range(POP_MULTIPLY - 1):
                    new_chromosome = self.mutate(chromosome)
                    new_puzzle = copy.deepcopy(self.puzzle)
                    new_puzzle.apply_moves(new_chromosome)
                    extra_population.update({new_chromosome: new_puzzle.fitness()})
            population.update(extra_population)
            self.select(population)
            print(population)
        sorted_population = sorted(population.items(), key=lambda t: t[1])
        print("Final sorted:")
        for item in sorted_population:
            print(item)

    # def run(self):
    #     population = {}
    #     for i in range(POP_SIZE):
    #         chromosome = self.generate(INITIAL_LENGTH)
    #         new_puzzle = copy.deepcopy(self.puzzle)
    #         new_puzzle.apply_moves(chromosome)
    #         population.update({chromosome: new_puzzle.fitness()})
    #     print(population)
        
    #     while 1 not in population.values():
    #         print("Iteration: " + str(i))
    #         extra_population = {}
    #         for chromosome in population.keys():
    #             for j in range(POP_MULTIPLY - 1):
    #                 new_chromosome = self.mutate(chromosome)
    #                 new_puzzle = copy.deepcopy(self.puzzle)
    #                 new_puzzle.apply_moves(new_chromosome)
    #                 extra_population.update({new_chromosome: new_puzzle.fitness()})
    #         population.update(extra_population)
    #         self.select(population)
    #         print(population)
    #     sorted_population = sorted(population.items(), key=lambda t: t[1])
    #     print("Final sorted:")
    #     for item in sorted_population:
    #         print(item)

class SolveW: #White Side Solve
    
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def cross_bf(self):
        for c in self.puzzle.cubies:
            if (c.is_edge() and c.identity.z == 1):
                print(c)
        moves = [0]
        currMove = ""
        solutions = []
        temp = copy.deepcopy(self.puzzle)
        solved = False
        while solved == False:
            print(moves)
            for i in range(len(moves)):
                temp.apply_move(temp.moves[moves[i]%6] + temp.modifiers[moves[i]//6])
                currMove += str(temp.moves[moves[i]%6] + temp.modifiers[moves[i]//6])
            tempSolve = True
            WEdges = [Vector(1, 0, 1), Vector(-1, 0, 1), Vector(0, 1, 1), Vector(0, -1, 1)]
            for v in WEdges:
                c = temp.arrange_cubies()[v.x, v.y, v.z]
                if ((c.orientation_x.equals(Vector(1, 0, 0))) and (c.orientation_y.equals(Vector(0, 1, 0)))) == False:
                    tempSolve = False
                    break
            if tempSolve:
                solutions += [currMove]
                print(currMove)
            moves[len(moves)-1]+=1
            temp = copy.deepcopy(self.puzzle)
            currMove = ""
            for i in range (len(moves)-1, 0, -1):
                if (moves[i] == 18):
                    moves[i] = 0
                    moves[i-1]+=1
            if moves[0] == 18:
                if len(solutions) > 0:
                    solved = True
                    break
                moves[0] = 0
                moves+=[0]
        return solutions
        

p = SolveW(ThreeSCube())
p.puzzle.scramble()
print(p.cross_bf())