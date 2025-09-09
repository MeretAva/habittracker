import pytest
import os
from src.models import Habit, Periodicity
from src.data import DataManager


@pytest.fixture
def habits():
    return [
        Habit("Read", "Read a book", Periodicity.DAILY),
        Habit("Exercise", "Morning run", Periodicity.WEEKLY),
    ]


@pytest.fixture
def data_manager(tmp_path):
    # Use a temporary directory for test files
    return DataManager(str(tmp_path / "habits.json"))


def test_save_and_load_habits(data_manager, habits):
    for habit in habits:
        data_manager.save_habit(habit)
    loaded = data_manager.load_habits()
    assert len(loaded) == 2
    print(loaded)
    assert loaded[0].name == "Read"
    assert loaded[1].periodicity == Periodicity.WEEKLY


def test_save_creates_file(data_manager, habits):
    data_manager.save_habits(habits)
    assert os.path.exists(data_manager.filepath)
