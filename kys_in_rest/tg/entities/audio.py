import dataclasses


@dataclasses.dataclass
class TgAudio:
    audio: bytes
    artist: str
    title: str
    cover: bytes
    duration: int = 0

