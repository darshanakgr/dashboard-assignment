import numpy as np
import pymc3 as pm
from dataclasses import dataclass, asdict
from collections import Counter


class BerTSAgent:  # the agent to select the arm to pull
    def get_arm(self, env, counts, wins):
        if 0 in counts:
            return env.arms[counts.index(0)]

        model = pm.Model()
        with model:
            beta = pm.Normal('beta', mu=0, sigma=10, shape=3)
            linpred = pm.math.dot(beta, env.phis)
            theta = pm.Deterministic('theta', 1 / (1 + pm.math.exp(-linpred)))
            obs = pm.Binomial('obs', n=counts, p=theta, observed=wins)
            trace = pm.sample(1000, chains=1)

        sample = pm.sample_posterior_predictive(trace, samples=1, model=model, var_names=['theta'])
        idx = np.argmax(sample['theta'])
        return env.arms[idx]