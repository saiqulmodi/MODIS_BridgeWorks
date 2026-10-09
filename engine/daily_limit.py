"""Daily answer limit shared by every way of answering questions for money.

A player may submit DAILY_ANSWER_LIMIT answers per calendar day, in any phase they choose.
The count lives in the save file under "daily_answers", not in the login session, so closing
the game, logging in again or registering a new name on the same device does not reset it.
It resets at local midnight.
"""
import datetime

DAILY_ANSWER_LIMIT = 25
KEY = "daily_answers"


def _today(today=None):
    return (today or datetime.date.today()).isoformat()


def _counter(data, today=None):
    day = _today(today)
    c = data.get(KEY)
    if not isinstance(c, dict) or c.get("date") != day:
        c = {"date": day, "count": 0}
        data[KEY] = c
    return c


def answers_used(data, today=None):
    return _counter(data, today)["count"]


def answers_left(data, today=None):
    return max(0, DAILY_ANSWER_LIMIT - answers_used(data, today))


def use_answer(data, today=None):
    """Count one answer. Returns False (and counts nothing) when today's limit is used up."""
    c = _counter(data, today)
    if c["count"] >= DAILY_ANSWER_LIMIT:
        return False
    c["count"] += 1
    return True
