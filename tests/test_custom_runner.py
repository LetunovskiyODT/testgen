#!/usr/bin/env python3
"""
Тесты для проверки работы собственного тестраннера
"""

import os
import tempfile
from testengines.custom_runner import TestCase, TestRunner, run_tests

# Пример тестового класса для тестирования собственного тестраннера
class SampleTestCase(TestCase):
    """Пример тестового класса для тестирования собственного тестраннера"""
    
    def setUp(self) -> None:
        """Инициализация перед каждым тестом"""
        self.value = 10
    
    def test_success(self) -> None:
        """Успешный тест"""
        assert self.value == 10
    
    def test_failure(self) -> None:
        """Тест с ошибкой утверждения"""
        assert self.value == 5
    
    def test_error(self) -> None:
        """Тест с ошибкой выполнения"""
        raise ValueError("Пример ошибки")


# Тесты для тестирования тестраннера с использованием pytest
def test_test_runner_discovery() -> None:
    """Тестирует обнаружение тестов"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Создаем временный тестовый файл
        with open(os.path.join(tmp_dir, "test_sample.py"), "w") as f:
            f.write("""
from testengines.custom_runner import TestCase

class SampleTest(TestCase):
    def test_one(self):
        assert True
        
    def test_two(self):
        assert False
            """)
        
        runner = TestRunner(verbosity=0)
        tests = runner.discover_tests(tmp_dir)
        
        # Проверяем, что тесты обнаружены
        assert len(tests) == 1
        
        file_path = os.path.join(tmp_dir, "test_sample.py")
        assert file_path in tests
        assert "SampleTest" in tests[file_path]
        assert len(tests[file_path]["SampleTest"]) == 2
        assert "test_one" in tests[file_path]["SampleTest"]
        assert "test_two" in tests[file_path]["SampleTest"]


def test_test_runner_execution() -> None:
    """Тестирует выполнение тестов"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Создаем временный тестовый файл
        with open(os.path.join(tmp_dir, "test_execution.py"), "w") as f:
            f.write("""
from testengines.custom_runner import TestCase

class ExecutionTest(TestCase):
    def test_success(self):
        assert True
        
    def test_failure(self):
        assert False
        
    def test_error(self):
        raise ValueError("Ошибка")
            """)
        
        # Запускаем тесты с низким уровнем вывода
        runner = TestRunner(verbosity=0)
        result = runner.run(tmp_dir)
        
        # Проверяем результаты
        assert result.total == 3
        assert result.success == 1
        assert len(result.failures) == 1
        assert len(result.errors) == 1
        assert not result.was_successful


def test_test_runner_filtering() -> None:
    """Тестирует фильтрацию тестов"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Создаем временный тестовый файл
        with open(os.path.join(tmp_dir, "test_filtering.py"), "w") as f:
            f.write("""
from testengines.custom_runner import TestCase

class FilteringTest(TestCase):
    def test_one(self):
        assert True
        
    def test_two(self):
        assert True
        
    def test_three(self):
        assert True
            """)
        
        # Запускаем тесты с фильтрацией по шаблону
        runner = TestRunner(verbosity=0, include_patterns=["test_one", "test_three"])
        result = runner.run(tmp_dir)
        
        # Проверяем результаты - должно быть только 2 теста
        assert result.total == 2
        assert result.success == 2
        
        # Запускаем тесты с исключением по шаблону
        runner = TestRunner(verbosity=0, exclude_patterns=["test_three"])
        result = runner.run(tmp_dir)
        
        # Проверяем результаты - должно быть только 2 теста (test_one и test_two)
        assert result.total == 2
        assert result.success == 2 