from models.college_class import CollegeClass
from models.teacher import Teacher
import json

class JsonReader:
    dataFile = "data/input.json"

    def __init__(self):
        self.classes = []
        self.teachers = []

    ## It reads the input data JSON
    def read_input_json(self):
        f = open(self.dataFile)
        jsonData = json.load(f)
        
        for json_teacher in jsonData["teachers"]:
            self.teachers.append(Teacher(json_teacher["id"], json_teacher["name"], json_teacher["availability"]))    

        for json_class in jsonData["classes"]:
            self.classes.append(CollegeClass(json_class["name"], json_class["subjects"], json_class["availability"], self.teachers))    
        
        f.close()

        return (self.classes, self.teachers)

    ## Prints the data readed from the input json
    def print_loaded_data(self):
        for college_class in self.classes:
            print(f"\n{college_class.to_string()}\n")

        for teacher in self.teachers:
            print(f"{teacher.to_string()}\n")
