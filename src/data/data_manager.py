class DataManager:
    """Handles all database operations for HabitTracker."""

    def __init__(self, db_path: str = "habittracker.db"):
        self.db_path = db_path
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


class DataManager:
    def __init__(self, connection, db_path="habittracker.db"):
        self.connection = connection
        pass

    def create_tables():
        pass

    def save_habit(habit=Habit):
        pass

    def load_habits():
        pass

    def save_completion(habit_id, timestamp):
        pass

    def load_completions(habit_id):
        pass

    def delete_habit(habit_id):
        pass

    def close_connection():
        pass
