"""Pytest fixtures for providing reusable test data across all test modules."""

import pytest
from fixtures.test_data import predefined_habits


@pytest.fixture
def habits():
    """Provides a list of predefined Habit objects for use in tests."""
    return predefined_habits
