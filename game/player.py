# -*- coding: utf-8 -*-
"""
Space Shooter Arcade - Класс игрока
"""

import arcade
import math

import settings


class Player(arcade.Sprite):
    """
    Класс игрока.
    Управление: WASD или стрелочки для движения, ЛКМ для стрельбы.
    """

    def __init__(self, x: float, y: float):
        super().__init__(settings.SPRITES_DIR + "/" + settings.SPRITE_PLAYER, center_x=x, center_y=y)
        self.width = settings.PLAYER_SIZE
        self.height = settings.PLAYER_SIZE
        self.speed = settings.PLAYER_SPEED
        self.max_hp = settings.PLAYER_MAX_HP
        self.current_hp = settings.PLAYER_MAX_HP
        self.fire_rate = settings.BASE_FIRE_RATE
        self.fire_cooldown = 0
        self.bullet_size_multiplier = 1.0
        self.fire_rate_multiplier = 1.0
        self.xp = 0
        self.aim_angle = 0
    
    def update(self):
        """Обновление состояния игрока."""
        # Применяем изменение координат
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        # Ограничение движения пределами игрового поля
        if self.left < 0:
            self.left = 0
        if self.right > settings.GAME_WIDTH:
            self.right = settings.GAME_WIDTH
        if self.bottom < 0:
            self.bottom = 0
        if self.top > settings.GAME_HEIGHT:
            self.top = settings.GAME_HEIGHT

        # Перезарядка оружия
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
    
    def move(self, key_left: bool, key_right: bool, key_up: bool, key_down: bool):
        """
        Движение игрока.
        
        :param key_left: Нажата ли клавиша влево
        :param key_right: Нажата ли клавиша вправо
        :param key_up: Нажата ли клавиша вверх
        :param key_down: Нажата ли клавиша вниз
        """
        if key_left:
            self.change_x = -self.speed
        elif key_right:
            self.change_x = self.speed
        else:
            self.change_x = 0
        
        if key_up:
            self.change_y = self.speed
        elif key_down:
            self.change_y = -self.speed
        else:
            self.change_y = 0
    
    def aim_at(self, mouse_x: float, mouse_y: float):
        """
        Прицеливание в сторону курсора мыши.
        
        :param mouse_x: Позиция курсора по X
        :param mouse_y: Позиция курсора по Y
        """
        dx = mouse_x - self.center_x
        dy = mouse_y - self.center_y
        self.aim_angle = math.atan2(dy, dx)
    
    def can_shoot(self) -> bool:
        """Проверка возможности выстрела."""
        return self.fire_cooldown <= 0
    
    def shoot(self) -> tuple:
        """
        Выстрел.
        
        :return: Кортеж (направление_x, направление_y) для пули
        """
        if self.can_shoot():
            self.fire_cooldown = int(self.fire_rate / self.fire_rate_multiplier)
            
            # Вычисляем направление пули
            bullet_dx = math.cos(self.aim_angle) * settings.BULLET_SPEED
            bullet_dy = math.sin(self.aim_angle) * settings.BULLET_SPEED
            
            return (bullet_dx, bullet_dy)
        
        return (0, 0)
    
    def take_damage(self, damage: int):
        """
        Получение урона.
        
        :param damage: Количество урона
        """
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
    
    def heal(self, amount: int):
        """
        Лечение.

        :param amount: Количество здоровья для восстановления
        """
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def heal_to_full(self):
        """Полное восстановление здоровья до максимума."""
        self.current_hp = self.max_hp
    
    def add_xp(self, amount: int):
        """
        Добавление опыта.
        
        :param amount: Количество опыта
        """
        self.xp += amount
    
    def apply_weapon_upgrade(self, wave: int):
        """
        Применение улучшения оружия после прохождения волны.

        :param wave: Номер пройденной волны
        """
        if wave == settings.UPGRADE_WAVE_1:
            self.fire_rate_multiplier *= settings.FIRE_RATE_MULTIPLIER_1
        elif wave == settings.UPGRADE_WAVE_2:
            self.bullet_size_multiplier *= settings.BULLET_SIZE_MULTIPLIER
        elif wave == settings.UPGRADE_WAVE_3:
            self.fire_rate_multiplier *= settings.FIRE_RATE_MULTIPLIER_2
        elif wave == settings.UPGRADE_WAVE_4:
            self.fire_rate_multiplier *= settings.FIRE_RATE_MULTIPLIER_3
    
    def is_alive(self) -> bool:
        """Проверка, жив ли игрок."""
        return self.current_hp > 0
    
    def draw_health_bar(self):
        """Отрисовка полоски здоровья."""
        # Фон полоски здоровья
        bar_width = 200
        bar_height = 20
        x = self.center_x - bar_width // 2
        y = self.center_y + self.height // 2 + 10

        arcade.draw_rectangle_filled(x + bar_width // 2, y, bar_width, bar_height, settings.COLOR_RED)

        # Заполненная часть
        hp_percent = self.current_hp / self.max_hp
        filled_width = int(bar_width * hp_percent)
        arcade.draw_rectangle_filled(x + filled_width // 2, y, filled_width, bar_height, settings.COLOR_GREEN)

        # Рамка
        arcade.draw_rectangle_outline(x + bar_width // 2, y, bar_width, bar_height, settings.COLOR_WHITE, 2)
