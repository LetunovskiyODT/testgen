#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="testgen",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.3",
        "rich>=12.0.0",
        "prompt-toolkit>=3.0.28",
        "pyyaml>=6.0",
        "pytest>=7.3.1",
        "textual>=0.27.0",
        "typer==0.9.0",
        "pyfiglet>=0.8.post1",
        "pytest-cov>=4.1.0",
        "gitpython>=3.1.30",
    ],
    entry_points={
        "console_scripts": [
            "testgen=testgen:main",
        ],
    },
) 