# -*- coding: utf-8 -*-
"""
Space Shooter Arcade - Главная точка входа
Космический шутер с волнами врагов, боссами и системой прогрессии
"""

import arcade
import settings
import database


class SpaceShooterArcade(arcade.Window):
    """
    Основное окно игры.
    """

    def __init__(self):
        super().__init__(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.SCREEN_TITLE)
        database.init_database()
        
        settings.FONT_FOR_ARCADE = settings.FONT_NAME
        
        self.current_state = 'menu'
        self.menu_state = None
        self.game_state = None
        self.game_over_state = None
        
        self.keys = {}
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_pressed = False
        self.set_mouse_visible(True)
        
        self.setup_menu()

    def setup_menu(self):
        """Настройка главного меню."""
        from states.menu import MenuState
        self.menu_state = MenuState()
        self.current_state = 'menu'

    def setup_game(self, level: int, start_wave: int = 1):
        """Настройка игры"""
        from states.game import GameState
        
        # Проверяем чек-поинт для 3го уровня
        if level == 3:
            checkpoint_wave = database.get_checkpoint(3)
            if checkpoint_wave == 10:
                start_wave = 10
        
        self.game_state = GameState(level, start_wave=start_wave)
        self.game_state.setup()
        self.current_state = 'game'

    def setup_game_over(self, level: int, xp: int, enemies_killed: int, is_victory: bool = False):
        """
        Настройка экрана Game Over.

        :param level: Номер уровня
        :param xp: Набранный опыт
        :param enemies_killed: Количество убитых врагов
        :param is_victory: Победа ли это
        """
        from states.game_over import GameOverState
        self.game_over_state = GameOverState(level, xp, enemies_killed, is_victory)
        self.current_state = 'game_over'

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш."""
        self.keys[key] = True

        # Пауза (ESC)
        if key == arcade.key.ESCAPE and self.current_state == 'game':
            if not self.game_state.is_paused:
                self.game_state.toggle_pause()
            # Иначе пауза снимается только кнопкой "Продолжить"

        # Возврат в меню (Enter на экране Game Over)
        if key == arcade.key.ENTER and self.current_state == 'game_over':
            self.setup_menu()

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш."""
        self.keys[key] = False

    def get_movement_keys(self) -> dict:
        """Получение состояния клавиш движения."""
        return {
            'left': self.keys.get(arcade.key.A, False) or self.keys.get(arcade.key.LEFT, False),
            'right': self.keys.get(arcade.key.D, False) or self.keys.get(arcade.key.RIGHT, False),
            'up': self.keys.get(arcade.key.W, False) or self.keys.get(arcade.key.UP, False),
            'down': self.keys.get(arcade.key.S, False) or self.keys.get(arcade.key.DOWN, False),
        }

    def on_mouse_motion(self, x, y, dx, dy):
        """Обработка движения мыши."""
        self.mouse_x = x
        self.mouse_y = y

        if self.current_state == 'menu':
            self.menu_state.update(x, y)
        elif self.current_state == 'game_over':
            self.game_over_state.update(x, y)
        elif self.current_state == 'game' and self.game_state.is_paused:
            self.game_state.update_pause_buttons(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка нажатия кнопки мыши."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_pressed = True

            if self.current_state == 'menu':
                result = self.menu_state.on_mouse_click(x, y)
                if result:
                    action, value = result
                    if action == 'start_level':
                        self.setup_game(value)

            elif self.current_state == 'game_over':
                action = self.game_over_state.on_mouse_click(x, y)
                if action == 'restart':
                    self.setup_game(self.game_over_state.level)
                elif action == 'next_level':
                    # Переход на следующий уровень
                    next_level = self.game_over_state.level + 1
                    if next_level <= 3:
                        self.setup_game(next_level)
                elif action == 'menu':
                    self.setup_menu()
            
            elif self.current_state == 'game' and self.game_state.is_paused:
                # Обработка клика по кнопкам паузы
                action = self.game_state.on_pause_click(x, y)
                if action == 'resume':
                    self.game_state.toggle_pause()
                elif action == 'restart':
                    self.setup_game(self.game_state.level)
                elif action == 'menu':
                    self.setup_menu()

    def on_mouse_release(self, x, y, button, modifiers):
        """Обработка отпускания кнопки мыши."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_pressed = False

    def on_update(self, delta_time):
        """Обновление игры."""
        if self.current_state == 'game':
            movement_keys = self.get_movement_keys()
            self.game_state.update(
                delta_time,
                movement_keys,
                self.mouse_x,
                self.mouse_y,
                self.mouse_pressed
            )

            # Проверка окончания игры
            if self.game_state.is_game_over:
                result = self.game_state.get_result()
                self.setup_game_over(
                    result['level'],
                    result['xp'],
                    result['enemies_killed'],
                    result['is_victory']
                )

    def on_draw(self):
        """Отрисовка игры."""
        arcade.start_render()

        if self.current_state == 'menu':
            self.menu_state.draw()
        elif self.current_state == 'game':
            self.game_state.draw()
        elif self.current_state == 'game_over':
            self.game_over_state.draw()


def main():
    """Главная функция запуска игры."""
    # Создаём окно
    window = SpaceShooterArcade()

    # Запускаем игру
    arcade.run()


if __name__ == "__main__":
    main()
