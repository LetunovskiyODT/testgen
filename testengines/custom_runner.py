#!/usr/bin/env python3
"""
Собственный тестраннер для TestGen
"""

import os
import sys
import importlib
import inspect
import time
import traceback
from typing import Dict, List, Tuple, Any, Optional, Set, Callable
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class TestCase:
    """Базовый класс для тест-кейса"""
    
    def setUp(self) -> None:
        """Подготовка перед выполнением теста"""
        pass
        
    def tearDown(self) -> None:
        """Очистка после выполнения теста"""
        pass


class TestResult:
    """Класс для хранения результатов тестирования"""
    
    def __init__(self):
        self.total = 0
        self.success = 0
        self.failures = []
        self.errors = []
        self.skipped = []
        self.start_time = 0.0
        self.end_time = 0.0
        
    @property
    def duration(self) -> float:
        """Возвращает продолжительность выполнения тестов"""
        return self.end_time - self.start_time
        
    @property
    def was_successful(self) -> bool:
        """Возвращает True, если все тесты прошли успешно"""
        return len(self.failures) == 0 and len(self.errors) == 0


class TestRunner:
    """Собственный тестраннер для запуска и анализа тестов"""
    
    def __init__(self, verbosity: int = 1, include_patterns: List[str] = None, exclude_patterns: List[str] = None):
        self.verbosity = verbosity
        self.include_patterns = include_patterns or []
        self.exclude_patterns = exclude_patterns or []
        self.result = TestResult()
        
    def _should_run_test(self, test_name: str) -> bool:
        """
        Проверяет, должен ли тест быть запущен на основе шаблонов включения и исключения
        
        Args:
            test_name (str): Имя теста
            
        Returns:
            bool: True, если тест должен быть запущен, иначе False
        """
        # Если есть шаблоны включения, проверяем, соответствует ли тест хотя бы одному из них
        if self.include_patterns:
            included = any(pattern in test_name for pattern in self.include_patterns)
            if not included:
                return False
                
        # Если есть шаблоны исключения, проверяем, соответствует ли тест хотя бы одному из них
        if self.exclude_patterns:
            excluded = any(pattern in test_name for pattern in self.exclude_patterns)
            if excluded:
                return False
                
        return True
        
    def discover_tests(self, start_dir: str) -> Dict[str, Dict[str, List[str]]]:
        """
        Находит все тесты в указанной директории
        
        Args:
            start_dir (str): Директория для поиска тестов
            
        Returns:
            Dict[str, Dict[str, List[str]]]: Словарь с найденными тестами
        """
        test_files = {}
        
        # Ищем все файлы Python, начинающиеся с 'test_'
        for root, dirs, files in os.walk(start_dir):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    module_path = os.path.join(root, file)
                    module_name = os.path.splitext(file)[0]
                    
                    # Загружаем модуль
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                    
                    # Находим все классы тестов и методы тестирования
                    test_classes = {}
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, TestCase) and obj != TestCase:
                            test_methods = []
                            for method_name, method in inspect.getmembers(obj):
                                if method_name.startswith('test_') and inspect.isfunction(method):
                                    if self._should_run_test(f"{module_name}.{name}.{method_name}"):
                                        test_methods.append(method_name)
                            
                            if test_methods:
                                test_classes[name] = test_methods
                    
                    if test_classes:
                        test_files[module_path] = test_classes
        
        return test_files
        
    def run(self, test_dir: str) -> TestResult:
        """
        Запускает все найденные тесты
        
        Args:
            test_dir (str): Директория с тестами
            
        Returns:
            TestResult: Результаты выполнения тестов
        """
        self.result = TestResult()
        self.result.start_time = time.time()
        
        console.print(Panel.fit(f"[bold]Запуск тестов из директории: {test_dir}[/bold]"))
        
        # Находим все тесты
        test_files = self.discover_tests(test_dir)
        
        if not test_files:
            console.print("[yellow]Тесты не найдены[/yellow]")
            self.result.end_time = time.time()
            return self.result
        
        total_tests = sum(len(methods) for file_tests in test_files.values() for methods in file_tests.values())
        console.print(f"Найдено тестов: {total_tests}")
        
        # Запускаем тесты
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("Выполнение тестов...", total=total_tests)
            
            for module_path, test_classes in test_files.items():
                module_name = os.path.splitext(os.path.basename(module_path))[0]
                
                # Загружаем модуль
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                
                # Запускаем тесты для каждого класса
                for class_name, test_methods in test_classes.items():
                    test_class = getattr(module, class_name)
                    
                    for method_name in test_methods:
                        progress.update(task, description=f"Выполнение {module_name}.{class_name}.{method_name}")
                        self.result.total += 1
                        
                        test_instance = test_class()
                        try:
                            test_instance.setUp()
                            try:
                                getattr(test_instance, method_name)()
                                self.result.success += 1
                                if self.verbosity > 1:
                                    console.print(f"[green]✓[/green] {module_name}.{class_name}.{method_name}")
                            except AssertionError as e:
                                self.result.failures.append((f"{module_name}.{class_name}.{method_name}", str(e)))
                                if self.verbosity > 0:
                                    console.print(f"[red]✗[/red] {module_name}.{class_name}.{method_name} - {str(e)}")
                            except Exception as e:
                                self.result.errors.append((f"{module_name}.{class_name}.{method_name}", traceback.format_exc()))
                                if self.verbosity > 0:
                                    console.print(f"[red]![/red] {module_name}.{class_name}.{method_name} - {str(e)}")
                        except Exception as e:
                            self.result.errors.append((f"{module_name}.{class_name}.{method_name} (setUp)", traceback.format_exc()))
                            if self.verbosity > 0:
                                console.print(f"[red]![/red] {module_name}.{class_name}.{method_name} (setUp) - {str(e)}")
                        finally:
                            try:
                                test_instance.tearDown()
                            except Exception as e:
                                self.result.errors.append((f"{module_name}.{class_name}.{method_name} (tearDown)", traceback.format_exc()))
                                if self.verbosity > 0:
                                    console.print(f"[red]![/red] {module_name}.{class_name}.{method_name} (tearDown) - {str(e)}")
                        
                        progress.update(task, advance=1)
        
        self.result.end_time = time.time()
        self._print_result()
        
        return self.result
    
    def _print_result(self) -> None:
        """Выводит результаты тестирования"""
        console.print()
        
        table = Table(title="Результаты тестирования")
        table.add_column("Метрика", style="cyan")
        table.add_column("Значение", style="green")
        
        table.add_row("Всего тестов", str(self.result.total))
        table.add_row("Успешно", str(self.result.success))
        table.add_row("Падений", str(len(self.result.failures)))
        table.add_row("Ошибок", str(len(self.result.errors)))
        table.add_row("Пропущено", str(len(self.result.skipped)))
        table.add_row("Время выполнения", f"{self.result.duration:.2f} сек")
        
        console.print(table)
        
        if self.result.failures:
            console.print("\n[bold red]Падения:[/bold red]")
            for i, (test, error) in enumerate(self.result.failures, 1):
                console.print(f"{i}. [red]{test}[/red]")
                console.print(f"   {error}")
        
        if self.result.errors:
            console.print("\n[bold red]Ошибки:[/bold red]")
            for i, (test, error) in enumerate(self.result.errors, 1):
                console.print(f"{i}. [red]{test}[/red]")
                console.print(f"   {error}")
        
        if self.result.was_successful:
            console.print("\n[bold green]Все тесты прошли успешно![/bold green]")
        else:
            console.print("\n[bold red]Тесты завершились с ошибками![/bold red]")


def run_tests(test_dir: str, verbosity: int = 1, include_patterns: List[str] = None, exclude_patterns: List[str] = None) -> TestResult:
    """
    Запускает тесты из указанной директории
    
    Args:
        test_dir (str): Директория с тестами
        verbosity (int): Уровень детализации вывода (0 - минимальный, 2 - максимальный)
        include_patterns (List[str]): Шаблоны для включения тестов
        exclude_patterns (List[str]): Шаблоны для исключения тестов
        
    Returns:
        TestResult: Результаты выполнения тестов
    """
    runner = TestRunner(verbosity, include_patterns, exclude_patterns)
    return runner.run(test_dir) 