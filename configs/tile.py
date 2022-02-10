import numpy as np

# create a list for each tile
# each tile has a name, priority, icon
tiles = [
    {"id": "balance", "name": "Balance", "priority": 1, "icon": "bi bi-piggy-bank"},
    {"id": "analytics", "name": "Analytics", "priority": 2, "icon": "bi bi-pie-chart"},
    {"id": "time_deposits", "name": "Time Deposits", "priority": 3, "icon": "bi bi-stopwatch"},
    {"id": "bill_payments", "name": "Bill Payments", "priority": 4, "icon": "bi bi-clipboard2-fill"},
    {"id": "transfer_funds", "name": "Transfer Funds", "priority": 5, "icon": "bi bi-arrow-up-circle"},
    {"id": "cards", "name": "Cards", "priority": 6, "icon": "bi bi-credit-card"},
    {"id": "transaction_history", "name": "Transaction History", "priority": 7, "icon": "bi-calendar-check"},
    {"id": "settings", "name": "Settings", "priority": 8, "icon": "bi bi-wrench"},
    {"id": "loan", "name": "Loan", "priority": 9, "icon": "bi bi-file-text"},
    {"id": "spending_limits", "name": "Spending Limits", "priority": 10, "icon": "bi bi-wallet"},
    {"id": "token", "name": "Token", "priority": 11, "icon": "bi bi-file-text"},
    {"id": "grio", "name": "GRIO", "priority": 12, "icon": "bi bi-file-text"},
    {"id": "insurance", "name": "Insurance", "priority": 13, "icon": "bi bi-file-text"},
    {"id": "investment", "name": "Investment", "priority": 14, "icon": "bi bi-file-text"}
]

class Config:
    def __init__(self) -> None:
        self.__text_size = 20
        self.__icon_size = 40
        
    def set_text_size(self, text_size):
        self.__text_size = text_size
        
    def get_text_size(self):
        return self.__text_size
    
    def set_icon_size(self, icon_size):
        self.__icon_size = icon_size
        
    def get_icon_size(self):
        return self.__icon_size






    