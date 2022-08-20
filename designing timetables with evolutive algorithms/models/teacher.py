from models.week_availability import WeekAvailability

class Teacher:
    def __init__(self, id, name, availability):
        self.id = id
        self.name = name
        self.availability = WeekAvailability(availability)

    def to_string(self): 
        return f"Teacher: {self.name}   Availability:\n{self.availability.to_string()}"

    def get_day_availability(self, day):
        if day == 0:
            return self.availability.monday
        if day == 1:
            return self.availability.tuesday
        if day == 2:
            return self.availability.wednesday
        if day == 3:
            return self.availability.thursday
        if day == 4:
            return self.availability.friday