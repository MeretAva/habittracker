"""Defines the HabitTracker class to manage collections of habits and coordinate operations."""

from ..models import Habit, Periodicity
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from ..data import DataManager
from ..analytics import (
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
        """Load all habits from the database."""
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
        """
        Add a habit to the database.

        Args:
                habit: Habit object to insert

        """
        if habit.id is None:
            habit_id = self.data_manager.insert_habit(habit)
            habit.id = habit_id
        self.habits[habit.id] = habit

    def remove_habit(self, habit_id: int) -> bool:
        """
        Remove a habit from the database.

        Args:
            habit_id: ID of the habit to remove

        Returns:
            bool: True is habit was removes successfully, False if not
        """
        if habit_id not in self.habits:
            return False
        self.data_manager.delete_habit(habit_id)
        del self.habits[habit_id]
        return True

    def get_habit_by_name(self, name: str) -> Optional[Habit]:
        """
        Retrieve a single habit from the database.

        Args:
            name: name of the habit to get

        Returns:
            Habit: Habit object that was gotten
        """
        for habit in self.habits.values():
            if habit.name == name:
                return habit
        return None

    def get_all_habits(self) -> List[Habit]:
        """
        Return a list of all currently tracked habits using analytics module.

        Returns:
            List[Habit]: list of all habits from the database
        """
        return get_all_habits(list(self.habits.values()))

    def complete_habit(self, habit_id: int) -> Optional[int]:
        """
        Mark a habit as completed and insert the completion into the database.

        Args:
            habit_id: ID of the habit to complete

        Returns:
            int: current streak of the completed habit
        """
        habit = self.habits.get(habit_id)
        if not habit:
            return None
        try:
            timestamp = datetime.now()
            # This will raise ValueError if already completed in same period
            habit.mark_completed(timestamp)
            self.data_manager.insert_completion(habit_id, timestamp)
            return habit.get_current_streak()
        except ValueError as e:
            # Re-raise the validation error from mark_completed
            raise e

    def get_habits_by_periodicity(self, periodicity: Periodicity) -> List[Habit]:
        """Return habits with specified periodicity using analytics module.
        Args:
            periodicity: periodicity defining which habits to get

        Returns:
            List[Habit]: list of all habits with matching periodicity
        """
        return get_habits_by_periodicity(list(self.habits.values()), periodicity.value)

    def get_longest_streak_all_habits(self) -> int:
        """
        Return the longest streak across all habits using analytics module.

        Returns:
            int: longest streak of all currently tracked habits
        """
        return get_longest_streak_all_habits(list(self.habits.values()))
