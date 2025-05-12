#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="testgen",
    version="1.0.0",
    author="TestGen Contributors",
    author_email="example@example.com",
    description="CLI-утилита для генерации и запуска тестов для разных языков программирования",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/testgen",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/testgen/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Unit",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "typer>=0.4.0",
        "rich>=10.0.0",
        "pyfiglet>=0.8.post1",
        "pytest>=6.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.5b2",
            "isort>=5.9.1",
            "mypy>=0.812",
            "pylint>=2.8.2",
        ],
    },
    entry_points={
        "console_scripts": [
            "testgen=cmd.testgen.main:app",
        ],
    },
) 