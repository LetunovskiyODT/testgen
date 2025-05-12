# TestGen

CLI-утилита для генерации и запуска тестов для приложений на разных языках программирования.

![TestGen Demo](docs/demo.gif)

## Описание

TestGen - это мощный инструмент для автоматизации создания и запуска тестов для различных языков программирования. Утилита предоставляет удобный текстовый интерфейс пользователя (TUI) с использованием библиотек Rich и Textual.

### Поддерживаемые языки:

- Python (pytest, unittest)
- JavaScript (Jest, Mocha)
- Go (встроенный testing)
- Java (JUnit, TestNG)
- Ruby (RSpec, Minitest)
- Rust (cargo-test)
- PHP (PHPUnit)
- C# (NUnit, xUnit, MSTest)

## Установка

```bash
# Клонирование репозитория
git clone https://github.com/username/testgen.git
cd testgen

# Установка зависимостей
pip install -r requirements.txt
```

## Использование

### CLI-команды

```bash
# Инициализация проекта
python testgen.py init [--lang LANGUAGE] [--framework FRAMEWORK]

# Генерация тестов
python testgen.py gen [PATH] [--lang LANGUAGE] [--framework FRAMEWORK]

# Запуск тестов
python testgen.py run [PATH] [--verbose]

# Настройка конфигурации
python testgen.py config

# Генерация отчета
python testgen.py report [--format FORMAT] [--output OUTPUT]

# Генерация конфигурации CI
python testgen.py ci [--type TYPE] [--output OUTPUT]
```

### Интерактивный режим (TUI)

```bash
python -m ui.tui
```

## Примеры

### Инициализация проекта с автоматическим определением языка

```bash
python testgen.py init
```

### Генерация тестов для Python с использованием pytest

```bash
python testgen.py gen --lang python --framework pytest
```

### Запуск тестов с подробным выводом

```bash
python testgen.py run --verbose
```

### Генерация отчета в формате HTML

```bash
python testgen.py report --format html --output ./reports
```

### Генерация конфигурации для GitHub Actions

```bash
python testgen.py ci --type github
```

## Структура проекта

```
testgen/
├── cmd/               # Команды CLI
│   └── testgen/       # Основные команды
├── langs/             # Генераторы для разных языков
├── testengines/       # Запуск и анализ тестов
├── ui/                # Компоненты TUI
├── requirements.txt   # Зависимости проекта
└── README.md          # Документация
```

## Разработка

### Требования

- Python >= 3.7
- Rich
- Textual
- Typer
- PyYAML
- PyFiglet

### Запуск тестов

```bash
pytest
```

## Лицензия

MIT 