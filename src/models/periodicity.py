"""Defines the Periodicity enum for habit tracking (daily or weekly)."""

from enum import Enum


class Periodicity(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
