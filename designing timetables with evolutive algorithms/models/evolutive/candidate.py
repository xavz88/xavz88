import itertools
import random

# Genotype
class Candidate:

    def __init__(self):
        # Fitness score obtained by the fitness function
        self.fitness = 0
        # Set of genes
        self.calendar = []

    # Returns the first free day and hour at the calendar of the given college_class
    def get_free_slot(self, college_class):
        days = range(5) # From monday to friday
        hours = range(college_class.availability.time_from, college_class.availability.time_to)

        # Obtain every possible slot
        possible_slots = self.get_possible_slots(days, hours)

        # Find all gene from the class given by parameter
        college_class_genes = [gene for gene in self.calendar if gene.subject.college_class == college_class]

        # Find all slots (day, hour) already occupied
        occupied_slots = [(gene.day, gene.hour) for gene in college_class_genes]

        free_slots = self.get_free_slots(possible_slots, occupied_slots)

        if not free_slots:
            raise "There is no free slots."

        return random.choice(free_slots)
    
    # Returns all free slots (day, hour) at the calendar
    def get_free_slots(self, possible_slots, occupied_slots):
        free_slots = []

        for ps in possible_slots:   
            # [0] == day, [1] == hour         
            if all(os[0] != ps[0] or os[1] != ps[1] for os in occupied_slots):
                free_slots.append(ps)

        return free_slots
    
    # Prints the full calendar of the current candidate
    def print_calendar(self):
        for gene in self.calendar:
            print(gene.to_string())

    # Returns de cartesian product of days and hours
    def get_possible_slots(self, days, hours):
        cartesian_product = itertools.product(days, hours)

        return [(day_hour[0], day_hour[1]) for day_hour in cartesian_product]

    # Get the gene at day/hour given by parameter
    def get_gene(self, day, hour, college_class):
        # Find all gene from the class given by parameter
        college_class_genes = [gene for gene in self.calendar if gene.subject.college_class == college_class]

        for gene in college_class_genes:
            if gene.day == day and gene.hour == hour:
                return gene
            
        return None
