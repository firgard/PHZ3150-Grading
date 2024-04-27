from funcs import return_att, same_list
import numpy as np
from classes import problem
import random
import string


def triathlon_times(sports, athletes_times):
    # Number of athletes
    n = len(athletes_times[:, 0])

    # Number of sports
    m = len(sports)

    # Array that will hold the total times for each athlete
    times = np.zeros(n)

    # Loops through each athlete
    for i in range(n):
        # Loops through each sport
        for j in range(m):
            t = sports[j] / athletes_times[i, j+1]
            times[i] += t

    # Gets the index of the winner/loser (index = ID - 1)
    first = np.argmin(times)
    last = np.argmax(times)

    return first + 1, times[first]/3600, last + 1, times[last]/3600

def triathlon_times_dict(sports_dict, athletes_times_dict):
    # Number of athletes
    n = len(athletes_times_dict)

    # Array to store the times
    times = np.zeros(n)

    # Loops trough the athletes
    for x, i in enumerate(athletes_times_dict):
        # Loops through the sports
        for y, j in enumerate(sports_dict):
            t = sports_dict[j] / athletes_times_dict[i][y]
            times[x] += t

    # Gets the index of the winner/loser (index = ID - 1)
    first = np.argmin(times)
    last = np.argmax(times)

    return first + 1, times[first]/3600, last + 1, times[last]/3600


class prob1(problem):
    def __init__(self, module):
        super().__init__(module)

        sports = np.array([1500, 40000, 10000])

        athletes_times = np.zeros((6, 4))
        athletes_times[:, 0] = np.arange(1, 7)
        athletes_times[:, 1] = np.array([1.204, 1.212, 1.14, 1.12, 1.24, 1.201])
        athletes_times[:, 2] = np.array([6.6, 6.5, 6.6, 6.2, 5.6, 6])
        athletes_times[:, 3] = np.array([0.32, 0.36, 0.38, 0.38, 0.4, 0.3])

        sports_dict = {'swimming': 1500, 'cycling': 40000, 'running': 10000}

        athletes_times_dict = {1: [1.204, 6.6, 0.32],
                               2: [1.212, 6.5, 0.36],
                               3: [1.14, 6.6, 0.38],
                               4: [1.12, 6.2, 0.38],
                               5: [1.24, 5.6, 0.4],
                               6: [1.201, 6.0, 0.3]}

        self.add_prob_grade_and_comment(self.grade_variables(['sports', 'sports_dict', 'athletes_times', 'athletes_times_dict'], [sports, sports_dict, athletes_times, athletes_times_dict]))
        self.add_prob_grade_and_comment(self.grade_functions(['triathlon_times', 'triathlon_times_dict'], [triathlon_times, triathlon_times_dict], [[sports, athletes_times], [sports_dict, athletes_times_dict]]))

        self.n = 2
        self.normalize_grade()
