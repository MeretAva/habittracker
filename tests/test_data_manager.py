"""Unit Tests covering the DataManager Class."""

import pytest
import tempfile
import os
from datetime import datetime, timedelta
from src.models import Habit, Periodicity
from src.data import DataManager


@pytest.fixture
def data_manager():
    """Create a DataManager with temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
        temp_path = temp_file.name

    dm = DataManager(temp_path)
    yield dm

    # Cleanup
    try:
        os.unlink(temp_path)
    except (FileNotFoundError, PermissionError):
        pass


@pytest.fixture
def sample_habit(habits):
    """Use a habit from fixtures but clear completions for clean
    testing."""
    habit = habits[0]  # "Read" habit
    habit.completions = []  # Clear completions for database testing
    habit.id = None  # Clear ID so database can assign new one
    return habit


def test_create_database_tables(data_manager):
    """Test that database tables are created properly."""
    # Tables should be created during initialisation
    import sqlite3

    with sqlite3.connect(data_manager.db_path) as conn:
        cursor = conn.cursor()

        # Check habits table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='habits'"
        )
        assert cursor.fetchone() is not None

        # Check completions table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='completions'"
        )
        assert cursor.fetchone() is not None


def test_insert_habit(data_manager, sample_habit):
    """Test inserting a new habit."""
    habit_id = data_manager.insert_habit(sample_habit)

    assert isinstance(habit_id, int)
    assert habit_id > 0

    # Verify it was inserted
    habits = data_manager.load_habits()
    assert len(habits) == 1
    assert habits[0]["name"] == "Read"
    assert habits[0]["description"] == "Read one chapter"
    assert habits[0]["periodicity"] == "daily"


def test_load_habits_empty_database(data_manager):
    """Test loading habits from empty database."""
    habits = data_manager.load_habits()
    assert habits == []


def test_load_habits_with_data(data_manager, sample_habit):
    """Test loading habits with existing data."""
    # Insert test habit
    habit_id = data_manager.insert_habit(sample_habit)

    # Load and verify
    habits = data_manager.load_habits()
    assert len(habits) == 1

    habit_data = habits[0]
    assert habit_data["id"] == habit_id
    assert habit_data["name"] == "Read"
    assert habit_data["periodicity"] == "daily"
    assert "created_date" in habit_data


def test_load_habit_by_id(data_manager, sample_habit):
    """Test loading a specific habit by ID."""
    habit_id = data_manager.insert_habit(sample_habit)

    # Load by ID
    habit_data = data_manager.load_habit_by_id(habit_id)
    assert habit_data is not None
    assert habit_data["id"] == habit_id
    assert habit_data["name"] == "Read"

    # Test non-existent ID
    assert data_manager.load_habit_by_id(999) is None


def test_insert_completion(data_manager, sample_habit):
    """Test inserting habit completions."""
    habit_id = data_manager.insert_habit(sample_habit)
    completion_time = datetime(2025, 1, 2, 8, 0, 0)

    # Insert completion
    data_manager.insert_completion(habit_id, completion_time)

    # Verify completion was saved
    completions = data_manager.load_completions(habit_id)
    assert len(completions) == 1
    assert completions[0] == completion_time


def test_load_completions_empty(data_manager, sample_habit):
    """Test loading completions for habit with no completions."""
    habit_id = data_manager.insert_habit(sample_habit)
    completions = data_manager.load_completions(habit_id)
    assert completions == []


def test_load_completions_multiple(data_manager, sample_habit):
    """Test loading multiple completions ordered by time."""
    habit_id = data_manager.insert_habit(sample_habit)

    # Insert completions in random order
    times = [
        datetime(2025, 1, 3, 8, 0, 0),
        datetime(2025, 1, 1, 8, 0, 0),
        datetime(2025, 1, 2, 8, 0, 0),
    ]

    for time in times:
        data_manager.insert_completion(habit_id, time)

    # Load and verify they're ordered
    completions = data_manager.load_completions(habit_id)
    assert len(completions) == 3

    # Should be ordered chronologically (ASC)
    assert completions[0] == datetime(2025, 1, 1, 8, 0, 0)
    assert completions[1] == datetime(2025, 1, 2, 8, 0, 0)
    assert completions[2] == datetime(2025, 1, 3, 8, 0, 0)


def test_delete_habit(data_manager, sample_habit):
    """Test deleting a habit and its completions."""
    habit_id = data_manager.insert_habit(sample_habit)

    # Add some completions
    data_manager.insert_completion(habit_id, datetime.now())
    data_manager.insert_completion(habit_id, datetime.now() - timedelta(days=1))

    # Verify habit and completions exist
    assert data_manager.load_habit_by_id(habit_id) is not None
    assert len(data_manager.load_completions(habit_id)) == 2

    # Delete habit
    result = data_manager.delete_habit(habit_id)
    assert result is True

    # Verify habit and completions are deleted
    assert data_manager.load_habit_by_id(habit_id) is None
    assert data_manager.load_completions(habit_id) == []


def test_delete_nonexistent_habit(data_manager):
    """Test deleting a habit that doesn't exist."""
    result = data_manager.delete_habit(999)
    assert result is False


def test_multiple_habits_isolation(data_manager):
    """Test that multiple habits and their completions are properly isolated."""
    # Create two habits
    habit1 = Habit("Read", "Read daily", Periodicity.DAILY)
    habit2 = Habit("Exercise", "Workout", Periodicity.WEEKLY)

    habit1_id = data_manager.insert_habit(habit1)
    habit2_id = data_manager.insert_habit(habit2)

    # Add completions to each
    data_manager.insert_completion(habit1_id, datetime(2025, 1, 1))
    data_manager.insert_completion(habit1_id, datetime(2025, 1, 2))
    data_manager.insert_completion(habit2_id, datetime(2025, 1, 1))

    # Verify completions are isolated
    habit1_completions = data_manager.load_completions(habit1_id)
    habit2_completions = data_manager.load_completions(habit2_id)

    assert len(habit1_completions) == 2
    assert len(habit2_completions) == 1

    # Delete one habit, verify the other is unaffected
    data_manager.delete_habit(habit1_id)

    assert data_manager.load_habit_by_id(habit1_id) is None
    assert data_manager.load_habit_by_id(habit2_id) is not None
    assert len(data_manager.load_completions(habit2_id)) == 1


def test_datetime_serialization(data_manager):
    """Test that datetime objects are properly serialized/deserialized."""
    created_date = datetime(2025, 1, 1, 10, 30, 45)
    completion_date = datetime(2025, 1, 2, 8, 15, 30)

    habit = Habit("Test", "Test habit", Periodicity.DAILY, created_date=created_date)
    habit_id = data_manager.insert_habit(habit)
    data_manager.insert_completion(habit_id, completion_date)

    # Load and verify dates are preserved
    habit_data = data_manager.load_habit_by_id(habit_id)
    completions = data_manager.load_completions(habit_id)

    # Note: created_date in database will be ISO string, but completions return datetime objects
    assert "2025-01-01T10:30:45" in habit_data["created_date"]
    assert completions[0] == completion_date
