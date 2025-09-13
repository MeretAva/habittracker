"""Setup Script to define metadata on the project: name, version, dependencies, entry points, author, description, version compatibility."""

from setuptools import setup, find_packages

setup(
    name="habittracker",
    version="1.0.0",
    author="Meret Ava Ditzler",
    description="A habit tracking application with analytics and CLI created for the course Object Oriented and Functional Programming with Python",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0",
    ],
)
