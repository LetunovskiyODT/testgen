"""
Модуль для генерации конфигураций CI/CD систем.
"""

import os
import yaml
from typing import Dict, List, Optional
from rich.console import Console

console = Console()

def generate_github_actions_config(
    language: str,
    framework: str,
    python_versions: List[str] = ["3.8", "3.9", "3.10"],
    output_dir: str = ".github/workflows"
) -> str:
    """
    Генерирует конфигурацию GitHub Actions для тестирования проекта.
    
    Args:
        language (str): Язык программирования проекта
        framework (str): Тестовый фреймворк
        python_versions (List[str]): Список версий Python для тестирования
        output_dir (str): Директория для сохранения конфигурации
        
    Returns:
        str: Путь к сгенерированному файлу конфигурации
    """
    # Имя файла конфигурации в зависимости от языка
    filename = "tests.yml"
    
    # Создаем директорию, если она не существует
    os.makedirs(output_dir, exist_ok=True)
    
    # Формируем конфигурацию в зависимости от языка и фреймворка
    config = {}
    
    if language.lower() == "python":
        # Конфигурация для Python
        config = {
            "name": "Tests",
            "on": {
                "push": {
                    "branches": ["main"]
                },
                "pull_request": {
                    "branches": ["main"]
                }
            },
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "strategy": {
                        "matrix": {
                            "python-version": python_versions
                        }
                    },
                    "steps": [
                        {
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Set up Python ${{ matrix.python-version }}",
                            "uses": "actions/setup-python@v4",
                            "with": {
                                "python-version": "${{ matrix.python-version }}"
                            }
                        },
                        {
                            "name": "Install dependencies",
                            "run": "\n".join([
                                "python -m pip install --upgrade pip",
                                f"pip install {framework} pytest-cov",
                                "if [ -f requirements.txt ]; then pip install -r requirements.txt; fi"
                            ])
                        },
                        {
                            "name": "Test with pytest",
                            "run": "\n".join([
                                f"{framework} --cov=./ --cov-report=xml"
                            ])
                        },
                        {
                            "name": "Upload coverage to Codecov",
                            "uses": "codecov/codecov-action@v3",
                            "with": {
                                "file": "./coverage.xml",
                                "fail_ci_if_error": True
                            }
                        }
                    ]
                }
            }
        }
    elif language.lower() == "javascript":
        # Конфигурация для JavaScript
        config = {
            "name": "Tests",
            "on": {
                "push": {
                    "branches": ["main"]
                },
                "pull_request": {
                    "branches": ["main"]
                }
            },
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "strategy": {
                        "matrix": {
                            "node-version": ["14.x", "16.x", "18.x"]
                        }
                    },
                    "steps": [
                        {
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Use Node.js ${{ matrix.node-version }}",
                            "uses": "actions/setup-node@v3",
                            "with": {
                                "node-version": "${{ matrix.node-version }}",
                                "cache": "npm"
                            }
                        },
                        {
                            "name": "Install dependencies",
                            "run": "npm ci"
                        },
                        {
                            "name": "Run tests",
                            "run": f"npm test -- --coverage"
                        },
                        {
                            "name": "Upload coverage to Codecov",
                            "uses": "codecov/codecov-action@v3",
                            "with": {
                                "fail_ci_if_error": True
                            }
                        }
                    ]
                }
            }
        }
    elif language.lower() == "go":
        # Конфигурация для Go
        config = {
            "name": "Tests",
            "on": {
                "push": {
                    "branches": ["main"]
                },
                "pull_request": {
                    "branches": ["main"]
                }
            },
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "strategy": {
                        "matrix": {
                            "go-version": ["1.18", "1.19", "1.20"]
                        }
                    },
                    "steps": [
                        {
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Set up Go ${{ matrix.go-version }}",
                            "uses": "actions/setup-go@v4",
                            "with": {
                                "go-version": "${{ matrix.go-version }}"
                            }
                        },
                        {
                            "name": "Install dependencies",
                            "run": "go mod download"
                        },
                        {
                            "name": "Run tests",
                            "run": "go test -race -coverprofile=coverage.txt -covermode=atomic ./..."
                        },
                        {
                            "name": "Upload coverage to Codecov",
                            "uses": "codecov/codecov-action@v3",
                            "with": {
                                "file": "./coverage.txt",
                                "fail_ci_if_error": True
                            }
                        }
                    ]
                }
            }
        }
    else:
        # Базовая конфигурация для других языков
        config = {
            "name": "Tests",
            "on": {
                "push": {
                    "branches": ["main"]
                },
                "pull_request": {
                    "branches": ["main"]
                }
            },
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Run tests",
                            "run": "echo 'Add test command for " + language + " here'"
                        }
                    ]
                }
            }
        }
    
    # Полный путь к файлу конфигурации
    config_path = os.path.join(output_dir, filename)
    
    # Сохраняем конфигурацию в файл
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    return config_path


def generate_gitlab_ci_config(
    language: str,
    framework: str,
    output_path: str = ".gitlab-ci.yml"
) -> str:
    """
    Генерирует конфигурацию GitLab CI для тестирования проекта.
    
    Args:
        language (str): Язык программирования проекта
        framework (str): Тестовый фреймворк
        output_path (str): Путь для сохранения конфигурации
        
    Returns:
        str: Путь к сгенерированному файлу конфигурации
    """
    # Формируем конфигурацию в зависимости от языка и фреймворка
    config = {}
    
    if language.lower() == "python":
        # Конфигурация для Python
        config = {
            "image": "python:3.9",
            "stages": ["test"],
            "before_script": [
                "pip install -r requirements.txt",
                f"pip install {framework} pytest-cov"
            ],
            "test": {
                "stage": "test",
                "script": [
                    f"{framework} --cov=./ --cov-report=xml",
                    "coverage report"
                ],
                "artifacts": {
                    "reports": {
                        "coverage_report": {
                            "coverage_format": "cobertura",
                            "path": "coverage.xml"
                        }
                    }
                }
            }
        }
    elif language.lower() == "javascript":
        # Конфигурация для JavaScript
        config = {
            "image": "node:16",
            "stages": ["test"],
            "before_script": [
                "npm ci"
            ],
            "test": {
                "stage": "test",
                "script": [
                    "npm test -- --coverage"
                ],
                "artifacts": {
                    "reports": {
                        "coverage_report": {
                            "coverage_format": "cobertura",
                            "path": "coverage/cobertura-coverage.xml"
                        }
                    }
                }
            }
        }
    elif language.lower() == "go":
        # Конфигурация для Go
        config = {
            "image": "golang:1.19",
            "stages": ["test"],
            "before_script": [
                "go mod download"
            ],
            "test": {
                "stage": "test",
                "script": [
                    "go test -race -coverprofile=coverage.txt -covermode=atomic ./...",
                    "go tool cover -func=coverage.txt"
                ],
                "artifacts": {
                    "paths": ["coverage.txt"]
                }
            }
        }
    else:
        # Базовая конфигурация для других языков
        config = {
            "stages": ["test"],
            "test": {
                "stage": "test",
                "script": [
                    f"echo 'Add test command for {language} here'"
                ]
            }
        }
    
    # Сохраняем конфигурацию в файл
    with open(output_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    return output_path


def generate_circle_ci_config(
    language: str,
    framework: str,
    output_dir: str = ".circleci"
) -> str:
    """
    Генерирует конфигурацию CircleCI для тестирования проекта.
    
    Args:
        language (str): Язык программирования проекта
        framework (str): Тестовый фреймворк
        output_dir (str): Директория для сохранения конфигурации
        
    Returns:
        str: Путь к сгенерированному файлу конфигурации
    """
    # Создаем директорию, если она не существует
    os.makedirs(output_dir, exist_ok=True)
    
    # Полный путь к файлу конфигурации
    config_path = os.path.join(output_dir, "config.yml")
    
    # Формируем конфигурацию в зависимости от языка и фреймворка
    config = {}
    
    if language.lower() == "python":
        # Конфигурация для Python
        config = {
            "version": 2.1,
            "orbs": {
                "python": "circleci/python@1.5"
            },
            "jobs": {
                "build-and-test": {
                    "docker": [
                        {"image": "cimg/python:3.9"}
                    ],
                    "steps": [
                        "checkout",
                        {"run": {"name": "Install dependencies", "command": "\n".join([
                            "python -m venv venv",
                            ". venv/bin/activate",
                            "pip install -r requirements.txt",
                            f"pip install {framework} pytest-cov"
                        ])}},
                        {"run": {"name": "Run tests", "command": "\n".join([
                            ". venv/bin/activate",
                            f"{framework} --cov=./ --cov-report=xml"
                        ])}},
                        {"store_artifacts": {"path": "coverage.xml"}}
                    ]
                }
            },
            "workflows": {
                "main": {
                    "jobs": ["build-and-test"]
                }
            }
        }
    elif language.lower() == "javascript":
        # Конфигурация для JavaScript
        config = {
            "version": 2.1,
            "orbs": {
                "node": "circleci/node@5.0.2"
            },
            "jobs": {
                "build-and-test": {
                    "docker": [
                        {"image": "cimg/node:16.14"}
                    ],
                    "steps": [
                        "checkout",
                        {"node/install-packages": {"pkg-manager": "npm"}},
                        {"run": {"name": "Run tests", "command": "npm test -- --coverage"}},
                        {"store_artifacts": {"path": "coverage"}}
                    ]
                }
            },
            "workflows": {
                "main": {
                    "jobs": ["build-and-test"]
                }
            }
        }
    elif language.lower() == "go":
        # Конфигурация для Go
        config = {
            "version": 2.1,
            "jobs": {
                "build-and-test": {
                    "docker": [
                        {"image": "cimg/go:1.19"}
                    ],
                    "steps": [
                        "checkout",
                        {"run": {"name": "Install dependencies", "command": "go mod download"}},
                        {"run": {"name": "Run tests", "command": "go test -race -coverprofile=coverage.txt -covermode=atomic ./..."}},
                        {"store_artifacts": {"path": "coverage.txt"}}
                    ]
                }
            },
            "workflows": {
                "main": {
                    "jobs": ["build-and-test"]
                }
            }
        }
    else:
        # Базовая конфигурация для других языков
        config = {
            "version": 2.1,
            "jobs": {
                "build-and-test": {
                    "docker": [
                        {"image": "cimg/base:2022.06"}
                    ],
                    "steps": [
                        "checkout",
                        {"run": {"name": "Run tests", "command": f"echo 'Add test command for {language} here'"}}
                    ]
                }
            },
            "workflows": {
                "main": {
                    "jobs": ["build-and-test"]
                }
            }
        }
    
    # Сохраняем конфигурацию в файл
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    return config_path


def generate_ci_config(language: str, framework: str, ci_type: str, output_path: str = ".") -> str:
    """
    Генерирует конфигурацию для CI в зависимости от типа CI.
    
    Args:
        language (str): Язык программирования проекта
        framework (str): Тестовый фреймворк
        ci_type (str): Тип CI (github, gitlab, circle)
        output_path (str): Путь для сохранения конфигурации
        
    Returns:
        str: Путь к сгенерированному файлу конфигурации
    """
    ci_type = ci_type.lower()
    
    if ci_type == "github":
        output_dir = os.path.join(output_path, ".github", "workflows")
        return generate_github_actions_config(language, framework, output_dir=output_dir)
    elif ci_type == "gitlab":
        output_file = os.path.join(output_path, ".gitlab-ci.yml")
        return generate_gitlab_ci_config(language, framework, output_path=output_file)
    elif ci_type == "circle":
        output_dir = os.path.join(output_path, ".circleci")
        return generate_circle_ci_config(language, framework, output_dir=output_dir)
    else:
        console.print(f"[red]Неподдерживаемый тип CI: {ci_type}[/red]")
        console.print("[yellow]Поддерживаемые типы: github, gitlab, circle[/yellow]")
        return "" 