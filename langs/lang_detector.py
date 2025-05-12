import os
import glob
from typing import Optional, Dict, List

LANGUAGE_PATTERNS = {
    "python": ["*.py", "requirements.txt", "setup.py", "pyproject.toml"],
    "javascript": ["*.js", "package.json", "*.jsx", "*.ts", "*.tsx"],
    "go": ["*.go", "go.mod", "go.sum"],
    "java": ["*.java", "pom.xml", "build.gradle"],
    "ruby": ["*.rb", "Gemfile"],
    "rust": ["*.rs", "Cargo.toml"],
    "php": ["*.php", "composer.json"],
    "csharp": ["*.cs", "*.csproj", "*.sln"],
}

def detect_project_language(project_path: str = ".") -> Optional[str]:
    """
    Определяет основной язык программирования проекта на основе файлов в директории.
    
    Args:
        project_path (str): Путь к корневой директории проекта
        
    Returns:
        Optional[str]: Определенный язык программирования или None, если не удалось определить
    """
    language_scores = {lang: 0 for lang in LANGUAGE_PATTERNS}
    
    for lang, patterns in LANGUAGE_PATTERNS.items():
        for pattern in patterns:
            matching_files = glob.glob(os.path.join(project_path, "**", pattern), recursive=True)
            language_scores[lang] += len(matching_files)
    
    # Сортируем языки по количеству найденных файлов
    sorted_langs = sorted(language_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Если есть хотя бы один файл, возвращаем язык с наибольшим количеством файлов
    if sorted_langs and sorted_langs[0][1] > 0:
        return sorted_langs[0][0]
        
    return None


def get_available_test_frameworks(language: str) -> List[str]:
    """
    Возвращает список доступных тестовых фреймворков для указанного языка.
    
    Args:
        language (str): Язык программирования
        
    Returns:
        List[str]: Список доступных тестовых фреймворков
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
    
    return frameworks.get(language.lower(), []) 