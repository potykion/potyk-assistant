import abc
from typing import Coroutine, Any, List

from kys_in_rest.tg.entities.audio import TgAudio


class BotMsgRepo(abc.ABC):
    @abc.abstractmethod
    def send_audio(self, audio: TgAudio) -> Coroutine[Any, Any, None]:
        raise NotImplementedError()

    @abc.abstractmethod
    def send_text(self, text: str) -> Coroutine[Any, Any, None]:
        raise NotImplementedError()

    @abc.abstractmethod
    def send_photo(self, photo: bytes, caption: str = None) -> Coroutine[Any, Any, None]:
        raise NotImplementedError()

    @abc.abstractmethod
    def send_multiple_audio(self, audios: List[TgAudio]) -> Coroutine[Any, Any, None]:
        """Отправляет несколько аудио файлов с прогрессом"""
        raise NotImplementedError()

    @abc.abstractmethod
    def send_audio_group(self, audios: List[TgAudio]) -> Coroutine[Any, Any, None]:
        """Пытается отправить аудио как медиагруппу (может не работать)"""
        raise NotImplementedError()
