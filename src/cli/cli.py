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
@click.argument("name")
@click.argument("description")
@click.option(
    "--periodicity",
    "-p",
    type=click.Choice(["daily", "weekly"], case_sensitive=False),
    default="daily",
    help="How often the habit should be completed (default: daily)",
)
@click.pass_context
def add(ctx, name: str, description: str, periodicity: str):
    """Add a new habit to track."""
    tracker = ctx.obj["tracker"]

    try:
        habit = Habit(
            name=name,
            description=description,
            periodicity=Periodicity(periodicity.lower()),
        )
        tracker.add_habit(habit)
        click.echo(f"✓ Added habit '{name}' ({periodicity})")
    except Exception as e:
        click.echo(f"Error adding habit: {e}", err=True)


@cli.command()
@click.argument("name")
@click.pass_context
def complete(ctx, name: str):
    """Mark a habit as completed."""
    tracker = ctx.obj["tracker"]

    habit = tracker.get_habit_by_name(name)
    if not habit:
        click.echo(f"Habit '{name}' not found", err=True)
        return

    try:
        streak = tracker.complete_habit(habit.id)
        click.echo(f"✓ Completed '{name}' - Current streak: {streak}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("name")
@click.pass_context
def remove(ctx, name: str):
    """Remove a habit from tracking."""
    tracker = ctx.obj["tracker"]

    habit = tracker.get_habit_by_name(name)
    if not habit:
        click.echo(f"Habit '{name}' not found", err=True)
        return

    if click.confirm(f"Are you sure you want to remove '{name}'?"):
        if tracker.remove_habit(habit.id):
            click.echo(f"✓ Removed habit '{name}'")
        else:
            click.echo("Failed to remove habit", err=True)


@cli.command()
@click.option(
    "--periodicity",
    "-p",
    type=click.Choice(["daily", "weekly", "all"], case_sensitive=False),
    default="all",
    help="Filter by periodicity (default: all)",
)
@click.pass_context
def list(ctx, periodicity: str):
    """List all tracked habits."""
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
        status = "🔥" if habit.get_current_streak() > 0 else "⏸️"
        due_status = "DUE" if habit.is_due() else "✓"
        broken_status = "BROKEN" if habit.is_broken() else ""

        click.echo(f"{status} {habit.name} ({habit.periodicity.value})")
        click.echo(f"   {habit.description}")
        click.echo(
            f"  Current streak: {habit.get_current_streak()} | Longest: {habit.get_longest_streak()}"
        )
        click.echo(f"   Status: {due_status} {broken_status}")
        click.echo()


@cli.command()
@click.argument("name")
@click.pass_context
def status(ctx, name: str):
    """Show detailed status for a specific habit."""
    tracker = ctx.obj["tracker"]

    habit = tracker.get_habit_by_name(name)
    if not habit:
        click.echo(f"Habit '{name}' not found", err=True)
        return

    click.echo(f"\nHabit: {habit.name}")
    click.echo(f"Description: {habit.description}")
    click.echo(f"Periodicity: {habit.periodicity.value}")
    click.echo(f"Created: {habit.created_date.strftime('%Y-%m-%d')}")
    click.echo(f"Total completions: {len(habit.completions)}")
    click.echo(f"Current streak: {habit.get_current_streak()}")
    click.echo(f"Longest streak: {habit.get_longest_streak()}")

    if habit.is_due():
        click.echo("This habit is DUE")
    elif habit.is_broken():
        click.echo("This habit is BROKEN")
    else:
        click.echo("This habit is up to date")

    if habit.completions:
        click.echo(
            f"Last completed: {max(habit.completions).strftime('%Y-%m-%d %H:%M')}"
        )


@cli.command()
@click.pass_context
def analytics(ctx):
    """Show analytics and insights for all habits."""
    tracker = ctx.obj["tracker"]
    habits = tracker.get_all_habits()

    if not habits:
        click.echo("No habits to analyze")
        return

    daily_habits = tracker.get_habits_by_periodicity(Periodicity.DAILY)
    weekly_habits = tracker.get_habits_by_periodicity(Periodicity.WEEKLY)
    longest_streak = tracker.get_longest_streak_all_habits()

    due_habits = [h for h in habits if h.is_due()]
    broken_habits = [h for h in habits if h.is_broken()]
    active_habits = [h for h in habits if h.get_current_streak() > 0]

    click.echo("\nHABIT ANALYTICS")
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

    if active_habits:
        click.echo(f"\nTOP ACTIVE STREAKS:")
        sorted_active = sorted(
            active_habits, key=lambda h: h.get_current_streak(), reverse=True
        )[:5]
        for habit in sorted_active:
            click.echo(f"   • {habit.name}: {habit.get_current_streak()} days")


if __name__ == "__main__":
    cli()