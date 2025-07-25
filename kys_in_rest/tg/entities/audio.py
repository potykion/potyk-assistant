import dataclasses


@dataclasses.dataclass
class TgAudio:
    audio: bytes
    artist: str | None = None
    title: str | None = None
    cover: bytes | None = None
    duration: int = 0

    @property
    def filename(self):
        if self.artist and self.title:
            return f"{self.artist} - {self.title}"
        else:
            return "audio"
