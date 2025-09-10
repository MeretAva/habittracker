from setuptools import setup, find_packages

setup(
    name="habittracker",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": ["habittracker=src.cli.cli:cli", "ht=src.cli.cli:cli"],
    },
    author="Meret Ava Ditzler",
    description="A habit tracking application with analytics and CLI",
    python_requires=">=3.7",
)
