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
