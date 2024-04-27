from funcs import return_att, same_list
import numpy as np
from classes import problem

def my_circuit(sys_info, resistances, IV):
    if sys_info == 'series':
        R_tot = np.sum(resistances)
        V = R_tot * IV

        return R_tot, V
        
    elif sys_info == 'parallel':
        R_tot = 1/np.sum(1/resistances)
        I = IV / R_tot

        return R_tot, I
        
    else:
        print('Wrong input!')
        return None, None


class prob2(problem):
    def __init__(self, module):
        super().__init__(module)

        inp1 = ['series', np.array([5, 2, 7]), 10]
        inp2 = ['parallel', np.array([12, 5, 20]), 15]

        inps = [inp1, inp2]

        for inp in inps:
            self.add_prob_grade_and_comment(self.grade_functions(['my_circuit'], [my_circuit], [inp]))

        self.n = 2
        self.normalize_grade()
