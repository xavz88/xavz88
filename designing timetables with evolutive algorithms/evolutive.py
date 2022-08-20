import random
from fitness import Fitness
from models.evolutive.candidate import Candidate
from models.evolutive.gene import Gene
from models.evolutive.population import Population
from random import randrange
import math


class Evolutive:

    percentage_completed = 0.05

    def __init__(self, population_size, selection_size, mutation_rate, max_generations, college_classes, teacher_list):
        self.fitness = Fitness()
        self.population_size = population_size
        self.selection_size = selection_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.college_classes = college_classes
        self.teacher_list = teacher_list
        self.child_creation_rate = math.ceil(population_size / 2)

        if (self.population_size == 0
            or self.selection_size == 0
            or self.mutation_rate == 0
            or self.max_generations == 0
            or self.selection_size > self.population_size):
            raise "Invalid parameters"

    def get_result(self):
        generation = 0
        population = self.get_initial_population()
        # population.print_population()
        [self.fitness.set_fitness_score(candidate, self.teacher_list, self.college_classes) for candidate in population.candidates]
        max_fitness = 0

        while not self.end_condition(generation, population):
            population.candidates = self.select_candidates(population)
            population.candidates = self.combination(population)
            population.candidates = self.mutation(population)
            [self.fitness.set_fitness_score(candidate, self.teacher_list, self.college_classes) for candidate in population.candidates]

            best_solution = max(population.candidates, key = lambda candidates: candidates.fitness).fitness
            if best_solution > max_fitness:
                max_fitness = best_solution
                print(f"Max fitness found: {best_solution}")

            generation += 1
        
        best_solution = max(population.candidates, key = lambda candidates: candidates.fitness)

        return best_solution

    # We will create a number of childs equal to the child_creation_rate (it is population_size / 2)  
    # For every subject at the input Json, we will assign the half of the subjects schedule of one
    # parent and the half of the other to the child. If there is a conflict, we will assign a random free slot instead
    # in order to create a valid child
    def combination(self, population):
        children = []

        for _ in range(self.child_creation_rate):
            parent1, parent2 = random.sample(population.candidates, 2)
            child = Candidate()
            
            for college_class in self.college_classes:
                for subject in college_class.subjects:
                    parent1_subject_genes = [gene for gene in parent1.calendar if gene.subject == subject]
                    parent2_subject_genes = [gene for gene in parent2.calendar if gene.subject == subject]
                    
                    number_of_hours_of_subject_to_get_from_parent_1 = math.ceil(subject.week_hours / 2)

                    parent_genes = random.sample(parent1_subject_genes,
                                                    number_of_hours_of_subject_to_get_from_parent_1)
                    parent_genes += random.sample(parent2_subject_genes,
                                                    subject.week_hours - number_of_hours_of_subject_to_get_from_parent_1)

                    for parent_gene in parent_genes:
                        child_gene = parent_gene.clone()

                        # Check if there is a conflict
                        conflicting_gene = child.get_gene(parent_gene.day, parent_gene.hour, parent_gene.subject.college_class)

                        if conflicting_gene:
                            # There is a conflict. Let's assign a random free slot to the parent gene
                            child_gene.day, child_gene.hour = child.get_free_slot(parent_gene.subject.college_class)
                            
                        child.calendar.append(child_gene)

            children.append(child)

        population.candidates += children

        return population.candidates

    # Mutates a random gene in every candidate with a probability equals to mutation_rate
    def mutation(self, population):
        rand_number = random.random()

        if rand_number <= self.mutation_rate:
            candidate = random.choice(population.candidates)
            random_gene = random.choice(candidate.calendar)
            day = random.choice(range(5))
            hour = random.choice(range(random_gene.subject.college_class.availability.time_from,
                                                    random_gene.subject.college_class.availability.time_to))
            
            # Check if there is a conflict. If so, assign a random free slot to the subject
            conflicting_gene = candidate.get_gene(day, hour, random_gene.subject.college_class)
            
            if not conflicting_gene:
                random_gene.day = day
                random_gene.hour = hour
            else:
                random_gene.day, random_gene.hour = candidate.get_free_slot(random_gene.subject.college_class)

        return population.candidates

    # Initializes the population with candidates with random values
    def get_initial_population(self):
        population = Population()

        for _ in range(self.population_size):
            candidate = Candidate()
            for college_class in self.college_classes:
                for subject in college_class.subjects:
                    for _ in range(subject.week_hours):
                        day, hour = candidate.get_free_slot(college_class)
                        candidate.calendar.append(Gene(day, hour, subject))

            population.candidates.append(candidate)

        return population

    # Selects #selection_size candidates randomly with a probability equals to candidate_fitness_score/population_total_score
    # This function will take the #selection_size/4 candidates with most fitness in order 
    # to protect the best candidates against randomness. The rest of the elements are chosen
    # using the roulette strategy
    def select_candidates(self, population):
        selection = []

        # Get the best candidates
        for _ in range(math.ceil(self.selection_size / 4)):
            selection.append(population.pop_best_candidate())

        # Get the rest of the candidates using the roulette method
        for _ in range(self.selection_size - (math.ceil(self.selection_size / 4))):
            fitness_accumulated = 0

            if population.get_total_fitness() > 0:
                rand_number = randrange(population.get_total_fitness())

                for candidate in population.candidates:
                    fitness_accumulated += candidate.fitness
                    if fitness_accumulated >= rand_number:
                        selection.append(candidate)
                        population.candidates.remove(candidate)
                        break

        selection_size = len(selection)
        
        # If selection lenght is less than selection_size is because more than #selection_size
        # elements has fitness = 0. Select randomly the rest of the candidates
        if selection_size < self.selection_size:
            selection += random.sample(population.candidates, self.selection_size - selection_size)

        return selection

    def end_condition(self, generation, population):
        # 95% of the maximum fitness value is enaugh to consider the solution as optimal
        if any(candidate.fitness >= (self.fitness.get_max_possible_fitness(self.college_classes, self.teacher_list, candidate) * 0.95)
                for candidate in population.candidates):
            return True

        # Print the % of the generations completed
        if round(self.max_generations * self.percentage_completed) == generation:
            print(f"{round(self.percentage_completed * 100)}% completed...")
            self.percentage_completed = self.percentage_completed + 0.05

        return generation == self.max_generations
