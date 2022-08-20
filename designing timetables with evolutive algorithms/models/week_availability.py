from models.availability import Availability

class WeekAvailability:
    monday = []
    tuesday = []
    wednesday = []
    thursday = []
    friday = []
    
    def __init__(self, week_availability):
        self.monday = self.get_availability_intervals(week_availability["monday"])
        self.tuesday = self.get_availability_intervals(week_availability["tuesday"])
        self.wednesday = self.get_availability_intervals(week_availability["wednesday"])
        self.thursday = self.get_availability_intervals(week_availability["thursday"])
        self.friday = self.get_availability_intervals(week_availability["friday"])

    def get_availability_intervals(self, availability_list):
        intervals = []

        for interval in availability_list:
            intervals.append(Availability(interval["from"], interval["to"]))

        return intervals

    def to_string(self):
        return f"""\nMonday: \n {[availability.to_string() for availability in self.monday]}
                   \nTuesday: \n {[availability.to_string() for availability in self.tuesday]}
                   \nWednesday: \n {[availability.to_string() for availability in self.wednesday]}
                   \nThursday: \n {[availability.to_string() for availability in self.thursday]}
                   \nFriday: \n {[availability.to_string() for availability in self.friday]}"""
