"""Defines the DataManager class to manage all database operations for HabitTracker."""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from ..models import Habit, Periodicity
from pathlib import Path


class DataManager:
    """Handles all database operations for HabitTracker."""

    def __init__(self, db_path: str = "database/habittracker.db"):
        """
        Initialize DataManager with database path.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        # Create database directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
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

    def load_habit_by_id(self, habit_id: int) -> Optional[Dict[str, Any]]:
        """
        Load a specific habit by ID.

        Args:
            habit_id: ID of the habit to load

        Returns:
            Optional[Dict[str, Any]]: Habit dictionary or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, name, description, periodicity, created_date
                FROM habits
                WHERE id = ?
            """,
                (habit_id,),
            )

            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "periodicity": row[3],
                    "created_date": row[4],
                }
            return None

    def insert_habit(self, habit: Habit) -> int:
        """
        Insert a new habit into the database.

        Args:
            habit: Habit object to insert

        Returns:
            int: The auto-generated habit ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO habits (name, description, periodicity, created_date)
                VALUES (?, ?, ?, ?)
            """,
                (
                    habit.name,
                    habit.description,
                    habit.periodicity.value,  # Convert enum to string
                    habit.created_date.isoformat(),  # Convert datetime to ISO string
                ),
            )

            habit_id = cursor.lastrowid
            conn.commit()
            return habit_id

    def load_habits(self) -> List[Dict[str, Any]]:
        """
        Load all habits from the database.

        Returns:
            List[Dict[str, Any]]: List of habit dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, name, description, periodicity, created_date
                FROM habits
                ORDER BY created_date DESC
            """
            )

            rows = cursor.fetchall()
            habits = []

            for row in rows:
                habit_dict = {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "periodicity": row[3],
                    "created_date": row[4],
                }
                habits.append(habit_dict)

            return habits

    def insert_completion(self, habit_id: int, timestamp: datetime):
        """
        Insert a habit completion into the database.

        Args:
            habit_id: ID of the habit that was completed
            timestamp: When the habit was completed
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO completions (habit_id, completion_timestamp)
                VALUES (?, ?)
            """,
                (habit_id, timestamp.isoformat()),  # Convert datetime to ISO string
            )

            conn.commit()

    def load_completions(self, habit_id: int) -> List[datetime]:
        """
        Load all completions for a specific habit.

        Args:
            habit_id: ID of the habit

        Returns:
            List[datetime]: List of completion timestamps
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT completion_timestamp
                FROM completions
                WHERE habit_id = ?
                ORDER BY completion_timestamp ASC
            """,
                (habit_id,),
            )

            rows = cursor.fetchall()
            completions = []

            for row in rows:
                # Convert ISO string back to datetime
                timestamp = datetime.fromisoformat(row[0])
                completions.append(timestamp)

            return completions

    def delete_habit(self, habit_id: int) -> bool:
        """
        Delete a habit and all its completions from the database.

        Args:
            habit_id: ID of the habit to delete

        Returns:
            bool: True if habit was deleted, False if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Check if habit exists
            cursor.execute("SELECT id FROM habits WHERE id = ?", (habit_id,))
            if not cursor.fetchone():
                return False

            # Delete completions first (foreign key constraint)
            cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))

            # Delete the habit
            cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))

            conn.commit()
            return True

    def close_connection(self):
        """
        Close database connection.
        Note: We use context managers (with statements) so this is optional.
        """
        # Not needed since we use context managers, but kept for interface completeness
        pass

    def _format_timestamp(self, timestamp: datetime) -> str:
        """
        Helper method to format datetime as ISO string.

        Args:
            timestamp: Datetime to format

        Returns:
            str: ISO formatted timestamp
        """
        return timestamp.isoformat()

    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """
        Helper method to parse ISO timestamp string to datetime.

        Args:
            timestamp_str: ISO formatted timestamp string

        Returns:
            datetime: Parsed datetime object
        """
        return datetime.fromisoformat(timestamp_str)
