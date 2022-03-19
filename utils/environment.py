import numpy as np
from dataclasses import dataclass, asdict
from collections import Counter
from utils.data_types import Arm
from utils.state_repository import StateRepository

'''
Last update time: 2022-03-19
Updated by Geng, Minghong
'''


class Env(object):
    def __init__(self, load_repo=True):
        self.arms = [
            Arm('no-preference', 'no-frequency'),  # ALPHABETICAL = 0
            Arm('no-preference', 'frequency'),  # FREQ_ONLY = 1
            Arm('preference', 'no-frequency'),  # PREF_ONLY = 2
            Arm('preference', 'frequency')  # COMBINED = 3
        ]

        # todo: check whether these phis are set correctly
        self.phis = np.array([
            [0, 0, 1],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ]).T
        # try to include the state repository inside the environment
        self.repo = StateRepository(load_repository=load_repo)

    @property
    def cum_rewards(self):
        rewards = []
        for arm in self.arms:
            rewards.append(sum([res.reward for res in self.repo.responses if res.arm == arm]))
        return rewards

    @property
    def counts(self):
        c = Counter()
        c.update({arm: 0 for arm in self.arms})
        arms = map(lambda res: res.arm, self.repo.responses)
        c.update(arms)
        return [c[arm] for arm in self.arms]
# class BerTSAgent:  # the agent to select the arm to pull
#     def get_arm(self, counts, wins):
#         if 0 in counts:
#             return Env.arms[counts.index(0)]
#
#         model = pm.Model()
#         with model:
#             beta = pm.Normal('beta', mu=0, sigma=10, shape=3)
#             linpred = pm.math.dot(beta, Env.phis)
#             theta = pm.Deterministic('theta', 1 / (1 + pm.math.exp(-linpred)))
#             obs = pm.Binomial('obs', n=counts, p=theta, observed=wins)
#             trace = pm.sample(1000, chains=1)
#
#         sample = pm.sample_posterior_predictive(trace, samples=1, model=model, var_names=['theta'])
#         idx = np.argmax(sample['theta'])
#         return Env.arms[idx]
