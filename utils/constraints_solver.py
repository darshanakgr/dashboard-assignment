from constraint import *
from itertools import product
import pulp

from utils.config import Config


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


def normalize(d: dict):
    v = d.values()
    vmax = max(v)
    vmin = min(v)
    for k in d.keys():
        d[k] = (d[k] - vmin) / (vmax - vmin)
    return d


def reorder_tiles(tiles_data, user):
    tiles = []
    frequencies = {}
    preferences = {}
    placeholders = []

    for i in range(len(tiles_data)):
        id = tiles_data[i]["id"]
        tiles.append(id)
        placeholders.append(i)
        frequencies[id] = user.get_frequency(i)
        preferences[id] = user.get_preference(i)

    normalize(frequencies)
    normalize(preferences)

    cs = list(product(tiles, placeholders))

    if user.get_mode() == Config.FREQ_ONLY:
        wf, wp = 1, 0
    elif user.get_mode() == Config.PREF_ONLY:
        wf, wp = 0, 1
    else:
        wf, wp = 0.5, 0.5

    costs = {(t, p): (wf * frequencies[t] + wp * preferences[t]) * p for t, p in cs}

    prob = pulp.LpProblem('LinearMenu', pulp.LpMinimize)

    x = pulp.LpVariable.dicts('x', cs, cat='Binary')

    # Each slot must be filled by exactly one command
    for p in placeholders:
        prob += pulp.lpSum([x[t, p] for t in tiles]) == 1

    # Each command must be assigned to exactly one slot
    for t in tiles:
        prob += pulp.lpSum([x[t, p] for p in placeholders]) == 1

    # Objective function
    objective = pulp.lpSum([costs[t, p] * x[t, p] for t, p in cs])
    prob += objective

    status = prob.solve()

    solution = {}

    for t, p in cs:
        if x[t, p].value() == 1:
            solution[t] = p

    tiles_data.sort(key=lambda x: solution[x["id"]])

    return tiles_data
