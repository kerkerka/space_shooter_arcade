# -*- coding: utf-8 -*-
"""
Скрипт для сборки .exe файла игры Space Shooter Arcade
Использует PyInstaller для создания исполняемого файла

Запуск:
    python build_exe.py

После сборки .exe файл будет в папке dist/
"""

import PyInstaller.__main__
import os
import shutil

# Путь к проекту
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(PROJECT_DIR, 'dist')
BUILD_DIR = os.path.join(PROJECT_DIR, 'build_temp')
ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')

# Очищаем старые сборки
if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR)
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)

# Создаём папку assets если она не существует (для сборки без ассетов)
if not os.path.exists(ASSETS_DIR):
    print("⚠️  Папка assets не найдена. Создаём пустую папку для сборки...")
    os.makedirs(ASSETS_DIR, exist_ok=True)
    os.makedirs(os.path.join(ASSETS_DIR, 'sprites'), exist_ok=True)
    os.makedirs(os.path.join(ASSETS_DIR, 'sounds'), exist_ok=True)
    os.makedirs(os.path.join(ASSETS_DIR, 'fonts'), exist_ok=True)
    print("✅ Пустая папка assets создана. Скопируйте графические и звуковые файлы!")

print("🚀 Сборка Space Shooter Arcade...")

PyInstaller.__main__.run([
    'main.py',
    '--name=SpaceShooterArcade',
    '--onefile',
    '--windowed',  # Без консоли
    # '--icon=assets/sprites/player.ico',  # Иконка (опционально, если есть)
    '--add-data=assets;assets',  # Включаем папку assets
    '--hidden-import=arcade',
    '--hidden-import=PIL',
    f'--distpath={DIST_DIR}',
    f'--workpath={BUILD_DIR}',
    '--noconfirm',
])

print(f"\n✅ Сборка завершена!")
print(f"📦 .exe файл находится в: {DIST_DIR}")
print(f"\nДля запуска игры откройте: {os.path.join(DIST_DIR, 'SpaceShooterArcade.exe')}")
