# -*- coding: utf-8 -*-
"""Камера и система затемнения"""

import arcade
import math
import settings


class Camera:
    """Камера с круглой зоной видимости, следящая за игроком"""

    def __init__(self, radius: int = None):
        """Инициализация камеры"""
        self.radius = radius if radius else settings.CAMERA_RADIUS
        self.center_x = 0
        self.center_y = 0
        self.smoothing = 0.1  # Плавность слежения

    def follow(self, target_x: float, target_y: float):
        """Плавное слежение за целью"""
        self.center_x += (target_x - self.center_x) * self.smoothing
        self.center_y += (target_y - self.center_y) * self.smoothing
        # Ограничение пределами поля
        self.center_x = max(self.radius, min(settings.GAME_WIDTH - self.radius, self.center_x))
        self.center_y = max(self.radius, min(settings.GAME_HEIGHT - self.radius, self.center_y))

    def is_visible(self, x: float, y: float) -> bool:
        """Проверка видимости точки в круге камеры"""
        dx = x - self.center_x
        dy = y - self.center_y
        return math.sqrt(dx * dx + dy * dy) <= self.radius


class DarknessOverlay:
    """Затемнение за пределами круглой камеры"""

    def __init__(self):
        """Инициализация затемнения"""
        self.color = settings.COLOR_BLACK

    def draw(self, camera: Camera):
        """Отрисовка затемнения вокруг круга видимости"""
        r = camera.radius
        cx, cy = camera.center_x, camera.center_y
        
        # 4 прямоугольника с запасом для перекрытия
        arcade.draw_rectangle_filled(
            settings.GAME_WIDTH // 2,
            settings.GAME_HEIGHT - (settings.GAME_HEIGHT - (cy + r)) // 2,
            settings.GAME_WIDTH + 200,
            settings.GAME_HEIGHT - (cy + r) + 50,
            self.color
        )
        arcade.draw_rectangle_filled(
            settings.GAME_WIDTH // 2,
            (cy - r) // 2,
            settings.GAME_WIDTH + 200,
            cy - r + 50,
            self.color
        )
        arcade.draw_rectangle_filled(
            (cx - r) // 2,
            cy,
            cx - r + 50,
            settings.GAME_HEIGHT + 200,
            self.color
        )
        arcade.draw_rectangle_filled(
            settings.GAME_WIDTH - (settings.GAME_WIDTH - (cx + r)) // 2,
            cy,
            settings.GAME_WIDTH - (cx + r) + 50,
            settings.GAME_HEIGHT + 200,
            self.color
        )
