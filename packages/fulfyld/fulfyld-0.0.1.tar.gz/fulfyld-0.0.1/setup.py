#!/usr/bin/env python

"""Setup script for the package."""

import logging
import os
import sys

import setuptools

PACKAGE_NAME = "fulfyld"
MINIMUM_PYTHON_VERSION = "3.8"


def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version < MINIMUM_PYTHON_VERSION:
        sys.exit("Python {0}+ is required.".format(MINIMUM_PYTHON_VERSION))


def read_package_variable(key, filename="__init__.py"):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join("src", PACKAGE_NAME, filename)
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(" ", 2)
            if parts[:-1] == [key, "="]:
                return parts[-1].strip("'").strip('"')
    logging.warning("'%s' not found in '%s'", key, module_path)
    return None


DEV_REQUIRES = [
    "pytest",
    "pre-commit",
    "pylint",
    "black",
]


setuptools.setup(
    name=read_package_variable("__project__"),
    version=read_package_variable("__version__"),
    description="",
    url="https://github.com/olirice/doci",
    author="Oliver Rice",
    author_email="oliver@oliverrice.com",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "fulfyld = fulfyld.cli:app",
        ]
    },
    install_requires=["typer", "typing_extensions", "pandas", "coloredlogs"],
    tests_require=["pytest", "coverage"],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    extras_require={"dev": DEV_REQUIRES},
)
