from typing import TypedDict


class Restaurant(TypedDict):
    name: str
    yandex_maps: str
    tags: str
    city: str
    metro: str
    prices: str
    rating: int | None
    comment: str
    date_created: str
    telegram: str
    site: str
    owner: str
    chief: str
    visited: str
    from_channel: str
    from_post: str
