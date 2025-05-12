import os
import tempfile
import pytest
from langs.lang_detector import detect_project_language, get_available_test_frameworks

def test_get_available_test_frameworks():
    """Тестирует получение списка доступных тестовых фреймворков"""
    # Проверка для Python
    frameworks = get_available_test_frameworks("python")
    assert "pytest" in frameworks
    assert "unittest" in frameworks
    
    # Проверка для JavaScript
    frameworks = get_available_test_frameworks("javascript")
    assert "jest" in frameworks
    assert "mocha" in frameworks
    
    # Проверка для неподдерживаемого языка
    frameworks = get_available_test_frameworks("nonexistent")
    assert frameworks == []

def test_detect_project_language_empty_dir():
    """Тестирует определение языка в пустой директории"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        detected_lang = detect_project_language(tmp_dir)
        assert detected_lang is None

def test_detect_project_language_python():
    """Тестирует определение языка Python"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Создаем файлы Python
        with open(os.path.join(tmp_dir, "main.py"), "w") as f:
            f.write("print('Hello, World!')")
        with open(os.path.join(tmp_dir, "requirements.txt"), "w") as f:
            f.write("pytest==7.3.1")
            
        detected_lang = detect_project_language(tmp_dir)
        assert detected_lang == "python"

def test_detect_project_language_javascript():
    """Тестирует определение языка JavaScript"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Создаем файлы JavaScript
        with open(os.path.join(tmp_dir, "index.js"), "w") as f:
            f.write("console.log('Hello, World!');")
        with open(os.path.join(tmp_dir, "package.json"), "w") as f:
            f.write('{"name": "test", "version": "1.0.0"}')
            
        detected_lang = detect_project_language(tmp_dir)
        assert detected_lang == "javascript"

def test_detect_project_language_mixed():
    """Тестирует определение языка в директории с файлами разных языков"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Создаем файлы Python
        with open(os.path.join(tmp_dir, "main.py"), "w") as f:
            f.write("print('Hello, World!')")
            
        # Создаем файлы JavaScript (больше файлов)
        with open(os.path.join(tmp_dir, "index.js"), "w") as f:
            f.write("console.log('Hello, World!');")
        with open(os.path.join(tmp_dir, "app.js"), "w") as f:
            f.write("// App")
        with open(os.path.join(tmp_dir, "utils.js"), "w") as f:
            f.write("// Utils")
        with open(os.path.join(tmp_dir, "package.json"), "w") as f:
            f.write('{"name": "test", "version": "1.0.0"}')
            
        detected_lang = detect_project_language(tmp_dir)
        assert detected_lang == "javascript" 