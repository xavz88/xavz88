import math


class Fitness:
    
    max_possible_score = 0
    max_number_of_subjects_per_day = 6
    max_teacher_number_of_subjects_per_day = 4
    max_hours_per_subject_per_day = 2
    s1_score = 20
    s2_score = 10
    s3_score = 20
    s4_score = 20
    s5_score = 20
    s6_score = 10

    # Sets the fitness score to the candidate given
    def set_fitness_score(self, candidate, teacher_list, college_classes):        
        score = 0

        score += self.s1(candidate, college_classes)
        score += self.s2(candidate, teacher_list)
        score += self.s3(candidate, college_classes)
        score += self.s4(candidate, college_classes)
        score += self.s5(candidate, college_classes)
        score += self.s6(candidate, teacher_list)
        score = self.h1(candidate, teacher_list, score)
        score = self.h2(candidate, teacher_list, score)

        candidate.fitness = score


    # Hard condition - A teacher cannot be in two different classes at the same time.
    def h1(self, candidate, teacher_list, current_score):
        already_punished_subjects = []
        
        for teacher in teacher_list:
            calendar_teacher_subjects = [gene for gene in candidate.calendar if gene.subject.teacher == teacher]

            for teacher_subject in calendar_teacher_subjects:
                if all(teacher_subject != aps for aps in already_punished_subjects):
                    conflicting_subjects = [ts for ts in calendar_teacher_subjects if ts != teacher_subject 
                                                                                        and ts.day == teacher_subject.day     
                                                                                        and ts.hour == teacher_subject.hour]
                    for _ in range(len(conflicting_subjects)):
                        current_score = math.floor(current_score / 2)

                    already_punished_subjects += conflicting_subjects

        return current_score

    # Hard condition - A teacher cannot teach a subject if he/she is not in the center.
    def h2(self, candidate, teacher_list, current_score):
        for teacher in teacher_list:
            calendar_teacher_subjects = [gene for gene in candidate.calendar if gene.subject.teacher == teacher]

            for teacher_subject in calendar_teacher_subjects:
                teacher_day_availability = teacher.get_day_availability(teacher_subject.day)
                if not any(availability_interval.time_from <= teacher_subject.hour and availability_interval.time_to >= teacher_subject.hour for availability_interval in teacher_day_availability):
                    current_score = math.floor(current_score / 2)

        return current_score

    # Soft condition - Penalize class schedules with many hours on the same day.
    def s1(self, candidate, college_classes, debug = False):
        score = 0
        
        for college_class in college_classes:
            for day in range(5):
                day_subjects = [gene for gene in candidate.calendar if gene.subject.college_class == college_class and gene.day == day]
                if debug or len(day_subjects) <= self.max_number_of_subjects_per_day:
                    score += self.s1_score

        return score

    # Soft condition - Penalize teachers schedules with many hours on the same day.
    def s2(self, candidate, teacher_list, debug = False):
        score = 0
        
        for teacher in teacher_list:
            for day in range(5):
                day_subjects = [gene for gene in candidate.calendar if gene.day == day and gene.subject.teacher == teacher]
                if debug or len(day_subjects) <= self.max_teacher_number_of_subjects_per_day:
                    score += self.s2_score

        return score

    # Soft condition - Penalize schedules with days with more than self.max_hours_per_subject_per_day hours of the same subject for students.
    def s3(self, candidate, college_classes, debug = False):
        score = 0
        already_checked_genes = []
        
        for college_class in college_classes:
            for day in range(5):
                class_day_genes = [gene for gene in candidate.calendar if gene.subject.college_class == college_class and gene.day == day]
                day_is_ok = True

                for gene in class_day_genes:
                    # Check if the gene has been already checked
                    if all(gene != apg for apg in already_checked_genes):
                        same_subject_genes = [ts for ts in class_day_genes if ts.subject == gene.subject]
                        already_checked_genes += same_subject_genes

                        if len(same_subject_genes) > self.max_hours_per_subject_per_day:
                            day_is_ok = False
                            break
                        
                if debug or day_is_ok:
                    score += self.s3_score
                    
        return score
     
    # Soft condition - If a subject has hours in a day, they should be followed.
    def s4(self, candidate, college_classes, debug = False):
        score = 0
        already_scored_genes = []
        
        for college_class in college_classes:
            for day in range(5):
                class_day_genes = [gene for gene in candidate.calendar if gene.subject.college_class == college_class and gene.day == day]
                day_gaps = 0

                for gene in class_day_genes:
                    # Check if the gene has been already scored
                    if all(gene != apg for apg in already_scored_genes):
                        same_subject_genes = [ts for ts in class_day_genes if ts.subject == gene.subject]

                        already_scored_genes += same_subject_genes
                        day_gaps += self.get_number_of_gaps(same_subject_genes)

                if debug:
                    day_gaps = 0

                # More gaps, less score
                score += math.floor(self.s4_score / pow(day_gaps + 1, 2))

        return score

    # Soft condition - There should be no gaps in the class schedule.
    def s5(self, candidate, college_classes, debug = False):
        score = 0
        
        for college_class in college_classes:
            for day in range(5):
                class_day_subjects = [gene for gene in candidate.calendar if gene.day == day and gene.subject.college_class == college_class]                
                gaps = self.get_number_of_gaps(class_day_subjects)
                
                if debug:
                    gaps = 0
                
                # More gaps, less score
                score += math.floor(self.s5_score / pow(gaps + 1, 2))

        return score

    # Soft condition - There are no gaps in the teacher's class schedule.
    def s6(self, candidate, teacher_list, debug = False):
        score = 0

        for teacher in teacher_list:
            for day in range(5):
                teacher_day_subjects = [gene for gene in candidate.calendar if gene.day == day and gene.subject.teacher == teacher]
                gaps = self.get_number_of_gaps(teacher_day_subjects)

                if debug:
                    gaps = 0
                    
                # More gaps, less score
                score += math.floor(self.s5_score / pow(gaps + 1, 2))

        return score

    # Returns the number of gaps found into the subjects given by parameter
    def get_number_of_gaps(self, subjects):
        number_of_gaps = 0

        # If there is no subject for the current day, do not penalize
        if (not subjects):
            return 0

        # Sort subjects by hour
        subjects.sort(key = lambda ds: ds.hour)

        previous_hour = 0
        for subject in subjects:
            if previous_hour > 0:
                time_difference = subject.hour - previous_hour
                if time_difference > 1:
                    # Penalty is proportional to the number of hours of the gap
                    number_of_gaps += time_difference
            
            previous_hour = subject.hour

        return number_of_gaps

    # Returns the maximum fitness possible
    def get_max_possible_fitness(self, college_classes, teacher_list, candidate):
        if self.max_possible_score > 0:
            # Get value from cache (max_possible_score always will be the same)
            return self.max_possible_score

        score = self.s1(candidate, college_classes, True)
        score += self.s2(candidate, teacher_list, True)
        score += self.s3(candidate, college_classes, True)
        score += self.s4(candidate, college_classes, True)
        score += self.s5(candidate, college_classes, True)
        score += self.s6(candidate, teacher_list, True)

        self.max_possible_score = score

        print(f"Max possible fitness is {score}")

        return self.max_possible_score
        