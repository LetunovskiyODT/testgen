from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, Input, Label
from textual.containers import Container, Horizontal, Vertical
from textual import events
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from typing import Dict, List, Optional

console = Console()

class TestGenApp(App):
    """Основное приложение TestGen с текстовым интерфейсом"""
    
    CSS = """
    Screen {
        background: #0f111a;
    }
    
    Header {
        background: #1e88e5;
        color: white;
    }
    
    Footer {
        background: #1e88e5;
        color: white;
    }
    
    .title {
        text-align: center;
        padding: 1;
        color: #1e88e5;
        text-style: bold;
    }
    
    .container {
        margin: 1;
        padding: 1;
        border: solid #1e88e5;
    }
    
    Button {
        margin: 1;
        min-width: 15;
    }
    
    #main-container {
        height: 100%;
        width: 100%;
    }
    
    #results {
        height: 60%;
        background: #1a1c25;
        color: white;
        overflow-y: auto;
        padding: 1;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Выход"),
        ("r", "run_tests", "Запустить тесты"),
        ("g", "generate_tests", "Сгенерировать тесты"),
    ]
    
    def compose(self) -> ComposeResult:
        """Создает интерфейс приложения"""
        yield Header(show_clock=True)
        
        with Container(id="main-container"):
            yield Label("TestGen - Утилита для генерации и запуска тестов", classes="title")
            
            with Horizontal(classes="container"):
                yield Button("Инициализация", id="init-btn", variant="primary")
                yield Button("Генерация тестов", id="gen-btn", variant="primary")
                yield Button("Запуск тестов", id="run-btn", variant="primary")
                yield Button("Настройка", id="config-btn", variant="primary")
                yield Button("Отчет", id="report-btn", variant="primary")
                yield Button("CI", id="ci-btn", variant="primary")
            
            with Container(id="results", classes="container"):
                yield Static("Добро пожаловать в TestGen!\n\nВыберите команду для начала работы.")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Обработчик нажатия на кнопки"""
        button_id = event.button.id
        
        if button_id == "init-btn":
            self.action_init_project()
        elif button_id == "gen-btn":
            self.action_generate_tests()
        elif button_id == "run-btn":
            self.action_run_tests()
        elif button_id == "config-btn":
            self.action_config()
        elif button_id == "report-btn":
            self.action_report()
        elif button_id == "ci-btn":
            self.action_ci()
    
    def action_init_project(self) -> None:
        """Действие инициализации проекта"""
        results = self.query_one("#results", Static)
        results.update("Инициализация проекта...\n\nОпределение языка программирования...")
        # Здесь будет логика определения языка программирования и инициализации проекта
    
    def action_generate_tests(self) -> None:
        """Действие генерации тестов"""
        results = self.query_one("#results", Static)
        results.update("Генерация тестов...\n\nАнализ исходного кода...")
        # Здесь будет логика генерации тестов
    
    def action_run_tests(self) -> None:
        """Действие запуска тестов"""
        results = self.query_one("#results", Static)
        results.update("Запуск тестов...\n\nПоиск тестов...")
        # Здесь будет логика запуска тестов
    
    def action_config(self) -> None:
        """Действие настройки"""
        results = self.query_one("#results", Static)
        results.update("Настройка TestGen...\n\nЗагрузка конфигурации...")
        # Здесь будет логика настройки
    
    def action_report(self) -> None:
        """Действие генерации отчета"""
        results = self.query_one("#results", Static)
        results.update("Генерация отчета...\n\nАнализ результатов тестирования...")
        # Здесь будет логика генерации отчета
    
    def action_ci(self) -> None:
        """Действие генерации конфигурации CI"""
        results = self.query_one("#results", Static)
        results.update("Генерация конфигурации CI...\n\nПодготовка файлов...")
        # Здесь будет логика генерации конфигурации CI


def run_app() -> None:
    """Запускает текстовый интерфейс приложения"""
    app = TestGenApp()
    app.run()


def show_lang_select() -> Optional[str]:
    """
    Отображает интерактивный выбор языка программирования
    
    Returns:
        Optional[str]: Выбранный язык программирования или None, если пользователь отменил выбор
    """
    languages = [
        "python",
        "javascript",
        "go",
        "java",
        "ruby",
        "rust",
        "php",
        "csharp",
    ]
    
    console.print(Panel.fit("Выберите язык программирования:"))
    
    for i, lang in enumerate(languages, 1):
        console.print(f"{i}. {lang}")
    
    console.print("\nВведите номер языка (или 'q' для отмены):")
    choice = console.input("> ")
    
    if choice.lower() == 'q':
        return None
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(languages):
            return languages[index]
        else:
            console.print("[red]Неверный выбор[/red]")
            return show_lang_select()
    except ValueError:
        console.print("[red]Пожалуйста, введите число[/red]")
        return show_lang_select()


def show_framework_select(language: str) -> Optional[str]:
    """
    Отображает интерактивный выбор тестового фреймворка для указанного языка
    
    Args:
        language (str): Язык программирования
        
    Returns:
        Optional[str]: Выбранный тестовый фреймворк или None, если пользователь отменил выбор
    """
    frameworks = {
        "python": ["pytest", "unittest"],
        "javascript": ["jest", "mocha"],
        "go": ["testing"],
        "java": ["junit", "testng"],
        "ruby": ["rspec", "minitest"],
        "rust": ["cargo-test"],
        "php": ["phpunit"],
        "csharp": ["nunit", "xunit", "mstest"],
    }
    
    available_frameworks = frameworks.get(language.lower(), [])
    
    if not available_frameworks:
        console.print(f"[red]Для языка {language} нет доступных тестовых фреймворков[/red]")
        return None
    
    console.print(Panel.fit(f"Выберите тестовый фреймворк для {language}:"))
    
    for i, framework in enumerate(available_frameworks, 1):
        console.print(f"{i}. {framework}")
    
    console.print("\nВведите номер фреймворка (или 'q' для отмены):")
    choice = console.input("> ")
    
    if choice.lower() == 'q':
        return None
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(available_frameworks):
            return available_frameworks[index]
        else:
            console.print("[red]Неверный выбор[/red]")
            return show_framework_select(language)
    except ValueError:
        console.print("[red]Пожалуйста, введите число[/red]")
        return show_framework_select(language) 