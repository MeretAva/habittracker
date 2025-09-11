# HabitTracker CLI Usage Guide

## Installation

First, install the package:

```bash
pip install -e .
```

This creates two commands:

- `habittracker` (full name)
- `ht` (short alias)

## Quick Start

```bash
# Add a daily habit
python main.py add "Read" "Read one chapter daily" --periodicity daily

# Add a weekly habit  
python main.py add "Exercise" "Go to gym" --periodicity weekly

# Complete a habit
python main.py complete "Read"

# List all habits
python main.py list

# Show habit details
python main.py status "Read"

# View analytics
python main.py analytics

# Remove a habit
python main.py remove "Read"
```

## Available Commands

### `add NAME DESCRIPTION [OPTIONS]`

Add a new habit to track.

Options:

- `-p, --periodicity [daily|weekly]`: How often to complete (default: daily)

Example:

```bash
python main.py add "Meditate" "10 minutes daily meditation" -p daily
```

### `complete NAME`

Mark a habit as completed for the current period.

Example:

```bash
python main.py complete "Meditate"
```

### `list [OPTIONS]`

List all tracked habits with current status.

Options:

- `-p, --periodicity [daily|weekly|all]`: Filter by periodicity (default: all)

Example:

```bash
python main.py list -p daily
```

### `status NAME`

Show detailed information about a specific habit.

Example:

```bash
python main.py status "Meditate"
```

### `analytics`

Display comprehensive analytics and insights about all habits.

Shows:

- Total habit counts
- Active streaks
- Habits due today/this week
- Broken habits
- Longest streaks

### `remove NAME`

Remove a habit from tracking (with confirmation prompt).

Example:

```bash
python main.py remove "Meditate"
```

## Status Indicators

- 🔥 Active streak
- ⏸️ No current streak
- 📅 DUE - needs completion
- ✓ Up to date
- 💔 BROKEN - missed too many periods

## Tips

1. Use quotes around habit names with spaces: `"Read Books"`
2. The CLI remembers all your data in `database/habittracker.db`
3. Weekly habits reset on Monday
4. Daily habits reset each day
5. Use `python main.py COMMAND --help` for detailed command help
