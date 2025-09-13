"""Defines the CLI commands to interact with the HabitTracker"""

import click
from datetime import datetime
from typing import Optional
from ..core.habit_tracker import HabitTracker
from ..models.habit import Habit
from ..models.periodicity import Periodicity


@click.group()
@click.pass_context
def cli(ctx):
    """HabitTracker CLI - Track and analyse your daily habits."""
    ctx.ensure_object(dict)
    ctx.obj["tracker"] = HabitTracker()


@cli.command()
@click.pass_context
def add(ctx):
    """Add a new habit to track."""
    tracker = ctx.obj["tracker"]

    # Interactive prompts
    click.echo("\nLet's create a new habit!")
    name = click.prompt("What would you like to call this habit?", type=str).strip()

    description = click.prompt(
        "Enter a description (define the task)",
        type=str,
    ).strip()

    # Periodicity selection
    click.echo("\nHow often should this habit be completed?")
    click.echo("1. Daily")
    click.echo("2. Weekly")

    while True:
        choice = click.prompt("Please select (1 or 2)", type=int)
        if choice == 1:
            periodicity = "daily"
            break
        elif choice == 2:
            periodicity = "weekly"
            break
        else:
            click.echo("Please enter 1 for daily or 2 for weekly")

    try:
        habit = Habit(
            name=name,
            description=description,
            periodicity=Periodicity(periodicity.lower()),
        )
        tracker.add_habit(habit)
        click.echo(f"\n✓ Added habit '{name}' ({periodicity})")
        click.echo(f"  Description: {description}")
    except Exception as e:
        click.echo(f"Error adding habit: {e}", err=True)


@cli.command()
@click.pass_context
def complete(ctx):
    """Mark a habit as completed (interactive)."""
    tracker = ctx.obj["tracker"]
    habits = tracker.get_all_habits()

    if not habits:
        click.echo("\nNo habits found to complete.")
        return

    # Use existing list display logic
    click.echo(f"\nSelect a habit to mark as completed:")
    click.echo(f"{len(habits)} habit(s) found:")
    click.echo("-" * 50)

    for i, habit in enumerate(habits, 1):
        status = "✴️" if habit.get_current_streak() > 0 else "⏸️"
        due_status = "DUE" if habit.is_due() else "✓"
        broken_status = "BROKEN" if habit.is_broken() else ""

        click.echo(f"{i}. {status} {habit.name} ({habit.periodicity.value})")
        click.echo(f"   {habit.description}")
        click.echo(
            f"   Current streak: {habit.get_current_streak()} | Longest: {habit.get_longest_streak()}"
        )
        click.echo(f"   Status: {due_status} {broken_status}")
        click.echo()

    while True:
        try:
            choice = click.prompt("Select habit number (or 0 to cancel)", type=int)

            if choice == 0:
                click.echo("Cancelled.")
                return
            elif 1 <= choice <= len(habits):
                selected_habit = habits[choice - 1]
                break
            else:
                click.echo(
                    f"Please enter a number between 1 and {len(habits)} (or 0 to cancel)"
                )
        except (ValueError, click.Abort):
            click.echo("Please enter a valid number")

    try:
        streak = tracker.complete_habit(selected_habit.id)
        click.echo(f"✓ Completed '{selected_habit.name}' - Current streak: {streak}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.pass_context
def remove(ctx):
    """Remove a habit from tracking (interactive)."""
    tracker = ctx.obj["tracker"]
    habits = tracker.get_all_habits()

    if not habits:
        click.echo("\nNo habits found to remove.")
        return

    # Use existing list display logic
    click.echo(f"\nSelect a habit to remove:")
    click.echo(f"{len(habits)} habit(s) found:")
    click.echo("-" * 50)

    for i, habit in enumerate(habits, 1):
        status = "✴️" if habit.get_current_streak() > 0 else "⏸️"
        due_status = "DUE" if habit.is_due() else "✓"
        broken_status = "BROKEN" if habit.is_broken() else ""

        click.echo(f"{i}. {status} {habit.name} ({habit.periodicity.value})")
        click.echo(f"   {habit.description}")
        click.echo(
            f"   Current streak: {habit.get_current_streak()} | Longest: {habit.get_longest_streak()}"
        )
        click.echo(f"   Status: {due_status} {broken_status}")
        click.echo()

    while True:
        try:
            choice = click.prompt("Select habit number (or 0 to cancel)", type=int)

            if choice == 0:
                click.echo("Cancelled.")
                return
            elif 1 <= choice <= len(habits):
                selected_habit = habits[choice - 1]
                break
            else:
                click.echo(
                    f"Please enter a number between 1 and {len(habits)} (or 0 to cancel)"
                )
        except (ValueError, click.Abort):
            click.echo("Please enter a valid number")

    # Confirm removal
    if click.confirm(f"Are you sure you want to remove '{selected_habit.name}'?"):
        if tracker.remove_habit(selected_habit.id):
            click.echo(f"✓ Removed habit '{selected_habit.name}'")
        else:
            click.echo("Failed to remove habit", err=True)
    else:
        click.echo("Removal cancelled.")


@cli.command()
@click.pass_context
def status(ctx):
    """Show detailed status for a specific habit (interactive)."""
    tracker = ctx.obj["tracker"]
    habits = tracker.get_all_habits()

    if not habits:
        click.echo("\nNo habits found.")
        return

    # Use existing list display logic
    click.echo(f"\nSelect a habit to view status:")
    click.echo(f"{len(habits)} habit(s) found:")
    click.echo("-" * 50)

    for i, habit in enumerate(habits, 1):
        status = "✴️" if habit.get_current_streak() > 0 else "⏸️"
        due_status = "DUE" if habit.is_due() else "✓"
        broken_status = "BROKEN" if habit.is_broken() else ""

        click.echo(f"{i}. {status} {habit.name} ({habit.periodicity.value})")
        click.echo(f"   {habit.description}")
        click.echo(
            f"   Current streak: {habit.get_current_streak()} | Longest: {habit.get_longest_streak()}"
        )
        click.echo(f"   Status: {due_status} {broken_status}")
        click.echo()

    while True:
        try:
            choice = click.prompt("Select habit number (or 0 to cancel)", type=int)

            if choice == 0:
                click.echo("Cancelled.")
                return
            elif 1 <= choice <= len(habits):
                selected_habit = habits[choice - 1]
                break
            else:
                click.echo(
                    f"Please enter a number between 1 and {len(habits)} (or 0 to cancel)"
                )
        except (ValueError, click.Abort):
            click.echo("Please enter a valid number")

    # Show detailed status using existing habit methods
    click.echo(f"\n--- DETAILED STATUS ---")
    click.echo(f"Habit: {selected_habit.name}")
    click.echo(f"Description: {selected_habit.description}")
    click.echo(f"Periodicity: {selected_habit.periodicity.value}")
    click.echo(f"Created: {selected_habit.created_date.strftime('%Y-%m-%d')}")
    click.echo(f"Total completions: {len(selected_habit.completions)}")
    click.echo(f"Current streak: {selected_habit.get_current_streak()}")
    click.echo(f"Longest streak: {selected_habit.get_longest_streak()}")

    if selected_habit.is_due():
        click.echo("Status: This habit is DUE")
    elif selected_habit.is_broken():
        click.echo("Status: This habit is BROKEN")
    else:
        click.echo("Status: This habit is up to date")

    if selected_habit.completions:
        last_completion = max(selected_habit.completions)
        click.echo(f"Last completed: {last_completion.strftime('%Y-%m-%d %H:%M')}")


@cli.group()
def analytics():
    """Analytics and insights for habits."""
    pass


@analytics.command()
@click.pass_context
def overview(ctx):
    """Show overview analytics for all habits."""
    tracker = ctx.obj["tracker"]
    habits = tracker.get_all_habits()

    if not habits:
        click.echo("No habits to analyse")
        return

    daily_habits = tracker.get_habits_by_periodicity(Periodicity.DAILY)
    weekly_habits = tracker.get_habits_by_periodicity(Periodicity.WEEKLY)
    longest_streak = tracker.get_longest_streak_all_habits()

    due_habits = [h for h in habits if h.is_due()]
    broken_habits = [h for h in habits if h.is_broken()]
    active_habits = [h for h in habits if h.get_current_streak() > 0]

    click.echo("\nHABIT ANALYTICS OVERVIEW")
    click.echo("=" * 50)
    click.echo(f"Total habits: {len(habits)}")
    click.echo(f"Daily habits: {len(daily_habits)}")
    click.echo(f"Weekly habits: {len(weekly_habits)}")
    click.echo(f"Active streaks: {len(active_habits)}")
    click.echo(f"Due today/this week: {len(due_habits)}")
    click.echo(f"Broken habits: {len(broken_habits)}")
    click.echo(f"Longest streak (all habits): {longest_streak}")

    if due_habits:
        click.echo(f"\nHABITS DUE:")
        for habit in due_habits:
            click.echo(f"   • {habit.name}")

    if broken_habits:
        click.echo(f"\nBROKEN HABITS:")
        for habit in broken_habits:
            click.echo(f"   • {habit.name}")


@analytics.command()
@click.pass_context
def longest_streak(ctx):
    """Show the longest streak across all habits."""
    tracker = ctx.obj["tracker"]
    habits = tracker.get_all_habits()

    if not habits:
        click.echo("No habits to analyse")
        return

    longest_streak = tracker.get_longest_streak_all_habits()
    click.echo(f"\nLongest streak across all habits: {longest_streak} days")

    # Find which habit(s) have this longest streak
    longest_habits = []
    for habit in habits:
        if habit.get_longest_streak() == longest_streak:
            longest_habits.append(habit)

    if longest_habits:
        click.echo(f"\nHabit(s) with longest streak:")
        for habit in longest_habits:
            click.echo(f"   • {habit.name}: {habit.get_longest_streak()} days")


@analytics.command()
@click.argument("habit_name")
@click.pass_context
def habit_streak(ctx, habit_name: str):
    """Show streak information for a specific habit."""
    tracker = ctx.obj["tracker"]
    habit = tracker.get_habit_by_name(habit_name)

    if not habit:
        click.echo(f"Habit '{habit_name}' not found", err=True)
        return

    current_streak = habit.get_current_streak()
    longest_streak = habit.get_longest_streak()

    click.echo(f"\nStreak Analytics for '{habit.name}':")
    click.echo("-" * 40)
    click.echo(f"Current streak: {current_streak} days")
    click.echo(f"Longest streak: {longest_streak} days")

    if current_streak == longest_streak and current_streak > 0:
        click.echo("You're on your longest streak ever!")
    elif current_streak == 0:
        click.echo("Start a new streak today!")


@analytics.command()
@click.pass_context
def active_streaks(ctx):
    """Show all habits with active streaks."""
    tracker = ctx.obj["tracker"]
    habits = tracker.get_all_habits()

    if not habits:
        click.echo("No habits to analyse")
        return

    active_habits = [h for h in habits if h.get_current_streak() > 0]

    if not active_habits:
        click.echo("No active streaks found")
        return

    click.echo(f"\nACTIVE STREAKS ({len(active_habits)} habits)")
    click.echo("=" * 40)

    sorted_active = sorted(
        active_habits, key=lambda h: h.get_current_streak(), reverse=True
    )

    for habit in sorted_active:
        streak = habit.get_current_streak()
        longest = habit.get_longest_streak()
        status = "✴️" if streak == longest else "⚡"
        click.echo(f"{status} {habit.name}: {streak} days (best: {longest})")


@analytics.command()
@click.pass_context
def broken_habits(ctx):
    """Show habits that are currently broken."""
    tracker = ctx.obj["tracker"]
    habits = tracker.get_all_habits()

    if not habits:
        click.echo("No habits to analyse")
        return

    broken_habits = [h for h in habits if h.is_broken()]

    if not broken_habits:
        click.echo("No broken habits! Keep up the good work!")
        return

    click.echo(f"\nBROKEN HABITS ({len(broken_habits)} habits)")
    click.echo("=" * 40)

    for habit in broken_habits:
        click.echo(f" {habit.name} ({habit.periodicity.value})")
        if habit.completions:
            last_completion = max(habit.completions)
            click.echo(f"   Last completed: {last_completion.strftime('%Y-%m-%d')}")
        else:
            click.echo(f"   Never completed")


@analytics.command()
@click.pass_context
def due_today(ctx):
    """Show habits that are due today."""
    tracker = ctx.obj["tracker"]
    habits = tracker.get_all_habits()

    if not habits:
        click.echo("No habits to analyse")
        return

    due_habits = [h for h in habits if h.is_due()]

    if not due_habits:
        click.echo("All habits are up to date!")
        return

    click.echo(f"\nHABITS DUE ({len(due_habits)} habits)")
    click.echo("=" * 30)

    for habit in due_habits:
        click.echo(f" {habit.name} ({habit.periodicity.value})")
        click.echo(f"   {habit.description}")


@analytics.command()
@click.option(
    "--periodicity",
    "-p",
    type=click.Choice(["daily", "weekly", "all"], case_sensitive=False),
    default="all",
    help="Filter by periodicity (default: all)",
)
@click.pass_context
def list(ctx, periodicity: str):
    """
    List all tracked habits.

    Args:
        periodicity: string defining the periodicity
    """
    tracker = ctx.obj["tracker"]

    if periodicity == "all":
        habits = tracker.get_all_habits()
    else:
        habits = tracker.get_habits_by_periodicity(Periodicity(periodicity))

    if not habits:
        click.echo("No habits found")
        return

    click.echo(f"\n{len(habits)} habit(s) found:")
    click.echo("-" * 50)

    for habit in habits:
        status = "✴️" if habit.get_current_streak() > 0 else "⏸️"
        due_status = "DUE" if habit.is_due() else "✓"
        broken_status = "BROKEN" if habit.is_broken() else ""

        click.echo(f"{status} {habit.name} ({habit.periodicity.value})")
        click.echo(f"   {habit.description}")
        click.echo(
            f"  Current streak: {habit.get_current_streak()} | Longest: {habit.get_longest_streak()}"
        )
        click.echo(f"   Status: {due_status} {broken_status}")
        click.echo()


@analytics.command()
@click.pass_context
def daily_habits(ctx):
    """Show all daily habits."""
    tracker = ctx.obj["tracker"]
    daily_habits = tracker.get_habits_by_periodicity(Periodicity.DAILY)

    if not daily_habits:
        click.echo("No daily habits found")
        return

    click.echo(f"\nDAILY HABITS ({len(daily_habits)} habits)")
    click.echo("=" * 40)

    for habit in daily_habits:
        status = "✴️" if habit.get_current_streak() > 0 else "⏸️"
        due_status = "DUE" if habit.is_due() else "✓"
        broken_status = "BROKEN" if habit.is_broken() else ""

        click.echo(f"{status} {habit.name}")
        click.echo(f"   {habit.description}")
        click.echo(
            f"   Current streak: {habit.get_current_streak()} | Longest: {habit.get_longest_streak()}"
        )
        click.echo(f"   Status: {due_status} {broken_status}")
        click.echo()


@analytics.command()
@click.pass_context
def weekly_habits(ctx):
    """Show all weekly habits."""
    tracker = ctx.obj["tracker"]
    weekly_habits = tracker.get_habits_by_periodicity(Periodicity.WEEKLY)

    if not weekly_habits:
        click.echo("No weekly habits found")
        return

    click.echo(f"\nWEEKLY HABITS ({len(weekly_habits)} habits)")
    click.echo("=" * 40)

    for habit in weekly_habits:
        status = "✴️" if habit.get_current_streak() > 0 else "⏸️"
        due_status = "DUE" if habit.is_due() else "✓"
        broken_status = "BROKEN" if habit.is_broken() else ""

        click.echo(f"{status} {habit.name}")
        click.echo(f"   {habit.description}")
        click.echo(
            f"   Current streak: {habit.get_current_streak()} | Longest: {habit.get_longest_streak()}"
        )
        click.echo(f"   Status: {due_status} {broken_status}")
        click.echo()
