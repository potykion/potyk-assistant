from pydantic import BaseModel


class Tag(BaseModel):
    id: int
    title: str
    entity_type: str


class TagM2m(BaseModel):
    tag_id: int
    entity_id: int
    entity_type: str
