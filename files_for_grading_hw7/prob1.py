from funcs import return_att, same_list, add_comment
import numpy as np
from classes import problem
import random
import string


def var_inputs():
    return [0.4, 0.7, 1.524, 5.2, 9.6, 19.2, 30.1], [0.38707637398311073, 0.7233390285130801, 1.5236961311031048, 5.201400341240987, 9.547745291596849, 19.1827509207773, 30.057733077422224]


def inputs():
    return [random.uniform(1.0, 100.0) for i in range(100)]


def func_sol(period):
    return period**(2.0/3.0)


class prob1(problem):
    def __init__(self, module):
        super().__init__(module)

        self.add_prob_grade_and_comment(self.check_variables)
        self.add_prob_grade_and_comment(self.check_function)

        self.n = 2
        self.normalize_grade()

    def check_variables(self):
        def check_single_variable(var_name, var_value):
            var = return_att(self.module, var_name)
            if var_name == None:
                return 0, f'No variable named {var_name}.'

            if type(var_value) == type([]):
                if not same_list(var_value, var):
                    return 0.5, f'Variable {var_name} is not correct.'
            elif type(var_value) == type(np.array([])):
                if not np.array_equal(var, var_value):
                    return 0.5, f'Variable {var_name} is not correct.'
            else:
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

        var_inps = var_inputs()
        var_list = ['dist_actual', 'dist_calc']
        return check_multiple_variables(var_list, var_inps)

    def check_function(self):
        function_name = 'kepler_3rd'
        func = return_att(self.module, function_name)
        if func == None:
            return 0, f'No function named {function_name}.'

        inps = inputs()
        for inp in inps:
            try:
                result = func_sol(inp) == func(inp)
                if not result:
                    return 0.5, f'The function {function_name} did not return the right output.'

            except:
                return 0, f'The function {function_name} did not take the right input.'
        return 1, ''
