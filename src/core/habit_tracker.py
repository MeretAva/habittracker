"""Defines the HabitTracker class to manage collections of habits and coordinate operations."""

from src.models import Habit, Periodicity
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from src.data import DataManager
from src.analytics import (
    get_all_habits,
    get_habits_by_periodicity,
    get_longest_streak_all_habits,
    get_longest_streak_for_habit,
)


class HabitTracker:
    """Manages a collection of Habit objects, allowing addition, removal, and tracking."""

    def __init__(self, db_path: str = "database/habittracker.db"):
        self.data_manager = DataManager(db_path)  # Database connection
        self.habits: Dict[int, Habit] = {}
        self._load_habits()

    def _load_habits(self) -> None:
        records = self.data_manager.load_habits()
        for record in records:
            habit = Habit(
                habit_id=record["id"],
                name=record["name"],
                description=record["description"],
                periodicity=Periodicity(record["periodicity"]),
                created_date=datetime.fromisoformat(record["created_date"]),
                completions=self.data_manager.load_completions(record["id"]),
            )
            self.habits[habit.id] = habit

    def add_habit(self, habit: Habit):
        if habit.id is None:
            habit_id = self.data_manager.insert_habit(habit)
            habit.id = habit_id
        self.habits[habit.id] = habit

    def remove_habit(self, habit_id: int) -> bool:
        if habit_id not in self.habits:
            return False
        self.data_manager.delete_habit(habit_id)
        del self.habits[habit_id]
        return True

    def get_habit_by_name(self, name: str) -> Optional[Habit]:
        for habit in self.habits.values():
            if habit.name == name:
                return habit
        return None

    def get_all_habits(self) -> List[Habit]:
        """Return a list of all currently tracked habits using analytics module."""
        return get_all_habits(list(self.habits.values()))

    def complete_habit(self, habit_id: int) -> Optional[int]:
        habit = self.habits.get(habit_id)
        if not habit:
            return None
        try:
            timestamp = datetime.now()
            # This will raise ValueError if already completed in same period
            habit.mark_completed(timestamp)
            self.data_manager.insert_completion(habit_id, timestamp)
            habit.completions.append(timestamp)
            return habit.get_current_streak()
        except ValueError as e:
            # Re-raise the validation error from mark_completed
            raise e

    def get_habits_by_periodicity(self, periodicity: Periodicity) -> List[Habit]:
        """Return habits with specified periodicity using analytics module."""
        return get_habits_by_periodicity(list(self.habits.values()), periodicity)

    def get_longest_streak_all_habits(self) -> int:
        """Return the longest streak across all habits using analytics module."""
        return get_longest_streak_all_habits(list(self.habits.values()))

    def get_longest_streak_for_habit(self, habit_id: int) -> Optional[int]:
        """Return longest streak for a specific habit using analytics module."""
        habit = self.habits.get(habit_id)
        if not habit:
            return None
        return get_longest_streak_for_habit(habit)
