#!/usr/bin/env python3
"""
Скрипт для создания репозитория GitHub через API и загрузки файлов проекта.
"""

import os
import sys
import base64
import getpass
from typing import Dict, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ci.github_api import create_github_repo, configure_github_actions, push_files_to_github

console = Console()

def create_repository(repo_name: str, description: str, private: bool = False, token: Optional[str] = None) -> Optional[str]:
    """
    Создает репозиторий на GitHub и возвращает имя пользователя владельца.
    
    Args:
        repo_name (str): Имя репозитория
        description (str): Описание репозитория
        private (bool): Приватный или публичный репозиторий
        token (Optional[str]): GitHub токен авторизации
        
    Returns:
        Optional[str]: Имя пользователя владельца репозитория или None в случае ошибки
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Создание репозитория {repo_name}...", total=1)
        
        # Создаем репозиторий
        success, result = create_github_repo(repo_name, description, private, token)
        
        progress.update(task, completed=1)
        
        if success:
            # Получаем имя пользователя из URL репозитория
            repo_url = result.get("html_url", "")
            owner = repo_url.split("/")[-2] if repo_url else None
            
            console.print(f"[green]Репозиторий успешно создан:[/green] {repo_url}")
            return owner
        else:
            error_msg = result.get("error", "Неизвестная ошибка")
            console.print(f"[red]Ошибка при создании репозитория:[/red] {error_msg}")
            if "message" in result:
                console.print(f"[red]Сообщение API:[/red] {result['message']}")
            return None


def push_repo_files(owner: str, repo_name: str, token: Optional[str] = None) -> bool:
    """
    Загружает основные файлы проекта в созданный репозиторий.
    
    Args:
        owner (str): Имя пользователя владельца репозитория
        repo_name (str): Имя репозитория
        token (Optional[str]): GitHub токен авторизации
        
    Returns:
        bool: True в случае успеха, False в случае ошибки
    """
    # Список основных файлов, которые мы хотим загрузить
    files_to_push = [
        "requirements.txt",
        "README.md",
        "testgen.py",
        "main.py",
        "LICENSE",
        "pytest.ini",
        ".gitignore",
        "langs/lang_detector.py",
        "testengines/runner.py",
        "ui/tui.py",
        "cmd/testgen/main.py",
        "tests/test_lang_detector.py"
    ]
    
    # Создаем директории
    directories = [
        "langs",
        "testengines",
        "ui",
        "cmd/testgen",
        "tests",
        ".github/workflows"
    ]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        main_task = progress.add_task("Загрузка файлов в репозиторий...", total=len(files_to_push) + 1)
        
        # Считываем содержимое файлов
        files_data = {}
        
        for file_path in files_to_push:
            progress.update(main_task, description=f"Чтение файла {file_path}...")
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    files_data[file_path] = base64.b64encode(content.encode("utf-8")).decode("utf-8")
            except Exception as e:
                console.print(f"[yellow]Предупреждение: не удалось прочитать файл {file_path}:[/yellow] {str(e)}")
                
            progress.update(main_task, advance=1)
        
        # Загружаем GitHub Actions конфигурацию
        progress.update(main_task, description="Загрузка GitHub Actions конфигурации...")
        
        try:
            with open(".github/workflows/tests.yml", "r", encoding="utf-8") as f:
                content = f.read()
                
                # Создаем директорию .github/workflows в репозитории
                success, result = push_files_to_github(
                    owner,
                    repo_name,
                    {".github/workflows/tests.yml": base64.b64encode(content.encode("utf-8")).decode("utf-8")},
                    "Добавлена конфигурация GitHub Actions",
                    token
                )
                
                if not success:
                    console.print("[yellow]Предупреждение: не удалось загрузить GitHub Actions конфигурацию[/yellow]")
                    if result.get("errors"):
                        for error in result["errors"]:
                            console.print(f"[yellow]- Файл {error.get('file')}: {error.get('error')}[/yellow]")
        except Exception as e:
            console.print(f"[yellow]Предупреждение: не удалось загрузить GitHub Actions конфигурацию:[/yellow] {str(e)}")
        
        progress.update(main_task, advance=1)
        
        # Загружаем остальные файлы
        progress.update(main_task, description="Загрузка основных файлов проекта...")
        
        success, result = push_files_to_github(
            owner,
            repo_name,
            files_data,
            "Начальная загрузка проекта TestGen",
            token
        )
        
        if success:
            console.print("[green]Файлы успешно загружены в репозиторий![/green]")
            return True
        else:
            console.print("[red]Ошибка при загрузке файлов в репозиторий[/red]")
            if result.get("errors"):
                for error in result["errors"]:
                    console.print(f"[red]- Файл {error.get('file')}: {error.get('error')}[/red]")
            return False


def main():
    """Основная функция скрипта"""
    console.print(Panel.fit("Создание репозитория GitHub для проекта TestGen", border_style="bright_blue"))
    
    # Получаем токен GitHub
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        console.print("[yellow]Токен GitHub не найден в переменных окружения[/yellow]")
        console.print("Пожалуйста, введите ваш персональный токен GitHub (токен не будет отображаться):")
        token = getpass.getpass()
    
    # Запрашиваем имя репозитория
    repo_name = console.input("Введите имя репозитория [cyan](testgen)[/cyan]: ") or "testgen"
    
    # Запрашиваем описание репозитория
    description = console.input("Введите описание репозитория [cyan](CLI-утилита для генерации и запуска тестов)[/cyan]: ") or "CLI-утилита для генерации и запуска тестов"
    
    # Запрашиваем тип репозитория
    is_private = console.input("Сделать репозиторий приватным? [cyan](n/y)[/cyan]: ").lower() == "y"
    
    # Создаем репозиторий
    owner = create_repository(repo_name, description, is_private, token)
    
    if owner:
        # Загружаем файлы в репозиторий
        success = push_repo_files(owner, repo_name, token)
        
        if success:
            console.print(f"\n[green]Репозиторий успешно создан и заполнен![/green]")
            console.print(f"URL репозитория: [link]https://github.com/{owner}/{repo_name}[/link]")
        else:
            console.print("\n[yellow]Репозиторий создан, но загрузка файлов не завершена.[/yellow]")
            console.print(f"Вы можете загрузить файлы вручную: [link]https://github.com/{owner}/{repo_name}[/link]")
    else:
        console.print("\n[red]Не удалось создать репозиторий. Пожалуйста, проверьте токен GitHub и попробуйте снова.[/red]")


if __name__ == "__main__":
    main() 