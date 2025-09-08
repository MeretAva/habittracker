"""Defines the DataManager class to manage all database operations for HabitTracker."""

import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
from src.models import Habit, Periodicity


class DataManager:
    """Handles all database operations for HabitTracker."""

    def __init__(self, db_path: str = "database/habittracker.db"):
        self.db_path = db_path
        self.create_database()

    def create_database(self):
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Habits table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    periodicity TEXT NOT NULL CHECK (periodicity IN ('daily', 'weekly')),
                    created_date TEXT NOT NULL
                )
            """
            )

            # Completions table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completion_timestamp TEXT NOT NULL,
                    FOREIGN KEY (habit_id) REFERENCES habits (id)
                )
            """
            )

            conn.commit()

    def save_habit(self):
        pass

    def load_habits(self):
        pass

    def save_completion(self):
        pass

    def load_completions(self):
        pass

    def delete_habit(self):
        pass

    def close_connection(self):
        pass
