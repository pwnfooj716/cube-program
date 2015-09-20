import random
import copy

from puzzles import ThreeByThreeCube

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
                fitness = population[chromosome]
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
