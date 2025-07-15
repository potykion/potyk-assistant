from pydantic import BaseModel

from kys_in_rest.core.zen_money import ZenMoneyDiffRaw


class ZenMoneyDiff(BaseModel):
    server_timestamp: int
    diff: ZenMoneyDiffRaw
