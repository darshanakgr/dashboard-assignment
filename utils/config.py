class Config:
    ALPHABETICAL = 0
    FREQ_ONLY = 1
    PREF_ONLY = 2
    COMBINED = 3
    DATA_DIR = "data"
    N_TILES = 12
    TILES = [
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
        {"id": "insurance", "name": "Insurance", "priority": 13, "icon": "bi bi-file-text"},
        {"id": "investment", "name": "Investment", "priority": 14, "icon": "bi bi-file-text"}
    ]

    PRIMARY = [
        {"name": "Turquoise", "hex": "#1abc9c"},
        {"name": "Emerald", "hex": "#2ecc71"},
        {"name": "Peter River", "hex": "#3498db"},
        {"name": "Amethyst", "hex": "#9b59b6"},
        {"name": "Wet Asphalt", "hex": "#34495e"},
        {"name": "Sun Flower", "hex": "#f1c40f"},
        {"name": "Carrot", "hex": "#e67e22"},
        {"name": "Alizarin", "hex": "#e74c3c"},
        {"name": "Concrete", "hex": "#95a5a6"},
    ]

    SECONDARY = [
        {"name": "Green Sea", "hex": "#16a085"},
        {"name": "Nephritis", "hex": "#27ae60"},
        {"name": "Belize Hole", "hex": "#2980b9"},
        {"name": "Wisteria", "hex": "#8e44ad"},
        {"name": "Midnight Blue", "hex": "#2c3e50"},
        {"name": "Orange", "hex": "#f39c12"},
        {"name": "Pumpkin", "hex": "#d35400"},
        {"name": "Pink Glamour", "hex": "#ff7675"},
        {"name": "Asbestos", "hex": "#7f8c8d"}
    ]
