import numpy as np
from utils.config import Config


class User:
    def __init__(self, user_id):
        self.__frequencies = []
        self.__preferences = np.ones(Config.N_TILES) * 3
        self.__mode = Config.ALPHABETICAL
        self.__user_id = user_id
        self.__vote = None

    def generate_frequencies(self):
        frequencies = np.random.randint(0, 100, Config.N_TILES)
        self.__frequencies = frequencies.tolist()

    def generate_preferences(self):
        preferences = np.random.randint(0, 5, Config.N_TILES) + 1
        self.__preferences = preferences.tolist()

    def set_frequencies(self, frequencies):
        self.__frequencies = frequencies

    def get_frequency(self, i):
        return self.__frequencies[i]

    def get_frequencies(self):
        return self.__frequencies

    def set_preferences(self, preferences):
        self.__preferences = preferences

    def get_preferences(self):
        return self.__preferences

    def get_preference(self, i):
        return self.__preferences[i]

    def set_mode(self, mode):
        self.__mode = mode

    def get_mode(self):
        return self.__mode

    def get_user_id(self):
        return self.__user_id

    def set_vote(self, vote):
        self.__vote = vote

    def get_vote(self):
        return self.__vote
