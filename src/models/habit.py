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
        self, name, description, periodicity, created_date=None, habit_id=None
    ):
        """
        Initialize a new Habit instance.

        Args:
            name (str): Name of the habit.
            description (str): Description of the habit.
            periodicity (Periodicity or str): How often the habit should be completed.
            created_date (datetime, optional): When the habit was created.
            habit_id (Any, optional): Unique identifier for the habit.
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
        self.completions = []

    def mark_completed(self, timestamp: Optional[datetime] = None):
        """Mark the habit as completed at the given timestamp.
        Args: timestamp: When the habit was completed. Defaults to current time."""
        if timestamp is None:
            timestamp = datetime.now()

        # Add the completion to timestamp list
        self.completions.append(timestamp)

    def get_current_streak(self) -> int:
        """
        Calculate the current streak of consecutive completions up to today (daily) or this week (weekly).

        Returns:
            int: The current streak count.
        """
        if not self.completions:
            return 0
        # Sort completions in ascending order
        completions = sorted([dt.date() for dt in self.completions])
        streak = 0
        today = datetime.now().date()

        if self.periodicity == Periodicity.DAILY:
            # Count consecutive days from today backwards
            day = today
            idx = len(completions) - 1
            while idx >= 0 and completions[idx] == day:
                streak += 1
                day -= timedelta(days=1)
                idx -= 1
            return streak

        elif self.periodicity == Periodicity.WEEKLY:
            # Count consecutive weeks from current week backwards
            # Find the Monday of the current week
            week_start = today - timedelta(days=today.weekday())
            idx = len(completions) - 1
            while (
                idx >= 0
                and completions[idx] >= week_start
                and completions[idx] <= today
            ):
                streak += 1
                # Move to previous week
                week_start -= timedelta(days=7)
                today = week_start + timedelta(days=6)
                # Find if there's a completion in that week
                found = False
                for j in range(idx, -1, -1):
                    if completions[j] >= week_start and completions[j] <= today:
                        idx = j
                        found = True
                        break
                if not found:
                    break
            return streak

        return 0

    def get_longest_streak(self):
        """
        Calculate the longest streak of consecutive completions (daily or weekly).
        Returns:
            int: The longest streak count.
        """
        if not self.completions:
            return 0

        completions = sorted([dt.date() for dt in self.completions])

        if self.periodicity == Periodicity.DAILY:
            longest = current = 1
            for i in range(1, len(completions)):
                if (completions[i] - completions[i - 1]).days == 1:
                    current += 1
                else:
                    longest = max(longest, current)
                    current = 1
            longest = max(longest, current)
            return longest

        elif self.periodicity == Periodicity.WEEKLY:
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

    def get_completion_count(self) -> int:
        """Return the total number of times this habit has been completed.
        Returns: int: The total count of completions."""

        return len(self.completions)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the habit to a dictionary representation.
        Returns: Dict[str, Any]: Dictionary containing all habit data"""

        return {
            # TODO "id": self.id,
            "name": self.name,
            "description": self.description,
            "periodicity": self.periodicity.value,  # Convert enum to string
            "created_date": self.created_date.isoformat(),  # Convert datetime to ISO string
            "completions": [
                completion.isoformat() for completion in self.completions
            ],  # Convert all datetimes to ISO strings
        }
