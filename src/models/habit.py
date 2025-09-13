"""Defines the Habit class for tracking habits and their completion streaks."""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from .periodicity import Periodicity


class Habit:
    """
    Represents a habit with a name, description, periodicity, creation date, and completion history.
    Provides methods to mark completions, check streaks, and determine if the habit is due or broken.
    """

    def __init__(
        self,
        name,
        description,
        periodicity,
        created_date=None,
        habit_id=None,
        completions=None,
    ):
        """
        Initialize a new Habit instance.

        Args:
            name (str): Name of the habit.
            description (str): Description of the habit.
            periodicity (Periodicity or str): How often the habit should be completed.
            created_date (datetime, optional): When the habit was created.
            habit_id (Any, optional): Unique identifier for the habit.
            completions (List, optional): List of all the times the habit has been completed.
        """
        if isinstance(periodicity, str):
            # Convert string to enum
            periodicity = Periodicity(periodicity)  # Raises ValueError if invalid
        elif not isinstance(periodicity, Periodicity):
            raise ValueError(
                "Periodicity must be 'daily', 'weekly', or Periodicity enum"
            )

        self.id = habit_id
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.created_date = created_date if created_date else datetime.now()
        self.completions = completions if completions is not None else []

    def mark_completed(self, timestamp: Optional[datetime] = None):
        """Mark the habit as completed at the given timestamp.
        Args: timestamp: When the habit was completed. Defaults to current time.
        Raises: ValueError: if habit already completed in the same period."""
        if timestamp is None:
            timestamp = datetime.now()

        # Check for existing completion in same period
        completion_date = timestamp.date()

        if self.periodicity == Periodicity.DAILY:
            # Check if completed today
            if any(comp.date() == completion_date for comp in self.completions):
                raise ValueError(f"Habit '{self.name}' already completed today")

        elif self.periodicity == Periodicity.WEEKLY:
            # Check if already completed this week
            days_since_monday = completion_date.weekday()
            week_start = completion_date - timedelta(days=days_since_monday)
            week_end = week_start + timedelta(days=6)

            if any(week_start <= comp.date() <= week_end for comp in self.completions):
                raise ValueError(f"Habit '{self.name}' already completed this week")

        # Add the completion to timestamp list
        self.completions.append(timestamp)

    def get_current_streak(self) -> int:
        """Calculate current streak using analytics module"""
        from ..analytics import calculate_current_streak

        return calculate_current_streak(self.completions, self.periodicity.value)

    def get_longest_streak(self) -> int:
        """Calculate longest streak using analytics module"""
        from ..analytics import calculate_longest_streak

        return calculate_longest_streak(self.completions, self.periodicity.value)

    def is_due(self) -> bool:
        """
        Check if the habit is due to be completed based on its periodicity.

        Returns:
        bool: True if the habit is due, False otherwise
        """
        if not self.completions:
            # No completions yet, so it's due
            return True

        # Get the most recent completion
        last_completion = max(self.completions)
        now = datetime.now()

        if self.periodicity == Periodicity.DAILY:
            # Due if last completion was not today
            return last_completion.date() < now.date()

        elif self.periodicity == Periodicity.WEEKLY:
            # Due if last completion was not in current week
            # Calculate start of current week (Monday)
            days_since_monday = now.weekday()
            start_of_week = now.date() - timedelta(days=days_since_monday)

            return last_completion.date() < start_of_week

        return False

    def is_broken(self) -> bool:
        """
        Check if the habit is broken based on its periodicity

        Returns:
            bool: True if the habit is broken, False otherwise.
        """
        if not self.completions:
            # No completions yet - check if we're past the first required period
            now = datetime.now()

            if self.periodicity == Periodicity.DAILY:
                # Broken if created more than 1 day ago and no completions
                return (now.date() - self.created_date.date()).days > 0

            elif self.periodicity == Periodicity.WEEKLY:
                # Broken if created more than 1 week ago and no completions
                return (now - self.created_date).days > 7

        # Get the most recent completion
        last_completion = max(self.completions)
        now = datetime.now()

        if self.periodicity == Periodicity.DAILY:
            # Broken if last completion was more than 1 day ago
            return (now.date() - last_completion.date()).days > 1

        elif self.periodicity == Periodicity.WEEKLY:
            # Broken if last completion was more than 1 week ago
            return (now - last_completion).days > 14  # 2 weeks = broken

        return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert the habit to a dictionary representation.
        Returns: Dict[str, Any]: Dictionary containing all habit data except the ID"""

        return {
            "name": self.name,
            "description": self.description,
            "periodicity": self.periodicity.value,  # Convert enum to string
            "created_date": self.created_date.isoformat(),  # Convert datetime to ISO string
            "completions": [
                completion.isoformat() for completion in self.completions
            ],  # Convert all datetimes to ISO strings
        }
