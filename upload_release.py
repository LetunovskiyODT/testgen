import os
import requests
import json
import sys

# Настройки GitHub
REPO_OWNER = "LetunovskiyODT"
REPO_NAME = "testgen"
TAG_NAME = "v1.0.0"
RELEASE_NAME = "TestGen v1.0.0"
RELEASE_BODY = """
# TestGen v1.0.0

Первый официальный релиз TestGen - мощной утилиты для генерации тестов для различных языков программирования.

## Что включено:

- Поддержка множества языков программирования
- Полный исходный код
- Портативная версия
- Установщик для Windows

## Скачать:

- [Портативная версия](https://github.com/LetunovskiyODT/testgen/releases/latest/download/TestGen_Portable.zip)
- [Полная версия](https://github.com/LetunovskiyODT/testgen/releases/latest/download/TestGen_Full.zip)
- [Установщик для Windows](https://github.com/LetunovskiyODT/testgen/releases/latest/download/TestGen_Setup.bat)
"""

# Путь к файлам для загрузки
FILES_TO_UPLOAD = [
    "release_files/TestGen_Portable.zip",
    "release_files/TestGen_Full.zip",
    "release_files/TestGen_Setup.bat"
]

def print_token_instructions():
    """Выводит инструкции по созданию токена GitHub"""
    print("\n=== Инструкции по созданию токена GitHub ===")
    print("1. Перейдите на https://github.com/settings/tokens")
    print("2. Нажмите 'Generate new token' -> 'Generate new token (classic)'")
    print("3. Введите описание токена, например 'TestGen Release Token'")
    print("4. ВАЖНО: Выберите разрешения 'repo' (полный доступ к репозиторию)")
    print("5. Нажмите 'Generate token'")
    print("6. Скопируйте созданный токен и используйте его в этом скрипте")
    print("=== Конец инструкций ===\n")

def main():
    print_token_instructions()
    token = input("Введите GitHub токен: ")
    
    # Проверка формата токена
    if not token.startswith("ghp_") and not token.startswith("github_pat_"):
        print("Предупреждение: Формат токена выглядит необычно. Убедитесь, что вы используете персональный токен доступа GitHub.")
        confirm = input("Продолжить? (y/n): ")
        if confirm.lower() != "y":
            print("Операция отменена.")
            return
    
    # Заголовки для запросов
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Проверяем доступность API GitHub
    try:
        test_response = requests.get(f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}", headers=headers)
        if test_response.status_code == 404:
            print(f"Ошибка: Репозиторий {REPO_OWNER}/{REPO_NAME} не найден.")
            return
        elif test_response.status_code != 200:
            print(f"Ошибка доступа к репозиторию: {test_response.status_code}")
            print(f"Ответ: {test_response.text}")
            return
    except Exception as e:
        print(f"Ошибка соединения с GitHub: {str(e)}")
        return
    
    # Проверяем, существует ли релиз
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/tags/{TAG_NAME}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(f"Релиз с тегом {TAG_NAME} уже существует.")
        release = response.json()
    else:
        # Создаем новый релиз
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
        data = {
            "tag_name": TAG_NAME,
            "name": RELEASE_NAME,
            "body": RELEASE_BODY,
            "draft": False,
            "prerelease": False
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code != 201:
                print(f"Ошибка при создании релиза: {response.text}")
                
                if response.status_code == 403 and "personal access token" in response.text:
                    print("\nОшибка 403: У токена недостаточно прав.")
                    print("Убедитесь, что токен имеет разрешение 'repo' (полный доступ к репозиторию).")
                    print_token_instructions()
                    return
                
                sys.exit(1)
                
            release = response.json()
            print(f"Создан новый релиз: {RELEASE_NAME}")
        except Exception as e:
            print(f"Ошибка при создании релиза: {str(e)}")
            return
    
    # Загружаем файлы
    for file_path in FILES_TO_UPLOAD:
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден. Пропускаем.")
            continue
            
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        print(f"Загрузка {file_name} ({file_size} байт)...")
        
        # Определение content type
        content_type = "application/octet-stream"
        if file_name.endswith(".zip"):
            content_type = "application/zip"
        elif file_name.endswith(".exe"):
            content_type = "application/vnd.microsoft.portable-executable"
        
        try:
            with open(file_path, "rb") as file:
                upload_url = release["upload_url"].replace("{?name,label}", "")
                headers_upload = headers.copy()
                headers_upload["Content-Type"] = content_type
                
                params = {
                    "name": file_name
                }
                
                response = requests.post(
                    upload_url,
                    headers=headers_upload,
                    params=params,
                    data=file
                )
                
                if response.status_code == 201:
                    print(f"Файл {file_name} успешно загружен!")
                else:
                    print(f"Ошибка при загрузке файла {file_name}: {response.text}")
        except Exception as e:
            print(f"Ошибка при загрузке файла {file_name}: {str(e)}")

if __name__ == "__main__":
    main() 