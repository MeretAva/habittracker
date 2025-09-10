"""Analytics package: exposes analytics functionality for analyising habits."""

from .analytics import (
    calculate_current_streak,
    calculate_longest_streak,
    get_all_habits,
    get_habits_by_periodicity,
    get_longest_streak_all_habits,
    get_longest_streak_for_habit,
)

__all__ = [
    "calculate_current_streak",
    "calculate_longest_streak",
    "get_all_habits",
    "get_habits_by_periodicity",
    "get_longest_streak_all_habits",
    "get_longest_streak_for_habit",
]
