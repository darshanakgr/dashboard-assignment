import numpy as np

# create a list for each tile
# each tile has a name, priority, icon
tiles = [
    {"id": "account", "name": "Account", "priority": 1, "icon": "bi bi-piggy-bank"},
    {"id": "analytics", "name": "Analytics", "priority": 2, "icon": "bi bi-pie-chart"},
    {"id": "time_deposits", "name": "Time Deposits", "priority": 3, "icon": "bi bi-stopwatch"},
    {"id": "bill_payments", "name": "Bill Payments", "priority": 4, "icon": "bi bi-clipboard2-fill"},
    {"id": "transfer_funds", "name": "Transfer Funds", "priority": 5, "icon": "bi bi-arrow-up-circle"},
    {"id": "cards", "name": "Cards", "priority": 6, "icon": "bi bi-credit-card"},
    {"id": "transaction_history", "name": "Transaction History", "priority": 7, "icon": "bi-calendar-check"},
    {"id": "settings", "name": "Settings", "priority": 8, "icon": "bi bi-wrench"},
    {"id": "loan", "name": "Loan", "priority": 9, "icon": "bi bi-file-text"},
    {"id": "spending_limits", "name": "Spending Limits", "priority": 10, "icon": "bi bi-wallet"},
    # {"id": "token", "name": "Token", "priority": 11, "icon": "bi bi-file-text"},
    # {"id": "grio", "name": "GRIO", "priority": 12, "icon": "bi bi-file-text"},
    {"id": "insurance", "name": "Insurance", "priority": 13, "icon": "bi bi-file-text"},
    {"id": "investment", "name": "Investment", "priority": 14, "icon": "bi bi-file-text"}
]


class Config:
    ALPHABETICAL = 0
    CUSTOM = 1

    def __init__(self, n_tiles):
        self.__text_size = 20
        self.__icon_size = 40
        self.__frequencies = []
        self.__preferences = np.ones(n_tiles) * 3
        self.__n_tiles = n_tiles
        self.__mode = Config.ALPHABETICAL

        self.randomize_frequencies()
        self.randomize_preferences()

    def set_text_size(self, text_size):
        self.__text_size = text_size

    def get_text_size(self):
        return self.__text_size

    def set_icon_size(self, icon_size):
        self.__icon_size = icon_size

    def get_icon_size(self):
        return self.__icon_size

    def randomize_frequencies(self):
        self.__frequencies = np.random.randint(0, 100, self.__n_tiles)

    def randomize_preferences(self):
        self.__preferences = np.random.randint(0, 5, self.__n_tiles) + 1

    def set_preferences(self, preferences):
        self.__preferences = preferences

    def get_frequencies(self):
        return self.__frequencies

    def get_frequency(self, i):
        return self.__frequencies[i]

    def get_preferences(self):
        return self.__preferences

    def get_preference(self, i):
        return self.__preferences[i]

    def set_mode(self, mode):
        self.__mode = mode

    def get_mode(self):
        return self.__mode


cfg = Config(n_tiles=len(tiles))
