# Imports good functions and the grading for each problem
# Problems here are examples and would need to be changed accordingly
from funcs import import_module, print_to_file, add_comment
from prob1 import prob1
from prob2 import prob2
from prob3 import prob3

# Homework class puts all the problems together and does all the grading
class homework:
    def __init__(self, module, p_points):
        self.module = module # Imported module (the notebook)
        self.p_points = p_points # Points for each problem
        self.p1 = prob1(self.module)
        self.p2 = prob2(self.module)
        self.p3 = prob3(self.module)

        # Adds the problems (p1, p2, p3) to a list
        self.probs = [getattr(self, f'p{i}') for i in range(1, len(p_points) + 1)]
        self.calculate_final_grade()
        self.get_final_comment()
        self.add_end_comment()

        print_to_file(self.final_grade, self.final_comment)

    def calculate_final_grade(self):
        self.final_grade = 0
        for prob, points in zip(self.probs, self.p_points):
            self.final_grade += prob.prob_grade * points

    def get_final_comment(self):
        self.final_comment = ''
        for n, prob in enumerate(self.probs, start = 1):
            self.final_comment = add_comment(self.final_comment, prob.prob_comment, f'Problem {n}')

    # Adds a comment at the end
    # TODO Add a specific comment for the last round of grading, so students know not to submit again
    def add_end_comment(self):
        if self.final_grade < sum(self.p_points):
            comment = "\nPlease try again, and if you need help please contact the TA or the professor, and resubmit your work once you're done."
        else:
            comment = 'Good job!'
        self.final_comment = add_comment(self.final_comment, comment)

try:
    module = import_module('module_for_grading.py')
except:
    print_to_file(0, 'Notebook did not compile without errors.')
    exit()

hw = homework(module, [30, 10, 15])
