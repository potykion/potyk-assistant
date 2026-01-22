from pydantic import BaseModel


class Album(BaseModel):
    id: int | None = None
    title: str
    artist: str
    year: int
    cover: str
    link: str | None
