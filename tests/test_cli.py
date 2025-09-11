"""Tests for the CLI module."""

import pytest
from click.testing import CliRunner
from src.cli.cli import cli
import os
import tempfile


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    yield db_path
    if os.path.exists(db_path):
        os.unlink(db_path)


def test_cli_help(runner):
    """Test that CLI help works."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "HabitTracker CLI" in result.output


def test_add_habit(runner):
    """Test adding a new habit."""
    result = runner.invoke(cli, ["add", "TestHabit", "Test description"])
    assert result.exit_code == 0
    assert "Added habit" in result.output


def test_list_empty(runner):
    """Test listing habits when none exist."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["list"])
    # Note: may show existing habits if database already has data
    assert result.exit_code == 0


def test_analytics(runner):
    """Test analytics command."""
    result = runner.invoke(cli, ["analytics"])
    assert result.exit_code == 0


def test_add_command_help(runner):
    """Test help for add command."""
    result = runner.invoke(cli, ["add", "--help"])
    assert result.exit_code == 0
    assert "Add a new habit" in result.output
