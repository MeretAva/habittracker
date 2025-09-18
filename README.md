### Object Oriented and Functional Programming with Python – HabitTracker

This is the repository for my IU course Object Oriented and Functional Programming with Python. To complete the course I developed a habit tracking application with basic functionality, analytics, and a CLI.
To install the application please clone the repository onto your local machine and interact with the application using the CLI following the instructions provided in CLI_USAGE.md. Please ensure that the local machine meets defined the requirements and dependencies. For further information please regard the information below:

## Installation

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Setup Instructions

1. **Clone the repository**

   ```bash
      git clone https://github.com/MeretAva/habittracker
      cd habittracker
   ```

2. **Create and activate a virtual environment**

    Create virtual environment

   ```bash
   python -m venv .venv
   ```

    Activate virtual environment

    On Windows:

   ```bash
   .venv\Scripts\activate
   ```

    On macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python main.py --help
   ```

## Quick Start

All commands are interactive - just run them and follow the prompts!

```bash
# Start the application
python main.py

# Add your first habit
python main.py add

# Mark a habit as completed
python main.py complete

# View your progress
python main.py analytics overview

# Get detailed usage instructions
python main.py --help
```

## Documentation

For detailed command usage and examples, see [CLI_USAGE.md](CLI_USAGE.md)

## Testing

Run the test suite:

```bash
pytest tests/
```

## Requirements

See [requirements.txt](requirements.txt) for a complete list of dependencies.

```

```
