from evolutive import Evolutive
from json_reader import JsonReader
from toCSV import ToCsv

# Number of candidates at the population
population_size = 24
# Number of best candidates chosen each iteration
selection_size = 12
# Probability of mutation of a random gene of the population
mutation_rate = 0.02
# Max number of generations made by the algorithm
max_generations = 10000

jsonReader = JsonReader()
classes, teachers = jsonReader.read_input_json()
#jsonReader.print_loaded_data()

model = Evolutive(population_size, selection_size, mutation_rate, max_generations, classes, teachers)
result = model.get_result()

result.print_calendar()
print(f"Best solution fitness: {result.fitness}")
ToCsv.create_classes_schedule_csv(result)
ToCsv.create_teachers_schedule_csv(result)