#!/usr/bin/env python3
"""
Скрипт для создания инсталлятора TestGen
"""

import os
import sys
import subprocess
import shutil
import tempfile
import zipfile
import requests
from pathlib import Path

# Проверка, работаем ли мы в Windows
if sys.platform != "win32":
    print("Этот скрипт должен выполняться только в Windows!")
    sys.exit(1)

def check_requirements():
    """Проверяет, установлены ли необходимые зависимости"""
    try:
        import PyInstaller
        print("PyInstaller уже установлен.")
    except ImportError:
        print("Установка PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    try:
        import tqdm
        print("tqdm уже установлен.")
    except ImportError:
        print("Установка tqdm...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
    
    try:
        import innosetup
        print("innosetup уже установлен.")
    except ImportError:
        print("Установка innosetup...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "innosetup"])

def create_executable():
    """Создает исполняемый файл с помощью PyInstaller"""
    print("Создание исполняемого файла testgen.exe...")
    
    # Настройка путей
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['testgen.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=['cmd', 'cmd.testgen', 'cmd.testgen.main', 'langs', 'testengines', 'ui', 'rich.live', 'rich.syntax'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
             
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='testgen',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='icon.ico')
"""
    # Создаем временный testgen.py
    with open("testgen.py", "w") as f:
        f.write("""#!/usr/bin/env python3
import sys
import os
from cmd.testgen.main import app

if __name__ == "__main__":
    app()
""")
    
    # Создаем spec файл
    with open("testgen.spec", "w") as f:
        f.write(spec_content)
    
    # Запускаем PyInstaller
    subprocess.check_call([
        sys.executable, 
        "-m", 
        "PyInstaller", 
        "--clean",
        "testgen.spec"
    ])
    
    print("Исполняемый файл создан в директории dist/")

def create_installer():
    """Создает установщик с помощью Inno Setup"""
    print("Создание инсталлятора...")
    
    # Создаем скрипт для Inno Setup
    inno_script = """
#define MyAppName "TestGen"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "TestGen Contributors"
#define MyAppURL "https://github.com/yourusername/testgen"
#define MyAppExeName "testgen.exe"

[Setup]
AppId={{4F6E7A42-8B9C-4F0A-91D8-B9B2C0F9C8A3}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\\LICENSE
OutputDir=.\\output
OutputBaseFilename=TestGen_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\\Russian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\\dist\\testgen\\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\\dist\\testgen\\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"
Name: "{group}\\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
"""
    
    # Создаем директории
    os.makedirs("installer", exist_ok=True)
    os.makedirs("installer/output", exist_ok=True)
    
    # Записываем скрипт
    with open("installer/setup.iss", "w") as f:
        f.write(inno_script)
    
    # Запускаем Inno Setup
    try:
        import innosetup
        compiler = innosetup.Compiler()
        compiler.compile("installer/setup.iss")
        print("Инсталлятор создан в директории installer/output/")
    except Exception as e:
        print(f"Ошибка при создании инсталлятора: {e}")
        print("Убедитесь, что Inno Setup установлен и доступен в PATH.")

def create_zip_release():
    """Создает ZIP-архив с исполняемым файлом"""
    print("Создание ZIP-архива...")
    
    # Создаем директорию для релиза, если она не существует
    os.makedirs("release", exist_ok=True)
    
    # Путь к ZIP-файлу
    zip_path = "release/TestGen_1.0.0.zip"
    
    # Создаем ZIP-архив
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Добавляем исполняемый файл
        zipf.write("dist/testgen/testgen.exe", "testgen.exe")
        
        # Добавляем лицензию и README
        zipf.write("LICENSE", "LICENSE")
        zipf.write("README.md", "README.md")
        
        # Добавляем зависимости из папки dist
        for root, _, files in os.walk("dist/testgen"):
            for file in files:
                if file != "testgen.exe":
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, "dist/testgen")
                    zipf.write(file_path, arcname)
    
    print(f"ZIP-архив создан: {zip_path}")

if __name__ == "__main__":
    # Проверяем зависимости
    check_requirements()
    
    # Создаем исполняемый файл
    create_executable()
    
    # Создаем инсталлятор
    create_installer()
    
    # Создаем ZIP-архив
    create_zip_release()
    
    print("Готово! Инсталлятор и ZIP-архив созданы.") 