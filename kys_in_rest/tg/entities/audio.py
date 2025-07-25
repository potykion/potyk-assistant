import dataclasses


@dataclasses.dataclass
class TgAudio:
    audio: bytes
    artist: str | None = None
    title: str | None = None
    cover: bytes | None = None
    duration: int = 0

