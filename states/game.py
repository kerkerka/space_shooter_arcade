# -*- coding: utf-8 -*-
"""Игровой процесс и логика"""

import arcade
import math
import random
import settings
import database
from game.player import Player
from game.bullets import Bullet
from game.particles import ParticleSystem
from game.camera import Camera, DarknessOverlay
from game.levels import LevelManager
from game.hud import HUD


class Button:
    """Кнопка для интерфейса"""

    def __init__(self, x: float, y: float, width: float, height: float, text: str, color: tuple = None):
        """Создание кнопки"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color if color else settings.COLOR_DARK_BLUE
        self.hover_color = settings.COLOR_BLUE
        self.is_hovered = False

    def is_mouse_over(self, mouse_x: float, mouse_y: float) -> bool:
        """Проверка наведения мыши"""
        return (self.x - self.width // 2 <= mouse_x <= self.x + self.width // 2 and
                self.y - self.height // 2 <= mouse_y <= self.y + self.height // 2)

    def draw(self):
        """Отрисовка кнопки"""
        color = self.hover_color if self.is_hovered else self.color
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, color)
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, settings.COLOR_WHITE, 3)
        arcade.draw_text(self.text, self.x, self.y, settings.COLOR_WHITE, 20,
                        anchor_x="center", anchor_y="center", bold=True,
                        font_name=settings.FONT_FOR_ARCADE)


class GameState:
    """Основное состояние игры"""

    def __init__(self, level: int = 1, start_wave: int = 1):
        """Инициализация игры"""
        self.level = level
        self.start_wave = start_wave
        self.is_paused = False
        self.is_game_over = False
        self.is_victory = False
        
        self.pause_buttons = []
        self._create_pause_buttons()
        
        self.player = Player(settings.GAME_WIDTH // 2, settings.GAME_HEIGHT // 2)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.particle_system = ParticleSystem()
        self.camera = Camera()
        self.darkness = DarknessOverlay()
        self.level_manager = LevelManager()
        self.level_manager.start_level(level)
        self.hud = HUD()
        
        self.wave_break_timer = 0
        self.show_wave_start = True
        self.wave_start_timer = 120
        
        self.sounds = {}
        self.bg_texture = None
        self.click_sound = None
        self._load_sounds()
        self._load_background()
        self._load_click_sound()
        
        self.total_enemies_killed = 0
        self.shots_fired = 0
        self.prev_mouse_pressed = False
        self.continuous_fire_counter = 0

    def _load_click_sound(self):
        """Загрузка звука клика для кнопок."""
        try:
            self.click_sound = arcade.load_sound(settings.SOUNDS_DIR + "/" + settings.SOUND_BUTTON_CLICK)
        except:
            self.click_sound = None

    def _create_pause_buttons(self):
        """Создание кнопок паузы."""
        button_width = 250
        button_height = 60
        center_x = settings.SCREEN_WIDTH // 2
        base_y = settings.SCREEN_HEIGHT // 2

        # Кнопка "Продолжить" - по центру сверху
        self.resume_btn = Button(
            center_x, base_y + 50,
            button_width, button_height,
            "Продолжить"
        )
        self.pause_buttons.append(self.resume_btn)

        # Кнопка "Рестарт" - слева снизу
        self.restart_btn = Button(
            center_x - 150, base_y - 50,
            button_width, button_height,
            "Рестарт"
        )
        self.pause_buttons.append(self.restart_btn)

        # Кнопка "Главное меню" - справа снизу
        self.menu_btn = Button(
            center_x + 150, base_y - 50,
            button_width, button_height,
            "Главное меню"
        )
        self.pause_buttons.append(self.menu_btn)

    def _load_sounds(self):
        """Загрузка звуков"""
        self.sounds = {}
        self.sounds['shoot'] = arcade.load_sound(settings.SOUNDS_DIR + "/" + settings.SOUND_SHOOT)
        self.sounds['enemy_death'] = arcade.load_sound(settings.SOUNDS_DIR + "/" + settings.SOUND_ENEMY_DEATH)
        self.sounds['player_hit'] = arcade.load_sound(settings.SOUNDS_DIR + "/" + settings.SOUND_PLAYER_HIT)
        self.sounds['player_death'] = arcade.load_sound(settings.SOUNDS_DIR + "/" + settings.SOUND_PLAYER_DEATH)

    def _load_background(self):
        """Загрузка фона уровня"""
        bg_file = settings.SPRITE_BACKGROUND_LEVEL4 if self.level == 4 else settings.SPRITE_BACKGROUND_LEVEL1
        self.bg_texture = arcade.load_texture(settings.SPRITES_DIR + "/" + bg_file)

    def _play_sound(self, sound_name: str):
        """Воспроизведение звука."""
        if sound_name in self.sounds:
            try:
                arcade.play_sound(self.sounds[sound_name], volume=settings.SOUND_VOLUME)
            except Exception as e:
                pass  # Игнорируем ошибки XAudio2

    def setup(self):
        """Настройка игры"""
        if self.start_wave > 1:
            for wave in range(1, self.start_wave):
                self.level_manager.start_next_wave()
                self.level_manager.wave_in_progress = False
        self.start_next_wave()

    def start_next_wave(self):
        """Запуск следующей волны"""
        self.level_manager.start_next_wave()
        self.show_wave_start = True
        self.wave_start_timer = 120
        
        # Применяем улучшение ДО начала волны 10
        if self.level_manager.current_wave == 10:
            self.player.apply_weapon_upgrade(10)

    def update(self, delta_time: float, keys: dict, mouse_x: float, mouse_y: float,
               mouse_pressed: bool):
        """
        Обновление игры.

        :param delta_time: Время с последнего кадра
        :param keys: Состояние клавиш
        :param mouse_x: Позиция курсора по X
        :param mouse_y: Позиция курсора по Y
        :param mouse_pressed: Нажата ли ЛКМ
        """
        if self.is_paused or self.is_game_over:
            return

        # Обновление игрока
        self.player.move(
            keys.get('left', False),
            keys.get('right', False),
            keys.get('up', False),
            keys.get('down', False)
        )
        self.player.update()
        self.player.aim_at(mouse_x, mouse_y)

        # Стрельба с умным звуком
        if mouse_pressed and self.player.can_shoot():
            bullet_dir = self.player.shoot()
            if bullet_dir != (0, 0):
                self.shots_fired += 1
                
                # Определяем, нужен ли звук для этой пули
                play_sound = True
                
                # Если ЛКМ было зажато в прошлом кадре - это непрерывная стрельба
                if self.prev_mouse_pressed:
                    self.continuous_fire_counter += 1
                    
                    # Вычисляем множитель скорострельности (округляем до целого)
                    fire_rate_level = round(self.player.fire_rate_multiplier)
                    
                    # Звук только для каждой N-ной пули при непрерывной стрельбе
                    # На 1x - каждый выстрел, на 2x - каждый 2-й, на 3x - каждый 3-й
                    if fire_rate_level > 1 and self.continuous_fire_counter % fire_rate_level != 0:
                        play_sound = False
                else:
                    # Первый выстрел после отпускания - всегда со звуком
                    self.continuous_fire_counter = 1
                
                self._spawn_bullet(bullet_dir, play_sound=play_sound)
        
        # Сохраняем состояние мыши для следующего кадра
        self.prev_mouse_pressed = mouse_pressed
        
        # Сбрасываем счётчик если ЛКМ отпущена
        if not mouse_pressed:
            self.continuous_fire_counter = 0

        # Обновление пуль
        self.bullet_list.update()

        # Обновление врагов
        for enemy in self.enemy_list:
            enemy.update(self.player.center_x, self.player.center_y)

        # Спавн врагов
        new_enemies = self.level_manager.update_spawning(
            self.player.center_x, self.player.center_y
        )
        for enemy in new_enemies:
            self.enemy_list.append(enemy)

        # Обновление частиц
        self.particle_system.update()

        # Обновление камеры
        self.camera.follow(self.player.center_x, self.player.center_y)

        # Обработка перерыва между волнами
        if self.level_manager.wave_break:
            if self.level_manager.update_wave_break():
                # Перерыв закончен - начинаем следующую волну
                if not self.level_manager.is_level_complete():
                    self.start_next_wave()
                else:
                    # Уровень завершён
                    self._complete_level()

        # Проверка завершения волны
        if (self.level_manager.wave_in_progress and
                not self.level_manager.enemies_to_spawn and
                len(self.enemy_list) == 0):
            self.level_manager.wave_in_progress = False
            self._on_wave_complete()

        # Проверка подкрепления от босса
        self._check_boss_support()

        # Столкновения
        self._check_collisions()

        # Проверка смерти игрока
        if not self.player.is_alive():
            self._on_player_death()

    def _spawn_bullet(self, direction: tuple, play_sound: bool = True):
        """
        Создание пули.

        :param direction: Кортеж (dx, dy) направления
        :param play_sound: Воспроизводить ли звук выстрела
        """
        bullet = Bullet(
            self.player.center_x,
            self.player.center_y,
            direction[0],
            direction[1],
            self.player.bullet_size_multiplier
        )
        self.bullet_list.append(bullet)

        # Частицы выстрела
        angle = math.atan2(direction[1], direction[0])
        self.particle_system.emit_bullet_particles(
            self.player.center_x, self.player.center_y, angle
        )

        # Звук выстрела (только если play_sound=True)
        if play_sound:
            self._play_sound('shoot')

    def _check_collisions(self):
        """Проверка столкновений."""
        # Пули попадают во врагов
        for bullet in self.bullet_list:
            hits = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if hits:
                bullet.kill()
                for enemy in hits:
                    killed = enemy.take_damage(bullet.damage)
                    self.particle_system.emit_hit_particles(
                        enemy.center_x, enemy.center_y
                    )
                    if killed:
                        self._on_enemy_killed(enemy)
                break

        # Враги сталкиваются с игроком
        for enemy in self.enemy_list:
            if arcade.check_for_collision(enemy, self.player):
                # Проверяем, босс ли это
                is_boss = hasattr(enemy, 'boss_level')
                
                if is_boss and not self.player.is_invulnerable():
                    # Столкновение с боссом — игрок получает урон и неуязвимость
                    self.player.take_damage(enemy.damage)
                    
                    # Звук и частицы
                    self._play_sound('player_hit')
                    self.particle_system.emit_hit_particles(
                        enemy.center_x, enemy.center_y
                    )
                    
                    # Отталкиваем босса
                    self._push_back_enemy(enemy)
                    
                elif is_boss and self.player.is_invulnerable():
                    # Игрок ещё неуязвим после удара босса — просто отталкиваем
                    self._push_back_enemy(enemy)
                    
                elif not is_boss:
                    # Обычный враг — урон без неуязвимости
                    self.player.take_damage(enemy.damage)
                    self._play_sound('player_hit')
                    self.particle_system.emit_hit_particles(
                        enemy.center_x, enemy.center_y
                    )
                    enemy.kill()

    def _push_back_enemy(self, enemy):
        """Отталкивание врага от игрока при столкновении."""
        import math
        # Вычисляем направление от игрока к врагу
        dx = enemy.center_x - self.player.center_x
        dy = enemy.center_y - self.player.center_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            # Отталкиваем на 100 пикселей
            push_distance = 100
            enemy.center_x += (dx / distance) * push_distance
            enemy.center_y += (dy / distance) * push_distance

    def _check_boss_support(self):
        """Проверка призыва подкрепления боссом."""
        for enemy in self.enemy_list:
            if hasattr(enemy, 'check_support_spawn'):
                support_type = enemy.check_support_spawn()
                if support_type:
                    self._spawn_boss_support(support_type)

    def _spawn_boss_support(self, support_type: str):
        """
        Спавн подкрепления боссом.

        :param support_type: Тип подкрепления ('80', '60', '40', '20')
        """
        if support_type == '80':
            count_weak = settings.BOSS_SUPPORT_80_WEAK
            count_medium = settings.BOSS_SUPPORT_80_MEDIUM
            count_tank = 0
        elif support_type == '60':
            count_weak = settings.BOSS_SUPPORT_60_WEAK
            count_medium = settings.BOSS_SUPPORT_60_MEDIUM
            count_tank = settings.BOSS_SUPPORT_60_TANK
        elif support_type == '40':
            count_weak = settings.BOSS_SUPPORT_40_WEAK
            count_medium = settings.BOSS_SUPPORT_40_MEDIUM
            count_tank = settings.BOSS_SUPPORT_40_TANK
        else:  # '20'
            count_weak = settings.BOSS_SUPPORT_20_WEAK
            count_medium = settings.BOSS_SUPPORT_20_MEDIUM
            count_tank = settings.BOSS_SUPPORT_20_TANK

        # Спавн танков
        for _ in range(count_tank):
            self._spawn_support_enemy('tank')

        # Спавн слабых врагов
        for _ in range(count_weak):
            self._spawn_support_enemy('weak')

        # Спавн средних врагов
        for _ in range(count_medium):
            self._spawn_support_enemy('medium')

    def _spawn_support_enemy(self, enemy_type: str):
        """Спавн врага подкрепления."""
        from game.enemies import WeakEnemy, MediumEnemy, TankEnemy

        x, y = self.level_manager.current_wave_obj.get_spawn_position(
            self.player.center_x, self.player.center_y
        )

        if enemy_type == 'weak':
            enemy = WeakEnemy(x, y)
        elif enemy_type == 'medium':
            enemy = MediumEnemy(x, y)
        else:
            enemy = TankEnemy(x, y)

        self.enemy_list.append(enemy)

    def _on_enemy_killed(self, enemy):
        """
        Событие смерти врага.

        :param enemy: Умерший враг
        """
        self.player.add_xp(enemy.xp_value)
        self.total_enemies_killed += 1

        # Частицы
        is_boss = hasattr(enemy, 'boss_level')
        self.particle_system.emit_death_particles(
            enemy.center_x, enemy.center_y,
            enemy_type='boss' if is_boss else 'normal'
        )

        self._play_sound('enemy_death')

        enemy.kill()

    def _on_wave_complete(self):
        """Событие завершения волны."""
        # Проверяем, была ли это волна с боссом
        wave_info = self.level_manager.get_wave_info()

        if wave_info['is_boss_wave']:
            # Босс побеждён - переход на следующий уровень
            self._complete_level()
        else:
            # Обычная волна - перерыв и следующая волна
            self.level_manager.start_wave_break()
            self.wave_break_timer = int(settings.WAVE_BREAK_DURATION * settings.FPS)

            # Лечение игрока
            heal = self.level_manager.get_heal_amount()

            # Между 9й и 10й волной лечим полностью и сохраняем чек-поинт
            if self.level_manager.current_wave == 9:
                self.player.heal_to_full()
                if self.level == 2:
                    database.save_checkpoint(2, 10)
                elif self.level == 3:
                    database.save_checkpoint(3, 10)
            else:
                self.player.heal(heal)

            # Прокачка оружия
            if self.level == 4:
                # На 4 уровне: до 9 волны включительно - обычная прокачка
                if self.level_manager.current_wave <= 9:
                    self.player.apply_weapon_upgrade(self.level_manager.current_wave)
                # После 9 волны - каждые 3 волны +1.33x к скорострельности (12, 15, 18...)
                elif (self.level_manager.current_wave - 9) % 3 == 0:
                    self.player.fire_rate_multiplier *= 1.33
            elif self.level_manager.current_wave != 10:
                self.player.apply_weapon_upgrade(self.level_manager.current_wave)

    def _complete_level(self):
        """Завершение уровня."""
        # Сохраняем рекорд
        if self.player.xp > database.get_best_record(self.level):
            database.save_record(self.level, self.player.xp)

        # Показываем экран победы для текущего уровня
        self._show_victory_screen()

    def _show_victory_screen(self):
        """Показ экрана победы после уровня."""
        self.is_game_over = True
        self.is_victory = True  # Устанавливаем флаг победы

    def _on_player_death(self):
        """Смерть игрока."""
        self.is_game_over = True
        self.particle_system.emit_player_death_particles(
            self.player.center_x, self.player.center_y
        )

        # Сохраняем рекорд
        if self.player.xp > database.get_best_record(self.level):
            database.save_record(self.level, self.player.xp)

    def draw(self):
        """Отрисовка игры."""
        # Камера отключена для отладки - рисуем всё на полном экране
        
        # Фон
        if self.bg_texture:
            arcade.draw_texture_rectangle(
                settings.GAME_WIDTH // 2, settings.GAME_HEIGHT // 2,
                settings.GAME_WIDTH, settings.GAME_HEIGHT,
                self.bg_texture
            )
        else:
            arcade.set_background_color(settings.COLOR_DARK_BLUE)

        # Игровые объекты
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.player.draw()
        self.particle_system.draw()

        # Затемнение за пределами круглой камеры
        self.darkness.draw(self.camera)

        # HUD
        wave_info = self.level_manager.get_wave_info()
        self.hud.draw(
            self.player.current_hp,
            self.player.max_hp,
            self.player.xp,
            wave_info['wave'],
            wave_info['total_waves'],
            self.level,
            self.player.fire_rate_multiplier,
            self.player.bullet_size_multiplier,
            self.wave_break_timer if self.level_manager.wave_break else None,
            wave_info['is_boss_wave']
        )

        # Сообщение о начале волны
        if self.show_wave_start:
            self.hud.draw_wave_start(
                self.level_manager.current_wave,
                self.level
            )
            self.wave_start_timer -= 1
            if self.wave_start_timer <= 0:
                self.show_wave_start = False

        # Сообщение о паузе с кнопками
        if self.is_paused:
            # Затемнение фона
            arcade.draw_rectangle_filled(
                settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2,
                settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT,
                (0, 0, 0, 150)
            )
            
            # Заголовок
            arcade.draw_text("ПАУЗА", settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 300,
                            settings.COLOR_WHITE, 64, anchor_x="center", bold=True,
                            font_name=settings.FONT_FOR_ARCADE)
            
            # Кнопки
            for btn in self.pause_buttons:
                btn.draw()

    def toggle_pause(self):
        """Переключение паузы."""
        self.is_paused = not self.is_paused

    def update_pause_buttons(self, mouse_x: float, mouse_y: float):
        """Обновление кнопок паузы."""
        for btn in self.pause_buttons:
            btn.is_hovered = btn.is_mouse_over(mouse_x, mouse_y)

    def on_pause_click(self, mouse_x: float, mouse_y: float) -> str:
        """
        Обработка клика по кнопкам паузы.

        :return: Действие ('resume', 'restart', 'menu')
        """
        # Воспроизводим звук клика
        if self.click_sound:
            try:
                arcade.play_sound(self.click_sound, volume=settings.SOUND_VOLUME)
            except:
                pass
        
        if self.resume_btn.is_mouse_over(mouse_x, mouse_y):
            return 'resume'
        elif self.restart_btn.is_mouse_over(mouse_x, mouse_y):
            return 'restart'
        elif self.menu_btn.is_mouse_over(mouse_x, mouse_y):
            return 'menu'
        return None

    def get_result(self) -> dict:
        """
        Получение результатов игры.

        :return: Словарь с результатами
        """
        return {
            'level': self.level,
            'xp': self.player.xp,
            'is_victory': self.is_victory,
            'is_game_over': self.is_game_over,
            'enemies_killed': self.total_enemies_killed,
        }
