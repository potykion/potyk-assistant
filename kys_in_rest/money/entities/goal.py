import datetime
import decimal

from pydantic import BaseModel

from kys_in_rest.core.tg_utils import TgFeature


class MoneyGoal(BaseModel):
    due_date: datetime.date
    val: decimal.Decimal
    category: str
