""" "Unit Tests covering the Analytics Functionality."""

import pytest
from datetime import datetime, timedelta
from src.analytics import (
    calculate_current_streak,
    calculate_longest_streak,
    get_all_habits,
    get_habits_by_periodicity,
    get_longest_streak_all_habits,
    get_longest_streak_for_habit,
)
from src.models import Habit, Periodicity


class TestCalculateCurrentStreak:
    """Test current streak calculations for daily and weekly habits."""

    def test_empty_completions(self):
        """Test current streak with no completions."""
        assert calculate_current_streak([], "daily") == 0
        assert calculate_current_streak([], "weekly") == 0

    def test_daily_current_streak_consecutive(self):
        """Test daily current streak with consecutive completions."""
        today = datetime.now()
        completions = [
            today,
            today - timedelta(days=1),
            today - timedelta(days=2),
            today - timedelta(days=3),
        ]
        assert calculate_current_streak(completions, "daily") == 4

    def test_daily_current_streak_broken(self):
        """Test daily current streak with gap in completions."""
        today = datetime.now()
        completions = [
            today,
            today - timedelta(days=1),
            today - timedelta(days=3),  # Skipped days=2 here
            today - timedelta(days=4),
        ]
        assert calculate_current_streak(completions, "daily") == 2

    def test_daily_current_streak_no_today(self):
        """Test daily current streak when not completed today."""
        today = datetime.now()
        completions = [
            today - timedelta(days=1),
            today - timedelta(days=2),
        ]
        assert calculate_current_streak(completions, "daily") == 0

    def test_weekly_current_streak_consecutive(self):
        """Test weekly current streak with consecutive weeks."""
        today = datetime.now()
        # Get start of current week (Monday)
        days_since_monday = today.weekday()
        this_week = today - timedelta(days=days_since_monday)
        completions = [
            this_week,  # This week
            this_week - timedelta(weeks=1),  # Last week
            this_week - timedelta(weeks=2),  # 2 weeks ago
        ]
        assert calculate_current_streak(completions, "weekly") == 3

    def test_weekly_current_streak_broken(self):
        """Test weekly current streak with gap in weeks."""
        today = datetime.now()
        days_since_monday = today.weekday()
        this_week = today - timedelta(days=days_since_monday)
        completions = [
            this_week,  # This week
            this_week - timedelta(weeks=1),  # Last week
            this_week - timedelta(weeks=3),  # Gap: 3 weeks ago
        ]
        assert calculate_current_streak(completions, "weekly") == 2

    def test_invalid_periodicity(self):
        """Test with invalid periodicity returns 0."""
        today = datetime.now()
        completions = [today]
        assert calculate_current_streak(completions, "invalid") == 0


class TestCalculateLongestStreak:
    """Test longest streak calculations for daily and weekly habits."""

    def test_empty_completions(self):
        """Test longest streak with no completions."""
        assert calculate_longest_streak([], "daily") == 0
        assert calculate_longest_streak([], "weekly") == 0

    def test_daily_longest_streak_consecutive(self):
        """Test daily longest streak with consecutive days."""
        today = datetime.now()
        completions = [
            today - timedelta(days=0),
            today - timedelta(days=1),
            today - timedelta(days=2),
            today - timedelta(days=3),
            today - timedelta(days=4),
        ]
        assert calculate_longest_streak(completions, "daily") == 5

    def test_daily_longest_streak_with_gaps(self):
        """Test daily longest streak with gaps finding the longest sequence."""
        today = datetime.now()
        completions = [
            # First streak: 3 days
            today - timedelta(days=0),
            today - timedelta(days=1),
            today - timedelta(days=2),
            # Gap
            today - timedelta(days=5),
            today - timedelta(days=6),
            today - timedelta(days=7),
            today - timedelta(days=8),  # Second streak: 4 days (longest)
        ]
        assert calculate_longest_streak(completions, "daily") == 4

    def test_weekly_longest_streak_consecutive(self):
        """Test weekly longest streak with consecutive weeks."""
        today = datetime.now()
        days_since_monday = today.weekday()
        week_start = today - timedelta(days=days_since_monday)
        completions = [
            week_start,
            week_start - timedelta(weeks=1),
            week_start - timedelta(weeks=2),
        ]
        assert calculate_longest_streak(completions, "weekly") == 3

    def test_weekly_longest_streak_with_gaps(self):
        """Test weekly longest streak with gaps finding the longest sequence."""
        today = datetime.now()
        days_since_monday = today.weekday()
        week_start = today - timedelta(days=days_since_monday)
        completions = [
            # First streak: 2 weeks
            week_start,
            week_start - timedelta(weeks=1),
            # Gap
            week_start - timedelta(weeks=4),
            week_start - timedelta(weeks=5),
            week_start - timedelta(weeks=6),  # Second streak: 3 weeks (longest)
        ]
        assert calculate_longest_streak(completions, "weekly") == 3

    def test_single_completion(self):
        """Test longest streak with single completion."""
        today = datetime.now()
        completions = [today]
        assert calculate_longest_streak(completions, "daily") == 1
        assert calculate_longest_streak(completions, "weekly") == 1

    def test_invalid_periodicity(self):
        """Test with invalid periodicity returns 0."""
        today = datetime.now()
        completions = [today]
        assert calculate_longest_streak(completions, "invalid") == 0


class TestGetAllHabits:
    """Test get_all_habits function."""

    def test_empty_habits_list(self):
        """Test with empty habits list."""
        assert get_all_habits([]) == []

    def test_none_habits_list(self):
        """Test with None habits list."""
        assert get_all_habits(None) == []

    def test_returns_copy_of_habits(self):
        """Test that function returns a copy of the input list."""
        habits = [
            Habit("Test1", "Description1", Periodicity.DAILY),
            Habit("Test2", "Description2", Periodicity.WEEKLY),
        ]
        result = get_all_habits(habits)
        assert result == habits
        assert result is not habits  # Should be a different object

        # Modifying result shouldn't affect original
        result.append(Habit("Test3", "Description3", Periodicity.DAILY))
        assert len(habits) == 2
        assert len(result) == 3


class TestGetHabitsByPeriodicity:
    """Test get_habits_by_periodicity function."""

    @pytest.fixture
    def mixed_habits(self):
        """Create habits with different periodicities."""
        return [
            Habit("Daily1", "Description1", Periodicity.DAILY),
            Habit("Daily2", "Description2", Periodicity.DAILY),
            Habit("Weekly1", "Description3", Periodicity.WEEKLY),
            Habit("Weekly2", "Description4", Periodicity.WEEKLY),
            Habit("Daily3", "Description5", Periodicity.DAILY),
        ]

    def test_filter_daily_habits(self, mixed_habits):
        """Test filtering for daily habits."""
        daily_habits = get_habits_by_periodicity(mixed_habits, "daily")
        assert len(daily_habits) == 3
        for habit in daily_habits:
            assert habit.periodicity == Periodicity.DAILY

    def test_filter_weekly_habits(self, mixed_habits):
        """Test filtering for weekly habits."""
        weekly_habits = get_habits_by_periodicity(mixed_habits, "weekly")
        assert len(weekly_habits) == 2
        for habit in weekly_habits:
            assert habit.periodicity == Periodicity.WEEKLY

    def test_empty_habits_list(self):
        """Test with empty habits list."""
        assert get_habits_by_periodicity([], "daily") == []
        assert get_habits_by_periodicity([], "weekly") == []

    def test_no_matching_habits(self, mixed_habits):
        """Test when no habits match the periodicity."""
        # Filter for a periodicity that doesn't exist in our test data
        result = get_habits_by_periodicity(mixed_habits, "nonexistent")
        assert result == []


class TestGetLongestStreakAllHabits:
    """Test get_longest_streak_all_habits function."""

    def test_empty_habits_list(self):
        """Test with empty habits list."""
        assert get_longest_streak_all_habits([]) == 0

    def test_single_habit_with_completions(self):
        """Test with single habit with completions."""
        habit = Habit("Test", "Description", Periodicity.DAILY)
        today = datetime.now()
        habit.completions = [
            today,
            today - timedelta(days=1),
            today - timedelta(days=2),
        ]
        assert get_longest_streak_all_habits([habit]) == 3

    def test_multiple_habits_different_streaks(self):
        """Test with multiple habits having different streak lengths."""
        habit1 = Habit("Habit1", "Description1", Periodicity.DAILY)
        habit2 = Habit("Habit2", "Description2", Periodicity.DAILY)
        today = datetime.now()
        # Habit1 has streak of 2
        habit1.completions = [today, today - timedelta(days=1)]
        # Habit2 has streak of 5 (should be the maximum)
        habit2.completions = [
            today,
            today - timedelta(days=1),
            today - timedelta(days=2),
            today - timedelta(days=3),
            today - timedelta(days=4),
        ]

        assert get_longest_streak_all_habits([habit1, habit2]) == 5

    def test_habits_with_no_completions(self):
        """Test with habits that have no completions."""
        habits = [
            Habit("Habit1", "Description1", Periodicity.DAILY),
            Habit("Habit2", "Description2", Periodicity.WEEKLY),
        ]
        assert get_longest_streak_all_habits(habits) == 0


class TestGetLongestStreakForHabit:
    """Test get_longest_streak_for_habit function."""

    def test_habit_with_completions(self):
        """Test with habit that has completions."""
        habit = Habit("Test", "Description", Periodicity.DAILY)
        today = datetime.now()
        habit.completions = [
            today,
            today - timedelta(days=1),
            today - timedelta(days=2),
            today - timedelta(days=3),
        ]
        assert get_longest_streak_for_habit(habit) == 4

    def test_habit_with_no_completions(self):
        """Test with habit that has no completions."""
        habit = Habit("Test", "Description", Periodicity.DAILY)
        assert get_longest_streak_for_habit(habit) == 0

    def test_weekly_habit_with_completions(self):
        """Test with weekly habit."""
        habit = Habit("Test", "Description", Periodicity.WEEKLY)
        today = datetime.now()
        days_since_monday = today.weekday()
        week_start = today - timedelta(days=days_since_monday)
        habit.completions = [
            week_start,
            week_start - timedelta(weeks=1),
            week_start - timedelta(weeks=2),
        ]
        assert get_longest_streak_for_habit(habit) == 3


class TestAnalyticsIntegration:
    """Integration tests using analytics functions with real habit data."""

    @pytest.fixture
    def habits_with_streaks(self):
        """Create habits with specific completion patterns for testing."""
        today = datetime.now()
        # Daily habit with perfect 7-day streak
        daily_habit = Habit("Daily Exercise", "30 min workout", Periodicity.DAILY)
        daily_habit.completions = [today - timedelta(days=i) for i in range(7)]
        # Weekly habit with 3-week streak
        days_since_monday = today.weekday()
        week_start = today - timedelta(days=days_since_monday)
        weekly_habit = Habit("Weekly Cleaning", "Deep clean house", Periodicity.WEEKLY)
        weekly_habit.completions = [week_start - timedelta(weeks=i) for i in range(3)]
        return [daily_habit, weekly_habit]

    def test_analytics_integration(self, habits_with_streaks):
        """Test that all analytics functions work together correctly."""
        daily_habit, weekly_habit = habits_with_streaks
        # Test individual habit streaks
        assert get_longest_streak_for_habit(daily_habit) == 7
        assert get_longest_streak_for_habit(weekly_habit) == 3
        # Test overall maximum streak
        assert get_longest_streak_all_habits(habits_with_streaks) == 7
        # Test filtering by periodicity
        daily_habits = get_habits_by_periodicity(habits_with_streaks, "daily")
        weekly_habits = get_habits_by_periodicity(habits_with_streaks, "weekly")
        assert len(daily_habits) == 1
        assert len(weekly_habits) == 1
        assert daily_habits[0].name == "Daily Exercise"
        assert weekly_habits[0].name == "Weekly Cleaning"
        # Test get_all_habits
        all_habits = get_all_habits(habits_with_streaks)
        assert len(all_habits) == 2
        assert all_habits[0].name in ["Daily Exercise", "Weekly Cleaning"]
        assert all_habits[1].name in ["Daily Exercise", "Weekly Cleaning"]
