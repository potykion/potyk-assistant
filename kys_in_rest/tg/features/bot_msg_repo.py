import abc
from typing import Coroutine, Any

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
