#!/usr/bin/env python3
"""
Скрипт для удаления файлов с суффиксом _thumb из указанных директорий
"""

import os
from pathlib import Path


def remove_thumb_files(directory: str) -> int:
    """
    Удаляет все файлы с суффиксом _thumb из указанной директории
    
    Args:
        directory: Путь к директории
        
    Returns:
        Количество удаленных файлов
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        print(f"❌ Директория не найдена: {directory}")
        return 0
    
    if not dir_path.is_dir():
        print(f"❌ Путь не является директорией: {directory}")
        return 0
    
    removed_count = 0
    
    try:
        # Переходим в директорию (для совместимости, хотя Path работает и без этого)
        os.chdir(directory)
        
        # Ищем все файлы с _thumb в имени
        for file_path in dir_path.iterdir():
            if file_path.is_file() and "_thumb" in file_path.name:
                try:
                    file_path.unlink()
                    print(f"✅ Удален: {file_path.name}")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Ошибка при удалении {file_path.name}: {e}")
    
    except Exception as e:
        print(f"❌ Ошибка при обработке директории {directory}: {e}")
    
    return removed_count


def main() -> None:
    """Основная функция"""
    # Список директорий для обработки
    directories = [
        r"C:\Users\admin\Downloads\Telegram Desktop\ChatExport_2026-03-16\photos",
        r"C:\Users\admin\Downloads\Telegram Desktop\ChatExport_2026-03-16\video_files",
        r"C:\Users\admin\Downloads\Telegram Desktop\ChatExport_2026-03-16\stickers",
        r"C:\Users\admin\Downloads\Telegram Desktop\ChatExport_2026-03-16\round_video_messages",
    ]
    
    total_removed = 0
    
    print("🔍 Начинаем удаление файлов с суффиксом _thumb...\n")
    
    for directory in directories:
        print(f"📁 Обрабатываем директорию: {directory}")
        removed = remove_thumb_files(directory)
        total_removed += removed
        print(f"   Удалено файлов: {removed}\n")
    
    print(f"✨ Готово! Всего удалено файлов: {total_removed}")


if __name__ == "__main__":
    main()
