# -*- coding: utf-8 -*-
"""
Space Shooter Arcade - Система частиц
"""

import arcade
import random
import math

import settings


class Particle(arcade.Sprite):
    """
    Класс частицы для эффектов.
    """

    def __init__(self, x: float, y: float, color: tuple,
                 speed: float = None, lifetime: int = None):
        super().__init__(settings.SPRITES_DIR + "/" + settings.SPRITE_PARTICLE, center_x=x, center_y=y)
        self.width = 4 + random.randint(0, 4)
        self.height = self.width
        self.color = color
        if speed is None:
            speed = random.uniform(2, 6)
        angle = random.uniform(0, 2 * math.pi)
        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed
        self.lifetime = lifetime if lifetime else random.randint(20, 40)
        self.alpha = 255
        self.decay_rate = random.randint(5, 10)
    
    def update(self):
        """Обновление частицы."""
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Замедление
        self.change_x *= 0.95
        self.change_y *= 0.95

        # Исчезновение
        self.alpha = max(0, self.alpha - self.decay_rate)
        if self.alpha == 0:
            self.kill()


class ParticleSystem:
    """
    Система частиц для управления множеством эффектов.
    """
    
    def __init__(self):
        self.particle_list = arcade.SpriteList()
    
    def emit_bullet_particles(self, x: float, y: float, angle: float):
        """
        Создание частиц при выстреле.
        
        :param x: Позиция X
        :param y: Позиция Y
        :param angle: Угол выстрела
        """
        for _ in range(settings.PARTICLE_BULLET_COUNT):
            particle = Particle(x, y, settings.COLOR_YELLOW)
            # Направляем частицы в сторону выстрела
            particle.change_x = math.cos(angle) * random.uniform(1, 3) + random.uniform(-2, 2)
            particle.change_y = math.sin(angle) * random.uniform(1, 3) + random.uniform(-2, 2)
            particle.lifetime = random.randint(10, 20)
            self.particle_list.append(particle)
    
    def emit_hit_particles(self, x: float, y: float, color: tuple = None):
        """
        Создание частиц при попадании.
        
        :param x: Позиция X
        :param y: Позиция Y
        :param color: Цвет частиц
        """
        if color is None:
            color = settings.COLOR_ORANGE
        
        for _ in range(settings.PARTICLE_HIT_COUNT):
            particle = Particle(x, y, color)
            self.particle_list.append(particle)
    
    def emit_death_particles(self, x: float, y: float, color: tuple = None, 
                            enemy_type: str = 'normal'):
        """
        Создание частиц при смерти врага.
        
        :param x: Позиция X
        :param y: Позиция Y
        :param color: Цвет частиц
        :param enemy_type: Тип врага ('normal' или 'boss')
        """
        if color is None:
            if enemy_type == 'boss':
                color = settings.COLOR_RED
            else:
                color = settings.COLOR_ORANGE
        
        count = settings.PARTICLE_DEATH_COUNT
        if enemy_type == 'boss':
            count *= 3  # Больше частиц для босса
        
        for _ in range(count):
            particle = Particle(x, y, color)
            self.particle_list.append(particle)
    
    def emit_player_death_particles(self, x: float, y: float):
        """
        Создание частиц при смерти игрока.
        
        :param x: Позиция X
        :param y: Позиция Y
        """
        for _ in range(settings.PARTICLE_PLAYER_DEATH_COUNT):
            particle = Particle(x, y, settings.COLOR_CYAN)
            self.particle_list.append(particle)
    
    def update(self):
        """Обновление всех частиц."""
        self.particle_list.update()
        
        # Удаляем невидимые частицы
        for particle in self.particle_list:
            if particle.alpha <= 0:
                particle.kill()
    
    def draw(self):
        """Отрисовка всех частиц."""
        self.particle_list.draw()
    
    def clear(self):
        """Очистка всех частиц."""
        self.particle_list = arcade.SpriteList()
