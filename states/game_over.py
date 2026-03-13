# -*- coding: utf-8 -*-
"""
Space Shooter Arcade - Экран Game Over
"""

import arcade

import settings
import database


class Button:
    """Класс кнопки."""
    
    def __init__(self, x: float, y: float, width: float, height: float, 
                 text: str, color: tuple = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color if color else settings.COLOR_DARK_BLUE
        self.hover_color = settings.COLOR_BLUE
        self.is_hovered = False
    
    def is_mouse_over(self, mouse_x: float, mouse_y: float) -> bool:
        """Проверка, находится ли курсор над кнопкой."""
        return (self.x - self.width // 2 <= mouse_x <= self.x + self.width // 2 and
                self.y - self.height // 2 <= mouse_y <= self.y + self.height // 2)
    
    def draw(self):
        """Отрисовка кнопки."""
        color = self.hover_color if self.is_hovered else self.color

        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, color)
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height,
                                     settings.COLOR_WHITE, 3)
        arcade.draw_text(self.text, self.x, self.y, settings.COLOR_WHITE, 20,
                        anchor_x="center", anchor_y="center", bold=True,
                        font_name=settings.FONT_FOR_ARCADE)


class GameOverState:
    """
    Состояние экрана смерти / Game Over.
    """
    
    def __init__(self, level: int, xp: int, enemies_killed: int, is_victory: bool = False):
        """
        Инициализация экрана Game Over.
        
        :param level: Номер уровня
        :param xp: Набранный опыт
        :param enemies_killed: Количество убитых врагов
        :param is_victory: Победа ли это
        """
        self.level = level
        self.xp = xp
        self.enemies_killed = enemies_killed
        self.is_victory = is_victory
        self.click_sound = arcade.load_sound(settings.SOUNDS_DIR + "/" + settings.SOUND_BUTTON_CLICK)
        self.buttons = []
        self._create_buttons()
        self.best_record = database.get_best_record(level)
        self.is_new_record = xp >= self.best_record
    
    def _create_buttons(self):
        """Создание кнопок."""
        button_width = 250
        button_height = 60
        center_x = settings.SCREEN_WIDTH // 2
        base_y = settings.SCREEN_HEIGHT // 2 - 100

        if self.is_victory:
            # Для победы: 3 кнопки в ряд
            # Кнопка "След. уровень"
            self.next_level_btn = Button(
                center_x - 300, base_y,
                button_width, button_height,
                "След. уровень",
                settings.COLOR_GREEN
            )
            self.buttons.append(self.next_level_btn)

            # Кнопка "Рестарт"
            self.restart_btn = Button(
                center_x, base_y,
                button_width, button_height,
                "Рестарт"
            )
            self.buttons.append(self.restart_btn)

            # Кнопка "Главное меню"
            self.menu_btn = Button(
                center_x + 300, base_y,
                button_width, button_height,
                "Главное меню"
            )
            self.buttons.append(self.menu_btn)
        else:
            # Для поражения: 2 кнопки
            # Кнопка "Рестарт"
            self.restart_btn = Button(
                center_x - 150, base_y,
                button_width, button_height,
                "Рестарт"
            )
            self.buttons.append(self.restart_btn)

            # Кнопка "Главное меню"
            self.menu_btn = Button(
                center_x + 150, base_y,
                button_width, button_height,
                "Главное меню"
            )
            self.buttons.append(self.menu_btn)
    
    def update(self, mouse_x: float, mouse_y: float):
        """
        Обновление состояния.
        
        :param mouse_x: Позиция курсора по X
        :param mouse_y: Позиция курсора по Y
        """
        for btn in self.buttons:
            btn.is_hovered = btn.is_mouse_over(mouse_x, mouse_y)
    
    def on_mouse_click(self, mouse_x: float, mouse_y: float) -> str:
        """
        Обработка клика мыши.

        :param mouse_x: Позиция курсора по X
        :param mouse_y: Позиция курсора по Y
        :return: Действие ('restart', 'next_level' или 'menu')
        """
        # Воспроизводим звук клика
        if self.click_sound:
            try:
                arcade.play_sound(self.click_sound, volume=0.5)
            except:
                pass
        
        if self.is_victory and hasattr(self, 'next_level_btn'):
            if self.next_level_btn.is_mouse_over(mouse_x, mouse_y):
                return 'next_level'
        
        if self.restart_btn.is_mouse_over(mouse_x, mouse_y):
            return 'restart'
        elif self.menu_btn.is_mouse_over(mouse_x, mouse_y):
            return 'menu'
        return None
    
    def draw(self):
        """Отрисовка экрана Game Over."""
        # Фон
        arcade.set_background_color(settings.COLOR_DARK_BLUE)

        # Заголовок
        if self.is_victory:
            title = "YOU WIN!"
            title_color = settings.COLOR_GREEN
        else:
            title = "GAME OVER"
            title_color = settings.COLOR_RED

        arcade.draw_text(title, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 250,
                        title_color, 72, anchor_x="center", bold=True,
                        font_name=settings.FONT_FOR_ARCADE)
        
        # Статистика
        stats_y = settings.SCREEN_HEIGHT // 2 + 50
        stat_gap = 50

        arcade.draw_text(f"Уровень: {self.level}", settings.SCREEN_WIDTH // 2, stats_y,
                        settings.COLOR_WHITE, 32, anchor_x="center",
                        font_name=settings.FONT_FOR_ARCADE)
        arcade.draw_text(f"Опыт: {self.xp} XP", settings.SCREEN_WIDTH // 2, stats_y - stat_gap,
                        settings.COLOR_YELLOW, 32, anchor_x="center",
                        font_name=settings.FONT_FOR_ARCADE)
        arcade.draw_text(f"Врагов убито: {self.enemies_killed}", settings.SCREEN_WIDTH // 2,
                        stats_y - stat_gap * 2, settings.COLOR_CYAN, 32, anchor_x="center",
                        font_name=settings.FONT_FOR_ARCADE)

        # Рекорд
        if self.is_new_record:
            arcade.draw_text("НОВЫЙ РЕКОРД!", settings.SCREEN_WIDTH // 2,
                            150,
                            settings.COLOR_ORANGE, 36, anchor_x="center", bold=True,
                            font_name=settings.FONT_FOR_ARCADE)
        else:
            arcade.draw_text(f"Рекорд уровня: {self.best_record} XP",
                            settings.SCREEN_WIDTH // 2, 150,
                            settings.COLOR_GRAY, 24, anchor_x="center",
                            font_name=settings.FONT_FOR_ARCADE)

        # Кнопки
        for btn in self.buttons:
            btn.draw()

        # Подсказка
        arcade.draw_text("Выберите действие", settings.SCREEN_WIDTH // 2, 100,
                        settings.COLOR_GRAY, 20, anchor_x="center",
                        font_name=settings.FONT_FOR_ARCADE)
