# -*- coding: utf-8 -*-
"""
Space Shooter Arcade - База данных (SQLite) для хранения рекордов
"""

import sqlite3
import os

import settings

DB_PATH = os.path.join(settings.BASE_DIR, "records.db")


def init_database():
    """Инициализация базы данных и создание таблиц."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level INTEGER NOT NULL,
            xp INTEGER NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Таблица чек-поинтов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkpoints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level INTEGER NOT NULL,
            wave INTEGER NOT NULL,
            unlocked INTEGER DEFAULT 1,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_best_record(level: int) -> int:
    """Получить лучший рекорд опыта для указанного уровня."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT MAX(xp) FROM records WHERE level = ?",
        (level,)
    )
    result = cursor.fetchone()[0]
    conn.close()
    
    return result if result else 0


def save_record(level: int, xp: int):
    """Сохранить рекорд опыта для указанного уровня."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO records (level, xp) VALUES (?, ?)",
        (level, xp)
    )
    
    conn.commit()
    conn.close()


def get_all_records() -> list:
    """Получить все рекорды."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT level, MAX(xp), date FROM records GROUP BY level ORDER BY level"
    )
    results = cursor.fetchall()
    conn.close()

    return results


def save_checkpoint(level: int, wave: int):
    """Сохранить чек-поинт для указанного уровня и волны."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Удаляем старые чек-поинты для этого уровня
    cursor.execute("DELETE FROM checkpoints WHERE level = ?", (level,))
    
    # Сохраняем новый чек-поинт
    cursor.execute(
        "INSERT INTO checkpoints (level, wave, unlocked) VALUES (?, ?, 1)",
        (level, wave)
    )
    
    conn.commit()
    conn.close()


def get_checkpoint(level: int) -> int:
    """Получить номер волны чек-поинта для указанного уровня."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT wave FROM checkpoints WHERE level = ? ORDER BY wave DESC LIMIT 1",
        (level,)
    )
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else 1


def clear_checkpoints():
    """Очистить все чек-поинты."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM checkpoints")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Тест базы данных
    init_database()
    print("База данных инициализирована!")
    print(f"Лучший рекорд уровня 1: {get_best_record(1)}")
