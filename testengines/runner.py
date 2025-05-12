import os
import subprocess
from typing import Dict, List, Optional, Tuple
from rich.console import Console
from rich.progress import Progress

console = Console()

class TestResult:
    """Класс для хранения результатов тестирования"""
    def __init__(self, success: bool, output: str, errors: str = "", duration: float = 0.0):
        self.success = success
        self.output = output
        self.errors = errors
        self.duration = duration

def run_tests(language: str, framework: str, test_path: str, verbose: bool = False) -> TestResult:
    """
    Запускает тесты для указанного языка и фреймворка.
    
    Args:
        language (str): Язык программирования
        framework (str): Тестовый фреймворк
        test_path (str): Путь к директории с тестами
        verbose (bool): Флаг подробного вывода
        
    Returns:
        TestResult: Результат выполнения тестов
    """
    # Словарь команд для запуска тестов для разных языков и фреймворков
    commands = {
        "python": {
            "pytest": ["pytest", test_path, "--color=yes"],
            "unittest": ["python", "-m", "unittest", "discover", test_path]
        },
        "javascript": {
            "jest": ["npx", "jest", test_path],
            "mocha": ["npx", "mocha", test_path]
        },
        "go": {
            "testing": ["go", "test", "./..." if test_path == "." else f"./{test_path}/..."]
        },
        "java": {
            "junit": ["./gradlew", "test"],
            "testng": ["./gradlew", "test"]
        },
        "ruby": {
            "rspec": ["bundle", "exec", "rspec", test_path],
            "minitest": ["ruby", "-Ilib:test", test_path]
        },
        "rust": {
            "cargo-test": ["cargo", "test"]
        },
        "php": {
            "phpunit": ["./vendor/bin/phpunit", test_path]
        },
        "csharp": {
            "nunit": ["dotnet", "test", "--filter", "TestCategory=NUnit"],
            "xunit": ["dotnet", "test", "--filter", "TestCategory=XUnit"],
            "mstest": ["dotnet", "test", "--filter", "TestCategory=MSTest"]
        }
        # Добавить другие языки и фреймворки по необходимости
    }
    
    try:
        if language.lower() not in commands:
            return TestResult(False, "", f"Язык {language} не поддерживается")
            
        if framework.lower() not in commands[language.lower()]:
            return TestResult(False, "", f"Фреймворк {framework} не поддерживается для языка {language}")
            
        command = commands[language.lower()][framework.lower()]
        
        # Добавляем флаги для подробного вывода, если требуется
        if verbose:
            if language.lower() == "python" and framework.lower() == "pytest":
                command.append("-v")
            elif language.lower() == "python" and framework.lower() == "unittest":
                command.append("-v")
            elif language.lower() == "javascript" and framework.lower() == "jest":
                command.append("--verbose")
            elif language.lower() == "javascript" and framework.lower() == "mocha":
                command.append("--reporter=spec")
            elif language.lower() == "go" and framework.lower() == "testing":
                command.append("-v")
            elif language.lower() == "ruby" and framework.lower() == "rspec":
                command.append("--format=documentation")
            # Добавить другие флаги для других языков и фреймворков
            
        with Progress() as progress:
            task = progress.add_task(f"Запуск тестов ({language}/{framework})", total=1)
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            success = process.returncode == 0
            
            progress.update(task, completed=1)
            
        return TestResult(success, stdout, stderr)
        
    except Exception as e:
        return TestResult(False, "", str(e))


def generate_report(test_result: TestResult, format: str = "html", output_path: str = "report") -> str:
    """
    Генерирует отчет о тестировании.
    
    Args:
        test_result (TestResult): Результаты тестирования
        format (str): Формат отчета (html, markdown, text)
        output_path (str): Путь для сохранения отчета
        
    Returns:
        str: Путь к сгенерированному отчету
    """
    # Создаем директорию для отчета, если она не существует
    os.makedirs(output_path, exist_ok=True)
    
    # Путь к файлу отчета
    file_extension = {"html": ".html", "markdown": ".md", "text": ".txt"}.get(format, ".txt")
    report_file = os.path.join(output_path, f"test_report{file_extension}")
    
    # Генерируем содержимое отчета в зависимости от формата
    if format == "html":
        content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>TestGen Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .success {{ color: green; }}
                .failure {{ color: red; }}
                pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>TestGen Report</h1>
            <p>Status: <span class="{'success' if test_result.success else 'failure'}">
                {test_result.success and 'SUCCESS' or 'FAILURE'}
            </span></p>
            <h2>Output:</h2>
            <pre>{test_result.output}</pre>
            {f'<h2>Errors:</h2><pre>{test_result.errors}</pre>' if test_result.errors else ''}
        </body>
        </html>
        """
    elif format == "markdown":
        content = f"""
        # TestGen Report
        
        Status: **{test_result.success and 'SUCCESS' or 'FAILURE'}**
        
        ## Output:
        
        ```
        {test_result.output}
        ```
        
        {f'## Errors:\n\n```\n{test_result.errors}\n```' if test_result.errors else ''}
        """
    else:  # text
        content = f"""
        TestGen Report
        ==============
        
        Status: {test_result.success and 'SUCCESS' or 'FAILURE'}
        
        Output:
        -------
        {test_result.output}
        
        {f'Errors:\n-------\n{test_result.errors}' if test_result.errors else ''}
        """
    
    # Записываем отчет в файл
    with open(report_file, "w") as f:
        f.write(content.strip())
    
    return report_file 