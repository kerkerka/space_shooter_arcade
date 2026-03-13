# -*- coding: utf-8 -*-
"""
Space Shooter Arcade - Главное меню
"""

import arcade

import settings
import database


class Button:
    """Класс кнопки для меню."""

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

        # Фон кнопки
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, color)
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height,
                                     settings.COLOR_WHITE, 3)

        # Текст
        arcade.draw_text(self.text, self.x, self.y, settings.COLOR_WHITE, 20,
                        anchor_x="center", anchor_y="center", bold=True,
                        font_name=settings.FONT_FOR_ARCADE)


class MenuState:
    """
    Состояние главного меню.
    """
    
    def __init__(self):
        """Инициализация меню"""
        self.buttons = []
        self.selected_level = 1
        self.best_records = {}
        self.click_sound = arcade.load_sound(settings.SOUNDS_DIR + "/" + settings.SOUND_BUTTON_CLICK)
        self._create_buttons()
        self._load_records()
    
    def _create_buttons(self):
        """Создание кнопок меню."""
        button_width = 300
        button_height = 60
        start_y = settings.SCREEN_HEIGHT // 2 + 50
        gap = 80
        
        # Кнопки уровней (для уровней 1-3)
        for i in range(3):
            level = i + 1
            btn = Button(
                settings.SCREEN_WIDTH // 2, 
                start_y - i * gap,
                button_width, button_height,
                f"Уровень {level}"
            )
            self.buttons.append(('level', level, btn))
        
        # Кнопка бесконечного режима (уровень 4)
        btn = Button(
            settings.SCREEN_WIDTH // 2,
            start_y - 3 * gap,
            button_width, button_height,
            "Бесконечный режим"
        )
        self.buttons.append(('level', 4, btn))
        
        # Кнопки громкости
        self.sound_btn = Button(
            settings.SCREEN_WIDTH // 2 - 150,
            150,
            200, button_height,
            f"Звук: {int(settings.SOUND_VOLUME * 100)}%"
        )
        self.buttons.append(('sound', None, self.sound_btn))

        self.music_btn = Button(
            settings.SCREEN_WIDTH // 2 + 150,
            150,
            200, button_height,
            f"Музыка: {int(settings.MUSIC_VOLUME * 100)}%"
        )
        self.buttons.append(('music', None, self.music_btn))
    
    def _load_records(self):
        """Загрузка рекордов из базы данных."""
        database.init_database()
        for level in range(1, 5):
            self.best_records[level] = database.get_best_record(level)
    
    def update(self, mouse_x: float, mouse_y: float):
        """
        Обновление состояния меню.
        
        :param mouse_x: Позиция курсора по X
        :param mouse_y: Позиция курсора по Y
        """
        for btn_type, btn_value, btn in self.buttons:
            btn.is_hovered = btn.is_mouse_over(mouse_x, mouse_y)
    
    def on_mouse_click(self, mouse_x: float, mouse_y: float) -> tuple:
        """
        Обработка клика мыши.

        :param mouse_x: Позиция курсора по X
        :param mouse_y: Позиция курсора по Y
        :return: Кортеж (действие, значение) или None
        """
        # Воспроизводим звук клика
        if self.click_sound:
            try:
                arcade.play_sound(self.click_sound, volume=settings.SOUND_VOLUME)
            except:
                pass
        
        for btn_type, btn_value, btn in self.buttons:
            if btn.is_mouse_over(mouse_x, mouse_y):
                if btn_type == 'level':
                    return ('start_level', btn_value)
                elif btn_type == 'sound':
                    settings.SOUND_VOLUME = (settings.SOUND_VOLUME + settings.SOUND_VOLUME_STEP) % 1.25
                    if settings.SOUND_VOLUME > 1:
                        settings.SOUND_VOLUME = 0
                    btn.text = f"Звук: {int(settings.SOUND_VOLUME * 100)}%"
                    return ('sound_change', settings.SOUND_VOLUME)
                elif btn_type == 'music':
                    settings.MUSIC_VOLUME = (settings.MUSIC_VOLUME + settings.SOUND_VOLUME_STEP) % 1.25
                    if settings.MUSIC_VOLUME > 1:
                        settings.MUSIC_VOLUME = 0
                    btn.text = f"Музыка: {int(settings.MUSIC_VOLUME * 100)}%"
                    return ('music_change', settings.MUSIC_VOLUME)
        
        return None
    
    def draw(self):
        """Отрисовка меню."""
        # Фон
        arcade.set_background_color(settings.COLOR_DARK_BLUE)

        # Заголовок
        arcade.draw_text("SPACE SHOOTER",
                        settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 200,
                        settings.COLOR_CYAN, 72, anchor_x="center", bold=True,
                        font_name=settings.FONT_FOR_ARCADE)
        arcade.draw_text("ARCADE",
                        settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 280,
                        settings.COLOR_YELLOW, 72, anchor_x="center", bold=True,
                        font_name=settings.FONT_FOR_ARCADE)

        # Кнопки
        for btn_type, btn_value, btn in self.buttons:
            btn.draw()

        # Общий рекорд (максимальный из всех уровней)
        y_pos = 220
        best_overall = max(self.best_records.values()) if self.best_records else 0
        arcade.draw_text(f"ЛУЧШИЙ РЕКОРД: {best_overall} XP",
                        settings.SCREEN_WIDTH // 2, y_pos,
                        settings.COLOR_ORANGE, 28, anchor_x="center", bold=True,
                        font_name=settings.FONT_FOR_ARCADE)

        # Подсказка
        arcade.draw_text("Выберите уровень для начала игры",
                        settings.SCREEN_WIDTH // 2, 30,
                        settings.COLOR_GRAY, 16, anchor_x="center",
                        font_name=settings.FONT_FOR_ARCADE)
