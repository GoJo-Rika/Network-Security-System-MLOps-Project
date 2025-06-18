"""
The setup.py file is an essential part of packaging and distributing Python projects.

It is used by setuptools (or distutils in older Python versions) to define the configuration
of your project, such as its metadata, dependencies, and more
"""

from pathlib import Path

from setuptools import find_packages, setup


def get_requirements() -> list[str]:
    """Return a list of requirements."""
    requirement_lst: list[str] = []
    try:
        with Path("requirements.txt").open("r") as file:
            # Read lines from the file
            lines = file.readlines()
            ## Process each line
            for line in lines:
                requirement = line.strip()
                ## ignore empty lines and -e .
                if requirement and requirement != "-e .":
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_lst


# print(get_requirements())

setup(
    name="Network-Security",
    version="0.0.1",
    author="Mit Patel",
    author_email="patel.m9521@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
