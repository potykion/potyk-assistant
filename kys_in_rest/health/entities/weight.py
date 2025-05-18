import datetime

from pydantic import BaseModel, Field


class WeightEntry(BaseModel):
    weight: float
    date: datetime.date = Field(default_factory=datetime.date.today)
