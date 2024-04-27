from funcs import return_att, add_comment
import numpy as np
from classes import problem
from random import randint
import os


def inps():
    return 10, 10, 10, 15, 800

class solution:
    def __init__(self, a, b, c, gifts, paper):
        self.a = a
        self.b = b
        self.c = c
        self.gifts = gifts
        self.paper = paper
        
    def surface_area(self):
        return 2*(self.a*self.b + self.a*self.c + self.c*self.b)
    
    def volume(self):
        return self.a * self.b * self.c
    
    def enough_paper(self):
        return self.paper >= self.surface_area()
    
    def fits(self):
        return self.volume() >= self.gifts*25


class prob2(problem):
    def __init__(self, module):
        super().__init__(module)

        self.add_prob_grade_and_comment(self.grade_class)

        self.n = 1
        self.normalize_grade()

    def grade_class(self):
        class_grade, class_comment = 0, ''
        class_name = 'graduation_presents'
        att_names = ['a', 'b', 'c', 'gifts', 'paper']
        class_funcs = ['surface_area', 'volume', 'enough_paper', 'fits']

        def grade_class_function(class_obj, class_name, func_name, sol_class):
            f = return_att(class_obj, func_name)
            if f == None:
                return 0, f"Class {class_name} doesn't have {func_name} function."

            output = f()

            if output == getattr(sol_class, func_name)():
                return 1, ''
            return 0.5, f"Function  {func_name} doesn't return the right value."

        def grade_class_att(class_obj, class_name, att_name):
            f = return_att(class_obj, att_name)
            if f == None:
                return 0, f"Class {class_name} doesn't have {att_name} function."
            return 1, ''

        # Check if class exists
        c = return_att(self.module, class_name)
        if c == None:
            return 0, f'No class named {class_name}'


        inputs = inps()
        c_obj = c(*inputs)

        c_sol = solution(*inputs)

        # Check if the right attributes are there
        #temp_grade = 0
        #for att_name in att_names:
        #    grade, comment = grade_class_att(c_obj, class_name, att_name)
        #    temp_grade += grade
        #    class_comment = add_comment(class_comment, comment)

        #class_grade = temp_grade/len(att_names)

        # Check the functions in the class
        temp_grade = 0
        for class_func in class_funcs:
            grade, comment = grade_class_function(c_obj, class_name, class_func, c_sol)
            temp_grade += grade
            class_comment = add_comment(class_comment, comment)

        class_grade += temp_grade/len(class_funcs)

        #class_grade /= 2

        return class_grade, class_comment
