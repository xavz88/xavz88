from models.availability import Availability
from models.subject import Subject

class CollegeClass:
    def __init__(self, name, subjects, availability, teacher_list):
        self.name = name
        self.availability = Availability(availability["from"], availability["to"])
        self.subjects = []

        for subject in subjects:
            self.subjects.append(Subject(subject["name"], subject["weekHours"], subject["teacher"], self, teacher_list))
    
    def to_string(self): 
        class_data = f"  Class: {self.name}\n   Availability: {self.availability.to_string()}   Subjects:\n"
        for subject in self.subjects:
            class_data += f"{subject.to_string()}\n"
        
        return class_data