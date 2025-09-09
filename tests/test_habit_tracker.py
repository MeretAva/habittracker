import pytest
from src.models import Habit, Periodicity
from src.core import HabitTracker


@pytest.fixture
def tracker():
    return HabitTracker()


@pytest.fixture
def habit():
    return Habit("Read", "Read a book", Periodicity.DAILY)


def test_add_habit(tracker, habit):
    tracker.add_habit(habit)
    assert habit in tracker.habits


def test_remove_habit(tracker, habit):
    tracker.add_habit(habit)
    tracker.remove_habit(habit)
    assert habit not in tracker.habits


def test_get_habit_by_name(tracker, habit):
    tracker.add_habit(habit)
    found = tracker.get_habit_by_name("Read")
    assert found == habit


def test_list_habits(tracker, habit):
    tracker.add_habit(habit)
    habits = tracker.list_habits()
    assert len(habits) == 1
    assert habits[0].name == "Read"
