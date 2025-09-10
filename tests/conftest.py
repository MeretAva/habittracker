"""Pytest fixtures for providing reusable test data across all test modules."""

import pytest
from fixtures.test_data import create_predefined_habits


@pytest.fixture
def habits():
    """Provides a fresh list of predefined Habit objects for use in tests."""
    return create_predefined_habits()
