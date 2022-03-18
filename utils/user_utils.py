import os
import json
import sys

from utils.config import Config
from db.user import User

DATA_DIR = "data"


def create_user(user_id):
    user = User(user_id)
    user.generate_frequencies()
    user.generate_preferences()
    user.set_mode(Config.ALPHABETICAL)
    user.set_vote(None)
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
    return os.path.exists(os.path.join(DATA_DIR, f"{user_id}.json"))


def save_user(user):
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    with open(os.path.join(DATA_DIR, f"{user.get_user_id()}.json"), "w") as output_file:
        json.dump(user_to_dict(user), output_file)


def load_user(user_id):
    if user_exists(user_id):
        with open(os.path.join(DATA_DIR, f"{user_id}.json")) as output_file:
            user = json.load(output_file)
            return dict_to_user(user)
    else:
        user = create_user(user_id)
        save_user(user)
        return user
