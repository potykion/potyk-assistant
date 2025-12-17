from pydantic import BaseModel


class Movie(BaseModel):
    id: int | None = None
    title: str | None = None
    image: str | None = None
    kinopoisk_url: str | None = None
    download_url: str | None = None
    watch_url: str | None = None
    why: str | None = None



