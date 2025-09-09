"""Defines a set of five predefined Habit objects with sample data spanning over four weeks for testing purposes."""

from src.models import Habit, Periodicity
from datetime import datetime, timedelta

habit1 = Habit("Read", "Read one chapter", Periodicity.DAILY)
habit2 = Habit("Stretch", "Stretch for ten minutes", Periodicity.DAILY)
habit3 = Habit("Take Vitamins", "Take D3 and B12 Vitamins", Periodicity.DAILY)
habit4 = Habit("Call Family", "Call grandparents", Periodicity.WEEKLY)
habit5 = Habit("Vacuum", "Vacuum the apartment", Periodicity.WEEKLY)

# Add 4 weeks of daily completions for daily habits
today = datetime.now()
for i in range(28):  # 4 weeks * 7 days
    habit1.completions.append(today - timedelta(days=i))
    habit3.completions.append(today - timedelta(days=i))
    habit5.completions.append(today - timedelta(days=i))

# Add 4 weekly completions for weekly habits (every Monday)
for i in range(4):
    week_date = today - timedelta(weeks=i)
    monday = week_date - timedelta(days=week_date.weekday())
    habit2.completions.append(monday)
    habit4.completions.append(monday)

predefined_habits = [habit1, habit2, habit3, habit4, habit5]
