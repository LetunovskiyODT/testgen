#!/usr/bin/env python3
"""
Простой скрипт запуска TestGen
"""

import os
import sys
from rich.console import Console
from rich.panel import Panel
import pyfiglet

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from langs.lang_detector import detect_project_language, get_available_test_frameworks

console = Console()

def show_header():
    """Отображение заголовка приложения"""
    header = pyfiglet.figlet_format("TestGen", font="slant")
    console.print(Panel.fit(header, border_style="bright_blue"))
    console.print("Утилита для генерации и запуска тестов", style="italic")

def init_project():
    """Инициализация тестового окружения в проекте"""
    show_header()
    console.print("[bold green]Инициализация проекта[/bold green]")
    
    # Определяем язык программирования
    detected_lang = detect_project_language()
    if detected_lang:
        console.print(f"Обнаружен язык программирования: [bold]{detected_lang}[/bold]")
        
        # Получаем доступные тестовые фреймворки
        frameworks = get_available_test_frameworks(detected_lang)
        console.print(f"Доступные тестовые фреймворки: [bold]{', '.join(frameworks)}[/bold]")
    else:
        console.print("[yellow]Не удалось автоматически определить язык программирования[/yellow]")
    
    console.print("\n[green]Инициализация проекта завершена![/green]")

if __name__ == "__main__":
    # Простое меню
    show_header()
    console.print("\nДоступные команды:")
    console.print("1. Инициализация проекта")
    console.print("2. Выход")
    
    choice = console.input("\nВыберите команду (1-2): ")
    
    if choice == "1":
        init_project()
    else:
        console.print("[yellow]Выход из программы[/yellow]") 