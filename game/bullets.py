# -*- coding: utf-8 -*-
"""
Space Shooter Arcade - Классы пуль
"""

import arcade

import settings


class Bullet(arcade.Sprite):
    """
    Класс пули.
    Пуля летит в направлении, заданном при создании, пока не покинет игровое поле.
    """

    def __init__(self, x: float, y: float, dx: float, dy: float, size_multiplier: float = 1.0):
        super().__init__(settings.SPRITES_DIR + "/" + settings.SPRITE_BULLET, center_x=x, center_y=y)
        self.change_x = dx
        self.change_y = dy
        self.damage = settings.BULLET_DAMAGE
        base_size = settings.BULLET_BASE_SIZE * size_multiplier
        self.width = base_size
        self.height = base_size * 2
    
    def update(self):
        """Обновление позиции пули."""
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        # Проверка выхода за пределы игрового поля
        if (self.center_x < 0 or self.center_x > settings.GAME_WIDTH or
            self.center_y < 0 or self.center_y > settings.GAME_HEIGHT):
            self.kill()
    
    def is_on_screen(self) -> bool:
        """Проверка, находится ли пуля на игровом поле."""
        return (0 <= self.center_x <= settings.GAME_WIDTH and
                0 <= self.center_y <= settings.GAME_HEIGHT)
