"""
Analytics module for HabitTracker.
Implements analytics functionality using functional programming paradigms.
All functions are pure functions with no side effects.
"""

from datetime import datetime, timedelta
from typing import List


def calculate_current_streak(completions: List[datetime], periodicity: str) -> int:
    """
    Calculate the current streak of consecutive completions up to today (daily) or this week (weekly).

    Args:
        completions: List of completion timestamps
        periodicity: String either "daily" or "weekly"

    Returns:
        int: The current streak count.
    """
    if not completions:
        return 0

    # Sort completions in descending order - most recent first
    sorted_completions = sorted([dt.date() for dt in completions], reverse=True)
    today = datetime.now().date()

    if periodicity == "daily":
        streak = 0
        expected_date = today

        for completion_date in sorted_completions:
            if completion_date == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)
            elif completion_date < expected_date:
                # Gap found, streak broken
                break

        return streak

    elif periodicity == "weekly":
        streak = 0
        # Find Monday of current week
        days_since_monday = today.weekday()
        current_week_start = today - timedelta(days=days_since_monday)

        expected_week_start = current_week_start

        for completion_date in sorted_completions:
            # Check if completion falls within expected week
            week_end = expected_week_start + timedelta(days=6)

            if expected_week_start <= completion_date <= week_end:
                streak += 1
                expected_week_start -= timedelta(weeks=1)
            elif completion_date < expected_week_start:
                # Gap found, streak broken
                break

        return streak

    return 0


def calculate_longest_streak(completions: List[datetime], periodicity: str) -> int:
    """
    Calculate the longest streak of consecutive completions (daily or weekly).

    Args:
        completions: List of completion timestamps
        periodicity: Either Periodicity.DAILY or Periodicity.WEEKLY

    Returns:
        int: The longest streak count.
    """

    if not completions:
        return 0

    completions = sorted([dt.date() for dt in completions])

    if periodicity == "daily":
        longest = current = 1
        for i in range(1, len(completions)):
            if (completions[i] - completions[i - 1]).days == 1:
                current += 1
            else:
                longest = max(longest, current)
                current = 1
        longest = max(longest, current)
        return longest

    elif periodicity == "weekly":
        # Get the week start (Monday) for each completion
        weeks = [dt - timedelta(days=dt.weekday()) for dt in completions]
        longest = current = 1
        for i in range(1, len(weeks)):
            if (weeks[i] - weeks[i - 1]).days == 7:
                current += 1
            else:
                longest = max(longest, current)
                current = 1
        longest = max(longest, current)
        return longest

    return 0


def get_all_habits(habits: List) -> List:
    """
    Return a list of all currently tracked habits.
    Pure function - simply returns the input list.

    Args:
        habits: List of Habit objects

    Returns:
        List: All habits (copy of input list)
    """
    return habits.copy() if habits else []


def get_habits_by_periodicity(habits: List, periodicity: str) -> List:
    """
    Return a list of all habits with the same periodicity.
    Pure function using filter.

    Args:
        habits: List of Habit objects
        periodicity: Periodicity to filter by (DAILY or WEEKLY)

    Returns:
        List: Habits matching the specified periodicity
    """
    return [habit for habit in habits if habit.periodicity.value == periodicity]


def get_longest_streak_all_habits(habits: List) -> int:
    """
    Return the longest run streak of all defined habits.
    Pure function using functional programming with map and max.

    Args:
        habits: List of Habit objects

    Returns:
        int: The longest streak found across all habits
    """
    if not habits:
        return 0

    # Use functional approach: map each habit to its longest streak, then find max
    streaks = [
        calculate_longest_streak(habit.completions, habit.periodicity.value)
        for habit in habits
    ]
    return max(streaks) if streaks else 0
