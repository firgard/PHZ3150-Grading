from funcs import return_att, same_list
import numpy as np
from classes import problem

def piston(V, P0, V0, T0, gamma):
    P = P0*(V0/V)**gamma
    T = P * V * T0 / (P0 * V0)

    return np.transpose(([P, V, T]))


class prob3(problem):
    def __init__(self, module):
        super().__init__(module)

        V = np.linspace(1, 0.1, 100)
        P0 = 1
        V0 = 1
        T0 = 300
        gamma = 1.4

        variables = [V, P0, V0, T0, gamma]

        self.add_prob_grade_and_comment(self.grade_functions(['piston'], [piston], [variables]))

        self.n = 1
        self.normalize_grade()
