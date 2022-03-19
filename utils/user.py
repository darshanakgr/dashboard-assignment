import os
import json
# import sys
from utils.config import Config
from db.user import User
from utils.environment import Env
from utils.agent import BerTSAgent
'''
Last update time: 2022-03-19
Updated by Geng, Minghong
'''


def create_user(user_id):
    user = User(user_id)  # add the preference into the User object
    user.generate_frequencies()
    user.generate_preferences()
    # todo: the task of the contextual bandit problem is to change the mode
    # todo we need to pass in a mode that is generated by the model itself.
    env = Env(load_repo=False)
    agent = BerTSAgent()
    user_arm = agent.get_arm(env, env.counts, env.cum_rewards)
    arm_ind = env.arms.index(user_arm)
    user.set_mode(arm_ind)
    user.set_vote(None)  # todo Capture the vote after the clicking of user
    return user


def user_to_dict(user):
    return {
        "user_id": user.get_user_id(),
        "vote": user.get_vote(),
        "mode": user.get_mode(),
        "frequencies": user.get_frequencies(),
        "preferences": user.get_preferences()
    }


def dict_to_user(user_dict):
    user = User(user_dict["user_id"])
    user.set_frequencies(user_dict["frequencies"])
    user.set_preferences(user_dict["preferences"])
    user.set_vote(user_dict["vote"])
    user.set_mode(user_dict["mode"])
    return user


def user_exists(user_id):
    return os.path.exists(os.path.join(Config.DATA_DIR, f"{user_id}.json"))


def save_user(user):
    if not os.path.exists(Config.DATA_DIR):
        os.mkdir(Config.DATA_DIR)

    with open(os.path.join(Config.DATA_DIR, f"{user.get_user_id()}.json"), "w") as output_file:
        json.dump(user_to_dict(user), output_file)


def load_user(user_id):
    if user_exists(user_id):
        with open(os.path.join(Config.DATA_DIR, f"{user_id}.json")) as output_file:
            user = json.load(output_file)
            return dict_to_user(user)
    else:
        user = create_user(user_id)
        save_user(user)
        return user
