import pytest
from datetime import datetime, timedelta
from src.models import Periodicity


@pytest.mark.usefixtures("habits")
def test_initialization(habits):
    habit = habits[0]
    assert habit.name == "Read"
    assert habit.periodicity == Periodicity.DAILY
    assert isinstance(habit.created_date, datetime)
    assert isinstance(habit.completions, list)


def test_mark_completed(habits):
    habit = habits[1]
    initial_count = len(habit.completions)
    habit.mark_completed()
    assert len(habit.completions) == initial_count + 1


def test_is_due(habits):
    habit = habits[2]
    # Remove all completions to simulate a new habit
    habit.completions.clear()
    assert habit.is_due()
    habit.mark_completed()
    assert not habit.is_due()


def test_is_broken(habits):
    habit = habits[3]
    # Remove all completions and set created_date to 2 weeks ago
    habit.completions.clear()
    habit.created_date = datetime.now() - timedelta(days=15)
    assert habit.is_broken()
    # Add a recent completion
    habit.mark_completed()
    assert not habit.is_broken()


def test_to_dict(habits):
    habit = habits[4]
    d = habit.to_dict()
    assert isinstance(d, dict)
    assert "name" in d
    assert "description" in d
    assert "periodicity" in d
    assert "created_date" in d
    assert "completions" in d
