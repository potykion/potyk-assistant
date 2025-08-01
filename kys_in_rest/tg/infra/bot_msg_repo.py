from typing import Coroutine, Any, List

from telegram import Message, InputMediaAudio

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
