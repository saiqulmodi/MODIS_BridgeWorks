"""Answer limit per login, shared by every way of answering questions for money.

A player may submit LOGIN_ANSWER_LIMIT paid answers per login, in any phase they choose.
Logging in again (registering with the same name in the game, or starting the question
game again) gives a fresh LOGIN_ANSWER_LIMIT, so a student keeps earning by learning.
The count lives in the save file under "login_answers".
"""
LOGIN_ANSWER_LIMIT = 25
KEY = "login_answers"


def _counter(data):
    c = data.get(KEY)
    if not isinstance(c, dict):
        c = {"count": 0, "logins": 0}
        data[KEY] = c
    return c


def start_login(data):
    """A new login: the answer count starts again from 0."""
    c = _counter(data)
    c["count"] = 0
    c["logins"] = c.get("logins", 0) + 1


def answers_used(data):
    return _counter(data)["count"]


def answers_left(data):
    return max(0, LOGIN_ANSWER_LIMIT - answers_used(data))


def use_answer(data):
    """Count one answer. Returns False (and counts nothing) when this login's limit is used up."""
    c = _counter(data)
    if c["count"] >= LOGIN_ANSWER_LIMIT:
        return False
    c["count"] += 1
    return True
