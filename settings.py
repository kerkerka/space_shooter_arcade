# -*- coding: utf-8 -*-
"""
Space Shooter Arcade - Настройки и константы
"""

import os

# === Пути к директориям ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
# FONTS_DIR удалён (шрифт не используется)

# === Шрифты ===
# Используем системный шрифт Impact (встроен в Windows, поддерживает кириллицу!)
# Жирный, заметный, отлично подходит для игр
FONT_NAME = "Impact"
FONT_PATH = None  # Используем системный шрифт
FONT = None
FONT_FOR_ARCADE = FONT_NAME  # Используем имя системного шрифта

# === Окно и экран ===
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Space Shooter Arcade"
FPS = 60

# === Игровое поле ===
GAME_WIDTH = 1920
GAME_HEIGHT = 1080

# === Камера ===
CAMERA_RADIUS = 400  # Радиус круглой зоны видимости

# === Игрок ===
PLAYER_SPEED = 5.5
PLAYER_MAX_HP = 100
PLAYER_SIZE = 64

# === Пули ===
BULLET_SPEED = 12
BULLET_BASE_SIZE = 8
BULLET_DAMAGE = 1

# === Базовая скорострельность (кадров между выстрелами) ===
BASE_FIRE_RATE = 10  # 10 кадров = ~6 выстрелов в секунду при 60 FPS

# === Враги ===
# Weak (быстрый, слабый)
ENEMY_WEAK_SIZE = 32
ENEMY_WEAK_SPEED = 8.0  # было 6.0
ENEMY_WEAK_HP = 1
ENEMY_WEAK_DAMAGE = 5
ENEMY_WEAK_XP = 1

# Medium (средний)
ENEMY_MEDIUM_SIZE = 64
ENEMY_MEDIUM_SPEED = 5.0  # было 3.5
ENEMY_MEDIUM_HP = 2
ENEMY_MEDIUM_DAMAGE = 10
ENEMY_MEDIUM_XP = 2

# Tank (медленный, сильный)
ENEMY_TANK_SIZE = 64
ENEMY_TANK_SPEED = 3.0  # было 2.0
ENEMY_TANK_HP = 3
ENEMY_TANK_DAMAGE = 15
ENEMY_TANK_XP = 3

# Mini Boss (уровень 1)
MINI_BOSS_1_SIZE = 96
MINI_BOSS_1_SPEED = 3.5  # было 2.5
MINI_BOSS_1_HP = 100  # было 50, потом 75, теперь 100
MINI_BOSS_1_DAMAGE = 25
MINI_BOSS_1_XP = 100

# Mini Boss (уровень 2 - с рывками)
MINI_BOSS_2_SIZE = 96
MINI_BOSS_2_SPEED = 4.5  # было 3.0
MINI_BOSS_2_HP = 150  # было 75, потом 100, теперь 150
MINI_BOSS_2_DAMAGE = 25
MINI_BOSS_2_XP = 100
MINI_BOSS_2_DASH_COOLDOWN = 120  # 2 секунды между рывками
MINI_BOSS_2_DASH_DURATION = 30   # 0.5 секунды рывок

# Final Boss (уровень 3 - с рывками и спавном)
FINAL_BOSS_SIZE = 128
FINAL_BOSS_SPEED = 2.0
FINAL_BOSS_HP = 300  # было 150, потом 200, теперь 300
FINAL_BOSS_DAMAGE = 20
FINAL_BOSS_XP = 100
FINAL_BOSS_DASH_COOLDOWN = 180
FINAL_BOSS_DASH_DURATION = 30

# === Уровни и волны ===
TOTAL_LEVELS = 4
WAVES_PER_LEVEL = 10
WAVE_BREAK_DURATION = 5.0  # секунд
WAVE_BREAK_HEAL = 7  # среднее между 5 и 10

# === Усложнение волн ===
# Базовое количество врагов увеличивается с каждой волной
ENEMY_COUNT_BASE = 4  # было 3
ENEMY_COUNT_MULTIPLIER = 2.5  # было 2

# === Прокачка оружия ===
UPGRADE_WAVE_1 = 3   # скорострельность x1.5
UPGRADE_WAVE_2 = 6   # размер пуль x1.5
UPGRADE_WAVE_3 = 9   # скорострельность x1.5 (итого x2.25)
UPGRADE_WAVE_4 = 10  # скорострельность x1.33 (итого x3.0 после 10 волны)

FIRE_RATE_MULTIPLIER_1 = 1.5
BULLET_SIZE_MULTIPLIER = 1.5
FIRE_RATE_MULTIPLIER_2 = 1.5
FIRE_RATE_MULTIPLIER_3 = 1.33  # Для итогового множителя x3.0

# === Подкрепление от босса ===
# 80% HP
BOSS_SUPPORT_80_WEAK = 4
BOSS_SUPPORT_80_MEDIUM = 2

# 60% HP
BOSS_SUPPORT_60_MEDIUM = 6
BOSS_SUPPORT_60_WEAK = 3
BOSS_SUPPORT_60_TANK = 1

# 40% HP
BOSS_SUPPORT_40_MEDIUM = 8
BOSS_SUPPORT_40_WEAK = 4
BOSS_SUPPORT_40_TANK = 3

# 20% HP
BOSS_SUPPORT_20_MEDIUM = 10
BOSS_SUPPORT_20_TANK = 6
BOSS_SUPPORT_20_WEAK = 5

# === Система частиц ===
PARTICLE_BULLET_COUNT = 3      # частиц при выстреле
PARTICLE_HIT_COUNT = 5         # частиц при попадании
PARTICLE_DEATH_COUNT = 15      # частиц при смерти врага
PARTICLE_PLAYER_DEATH_COUNT = 30  # частиц при смерти игрока

# === Цвета (RGB) ===
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_PURPLE = (128, 0, 128)
COLOR_CYAN = (0, 255, 255)
COLOR_DARK_BLUE = (10, 10, 30)
COLOR_GRAY = (128, 128, 128)
COLOR_DARK_GRAY = (64, 64, 64)
COLOR_LIGHT_GRAY = (192, 192, 192)

# === Звуки ===
SOUND_VOLUME = 0.5  # Громкость звуковых эффектов (0.0 - 1.0)
MUSIC_VOLUME = 0.3  # Громкость музыки (0.0 - 1.0)
SOUND_VOLUME_DEFAULT = 0.5
MUSIC_VOLUME_DEFAULT = 0.3
SOUND_VOLUME_STEP = 0.25  # Шаг изменения громкости
SOUND_SHOOT = "shoot.wav"
SOUND_ENEMY_DEATH = "enemy_death.wav"
SOUND_PLAYER_HIT = "player_hit.wav"
SOUND_PLAYER_DEATH = "player_death.wav"
SOUND_BUTTON_CLICK = "button_click.wav"

# === Названия файлов ассетов ===
# Спрайты
SPRITE_PLAYER = "player.png"
SPRITE_ENEMY_WEAK = "enemy_weak.png"
SPRITE_ENEMY_MEDIUM = "enemy_medium.png"
SPRITE_ENEMY_TANK = "enemy_tank.png"
SPRITE_BOSS_MINI = "boss_mini.png"
SPRITE_BOSS_FINAL = "boss_final.png"
SPRITE_BULLET = "bullet.png"
SPRITE_PARTICLE = "particle.png"
SPRITE_BACKGROUND_LEVEL1 = "background_level1.png"
SPRITE_BACKGROUND_LEVEL4 = "background_level4.png"
