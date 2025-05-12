#!/usr/bin/env python3
import typer
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint
import pyfiglet
import os
import sys

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from langs import lang_detector
from testengines import runner
from ui import tui

app = typer.Typer(help="TestGen - утилита для генерации и запуска тестов")
console = Console()

def show_header():
    """Отображение заголовка приложения"""
    header = pyfiglet.figlet_format("TestGen", font="slant")
    console.print(Panel.fit(header, border_style="bright_blue"))
    console.print("Утилита для генерации и запуска тестов", style="italic")

@app.command()
def init(
    language: str = typer.Option(None, "--lang", "-l", help="Язык программирования проекта"),
    test_framework: str = typer.Option(None, "--framework", "-f", help="Тестовый фреймворк"),
):
    """Инициализация тестового окружения в проекте"""
    show_header()
    console.print("[bold green]Инициализация проекта[/bold green]")
    
    # Если язык не указан, пытаемся определить его автоматически
    if not language:
        detected_lang = lang_detector.detect_project_language()
        if detected_lang:
            console.print(f"Обнаружен язык программирования: [bold]{detected_lang}[/bold]")
            language = detected_lang
        else:
            console.print("[yellow]Не удалось автоматически определить язык программирования[/yellow]")
            # Здесь можно добавить интерактивный выбор языка
    
    # TODO: Добавить логику инициализации проекта
    console.print(f"Инициализация проекта для языка {language} завершена!")


@app.command()
def gen(
    path: str = typer.Argument(".", help="Путь к файлам для генерации тестов"),
    language: str = typer.Option(None, "--lang", "-l", help="Язык программирования"),
    test_framework: str = typer.Option(None, "--framework", "-f", help="Тестовый фреймворк"),
):
    """Генерация тестов для указанных файлов"""
    show_header()
    console.print(f"[bold green]Генерация тестов для[/bold green]: {path}")
    
    # TODO: Добавить логику генерации тестов


@app.command()
def run(
    path: str = typer.Argument(".", help="Путь к тестам для запуска"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Подробный вывод"),
):
    """Запуск тестов"""
    show_header()
    console.print(f"[bold green]Запуск тестов в[/bold green]: {path}")
    
    # TODO: Добавить логику запуска тестов


@app.command()
def config():
    """Настройка конфигурации TestGen"""
    show_header()
    console.print("[bold green]Настройка конфигурации[/bold green]")
    
    # TODO: Добавить логику настройки конфигурации


@app.command()
def report(
    format: str = typer.Option("html", help="Формат отчета (html, markdown, text)"),
    output: str = typer.Option("report", help="Путь для сохранения отчета"),
):
    """Генерация отчета о тестировании"""
    show_header()
    console.print(f"[bold green]Генерация отчета в формате[/bold green]: {format}")
    
    # TODO: Добавить логику генерации отчетов


@app.command()
def ci(
    type: str = typer.Option("github", help="Тип CI (github, gitlab, jenkins)"),
    output: str = typer.Option(".", help="Путь для сохранения конфигурации CI"),
):
    """Генерация конфигурации для CI"""
    show_header()
    console.print(f"[bold green]Генерация конфигурации для CI[/bold green]: {type}")
    
    # TODO: Добавить логику генерации конфигурации CI


if __name__ == "__main__":
    app() 