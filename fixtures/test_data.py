"""Defines a function to create fresh  predefined Habit objects with sample data spanning over four weeks for testing purposes."""

from src.models import Habit, Periodicity
from datetime import datetime, timedelta


def create_predefined_habits():
    habit1 = Habit("Read", "Read one chapter", Periodicity.DAILY)
    habit2 = Habit("Stretch", "Stretch for ten minutes", Periodicity.DAILY)
    habit3 = Habit("Take Vitamins", "Take D3 and B12 Vitamins", Periodicity.DAILY)
    habit4 = Habit("Call Family", "Call grandparents", Periodicity.WEEKLY)
    habit5 = Habit("Vacuum", "Vacuum the apartment", Periodicity.WEEKLY)

    # Add 4 weeks of sample data for testing purposes
    today = datetime.now()

    # Habit1: "Read" - Consistent with some gaps
    # Completed: 0,1,2,4,5,7,8,9,11,12,13,15,16,17,19,20,22,23,24,26,27 (21/28 days)
    read_completion_days = [
        0,
        1,
        2,
        4,
        5,
        7,
        8,
        9,
        11,
        12,
        13,
        15,
        16,
        17,
        19,
        20,
        22,
        23,
        24,
        26,
        27,
    ]
    for day in read_completion_days:
        habit1.completions.append(today - timedelta(days=day))

    # Habit3: "Take Vitamins" - Last 3 days missed, perfect before
    # Completed: 3-27
    for i in range(3, 28):
        habit3.completions.append(today - timedelta(days=i))

    # Habit5 "Vacuum" - Inconsistent
    # Completed: 0,3,6,10,14,17,21,24,27 (9/28 days)
    vacuum_completion_days = [0, 3, 6, 10, 14, 17, 21, 24, 27]
    for day in vacuum_completion_days:
        habit5.completions.append(today - timedelta(days=day))

    # Habit2 "Stretch" - Perfect completion on different days
    # Week 0: Friday, Week 1: Tuesday, Week 2: Sunday, Week 3: Wednesday
    weekly_days = [4, 1, 6, 2]  # Days of the week (O = Monday, 6 = Sunday)
    for i in range(4):
        week_date = today - timedelta(weeks=i)
        monday = week_date - timedelta(days=week_date.weekday())
        completion_day = monday + timedelta(days=weekly_days[i])
        habit2.completions.append(completion_day)

    # Habit4 "Call Family" - Completion missed one week
    # Completed weeks 0, 1, 3 on different days
    call_weeks = [0, 1, 3]  # Skip week 2
    call_days = [6, 3, 1]  # Days of the week (O = Monday, 6 = Sunday)
    for i, week in enumerate(call_weeks):
        week_date = today - timedelta(weeks=week)
        monday = week_date - timedelta(days=week_date.weekday())
        completion_day = monday + timedelta(days=call_days[i])
        habit4.completions.append(completion_day)

    return [habit1, habit2, habit3, habit4, habit5]
