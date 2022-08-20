from models.evolutive.candidate import Candidate
from itertools import groupby
import csv


class ToCsv():

    def create_teachers_schedule_csv(result: Candidate()):
        teachers = groupby(result.calendar, lambda gene: gene.subject.teacher)   
        
        with open('teacher_schedule.csv', 'w') as f:
            write = csv.writer(f, delimiter =';')

            for teacher, _ in teachers:
                write.writerow(["", f"---- Schedule of { teacher.name } ----"])
                
                for hour in range(8, 17):
                    formatted_hour = f"{hour}:00"
                    row = [formatted_hour]

                    for day in range(5):
                        column = " - "
                        row_genes = [gene for gene in result.calendar if gene.hour == hour and gene.day == day and gene.subject.teacher == teacher]

                        if len(row_genes) > 1:
                            raise "Invalid calendar"

                        if row_genes:
                            column = f"{row_genes[0].subject.name} ({row_genes[0].subject.college_class.name})"

                        row.append(column)

                    write.writerow(row)
                    
                write.writerow(['\n\n\n'])

    def create_classes_schedule_csv(result: Candidate()):
        classes = groupby(result.calendar, lambda gene: gene.subject.college_class)   
        
        with open('class_schedule.csv', 'w') as f:
            write = csv.writer(f, delimiter =';')
    
            for college_class, _ in classes:
                write.writerow(["", f"---- Schedule of { college_class.name } ----"])
                
                for hour in range(college_class.availability.time_from, college_class.availability.time_to):
                    formatted_hour = f"{hour}:00"
                    row = [formatted_hour]

                    for day in range(5):
                        column = " - "
                        row_genes = [gene for gene in result.calendar if gene.hour == hour and gene.day == day and gene.subject.college_class == college_class]

                        if len(row_genes) > 1:
                            raise "Invalid calendar"

                        if row_genes:
                            column = f"{row_genes[0].subject.name} ({row_genes[0].subject.teacher.name})"

                        row.append(column)

                    write.writerow(row)
                    
                write.writerow(['\n\n\n'])
