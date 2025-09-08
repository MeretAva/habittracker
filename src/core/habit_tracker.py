"""Defines the HabitTracker class to manage collections of habits and coordinate operations."""

from models import Habit, Periodicity
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from data import DataManager


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
                id=record["id"],
                name=record["name"],
                description=record["description"],
                periodicity=Periodicity(record["periodicity"]),
                created_date=datetime.fromisoformat(record["created_date"]),
                completions=self.data_manager.load_completions(record["id"]),
            )
            self.habits[habit.id] = habit

    def add_habit(self, name: str, description: str, periodicity: Periodicity) -> Habit:
        habit = Habit(
            id=None,
            name=name,
            description=description,
            periodicity=periodicity,
            created_date=datetime.now(),
            completions=[],
        )
        habit_id = self.data_manager.insert_habit(habit)
        habit.id = habit_id
        self.habits[habit_id] = habit
        return habit

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
            return list(self.habits.values())

    def complete_habit(self, habit_id: int) -> Optional[int]:
        habit = self.habits.get(habit_id)
        if not habit:
            return None
        timestamp = datetime.now()
        self.data_manager.insert_completion(habit_id, timestamp)
        habit.completions.append(timestamp)
        return habit.calculate_streak()


def save_habits(self) -> None:
    for habit in self.habits.values():
        self.data_manager.update_habit(habit)

    def initialize_predefined_habits(self) -> None:
        predefined = [
            ("Drink water", "Drink 2 liters of water", Periodicity.DAILY),
            ("Exercise", "30 minutes workout", Periodicity.DAILY),
            ("Read book", "Read 20 pages", Periodicity.DAILY),
            ("Weekly review", "Reflect on weekly goals", Periodicity.WEEKLY),
            ("Call family", "Catch up with loved ones", Periodicity.WEEKLY),
        ]
        for name, desc, per in predefined:
            habit = self.add_habit(name, desc, per)
            # Generate 4 weeks of example completions
            base = datetime.now() - timedelta(weeks=4)
            for i in range(28 if per == Periodicity.DAILY else 4):
                ts = base + (
                    timedelta(days=i)
                    if per == Periodicity.DAILY
                    else timedelta(weeks=i)
                )
                self.data_manager.insert_completion(habit.id, ts)
                habit.completions.append(ts)

    def get_habits_by_periodicity(self, periodicity: Periodicity) -> List[Habit]:
        return [
            habit for habit in self.habits.values() if habit.periodicity == periodicity
        ]
