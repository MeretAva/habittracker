"""Unit Tests covering the HabitTracker Class."""

import pytest
from src.models import Habit, Periodicity
from src.core import HabitTracker
from datetime import datetime


@pytest.fixture
def habit(habits):
    return habits[0]


@pytest.fixture
def tracker():
    import tempfile
    import os

    # Create a temporary database file for this test
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
        temp_path = temp_file.name

    # Create tracker with temporary database
    tracker = HabitTracker(temp_path)
    # Clear any initial data that may have been loaded
    tracker.data_manager.clear_all_habits()
    # Clear in memory habits and reload from empty database
    tracker.habits.clear()
    tracker._load_habits()

    yield tracker  # Provide tracker to test

    # Cleanup after test completes
    try:
        os.unlink(temp_path)
    except (FileNotFoundError, PermissionError):
        pass  # File already deleted or in use


def test_add_habit(tracker, habit):
    tracker.add_habit(habit)
    assert habit in tracker.habits.values()


def test_remove_habit(tracker, habit):
    tracker.add_habit(habit)
    habit_id = habit.id
    result = tracker.remove_habit(habit_id)
    assert result is True
    assert habit_id not in tracker.habits


def test_get_habit_by_name(tracker, habit):
    tracker.add_habit(habit)
    found = tracker.get_habit_by_name("Read")
    assert found.name == habit.name


def test_get_all_habits(tracker, habit):
    tracker.add_habit(habit)
    habits = tracker.get_all_habits()
    assert len(habits) == 1
    assert habits[0].name == "Read"


def test_complete_habit(tracker, habit):
    habit.completions.clear()
    tracker.add_habit(habit)
    habit_id = habit.id
    initial_count = len(habit.completions)
    streak = tracker.complete_habit(habit_id)
    assert len(habit.completions) == initial_count + 1
    assert isinstance(streak, int)


def test_get_habits_by_periodicity(tracker, habits):
    tracker.add_habit(habits[0])
    tracker.add_habit(habits[1])
    tracker.add_habit(habits[3])

    daily_habits = tracker.get_habits_by_periodicity(Periodicity.DAILY)
    weekly_habits = tracker.get_habits_by_periodicity(Periodicity.WEEKLY)

    assert len(daily_habits) == 2
    assert len(weekly_habits) == 1
    assert habits[0] in daily_habits
    assert habits[1] in daily_habits
    assert habits[3] in weekly_habits


def test_get_longest_streak_all_habits(tracker, habits):
    tracker.add_habit(habits[0])
    tracker.add_habit(habits[3])
    longest_streak = tracker.get_longest_streak_all_habits()
    assert isinstance(longest_streak, int)
    assert longest_streak > 0


def test_get_longest_streak_empty_tracker(tracker):
    assert tracker.get_longest_streak_all_habits() == 0
