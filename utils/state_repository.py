from utils.data_types import Response


class StateRepository:
    def __init__(self, load_repository=None):
        if load_repository:
            self.responses = [0,1,3,2]  # todo: load the local response file
        else:
            self.responses = []
    # @property
    # def cum_rewards(self):
    #     rewards = []
    #     for arm in Env.arms:
    #         rewards.append(sum([res.reward for res in self.responses if res.arm == arm]))
    #     return rewards
    #
    # @property
    # def counts(self):
    #     c = Counter()
    #     c.update({arm: 0 for arm in Env.arms})
    #     arms = map(lambda res: res.arm, self.responses)
    #     c.update(arms)
    #     return [c[arm] for arm in Env.arms]

    def append(self, response: Response):
        self.responses.append(response)
