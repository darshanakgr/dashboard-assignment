from constraint import *


class TileCP(object):
    def __init__(self):
        self.text_size = [15, 20, 25, 30]
        self.icon_size = [20, 25, 30, 35, 40, 45, 50]

        self.problem = Problem()
        self.problem.reset()
        self.problem.addVariable('text_size', self.text_size)
        self.problem.addVariable('icon_size', self.icon_size)

    def get_solutions(self):
        return self.problem.getSolutions()

    def add_constraint(self, min_v, max_v, constraint='text_size'):
        self.problem.addConstraint(lambda v: min_v <= v <= max_v, [constraint])