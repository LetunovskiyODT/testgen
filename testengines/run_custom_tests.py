#!/usr/bin/env python3
"""
Скрипт для запуска тестов с помощью собственного тестраннера.
Может использоваться как самостоятельный инструмент.
"""

import argparse
import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from testengines.custom_runner import run_tests, TestResult


def main():
    """Точка входа для запуска тестов из командной строки"""
    parser = argparse.ArgumentParser(description="Запуск тестов с помощью собственного тестраннера TestGen")
    parser.add_argument("test_dir", help="Директория с тестами")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], default=1,
                        help="Уровень детализации вывода (0=минимальный, 1=нормальный, 2=подробный)")
    parser.add_argument("-i", "--include", help="Шаблоны для включения тестов (через запятую)")
    parser.add_argument("-e", "--exclude", help="Шаблоны для исключения тестов (через запятую)")
    
    args = parser.parse_args()
    
    # Разбор шаблонов включения и исключения
    include_patterns = args.include.split(",") if args.include else None
    exclude_patterns = args.exclude.split(",") if args.exclude else None
    
    # Запуск тестов
    result = run_tests(args.test_dir, args.verbosity, include_patterns, exclude_patterns)
    
    # Возвращаем код завершения в зависимости от результата тестов
    sys.exit(0 if result.was_successful else 1)


if __name__ == "__main__":
    main() 