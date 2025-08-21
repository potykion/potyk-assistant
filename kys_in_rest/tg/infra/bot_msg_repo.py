from typing import List

from telegram import Message, InputMediaAudio, Bot

from kys_in_rest.tg.entities.audio import TgAudio
from kys_in_rest.tg.features.bot_msg_repo import BotMsgRepo


class TgUpdateBotMsgRepo(BotMsgRepo):
    def __init__(self, update: Message):
        self.update = update

    async def send_audio(self, audio: TgAudio) -> None:
        await self.update.reply_audio(
            audio=audio.audio,
            performer=audio.artist,
            title=audio.title,
            thumbnail=audio.cover,
            duration=audio.duration,
            filename=audio.filename,
        )

    async def send_text(self, text: str) -> None:
        await self.update.reply_html(text)

    async def send_photo(self, photo: bytes, caption: str = None) -> None:
        await self.update.reply_photo(
            photo=photo,
            caption=caption,
        )

    async def send_multiple_audio(self, audios: List[TgAudio]) -> None:
        """Отправляет несколько аудио файлов с прогрессом"""
        if not audios:
            return
            
        total = len(audios)
        await self.send_text(f"Найдено {total} треков. Отправляю...")
        
        for i, audio in enumerate(audios, 1):
            try:
                await self.send_audio(audio)
            except Exception as e:
                await self.send_text(f"❌ Ошибка при отправке {i}/{total}: {str(e)}")
        
        await self.send_text(f"🎵 Отправлено {total} треков!")

    async def send_audio_group(self, audios: List[TgAudio]) -> None:
        """Пытается отправить аудио как медиагруппу (может не работать)"""
        if not audios:
            return
            
        try:
            # Создаем медиагруппу из аудио файлов
            media_group = []
            for audio in audios:
                media = InputMediaAudio(
                    media=audio.audio,
                    performer=audio.artist,
                    title=audio.title,
                    thumbnail=audio.cover,
                    duration=audio.duration,
                    filename=audio.filename,
                )
                media_group.append(media)
            
            # Отправляем медиагруппу
            await self.update.reply_media_group(media=media_group)

        except Exception as e:
            # Если медиагруппа не работает, fallback на обычную отправку
            await self.send_text("Медиагруппа не поддерживается, отправляю по одному...")
            await self.send_multiple_audio(audios)


class TgBotMsgRepo(BotMsgRepo):
    """Реализация BotMsgRepo для отправки уведомлений через python-telegram-bot"""

    def __init__(self, bot: Bot, chat_ids: List[int]):
        self.bot = bot
        self.chat_ids = chat_ids

    async def send_audio(self, audio: TgAudio) -> None:
        """Отправляет аудио во все указанные чаты"""
        for chat_id in self.chat_ids:
            try:
                await self.bot.send_audio(
                    chat_id=chat_id,
                    audio=audio.audio,
                    performer=audio.artist,
                    title=audio.title,
                    thumbnail=audio.cover,
                    duration=audio.duration,
                    filename=audio.filename,
                )
            except Exception as e:
                print(f"❌ Ошибка отправки аудио в чат {chat_id}: {e}")
                raise

    async def send_text(self, text: str) -> None:
        """Отправляет текст во все указанные чаты"""
        for chat_id in self.chat_ids:
            try:
                await self.bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode="HTML"
                )
                print(f"✅ Сообщение отправлено в чат {chat_id}")
            except Exception as e:
                print(f"❌ Ошибка отправки в чат {chat_id}: {e}")
                raise

    async def send_photo(self, photo: bytes, caption: str = None) -> None:
        """Отправляет фото во все указанные чаты"""
        for chat_id in self.chat_ids:
            try:
                await self.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=caption,
                    parse_mode="HTML" if caption else None
                )
            except Exception as e:
                print(f"❌ Ошибка отправки фото в чат {chat_id}: {e}")
                raise

    async def send_multiple_audio(self, audios: List[TgAudio]) -> None:
        """Отправляет несколько аудио файлов с прогрессом во все чаты"""
        if not audios:
            return

        total = len(audios)
        await self.send_text(f"Найдено {total} треков. Отправляю...")

        for i, audio in enumerate(audios, 1):
            try:
                await self.send_audio(audio)
            except Exception as e:
                await self.send_text(f"❌ Ошибка при отправке {i}/{total}: {str(e)}")

        await self.send_text(f"🎵 Отправлено {total} треков!")

    async def send_audio_group(self, audios: List[TgAudio]) -> None:
        """Пытается отправить аудио как медиагруппу во все чаты"""
        if not audios:
            return

        try:
            # Создаем медиагруппу из аудио файлов
            from telegram import InputMediaAudio

            media_group = []
            for audio in audios:
                media = InputMediaAudio(
                    media=audio.audio,
                    performer=audio.artist,
                    title=audio.title,
                    thumbnail=audio.cover,
                    duration=audio.duration,
                    filename=audio.filename,
                )
                media_group.append(media)

            # Отправляем медиагруппу во все чаты
            for chat_id in self.chat_ids:
                try:
                    await self.bot.send_media_group(
                        chat_id=chat_id,
                        media=media_group
                    )
                except Exception as e:
                    print(f"❌ Ошибка отправки медиагруппы в чат {chat_id}: {e}")
                    # Fallback на обычную отправку для этого чата
                    for audio in audios:
                        await self.bot.send_audio(
                            chat_id=chat_id,
                            audio=audio.audio,
                            performer=audio.artist,
                            title=audio.title,
                            thumbnail=audio.cover,
                            duration=audio.duration,
                            filename=audio.filename,
                        )

        except Exception as e:
            # Если медиагруппа не работает, fallback на обычную отправку
            await self.send_text("Медиагруппа не поддерживается, отправляю по одному...")
            await self.send_multiple_audio(audios)
