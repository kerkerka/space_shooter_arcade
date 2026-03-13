# -*- coding: utf-8 -*-
"""
Space Shooter Arcade - Классы врагов
"""

import arcade
import math
import random

import settings


class Enemy(arcade.Sprite):
    """Базовый класс врага"""

    def __init__(self, x: float, y: float, sprite_path: str, size: int,
                 speed: float, hp: int, damage: int, xp: int):
        super().__init__(sprite_path, center_x=x, center_y=y)
        self.width = size
        self.height = size
        self.speed = speed
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.xp_value = xp
    
    def update(self, player_x: float, player_y: float):
        """
        Обновление врага - движение к игроку.

        :param player_x: Позиция игрока по X
        :param player_y: Позиция игрока по Y
        """
        # Вычисляем направление к игроку
        dx = player_x - self.center_x
        dy = player_y - self.center_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            self.change_x = (dx / distance) * self.speed
            self.change_y = (dy / distance) * self.speed
        
        # Применяем изменение координат
        self.center_x += self.change_x
        self.center_y += self.change_y
    
    def take_damage(self, damage: int) -> bool:
        """
        Получение урона.
        
        :param damage: Количество урона
        :return: True если враг умер
        """
        self.hp -= damage
        return self.hp <= 0
    
    def is_alive(self) -> bool:
        """Проверка, жив ли враг."""
        return self.hp > 0


class WeakEnemy(Enemy):
    """Быстрый, но слабый враг"""

    def __init__(self, x: float, y: float):
        super().__init__(
            x, y,
            settings.SPRITES_DIR + "/" + settings.SPRITE_ENEMY_WEAK,
            settings.ENEMY_WEAK_SIZE,
            settings.ENEMY_WEAK_SPEED,
            settings.ENEMY_WEAK_HP,
            settings.ENEMY_WEAK_DAMAGE,
            settings.ENEMY_WEAK_XP
        )


class MediumEnemy(Enemy):
    """Средний враг"""

    def __init__(self, x: float, y: float):
        super().__init__(
            x, y,
            settings.SPRITES_DIR + "/" + settings.SPRITE_ENEMY_MEDIUM,
            settings.ENEMY_MEDIUM_SIZE,
            settings.ENEMY_MEDIUM_SPEED,
            settings.ENEMY_MEDIUM_HP,
            settings.ENEMY_MEDIUM_DAMAGE,
            settings.ENEMY_MEDIUM_XP
        )


class TankEnemy(Enemy):
    """Медленный, но сильный враг-танк"""

    def __init__(self, x: float, y: float):
        super().__init__(
            x, y,
            settings.SPRITES_DIR + "/" + settings.SPRITE_ENEMY_TANK,
            settings.ENEMY_TANK_SIZE,
            settings.ENEMY_TANK_SPEED,
            settings.ENEMY_TANK_HP,
            settings.ENEMY_TANK_DAMAGE,
            settings.ENEMY_TANK_XP
        )


class MiniBoss(Enemy):
    """Мини-босс для уровней 1 и 2"""

    def __init__(self, x: float, y: float, level: int = 1):
        super().__init__(
            x, y,
            settings.SPRITES_DIR + "/" + settings.SPRITE_BOSS_MINI,
            settings.MINI_BOSS_1_SIZE,
            settings.MINI_BOSS_1_SPEED if level == 1 else settings.MINI_BOSS_2_SPEED,
            settings.MINI_BOSS_1_HP if level == 1 else settings.MINI_BOSS_2_HP,
            settings.MINI_BOSS_1_DAMAGE,
            settings.MINI_BOSS_1_XP
        )
        self.boss_level = level
        
        # Для рывков (уровень 2)
        self.dash_cooldown = 0
        self.dash_duration = 0
        self.is_dashing = False
        self.dash_speed = self.speed * 3
        
        # Таймер для рывков
        if level == 2:
            self.dash_cooldown = settings.MINI_BOSS_2_DASH_COOLDOWN
    
    def update(self, player_x: float, player_y: float):
        """Обновление мини-босса."""
        if self.boss_level == 1:
            # Уровень 1 - просто преследует
            super().update(player_x, player_y)
        else:
            # Уровень 2 - с рывками
            self._update_with_dash(player_x, player_y)
    
    def _update_with_dash(self, player_x: float, player_y: float):
        """Обновление с механикой рывков."""
        dx = player_x - self.center_x
        dy = player_y - self.center_y
        distance = math.sqrt(dx * dx + dy * dy)

        if self.is_dashing:
            # Во время рывка движемся очень быстро к игроку
            self.dash_duration -= 1
            if self.dash_duration <= 0:
                self.is_dashing = False
                self.dash_cooldown = settings.MINI_BOSS_2_DASH_COOLDOWN

            if distance > 0:
                self.change_x = (dx / distance) * self.dash_speed
                self.change_y = (dy / distance) * self.dash_speed
        else:
            # Обычное преследование
            self.dash_cooldown -= 1

            if self.dash_cooldown <= 0 and distance > 100:
                # Начинаем рывок
                self.is_dashing = True
                self.dash_duration = settings.MINI_BOSS_2_DASH_DURATION
            else:
                # Обычное движение
                if distance > 0:
                    self.change_x = (dx / distance) * self.speed
                    self.change_y = (dy / distance) * self.speed
        
        # Применяем изменение координат
        self.center_x += self.change_x
        self.center_y += self.change_y


class FinalBoss(Enemy):
    """Финальный босс с рывками и призывом подкрепления"""

    def __init__(self, x: float, y: float):
        super().__init__(
            x, y,
            settings.SPRITES_DIR + "/" + settings.SPRITE_BOSS_FINAL,
            settings.FINAL_BOSS_SIZE,
            settings.FINAL_BOSS_SPEED,
            settings.FINAL_BOSS_HP,
            settings.FINAL_BOSS_DAMAGE,
            settings.FINAL_BOSS_XP
        )
        
        # Для рывков
        self.dash_cooldown = 0
        self.dash_duration = 0
        self.is_dashing = False
        self.dash_speed = self.speed * 2.5
        
        # Для призыва подкрепления
        self.support_75_called = False
        self.support_50_called = False
        self.support_25_called = False
        
        # Таймеры
        self.dash_cooldown = settings.FINAL_BOSS_DASH_COOLDOWN
    
    def update(self, player_x: float, player_y: float):
        """Обновление финального босса."""
        dx = player_x - self.center_x
        dy = player_y - self.center_y
        distance = math.sqrt(dx * dx + dy * dy)

        if self.is_dashing:
            # Во время рывка
            self.dash_duration -= 1
            if self.dash_duration <= 0:
                self.is_dashing = False
                self.dash_cooldown = settings.FINAL_BOSS_DASH_COOLDOWN

            if distance > 0:
                self.change_x = (dx / distance) * self.dash_speed
                self.change_y = (dy / distance) * self.dash_speed
        else:
            # Обычное состояние
            self.dash_cooldown -= 1

            if self.dash_cooldown <= 0 and distance > 150:
                self.is_dashing = True
                self.dash_duration = settings.FINAL_BOSS_DASH_DURATION
            else:
                if distance > 0:
                    self.change_x = (dx / distance) * self.speed
                    self.change_y = (dy / distance) * self.speed
        
        # Применяем изменение координат
        self.center_x += self.change_x
        self.center_y += self.change_y
    
    def check_support_spawn(self) -> str:
        """
        Проверка необходимости призыва подкрепления.
        
        :return: Тип подкрепления ('75', '50', '25' или '')
        """
        hp_percent = self.hp / self.max_hp
        
        if hp_percent <= 0.75 and not self.support_75_called:
            self.support_75_called = True
            return '75'
        elif hp_percent <= 0.50 and not self.support_50_called:
            self.support_50_called = True
            return '50'
        elif hp_percent <= 0.25 and not self.support_25_called:
            self.support_25_called = True
            return '25'
        
        return ''
