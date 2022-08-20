class Population:

    def __init__(self):
        self.candidates = []

    # Returns the sum of the fitness of all candidates
    def get_total_fitness(self):
        return sum(c.fitness for c in self.candidates)

    # Returns the best candidate and deletes it from the self.candidates list
    def pop_best_candidate(self):
        best_candidate = max(self.candidates, key = lambda candidates: candidates.fitness)
        self.candidates.remove(best_candidate)
        return best_candidate

    def print_population(self):
        for candidate in self.candidates:
            candidate.print_calendar()