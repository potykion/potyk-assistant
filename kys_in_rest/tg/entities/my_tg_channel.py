from pydantic import BaseModel


class MyTgChannel(BaseModel):
    name: str
    link: str