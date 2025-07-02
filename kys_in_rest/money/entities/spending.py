import decimal
from datetime import datetime

from pydantic import BaseModel, Field


class Spending(BaseModel):
    created_dt: datetime = Field(default_factory=datetime.now)
    amount: decimal.Decimal
    comment: str
