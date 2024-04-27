from funcs import return_att, add_comment
import numpy as np
from classes import problem
import random
import string

class prob4(problem):
    def __init__(self, module):
        super().__init__(module)

        self.add_prob_grade_and_comment(self.check_variables)

        self.n = 1
        self.normalize_grade()

    def check_variables(self):
        def check_single_variable(var_name, var_value):
            var = return_att(self.module, var_name)
            if var_name == None:
                return 0, f'No variable named {var_name}.'

            if var != var_value:
                return 0.5, f'Variable {var_name} is not correct.'

            return 1, ''

        def check_multiple_variables(var_names, var_values):
            grade, comment = 0, ''
            for v_name, v_val in zip(var_names, var_values):
                g, c = check_single_variable(v_name, v_val)
                grade += g
                comment = add_comment(comment, c)

            return grade/len(var_names), comment

        var_values = [25, 13]
        var_list = ['max_val', 'mean_val']
        return check_multiple_variables(var_list, var_values)
