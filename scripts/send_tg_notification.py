#!/usr/bin/env python3
"""
Скрипт для отправки уведомлений в Telegram
Используется в GitHub Actions для уведомления о статусе деплоя
"""

import os
import sys
import asyncio
import dotenv

from telegram import Bot

from kys_in_rest.applications.ioc import make_ioc
from kys_in_rest.core.cfg import root_dir
from kys_in_rest.tg.features.bot_msg_repo import BotMsgRepo
from kys_in_rest.tg.infra.bot_msg_repo import TgBotMsgRepo


async def send_notification(status: str, message: str) -> bool:
    """Отправляет уведомление используя IoC и BotMsgRepo"""
    try:
        # Загружаем переменные окружения
        dotenv.load_dotenv(root_dir / ".env")
        
        # Создаем IoC с безопасными значениями по умолчанию
        ioc = make_ioc(
            db_path=str(root_dir / os.environ.get("DB", "db.sqlite")),
            tg_admins=list(map(int, os.environ.get("TG_ADMINS", "").split(","))) if os.environ.get("TG_ADMINS") else [],
            yandex_music_token=os.environ.get("YANDEX_MUSIC_TOKEN", ""),
            zen_money_token=os.environ.get("ZEN_MONEY_TOKEN", ""),
        )
        
        # Получаем переменные для уведомлений
        tg_token = os.environ.get("TG_TOKEN")
        tg_admins_str = os.environ.get("TG_ADMINS")
        
        if not tg_token:
            print("❌ TG_TOKEN не найден в переменных окружения")
            return False
        
        if not tg_admins_str:
            print("❌ TG_ADMINS не найден в переменных окружения")
            return False
        
        # Парсим список админов
        try:
            tg_admins = [int(admin.strip()) for admin in tg_admins_str.split(",")]
        except ValueError as e:
            print(f"❌ Ошибка парсинга TG_ADMINS: {e}")
            return False
        
        # Получаем информацию о коммите и ветке
        commit_sha = os.environ.get("GITHUB_SHA", "unknown")[:8]
        ref_name = os.environ.get("GITHUB_REF_NAME", "unknown")
        workflow_run_id = os.environ.get("GITHUB_RUN_ID", "unknown")
        
        # Формируем сообщение
        if status == "success":
            emoji = "✅"
            status_text = "УСПЕШНО"
        elif status == "failure":
            emoji = "❌"
            status_text = "НЕУДАЧНО"
        else:
            emoji = "⚠️"
            status_text = status.upper()
        
        full_message = f"""
{emoji} <b>Деплой {status_text}</b>

{message}

<b>Детали:</b>
• Ветка: <code>{ref_name}</code>
• Коммит: <code>{commit_sha}</code>
• Run ID: <code>{workflow_run_id}</code>

<i>Отправлено автоматически из GitHub Actions</i>
""".strip()
        
        # Создаем бота
        bot = Bot(token=tg_token)
        
        # Создаем репозиторий для отправки уведомлений
        notification_repo = TgBotMsgRepo(bot, tg_admins)
        
        # Регистрируем репозиторий в IoC
        ioc.register(BotMsgRepo, notification_repo)
        
        # Отправляем сообщение
        await notification_repo.send_text(full_message)
        
        print("✅ Все уведомления отправлены успешно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при отправке уведомлений: {e}")
        return False


def main():
    """Основная функция"""
    if len(sys.argv) < 3:
        print("Использование: python send_tg_notification.py <status> <message>")
        print("  status: success|failure")
        print("  message: текст сообщения")
        sys.exit(1)
    
    status = sys.argv[1]
    message = sys.argv[2]
    
    # Запускаем асинхронную функцию
    success = asyncio.run(send_notification(status, message))
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
