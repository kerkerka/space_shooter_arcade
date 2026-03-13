# -*- coding: utf-8 -*-
"""
Space Shooter Arcade - Уровни и волны
"""

import random

import settings


class Wave:
    """
    Класс волны врагов.
    """
    
    def __init__(self, wave_number: int, level: int):
        """
        Инициализация волны.
        
        :param wave_number: Номер волны (1-10)
        :param level: Номер уровня (1-4)
        """
        self.wave_number = wave_number
        self.level = level
        self.enemies_spawned = 0
        self.enemies_alive = 0
        self.is_boss_wave = (wave_number == settings.WAVES_PER_LEVEL and level <= 3)
        
        # Расчёт количества врагов для этой волны
        self.enemy_counts = self._calculate_enemy_counts()
    
    def _calculate_enemy_counts(self) -> dict:
        """
        Расчёт количества врагов для волны.

        :return: Словарь с количеством каждого типа врагов
        """
        # Базовое количество врагов увеличивается с каждой волной
        base_count = settings.ENEMY_COUNT_BASE + int(self.wave_number * settings.ENEMY_COUNT_MULTIPLIER)

        if self.is_boss_wave:
            # Волна с боссом - только босс
            return {'boss': 1}

        # Распределение врагов по типам
        weak_count = base_count // 2
        medium_count = base_count // 3
        tank_count = base_count // 6

        # На уровне 4 (бесконечный) увеличиваем сложность
        if self.level == 4:
            multiplier = 1 + (self.wave_number - 1) * 0.2
            weak_count = int(weak_count * multiplier)
            medium_count = int(medium_count * multiplier)
            tank_count = int(tank_count * multiplier)

        return {
            'weak': weak_count,
            'medium': medium_count,
            'tank': tank_count,
        }
    
    def get_spawn_position(self, player_x: float, player_y: float) -> tuple:
        """
        Получение позиции спавна врага за пределами камеры.

        :param player_x: Позиция игрока по X
        :param player_y: Позиция игрока по Y
        :return: Кортеж (x, y)
        """
        # Спавн за пределами видимой зоны (круг радиусом 350)
        margin = settings.CAMERA_RADIUS + 100
        
        # Выбираем случайную сторону
        side = random.randint(0, 3)  # 0=верх, 1=низ, 2=лево, 3=право
        
        if side == 0:  # Верх
            x = random.uniform(0, settings.GAME_WIDTH)
            y = player_y + margin
        elif side == 1:  # Низ
            x = random.uniform(0, settings.GAME_WIDTH)
            y = player_y - margin
        elif side == 2:  # Лево
            x = player_x - margin
            y = random.uniform(0, settings.GAME_HEIGHT)
        else:  # Право
            x = player_x + margin
            y = random.uniform(0, settings.GAME_HEIGHT)
        
        # Ограничение пределами поля
        x = max(50, min(settings.GAME_WIDTH - 50, x))
        y = max(50, min(settings.GAME_HEIGHT - 50, y))
        
        return (x, y)
    
    def spawn_enemy(self, enemy_type: str, player_x: float, player_y: float):
        """
        Создание врага нужного типа.
        
        :param enemy_type: Тип врага ('weak', 'medium', 'tank', 'boss')
        :param player_x: Позиция игрока по X
        :param player_y: Позиция игрока по Y
        :return: Экземпляр врага
        """
        from game.enemies import WeakEnemy, MediumEnemy, TankEnemy, MiniBoss, FinalBoss
        
        x, y = self.get_spawn_position(player_x, player_y)
        
        if enemy_type == 'weak':
            return WeakEnemy(x, y)
        elif enemy_type == 'medium':
            return MediumEnemy(x, y)
        elif enemy_type == 'tank':
            return TankEnemy(x, y)
        elif enemy_type == 'boss':
            if self.level == 1:
                return MiniBoss(x, y, level=1)
            elif self.level == 2:
                return MiniBoss(x, y, level=2)
            elif self.level == 3:
                return FinalBoss(x, y)
        
        return None
    
    def get_enemies_to_spawn(self) -> list:
        """
        Получение списка врагов для спавна в этой волне.
        
        :return: Список типов врагов
        """
        enemies = []
        
        for enemy_type, count in self.enemy_counts.items():
            if enemy_type == 'boss':
                enemies.append('boss')
            else:
                enemies.extend([enemy_type] * count)
        
        # Перемешиваем для случайного порядка спавна
        random.shuffle(enemies)
        
        return enemies


class LevelManager:
    """
    Менеджер уровней и волн.
    """
    
    def __init__(self):
        """Инициализация менеджера уровней."""
        self.current_level = 1
        self.current_wave = 0
        self.wave_in_progress = False
        self.wave_break = False
        self.wave_break_timer = 0
        
        self.current_wave_obj = None
        self.enemies_to_spawn = []
        self.spawn_timer = 0
        self.spawn_interval = 30  # Кадры между спавном врагов
    
    def start_level(self, level: int):
        """
        Начало уровня.
        
        :param level: Номер уровня (1-4)
        """
        self.current_level = level
        self.current_wave = 0
        self.wave_in_progress = False
        self.wave_break = False
    
    def start_next_wave(self):
        """Запуск следующей волны."""
        if self.current_level == 4 and self.current_wave >= settings.WAVES_PER_LEVEL:
            # Бесконечный режим - продолжаем волны
            self.current_wave += 1
        elif self.current_wave >= settings.WAVES_PER_LEVEL:
            # Уровень завершён
            self.wave_in_progress = False
            return
        
        self.current_wave += 1
        self.current_wave_obj = Wave(self.current_wave, self.current_level)
        self.enemies_to_spawn = self.current_wave_obj.get_enemies_to_spawn()
        self.wave_in_progress = True
        self.wave_break = False
        self.spawn_timer = 0
    
    def start_wave_break(self):
        """Начало перерыва между волнами."""
        self.wave_break = True
        self.wave_break_timer = int(settings.WAVE_BREAK_DURATION * settings.FPS)
    
    def update_wave_break(self) -> bool:
        """
        Обновление таймера перерыва.
        
        :return: True если перерыв закончен
        """
        if self.wave_break:
            self.wave_break_timer -= 1
            if self.wave_break_timer <= 0:
                self.wave_break = False
                return True
        return False
    
    def get_heal_amount(self) -> int:
        """Получение количества здоровья для лечения в перерыве."""
        return settings.WAVE_BREAK_HEAL
    
    def update_spawning(self, player_x: float, player_y: float) -> list:
        """
        Обновление спавна врагов.
        
        :param player_x: Позиция игрока по X
        :param player_y: Позиция игрока по Y
        :return: Список новых врагов
        """
        if not self.wave_in_progress or self.wave_break:
            return []
        
        new_enemies = []
        
        if self.enemies_to_spawn and self.spawn_timer <= 0:
            enemy_type = self.enemies_to_spawn.pop(0)
            enemy = self.current_wave_obj.spawn_enemy(enemy_type, player_x, player_y)
            if enemy:
                new_enemies.append(enemy)
            self.spawn_timer = self.spawn_interval
        else:
            self.spawn_timer -= 1
        
        return new_enemies
    
    def is_wave_complete(self) -> bool:
        """Проверка завершения волны."""
        return self.wave_in_progress and not self.enemies_to_spawn
    
    def is_level_complete(self) -> bool:
        """Проверка завершения уровня."""
        return (self.current_wave >= settings.WAVES_PER_LEVEL and 
                not self.wave_in_progress and 
                self.current_level <= 3)
    
    def get_wave_info(self) -> dict:
        """
        Получение информации о текущей волне.
        
        :return: Словарь с информацией
        """
        return {
            'level': self.current_level,
            'wave': self.current_wave,
            'total_waves': settings.WAVES_PER_LEVEL if self.current_level <= 3 else '∞',
            'is_boss_wave': self.current_wave_obj.is_boss_wave if self.current_wave_obj else False,
            'enemies_remaining': len(self.enemies_to_spawn),
        }
