import requests
import os
import json
from typing import Dict, Optional, Tuple

def create_github_repo(repo_name: str, description: str = "", private: bool = False, token: Optional[str] = None) -> Tuple[bool, Dict]:
    """
    Создает новый репозиторий на GitHub через API.
    
    Args:
        repo_name (str): Имя репозитория
        description (str): Описание репозитория
        private (bool): Приватный или публичный репозиторий
        token (Optional[str]): GitHub токен авторизации
        
    Returns:
        Tuple[bool, Dict]: Статус операции (успех/неудача) и ответ API
    """
    # Если токен не передан, пытаемся получить его из переменной окружения
    if not token:
        token = os.environ.get("GITHUB_TOKEN")
        
    if not token:
        return False, {"error": "GitHub токен не найден. Укажите токен напрямую или через переменную окружения GITHUB_TOKEN"}
        
    # Заголовки для запроса к API
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Параметры для создания репозитория
    data = {
        "name": repo_name,
        "description": description,
        "private": private,
        "auto_init": True,  # Автоматическая инициализация с README
    }
    
    # URL для API GitHub
    url = "https://api.github.com/user/repos"
    
    try:
        # Отправляем POST запрос для создания репозитория
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # Проверяем статус ответа
        if response.status_code == 201:  # Код 201 означает успешное создание
            repo_info = response.json()
            return True, repo_info
        else:
            return False, response.json()
            
    except Exception as e:
        return False, {"error": str(e)}


def configure_github_actions(repo_owner: str, repo_name: str, workflow_file_path: str, token: Optional[str] = None) -> Tuple[bool, Dict]:
    """
    Загружает конфигурацию GitHub Actions в репозиторий.
    
    Args:
        repo_owner (str): Владелец репозитория (имя пользователя)
        repo_name (str): Имя репозитория
        workflow_file_path (str): Путь к файлу конфигурации GitHub Actions
        token (Optional[str]): GitHub токен авторизации
        
    Returns:
        Tuple[bool, Dict]: Статус операции (успех/неудача) и ответ API
    """
    # Если токен не передан, пытаемся получить его из переменной окружения
    if not token:
        token = os.environ.get("GITHUB_TOKEN")
        
    if not token:
        return False, {"error": "GitHub токен не найден. Укажите токен напрямую или через переменную окружения GITHUB_TOKEN"}
    
    # Проверяем существование файла конфигурации
    if not os.path.isfile(workflow_file_path):
        return False, {"error": f"Файл конфигурации не найден: {workflow_file_path}"}
    
    # Читаем содержимое файла конфигурации
    with open(workflow_file_path, "r") as f:
        content = f.read()
    
    # Заголовки для запроса к API
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # URL для API GitHub
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/.github/workflows/tests.yml"
    
    # Параметры для создания файла
    data = {
        "message": "Добавлена конфигурация GitHub Actions",
        "content": content.encode("utf-8").hex(),  # Содержимое файла в base64
        "branch": "main"
    }
    
    try:
        # Отправляем PUT запрос для создания файла
        response = requests.put(url, headers=headers, data=json.dumps(data))
        
        # Проверяем статус ответа
        if response.status_code in [201, 200]:  # Код 201 - создание, 200 - обновление
            return True, response.json()
        else:
            return False, response.json()
            
    except Exception as e:
        return False, {"error": str(e)}


def push_files_to_github(repo_owner: str, repo_name: str, files: Dict[str, str], commit_message: str, token: Optional[str] = None) -> Tuple[bool, Dict]:
    """
    Загружает несколько файлов в репозиторий GitHub.
    
    Args:
        repo_owner (str): Владелец репозитория (имя пользователя)
        repo_name (str): Имя репозитория
        files (Dict[str, str]): Словарь с путями к файлам и их содержимым
        commit_message (str): Сообщение коммита
        token (Optional[str]): GitHub токен авторизации
        
    Returns:
        Tuple[bool, Dict]: Статус операции (успех/неудача) и результат
    """
    # Если токен не передан, пытаемся получить его из переменной окружения
    if not token:
        token = os.environ.get("GITHUB_TOKEN")
        
    if not token:
        return False, {"error": "GitHub токен не найден. Укажите токен напрямую или через переменную окружения GITHUB_TOKEN"}
    
    # Заголовки для запроса к API
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    success_count = 0
    errors = []
    
    for file_path, content in files.items():
        # URL для API GitHub
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        
        # Параметры для создания файла
        data = {
            "message": commit_message,
            "content": content.encode("utf-8").hex(),  # Содержимое файла в base64
            "branch": "main"
        }
        
        try:
            # Отправляем PUT запрос для создания файла
            response = requests.put(url, headers=headers, data=json.dumps(data))
            
            # Проверяем статус ответа
            if response.status_code in [201, 200]:  # Код 201 - создание, 200 - обновление
                success_count += 1
            else:
                errors.append({
                    "file": file_path,
                    "status": response.status_code,
                    "error": response.json()
                })
                
        except Exception as e:
            errors.append({
                "file": file_path,
                "error": str(e)
            })
    
    return len(errors) == 0, {
        "success_count": success_count,
        "total_files": len(files),
        "errors": errors
    } 