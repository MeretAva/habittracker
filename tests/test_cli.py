"""Unit Tests covering the CLI."""

import pytest
from click.testing import CliRunner
from src.cli.cli import cli
import os
import tempfile


@pytest.fixture
def runner():

    return CliRunner()


@pytest.fixture
def temp_db():

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    yield db_path
    if os.path.exists(db_path):
        os.unlink(db_path)


def test_cli_help(runner):

    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "HabitTracker CLI" in result.output


def test_add_habit_interactive(runner):

    # Simulate user input: name, description, periodicity choice
    user_input = "TestHabit\nTest description\n1\n"
    result = runner.invoke(cli, ["add"], input=user_input)
    assert result.exit_code == 0
    assert "Added habit" in result.output


def test_analytics_list(runner):

    result = runner.invoke(cli, ["analytics", "list"])
    assert result.exit_code == 0


def test_analytics_overview(runner):

    result = runner.invoke(cli, ["analytics", "overview"])
    assert result.exit_code == 0


def test_analytics_daily_habits(runner):

    result = runner.invoke(cli, ["analytics", "daily-habits"])
    assert result.exit_code == 0


def test_analytics_weekly_habits(runner):

    result = runner.invoke(cli, ["analytics", "weekly-habits"])
    assert result.exit_code == 0


def test_add_command_help(runner):

    result = runner.invoke(cli, ["add", "--help"])
    assert result.exit_code == 0
    assert "Add a new habit" in result.output


def test_interactive_commands_exist(runner):

    # Test that commands exist and show help when run without input
    commands = ["add", "complete", "remove", "status"]

    for command in commands:
        result = runner.invoke(cli, [command, "--help"])
        assert result.exit_code == 0
        assert (
            "interactive" in result.output.lower() or command in result.output.lower()
        )


def test_complete_command_no_habits(runner):
    """Test complete command when no habits exist."""
    result = runner.invoke(cli, ["complete"])
    assert result.exit_code == 0
    assert "No habits found to complete" in result.output


def test_remove_command_no_habits(runner):
    """Test remove command when no habits exist."""
    result = runner.invoke(cli, ["remove"])
    assert result.exit_code == 0
    assert "No habits found to remove" in result.output


def test_status_command_no_habits(runner):
    """Test status command when no habits exist."""
    result = runner.invoke(cli, ["status"])
    assert result.exit_code == 0
    assert "No habits found" in result.output


def test_complete_command_with_habits(runner):
    """Test complete command with existing habits."""
    # First add a habit
    user_input = "TestHabit\nTest description\n1\n"
    runner.invoke(cli, ["add"], input=user_input)

    # Then test complete with cancel (0)
    complete_input = "0\n"  # Cancel
    result = runner.invoke(cli, ["complete"], input=complete_input)
    assert result.exit_code == 0
    assert "Cancelled" in result.output


def test_remove_command_with_habits(runner):
    """Test remove command with existing habits."""
    # First add a habit
    user_input = "TestHabit\nTest description\n1\n"
    runner.invoke(cli, ["add"], input=user_input)

    # Then test remove with cancel (0)
    remove_input = "0\n"  # Cancel
    result = runner.invoke(cli, ["remove"], input=remove_input)
    assert result.exit_code == 0
    assert "Cancelled" in result.output


def test_status_command_with_habits(runner):
    """Test status command with existing habits."""
    # First add a habit
    user_input = "TestHabit\nTest description\n1\n"
    runner.invoke(cli, ["add"], input=user_input)

    # Then test status with cancel (0)
    status_input = "0\n"  # Cancel
    result = runner.invoke(cli, ["status"], input=status_input)
    assert result.exit_code == 0
    assert "Cancelled" in result.output


def test_analytics_longest_streak(runner):
    """Test analytics longest-streak command."""
    result = runner.invoke(cli, ["analytics", "longest-streak"])
    assert result.exit_code == 0
    assert "Longest streak" in result.output


def test_analytics_active_streaks(runner):
    """Test analytics active-streaks command."""
    result = runner.invoke(cli, ["analytics", "active-streaks"])
    assert result.exit_code == 0


def test_analytics_broken_habits(runner):
    """Test analytics broken-habits command."""
    result = runner.invoke(cli, ["analytics", "broken-habits"])
    assert result.exit_code == 0


def test_analytics_due_today(runner):
    """Test analytics due-today command."""
    result = runner.invoke(cli, ["analytics", "due-today"])
    assert result.exit_code == 0


def test_analytics_list_with_periodicity_filter(runner):
    """Test analytics list command with periodicity filters."""
    # Test all
    result = runner.invoke(cli, ["analytics", "list", "--periodicity", "all"])
    assert result.exit_code == 0

    # Test daily
    result = runner.invoke(cli, ["analytics", "list", "--periodicity", "daily"])
    assert result.exit_code == 0

    # Test weekly
    result = runner.invoke(cli, ["analytics", "list", "--periodicity", "weekly"])
    assert result.exit_code == 0


def test_analytics_habit_streak_missing_habit(runner):
    """Test analytics habit-streak command with non-existent habit."""
    result = runner.invoke(cli, ["analytics", "habit-streak", "NonExistentHabit"])
    assert result.exit_code == 0
    assert "not found" in result.output


def test_analytics_help(runner):
    """Test analytics group help."""
    result = runner.invoke(cli, ["analytics", "--help"])
    assert result.exit_code == 0
    assert "Analytics and insights" in result.output


def test_complete_habit_workflow(runner):
    """Test complete workflow: add habit, complete it."""
    # Add a habit
    add_input = "TestHabit\nTest description\n1\n"
    result = runner.invoke(cli, ["add"], input=add_input)
    assert result.exit_code == 0
    assert "Added habit" in result.output

    # Complete the habit (select habit 1)
    complete_input = "1\n"
    result = runner.invoke(cli, ["complete"], input=complete_input)
    assert result.exit_code == 0
    assert "Completed" in result.output


def test_add_weekly_habit(runner):
    """Test adding a weekly habit."""
    # Add weekly habit (choice 2)
    user_input = "WeeklyHabit\nWeekly description\n2\n"
    result = runner.invoke(cli, ["add"], input=user_input)
    assert result.exit_code == 0
    assert "Added habit 'WeeklyHabit' (weekly)" in result.output


def test_add_habit_invalid_periodicity_then_valid(runner):
    """Test adding habit with invalid periodicity choice then valid."""
    # Invalid choice (3) then valid choice (1)
    user_input = "TestHabit\nTest description\n3\n1\n"
    result = runner.invoke(cli, ["add"], input=user_input)
    assert result.exit_code == 0
    assert "Please enter 1 for daily or 2 for weekly" in result.output
    assert "Added habit" in result.output
