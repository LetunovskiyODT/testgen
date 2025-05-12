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


def get_source_files(directory: str, language: str) -> List[str]:
    """
    Находит все исходные файлы указанного языка в директории.
    
    Args:
        directory (str): Директория для поиска
        language (str): Язык программирования
        
    Returns:
        List[str]: Список путей к найденным файлам
    """
    file_patterns = {
        "python": ["*.py"],
        "javascript": ["*.js", "*.jsx", "*.ts", "*.tsx"],
        "go": ["*.go"],
        "java": ["*.java"],
        "ruby": ["*.rb"],
        "rust": ["*.rs"],
        "php": ["*.php"],
        "csharp": ["*.cs"],
    }
    
    # Исключаем файлы тестов
    exclude_patterns = {
        "python": ["test_*.py", "*_test.py"],
        "javascript": ["*.test.js", "*.spec.js", "*-test.js"],
        "go": ["*_test.go"],
        "java": ["*Test.java"],
        "ruby": ["*_spec.rb", "*_test.rb"],
        "rust": ["*_test.rs"],
        "php": ["*Test.php"],
        "csharp": ["*Test.cs", "*Tests.cs"],
    }
    
    patterns = file_patterns.get(language.lower(), [])
    if not patterns:
        return []
    
    exclude_list = exclude_patterns.get(language.lower(), [])
    
    source_files = []
    for pattern in patterns:
        for file_path in glob.glob(os.path.join(directory, "**", pattern), recursive=True):
            # Проверяем, что это не тестовый файл
            is_test_file = any(
                os.path.basename(file_path).lower().endswith(exclude_pattern[1:].lower())
                or os.path.basename(file_path).lower().startswith(exclude_pattern[:-1].lower())
                for exclude_pattern in exclude_list if "*" in exclude_pattern
            )
            
            if not is_test_file:
                source_files.append(file_path)
    
    return source_files


def generate_tests_for_language(directory: str, language: str, framework: Optional[str] = None, output_dir: Optional[str] = None) -> List[str]:
    """
    Генерирует тесты для всех исходных файлов указанного языка в директории.
    
    Args:
        directory (str): Директория для поиска исходных файлов
        language (str): Язык программирования
        framework (Optional[str]): Тестовый фреймворк (если None, выбирается первый доступный)
        output_dir (Optional[str]): Директория для сохранения тестов (если None, возвращает тесты как строки)
        
    Returns:
        List[str]: Список путей к сгенерированным тестам
    """
    # Определяем язык и фреймворк
    if not language:
        language = detect_project_language(directory)
        if not language:
            raise ValueError("Не удалось определить язык программирования")
    
    # Выбираем фреймворк по умолчанию, если не указан
    if not framework:
        frameworks = get_available_test_frameworks(language)
        if not frameworks:
            raise ValueError(f"Для языка {language} не найдены доступные тестовые фреймворки")
        framework = frameworks[0]
    
    # Находим исходные файлы
    source_files = get_source_files(directory, language)
    if not source_files:
        raise ValueError(f"Не найдены исходные файлы языка {language} в директории {directory}")
    
    # Генерируем тесты для каждого файла
    generated_tests = []
    
    # Импортируем соответствующий генератор для каждого языка
    if language.lower() == "python":
        from langs.python_generator import generate_tests as py_gen
        for file_path in source_files:
            test_path = py_gen(file_path, framework, output_dir)
            if test_path:
                generated_tests.append(test_path)
    
    elif language.lower() == "javascript":
        from langs.javascript_generator import generate_tests as js_gen
        for file_path in source_files:
            test_path = js_gen(file_path, output_dir)
            if test_path:
                generated_tests.append(test_path)
    
    elif language.lower() == "go":
        from langs.go_generator import generate_tests as go_gen
        for file_path in source_files:
            test_path = go_gen(file_path, output_dir)
            if test_path:
                generated_tests.append(test_path)
    
    # TODO: Добавить поддержку других языков
    
    return generated_tests 