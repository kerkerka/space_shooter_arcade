# -*- coding: utf-8 -*-
"""
Space Shooter Arcade - Интерфейс (HUD)
"""

import arcade

import settings


class HUD:
    """
    Heads-Up Display - интерфейс игрока.
    Отображает HP, волну, опыт, скорострельность и размер пуль.
    """
    
    def __init__(self):
        """Инициализация HUD."""
        pass
    
    def draw(self, player_hp: int, max_hp: int, current_xp: int, 
             wave: int, total_waves: str, level: int,
             fire_rate_mult: float, bullet_size_mult: float,
             wave_break_timer: int = None, is_boss_wave: bool = False):
        """
        Отрисовка HUD.
        
        :param player_hp: Текущее здоровье игрока
        :param max_hp: Максимальное здоровье
        :param current_xp: Текущий опыт
        :param wave: Текущая волна
        :param total_waves: Всего волн
        :param level: Текущий уровень
        :param fire_rate_mult: Множитель скорострельности
        :param bullet_size_mult: Множитель размера пуль
        :param wave_break_timer: Таймер перерыва между волнами
        :param is_boss_wave: True если волна с боссом
        """
        # Полоска здоровья
        bar_width = 300
        bar_height = 25
        x = 20
        y = settings.SCREEN_HEIGHT - 30

        # Фон полоски
        arcade.draw_rectangle_filled(x + bar_width // 2, y, bar_width, bar_height,
                                    settings.COLOR_DARK_GRAY)

        # Заполненная часть
        hp_percent = player_hp / max_hp
        filled_width = int(bar_width * hp_percent)

        # Цвет зависит от здоровья
        if hp_percent > 0.6:
            hp_color = settings.COLOR_GREEN
        elif hp_percent > 0.3:
            hp_color = settings.COLOR_YELLOW
        else:
            hp_color = settings.COLOR_RED

        arcade.draw_rectangle_filled(x + filled_width // 2, y, filled_width, bar_height, hp_color)

        # Рамка
        arcade.draw_rectangle_outline(x + bar_width // 2, y, bar_width, bar_height,
                                     settings.COLOR_WHITE, 2)
        
        # Текст HP
        hp_text = f"HP: {player_hp}/{max_hp}"
        arcade.draw_text(hp_text, x + 10, y - 8, settings.COLOR_WHITE, 14, bold=True,
                        font_name=settings.FONT_FOR_ARCADE)

        # Опыт
        xp_text = f"XP: {current_xp}"
        arcade.draw_text(xp_text, x, y - 35, settings.COLOR_YELLOW, 16, bold=True,
                        font_name=settings.FONT_FOR_ARCADE)

        # Волна и уровень
        wave_info = f"Уровень {level} | Волна {wave}/{total_waves}"
        if is_boss_wave:
            wave_info += " [БОСС!]"
        arcade.draw_text(wave_info, settings.SCREEN_WIDTH // 2 - 100, y,
                        settings.COLOR_CYAN, 18, bold=True,
                        font_name=settings.FONT_FOR_ARCADE)

        # Таймер перерыва - надпись по центру сверху
        if wave_break_timer is not None and wave_break_timer > 0:
            arcade.draw_text("ПЕРЕРЫВ",
                            settings.SCREEN_WIDTH // 2,
                            settings.SCREEN_HEIGHT - 100,
                            settings.COLOR_GREEN, 36,
                            anchor_x="center", bold=True,
                            font_name=settings.FONT_FOR_ARCADE)

        # Статус оружия (справа вверху)
        weapon_x = settings.SCREEN_WIDTH - 250
        weapon_y = settings.SCREEN_HEIGHT - 30

        arcade.draw_text(f"Скорострельность: x{fire_rate_mult:.1f}",
                        weapon_x, weapon_y, settings.COLOR_ORANGE, 14,
                        font_name=settings.FONT_FOR_ARCADE)
        arcade.draw_text(f"Размер пуль: x{bullet_size_mult:.1f}",
                        weapon_x, weapon_y - 25, settings.COLOR_PURPLE, 14,
                        font_name=settings.FONT_FOR_ARCADE)
    
    def draw_wave_start(self, wave: int, level: int):
        """
        Отрисовка сообщения о начале волны.

        :param wave: Номер волны
        :param level: Номер уровня
        """
        text = f"ВОЛНА {wave}"
        if level <= 3 and wave == settings.WAVES_PER_LEVEL:
            text = f"БОСС УРОВНЯ {level}!"

        arcade.draw_text(text, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 50,
                        settings.COLOR_YELLOW, 48, anchor_x="center", bold=True,
                        font_name=settings.FONT_FOR_ARCADE)

        subtext = f"Уровень {level}"
        arcade.draw_text(subtext, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2,
                        settings.COLOR_WHITE, 24, anchor_x="center",
                        font_name=settings.FONT_FOR_ARCADE)

    def draw_level_complete(self, level: int):
        """
        Отрисовка сообщения о завершении уровня.

        :param level: Номер уровня
        """
        arcade.draw_text(f"УРОВЕНЬ {level} ЗАВЕРШЁН!",
                        settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 50,
                        settings.COLOR_GREEN, 48, anchor_x="center", bold=True,
                        font_name=settings.FONT_FOR_ARCADE)

        arcade.draw_text("Переход к следующему уровню...",
                        settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2,
                        settings.COLOR_WHITE, 24, anchor_x="center",
                        font_name=settings.FONT_FOR_ARCADE)

    def draw_record(self, level: int, best_xp: int):
        """
        Отрисовка рекорда.

        :param level: Номер уровня
        :param best_xp: Лучший опыт
        """
        text = f"Рекорд уровня {level}: {best_xp} XP"
        arcade.draw_text(text, settings.SCREEN_WIDTH // 2, 100,
                        settings.COLOR_YELLOW, 20, anchor_x="center", bold=True,
                        font_name=settings.FONT_FOR_ARCADE)
