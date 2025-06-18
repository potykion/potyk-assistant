import datetime

from pydantic import BaseModel


class WishlistItem(BaseModel):
    name: str
    received: datetime.datetime | None = None
