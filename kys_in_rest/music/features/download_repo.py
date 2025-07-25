import abc

from kys_in_rest.tg.entities.audio import TgAudio


class DownloadRepo(abc.ABC):
    @abc.abstractmethod
    def download_audio_from_url(
        self,
        url: str,
        artist: str | None = None,
        album: str | None = None,
    ) -> list[TgAudio]: ...
