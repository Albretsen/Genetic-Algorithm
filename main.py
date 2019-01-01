# Genetic Algorithm
# This is genetic algorithm for generating strings, but can be easily rebuilt to fit any type of DNA. It works by
# generating a random population, then it creates a new generation based on the best specimens from the last generation.
# How good a specimen is, is referred to as fitness. Fitness is how much of a specimens DNA matches our target DNA.
# Fitness can be easily changed to anything else though. If there is no target, fitness can for example be distance
# travelled, or even user inputted scores.

import random
import string

# This is the string the script will try to recreate through the algorithm
target_string = "only lower case ascii and spaces"
# This the population size. Optimal size depends on computer specs! You have to play around with this value to find
# your optimal size.
population_size = 800
# The mutation rate is how often DNA will randomly change
mutation_rate = 0.01
phrase_length = len(target_string)
# The space rate is how often spaces will appear in stead of ascii characters
space_rate = 0.03846153846


class Population:

    population = []

    def __init__(self, target_string_temp, mutation_rate_temp, population_size_temp):
        self.target = target_string_temp
        self.mutation_rate = mutation_rate_temp
        self.population_size = population_size_temp
        self.best_phrase = ""
        self.generation = 0
        self.perfect_score = 1
        self.finish = True
        for i in range(self.population_size):
            self.population.append(DNA())

    # This function calls the calculate fitness function on every single DNA in it's population
    def calc_fitness(self):
        for i in range(len(self.population)):
            self.population[i].calc_fitness()

    # This function is responsible for printing each generations best specimen and also stops the loop when the
    # optimal specimen is found.
    def evaluate(self):
        highest_fitness = 0
        for i in range(len(self.population)):
            if self.population[i].fitness > highest_fitness:
                highest_fitness = self.population[i].fitness
                temp_best_phrase = self.population[i].gen_string()
        self.best_phrase = temp_best_phrase
        print(self.best_phrase)
        if highest_fitness >= self.perfect_score:
            self.finish = False
            print("")
            print("Generations: " + str(self.generation))

    # This function generates the next generation
    def generate(self):
        self.generation += 1
        highest_fitness = 0
        for i in range(len(self.population)):
            if self.population[i].fitness > highest_fitness:
                highest_fitness = self.population[i].fitness
        pass

        new_population = []
        for i in range(len(self.population)):
            partner_a = self.accept_reject(highest_fitness)
            partner_b = self.accept_reject(highest_fitness)
            child = partner_a.cross_over(partner_b)
            child.mutate(self.mutation_rate)
            new_population.append(child)
        self.population = new_population

    # This function picks a partner while favoring higher fitness
    def accept_reject(self, highest_fitness):
        use_protection = 0
        while True:
            index = random.randint(0, len(self.population)-1)
            r = random.uniform(0, highest_fitness)
            partner = self.population[index]
            if r < partner.fitness:
                return partner
            use_protection += 1
            if use_protection > 10000:
                return None


class DNA:

    # The DNA automatically creates a string when initialized.
    def __init__(self):
        self.DNA = []
        self.fitness = 0
        for i in range(phrase_length):
            if random.uniform(0, 1) < space_rate:
                self.DNA.append(" ")
            else:
                self.DNA.append(random.choice(string.ascii_letters).lower())

    # This function calculates the fitness level for every string of DNA. It works by comparing the DNA string to
    # the target string. If there is a character or space match, the fitness level increases by 1. The last part
    # converts the fitness level to a 0-1 scale.
    def calc_fitness(self):
        score = 0
        for i in range(len(self.DNA)):
            if self.DNA[i] == target_string[i]:
                score += 1
        self.fitness = score / len(self.DNA)
        self.fitness = pow(self.fitness, 2) + 0.01

    # This function generates a string from the DNA so it can be printed
    def gen_string(self):
        s = ""
        for i in range(len(self.DNA)):
            s = s + self.DNA[i]
        return s

    # This function picks a random point in a DNA, and creates a child DNA. The child DNA is built upon partner_a's DNA
    # up to the random mid point, and the rest of the DNA is from partner_b.
    def cross_over(self, partner):
        child = DNA()
        mid_point = random.randint(0, len(self.DNA))

        for i in range(len(self.DNA)):
            if i > mid_point:
                child.DNA[i] = self.DNA[i]
            else:
                child.DNA[i] = partner.DNA[i]

        return child

    # DNA will randomly change to avoid the population getting stuck at certain points. If a population has no member
    # with a space or a character like "b", it would never appear.
    def mutate(self, mutation_rate_temp):
        for i in range(len(self.DNA)):
            if random.uniform(0, 1) < mutation_rate_temp:
                if random.uniform(0, 1) < space_rate:
                    self.DNA[i] = " "
                else:
                    self.DNA[i] = random.choice(string.ascii_letters).lower()


# Generates the population instance.
population = Population(target_string, mutation_rate, population_size)


# This loop will stop when the perfect DNA string is created
while population.finish:
    population.calc_fitness()
    population.evaluate()
    population.generate()

