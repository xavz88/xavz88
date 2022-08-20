class Gene:
    def __init__(self, day, hour, subject):
        self.day = day
        self.hour = hour
        self.subject = subject

    # Returns a copy of the current gene 
    def clone(self):
        return Gene(self.day, self.hour, self.subject)

    def to_string(self):
        return f"College Class: {self.subject.college_class.name}\nSubject: {self.subject.name}\nTeacher: {self.subject.teacher.name} \nDay: {self.day_to_string(self.day)}\nHour: {self.hour}"

    def day_to_string(self, day):
        if (day == 0):
            return "monday"
        if (day == 1):
            return "tuesday"
        if (day == 2):
            return "wednesday"
        if (day == 3):
            return "thursday"
        if (day == 4):
            return "friday"