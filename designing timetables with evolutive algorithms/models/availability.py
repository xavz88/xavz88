class Availability:
    def __init__(self, time_from, time_to):
        self.time_from = time_from
        self.time_to = time_to
        if (time_from > time_to):
            raise("Invalid availability")

    def to_string(self):
        return f"From: {self.time_from}, To: {self.time_to}"