#!/usr/bin/env python3
"""
Скрипт для создания файлов релиза TestGen
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path

def create_directories():
    """Создает необходимые директории для релизов"""
    os.makedirs("release_files/TestGen_Portable", exist_ok=True)
    os.makedirs("release_files/TestGen_Full", exist_ok=True)
    print("✓ Директории созданы")

def create_portable_version():
    """Создает портативную версию приложения"""
    print("Создание портативной версии...")
    
    # Директория для портативной версии
    portable_dir = Path("release_files/TestGen_Portable")
    
    # Очистка директории
    for item in portable_dir.glob("*"):
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)
    
    # Копируем файл из директории dist, если он существует
    exe_path = Path("dist/TestGen.exe")
    if exe_path.exists():
        shutil.copy(exe_path, portable_dir / "TestGen.exe")
        print(f"✓ Скопирован файл {exe_path} в {portable_dir}")
    else:
        print(f"⚠ Файл {exe_path} не найден. Пропускаем.")
    
    # Создаем bat-файл для запуска
    with open(portable_dir / "ЗАПУСТИТЬ_TESTGEN.bat", "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("echo Запуск TestGen...\n")
        f.write("TestGen.exe\n")
        f.write("pause\n")
    print("✓ Создан bat-файл для запуска")
    
    # Копируем документацию
    shutil.copy("README.md", portable_dir)
    shutil.copy("LICENSE", portable_dir)
    print("✓ Документация скопирована")
    
    # Создаем архив
    zipname = Path("release_files/TestGen_Portable.zip")
    if zipname.exists():
        zipname.unlink()
    
    with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(portable_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, portable_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"✓ Создан архив {zipname}")

def create_full_version():
    """Создает полную версию с исходным кодом"""
    print("Создание полной версии...")
    
    # Директория для полной версии
    full_dir = Path("release_files/TestGen_Full")
    
    # Очистка директории
    for item in full_dir.glob("*"):
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)
    
    # Копируем все основные директории кода
    for dir_name in ["cmd", "langs", "testengines", "ui", "tests"]:
        src_dir = Path(dir_name)
        if src_dir.exists():
            dest_dir = full_dir / dir_name
            shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
            print(f"✓ Скопирована директория {dir_name}")
    
    # Копируем файлы
    for file_name in ["README.md", "LICENSE", "testgen.py", "main.py", 
                      "requirements.txt", "Untitled (1).ico", "logo.png"]:
        if Path(file_name).exists():
            shutil.copy(file_name, full_dir)
            print(f"✓ Скопирован файл {file_name}")
    
    # Копируем исполняемый файл, если он существует
    exe_path = Path("dist/TestGen.exe")
    if exe_path.exists():
        shutil.copy(exe_path, full_dir / "TestGen.exe")
        print(f"✓ Скопирован файл {exe_path} в {full_dir}")
    
    # Создаем bat-файл для запуска
    with open(full_dir / "ЗАПУСТИТЬ_TESTGEN.bat", "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("echo Запуск TestGen...\n")
        f.write("TestGen.exe\n")
        f.write("pause\n")
    print("✓ Создан bat-файл для запуска")
    
    # Создаем bat-файл для запуска через Python
    with open(full_dir / "ЗАПУСТИТЬ_ИЗ_ИСХОДНИКОВ.bat", "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("echo Установка зависимостей...\n")
        f.write("pip install -r requirements.txt\n")
        f.write("echo Запуск TestGen из исходников...\n")
        f.write("python main.py\n")
        f.write("pause\n")
    print("✓ Создан bat-файл для запуска из исходников")
    
    # Создаем архив
    zipname = Path("release_files/TestGen_Full.zip")
    if zipname.exists():
        zipname.unlink()
    
    with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(full_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, full_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"✓ Создан архив {zipname}")

def create_setup_bat():
    """Создает пакетный файл для установки"""
    print("Создание установочного файла...")
    
    setup_path = Path("release_files/TestGen_Setup.bat")
    
    with open(setup_path, "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("echo TestGen Installer\n")
        f.write("echo -------------------\n")
        f.write("echo.\n")
        f.write("echo Это установщик TestGen - утилиты для генерации тестов.\n")
        f.write("echo.\n")
        f.write("set INSTALL_DIR=%ProgramFiles%\\TestGen\n")
        f.write("set DESKTOP=%USERPROFILE%\\Desktop\n")
        f.write("set STARTMENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\TestGen\n")
        f.write("\n")
        f.write("echo Установка в %INSTALL_DIR%\n")
        f.write("echo.\n")
        f.write("choice /C YN /M \"Продолжить установку?\"\n")
        f.write("if errorlevel 2 goto :end\n")
        f.write("\n")
        f.write("mkdir \"%INSTALL_DIR%\" 2>nul\n")
        f.write("echo Распаковка файлов...\n")
        f.write("xcopy /E /Y TestGen_Portable\\* \"%INSTALL_DIR%\"\n")
        f.write("\n")
        f.write("echo Создание ярлыков...\n")
        f.write("mkdir \"%STARTMENU%\" 2>nul\n")
        f.write("\n")
        f.write("echo @echo off > \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("echo Set oWS = WScript.CreateObject^(\"WScript.Shell\"^) >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("echo sLinkFile = \"%STARTMENU%\\TestGen.lnk\" >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("echo Set oLink = oWS.CreateShortcut^(sLinkFile^) >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("echo oLink.TargetPath = \"%INSTALL_DIR%\\TestGen.exe\" >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("echo oLink.WorkingDirectory = \"%INSTALL_DIR%\" >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("echo oLink.Description = \"TestGen - Утилита для генерации тестов\" >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("echo oLink.IconLocation = \"%INSTALL_DIR%\\TestGen.exe\" >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("echo oLink.Save >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("\n")
        f.write("echo sLinkFile = \"%DESKTOP%\\TestGen.lnk\" >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("echo Set oLink = oWS.CreateShortcut^(sLinkFile^) >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("echo oLink.TargetPath = \"%INSTALL_DIR%\\TestGen.exe\" >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("echo oLink.WorkingDirectory = \"%INSTALL_DIR%\" >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("echo oLink.Description = \"TestGen - Утилита для генерации тестов\" >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("echo oLink.IconLocation = \"%INSTALL_DIR%\\TestGen.exe\" >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("echo oLink.Save >> \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("cscript /nologo \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("del \"%TEMP%\\CreateShortcut.bat\"\n")
        f.write("\n")
        f.write("echo Установка завершена!\n")
        f.write("echo TestGen установлен в %INSTALL_DIR%\n")
        f.write("echo.\n")
        f.write("pause\n")
        f.write("\n")
        f.write(":end\n")
    
    # Удаляем копирование как .exe - это вызывает проблемы
    # shutil.copy(setup_path, Path("release_files/TestGen_Setup.exe"))
    
    print(f"✓ Создан установочный файл {setup_path}")
    # print(f"✓ Создан установочный файл TestGen_Setup.exe")

def main():
    """Основная функция"""
    print("=== Создание файлов релиза TestGen ===")
    
    create_directories()
    create_portable_version()
    create_full_version()
    create_setup_bat()
    
    print("\n=== Все файлы релиза созданы успешно! ===")
    print("Файлы доступны в директории release_files/")

if __name__ == "__main__":
    main() 