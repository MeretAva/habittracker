from setuptools import setup

setup(
    name="habittracker",
    version="1.0.0",
    py_modules=["models", "analytics", "cli"],
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "habittracker=cli:cli",
        ],
    },
    author="Meret Ava Ditzler",
    description="A habit tracking application with analytics",
    python_requires=">=3.7",
)