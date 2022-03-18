from db.db_connection import get_db
from utils.user import load_user


def count_votes():
    users = get_db().execute('SELECT id FROM user').fetchall()
    votes = [0] * 4

    for u in users:
        user = load_user(user_id=u[0])
        votes[user.get_mode()] += 1 if user.get_vote() else 0

    return votes
