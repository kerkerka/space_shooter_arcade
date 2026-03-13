# -*- coding: utf-8 -*-
"""
Скрипт для создания папок ассетов
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Создаём папки
os.makedirs(os.path.join(ASSETS_DIR, "sprites"), exist_ok=True)
os.makedirs(os.path.join(ASSETS_DIR, "sounds"), exist_ok=True)
os.makedirs(os.path.join(ASSETS_DIR, "fonts"), exist_ok=True)

print("✅ Папки созданы:")
print(f"   {os.path.join(ASSETS_DIR, 'sprites')}")
print(f"   {os.path.join(ASSETS_DIR, 'sounds')}")
print(f"   {os.path.join(ASSETS_DIR, 'fonts')}")
