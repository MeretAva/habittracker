"""Usage Guide of the HabitTracker CLI including instructions on installation, quick start commands, available commands, and examples."""

# HabitTracker CLI Usage Guide

## Quick Start

All commands are now **interactive** - just run the command and follow the prompts.

```bash
# Run the app
python main.py

# Add a new habit (interactive)
python main.py add

# Complete a habit (interactive selection)
python main.py complete

# View habit status (interactive selection)
python main.py status

# Remove a habit (interactive selection)
python main.py remove

# View analytics
python main.py analytics <subcommand>
```

## Interactive Commands

### `add`

Creates a new habit with guided prompts:

1. **Name**: What to call your habit
2. **Description**: What the habit involves (required)
3. **Frequency**: Choose between Daily (1) or Weekly (2)

Example interaction:

```
$ python main.py add

Let's create a new habit!
What would you like to call this habit?: Read
Enter a description (what does this habit involve?): Read for 30 minutes

How often should this habit be completed?
1. Daily
2. Weekly
Please select (1 or 2): 1

✓ Added habit 'Read' (daily)
  Description: Read for 30 minutes
```

### `complete`

Shows a numbered list of all your habits. Select which one to mark as completed:

```
$ python main.py complete

Select a habit to mark as completed:
5 habit(s) found:
--------------------------------------------------

1. ✴️ Read (daily)
   Read for 30 minutes
   Current streak: 5 | Longest: 12
   Status: ✓

2. ⏸️ Exercise (daily)
   Go to the gym
   Current streak: 0 | Longest: 3
   Status: DUE

Select habit number (or 0 to cancel): 1
✓ Completed 'Read' - Current streak: 6
```

### `remove`

Shows all habits and lets you select which to remove:

```
$ python main.py remove

Select a habit to remove:
Are you sure you want to remove 'Exercise'? [y/N]: y
✓ Removed habit 'Exercise'
```

### `status`

Shows all habits, then displays detailed information for your selection:

```
$ python main.py status

Select habit number (or 0 to cancel): 1

--- DETAILED STATUS ---
Habit: Read
Description: Read for 30 minutes
Periodicity: daily
Created: 2024-01-15
Total completions: 23
Current streak: 6
Longest streak: 12
Status: This habit is up to date
Last completed: 2024-01-20 19:30
```

## Analytics Commands

Analytics has specific subcommands for detailed insights:

### Overview

```bash
python main.py analytics overview
```

Shows complete analytics dashboard with totals, due habits, and broken habits.

### Streak Analytics

```bash
python main.py analytics longest-streak
python main.py analytics active-streaks
python main.py analytics habit-streak "Read"
```

### Habit Lists

```bash
python main.py analytics list              # All habits
python main.py analytics list -p daily     # Daily habits only
python main.py analytics list -p weekly    # Weekly habits only
python main.py analytics daily-habits      # Daily habits with details
python main.py analytics weekly-habits     # Weekly habits with details
```

### Status Checks

```bash
python main.py analytics due-today         # What needs to be done
python main.py analytics broken-habits     # What's been missed
```

## Status Indicators

- ✴️ Active streak
- ⏸️ No current streak
- ✓ Up to date
- DUE - needs completion today/this week
- BROKEN - missed too many periods

## Tips

1. **No more command line arguments** - everything is interactive!
2. **Type `0` to cancel** any selection prompt
3. **Data persists** in `database/habittracker.db`
4. **Weekly habits reset on Monday**
5. **Daily habits reset each day**
6. **Use `python main.py --help`** to see all available commands
