import pytest
from src.models import Habit, Periodicity
from datetime import datetime, timedelta


@pytest.fixture
def habit():
    return Habit("Test", "Test habit", Periodicity.DAILY)


def test_initialization(habit):
    assert habit.name == "Test"
    assert habit.periodicity == Periodicity.DAILY
    assert isinstance(habit.created_date, datetime)
    assert len(habit.completions) == 0


def test_mark_completed(habit):
    habit.mark_completed()
    assert len(habit.completions) == 1


def test_get_current_streak(habit):
    today = datetime.now()
    habit.completions = [today - timedelta(days=2), today - timedelta(days=1), today]
    assert habit.get_current_streak() == 3


def test_get_longest_streak(habit):
    today = datetime.now()
    habit.completions = [
        today - timedelta(days=4),
        today - timedelta(days=2),
        today - timedelta(days=1),
        today,
    ]
    assert habit.get_longest_streak() == 3


def test_is_due(habit):
    assert habit.is_due()
    habit.mark_completed()
    assert not habit.is_due()


def test_is_broken(habit):
    assert not habit.is_broken()
    habit.completions = [datetime.now() - timedelta(days=2)]
    assert habit.is_broken()
