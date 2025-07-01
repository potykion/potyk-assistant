import abc

from kys_in_rest.tg.entities.audio import TgAudio


class BotMsgRepo(abc.ABC):
    @abc.abstractmethod
    def send_audio(self, audio: TgAudio):
        raise NotImplementedError()

    @abc.abstractmethod
    def send_text(self, text: str):
        raise NotImplementedError()