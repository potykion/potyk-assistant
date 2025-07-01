from typing import Coroutine, Any

from telegram import Message

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
        )

    async def send_text(self, text: str) -> None:
        await self.update.reply_text(text)
