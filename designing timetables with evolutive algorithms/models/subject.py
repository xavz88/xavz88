class Subject:
    def __init__(self, name, week_hours, teacher_id, college_class, teacher_list):
        self.name = name
        self.week_hours = week_hours
        self.teacher_id = teacher_id
        self.college_class = college_class
        self.set_teacher(teacher_list)

    ## Adds a reference to the teacher instance for further use
    def set_teacher(self, teacher_list):
        for teacher in teacher_list:
            if (teacher.id == self.teacher_id):
                self.teacher = teacher
                return

    def to_string(self): 
        return f"      Name: {self.name}\n      Week hours: {self.week_hours}\n      Teacher: {self.teacher_id}\n"
