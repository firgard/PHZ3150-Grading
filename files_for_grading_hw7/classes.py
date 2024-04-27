from funcs import return_att, same_list, add_comment
import numpy as np

class problem:
    def __init__(self, module):
        self.module = module
        self.n = 0
        self.prob_grade, self.prob_comment = 0, ''

    def add_prob_grade_and_comment(self, func):
        grade, comment = func()
        self.prob_grade += grade
        self.prob_comment = add_comment(self.prob_comment, comment)

    def normalize_grade(self):
        self.prob_grade /= self.n

    def check_single_variable(self, var_name, var_value):
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

    def check_multiple_variables(self, var_names, var_values):
        grade, comment = 0, ''
        for v_name, v_val in zip(var_names, var_values):
            g, c = self.check_single_variable(v_name, v_val)
            grade += g
            comment = add_comment(comment, c)

        return grade/len(var_names), comment

    def grade_functions():
        pass

    def grade_classes(self, class_name, atts_names = None, init_atts_vals = None, funcs = None, exp_outputs = None):
        def grade_class_function(self, func_name, input = None, exp_output = None):
            f = return_att(self.class_obj, func_name)
            if f == None:
                return 0, f"Class {self.class_name} doesn't have {func_name} function."
            if input == None:
                output = f()
            else:
                output = f(*input)

            if output == exp_output:
                return 1, ''
            return 0.5, f"Function  {func_name} doesn't return the right value."

        def grade_class_att(self, att_name, exp_val):
            f = return_att(self.class_obj, att_name)
            if f == None:
                return 0, f"Class {self.class_name} doesn't have {att_name} function."

            if f == exp_val:
                return 1, ''
            return 0.5, f"Function  {att_name} doesn't return the right value."

        c = return_att(self.module, class_name)
        if c == None:
            return 0, f'No class named {class_name}'

        self.class_obj = c(*init_atts_vals)
        self.class_name = class_name

        
    def grade_class_object(self):
        pass
