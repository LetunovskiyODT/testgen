#!/usr/bin/env python3
"""
Скрипт для создания удаленного репозитория на GitHub.
"""

import os
import sys

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ci.create_repo import main

if __name__ == "__main__":
    main() 